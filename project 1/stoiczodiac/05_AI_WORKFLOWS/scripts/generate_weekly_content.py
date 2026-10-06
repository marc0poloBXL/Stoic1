#!/usr/bin/env python3
"""
Content Generation Pipeline — Stoic Wisdom × Zodiac Signs
==========================================================
Reads the 90-day rotation and quote library to generate weekly content:
  - 7 daily quote files (quote + application + challenge)
  - 7 caption files (with hashtags)
  - 7 story prompt files

Usage:
  python generate_weekly_content.py --week 5
  python generate_weekly_content.py --week 5 --dry-run
  python generate_weekly_content.py --all
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # stoiczodiac/
DATA_DIR = PROJECT_ROOT / "05_AI_WORKFLOWS"
SCHEDULED_DIR = PROJECT_ROOT / "11_MEDIA_LIBRARY" / "SCHEDULED"

SIGN_MASTER_PATH = DATA_DIR / "sign_master_data.json"
QUOTE_LIBRARY_PATH = DATA_DIR / "stoic_quote_library.json"

# Launch date: Aug 17, 2026 (Monday = day 1 of rotation)
LAUNCH_DATE = datetime(2026, 8, 17)

# ── Load data ──────────────────────────────────────────────────────────────
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_sign_map(data):
    """Build {sign_id: sign_object} lookup."""
    return {s["id"]: s for s in data["signs"]}


def get_rotation_map(data):
    """Build {day_number: rotation_entry} lookup."""
    return {entry["day"]: entry for entry in data["30_day_rotation"]}


def get_quote_map(data):
    """Build {philosopher_name: [quotes]} lookup."""
    return data["quotes"]


# ── Week resolution ────────────────────────────────────────────────────────
def week_number_to_days(week_num):
    """Convert week number (1-based) to day range."""
    start_day = (week_num - 1) * 7 + 1
    end_day = week_num * 7
    return start_day, end_day


def week_number_to_date_range(week_num):
    """Get the Monday-Sunday date range for a week number."""
    monday = LAUNCH_DATE + timedelta(weeks=week_num - 1)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def week_number_to_folder_name(week_num):
    """Get the folder name for a week number."""
    monday, _ = week_number_to_date_range(week_num)
    return f"week_{monday.strftime('%Y%m%d')}"


def find_week_folder(week_num):
    """Locate the week folder, trying both exact and prefix match."""
    folder_name = week_number_to_folder_name(week_num)
    exact = SCHEDULED_DIR / folder_name
    if exact.exists():
        return exact

    # Try prefix match (in case folder has a suffix)
    for p in SCHEDULED_DIR.iterdir():
        if p.is_dir() and p.name.startswith(folder_name):
            return p

    return None


# ── Quote matching ─────────────────────────────────────────────────────────
def tag_similarity(q_tags, theme_words):
    """
    Score how well a quote's tags match a theme.
    Returns count of overlapping significant words.
    """
    theme_lower = theme_words.lower()
    # Extract significant words from theme (skip stopwords)
    stopwords = {"the", "a", "an", "in", "of", "to", "for", "with", "and", "is", "as", "within", "through", "your"}
    # Split theme into individual words
    theme_terms = set()
    for word in re.findall(r"[a-z]+", theme_lower):
        if word not in stopwords and len(word) > 2:
            theme_terms.add(word)

    # Check each tag against theme terms
    score = 0
    for tag in q_tags:
        tag_lower = tag.lower()
        for term in theme_terms:
            if term in tag_lower or tag_lower in term:
                score += 1
        # Bonus: exact tag match on any theme word
        if tag_lower in theme_terms:
            score += 2

    return score


def select_quote(quotes, theme, used_texts=None):
    """
    Pick the best-matching quote from a philosopher's list for a given theme,
    avoiding already-used quotes.
    """
    if used_texts is None:
        used_texts = set()

    scored = []
    for q in quotes:
        if q["text"] in used_texts:
            continue
        score = tag_similarity(q.get("tags", []), theme)
        scored.append((score, q))

    if not scored:
        return None

    # Sort by score descending, then pick highest
    scored.sort(key=lambda x: -x[0])
    return scored[0][1]


def format_application(sign_name, philosopher_name, quote_text, theme, element=None):
    """Generate a 2-3 sentence application of the quote to the sign.

    Templates are element-aware so, e.g., a water sign never gets
    "ground your natural fire" wording.
    """
    element_clauses = {
        "fire": "whose element drives you to lead with passion — let this wisdom temper your natural fire",
        "earth": "whose element makes you steady and deliberate — let this wisdom soften your fixed habits",
        "air": "whose element keeps you curious and analytical — let this wisdom bring your ideas to rest",
        "water": "whose element makes you deep and feeling — let this wisdom steady your shifting tide",
    }
    clause = element_clauses.get(element or "") or "whose element shapes how you meet the world"

    templates = [
        f"For {sign_name}, {clause}. "
        f"The lesson isn't in what you do, but in how you choose to see it. "
        f"This week, let this truth settle into your daily rhythm.",

        f"As a {sign_name}, your strength can become your shadow if left unchecked. "
        f"{philosopher_name} reminds you that real power isn't in force — it's in the quiet mastery of your own mind. "
        f"Carry this into your day like a compass.",

        f"{sign_name} energy is magnetic — but without intention, it scatters. "
        f"{philosopher_name} offers a tether: a reminder that your greatest work begins inward. "
        f"Let this quote sit with you today. Let it shape one decision.",
    ]
    # Pick template based on theme length to add variety
    idx = sum(ord(c) for c in theme + sign_name) % len(templates)
    return templates[idx]


def format_challenge(sign_name, theme, philosopher_name, quote_text):
    """Generate a one-sentence daily challenge."""
    challenges = [
        f"Today, {sign_name}: pause once before reacting. Ask yourself — is this in my control?",
        f"{sign_name}, your challenge today: notice one thing you've been clinging to, and loosen your grip.",
        f"Today, {sign_name}, act as if your character — not your reputation — is the only thing that matters.",
        f"{sign_name}, before noon, write down one fear. Then ask: is this real, or imagined?",
        f"Today, {sign_name}: do one small thing not for applause, but because it's right.",
        f"{sign_name}, try this: when frustration rises, take three breaths before speaking.",
        f"Today, {sign_name}, notice where you're seeking approval — and give it to yourself instead.",
    ]
    idx = sum(ord(c) for c in theme + philosopher_name) % len(challenges)
    return challenges[idx]


def format_caption(sign_name, sign_symbol, philosopher_name, quote_text, theme):
    """Generate a caption with hashtags."""
    captions = [
        f"{sign_symbol} {sign_name} — {theme}\n\n"
        f"\"{quote_text}\"\n"
        f"— {philosopher_name}\n\n"
        f"This morning's reminder: philosophy isn't about escaping the world. "
        f"It's about showing up fully — grounded, clear, and ready.\n\n"
        f"Which sign are you? Drop it below. 👇",
    ]

    # Build hashtag set
    hashtags = (
        f"#StoicWisdom #{sign_name} #{sign_name}Zodiac "
        f"#DailyStoic #{philosopher_name.replace(' ', '')} "
        f"#StoicPhilosophy #ZodiacWisdom #Mindfulness "
        f"#StoicMindset #AncientWisdom"
    )

    return captions[0] + "\n\n" + hashtags


def format_story_prompt(sign_name, sign_symbol, philosopher_name, theme):
    """Generate a daily story prompt."""
    prompts = [
        f"📜 {sign_symbol} Stoic Prompt | {sign_name}\n\n"
        f"\"{theme}\"\n\n"
        f"Journal this: Where in your life today can you apply one word of "
        f"{philosopher_name}'s wisdom? Write it down. Sit with it. Act on it.\n\n"
        f"#Stoiczodiac #DailyPrompt",

        f"⚡ {sign_symbol} {sign_name} | Daily Challenge\n\n"
        f"{philosopher_name} teaches us about {theme.lower()}.\n"
        f"Your move today: pick ONE thing you can control, and give it your full attention.\n"
        f"The rest? Let it be.\n\n"
        f"#Stoiczodiac #DailyStoic",
    ]
    idx = sum(ord(c) for c in theme) % len(prompts)
    return prompts[idx]


# ── Content generation ─────────────────────────────────────────────────────
def load_used_quotes(exclude_week_folder=None):
    """Scan all previously generated week folders for quote texts.

    Quote files embed the quote as `> "..."`, so we collect every quoted line
    across existing weeks to keep the used-quote set persistent between runs.
    Without this, quotes repeat across weeks.
    """
    used = set()
    if not SCHEDULED_DIR.exists():
        return used
    for folder in SCHEDULED_DIR.iterdir():
        if not folder.is_dir() or folder.name == "week_manual":
            continue
        if exclude_week_folder and folder == exclude_week_folder:
            continue
        quotes_dir = folder / "quotes"
        if not quotes_dir.exists():
            continue
        for f in quotes_dir.glob("*.md"):
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("> \""):
                    quote = line[3:].strip().strip('"')
                    if quote:
                        used.add(quote)
    return used


def generate_week_content(rotation_map, sign_map, quote_map, start_day, end_day, week_folder, dry_run=False):
    """Generate all content for one week's day range."""
    used_quotes = load_used_quotes(exclude_week_folder=week_folder if not dry_run else None)

    subfolders = {
        "quotes": week_folder / "quotes",
        "captions": week_folder / "captions",
        "stories": week_folder / "stories",
    }

    results = []

    rotation_len = len(rotation_map)

    for day_num in range(start_day, end_day + 1):
        # Rotation repeats every 90 days — wrap day numbers so weeks 14+
        # keep generating instead of silently skipping.
        wrapped_day = ((day_num - 1) % rotation_len) + 1
        entry = rotation_map.get(wrapped_day)
        if not entry:
            print(f"  ⚠️  Day {day_num}: no rotation entry found, skipping")
            continue

        sign_id = entry["sign_id"]
        philosopher = entry["philosopher"]
        theme = entry["theme"]

        sign = sign_map.get(sign_id)
        if not sign:
            print(f"  ⚠️  Day {day_num}: sign '{sign_id}' not found, skipping")
            continue

        sign_name = sign["name"]
        sign_symbol = sign["symbol"]

        # Get quotes for this philosopher
        philosopher_quotes = quote_map.get(philosopher, [])
        if not philosopher_quotes:
            print(f"  ⚠️  Day {day_num}: no quotes for {philosopher}, skipping")
            continue

        # Select best matching quote
        quote = select_quote(philosopher_quotes, theme, used_quotes)
        if not quote:
            print(f"  ⚠️  Day {day_num}: no unused quote for {philosopher}, reusing with lowest score")
            quote = select_quote(philosopher_quotes, theme)

        if not quote:
            print(f"  ⚠️  Day {day_num}: could not find any quote for {philosopher}")
            continue

        used_quotes.add(quote["text"])

        # Generate content
        application = format_application(sign_name, philosopher, quote["text"], theme, element=sign.get("element"))
        challenge = format_challenge(sign_name, theme, philosopher, quote["text"])
        caption = format_caption(sign_name, sign_symbol, philosopher, quote["text"], theme)
        story_prompt = format_story_prompt(sign_name, sign_symbol, philosopher, theme)

        # Quote file
        quote_content = (
            f"# {sign_symbol} {sign_name} — Day {day_num}\n"
            f"**Theme**: {theme}\n"
            f"**Philosopher**: {philosopher}\n"
            f"**Source**: {quote['source']}\n\n"
            f"## Quote\n"
            f"> \"{quote['text']}\"\n\n"
            f"## Application\n"
            f"{application}\n\n"
            f"## Daily Challenge\n"
            f"{challenge}\n"
        )

        # Caption file
        caption_content = (
            f"# Caption — {sign_symbol} {sign_name} (Day {day_num})\n"
            f"**Theme**: {theme}\n\n"
            f"{caption}\n"
        )

        # Story prompt file
        story_content = (
            f"# Story Prompt — {sign_symbol} {sign_name} (Day {day_num})\n\n"
            f"{story_prompt}\n"
        )

        # Date for filename
        monday = week_number_to_date_range((start_day - 1) // 7 + 1)[0]
        day_date = monday + timedelta(days=day_num - start_day)
        date_str = day_date.strftime("%Y-%m-%d")
        file_prefix = f"{date_str}_{sign_id}"

        # Track result in both dry-run and real mode
        result_entry = {
            "day": day_num,
            "date": date_str,
            "sign": sign_name,
            "symbol": sign_symbol,
            "philosopher": philosopher,
            "theme": theme,
            "quote": quote["text"],
        }

        if dry_run:
            print(f"  ✓ Day {day_num} ({date_str}): {sign_symbol} {sign_name} — {philosopher} — \"{theme}\"")
            print(f"    Quote: \"{quote['text'][:60]}...\"")
            results.append(result_entry)
            continue

        # Write files (skip if already exists)
        files_written = {}
        for folder_key, content, ext, desc in [
            ("quotes", quote_content, "md", "quote"),
            ("captions", caption_content, "md", "caption"),
            ("stories", story_content, "md", "story"),
        ]:
            folder = subfolders[folder_key]
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
            file_path = folder / f"{file_prefix}_{desc}.{ext}"
            if file_path.exists():
                print(f"     ⏭️  {desc} already exists, skipping")
                continue
            file_path.write_text(content, encoding="utf-8")
            files_written[folder_key] = file_path

        result_entry["files"] = files_written
        results.append(result_entry)

        print(f"  ✓ Day {day_num} ({date_str}): {sign_symbol} {sign_name} — {philosopher} — \"{theme}\"")

    return results


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Generate weekly content for Stoic Wisdom × Zodiac Signs")
    parser.add_argument("--week", type=int, help="Week number (1-19)")
    parser.add_argument("--all", action="store_true", help="Generate content for ALL weeks")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no files written")
    args = parser.parse_args()

    if not args.week and not args.all:
        parser.print_help()
        print("\n💡 Provide --week N or --all to generate content")
        sys.exit(1)

    # Load data
    print("📚 Loading sign master data...")
    sign_data = load_json(SIGN_MASTER_PATH)
    sign_map = get_sign_map(sign_data)
    rotation_map = get_rotation_map(sign_data)

    print("📖 Loading quote library...")
    quote_data = load_json(QUOTE_LIBRARY_PATH)
    quote_map = get_quote_map(quote_data)

    # Summary stats
    total_quotes = sum(len(q) for q in quote_map.values())
    print(f"\n📊 Data loaded: {len(sign_map)} signs, {max(rotation_map.keys())} days in rotation, {total_quotes} quotes\n")

    # Determine weeks to process
    if args.all:
        max_day = max(rotation_map.keys())
        max_week = (max_day + 6) // 7
        weeks = list(range(1, max_week + 1))
        print(f"🏗️  Generating content for ALL {len(weeks)} weeks (days 1-{max_day})...\n")
    else:
        weeks = [args.week]
        print(f"🏗️  Generating content for Week {args.week}...\n")

    total_days = 0
    total_files = 0

    for week_num in weeks:
        start_day, end_day = week_number_to_days(week_num)
        monday, sunday = week_number_to_date_range(week_num)
        week_folder = find_week_folder(week_num)

        if not week_folder:
            print(f"\n⚠️  Week {week_num} ({monday.date()} — {sunday.date()}): folder not found, creating")
            folder_name = week_number_to_folder_name(week_num)
            week_folder = SCHEDULED_DIR / folder_name
            week_folder.mkdir(parents=True, exist_ok=True)
            # Create subfolders
            for sub in ["quotes", "captions", "stories", "reels", "carousels"]:
                (week_folder / sub).mkdir(exist_ok=True)

        print(f"\n{'='*60}")
        print(f"  Week {week_num}: {monday.strftime('%b %d')} — {sunday.strftime('%b %d')}, {sunday.year}")
        print(f"  Days {start_day}-{end_day} of rotation")
        print(f"  Location: {week_folder}")
        print(f"{'='*60}")

        results = generate_week_content(
            rotation_map, sign_map, quote_map,
            start_day, end_day, week_folder,
            dry_run=args.dry_run,
        )

        total_days += len(results)
        total_files += len(results) * 3  # quote + caption + story per day

    # Summary
    print(f"\n{'='*60}")
    if args.dry_run:
        print(f"\n🔍 DRY RUN COMPLETE — No files written")
        print(f"   Would process: {total_days} days × 3 files = {total_files} files")
        print(f"\n   Run without --dry-run to generate:")
        print(f"   python generate_weekly_content.py --week {args.week if args.week else 'N'}")
    else:
        print(f"\n✅ GENERATION COMPLETE")
        print(f"   Processed: {total_days} days across {len(weeks)} week(s)")
        print(f"   Created: ~{total_files} files (quotes, captions, story prompts)")
        print(f"   Location: {SCHEDULED_DIR}/week_YYYYMMDD/")
        print(f"\n   📌 Next steps:")
        print(f"      1. Review generated content in each week's folders")
        print(f"      2. Design quote images in Canva")
        print(f"      3. Edit Reels in CapCut")
        print(f"      4. Build Carousels per batch brief")
        print(f"      5. Schedule/queue all posts for the week")


if __name__ == "__main__":
    main()