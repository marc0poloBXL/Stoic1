"""
Instagram DM Automation — Meta Graph API
=========================================
Production-ready script using ONLY the official Meta Graph API.
No scraping, no Selenium, no unofficial libraries.

Requirements:
    pip install requests flask python-dotenv

Setup:
    1. Create .env file with:
        IG_BUSINESS_ID=17841438935909153
        PAGE_ACCESS_TOKEN=EA...
    2. Run webhook:  python instagram_dm.py webhook
    3. Send DM:      python instagram_dm.py send --user-id=<ig_id> --text="Hello"
"""

import os
import hmac
import hashlib
import logging
from typing import Optional
from dataclasses import dataclass
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()

API_VERSION = "v26.0"
GRAPH_API = f"https://graph.facebook.com/{API_VERSION}"

IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")       # e.g. "17841438935909153"
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")  # the EA... token
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")   # for webhook signature verification
WEBHOOK_VERIFY_TOKEN = os.getenv("WEBHOOK_VERIFY_TOKEN", "my-verify-token")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

@dataclass
class IncomingMessage:
    """A DM sent by a user to your Instagram Business account."""
    sender_id: str          # Instagram-scoped user ID (IGID)
    sender_username: str    # Instagram @username (if available)
    message_text: str       # The text they sent
    conversation_id: str    # Conversation thread ID
    timestamp: int          # Unix timestamp in milliseconds
    mid: str                # Message ID (for deduplication)

# ---------------------------------------------------------------------------
# 1. Send a DM
# ---------------------------------------------------------------------------

def send_text_dm(
    recipient_igid: str,
    message_text: str,
    business_id: str = IG_BUSINESS_ID,
    token: str = PAGE_ACCESS_TOKEN,
) -> dict:
    """
    Send a plain text DM via the Instagram Messaging API.

    https://developers.facebook.com/docs/messenger-platform/instagram/features/send-message

    Args:
        recipient_igid: The Instagram-scoped user ID (IGID) of the recipient.
        message_text:  The message body.
        business_id:   Your Instagram Business Account ID.
        token:         A valid Page Access Token.

    Returns:
        The API response JSON (includes `message_id` on success).
    """
    url = f"{GRAPH_API}/{business_id}/messages"

    payload = {
        "recipient": {"id": recipient_igid},
        "message": {"text": message_text},
        "access_token": token,
    }

    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        raise RuntimeError(f"Instagram API error: {data['error']['message']}")

    log.info("DM sent to %s: message_id=%s", recipient_igid, data.get("message_id"))
    return data


def send_dm_with_link(
    recipient_igid: str,
    message_text: str,
    link_url: str,
    button_label: str = "Open link",
    business_id: str = IG_BUSINESS_ID,
    token: str = PAGE_ACCESS_TOKEN,
) -> dict:
    """
    Send a DM with a tappable link button.

    Instagram messages support up to 2 buttons.
    OpenReply uses this pattern for tracked links.
    """
    url = f"{GRAPH_API}/{business_id}/messages"

    payload = {
        "recipient": {"id": recipient_igid},
        "message": {
            "text": message_text,
            "buttons": [
                {
                    "type": "web_url",
                    "url": link_url,
                    "title": button_label[:20],  # Max 20 chars
                }
            ],
        },
        "access_token": token,
    }

    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        raise RuntimeError(f"Instagram API error: {data['error']['message']}")

    log.info("DM with link sent to %s: message_id=%s", recipient_igid, data.get("message_id"))
    return data


# ---------------------------------------------------------------------------
# 2. Look up a user by Instagram username
# ---------------------------------------------------------------------------

def lookup_user_by_username(
    username: str,
    business_id: str = IG_BUSINESS_ID,
    token: str = PAGE_ACCESS_TOKEN,
) -> Optional[str]:
    """
    Find an Instagram user's IGID (Instagram-scoped ID) by @username.

    Meta restricts this endpoint — it only works for users who have
    interacted with your business account (commented, sent a DM, etc.).
    Returns None if the user isn't found or hasn't interacted.
    """
    url = f"{GRAPH_API}/{business_id}/conversations"
    params = {
        "fields": "participants{id,username}",
        "access_token": token,
    }

    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    for conversation in data.get("data", []):
        for participant in conversation.get("participants", {}).get("data", []):
            if participant.get("username") == username:
                return participant["id"]

    return None


def get_user_info(
    igid: str,
    token: str = PAGE_ACCESS_TOKEN,
) -> dict:
    """
    Get basic info about an Instagram user by their IGID.

    Only works for users who have interacted with your business account
    (within the 24-hour messaging window).
    """
    url = f"{GRAPH_API}/{igid}"
    params = {
        "fields": "id,username,name,profile_pic",
        "access_token": token,
    }

    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# 3. Webhook receiver (Flask)
# ---------------------------------------------------------------------------

def verify_webhook_signature(
    payload_body: bytes,
    signature_header: str,
    app_secret: str,
) -> bool:
    """
    Verify that a webhook payload was genuinely sent by Meta.

    Meta signs each POST with HMAC-SHA256 of the raw body using your
    App Secret. Always verify — it prevents fake events from reaching
    your logic.
    """
    if not signature_header:
        return False

    expected = hmac.new(
        app_secret.encode("utf-8"),
        payload_body,
        hashlib.sha256,
    ).hexdigest()

    # Meta prefixes the signature with "sha256="
    received = signature_header.replace("sha256=", "")
    return hmac.compare_digest(expected, received)


def parse_incoming_dm(payload: dict) -> Optional[IncomingMessage]:
    """
    Extract an incoming DM from a webhook payload.

    Instagram webhook payload structure:
    {
        "entry": [{
            "id": "...",        // IG Business Account ID (user_id)
            "time": 1234567890,
            "changes": [{
                "field": "messages",
                "value": {
                    "sender": {"id": "..."},
                    "message": {"text": "..."},
                    "conversation": {"id": "..."},
                    ...
                }
            }]
        }]
    }
    """
    try:
        entry = payload.get("entry", [])[0]
        change = entry.get("changes", [])[0]

        if change.get("field") != "messages":
            return None

        value = change.get("value", {})
        message = value.get("message", {})

        # Handle both new messages and existing thread messages
        sender = value.get("from", value.get("sender", {}))

        msg = IncomingMessage(
            sender_id=str(sender.get("id")),
            sender_username=str(sender.get("username", "")),
            message_text=message.get("text", ""),
            conversation_id=str(value.get("conversation", {}).get("id", "")),
            timestamp=entry.get("time", 0),
            mid=str(message.get("mid", "")),
        )

        return msg
    except (IndexError, KeyError, AttributeError):
        return None


def create_flask_app():
    """
    Create a Flask app with webhook endpoints for Instagram DM events.

    Run with:
        python instagram_dm.py webhook

    Or with gunicorn:
        gunicorn instagram_dm:app --bind 0.0.0.0:5000
    """
    from flask import Flask, request, abort

    app = Flask(__name__)

    @app.route("/webhook", methods=["GET"])
    def verify():
        """
        Meta sends a GET request to verify your webhook when you
        configure it in the Meta App Dashboard.

        The challenge response proves your server is alive.
        """
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == WEBHOOK_VERIFY_TOKEN:
            log.info("Webhook verified successfully!")
            return challenge, 200

        abort(403)

    @app.route("/webhook", methods=["POST"])
    def receive():
        """
        Receive incoming Instagram events (messages, comments).

        Always verify the HMAC signature when APP_SECRET is set.
        """
        raw_body = request.get_data()

        # Verify HMAC signature (recommended)
        if APP_SECRET:
            sig = request.headers.get("X-Hub-Signature-256", "")
            if not verify_webhook_signature(raw_body, sig, APP_SECRET):
                log.warning("Invalid webhook signature — rejecting")
                abort(401)

        payload = request.get_json()
        if not payload:
            abort(400)

        log.debug("Webhook received: %s", payload)

        # Parse the incoming DM
        msg = parse_incoming_dm(payload)

        if msg:
            log.info(
                "DM from %s (%s): \"%s\"",
                msg.sender_username or msg.sender_id,
                msg.sender_id,
                msg.message_text,
            )

            # ================================================================
            # YOUR CUSTOM LOGIC HERE
            # ================================================================
            #
            # Examples:
            #   1. Auto-reply to keyword matches
            #   2. Route by sign name (Aries → Aries wisdom)
            #   3. Trigger a follow-up campaign
            #   4. Log to database
            #
            # Example auto-reply:
            #
            #   if msg.message_text.lower() in ("hello", "hi"):
            #       send_text_dm(msg.sender_id, "Hey there! 👋")
            #
            # ================================================================

            # Placeholder: acknowledge receipt
            log.info("Processed message from %s", msg.sender_id)

        # Always return 200 — Meta will retry otherwise
        return "OK", 200

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return {"status": "ok"}

    return app


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Instagram DM Automation")
    sub = parser.add_subparsers(dest="command")

    # webhook command
    webhook_parser = sub.add_parser("webhook", help="Run the webhook server")
    webhook_parser.add_argument("--port", type=int, default=5000)
    webhook_parser.add_argument("--host", default="0.0.0.0")

    # send command
    send_parser = sub.add_parser("send", help="Send a DM")
    send_parser.add_argument("--user-id", required=True, help="Recipient IGID")
    send_parser.add_argument("--text", required=True, help="Message text")
    send_parser.add_argument("--link", help="Optional link URL")

    # lookup command
    lookup_parser = sub.add_parser("lookup", help="Look up a user by @username")
    lookup_parser.add_argument("username", help="Instagram username (without @)")

    args = parser.parse_args()

    if args.command == "webhook":
        app = create_flask_app()
        log.info("Starting webhook server on %s:%s", args.host, args.port)
        app.run(host=args.host, port=args.port, debug=False)

    elif args.command == "send":
        if not PAGE_ACCESS_TOKEN:
            log.error("PAGE_ACCESS_TOKEN not set in .env")
            return

        if args.link:
            result = send_dm_with_link(args.user_id, args.text, args.link)
        else:
            result = send_text_dm(args.user_id, args.text)

        log.info("Result: %s", result)

    elif args.command == "lookup":
        if not PAGE_ACCESS_TOKEN:
            log.error("PAGE_ACCESS_TOKEN not set in .env")
            return

        igid = lookup_user_by_username(args.username)
        if igid:
            log.info("User @%s has IGID: %s", args.username, igid)
        else:
            log.info("User @%s not found (may not have interacted yet)", args.username)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()