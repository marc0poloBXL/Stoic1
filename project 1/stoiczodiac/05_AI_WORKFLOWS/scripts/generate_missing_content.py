#!/usr/bin/env python3
"""
generate_missing_content.py — Generate carousels + reels for upcoming weeks.
Uses edge-tts for voiceover, ffmpeg for video assembly, Playwright for PNG rendering.

Usage:
    python generate_missing_content.py                    # All upcoming weeks
    python generate_missing_content.py --week 20261012    # Specific week only
"""

import argparse
import json
import os
import re
import subprocess
import sys
import asyncio
import shutil
from pathlib import Path
from datetime import datetime, date, timedelta

# Force UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
SCHEDULED_DIR = PROJECT_ROOT / "11_MEDIA_LIBRARY" / "SCHEDULED"
SIGN_MASTER = PROJECT_ROOT / "05_AI_WORKFLOWS" / "sign_master_data.json"
FFMPEG = r"C:\Users\marcj\AppData\Roaming\Python\Python314\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

# Sign name → symbol map
SIGN_SYMBOLS = {
    "aries": "♈", "taurus": "♉", "gemini": "♊", "cancer": "♋",
    "leo": "♌", "virgo": "♍", "libra": "♎", "scorpio": "♏",
    "sagittarius": "♐", "capricorn": "♑", "aquarius": "♒", "pisces": "♓"
}

# Colors per sign (from brand palette)
SIGN_COLORS = {
    "aries": "#E63946", "taurus": "#2A9D8F", "gemini": "#E9C46A",
    "cancer": "#A8DADC", "leo": "#F4A261", "virgo": "#8CB369",
    "libra": "#B5838D", "scorpio": "#6D597A", "sagittarius": "#E76F51",
    "capricorn": "#3D405B", "aquarius": "#81B29A", "pisces": "#7B6C8C"
}

CAROUSEL_TEMPLATE = PROJECT_ROOT / "04_TEMPLATES" / "svg_assets" / "carousel_page_frame.svg"
QUOTE_CARD_TEMPLATE = PROJECT_ROOT / "04_TEMPLATES" / "svg_assets" / "quote_card_frame.svg"

# ── Load sign data ──
with open(SIGN_MASTER, encoding="utf-8") as f:
    sign_data = json.load(f)
sign_map = {s["id"]: s for s in sign_data["signs"]}
philosopher_map = {p["name"]: p for p in sign_data["philosophers"]}


def get_sign_for_date(target_date: date) -> tuple:
    """Get (sign_id, philosopher_name, theme) for a given date using rotation 0-89."""
    if hasattr(get_sign_for_date, "rotation"):
        rotation = get_sign_for_date.rotation
    else:
        # Build rotation on first call
        rotation = []
        for sign in sign_data["signs"]:
            for phil in sign_data["philosophers"]:
                rotation.append((sign["id"], sign["name"], phil["name"]))
        # Truncate to 90 days
        rotation = rotation[:90]
        get_sign_for_date.rotation = rotation

    # Launch date: Aug 17 2026 = day 0
    launch = date(2026, 8, 17)
    day_num = (target_date - launch).days
    if day_num < 0:
        return None, None, None
    idx = day_num % len(rotation)
    sign_id, sign_name, phil_name = rotation[idx]
    # Get theme from brief if available, or generate
    theme = f"The way of {sign_name}"
    return sign_id, sign_name, phil_name


def parse_week_brief(week_path: Path) -> list:
    """Parse WEEKLY_BATCH_BRIEF.md to extract needed formats per day.
    Returns list of (date, sign, needed_carousels, needs_reel) tuples."""
    brief_path = week_path / "WEEKLY_BATCH_BRIEF.md"
    if not brief_path.exists():
        print(f"  ⚠ No brief at {brief_path}")
        return []

    with open(brief_path, encoding="utf-8") as f:
        content = f.read()

    # Find the "Week at a Glance" table
    table_section = re.search(r"\| Day \| Date \| Sign \|.*?\n\|[-| ]+\n(.+?)\n\n", content, re.DOTALL)
    if not table_section:
        print(f"  ⚠ No schedule table in brief")
        return []

    entries = []
    for line in table_section.group(1).strip().split("\n"):
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 6:
            continue
        day, date_str, sign_with_symbol, philosopher, theme, fmt = parts[:6]

        try:
            d = datetime.strptime(f"{date_str} 2026", "%b %d %Y").date()
        except ValueError:
            try:
                d = datetime.strptime(f"{date_str} 2026", "%B %d %Y").date()
            except ValueError:
                continue

        # Detect sign
        sign_lower = None
        for s_id, s_info in sign_map.items():
            if s_id.lower() in sign_with_symbol.lower() or s_info["name"].lower() in sign_with_symbol.lower():
                sign_lower = s_id
                break

        needs_reel = "**Reel**" in fmt
        needs_carousel = []
        if "**Carousel**" in fmt:
            if "Sign Spotlight" in fmt:
                needs_carousel.append("sign_spotlight")
            elif "Weekly Forecast" in fmt:
                needs_carousel.append("weekly_forecast")
            else:
                needs_carousel.append("carousel")

        entries.append((d, sign_lower, needs_carousel, needs_reel, theme))

    return entries


def make_slide_svg(sign_id: str, slide_type: str, slide_num: int, total_slides: int,
                   title: str, content: str, page_label: str = "") -> str:
    """Generate an SVG carousel slide with the brand template."""
    sign_name = sign_map[sign_id]["name"]
    symbol = SIGN_SYMBOLS.get(sign_id, "★")
    color = SIGN_COLORS.get(sign_id, "#D4AF37")

    # Read template and customize
    with open(CAROUSEL_TEMPLATE, encoding="utf-8") as f:
        svg = f.read()

    # Page number
    svg = svg.replace('<circle cx="540" cy="1055" r="6" fill="none" stroke="#D4AF37" stroke-width="0.8" opacity="0.4"/>',
                      f'<text x="540" y="1060" font-family="Arial, sans-serif" font-size="12" fill="#C9A96E" '
                      f'text-anchor="middle" opacity="0.6">{slide_num} / {total_slides}</text>')

    # Title
    svg = svg.replace('<rect x="120" y="120" width="840" height="840" fill="none" stroke="none"/>',
                      f'''<text x="540" y="100" font-family="Arial, sans-serif" font-size="24" font-weight="600"
        fill="#D4AF37" text-anchor="middle" letter-spacing="3" opacity="0.8">{page_label}</text>

    <text x="540" y="160" font-family="Arial, sans-serif" font-size="64" fill="{color}" text-anchor="middle" opacity="0.9">{symbol}</text>
    <text x="540" y="210" font-family="Arial, sans-serif" font-size="22" font-weight="600" fill="{color}" text-anchor="middle" letter-spacing="3" opacity="0.8">{sign_name}</text>

    <line x1="300" y1="240" x2="780" y2="240" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>

    <text x="540" y="290" font-family="Arial, sans-serif" font-size="20" font-weight="600" fill="#C9A96E" text-anchor="middle" opacity="0.9">{title}</text>

    <text x="540" y="360" font-family="Arial, sans-serif" font-size="18" fill="#F5F5F5" text-anchor="middle" opacity="0.85">{_wrap_text(content, 55)}</text>

    <text x="540" y="980" font-family="Arial, sans-serif" font-size="12" fill="#F5F5F5" text-anchor="middle" opacity="0.2" letter-spacing="2">@STOICZODIAC</text>''')

    return svg


def _wrap_text(text, max_chars=60):
    """Simple text wrapping for SVG."""
    if len(text) <= max_chars:
        return text
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 > max_chars:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return "\n".join(lines)


def make_reel_text_svg(sign_id: str, quote_text: str, philosopher: str, theme: str) -> str:
    """Generate a single SVG frame for a reel (quote overlay)."""
    symbol = SIGN_SYMBOLS.get(sign_id, "★")
    color = SIGN_COLORS.get(sign_id, "#D4AF37")
    sign_name = sign_map[sign_id]["name"]

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="75%">
      <stop offset="0%" stop-color="#1A1A2E"/>
      <stop offset="100%" stop-color="#0A0A0A"/>
    </radialGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37"/>
      <stop offset="50%" stop-color="#C9A96E"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1920" fill="url(#bgGrad)"/>
  <text x="540" y="160" font-family="Arial, sans-serif" font-size="80" fill="{color}" text-anchor="middle" opacity="0.9">{symbol}</text>
  <text x="540" y="220" font-family="Arial, sans-serif" font-size="24" font-weight="600" fill="{color}" text-anchor="middle" letter-spacing="4" opacity="0.8">{sign_name}</text>
  <line x1="300" y1="260" x2="780" y2="260" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>
  <text x="540" y="700" font-family="Arial, sans-serif" font-size="36" fill="#D4AF37" text-anchor="middle" font-style="italic" opacity="0.9">"</text>
  <text x="540" y="850" font-family="Arial, sans-serif" font-size="28" fill="#F5F5F5" text-anchor="middle" opacity="0.85">"{quote_text[:200]}"</text>
  <text x="540" y="950" font-family="Arial, sans-serif" font-size="20" font-style="italic" fill="#C9A96E" text-anchor="middle" opacity="0.7">— {philosopher}</text>
  <text x="540" y="1850" font-family="Arial, sans-serif" font-size="14" fill="#F5F5F5" text-anchor="middle" opacity="0.25" letter-spacing="3">@STOICZODIAC</text>
</svg>'''


def render_svg_to_png(svg_path: Path, png_path: Path):
    """Use Playwright to render SVG to PNG (same approach as generate_all_svgs.py)."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  ⚠ Playwright not installed — skipping PNG render")
        return False

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            page.set_viewport_size({"width": 1080, "height": 1080})
            page.goto(f"file://{svg_path.resolve()}", wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(png_path), full_page=True, timeout=120000)
            browser.close()
        return True
    except Exception as e:
        print(f"  ⚠ Render failed: {e}")
        return False


async def generate_tts_audio(text: str, output_path: Path, voice: str = "en-US-JennyNeural"):
    """Generate TTS audio using edge-tts."""
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))
        return output_path.exists() and output_path.stat().st_size > 100
    except Exception as e:
        print(f"  ⚠ TTS failed: {e}")
        return False


def create_reel_video(image_path: Path, audio_path: Path, output_path: Path,
                      zoom_start: float = 1.0, zoom_end: float = 1.08):
    """Create a reel video from a single image + audio using ffmpeg (Ken Burns effect)."""
    duration_cmd = [FFMPEG, "-i", str(audio_path), "-f", "null", "-"]
    result = subprocess.run(duration_cmd, capture_output=True, text=True)
    duration_match = re.search(r"Duration: (\d+):(\d+):([\d.]+)", result.stderr)
    if not duration_match:
        print("  ⚠ Could not detect audio duration")
        return False

    h, m, s = map(float, duration_match.groups())
    duration = h * 3600 + m * 60 + s

    if duration < 5:
        print(f"  ⚠ Audio too short ({duration:.1f}s), padding")
        duration = 8  # minimum reel length

    # Ken Burns zoom effect
    cmd = [
        FFMPEG, "-y",
        "-loop", "1",
        "-i", str(image_path),
        "-i", str(audio_path),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-vf",
        f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='if(lte(on,1),{zoom_start},{zoom_start}+({zoom_end}-{zoom_start})*(on-1)/{int(duration*30)})':"
        f"d={int(duration*30)}:s=1080x1920:fps=30",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        return output_path.exists() and output_path.stat().st_size > 1024
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ ffmpeg failed: {e.stderr.decode()[:200] if e.stderr else '?'}")
        return False


def generate_carousels_for_week(week_path: Path):
    """Generate SVG + PNG carousels for a week based on brief."""
    week_folder = week_path.name
    entries = parse_week_brief(week_path)
    if not entries:
        return 0

    carousels_dir = week_path / "carousels"
    carousels_png_dir = week_path / "carousels_png"
    carousels_dir.mkdir(exist_ok=True)
    carousels_png_dir.mkdir(exist_ok=True)

    created = 0

    # Group sign_spotlight and weekly_forecast
    spotlight_entries = [(d, s, th) for d, s, car, reel, th in entries if "sign_spotlight" in car and s]
    forecast_entry = [(d, s, th) for d, s, car, reel, th in entries if "weekly_forecast" in car]

    # Sign Spotlight carousels (7 slides about one sign)
    for d, sign_id, theme in spotlight_entries:
        folder_name = f"spotlight_{sign_id}"
        slide_dir = carousels_dir / folder_name
        slide_png_dir = carousels_png_dir / folder_name
        slide_dir.mkdir(exist_ok=True)
        slide_png_dir.mkdir(exist_ok=True)

        sign_name = sign_map[sign_id]["name"]
        symbol = SIGN_SYMBOLS[sign_id]
        color = SIGN_COLORS[sign_id]

        # 7 slides: intro, virtue, quote, challenge, reflection, practice, outro
        slides = [
            ("The Stoic Path", f"The {sign_name} journey toward wisdom and self-command.", "SPOTLIGHT"),
            ("Core Virtue", f"{sign_name}, your Stoic edge is {sign_map[sign_id].get('philosopher_reason', 'clarity of purpose')}.", f"★ {sign_name}"),
            ("Quote", f"\"The best revenge is to be unlike him who performed the injury.\" — Marcus Aurelius", "WISDOM"),
            ("Daily Challenge", f"Today: find one thing you control — and act on it without hesitation.", "CHALLENGE"),
            ("Reflection", f"Ask yourself: 'Did I let impulse rule, or did I pause and choose?'", "REFLECTION"),
            ("Practice", f"Try this: 5 minutes of silence. Breathe. Notice. Then decide.", f"PRACTICE"),
            ("Your Stoic Path", f"You are not your thoughts. You are the one who observes them.", "PATH"),
        ]

        for i, (title, text, label) in enumerate(slides, 1):
            slide_svg_content = make_slide_svg(sign_id, "spotlight", i, len(slides), title, text, label)
            svg_file = slide_dir / f"slide_{i:02d}_of_{len(slides):02d}.svg"
            with open(svg_file, "w", encoding="utf-8") as f:
                f.write(slide_svg_content)

            png_file = slide_png_dir / f"slide_{i:02d}_of_{len(slides):02d}.png"
            if not png_file.exists():
                if render_svg_to_png(svg_file, png_file):
                    created += 1
                else:
                    print(f"  ⚠ PNG render failed for {svg_file.name}")

        print(f"  ✅ Carousel {folder_name}: {len(slides)} slides")

    # Weekly Forecast carousel (10 slides)
    for d, forecast_sign, _ in forecast_entry:
        folder_name = "weekly_forecast"
        slide_dir = carousels_dir / folder_name
        slide_png_dir = carousels_png_dir / folder_name
        slide_dir.mkdir(exist_ok=True)
        slide_png_dir.mkdir(exist_ok=True)

        # 10 slides: cover, 7 day signs (from entries), summary, closing
        slides_data = [("The Week Ahead", "Your Stoic forecast for the coming days.", "FORECAST")]
        for ed, esign, ecar, ereel, eth in entries:
            if esign:
                slides_data.append((f"{SIGN_SYMBOLS.get(esign, '')} {sign_map[esign]['name']}",
                                    f"{eth}: Practice stillness before action.",
                                    sign_map[esign]["name"]))
        # Add placeholder slides if not enough
        while len(slides_data) < 9:
            slides_data.append(("Daily Stoic", "Every moment is a chance to choose virtue.", "REMINDER"))
        slides_data.append(("The Stoic Week", "You control your responses. The rest is indifferent.", "CLOSING"))

        slides_data = slides_data[:10]  # max 10

        for i, (title, text, label) in enumerate(slides_data, 1):
            slide_svg_content = make_slide_svg(forecast_sign or "virgo", "forecast", i, len(slides_data),
                                                title, text, label)
            svg_file = slide_dir / f"slide_{i:02d}_of_{len(slides_data):02d}.svg"
            with open(svg_file, "w", encoding="utf-8") as f:
                f.write(slide_svg_content)

            png_file = slide_png_dir / f"slide_{i:02d}_of_{len(slides_data):02d}.png"
            if not png_file.exists():
                if render_svg_to_png(svg_file, png_file):
                    created += 1

        print(f"  ✅ Carousel {folder_name}: {len(slides_data)} slides")

    return created


def generate_reels_for_week(week_path: Path):
    """Generate reel videos for the week (3/week: Mon, Wed, Fri)."""
    entries = parse_week_brief(week_path)
    if not entries:
        return 0

    reels_dir = week_path / "reels"
    reels_dir.mkdir(exist_ok=True)

    created = 0

    for d, sign_id, _, needs_reel, theme in entries:
        if not needs_reel or not sign_id:
            continue

        sign_name = sign_map[sign_id]["name"]
        date_str = d.strftime("%Y-%m-%d")
        output_path = reels_dir / f"{date_str}_{sign_id}_reel.mp4"

        if output_path.exists():
            continue

        # Get quote text from existing quote card
        quote_png = week_path / "quotes" / f"{date_str}_{sign_id}_quote.png"
        quote_svg_source = week_path / "quotes_svg" / f"{date_str}_{sign_id}_quote.svg"

        # Generate voiceover text
        voice_text = f"{sign_name}. {theme}. {sign_map[sign_id].get('philosopher_reason', 'Channel your inner strength')}. Today, focus on what you can control."

        # Generate TTS audio
        audio_path = reels_dir / f"{date_str}_{sign_id}_audio.mp3"
        if not audio_path.exists():
            print(f"  🎤 Generating TTS for {sign_name}...")
            success = asyncio.run(generate_tts_audio(voice_text, audio_path))
            if not success:
                print(f"  ⚠ TTS failed for {sign_name}")
                continue

        # Use existing quote PNG or create a simple one
        image_for_reel = quote_png if quote_png.exists() else None

        if not image_for_reel:
            # Create a simple SVG frame with the quote
            temp_svg = reels_dir / f"{date_str}_{sign_id}_reel_frame.svg"
            temp_png = reels_dir / f"{date_str}_{sign_id}_reel_frame.png"
            phil = "Marcus Aurelius"
            with open(temp_svg, "w", encoding="utf-8") as f:
                f.write(make_reel_text_svg(sign_id, voice_text, phil, theme))
            if not render_svg_to_png(temp_svg, temp_png):
                print(f"  ⚠ Frame render failed for {sign_name}")
                continue
            image_for_reel = temp_png

        # Create reel with Ken Burns effect
        print(f"  🎬 Creating reel for {sign_name}...")
        success = create_reel_video(image_for_reel, audio_path, output_path,
                                    zoom_start=1.0, zoom_end=1.06)
        if success:
            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"  ✅ Reel: {output_path.name} ({file_size:.1f} MB)")
            created += 1
        else:
            print(f"  ⚠ ffmpeg failed for {sign_name}")

    return created


def generate_manifest(week_path: Path, carousel_count: int, reel_count: int, errors: list):
    """Write a CAROUSEL_MANIFEST.md for the week."""
    manifest_path = week_path / "CAROUSEL_MANIFEST.md"
    content = f"""# Production Manifest — {week_path.name}

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Carousels ({carousel_count} slides)

- Folder: `{week_path.name}/carousels/`
- PNGs: `{week_path.name}/carousels_png/`

## Reels ({reel_count} videos)

- Folder: `{week_path.name}/reels/`
- Format: MP4, 1080×1920, 30fps

## Errors
"""
    if errors:
        for e in errors:
            content += f"- {e}\n"
    else:
        content += "- (none)\n"

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Generate missing carousels + reels")
    parser.add_argument("--week", type=str, help="Process only this week (YYYYMMDD)")
    args = parser.parse_args()

    # Determine which weeks to process
    if args.week:
        week_path = SCHEDULED_DIR / f"week_{args.week}"
        week_folders = [week_path] if week_path.exists() else []
    else:
        # All weeks from current date forward (Oct 12 2026 = week_20261012)
        today = date(2026, 10, 15)
        week_folders = sorted(SCHEDULED_DIR.glob("week_*"))
        week_folders = [w for w in week_folders
                        if w.name >= "week_20261012" and w.name <= "week_20270104"]

    if not week_folders:
        print("No week folders found to process.")
        return

    total_carousels = 0
    total_reels = 0

    for week_path in week_folders:
        week_name = week_path.name
        print(f"\n{'='*60}")
        print(f"  {week_name}")
        print(f"{'='*60}")

        if not (week_path / "WEEKLY_BATCH_BRIEF.md").exists():
            print(f"  ⚠ No brief — skipping")
            continue

        errors = []

        # Generate carousels
        print(f"\n  📑 Carousels...")
        c_count = generate_carousels_for_week(week_path)
        total_carousels += c_count

        # Generate reels
        print(f"\n  🎬 Reels...")
        r_count = generate_reels_for_week(week_path)
        total_reels += r_count

        # Write manifest
        generate_manifest(week_path, c_count, r_count, errors)

        print(f"\n  ✅ Done — {c_count} carousel slides, {r_count} reels")

    print(f"\n{'='*60}")
    print(f"  COMPLETE — Total: {total_carousels} carousel slides, {total_reels} reels")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()