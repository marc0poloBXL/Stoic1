#!/usr/bin/env python
"""
Stoic Scheduler — Instagram Auto-Poster

A self-hosted tool that posts images, carousels, reels, and stories
to Instagram. Single images go through Playwright browser automation;
carousels, reels, and stories go through the Meta Graph API.

Usage:
    python scheduler.py                  # Normal run (check queue, post if time)
    python scheduler.py --dry-run        # Preview everything in the queue
    python scheduler.py --post-now       # Force post next item immediately
    python scheduler.py --import-only    # Import all content from batch folders
    python scheduler.py --status         # Show queue status
    python scheduler.py --meta-verify    # Check Meta API access
    python scheduler.py --validate-config  # Check config and quit
"""

import argparse
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Windows consoles default to cp1252, which can't encode emoji in output.
if sys.platform == "win32":
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

# Load .env file before anything else
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(str(env_path))
except ImportError:
    pass


def load_config() -> dict:
    """Load and return the YAML configuration."""
    import yaml

    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        print(f"❌ Config not found: {config_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    script_dir = Path(__file__).parent
    for key in ["folder", "posted_folder", "failed_folder", "cookies_dir"]:
        for section in ["queue", "browser"]:
            if section in config and key in config[section]:
                val = config[section][key]
                if isinstance(val, str) and not os.path.isabs(val):
                    config[section][key] = str((script_dir / val).resolve())

    return config


def validate_config(config: dict) -> bool:
    """Validate the configuration and report any issues."""
    ok = True

    for section in ["instagram", "schedule", "queue", "browser", "recovery"]:
        if section not in config:
            print(f"❌ Missing config section: {section}")
            ok = False

    schedule = config.get("schedule", {})
    times = schedule.get("times", {})
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        for slot in times.get(day, []):
            try:
                parts = slot.split(":")
                h, m = int(parts[0]), int(parts[1])
                if h < 0 or h > 23 or m < 0 or m > 59:
                    print(f"❌ Invalid time in schedule.{day}: {slot}")
                    ok = False
            except (ValueError, IndexError):
                print(f"❌ Invalid time format in schedule.{day}: {slot}")
                ok = False

    queue_config = config.get("queue", {})
    for dir_key in ["folder", "posted_folder", "failed_folder"]:
        dir_path = queue_config.get(dir_key, "")
        if dir_path:
            p = Path(dir_path)
            if not p.exists():
                print(f"  ⚠  Directory does not exist: {dir_path}")

    browser_config = config.get("browser", {})
    if browser_config.get("headless", True) is False:
        print("  ℹ  Browser set to VISIBLE mode (headless: false)")

    username = config.get("instagram", {}).get("username", "") or os.getenv("INSTAGRAM_USERNAME", "")
    password = os.getenv("INSTAGRAM_PASSWORD", "")
    if not username:
        print("  ⚠  Instagram username not set in config or INSTAGRAM_USERNAME env")
    if not password:
        print("  ⚠  Instagram password not set. Set INSTAGRAM_PASSWORD in .env file.")

    # Meta API check (optional — warn only if routing says api but no creds)
    meta = config.get("meta", {})
    for content_type in ["carousels", "reels", "stories"]:
        route = meta.get(f"route_{content_type}_via", "api")
        if route == "api":
            page_token = os.getenv("META_PAGE_ACCESS_TOKEN", "")
            ig_user_id = os.getenv("META_IG_USER_ID", "")
            blob_token = os.getenv("BLOB_READ_WRITE_TOKEN", "")
            if not page_token:
                print(f"  ⚠  {content_type} routed via API but META_PAGE_ACCESS_TOKEN not set")
                print(f"     Carousel/reel/story items will be skipped until set up.")
            if not blob_token:
                print(f"  ⚠  BLOB_READ_WRITE_TOKEN not set — required for media hosting")
            if not ig_user_id:
                print(f"  ℹ   META_IG_USER_ID not set — will auto-resolve on first post")

    if ok:
        print("✅ Config validation passed")

    return ok


async def post_next_item(config: dict):
    """Post the next item from the queue. Dispatches by content type."""
    from queue_handler import QueueHandler, QueueItem
    from instagram_bot import InstagramBot
    from meta_api import MetaClient
    from media_uploader import MediaUploader

    queue = QueueHandler(config)
    items = queue.scan_queue()

    queued_items = [i for i in items if i.status == "queued"]
    if not queued_items:
        logger.info("Queue is empty — checking batch folders...")
        imported = queue.auto_import()
        if imported:
            items = queue.scan_queue()
            queued_items = [i for i in items if i.status == "queued"]

    if not queued_items:
        logger.info("Nothing to post — queue is empty")
        return

    item = queued_items[0]
    logger.info(f"Posting: [{item.post_type}] {item.filename}")

    # Determine which poster to use
    meta_routing = config.get("meta", {})
    route_map = {
        "image": meta_routing.get("route_images_via", "browser"),
        "carousel": meta_routing.get("route_carousels_via", "api"),
        "reel": meta_routing.get("route_reels_via", "api"),
        "story": meta_routing.get("route_stories_via", "api"),
    }
    method = route_map.get(item.post_type, "browser")

    if method == "browser":
        # Playwright web automation (existing)
        username = (config.get("instagram", {}).get("username", "")
                    or os.getenv("INSTAGRAM_USERNAME", ""))
        password = os.getenv("INSTAGRAM_PASSWORD", "")
        totp_secret = os.getenv("INSTAGRAM_TOTP_SECRET", "")

        if not password:
            logger.error("INSTAGRAM_PASSWORD not set. Configure .env file first.")
            return

        bot = InstagramBot(config, username, password, totp_secret)
        try:
            await bot.start()
            if not await bot.ensure_logged_in():
                logger.error("Failed to authenticate. Check credentials or login manually.")
                return
            success = await bot.post_image(item.image_path, item.caption_text)
        finally:
            await bot.close()

    elif method == "api":
        # Meta Graph API + Vercel Blob
        meta = MetaClient(config)
        uploader = MediaUploader()

        if not meta.is_configured:
            logger.error(
                "Meta API not configured. Set META_PAGE_ACCESS_TOKEN "
                "and BLOB_READ_WRITE_TOKEN in .env"
            )
            return

        try:
            success = await _post_via_api(item, meta, uploader)
        except Exception as e:
            logger.error(f"API posting failed: {e}")
            success = False
    else:
        logger.error(f"Unknown routing method: {method}")
        return

    # Handle result: move to posted or retry/fail
    if success:
        queue.move_to_posted(item)
        # Clean up blobs (optional — comment out to keep for debugging)
        # Media cleanup happens automatically since URLs are ephemeral
    else:
        item.retry_count += 1
        max_retries = config.get("recovery", {}).get("max_retries", 3)
        if item.retry_count >= max_retries:
            queue.move_to_failed(item, f"Failed after {item.retry_count} retries")
        else:
            logger.warning(f"Post failed. Will retry ({item.retry_count}/{max_retries})")


async def _post_via_api(item, meta: "MetaClient", uploader: "MediaUploader") -> bool:
    """Post a carousel/reel/story via the Meta Graph API with Vercel Blob uploads."""

    if item.post_type == "carousel":
        # Upload slides to Vercel Blob
        urls = []
        for slide in item.slides:
            url = await uploader.upload_image(slide)
            urls.append(url)
        try:
            ok = await meta.post_carousel(urls, item.caption_text)
        finally:
            for url in urls:
                await uploader.delete_blob(url)
        return ok

    elif item.post_type == "reel":
        url = await uploader.upload_video(item.video_path)
        cover_url = ""
        try:
            ok = await meta.post_reel(url, item.caption_text, cover_url)
        finally:
            await uploader.delete_blob(url)
            if cover_url:
                await uploader.delete_blob(cover_url)
        return ok

    elif item.post_type == "story":
        url = await uploader.upload_story_image(item.image_path)
        try:
            ok = await meta.post_story(url, item.caption_text)
        finally:
            await uploader.delete_blob(url)
        return ok

    elif item.post_type == "image":
        # Single image via API (unused by default; browser is default route)
        url = await uploader.upload_image(item.image_path)
        try:
            ok = await meta.post_image(url, item.caption_text)
        finally:
            await uploader.delete_blob(url)
        return ok

    else:
        logger.error(f"Unknown post type: {item.post_type}")
        return False


async def verify_meta(config: dict):
    """Verify Meta API credentials and resolve IG user ID if missing."""
    from meta_api import MetaClient

    meta = MetaClient(config)
    if not meta.page_token:
        print("❌ META_PAGE_ACCESS_TOKEN not set in .env file.")
        print("   See META_SETUP_GUIDE.md for setup steps.")
        return

    # Verify access
    ok, msg = await meta.verify_access()
    print(f"  {'✅' if ok else '❌'} {msg}")
    if not ok:
        return

    # Resolve IG user ID
    ig_id = await meta.resolve_ig_user_id()
    if ig_id:
        print(f"  ✅ Resolved IG Business Account ID: {ig_id}")
        if not os.getenv("META_IG_USER_ID", ""):
            print(f"  ℹ   Add this to your .env file: META_IG_USER_ID={ig_id}")
    else:
        print("  ❌ Could not resolve IG Business Account ID.")
        print("     Make sure your Instagram is a Professional account")
        print("     linked to a Facebook Page.")

    # Check Blob token
    blob_token = os.getenv("BLOB_READ_WRITE_TOKEN", "")
    if blob_token:
        print(f"  ✅ BLOB_READ_WRITE_TOKEN is set")
    else:
        print("  ⚠  BLOB_READ_WRITE_TOKEN not set — carousel/reel/story posts will fail")


def main():
    """Main entry point for the Stoic Scheduler."""
    parser = argparse.ArgumentParser(
        description="Stoic Scheduler — Instagram Auto-Poster",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would post without posting")
    parser.add_argument("--post-now", action="store_true",
                        help="Force post the next item immediately")
    parser.add_argument("--import-only", action="store_true",
                        help="Import content from weekly batch folders into the queue")
    parser.add_argument("--status", action="store_true",
                        help="Show queue status and exit")
    parser.add_argument("--meta-verify", action="store_true",
                        help="Check Meta API credentials + resolve IG account ID")
    parser.add_argument("--validate-config", action="store_true",
                        help="Check configuration and exit")

    args = parser.parse_args()
    config = load_config()

    from logger import setup_logger
    global logger
    logger = setup_logger()

    if args.validate_config:
        validate_config(config)
        return

    if args.meta_verify:
        asyncio.run(verify_meta(config))
        return

    if args.status:
        from queue_handler import QueueHandler
        queue = QueueHandler(config)
        items = queue.scan_queue()
        print(queue.get_queue_summary(items))
        return

    if args.import_only:
        from queue_handler import QueueHandler
        queue = QueueHandler(config)
        imported = queue.auto_import()
        if imported:
            print(f"✅ Imported {imported} new item(s) to the queue")
        else:
            print("No new items to import")
        return

    if args.dry_run:
        from queue_handler import QueueHandler
        queue = QueueHandler(config)
        schedule = config.get("schedule", {})
        now = datetime.now()
        day_name = now.strftime("%A").lower()
        today_slots = schedule.get("times", {}).get(day_name, [])
        print(f"\n📅 Today ({now.strftime('%A, %Y-%m-%d')})")
        print(f"   Scheduled slots: {', '.join(today_slots) if today_slots else 'None'}")
        print(f"   Current time: {now.strftime('%H:%M')}")
        should_post, slot_info = queue.is_time_to_post(
            schedule, tolerance_minutes=schedule.get("tolerance_minutes", 2))
        print(f"   Time to post: {'✅ YES' if should_post else '❌ NO'} ({slot_info})")
        items = queue.scan_queue()
        if items:
            print(f"\n{queue.get_queue_summary(items)}")
            print(f"\n   Items due for image (browser): {sum(1 for i in items if i.post_type == 'image')}")
            print(f"   Items due for API (carousel/reel/story): {sum(1 for i in items if i.post_type != 'image')}")
            if any(i.post_type != "image" for i in items):
                print("   (API items require META_PAGE_ACCESS_TOKEN + BLOB_READ_WRITE_TOKEN)")
        else:
            print("\nQueue is empty.")
        print()
        return

    should_post = args.post_now
    if not should_post:
        schedule = config.get("schedule", {})
        from queue_handler import QueueHandler
        queue = QueueHandler(config)
        should_post, slot_info = queue.is_time_to_post(
            schedule, tolerance_minutes=schedule.get("tolerance_minutes", 2))
        logger.info(slot_info)

    if should_post:
        asyncio.run(post_next_item(config))
    else:
        logger.info("Not a scheduled posting time — exiting")


if __name__ == "__main__":
    main()