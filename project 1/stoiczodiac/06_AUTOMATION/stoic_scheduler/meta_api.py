"""
Meta Graph API client for the Stoic Scheduler.
Handles Instagram content publishing via Meta's official API:
- Carousels (multi-image posts)
- Reels (video)
- Stories (image)
- Optional single-image post via API
"""

import asyncio
import os
from typing import Dict, List, Optional, Tuple

from logger import setup_logger

logger = setup_logger(__name__)


class MetaClient:
    """
    Meta Graph API client for publishing content to an Instagram
    Business/Creator account linked to a Facebook Page.
    """

    BASE = "https://graph.facebook.com"

    def __init__(
        self,
        config: dict,
        app_id: str = "",
        app_secret: str = "",
        page_token: str = "",
        ig_user_id: str = "",
    ):
        self.api_version = config.get("meta", {}).get("api_version", "v20.0")
        self.base_url = f"{self.BASE}/{self.api_version}"
        self.app_id = app_id or os.getenv("META_APP_ID", "")
        self.app_secret = app_secret or os.getenv("META_APP_SECRET", "")
        self.page_token = page_token or os.getenv("META_PAGE_ACCESS_TOKEN", "")
        self.ig_user_id = ig_user_id or os.getenv("META_IG_USER_ID", "")

    @property
    def is_configured(self) -> bool:
        """Check if Meta API credentials are present."""
        return bool(self.page_token and self.ig_user_id)

    async def verify_access(self) -> Tuple[bool, str]:
        """
        Verify that the page token and IG user ID are valid.
        Returns (is_valid, message).
        """
        if not self.page_token:
            return False, "META_PAGE_ACCESS_TOKEN not set"
        if not self.ig_user_id:
            return False, "META_IG_USER_ID not set; run with --meta-resolve to auto-detect"

        try:
            resp = await self._get(f"/{self.ig_user_id}", {
                "fields": "id,username,name",
                "access_token": self.page_token,
            })
            username = resp.get("username", "unknown")
            return True, f"Access OK — @{username} (id: {self.ig_user_id})"
        except Exception as e:
            return False, f"Verification failed: {e}"

    async def resolve_ig_user_id(self) -> Optional[str]:
        """
        Resolve the Instagram Business Account ID from the page access token.
        Calls GET /me/accounts → finds the page → GET /{page_id}?fields=instagram_business_account.
        Returns the IG user ID string or None.
        """
        try:
            # Get pages accessible with this token
            pages = await self._get("/me/accounts", {
                "access_token": self.page_token,
                "fields": "id,name,instagram_business_account,username",
            })
            paging = pages.get("data", [])
            if not paging:
                logger.warning("No Facebook Pages found. Make sure the token has a linked Page.")
                return None

            for page in paging:
                ig = page.get("instagram_business_account")
                if ig:
                    ig_id = ig["id"]
                    logger.info(f"Found IG Business Account: {ig_id} (Page: {page.get('name')})")
                    return str(ig_id)

            # Fallback: no IG linked — show pages owned
            names = [p.get("name", "?") for p in paging]
            logger.warning(
                f"None of your Pages ({', '.join(names)}) are linked to an Instagram account. "
                "Go to Instagram Settings → switch to Professional → link your Facebook Page."
            )
            return None
        except Exception as e:
            logger.error(f"Failed to resolve IG user ID: {e}")
            return None

    # ------------------------------------------------------------------ #
    #  Public posting methods
    # ------------------------------------------------------------------ #

    async def post_image(self, image_url: str, caption: str = "") -> bool:
        """Post a single image via the Graph API (optional; browser is default)."""
        return await self._create_and_publish({
            "image_url": image_url,
            "caption": caption,
        })

    async def post_carousel(self, image_urls: List[str], caption: str = "") -> bool:
        """Post a carousel (multi-image). Upload slides, then publish."""
        if not image_urls:
            logger.error("Carousel requires at least one image")
            return False

        # Step 1: Create child containers for each image
        child_ids = []
        for url in image_urls:
            ok, container = await self._create_container({
                "image_url": url,
                "is_carousel_item": "true",
            })
            if not ok:
                logger.error(f"Carousel child container creation failed for {url}")
                return False
            child_ids.append(container["id"])

        # Wait for all children to be ready
        for cid in child_ids:
            if not await self._wait_for_container(cid):
                logger.error(f"Carousel child container {cid} never finished")
                return False

        # Step 2: Create the carousel container
        return await self._create_and_publish({
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "caption": caption,
        })

    async def post_reel(
        self,
        video_url: str,
        caption: str = "",
        cover_url: str = "",
    ) -> bool:
        """Post a reel (video). Optional cover image URL."""
        params = {
            "media_type": "REELS",
            "video_url": video_url,
            "share_to_feed": "true",
        }
        if caption:
            params["caption"] = caption
        if cover_url:
            params["cover_url"] = cover_url
        return await self._create_and_publish(params)

    async def post_story(self, image_url: str, caption: str = "") -> bool:
        """Post a story (image only)."""
        params = {
            "media_type": "STORIES",
            "image_url": image_url,
        }
        # Note: captions on stories via API are unsupported for STORIES type
        return await self._create_and_publish(params)

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    async def _create_and_publish(self, params: Dict) -> bool:
        """Create a media container, wait for it, then publish."""
        ok, container = await self._create_container(params)
        if not ok:
            return False

        cid = container["id"]

        # Wait for processing
        if not await self._wait_for_container(cid):
            return False

        # Publish
        return await self._publish(cid)

    async def _create_container(self, params: Dict) -> Tuple[bool, Optional[Dict]]:
        """Create a media container. Returns (ok, response_body)."""
        try:
            params["access_token"] = self.page_token
            resp = await self._post(f"/{self.ig_user_id}/media", params)
            if "id" in resp:
                logger.info(f"Container created: id={resp['id']}")
                return True, resp
            error = resp.get("error", {}).get("message", str(resp))
            logger.error(f"Container creation failed: {error}")
            return False, None
        except Exception as e:
            logger.error(f"Container creation exception: {e}")
            return False, None

    async def _wait_for_container(self, container_id: str) -> bool:
        """Poll container status until FINISHED or timeout."""
        for attempt in range(15):  # ~75 seconds max
            try:
                resp = await self._get(f"/{container_id}", {
                    "fields": "status_code",
                    "access_token": self.page_token,
                })
                status = resp.get("status_code", "UNKNOWN")
                if status == "FINISHED":
                    logger.info(f"Container {container_id} → FINISHED")
                    return True
                if status in ("ERROR", "EXPIRED"):
                    error_msg = resp.get("error_message", status)
                    logger.error(f"Container {container_id} failed: {error_msg}")
                    return False
                logger.debug(f"Container {container_id} → {status} (attempt {attempt + 1})")
            except Exception as e:
                logger.warning(f"Status poll failed for {container_id}: {e}")
            await asyncio.sleep(5)
        logger.warning(f"Container {container_id} timed out after 75s")
        return False

    async def _publish(self, container_id: str) -> bool:
        """Publish a media container."""
        try:
            resp = await self._post(f"/{self.ig_user_id}/media_publish", {
                "creation_id": container_id,
                "access_token": self.page_token,
            })
            media_id = resp.get("id")
            if media_id:
                logger.info(f"✅ Published! Media ID: {media_id}")
                return True
            error = resp.get("error", {}).get("message", str(resp))
            logger.error(f"Publish failed: {error}")
            return False
        except Exception as e:
            logger.error(f"Publish exception: {e}")
            return False

    # ------------------------------------------------------------------ #
    #  HTTP helpers
    # ------------------------------------------------------------------ #

    async def _get(self, path: str, params: Dict = None) -> Dict:
        """Make an async GET request to the Graph API."""
        return await self._request("GET", path, params=params)

    async def _post(self, path: str, data: Dict = None) -> Dict:
        """Make an async POST request to the Graph API."""
        return await self._request("POST", path, data=data)

    async def _request(self, method: str, path: str, **kwargs) -> Dict:
        """Generic async HTTP request via httpx."""
        import httpx
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            if method == "GET":
                resp = await client.get(url, params=kwargs.get("params", {}))
            else:
                resp = await client.post(url, data=kwargs.get("data", {}))
            resp.raise_for_status()
            return resp.json()