"""
Login manager for the Stoic Scheduler (async Playwright).
Handles Instagram authentication with cookie persistence and 2FA.
"""

import json
import os
import time
from pathlib import Path

from logger import setup_logger

logger = setup_logger(__name__)

try:
    import pyotp
    HAS_PYOTP = True
except ImportError:
    HAS_PYOTP = False


class LoginManager:
    """Handles Instagram login with cookie persistence and 2FA fallback (async)."""

    def __init__(self, page, context, config: dict, totp_secret: str = ""):
        self.page = page
        self.context = context
        self.config = config
        self.totp_secret = totp_secret
        self.cookies_dir = Path(config["browser"]["cookies_dir"])
        self.cookies_file = self.cookies_dir / "instagram_session.json"

    async def load_session(self) -> bool:
        """Try to load a saved session. Returns True if cookies were loaded."""
        if not self.cookies_file.exists():
            logger.info("No saved session found — will log in fresh")
            return False

        try:
            with open(self.cookies_file, "r") as f:
                cookies = json.load(f)

            if not cookies:
                logger.warning("Saved session file is empty")
                return False

            await self.context.add_cookies(cookies)

            # Verify the session is still valid
            await self.page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
            await self.page.wait_for_timeout(2000)

            if await self._is_logged_in():
                logger.info("Session restored from saved cookies")
                return True
            else:
                logger.info("Saved session expired — will re-authenticate")
                await self.page.goto(
                    "https://www.instagram.com/accounts/login/",
                    wait_until="domcontentloaded",
                )
                return False

        except Exception as e:
            logger.warning(f"Failed to load saved session: {e}")
            return False

    async def login_fresh(self, username: str, password: str) -> bool:
        """Perform a fresh Instagram login. Returns True if successful."""
        try:
            logger.info("Navigating to Instagram login...")
            await self.page.goto(
                "https://www.instagram.com/accounts/login/",
                wait_until="domcontentloaded",
            )
            await self.page.wait_for_timeout(2000)

            # Accept cookies popup if present
            await self._dismiss_cookies_popup()

            # Fill username
            logger.info("Filling login form...")
            username_input = self.page.locator("input[name='username']")
            await username_input.fill(username)
            await self.page.wait_for_timeout(1000)

            # Fill password
            password_input = self.page.locator("input[name='password']")
            await password_input.fill(password)
            await self.page.wait_for_timeout(500)

            # Click login button
            login_button = self.page.locator("button[type='submit']")
            await login_button.click()

            # Wait for navigation after login
            await self.page.wait_for_timeout(5000)

            # Detect and handle 2FA if challenge appears
            await self._handle_2fa_if_present()

            # Handle popups
            await self._dismiss_save_info_dialog()
            await self._dismiss_notifications_popup()

            if await self._is_logged_in():
                await self._save_session()
                logger.info("Login successful")
                return True
            else:
                logger.error("Login failed — check credentials")
                return False

        except Exception as e:
            logger.error(f"Login error: {e}")
            return False

    async def _is_logged_in(self) -> bool:
        """Check if the user is logged in by looking for feed indicators."""
        try:
            await self.page.wait_for_selector(
                "svg[aria-label='New post'], "
                "svg[aria-label='Home'], "
                "a[href='/direct/inbox/']",
                timeout=8000,
            )
            return True
        except Exception:
            return False

    async def _dismiss_cookies_popup(self):
        """Dismiss the Instagram cookies/terms popup if it appears."""
        try:
            accept_btn = self.page.locator("button:has-text('Allow all cookies')")
            if await accept_btn.is_visible(timeout=3000):
                await accept_btn.click()
                await self.page.wait_for_timeout(1000)
        except Exception:
            pass

    async def _handle_2fa_if_present(self) -> bool:
        """
        Check if a 2FA challenge is showing and handle it.
        Returns True if 2FA was handled, False if no challenge detected.
        """
        try:
            challenge = self.page.locator("text=Enter Your Security Code")
            if not await challenge.is_visible(timeout=5000):
                return False

            logger.info("2FA challenge detected")

            # Try auto-generating TOTP code if secret is configured
            if self.totp_secret and HAS_PYOTP:
                code = pyotp.TOTP(self.totp_secret).now()
                logger.info("Auto-generating 2FA code from TOTP secret")

                code_input = self.page.locator("input[name='verificationCode']")
                await code_input.fill(code)
                await self.page.wait_for_timeout(500)

                confirm_btn = self.page.locator("button:has-text('Confirm')")
                await confirm_btn.click()
                await self.page.wait_for_timeout(3000)
                logger.info("2FA code submitted automatically")
                return True

            # No TOTP configured — wait for manual entry
            logger.info("=" * 60)
            logger.info("2FA CODE REQUIRED")
            logger.info("Enter the 6-digit code from your authenticator app.")
            logger.info(f"Go to: {self.page.url}")
            logger.info("You have 120 seconds before this attempt times out.")
            logger.info("=" * 60)

            # Wait for user to enter code manually
            for _ in range(120):
                if await self._is_logged_in() or "/login" not in self.page.url:
                    logger.info("2FA challenge resolved")
                    return True
                try:
                    if not await self.page.locator(
                        "input[name='verificationCode']"
                    ).is_visible(timeout=2000):
                        await self.page.wait_for_timeout(1000)
                        if await self._is_logged_in():
                            logger.info("2FA challenge resolved after user input")
                            return True
                except Exception:
                    pass
                await self.page.wait_for_timeout(1000)

            logger.warning("2FA timed out after 120 seconds")
            return False

        except Exception as e:
            logger.warning(f"2FA check skipped: {e}")
            return False

    async def _dismiss_save_info_dialog(self):
        """Dismiss 'Save Your Login Info?' dialog."""
        try:
            no_btn = self.page.locator("button:has-text('Not Now')")
            if await no_btn.is_visible(timeout=3000):
                await no_btn.click()
                await self.page.wait_for_timeout(1000)
        except Exception:
            pass

    async def _dismiss_notifications_popup(self):
        """Dismiss 'Turn on Notifications' popup."""
        try:
            not_now = self.page.locator("button:has-text('Not Now')")
            if await not_now.is_visible(timeout=3000):
                await not_now.click()
                await self.page.wait_for_timeout(1000)
        except Exception:
            pass

    async def _save_session(self):
        """Save the current browser session cookies to disk."""
        try:
            self.cookies_dir.mkdir(parents=True, exist_ok=True)
            cookies = await self.context.cookies()
            with open(self.cookies_file, "w") as f:
                json.dump(cookies, f, indent=2)
            logger.info(f"Session saved to {self.cookies_file}")
        except Exception as e:
            logger.warning(f"Failed to save session: {e}")

    async def clear_session(self):
        """Delete saved cookie file. Forces fresh login next time."""
        if self.cookies_file.exists():
            self.cookies_file.unlink()
            logger.info("Saved session cleared")