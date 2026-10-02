# 🎨 Production Workflow — Stoic Wisdom × Zodiac Signs

## Quick Reference

| Content Type | Format | Frequency | Tools |
|-------------|--------|-----------|-------|
| Daily Quote | 1080×1080 px | 1x/day (7x/week) | Leonardo AI + Canva |
| Sign Spotlight Carousel | 1080×1080 px (5-7 slides) | 2x/week | Canva |
| Reel | 1080×1920 px (15-30s) | 3x/week | CapCut |
| Weekly Forecast Carousel | 1080×1080 px (10 slides) | 1x/week | Canva |
| Story Prompt | 1080×1920 px | 1x/day | Canva |

---

## 1. Leonardo AI — Sign Background Images

Generate ONE base image per sign using these prompts. Style: dark, marble statues, dramatic lighting.

### Sign Prompts

| Sign | Prompt | Style Notes |
|------|--------|-------------|
| ♈ Aries | Marble ram statue, firelight glow, dramatic shadows, cinematic | Warm tones, red/orange |
| ♉ Taurus | Marble bull statue, earthy tones, moss accents, ancient | Green/brown, grounded |
| ♊ Gemini | Dual marble bust, split lighting, mirror effect, symmetrical | Yellow/gold, divided |
| ♋ Cancer | Moonlit marble crab, ocean mist, silver highlights, ethereal | Blue/silver, watery |
| ♌ Leo | Marble lion statue, golden hour light, majestic, royal | Gold/orange, grand |
| ♍ Virgo | Marble maiden statue, wheat fields, soft light, pure | Brown/cream, clean |
| ♎ Libra | Marble scales, balanced light, harmony, gold accents | Blue/gold, balanced |
| ♏ Scorpio | Marble scorpion, deep purple shadows, intense, dramatic | Purple/dark, intense |
| ♐ Sagittarius | Marble archer, celestial arrows, starry background, dynamic | Blue/star, adventurous |
| ♑ Capricorn | Marble sea-goat, mountain peaks, ancient, weathered | Dark green, stoic |
| ♒ Aquarius | Marble water bearer, flowing light, electric blue, visionary | Cyan/blue, futuristic |
| ♓ Pisces | Marble fish, ocean depths, bioluminescent, dreamy | Teal/dreamy, fluid |

### Leonardo AI Settings

```
Preset: Cinematic / Photography
Ratio: 1:1 (for quotes), 9:16 (for stories/reels)
Style: Dark, atmospheric, minimalist
Lighting: Low-key, dramatic
Output: 1 image per sign, download as PNG
```

**Save to**: `01_BRAND_ASSETS/graphics/` as `bg_{sign_id}.png`

---

## 2. Canva — Template Setup

### Create These Templates in Canva

#### A. Quote Card Template (1080×1080)
```
┌──────────────────────┐
│  ♈                   │  ← Sign symbol top-right (sign color, 36pt Cormorant Garamond)
│                      │
│  ┌──────┐ ┌────────┐ │
│  │      │ │ "The   │ │  ← Left: sign background image
│  │ Image│ │ happi- │ │  ← Right: quote text (Playfair Display Italic, 48-64pt, Gold #D4AF37)
│  │      │ │ ness..."│ │
│  └──────┘ └────────┘ │
│                      │
│  — Marcus Aurelius   │  ← Raleway Light 20pt, White #F5F5F5
│                      │
│  @stoiczodiac        │  ← Watermark bottom-right, 10pt
└──────────────────────┘
```

**Steps to create:**
1. New Canva design → Custom size 1080×1080
2. Background: `#0A0A0A`
3. Add sign image (left half) with rounded corners
4. Add text box (right half):
   - Font: Playfair Display Italic
   - Size: 48-64pt
   - Color: `#D4AF37`
5. Add philosopher attribution: Raleway Light 20pt, `#F5F5F5`
6. Add sign symbol top-right: Cormorant Garamond 36pt, sign color
7. Add `@stoiczodiac` watermark bottom-right
8. Save as template → name: `Quote Card - [SIGN]`

#### B. Carousel Template (1080×1080, multi-page)

**Slide 1 — Title**: Sign symbol + "The Stoic Path of [THEME]"  
**Slides 2-3 — Strengths**: "3 Natural Gifts" with bullet points  
**Slides 4-5 — Shadow**: "2 Traps to Watch For"  
**Slide 6 — Wisdom**: Philosopher quote + application  
**Slide 7 — Practice**: Daily exercise + CTA  

Each slide: dark background `#1A1A2E`, sign color accents, gold text for headings.

#### C. Story Template (1080×1920)
```
Full-bleed sign background image
→ Dark gradient overlay (top 40%)
→ Quote text center (Playfair Display, 36pt, Gold)
→ Sign symbol bottom-left (48pt)
→ "Swipe up for your daily wisdom" bottom
```

#### D. Reel Cover Template (1080×1920)
```
Solid #0A0A0A background
→ Large sign symbol center (120pt)
→ "STOIC WISDOM" top (Cormorant Garamond, Gold)
→ Sign name below (Raleway, 28pt, White)
→ "@stoiczodiac" bottom
```

---

## 3. Weekly Batch Production (Every Sunday)

### Step 1: Run the generator (1 min)
```bash
cd "05_AI_WORKFLOWS/scripts"
python run_weekly_batch.py
```
This creates the weekly folder in `11_MEDIA_LIBRARY/SCHEDULED/week_YYYYMMDD/` with pre-filled prompts.

### Step 2: Generate quotes via ChatGPT (10 min)
1. Open `WEEKLY_BATCH_BRIEF.md` → copy **Prompt 1**
2. Paste into ChatGPT → get 7 daily quotes
3. Save to `week_YYYYMMDD/quotes/quote_text.txt`

### Step 3: Generate carousels (15 min)
1. Copy **Prompt 2** from `05_AI_WORKFLOWS/prompts/master_prompt_library.md`
2. Replace `[SIGN NAME]` with this week's signs
3. Paste into ChatGPT → get 2 carousels
4. Save to `week_YYYYMMDD/carousels/`

### Step 4: Design in Canva (30 min)
1. **Quote cards**: Open template → paste quote text → replace sign image → export 7 PNGs
2. **Carousels**: Open template → paste content → export as PDF (multi-page)
3. **Stories**: Open template → paste quote → export as PNG

### Step 5: Edit Reels in CapCut (20 min)
1. Import sign background video (Pexels) + voiceover (from `07_AUDIO/voiceover_audio/`) + music (from `07_AUDIO/music/royalty_free/` — ambient piano tracks)
2. Add captions (Raleway 16pt, White)
3. Export as 1080×1920 MP4 → save to `week_YYYYMMDD/reels/`

> **Audio files are already pre-recorded**: All 12 sign voiceovers + daily prompts are in `07_AUDIO/voiceover_audio/`. Mixed versions (voiceover + music combined) are in `voiceover_audio/mixed/`. Reel scripts are in `07_AUDIO/voiceover_scripts/reel_voiceover_bank.md`.

---

## 4. Complete Color & Font Reference

### Backgrounds
| Element | Color | Usage |
|---------|-------|-------|
| Feed BG | `#0A0A0A` | Quote cards, reel covers |
| Carousel BG | `#1A1A2E` | Carousel slides |
| Gold accent | `#D4AF37` | Headlines, borders |
| White text | `#F5F5F5` | Body text |
| Bronze | `#C9A96E` | Subtitles |

### Typography
| Role | Font | Where to Get |
|------|------|-------------|
| Headlines | Cormorant Garamond | Google Fonts (free) |
| Body | Raleway | Google Fonts (free) |
| Quotes | Playfair Display | Google Fonts (free) |

---

## 5. 30-Day Sign Rotation

The sign rotation is 90 days long (repeats quarterly). Each day maps a sign to a philosopher + theme. Source: `05_AI_WORKFLOWS/sign_master_data.json`.

**Philosopher rotation per sign:**
| Sign | Primary | Secondary | Tertiary |
|------|---------|-----------|----------|
| Aries | Marcus Aurelius | Seneca | Epictetus |
| Taurus | Seneca | Marcus Aurelius | Zeno |
| Gemini | Epictetus | Marcus Aurelius | Seneca |
| Cancer | Marcus Aurelius | Epictetus | Seneca |
| Leo | Seneca | Marcus Aurelius | Epictetus |
| Virgo | Epictetus | Marcus Aurelius | Seneca |
| Libra | Marcus Aurelius | Epictetus | Seneca |
| Scorpio | Seneca | Marcus Aurelius | Epictetus |
| Sagittarius | Epictetus | Marcus Aurelius | Seneca |
| Capricorn | Marcus Aurelius | Seneca | Epictetus |
| Aquarius | Seneca | Epictetus | Marcus Aurelius |
| Pisces | Epictetus | Marcus Aurelius | Seneca |

---

## 6. File Organization

```
01_BRAND_ASSETS/
  graphics/      ← Leonardo AI sign background images
  fonts/         ← Downloaded font files
  colors/        ← Color palette reference
04_TEMPLATES/
  canva-app/     ← Canva app code
  PRODUCTION_WORKFLOW.md  ← THIS FILE
05_AI_WORKFLOWS/
  sign_master_data.json   ← Single source of truth (all 12 signs)
  scripts/        ← Python + JS generators
  prompts/        ← AI prompt library
11_MEDIA_LIBRARY/
  SCHEDULED/
    week_YYYYMMDD/
      quotes/      ← 7 quote PNGs
      carousels/   ← 2 carousel PDFs
      reels/       ← 3 reel MP4s
      stories/     ← 7 story PNGs
```

---

## 7. Quick Canva Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New design | `Cmd/Ctrl + N` |
| Duplicate page | `Cmd/Ctrl + D` |
| Export as PNG | `Cmd/Ctrl + Shift + E` |
| Text color | Select text → top toolbar → color picker |
| Add rounded corners | Select element → corner radius slider |