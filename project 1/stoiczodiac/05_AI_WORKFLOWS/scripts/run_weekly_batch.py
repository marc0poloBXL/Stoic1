#!/usr/bin/env python3
"""run_weekly_batch.py — One-command weekly batch routine.

Usage:
    python run_weekly_batch.py              # Stage the next un-staged week
    python run_weekly_batch.py --week 5     # Stage a specific week
    python run_weekly_batch.py --all        # Stage ALL remaining future weeks

Steps:
    1. Generate the weekly content calendar
    2. Create weekly folders in 11_MEDIA_LIBRARY/SCHEDULED/
    3. Write WEEKLY_BATCH_BRIEF.md with sign assignments and pre-filled prompts
    4. Update MASTER_PRODUCTION_TRACKER.md
    5. Log to BATCH_HISTORY.md
"""

import csv
import json
import os
import subprocess
import sys
from datetime import date, datetime, timedelta

# ── UTF-8 output for Windows terminals ──────────────────────────────────
if sys.platform == "win32" and sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  # Python 3.7+

# ── Paths (relative to this script) ──────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(SCRIPT_DIR, "..", ".."))
MEDIA_LIB = os.path.join(PROJECT_ROOT, "11_MEDIA_LIBRARY", "SCHEDULED")
GENERATED_DIR = os.path.join(PROJECT_ROOT, "03_CONTENT_CALENDAR", "generated")
MASTER_DATA = os.path.join(SCRIPT_DIR, "..", "sign_master_data.json")

LAUNCH_DATE = date(2026, 8, 17)  # Week 1 launch
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

REEL_TYPES_BY_DAY = {0: "Quote Narration", 2: "Rapid Wisdom", 4: "Quote Narration"}
# Mon=0, Wed=2, Fri=4 get Reels. Tuesday gets Spotlight, Sunday gets Forecast.

PHILOSOPHER_SHORT = {
    "Marcus Aurelius": "Marcus Aurelius",
    "Seneca": "Seneca",
    "Epictetus": "Epictetus",
    "Zeno": "Zeno",
    "Musonius Rufus": "Musonius Rufus",
}


# ── Helpers ──────────────────────────────────────────────────────────────

def compute_week_number(start_date):
    """Return which week number this Monday belongs to (1-indexed from launch)."""
    delta = (start_date - LAUNCH_DATE).days
    return delta // 7 + 1


def next_monday(from_date=None):
    """Return the next Monday from a given date (or today)."""
    if from_date is None:
        from_date = date.today()
    days_ahead = (7 - from_date.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7  # Always go forward to next Monday, not same-day
    return from_date + timedelta(days=days_ahead)


def load_sign_data():
    """Load canonical sign data."""
    with open(MASTER_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_sign_symbol(data, sign_id):
    """Get the Unicode symbol for a sign by ID."""
    for s in data["signs"]:
        if s["id"] == sign_id:
            return s["symbol"]
    return ""


def get_week_data(data, week_number, days=7):
    """Get the 7 day entries for a given week from the rotation."""
    start = LAUNCH_DATE + timedelta(weeks=week_number - 1)
    entries = []
    for i in range(days):
        d = start + timedelta(days=i)
        day_name = WEEKDAYS[d.weekday()]
        rot_idx = ((start - LAUNCH_DATE).days + i) % len(data["30_day_rotation"])
        rot = data["30_day_rotation"][rot_idx]
        entries.append({
            "date": d,
            "day_name": day_name,
            "sign_id": rot["sign_id"],
            "symbol": get_sign_symbol(data, rot["sign_id"]),
            "philosopher": rot["philosopher"],
            "theme": rot["theme"],
        })
    return entries


def format_date_range(entries):
    """Return 'Mon DD – Mon DD' for the first and last day."""
    start = entries[0]["date"]
    end = entries[-1]["date"]
    return f"{start.strftime('%b')} {start.day} – {end.strftime('%b')} {end.day}"


# ── Folder creation ─────────────────────────────────────────────────────

def create_week_folders(week_folder):
    """Create the weekly subfolder structure."""
    subs = ["quotes", "reels", "carousels", "stories", "captions"]
    for sub in subs:
        os.makedirs(os.path.join(week_folder, sub), exist_ok=True)
        # Create .gitkeep
        gitkeep = os.path.join(week_folder, sub, ".gitkeep")
        if not os.path.exists(gitkeep):
            with open(gitkeep, "w") as f:
                pass
    return week_folder


# ── Brief generation ─────────────────────────────────────────────────────

def build_prompt1(entries, week_number):
    """Build the pre-filled Prompt 1 query text."""
    lines = [
        "Generate 7 daily quote posts for a Stoic × Zodiac Instagram page.\n",
        f"Week {week_number} ({format_date_range(entries)}):",
    ]
    for e in entries:
        lines.append(f"- {e['date'].strftime('%a')}: {e['symbol']} {e['sign_id'].title()} + {e['philosopher']} — \"{e['theme']}\"")
    lines += [
        "",
        "For each day, provide:",
        "1. Day + date",
        "2. Zodiac sign",
        "3. A quote from the assigned philosopher matching the theme",
        "4. 2-3 sentence application to the sign's traits",
        "5. One-sentence daily challenge",
        "6. 5 hashtags",
        "",
        "Style: Direct \"you\" address, practical application, under 300 chars.",
    ]
    return "\n".join(lines)


def build_reel_table(entries):
    """Build a markdown reel schedule table."""
    lines = ["| Day | Sign | Reel Type | Duration |", "|-----|------|-----------|----------|"]
    for e in entries:
        day_idx = e["date"].weekday()
        if day_idx in REEL_TYPES_BY_DAY:
            reel_type = REEL_TYPES_BY_DAY[day_idx]
            dur = "15s" if reel_type == "Rapid Wisdom" else "20-25s"
            lines.append(f"| {e['date'].strftime('%a')} | {e['symbol']} {e['sign_id'].title()} | **{reel_type}** | {dur} |")
    if len(lines) == 1:
        return "*No reels this week*"
    return "\n".join(lines)


def build_format_column(e):
    """Determine format string for the 'Format' column."""
    day_idx = e["date"].weekday()
    parts = ["**Image**"]
    if day_idx in (0, 2, 4):
        parts.append("**Reel**")
    if day_idx in (1, 4):
        parts.append("**Carousel** (Sign Spotlight)")
    elif day_idx == 6:
        parts.append("**Carousel** (Weekly Forecast)")
    return " + ".join(parts)


def build_week_table(entries):
    """Build the 'Week at a Glance' markdown table."""
    lines = [
        "| Day | Date | Sign | Philosopher | Theme | Format |",
        "|-----|------|------|-------------|-------|--------|",
    ]
    for e in entries:
        lines.append(
            f"| {e['date'].strftime('%a')} | {e['date'].strftime('%b')} {e['date'].day} "
            f"| {e['symbol']} {e['sign_id'].title()} | {e['philosopher']} "
            f"| {e['theme']} | {build_format_column(e)} |"
        )
    return "\n".join(lines)


def build_brief(entries, week_number):
    """Generate the complete WEEKLY_BATCH_BRIEF.md content."""
    date_range = format_date_range(entries)
    prompt1 = build_prompt1(entries, week_number)
    reel_table = build_reel_table(entries)
    week_table = build_week_table(entries)

    count_reels = sum(1 for e in entries if e["date"].weekday() in REEL_TYPES_BY_DAY)
    count_carousels = sum(1 for e in entries if e["date"].weekday() in (1, 4, 6))

    return f"""# 📋 Weekly Batch Brief — Week {week_number}

**Dates**: {date_range}
**Status**: 🔵 STAGED (ready for batch production)
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 📦 Production Batch Checklist

- [ ] **Prompt 1** → Generate 7 daily quotes
- [ ] **Prompt 5** → Generate 7 captions
- [ ] **Design** 7 quote images in Canva → save to `quotes/`
- [ ] **Edit** {count_reels} Reels in CapCut → save to `reels/`
- [ ] **Carousel** ({count_carousels}) → `carousels/`
- [ ] **Write** 7 story prompts → `stories/`
- [ ] **Schedule/queue** all posts for the week
- [ ] **Pre-write** engagement comments (20)

---

## Week at a Glance

{week_table}

---

## Prompt 1 Pre-fill — Daily Quote Generator

Copy this into ChatGPT:

```
{prompt1}
```

---

## 🎬 Reel Schedule ({count_reels} this week)

{reel_table}

---

## 🎯 Content Targets

| Metric | Target |
|--------|--------|
| Quote Images | 7 (1080×1080) |
| Reels | {count_reels} (1080×1920, 15-30s) |
| Carousels | {count_carousels} |
| Stories | 7 (daily prompts) |
| Captions | 7 |
| Hashtag Sets | 7 |
"""


# ── Tracker update ───────────────────────────────────────────────────────

def update_tracker(week_number, date_range, week_folder_name):
    """Add or update the week entry in MASTER_PRODUCTION_TRACKER.md."""
    tracker_path = os.path.join(MEDIA_LIB, "MASTER_PRODUCTION_TRACKER.md")
    if not os.path.exists(tracker_path):
        return  # Tracker will be created separately

    week_line = f"## Week {week_number} — {date_range} 🟡 IN PROGRESS\n"
    with open(tracker_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Only add if not already present
    if f"## Week {week_number} —" in content:
        return  # Already tracked

    # Insert a full-line block before the first FUTURE line. Finding the marker
    # as a raw substring is wrong: it can land mid-line (inside a table row or a
    # caption), corrupting the tracker. Match whole lines that begin with the
    # marker instead.
    import re as _re
    new_block = f"""{week_line}

| Item | Status |
|------|--------|
| Batch brief | [OK]  |
| Quotes + Captions | □ |
| Reels | □ |
| Carousels | □ |
| Scheduled | □ |

> **Batch brief**: `{week_folder_name}/WEEKLY_BATCH_BRIEF.md`

---

"""

    lines = content.split("\n")
    future_line_idx = None
    for i, line in enumerate(lines):
        if _re.match(r"^\s*⚪ FUTURE", line):
            future_line_idx = i
            break

    if future_line_idx is not None:
        lines.insert(future_line_idx, new_block.rstrip("\n"))
    else:
        lines.append("")
        lines.append(new_block.rstrip("\n"))

    content = "\n".join(lines)

    with open(tracker_path, "w", encoding="utf-8") as f:
        f.write(content)


# ── Batch history ────────────────────────────────────────────────────────

def log_batch(week_number, date_range, week_folder_name):
    """Append a log entry to BATCH_HISTORY.md (idempotent — never duplicates)."""
    history_path = os.path.join(MEDIA_LIB, "BATCH_HISTORY.md")
    entry = f"| {datetime.now().strftime('%Y-%m-%d %H:%M')} | Week {week_number} | {date_range} | `{week_folder_name}` | [OK]  Staged |\n"

    # Dedupe by week folder: a re-run must not append a second row.
    if os.path.exists(history_path):
        existing = open(history_path, encoding="utf-8").read()
        if f"`{week_folder_name}`" in existing:
            print(f"  ⏭️  Batch history already has Week {week_number} — skipping")
            return
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(entry)
    else:
        with open(history_path, "w", encoding="utf-8") as f:
            f.write("# 📜 Batch History\n\n| Timestamp | Week | Dates | Folder | Status |\n|-----------|------|-------|--------|--------|\n")
            f.write(entry)


# ── Calendar generation (via subprocess) ─────────────────────────────────

def run_generator(week_number, days=7):
    """Run the batch_content_generator.py via subprocess.

    Raises on failure so callers don't log a failed stage as [OK].
    """
    gen_path = os.path.join(SCRIPT_DIR, "batch_content_generator.py")
    output_dir = GENERATED_DIR
    cmd = [sys.executable, gen_path, "--week", str(week_number), "--days", str(days),
           "--output-dir", output_dir]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=SCRIPT_DIR,
                            encoding="utf-8")
    if result.returncode != 0:
        raise RuntimeError(
            f"Generator failed (exit {result.returncode}): {result.stderr.strip()[:300]}"
        )
    return result.stdout


# ── Main ─────────────────────────────────────────────────────────────────

def stage_week(week_number):
    """Stage all batch materials for a single week number."""
    print(f"\n[Stage] Week {week_number}...")

    # Compute dates
    start = LAUNCH_DATE + timedelta(weeks=week_number - 1)
    end = start + timedelta(days=6)
    date_range = format_date_range([
        {"date": start},
        {"date": end},
    ])
    week_folder_name = f"week_{start.strftime('%Y%m%d')}"
    week_folder = os.path.join(MEDIA_LIB, week_folder_name)

    # 1. Generate calendar — abort the whole stage on failure so a broken run
    #    is never logged as [OK] Staged.
    print(f"  [Cal]  Generating calendar (Week {week_number}, {start} – {end})...")
    try:
        gen_output = run_generator(week_number)
    except RuntimeError as e:
        print(f"  [FAIL] {e}")
        print("  ✋ Aborting stage — generator failed, nothing was logged.")
        return None

    # 2. Create folders
    print(f"  [Dir]  Creating folders...")
    create_week_folders(week_folder)
    print(f"     {week_folder}/")

    # 3. Generate brief
    print(f"  [Doc]  Writing batch brief...")
    data = load_sign_data()
    entries = get_week_data(data, week_number)
    brief = build_brief(entries, week_number)
    brief_path = os.path.join(week_folder, "WEEKLY_BATCH_BRIEF.md")
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(brief)
    print(f"     {brief_path}")

    # 4. Update tracker
    print(f"  [Chrt]  Updating production tracker...")
    update_tracker(week_number, date_range, week_folder_name)

    # 5. Log history
    print(f"  📜 Logging batch history...")
    log_batch(week_number, date_range, week_folder_name)

    print(f"  [OK]  Week {week_number} staged successfully!")
    return week_number


def find_future_weeks():
    """Find all weeks (from next Monday) that are not yet staged."""
    staged = set()
    tracker_path = os.path.join(MEDIA_LIB, "MASTER_PRODUCTION_TRACKER.md")
    if os.path.exists(tracker_path):
        with open(tracker_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("## Week "):
                    try:
                        w = int(line.split(" ")[2])
                        staged.add(w)
                    except (IndexError, ValueError):
                        pass

    # What week number is next Monday?
    nm = next_monday()
    next_week = compute_week_number(nm)

    future = []
    for w in range(next_week, 100):  # 100 = safety cap
        if w not in staged:
            future.append(w)
        if len(future) >= 10:
            break  # Don't stage more than 10 weeks at a time
    return future


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Stage weekly batch production materials")
    parser.add_argument("--week", type=int, default=None,
                        help="Week number to stage (default: next un-staged week)")
    parser.add_argument("--all", action="store_true",
                        help="Stage ALL remaining future weeks")
    args = parser.parse_args()

    if args.week:
        stage_week(args.week)
    elif args.all:
        future = find_future_weeks()
        if not future:
            print("[Done]  All weeks are already staged!")
            return
        print(f"Staging {len(future)} weeks: {future}")
        for w in future:
            stage_week(w)
    else:
        future = find_future_weeks()
        if not future:
            print("[Done]  Next week is already staged!")
            return
        stage_week(future[0])

    print("\n[Done]  Batch routine complete!")


if __name__ == "__main__":
    main()