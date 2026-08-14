# Canva Setup Guide — Stoic Wisdom × Zodiac Signs

**Tool**: Canva (free tier) + Canva Developer App  
**Goal**: 3 reusable templates → batch 30 posts in 2 hours  
**App**: [`canva-app/`](./canva-app/) — React/Express developer app for AI image generation

---

## ✅ Step 1: Brand Kit Setup

1. Open Canva → **Brand Kit** (free: limited to 1 brand kit)
2. Upload **Brand Colors** (from brand_guidelines.md):
   - `#0A0A0A` Deep Void
   - `#1A1A2E` Midnight Blue
   - `#D4AF37` Stoic Gold
   - `#F5F5F5` Marble White
   - `#C9A96E` Aged Bronze
3. Upload **Fonts** (or use Canva equivalents):
   - Cormorant Garamond → Search "Cormorant Garamond" (free)
   - Raleway → Search "Raleway" (free)
   - Playfair Display → Search "Playfair Display" (free)
4. Upload **Logo** (create in Canva):
   - Search "zodiac wheel" → Add to canvas
   - Add text "STOIC" on top, "WISDOM" on bottom
   - Download as PNG → Upload to Brand Kit

---

## ✅ Step 2: Template 1 — Daily Quote Card (1080×1080)

### Create Once
1. New design → 1080×1080 px
2. Background: `#0A0A0A` (full canvas)
3. Add subtle texture: Elements → "marble texture" → opacity 10%
4. Add zodiac sign text (top-right): Font "Cormorant Garamond", 36pt, sign color
5. Add quote text (center): Font "Playfair Display", 48pt, `#D4AF37`
6. Add philosopher name (bottom-left): Font "Raleway", 20pt, `#F5F5F5`, light
7. Add watermark (bottom-right): "@stoiczodiac", 10pt, opacity 50%
8. Add subtle border: 2px gold line, 40px from edge

### Save as Template
- **File** → **Save as template**
- Name: "Daily Quote Template"
- Add to folder: "STOIC ZODIAC"

### Batch Production
1. Open template
2. Replace sign text + color
3. Replace quote text
4. Replace philosopher name
5. Download → "daily_[sign]_[date].png"
6. Repeat × 30 (takes ~3 min per post after setup)

---

## ✅ Step 3: Template 2 — Carousel (1080×1080, 7 pages)

### Create Once
1. New design → 1080×1080 px → **Add pages** (7 total)
2. **Page 1 (Title)**: 
   - Background: `#1A1A2E`
   - Sign icon (large, center): 120pt
   - Title text: "THE STOIC PATH", 36pt, Gold
   - Subtitle: "[SIGN NAME]", 24pt, sign color
3. **Page 2-6 (Content)**:
   - Background: `#0A0A0A`
   - Top: Section label (bold, 18pt, Gold)
   - Center: Content text (20pt, White)
   - Bottom: Page number (X/7, 12pt, Grey)
4. **Page 7 (CTA)**:
   - Background: `#1A1A2E`
   - Text: "Save this for your sign."
   - Text: "Follow @stoiczodiac"

### Save as Template
- Name: "Carousel — Sign Spotlight"

---

## ✅ Step 4: Template 3 — Story (1080×1920)

### Create Once
1. New design → 1080×1920 px
2. Background: Full-bleed image (search Pexels in Canva: "marble", "stars", "ocean")
3. Top: Sign icon + name (24pt, sign color)
4. Center: Quote text (42pt, White, with drop shadow)
5. Bottom: CTA (18pt, Gold) + @ handle
6. Add: "Swipe up" arrow (small, bottom)

### Save as Template
- Name: "Story — Daily Prompt"

---

## ✅ Step 5: Visual Assets — Stock Image Sources

### In-Canva (Free)
| Search Term | Best For | Type |
|-------------|----------|------|
| "Marble bust" | Stoic philosopher images | Elements |
| "Statue" | Ancient aesthetic | Elements |
| "Meditation" | Zen visuals | Photos |
| "Starry sky" | Cosmic background | Photos |
| "Candle" | Contemplative mood | Photos |
| "Nature landscape" | Element backgrounds | Photos |
| "Ripple" | Water effect | Elements |
| "Gold texture" | Overlays | Elements |

### External (Free, No Attribution)
| Site | License | Best For |
|------|---------|----------|
| [Pexels](https://pexels.com) | Free | Stock photos |
| [Pixabay](https://pixabay.com) | Free | Stock photos + vectors |
| [Unsplash](https://unsplash.com) | Free | High-quality photos |
| [Leonardo AI](https://leonardo.ai) | 150 credits/day | Custom AI images |

---

## ✅ Step 6: Leonardo AI — Custom Image Generation

**Use for**: Unique bust images, zodiac-themed AI art, philosopher portraits

> **Note on the Canva Developer App** (`canva-app/`): The Canva app is a
> general-purpose AI image generator — it lets users type any prompt and get
> AI-generated images. It does **not** have preset Stoic Zodiac themes.
> The prompts below are for **manual use** in Leonardo AI's web interface
> (https://leonardo.ai) when creating custom assets outside of Canva.
> If you build a feature to add preset theme buttons to the Canva app,
> these prompts are a good starting point.

### Leonardo AI Prompt Template
```
Marble bust of an ancient Greek philosopher, dramatic lighting,
dark background, gold accents, photorealistic, cinematic,
museum quality, 8K, --ar 1:1
```

### Sign-Specific Image Prompts
| Sign | Prompt |
|------|--------|
| ♈ Aries | Marble ram statue, firelight glow, dramatic shadows, cinematic |
| ♉ Taurus | Marble bull statue, earthy tones, moss accents, ancient |
| ♊ Gemini | Dual marble bust, split lighting, mirror effect, symmetrical |
| ♋ Cancer | Moonlit marble crab, ocean mist, silver highlights, ethereal |
| ♌ Leo | Marble lion statue, golden hour light, majestic, royal |
| ♍ Virgo | Marble maiden statue, wheat fields, soft light, pure |
| ♎ Libra | Marble scales, balanced light, harmony, gold accents |
| ♏ Scorpio | Marble scorpion, deep purple shadows, intense, dramatic |
| ♐ Sagittarius | Marble archer, celestial arrows, starry background, dynamic |
| ♑ Capricorn | Marble sea-goat, mountain peaks, ancient, weathered |
| ♒ Aquarius | Marble water bearer, flowing light, electric blue, visionary |
| ♓ Pisces | Marble fish, ocean depths, bioluminescent, dreamy |

### Workflow
1. Leonardo AI → Generate image → Download
2. Upload to Canva → Place in template
3. Add text overlays → Export

---

---

## 📁 Templates Directory

```
04_TEMPLATES/
├── canva_setup_guide.md        ← This file
├── canva-app/                   ← Developer app (React + Express backend)
│   ├── src/                     ← Frontend components
│   ├── backend/                 ← Express API server
│   └── README.md               ← Full setup guide
├── reels/
│   └── reel_template_guide.md   ← 3 reel templates (1080×1920)
├── carousels/
│   └── carousel_template_guide.md  ← 4 carousel templates (1080×1080)
└── stories/
    └── (story templates go here)
```

---

### Reels & Carousels

For dedicated template guides with page-by-page breakdowns, sign-specific colors, batch workflows, and detailed Canva creation steps:

- **Reels** → [`reels/reel_template_guide.md`](./reels/reel_template_guide.md) (3 templates: Quote, Sign Spotlight, Daily Prompt)
- **Carousels** → [`carousels/carousel_template_guide.md`](./carousels/carousel_template_guide.md) (4 templates: Sign Spotlight, Stoic Lesson, Element Series, Quick Quote)

### Canva Developer App

The [`canva-app/`](./canva-app/) directory contains a Canva Connect developer app for AI image generation:

```bash
cd "project 1/stoiczodiac/04_TEMPLATES/canva-app"
cp .env.template .env
# Edit .env → add your CANVA_APP_ID
npm start
```

See [`canva-app/README.md`](./canva-app/README.md) for the full API reference.

---

## ⚡ Quick-Start: First Batch Session

```
Session: Sunday, 2 hours

Hour 1: Template Setup
[ ] 0:00-0:15 — Create Brand Kit (colors, fonts, logo)
[ ] 0:15-0:30 — Create Quote Card template
[ ] 0:30-0:40 — Create Carousel template
[ ] 0:40-0:50 — Create Story template
[ ] 0:50-1:00 — Upload brand assets

Hour 2: Batch Production
[ ] 1:00-1:10 — Duplicate Quote Card × 7
[ ] 1:10-1:30 — Fill in quotes + signs (copy from ChatGPT output)
[ ] 1:30-1:40 — Create 1 Carousel (Sign Spotlight)
[ ] 1:40-1:50 — Create 3 Stories
[ ] 1:50-2:00 — Export all as PNGs → Name correctly → Upload to Later
```