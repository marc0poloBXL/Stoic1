"""
Queue handler for the Stoic Scheduler.
Folder-based queue — drop images with sidecar .txt caption files into queued/.
"""

import csv
import glob
import os
import re
import shutil
import time
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Tuple

from logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class QueueItem:
    """Represents a single queued post (any type)."""
    # Primary media (single image, story, reel thumbnail, first carousel slide)
    image_path: Optional[Path] = None
    caption_path: Optional[Path] = None
    video_path: Optional[Path] = None       # Reel video file
    slides: List[Path] = field(default_factory=list)  # Carousel slides
    post_type: str = "image"                # image | carousel | reel | story
    filename: str = ""
    status: str = "queued"
    retry_count: int = 0
    scheduled_date: Optional[str] = None
    added_at: Optional[str] = None

    def __post_init__(self):
        if not self.filename:
            if self.image_path:
                self.filename = self.image_path.stem
            elif self.video_path:
                self.filename = self.video_path.stem
                if self.post_type == "image":
                    self.post_type = "reel"
            elif self.slides:
                self.filename = self.slides[0].stem
                # Remove trailing _slide or _1 suffix for a clean name
                import re as _re
                self.filename = _re.sub(r"[_-]?(slide|1)$", "", self.filename)
        if not self.scheduled_date:
            match = re.match(r"(\d{4}-\d{2}-\d{2})", self.filename)
            if match:
                self.scheduled_date = match.group(1)
        if not self.added_at:
            self.added_at = datetime.now().isoformat()

    @property
    def caption_text(self) -> str:
        """Read and return the caption text from the sidecar file."""
        if not self.caption_path or not self.caption_path.exists():
            return ""
        try:
            with open(self.caption_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logger.warning(f"Failed to read caption for {self.filename}: {e}")
            return ""


class QueueHandler:
    """
    Manages the posting queue using a folder-based system.

    How it works:
    - Drop an image (PNG/JPG) into the queued/ folder
    - Optionally add a matching .txt file with the same name for the caption
    - The scheduler picks items up, posts them, and moves them to posted/
    """

    def __init__(self, config: dict):
        self.config = config
        queue_config = config["queue"]

        script_dir = Path(__file__).parent
        self.queue_dir = Path(queue_config["folder"])
        if not os.path.isabs(str(self.queue_dir)):
            self.queue_dir = (script_dir / self.queue_dir).resolve()

        self.carousels_dir = script_dir / "queued_carousels"
        self.reels_dir = script_dir / "queued_reels"
        self.stories_dir = script_dir / "queued_stories"

        self.posted_dir = Path(queue_config["posted_folder"])
        if not os.path.isabs(str(self.posted_dir)):
            self.posted_dir = (script_dir / self.posted_dir).resolve()

        self.failed_dir = Path(queue_config["failed_folder"])
        if not os.path.isabs(str(self.failed_dir)):
            self.failed_dir = (script_dir / self.failed_dir).resolve()

        self.require_caption = queue_config.get("require_caption", True)
        self.image_extensions = queue_config.get(
            "image_extensions", [".png", ".jpg", ".jpeg"]
        )
        self.video_extensions = (".mp4", ".mov", ".avi")

        # Ensure directories exist
        for d in [self.queue_dir, self.posted_dir, self.failed_dir,
                  self.carousels_dir, self.reels_dir, self.stories_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def scan_queue(self) -> List[QueueItem]:
        """
        Scan all queue folders for items.
        Returns items sorted by filename (oldest first), interleaving all types.
        """
        items = []
        items += self._scan_single_images()
        items += self._scan_carousels()
        items += self._scan_reels()
        items += self._scan_stories()
        items.sort(key=lambda x: x.filename)
        return items

    def _scan_single_images(self) -> List[QueueItem]:
        """Scan queued/ for single images with sidecar captions."""
        items = []
        seen = set()
        for ext in self.image_extensions:
            for img_path in sorted(self.queue_dir.glob(f"*{ext}")):
                if img_path.name in seen:
                    continue
                seen.add(img_path.name)
                caption_path = self._find_caption(img_path)
                if not caption_path and self.require_caption:
                    logger.warning(f"Skipping {img_path.name}: no caption file and require_caption is on")
                    continue
                items.append(QueueItem(image_path=img_path, caption_path=caption_path))
        return items

    def _scan_carousels(self) -> List[QueueItem]:
        """Scan queued_carousels/ for carousel items (subfolders with slides)."""
        items = []
        for folder in sorted(self.carousels_dir.iterdir()):
            if not folder.is_dir():
                continue
            slides = sorted(
                p for p in folder.iterdir()
                if p.suffix.lower() in self.image_extensions
            )
            if not slides:
                continue
            caption = self._find_caption_in_dir(folder)
            items.append(QueueItem(
                slides=slides,
                caption_path=caption,
                post_type="carousel",
                filename=folder.name,
            ))
        items.sort(key=lambda x: x.filename)
        return items

    def _scan_reels(self) -> List[QueueItem]:
        """Scan queued_reels/ for video files."""
        items = []
        for vid in sorted(self.reels_dir.iterdir()):
            if vid.suffix.lower() not in self.video_extensions:
                continue
            stem = vid.stem
            caption_path = self.reels_dir / f"{stem}.txt"
            if not caption_path.exists():
                caption_path = None
            items.append(QueueItem(
                video_path=vid,
                caption_path=caption_path,
                post_type="reel",
                filename=stem,
            ))
        return items

    def _scan_stories(self) -> List[QueueItem]:
        """Scan queued_stories/ for story images."""
        items = []
        for img in sorted(self.stories_dir.iterdir()):
            if img.suffix.lower() not in self.image_extensions:
                continue
            stem = img.stem
            caption_path = self.stories_dir / f"{stem}.txt"
            if not caption_path.exists():
                caption_path = None
            items.append(QueueItem(
                image_path=img,
                caption_path=caption_path,
                post_type="story",
                filename=stem,
            ))
        return items

    def is_time_to_post(self, schedule_config: dict, tolerance_minutes: int = 2) -> Tuple[bool, str]:
        """
        Check if the current time matches a scheduled posting slot.

        Args:
            schedule_config: The schedule.times dict from config
            tolerance_minutes: How many minutes before/after a slot counts

        Returns:
            (should_post, next_slot_info) tuple
        """
        now = datetime.now()
        day_name = now.strftime("%A").lower()  # monday, tuesday, etc.

        times = schedule_config.get("times", {}).get(day_name, [])
        if not times:
            return False, f"No slots scheduled for {day_name}"

        current_minutes = now.hour * 60 + now.minute

        for slot in times:
            try:
                slot_parts = slot.strip().split(":")
                slot_minutes = int(slot_parts[0]) * 60 + int(slot_parts[1])
            except (ValueError, IndexError):
                continue

            if abs(current_minutes - slot_minutes) <= tolerance_minutes:
                return True, f"Posting at {slot} ({day_name})"

        # Find next slot for display
        next_slot = self._get_next_slot(schedule_config)
        return False, next_slot

    def _get_next_slot(self, schedule_config: dict) -> str:
        """Return a string describing the next scheduled time slot."""
        now = datetime.now()
        day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        current_day_idx = now.weekday()
        current_minutes = now.hour * 60 + now.minute

        # Check later today
        times = schedule_config.get("times", {}).get(
            day_names[current_day_idx], []
        )
        for slot in times:
            try:
                slot_parts = slot.strip().split(":")
                slot_minutes = int(slot_parts[0]) * 60 + int(slot_parts[1])
                if slot_minutes > current_minutes:
                    return f"Next slot today at {slot}"
            except (ValueError, IndexError):
                continue

        # Check next days
        for offset in range(1, 8):
            next_day_idx = (current_day_idx + offset) % 7
            day_name = day_names[next_day_idx]
            times = schedule_config.get("times", {}).get(day_name, [])
            if times:
                next_slot = times[0]
                days_from_now = offset
                return f"Next slot {day_name} at {next_slot} ({days_from_now} day(s) from now)"

        return "No upcoming slots found"

    @staticmethod
    def _find_caption(img_path: Path) -> Optional[Path]:
        """Find a caption file for an image (same stem .txt or .md)."""
        for ext in (".txt", ".md"):
            p = img_path.with_suffix(ext)
            if p.exists():
                return p
        return None

    @staticmethod
    def _find_caption_in_dir(folder: Path) -> Optional[Path]:
        """Find a caption file inside a carousel folder."""
        for name in ("caption.txt", "caption.md", "cap.txt"):
            p = folder / name
            if p.exists():
                return p
        return None

    def move_to_posted(self, item: QueueItem) -> bool:
        """Move a posted item to the posted/ archive folder."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_dir = self.posted_dir / f"{timestamp}_{item.post_type}_{item.filename}"
            dest_dir.mkdir(parents=True, exist_ok=True)

            # Move primary image
            if item.image_path and item.image_path.exists():
                shutil.move(str(item.image_path), str(dest_dir / item.image_path.name))

            # Move video
            if item.video_path and item.video_path.exists():
                shutil.move(str(item.video_path), str(dest_dir / item.video_path.name))

            # Move carousel slides
            for slide in item.slides:
                if slide.exists():
                    shutil.move(str(slide), str(dest_dir / slide.name))

            # Move caption
            if item.caption_path and item.caption_path.exists():
                shutil.move(str(item.caption_path), str(dest_dir / item.caption_path.name))

            item.status = "posted"
            self._append_posting_log(item, timestamp, "success", "")
            logger.info(f"Moved to posted/: {item.filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to move posted item {item.filename}: {e}")
            return False

    def move_to_failed(self, item: QueueItem, error_reason: str = ""):
        """Move a failed item to the failed/ folder for review."""
        try:
            dest_dir = self.failed_dir / f"{item.post_type}_{item.filename}"
            dest_dir.mkdir(parents=True, exist_ok=True)

            if item.image_path and item.image_path.exists():
                shutil.move(str(item.image_path), str(dest_dir / item.image_path.name))
            if item.video_path and item.video_path.exists():
                shutil.move(str(item.video_path), str(dest_dir / item.video_path.name))
            for slide in item.slides:
                if slide.exists():
                    shutil.move(str(slide), str(dest_dir / slide.name))
            if item.caption_path and item.caption_path.exists():
                shutil.move(str(item.caption_path), str(dest_dir / item.caption_path.name))

            error_file = dest_dir / "error.txt"
            with open(error_file, "w") as f:
                f.write(f"Filename: {item.filename}\n")
                f.write(f"Type: {item.post_type}\n")
                f.write(f"Failed at: {datetime.now().isoformat()}\n")
                f.write(f"Retries: {item.retry_count}\n")
                f.write(f"Error: {error_reason}\n")

            item.status = "failed"
            self._append_posting_log(item, datetime.now().strftime("%Y%m%d_%H%M%S"), "failed", error_reason)
            logger.warning(f"Moved to failed/: {item.filename} — {error_reason}")

        except Exception as e:
            logger.error(f"Failed to move item {item.filename} to failed/: {e}")

    def auto_import(self) -> int:
        """
        Scan weekly batch folders for all content types and import into the queue.
        Handles: quotes (single images), carousels, reels, stories.

        Returns:
            Number of items imported.
        """
        imported = 0
        scheduler_dir = Path(__file__).parent
        sched_dir = (scheduler_dir / ".." / ".." / "11_MEDIA_LIBRARY" / "SCHEDULED").resolve()

        for week_dir in sorted(glob.glob(str(sched_dir / "week_*"))):
            week_path = Path(week_dir)

            # --- Single images from quotes/ (existing behavior) ---
            quotes_dir = week_path / "quotes"
            if quotes_dir.exists():
                for ext in self.image_extensions:
                    for img in sorted(quotes_dir.glob(f"*{ext}")):
                        if self._import_image(img, week_path):
                            imported += 1

            # --- Carousels from carousels/ (subfolders with slides + caption) ---
            car_dir = week_path / "carousels"
            if car_dir.exists():
                for carousel_folder in sorted(car_dir.iterdir()):
                    if not carousel_folder.is_dir():
                        continue
                    dest = self.carousels_dir / carousel_folder.name
                    if dest.exists():
                        continue  # already imported
                    # Copy the whole folder
                    shutil.copytree(str(carousel_folder), str(dest), dirs_exist_ok=True)
                    imported += 1
                    logger.info(f"Imported carousel: {carousel_folder.name}")

            # --- Reels from reels/ (mp4 + optional caption) ---
            reels_dir = week_path / "reels"
            if reels_dir.exists():
                for vid in sorted(reels_dir.glob("*.mp4")):
                    dest = self.reels_dir / vid.name
                    if dest.exists():
                        continue
                    shutil.copy2(str(vid), str(dest))
                    # Find matching caption
                    cap_src = reels_dir / f"{vid.stem}.txt"
                    if cap_src.exists():
                        shutil.copy2(str(cap_src), self.reels_dir / cap_src.name)
                    imported += 1
                    logger.info(f"Imported reel: {vid.name}")

            # --- Stories from stories/ (png/jpg + optional caption) ---
            stories_dir = week_path / "stories"
            if stories_dir.exists():
                for ext in self.image_extensions:
                    for story_img in sorted(stories_dir.glob(f"*{ext}")):
                        dest = self.stories_dir / story_img.name
                        if dest.exists():
                            continue
                        shutil.copy2(str(story_img), str(dest))
                        cap_src = stories_dir / f"{story_img.stem}.txt"
                        if cap_src.exists():
                            shutil.copy2(str(cap_src), self.stories_dir / cap_src.name)
                        imported += 1
                        logger.info(f"Imported story: {story_img.name}")

        logger.info(f"Auto-import: {imported} new item(s) added to queue")
        return imported

    def _import_image(self, img_path: Path, week_path: Optional[Path] = None,
                      skip_if_has_quotes_dir: bool = False) -> bool:
        """
        Import a single image from a batch folder into the queue.
        Also looks for a matching caption file.
        """
        # Skip if already in queue
        dest_image = self.queue_dir / img_path.name
        if dest_image.exists():
            return False

        # Skip if there's a quotes/ subfolder and we're in the root of the week
        if skip_if_has_quotes_dir and week_path:
            if (week_path / "quotes").exists():
                return False

        # Find matching caption file.
        # Captions follow the {date}_{sign}_caption.{txt,md} convention
        # (e.g. image 2026-09-21_virgo_quote.png ↔ caption 2026-09-21_virgo_caption.md).
        # Also try the same-stem name as a fallback.
        import re as _re
        stem = img_path.stem  # e.g. 2026-09-21_virgo_quote
        base = _re.sub(r"_quote$", "", stem)  # e.g. 2026-09-21_virgo

        caption_sources = [
            img_path.with_suffix(".txt"),                          # same stem
            img_path.with_suffix(".md"),
        ]
        if base != stem:
            caption_sources += [
                img_path.with_name(f"{base}_caption.txt"),
                img_path.with_name(f"{base}_caption.md"),
            ]

        # Also look in the captions/ subfolder if provided week_path
        if week_path:
            caps_dir = week_path / "captions"
            caption_sources += [
                caps_dir / f"{stem}.txt",
                caps_dir / f"{stem}.md",
                caps_dir / f"{base}_caption.txt",
                caps_dir / f"{base}_caption.md",
            ]

        caption_path = None
        for cap in caption_sources:
            if cap.exists():
                caption_path = cap
                break

        # Copy image to queue
        try:
            shutil.copy2(str(img_path), str(dest_image))
        except Exception as e:
            logger.warning(f"Failed to copy {img_path.name}: {e}")
            return False

        # Copy caption if found — strip markdown so it posts as clean text
        if caption_path:
            dest_caption = self.queue_dir / f"{img_path.stem}.txt"
            try:
                text = self._clean_caption(caption_path)
                with open(dest_caption, "w", encoding="utf-8") as f:
                    f.write(text)
            except Exception as e:
                logger.warning(f"Failed to copy caption for {img_path.name}: {e}")

        logger.info(f"Imported: {img_path.name}")
        return True

    @staticmethod
    def _clean_caption(caption_path: Path) -> str:
        """
        Read a caption file and strip markdown formatting so it posts as
        clean Instagram text.

        - Removes '# Heading' header lines (e.g. '# Caption — ♍ Virgo (Day 36)')
        - Strips **bold**, *italic*, `code`, [links], and similar markdown markup
        - Keeps hashtags, line breaks, and the main body intact
        """
        with open(caption_path, "r", encoding="utf-8") as f:
            raw = f.read()

        lines = []
        for line in raw.splitlines():
            stripped = line.strip()
            # Skip markdown headings and the caption header block
            if stripped.startswith("#"):
                continue
            # Strip blockquote markers and unordered list bullets
            if stripped.startswith(">"):
                stripped = stripped.lstrip(">").strip()
            cleaned = stripped
            # Remove markdown markers
            for marker in ("**", "__", "`", "*"):
                cleaned = cleaned.replace(marker, "")
            lines.append(cleaned)

        text = "\n".join(lines).strip()
        # Collapse 3+ blank lines into a single blank line
        import re as _re
        text = _re.sub(r"\n{3,}", "\n\n", text)
        return text

    def get_queue_summary(self, items: List[QueueItem]) -> str:
        """Return a human-readable summary of the queue."""
        if not items:
            return "Queue is empty."

        type_icons = {"image": "🖼️", "carousel": "🎠", "reel": "🎬", "story": "📖"}
        lines = ["📋 Posting Queue:"]
        for i, item in enumerate(items, 1):
            icon = type_icons.get(item.post_type, "📄")
            date_str = f" [{item.scheduled_date}]" if item.scheduled_date else ""
            caption_preview = item.caption_text[:60].replace("\n", " ") if item.caption_text else "(no caption)"
            slides_info = f" ({len(item.slides)} slides)" if item.slides else ""
            lines.append(
                f"  {i}. {icon} [{item.post_type}]{date_str} {item.filename}{slides_info}\n"
                f"     Caption: {caption_preview}…"
            )

        return "\n".join(lines)

    def _append_posting_log(self, item: QueueItem, timestamp: str, status: str, error: str):
        """Append a row to the posting log CSV."""
        log_file = self.posted_dir / "posting_log.csv"
        is_new = not log_file.exists()

        try:
            with open(log_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if is_new:
                    writer.writerow(["timestamp", "filename", "status", "caption_preview", "error"])
                writer.writerow([
                    timestamp,
                    item.filename,
                    status,
                    item.caption_text[:100].replace("\n", " "),
                    error,
                ])
        except Exception as e:
            logger.warning(f"Failed to append to posting log: {e}")