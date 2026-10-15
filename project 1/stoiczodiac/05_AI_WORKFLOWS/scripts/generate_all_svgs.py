#!/usr/bin/env python3
"""
generate_all_svgs.py — Generate SVG quote cards + stories for ALL weeks.
Reads existing text content (quotes/*.md, stories/*.md) from each week folder
and produces matching SVGs, then converts them to PNGs (--png flag, via Playwright).

Usage:
    python generate_all_svgs.py                    # Process all weeks
    python generate_all_svgs.py --week 10          # Process a specific week
    python generate_all_svgs.py --png              # Also convert to PNGs
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ── Force UTF-8 on Windows ──
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# ── Paths ──
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]  # stoiczodiac/
SCHEDULED_DIR = PROJECT_ROOT / "11_MEDIA_LIBRARY" / "SCHEDULED"
SIGN_MASTER_PATH = SCRIPT_DIR.parent / "sign_master_data.json"
RENDER_SCRIPT = SCRIPT_DIR / "render_pngs.js"

# ── Load sign data ──
with open(SIGN_MASTER_PATH, "r", encoding="utf-8") as f:
    sign_data = json.load(f)

sign_map = {s["id"]: s for s in sign_data["signs"]}
# philosopher_map is unused — sign/philosopher data accessed via sign_data["philosophers"] directly

# ── Helper: parse a quote .md file ──
def parse_quote_file(filepath):
    """Parse a generated quote .md file into structured fields."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    quote_match = re.search(r'>\s*"(.+?)"', text, re.DOTALL)
    quote = quote_match.group(1).strip() if quote_match else ""

    app_match = re.search(r'## Application\n(.+?)(?=\n## |\Z)', text, re.DOTALL)
    application = app_match.group(1).strip() if app_match else ""

    chal_match = re.search(r'## Daily Challenge\n(.+?)(?=\n#|\Z)', text, re.DOTALL)
    challenge = chal_match.group(1).strip() if chal_match else ""

    # Extract sign and theme from first lines
    sign_match = re.search(r'# [♈♉♊♋♌♍♎♏♐♑♒♓]\s+(\w+)', text)
    sign_name = sign_match.group(1).lower() if sign_match else ""

    theme_match = re.search(r'\*\*Theme\*\*:\s*(.+?)$', text, re.MULTILINE)
    theme = theme_match.group(1).strip() if theme_match else ""

    phil_match = re.search(r'\*\*Philosopher\*\*:\s*(.+?)$', text, re.MULTILINE)
    philosopher = phil_match.group(1).strip() if phil_match else ""

    return {
        "sign_id": sign_name,
        "theme": theme,
        "philosopher": philosopher,
        "quote": quote,
        "application": application,
        "challenge": challenge,
    }


def parse_story_file(filepath):
    """Parse a story .md file to extract the prompt."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    # Extract the journal prompt
    prompt_match = re.search(r'Journal this:\s*(.+?)(?:\n|$)', text)
    if prompt_match:
        return prompt_match.group(1).strip()
    # Fallback: get first non-header line
    lines = [l.strip() for l in text.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("📜")]
    return lines[0] if lines else "Reflect on today's Stoic lesson."


def parse_caption_file(filepath):
    """Parse a caption .md file."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    # Extract the main caption between header and hashtags
    lines = text.split("\n")
    # Find the actual caption (after attribution, before hashtags)
    caption_started = False
    caption_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("— "):
            continue
        if stripped.startswith("#Stoic") or stripped.startswith("#"):
            continue
        stripped and caption_lines.append(stripped)
    caption = " ".join(caption_lines) if caption_lines else ""
    return caption


# ── SVG templates ──


def generate_quote_svg(sign, philosopher, theme, quote, application, challenge):
    """Generate a 1080x1080 quote card SVG."""
    color = sign["color"]
    symbol = sign["symbol"]
    sign_name = sign["name"].upper()
    element = sign["element"].upper()

    # Wrap quote to ~48 chars per line
    words = quote.split()
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        if len(test) <= 50:
            current = test
        else:
            current and lines.append(current)
            current = w
    current and lines.append(current)

    quote_lines_svg = ""
    start_y = 380 - ((len(lines) - 2) * 28)
    for i, line in enumerate(lines):
        y = start_y + i * 58
        quote_lines_svg += (
            f'  <text x="540" y="{y}" '
            f'font-family="Georgia, serif" font-size="36" fill="#D4AF37" '
            f'text-anchor="middle" font-style="italic">'
            f'{"\\u201c" if i == 0 else ""}{line}{"\\u201d" if i == len(lines) - 1 else ""}'
            f'</text>\n'
        )

    # Escape XML entities
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    phil_label = f"— {philosopher}"
    theme_upper = theme.upper()[:40]
    challenge_text = esc(challenge[:80])
    app_text = esc(application[:200])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1A1A2E"/>
      <stop offset="100%" stop-color="#0A0A0A"/>
    </radialGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37"/>
      <stop offset="50%" stop-color="#C9A96E"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
  </defs>

  <rect width="1080" height="1080" fill="url(#bgGrad)"/>
  <rect x="30" y="30" width="1020" height="1020" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.7"/>
  <rect x="40" y="40" width="1000" height="1000" fill="none" stroke="#D4AF37" stroke-width="0.5" opacity="0.3"/>
  <line x1="240" y1="60" x2="840" y2="60" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.5"/>
  <line x1="240" y1="1018" x2="840" y2="1018" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.5"/>

  <rect x="340" y="100" width="400" height="44" rx="22" fill="none" stroke="url(#goldGrad)" stroke-width="1" opacity="0.5"/>
  <text x="540" y="127" font-family="Arial, sans-serif" font-size="15" font-weight="600" letter-spacing="5" fill="#D4AF37" text-anchor="middle" opacity="0.85">STOIC WISDOM</text>

  <text x="940" y="190" font-family="serif" font-size="56" fill="{color}" text-anchor="end" opacity="0.9">{symbol}</text>
  <text x="940" y="220" font-family="Arial, sans-serif" font-size="18" font-weight="600" fill="{color}" text-anchor="end" letter-spacing="3" opacity="0.7">{sign_name}</text>
  <text x="940" y="240" font-family="Arial, sans-serif" font-size="11" fill="{color}" text-anchor="end" letter-spacing="1" opacity="0.4">{element}</text>

  <rect x="380" y="175" width="320" height="32" rx="16" fill="none" stroke="#C9A96E" stroke-width="0.8" opacity="0.4"/>
  <text x="540" y="196" font-family="Arial, sans-serif" font-size="12" font-weight="500" letter-spacing="2" fill="#C9A96E" text-anchor="middle" opacity="0.6">{esc(theme_upper)}</text>

  <line x1="250" y1="280" x2="830" y2="280" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.2"/>

  {quote_lines_svg}

  <line x1="400" y1="610" x2="680" y2="610" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <text x="540" y="640" font-family="Georgia, serif" font-size="22" font-style="italic" fill="#F5F5F5" text-anchor="middle" opacity="0.85">{esc(phil_label)}</text>

  <line x1="200" y1="770" x2="880" y2="770" stroke="#C9A96E" stroke-width="0.5" opacity="0.15"/>
  <text x="540" y="810" font-family="Arial, sans-serif" font-size="15" fill="#F5F5F5" text-anchor="middle" opacity="0.6">{esc(app_text)}</text>

  <rect x="340" y="860" width="400" height="38" rx="19" fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.5"/>
  <text x="540" y="885" font-family="Arial, sans-serif" font-size="12" font-weight="600" fill="#D4AF37" text-anchor="middle" letter-spacing="1">TODAY: {esc(challenge_text[:70])}</text>

  <text x="540" y="1000" font-family="Arial, sans-serif" font-size="12" fill="#F5F5F5" text-anchor="middle" opacity="0.3" letter-spacing="2">@STOICZODIAC</text>
</svg>'''


def generate_story_svg(sign, philosopher, prompt, caption):
    """Generate a 1080x1920 story SVG."""
    color = sign["color"]
    symbol = sign["symbol"]
    sign_name = sign["name"].upper()

    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

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
  <rect x="25" y="25" width="1030" height="1870" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.6"/>
  <rect x="35" y="35" width="1010" height="1850" fill="none" stroke="#D4AF37" stroke-width="0.5" opacity="0.25"/>

  <rect x="340" y="60" width="400" height="40" rx="20" fill="none" stroke="url(#goldGrad)" stroke-width="1" opacity="0.5"/>
  <text x="540" y="86" font-family="Arial, sans-serif" font-size="14" font-weight="600" letter-spacing="4" fill="#D4AF37" text-anchor="middle" opacity="0.85">DAILY STOIC</text>

  <text x="540" y="380" font-family="serif" font-size="100" fill="{color}" text-anchor="middle" opacity="0.9">{symbol}</text>
  <text x="540" y="450" font-family="Arial, sans-serif" font-size="28" font-weight="600" fill="{color}" text-anchor="middle" letter-spacing="4" opacity="0.8">{sign_name}</text>

  <line x1="300" y1="490" x2="780" y2="490" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>

  <text x="540" y="600" font-family="Georgia, serif" font-size="42" fill="#D4AF37" text-anchor="middle" font-style="italic" opacity="0.9">"</text>
  <text x="540" y="740" font-family="Arial, sans-serif" font-size="28" fill="#F5F5F5" text-anchor="middle" opacity="0.85">"{esc(prompt[:120])}"</text>

  <line x1="350" y1="820" x2="730" y2="820" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>

  <text x="540" y="880" font-family="Georgia, serif" font-size="20" font-style="italic" fill="#C9A96E" text-anchor="middle" opacity="0.7">Take 2 minutes today.</text>
  <text x="540" y="920" font-family="Arial, sans-serif" font-size="16" fill="#F5F5F5" text-anchor="middle" opacity="0.5">Write it down. Sit with it. Act on it.</text>

  <text x="540" y="1850" font-family="Arial, sans-serif" font-size="14" fill="#F5F5F5" text-anchor="middle" opacity="0.25" letter-spacing="3">@STOICZODIAC</text>
</svg>'''


# ── Process one week ──
def process_week(week_folder, generate_pngs=False):
    """Generate SVGs for one week folder. Returns True if any were generated."""
    quotes_dir = week_folder / "quotes"
    stories_dir = week_folder / "stories"
    quotes_svg_dir = week_folder / "quotes_svg"
    stories_svg_dir = week_folder / "stories_svg"

    # Check for existing generated SVGs
    existing_quotes = list(quotes_svg_dir.glob("*.svg")) if quotes_svg_dir.exists() else []
    existing_stories = list(stories_svg_dir.glob("*.svg")) if stories_svg_dir.exists() else []

    # Gather quote .md files
    quote_files = sorted(quotes_dir.glob("*_quote.md"))
    story_files = sorted(stories_dir.glob("*_story.md"))

    if not quote_files:
        return False

    any_generated = False

    # Create output dirs
    quotes_svg_dir.mkdir(parents=True, exist_ok=True)
    stories_svg_dir.mkdir(parents=True, exist_ok=True)

    week_name = week_folder.name

    for qf in quote_files:
        stem = qf.stem.replace("_quote", "").replace(".md", "")
        svg_path = quotes_svg_dir / f"{stem}_quote.svg"

        if svg_path.exists():
            continue

        try:
            data = parse_quote_file(qf)
        except Exception as e:
            print(f"  ⚠  Failed to parse {qf.name}: {e}")
            continue

        sign = sign_map.get(data["sign_id"])
        if not sign:
            print(f"  ✗ Unknown sign: {data['sign_id']} in {qf.name}")
            continue

        svg = generate_quote_svg(
            sign,
            data["philosopher"],
            data["theme"],
            data["quote"],
            data["application"],
            data["challenge"],
        )
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  ✓ {svg_path.name}")
        any_generated = True

    for sf in story_files:
        stem = sf.stem.replace("_story", "").replace(".md", "")
        caption_path = stories_dir.parent / "captions" / f"{stem}_caption.md"
        svg_path = stories_svg_dir / f"{stem}_story.svg"

        if svg_path.exists():
            continue

        try:
            prompt = parse_story_file(sf)
            caption = ""
            if caption_path.exists():
                caption = parse_caption_file(caption_path)
        except Exception as e:
            print(f"  ⚠  Failed to parse {sf.name}: {e}")
            continue

        # Extract sign from story filename
        sign_id = None
        for sid in sign_map:
            if sid in sf.stem.lower():
                sign_id = sid
                break
        sign = sign_map.get(sign_id or "")
        if not sign:
            continue

        # Get philosopher from corresponding quote file
        philosopher = ""
        qf_candidate = quotes_dir / f"{stem}_quote.md"
        if qf_candidate.exists():
            data = parse_quote_file(qf_candidate)
            philosopher = data["philosopher"]

        svg = generate_story_svg(sign, philosopher, prompt, caption)
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  ✓ {svg_path.name}")
        any_generated = True

    return any_generated


def convert_to_pngs(week_folder):
    """Convert SVGs to PNGs using Playwright browser (headless Chrome).
    Also copies PNGs to the scheduler-accessible folders (quotes/, stories/)."""
    from playwright.sync_api import sync_playwright

    week_name = week_folder.name
    print(f"  Converting SVGs to PNGs...")

    jobs = [
        ("quotes_svg", "quotes_png", "quotes", 1080, 1080),
        ("stories_svg", "stories_png", "stories", 1080, 1920),
    ]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": 1920, "height": 1920},
        )

        for svg_dir_name, png_dir_name, copy_dir_name, w, h in jobs:
            svg_dir = week_folder / svg_dir_name
            png_dir = week_folder / png_dir_name
            copy_dir = week_folder / copy_dir_name
            if not svg_dir.exists():
                continue
            png_dir.mkdir(parents=True, exist_ok=True)
            copy_dir.mkdir(parents=True, exist_ok=True)

            for svg_file in sorted(svg_dir.glob("*.svg")):
                png_file = png_dir / svg_file.with_suffix(".png").name
                if not png_file.exists():
                    try:
                        svg_uri = svg_file.resolve().as_uri()
                        page.goto(svg_uri)
                        page.locator("svg").first.screenshot(
                            path=str(png_file),
                            scale="css",
                        )
                        print(f"    ✓ {png_file.name}")
                    except Exception as e:
                        print(f"    ✗ {png_file.name}: {e}")
                        continue

                # Also copy to scheduler-facing folder (quotes/ or stories/)
                dest = copy_dir / png_file.name
                if not dest.exists():
                    import shutil
                    shutil.copy2(str(png_file), str(dest))

        browser.close()


# ── Main ──
def main():
    parser = argparse.ArgumentParser(description="Generate SVG content for all weeks")
    parser.add_argument("--week", type=int, default=None, help="Specific week number to process")
    parser.add_argument("--png", action="store_true", help="Also convert to PNGs")
    args = parser.parse_args()

    # Find all week folders
    week_folders = sorted([d for d in SCHEDULED_DIR.iterdir()
                          if d.is_dir() and d.name.startswith("week_")])

    if not week_folders:
        print("❌ No week folders found in SCHEDULED/")
        return

    # Filter by week if specified
    if args.week is not None:
        from datetime import date, timedelta
        launch = date(2026, 8, 17)
        target_monday = launch + timedelta(weeks=args.week - 1)
        target_name = f"week_{target_monday.strftime('%Y%m%d')}"
        week_folders = [f for f in week_folders if f.name == target_name]
        if not week_folders:
            print(f"❌ Week folder '{target_name}' not found")
            print(f"   Available: {[f.name for f in SCHEDULED_DIR.iterdir() if f.is_dir() and f.name.startswith('week_')]}")
            return

    total_weeks = 0
    total_generated = 0

    for wf in week_folders:
        print(f"\n{'='*60}")
        print(f"  {wf.name}")
        print(f"{'='*60}")
        try:
            generated = process_week(wf, generate_pngs=args.png)
            if generated:
                total_generated += 1

            # Check if SVGs exist (either just generated or from before)
            svg_dir = wf / "quotes_svg"
            story_svg_dir = wf / "stories_svg"
            existing_svgs = list(svg_dir.glob("*.svg")) + list(story_svg_dir.glob("*.svg"))

            if existing_svgs:
                if not generated:
                    print(f"  {len(existing_svgs)} SVGs already exist")
                total_weeks += 1
                if args.png:
                    convert_to_pngs(wf)
            else:
                if not generated:
                    print(f"  No quote files found to process")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    print(f"\n{'='*60}")
    print(f"✅ Done! Processed content for weeks")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()