# Stoic Scheduler — Instagram Auto-Poster

A self-hosted tool that posts images, carousels, reels, and stories
to Instagram on a schedule. Replaces Later.com / Buffer.

**How it posts each content type:**

| Type | Method | Why |
|------|--------|-----|
| 🖼️ Single images | **Playwright** browser automation | Works without API setup, no hosting needed |
| 🎠 Carousels | **Meta Graph API** | Official API, supports multi-image |
| 🎬 Reels | **Meta Graph API** | Official API, supports video + caption |
| 📖 Stories | **Meta Graph API** | Official API, supports image + ephemeral |

**To use carousels/reels/stories**, set up the Meta API + Vercel Blob:
see `META_SETUP_GUIDE.md` (one-time ~30 min setup).

**What still needs the mobile app:**
- Nothing — all four content types are automated.

---

## Setup

### 1. Install Python dependencies

Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure credentials

```bash
copy .env.example .env
```

Then edit `.env` and fill in your Instagram password:

```
INSTAGRAM_USERNAME=stoiczodiac
INSTAGRAM_PASSWORD=your_actual_password_here
```

> **⚠️ Never commit .env to git.** It's already in `.gitignore`.

### 3. Verify configuration

```bash
python scheduler.py --validate-config
```

### 4. Test with a dry run

Drop a test image (PNG) and a matching `.txt` caption file into the `queued/` folder:

```
queued/
├── 2026-10-05_scorpio_quote.png
└── 2026-10-05_scorpio_quote.txt    ← same name, .txt extension
```

Then run:

```bash
python scheduler.py --dry-run
```

### 5. Post a test

```bash
python scheduler.py --post-now
```

This opens a browser, logs in, and posts. Watch it the first time to make sure everything works.

---

## Daily Usage

### Import from batch folders

After generating a week's content:

```bash
python scheduler.py --import-only
```

This scans `11_MEDIA_LIBRARY/SCHEDULED/week_*/` for single images + captions and copies them into `queued/`. Also imports carousels, reels, and stories if they exist in the batch folders.

### Check queue status

```bash
python scheduler.py --status
```

### Force post now

```bash
python scheduler.py --post-now
```

### Verify Meta API

After completing `META_SETUP_GUIDE.md`, test your setup:

```bash
python scheduler.py --meta-verify
```

---

## Queue Structure

Different content types go in different queue folders:

| Content | Queue folder | File format |
|---------|-------------|-------------|
| Single image | `queued/` | `.png` + `.txt` caption |
| Carousel | `queued_carousels/<name>/` | `1.png`, `2.png`... + `caption.txt` |
| Reel | `queued_reels/` | `.mp4` + `.txt` caption |
| Story | `queued_stories/` | `.jpg/.png` + optional `.txt` |

Auto-import from weekly batch folders automatically places files into the right queue folders.

---

## Windows Task Scheduler Setup

To make it post automatically every 15 minutes:

1. Open **Task Scheduler** (search "Task Scheduler" in Start menu)
2. Click **Create Basic Task**
3. **Name**: "Stoic Scheduler"
4. **Trigger**: "Repeat every 15 minutes", every day
5. **Action**: Start a program
   - **Program**: `python.exe` (find the path with `where python`)
   - **Arguments**: `scheduler.py`
   - **Start in**: The full path to this folder
6. Click Finish

The script is lightweight — it checks the time, and only posts if it's within 2 minutes of a scheduled slot. The rest of the time it exits immediately.

---

## Scheduling Customization

Edit `config.yaml` to change posting times:

```yaml
schedule:
  times:
    monday:    ["07:00", "12:00", "18:00"]
    tuesday:   ["07:00", "12:00", "18:00"]
    # ... etc
```

Format: 24-hour, colon-separated. Add or remove slots per day as needed.

---

## File Structure

```
stoic_scheduler/
├── scheduler.py          ← Run this
├── config.yaml           ← Schedule, paths, settings
├── .env                  ← Credentials (gitignored)
├── META_SETUP_GUIDE.md   ← Meta API + Blob setup guide
├── requirements.txt      ← Python packages
├── login_manager.py      ← Login + cookie handling (Playwright)
├── instagram_bot.py      ← Playwright browser automation (single images)
├── meta_api.py           ← Meta Graph API client (carousels, reels, stories)
├── media_uploader.py     ← Vercel Blob upload/cleanup
├── queue_handler.py      ← Queue management (all 4 content types)
├── logger.py             ← Logging utility
├── queued/               ← Drop single images here
├── queued_carousels/     ← Subfolders with carousel slides
├── queued_reels/         ← MP4 video files
├── queued_stories/       ← Story images
├── posted/               ← Archived posts (with CSV log)
├── cookies/              ← Session cookies (gitignored)
├── logs/                 ← Runtime logs (gitignored)
└── failed/               ← Failed items (gitignored)
```

---

## Troubleshooting

| Problem | Likely Cause |
|---------|-------------|
| "No saved session" | First run, or cookies expired. Login happens automatically. |
| Login fails | Check password in `.env`. Instagram may require 2FA. |
| 2FA challenge | Enter the code manually when prompted in the log. |
| Post fails silently | Run with `headless: false` in config to watch the browser. |
| "Rate limited" | Wait an hour. The tool auto-cooldowns. |
| Image won't post | Check it's a valid PNG/JPG under 5MB. |