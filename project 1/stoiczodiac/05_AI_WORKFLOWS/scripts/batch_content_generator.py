#!/usr/bin/env python3
"""Batch Content Generator — Stoic Wisdom x Zodiac Signs
Generates a 30-day content calendar CSV + Markdown report.
Sources sign data from the canonical `sign_master_data.json`.

Usage: python batch_content_generator.py [--days 30] [--output-dir ../../03_CONTENT_CALENDAR/generated]
"""

import csv
import json
import os
import sys
from datetime import date, datetime, timedelta

# Path to the canonical sign data (single source of truth)
MASTER_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "sign_master_data.json",
)

REEL_TYPES = [
    "Quote Narration",
    "Sign Comparison",
    "Rapid Wisdom",
    "Philosopher Speaks",
]

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def load_sign_data(path=None):
    """Load canonical sign data from sign_master_data.json."""
    if path is None:
        path = MASTER_DATA_PATH
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_lookup(data):
    """Build lookup dicts from the master data for fast access."""
    sign_by_id = {s["id"]: s for s in data["signs"]}
    # Build a sign order list that mirrors the old hardcoded rotation
    # (signs cycled in order: Aries → Taurus → ... → Pisces)
    sign_order = [s["id"] for s in data["signs"]]  # 12 signs in canonical order
    return sign_by_id, sign_order


def generate_calendar(days=30, start_date=None, data=None):
    if data is None:
        data = load_sign_data()
    sign_by_id, sign_order = build_lookup(data)

    # The project launched Aug 17, 2026 (Monday).
    # Rotation index advances by the day offset from launch.
    LAUNCH_DATE = date(2026, 8, 17)
    rotation = data.get("30_day_rotation", [])

    if start_date is None:
        start_date = datetime.now().date()
        # Round to next Monday if not already Monday
        while start_date.weekday() != 0:  # 0 = Monday
            start_date += timedelta(days=1)

    # Compute how many days we've advanced since launch
    days_since_launch = (start_date - LAUNCH_DATE).days
    rotation_offset = max(0, days_since_launch)

    calendar = []
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        day_name = WEEKDAYS[current_date.weekday()]
        week_num = i // 7 + 1

        # Use the curated rotation, advancing by the date offset
        rot_idx = (rotation_offset + i) % max(len(rotation), 1)
        if rotation:
            day_entry = rotation[rot_idx]
            sign_id = day_entry["sign_id"]
            philosopher = day_entry["philosopher"]
            theme = day_entry["theme"]
        else:
            sign_id = sign_order[i % len(sign_order)]
            philosopher = sign_by_id[sign_id]["philosopher"]
            theme = ""

        sign = sign_by_id[sign_id]
        sign_name = sign["name"]
        sign_symbol = sign["symbol"]
        element = sign["element"]

        # Determine content types
        has_reel = day_name in ("Monday", "Wednesday", "Friday")
        reel_type = REEL_TYPES[i % 4] if has_reel else "No"

        has_carousel = "No"
        if day_name in ("Tuesday", "Friday"):
            has_carousel = "Yes - Sign Spotlight"
        elif day_name == "Sunday":
            has_carousel = "Yes - Weekly Forecast"

        daily_post = f"{sign_symbol} {sign_name} - {philosopher}"

        entry = {
            "Day": i + 1,
            "Date": current_date.strftime("%Y-%m-%d"),
            "WeekDay": day_name,
            "Week": f"Week {week_num}",
            "Sign": sign_name,
            "Symbol": sign_symbol,
            "Element": element,
            "Philosopher": philosopher,
            "Theme": theme,
            "DailyPost": daily_post,
            "Reel": reel_type,
            "Carousel": has_carousel,
            "Story": "Yes - Daily Prompt",
            "Status": "PENDING",
        }
        calendar.append(entry)

    return calendar


def export_csv(calendar, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=calendar[0].keys())
        writer.writeheader()
        writer.writerows(calendar)
    print(f"  CSV: {filepath}")


def export_markdown(calendar, filepath):
    groups = {}
    for entry in calendar:
        groups.setdefault(entry["Week"], []).append(entry)

    lines = []
    lines.append("# Content Calendar -- Stoic Wisdom x Zodiac Signs")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Days**: {len(calendar)}")
    lines.append(f"**Start Date**: {calendar[0]['Date']}")
    lines.append(f"**Source**: `sign_master_data.json`")
    lines.append("")
    lines.append("---")
    lines.append("")

    for week_name, entries in groups.items():
        lines.append(f"## {week_name}")
        lines.append("")
        header = "| Day | Date | WeekDay | Sign | Philosopher | Theme | Daily Post | Reel | Carousel | Story | Status |"
        lines.append(header)
        lines.append("|" + "|".join(["---"] * 11) + "|")
        for e in entries:
            row = f"| {e['Day']} | {e['Date']} | {e['WeekDay']} | {e['Symbol']} {e['Sign']} | {e['Philosopher']} | {e['Theme']} | {e['DailyPost']} | {e['Reel']} | {e['Carousel']} | {e['Story']} | {e['Status']} |"
            lines.append(row)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Legend")
    lines.append("- **Daily Post**: Square image (1080x1080) -- quote + sign")
    lines.append("- **Reel**: Video (1080x1920) -- narrated voiceover + visuals")
    lines.append("- **Carousel**: Multi-slide (1080x1080) -- deep dive or forecast")
    lines.append("- **Story**: Vertical (1080x1920) -- daily prompt")
    lines.append("- **Status**: PENDING / DONE / SCHEDULED / POSTED")
    lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  MD:  {filepath}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Stoic Zodiac content calendar")
    parser.add_argument("--days", type=int, default=30, help="Number of days to generate")
    parser.add_argument("--start-date", type=str, default=None,
                        help="Start date YYYY-MM-DD (default: next Monday)")
    parser.add_argument("--week", type=int, default=None,
                        help="Week number from launch (week 1 = Aug 17, 2026). Overrides --start-date")
    parser.add_argument("--output-dir", default=os.path.join("..", "..", "03_CONTENT_CALENDAR", "generated"),
                        help="Output directory")
    parser.add_argument("--master-data", default=None,
                        help="Path to sign_master_data.json (auto-detected by default)")
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    data = load_sign_data(args.master_data)

    # Resolve start date: --week → --start-date → next Monday
    start_date = None
    if args.week is not None:
        # Week 1 = Aug 17 (launch Monday)
        launch = date(2026, 8, 17)
        start_date = launch + timedelta(weeks=args.week - 1)
    elif args.start_date is not None:
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()

    calendar = generate_calendar(days=args.days, start_date=start_date, data=data)

    # Use the calendar's start date for the filename, not today
    date_str = calendar[0]["Date"].replace("-", "")  # YYYYMMDD
    if args.week is not None:
        csv_path = os.path.join(output_dir, f"week{args.week}_{date_str}.csv")
        md_path = os.path.join(output_dir, f"week{args.week}_{date_str}.md")
    else:
        csv_path = os.path.join(output_dir, f"content_calendar_{date_str}.csv")
        md_path = os.path.join(output_dir, f"content_calendar_{date_str}.md")

    export_csv(calendar, csv_path)
    export_markdown(calendar, md_path)

    print(f"\nGenerated {len(calendar)} days of content!")
    print("Data sourced from: sign_master_data.json (canonical)")
    print("\nNext step: Copy the output into ChatGPT using Prompt 1")
    print("from 05_AI_WORKFLOWS/prompts/master_prompt_library.md")
    print("\nTip: Run this weekly to generate next week's calendar")
    print("      To update sign data, edit 05_AI_WORKFLOWS/sign_master_data.json")


if __name__ == "__main__":
    main()