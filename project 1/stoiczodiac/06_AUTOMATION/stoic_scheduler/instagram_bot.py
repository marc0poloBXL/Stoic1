"""
Instagram bot for the Stoic Scheduler.
Uses Playwright to automate posting single images to Instagram feed.
"""

import os
import time
from pathlib import Path

from logger import setup_logger
from login_manager import LoginManager

logger = setup_logger(__name__)

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class InstagramBot:
    """Playwright-powered Instagram poster for single-image feed posts."""

    def __init__(self, config: dict, username: str, password: str, totp_secret: str = ""):
        self.config = config
        self.username = username
        self.password = password
        self.totp_secret = totp_secret
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """Launch the Playwright browser and set up the page."""
        from playwright.async_api import async_playwright

        self._playwright = await async_playwright().start()

        browser_cfg = self.config["browser"]
        cookies_dir = Path(browser_cfg["cookies_dir"])
        cookies_dir.mkdir(parents=True, exist_ok=True)

        self.browser = await self._playwright.chromium.launch(
            headless=browser_cfg.get("headless", True),
            slow_mo=browser_cfg.get("slow_mo", 300),
        )

        self.context = await self.browser.new_context(
            viewport={
                "width": browser_cfg.get("viewport_width", 1280),
                "height": browser_cfg.get("viewport_height", 720),
            },
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        self.page = await self.context.new_page()
        self.page.set_default_timeout(browser_cfg.get("timeout", 30000))

    async def ensure_logged_in(self) -> bool:
        """Ensure we're logged in, restoring session or logging in fresh."""
        login_manager = LoginManager(
            page=self.page,
            context=self.context,
            config=self.config,
            totp_secret=self.totp_secret,
        )

        # Both methods are async — awaiting is required. Without it the
        # coroutine object is always truthy and the bot skips login entirely.
        if await login_manager.load_session():
            return True

        if not self.username or not self.password:
            logger.error("No Instagram credentials configured. Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in .env")
            return False

        return await login_manager.login_fresh(self.username, self.password)

    async def post_image(self, image_path: Path, caption: str = "") -> bool:
        """
        Post a single image to the Instagram feed.

        Args:
            image_path: Path to the image file (PNG/JPG)
            caption: Optional caption text

        Returns:
            True if the post was successful, False otherwise.
        """
        # Validate image
        if not image_path.exists():
            logger.error(f"Image not found: {image_path}")
            return False

        if HAS_PIL:
            try:
                img = Image.open(image_path)
                img.verify()
                logger.info(f"Image validated: {image_path.name} ({img.size[0]}x{img.size[1]})")
            except Exception as e:
                logger.error(f"Image validation failed: {image_path} — {e}")
                return False

        try:
            # Navigate to Instagram
            await self.page.goto("https://www.instagram.com/", wait_until="domcontentloaded")
            time.sleep(2)

            # Click the "+" (Create) button
            logger.info("Clicking Create button...")
            create_button = self.page.locator("svg[aria-label='New post'], svg[aria-label='Create']")
            await create_button.first.click(timeout=10000)
            time.sleep(1.5)

            # Click "Post" from the menu
            post_option = self.page.locator("span:has-text('Post'), div[role='button']:has-text('Post')")
            await post_option.first.click(timeout=5000)
            time.sleep(1)

            # File input: select the image
            logger.info(f"Selecting image: {image_path.name}")
            file_input = self.page.locator("input[type='file']")
            await file_input.set_input_files(str(image_path.absolute()))
            time.sleep(3)

            # Click "Next" after image preview loads
            next_button = self.page.locator("div[role='button']:has-text('Next')")
            await next_button.first.click(timeout=15000)
            time.sleep(2)

            # If there's a second "Next" (crop/adjust step), click it too
            try:
                next_button_2 = self.page.locator("div[role='button']:has-text('Next')")
                if await next_button_2.is_visible(timeout=3000):
                    await next_button_2.first.click()
                    time.sleep(1.5)
            except Exception:
                pass

            # Write caption
            if caption:
                logger.info("Writing caption...")
                caption_area = self.page.locator("div[aria-label='Write a caption...']")
                await caption_area.first.click()
                time.sleep(0.5)
                await caption_area.first.fill(caption)
                time.sleep(1)

            # Click "Share"
            logger.info("Clicking Share...")
            share_button = self.page.locator("div[role='button']:has-text('Share')")
            await share_button.first.click(timeout=10000)

            # Wait for success confirmation
            time.sleep(4)

            # Check if post was successful by looking for confirmation
            success = await self._confirm_post_success()
            if success:
                logger.info(f"✅ Posted: {image_path.name}")
            else:
                logger.warning(f"⚠️ Post may have failed: {image_path.name}")

            return success

        except Exception as e:
            logger.error(f"Post failed: {e}")
            # Take screenshot for debugging
            try:
                screenshot_path = f"logs/error_{Path(image_path).stem}_{int(time.time())}.png"
                await self.page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"Screenshot saved to {screenshot_path}")
            except Exception:
                pass
            return False

    async def _confirm_post_success(self) -> bool:
        """Check if the post was shared successfully."""
        try:
            # Wait for the post to appear — look for the create button again
            # (meaning we're back on the feed after posting)
            await self.page.wait_for_selector(
                "svg[aria-label='New post'], svg[aria-label='Create']",
                timeout=15000,
            )
            return True
        except Exception:
            # Also check for success toast
            try:
                toast = self.page.locator("text=Your post has been shared")
                if await toast.is_visible(timeout=5000):
                    return True
            except Exception:
                pass
            return False

    async def close(self):
        """Close the browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self._playwright:
            await self._playwright.stop()