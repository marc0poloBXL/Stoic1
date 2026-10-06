"""
Media uploader for the Stoic Scheduler.
Uploads local files to Vercel Blob for public HTTPS URLs,
then optionally cleans up after posting via Meta Graph API.
"""

import asyncio
import io
import os
from pathlib import Path

from logger import setup_logger

logger = setup_logger(__name__)

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class MediaUploader:
    """
    Uploads local media files to Vercel Blob → returns public HTTPS URL.
    Used by MetaClient to provide media URLs for the Graph API.
    """

    def __init__(self, blob_token: str = ""):
        self.token = blob_token or os.getenv("BLOB_READ_WRITE_TOKEN", "")

    @property
    def is_available(self) -> bool:
        """True if the BLOB_READ_WRITE_TOKEN is configured."""
        return bool(self.token)

    async def upload_image(self, file_path: Path, prefix: str = "stoic") -> str:
        """Upload an image (PNG/JPG) to Vercel Blob and return its public URL.
        Converts images to JPEG for platforms that require it (stories)."""
        from vercel_blob import put
        data = await self._read_file(file_path)
        pathname = f"{prefix}/{file_path.name}"
        # vercel_blob.put is synchronous — run it in a thread so awaiting
        # doesn't TypeError AND doesn't block the event loop.
        result = await asyncio.to_thread(put, pathname, data, {
            "access": "public",
            "token": self.token,
        })
        url = result["url"]
        logger.info(f"Uploaded {file_path.name} → {url}")
        return url

    async def upload_story_image(self, file_path: Path, prefix: str = "stoic") -> str:
        """
        Upload a story image, converting PNG → JPEG if needed.
        Instagram Graph API stories require JPEG format.
        """
        if not HAS_PIL:
            logger.warning("Pillow not available — uploading as-is (may fail for stories)")
            return await self.upload_image(file_path, prefix)

        suffix = file_path.suffix.lower()
        if suffix in (".jpg", ".jpeg"):
            return await self.upload_image(file_path, prefix)

        # Convert PNG → JPEG in-memory
        try:
            img = Image.open(file_path).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=95)
            buf.seek(0)
            jpg_name = file_path.stem + ".jpg"
            pathname = f"{prefix}/{jpg_name}"
            from vercel_blob import put
            result = await asyncio.to_thread(put, pathname, buf.getvalue(), {
                "access": "public",
                "token": self.token,
            })
            url = result["url"]
            logger.info(f"Uploaded {file_path.name} (converted to JPEG) → {url}")
            return url
        except Exception as e:
            logger.error(f"Failed to convert story image {file_path.name}: {e}")
            return await self.upload_image(file_path, prefix)

    async def upload_video(self, file_path: Path, prefix: str = "stoic") -> str:
        """Upload a video (MP4) to Vercel Blob and return its public URL."""
        return await self.upload_image(file_path, prefix)

    async def delete_blob(self, url: str):
        """Delete a blob from Vercel Blob after posting."""
        if not url or not self.token:
            return
        try:
            from vercel_blob import delete as _delete
            # Synchronous — run in a thread (see upload_image).
            await asyncio.to_thread(_delete, url, {"token": self.token})
            logger.info(f"Deleted blob: {url}")
        except Exception as e:
            logger.warning(f"Failed to delete blob {url}: {e}")

    async def _read_file(self, file_path: Path) -> bytes:
        """Read a binary file into bytes."""
        with open(file_path, "rb") as f:
            return f.read()