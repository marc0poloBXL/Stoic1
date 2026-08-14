# Carousel Template Guide — Stoic Wisdom × Zodiac Signs

**Format**: 1080×1080 (1:1 square, multi-page)  
**Pages**: 5–10 per carousel  
**Tool**: Canva (free tier) + Canva App (`04_TEMPLATES/canva-app/`)  
**Style**: Dark academia, minimalist, scrollable deep-dive

---

## 🎠 Carousel Types & Templates

### Template C1 — Sign Spotlight (7 pages)

Deep-dive into one zodiac sign's stoic wisdom.

| Page | Layout | Content |
|------|--------|---------|
| **1** (Title) | `#1A1A2E` bg, sign symbol (large, center), sign name below | "THE STOIC PATH / ♌ LEO" |
| **2** (Element) | `#0A0A0A` bg, element icon, key trait | Element + ruling planet |
| **3** (Strength) | Marble texture overlay, quote from matching philosopher | "The obstacle is the way" — Marcus Aurelius |
| **4** (Challenge) | Split layout: dark left / gold accent right | Common struggle + stoic solution |
| **5** (Insight) | Centered text, large quote mark decoration | Original stoic insight for this sign |
| **6** (Ritual) | Simple list layout | Daily stoic ritual for this sign |
| **7** (CTA) | `#1A1A2E` bg, sign symbol faded | "Save this for your sign ♌ / Follow @stoiczodiac" |

**Canva Creation Steps:**
1. New design → 1080×1080 px → **+ Add pages** (total 7)
2. Set backgrounds per page as above
3. Add marble texture (Elements → "marble" → opacity 10%) on pages 3-6
4. Add sign symbol: Search "[sign] zodiac symbol" → resize consistently
5. Text formatting:
   - Title page: Playfair Display, 48pt, Gold
   - Body: Cormorant Garamond, 24pt, White
   - Labels: Raleway, 18pt, Gold/Bronze
6. Page numbers (bottom-right): Raleway, 10pt, opacity 50%
7. **Save as template** → "Carousel — Sign Spotlight"

---

### Template C2 — Stoic Lesson (5 pages)

One stoic concept explained simply.

| Page | Layout | Content |
|------|--------|---------|
| **1** | Large concept word + subtitle | "AMOR FATI / Love of Fate" |
| **2** | Definition in simple terms | 2–3 sentence plain-language explanation |
| **3** | Real-life example | Relatable modern scenario |
| **4** | How to practice today | 3 actionable steps (numbered) |
| **5** | Quote + CTA | Matching philosopher quote + follow CTA |

**Canva Creation Steps:**
1. New design → 1080×1080 px → 5 pages
2. Page 1: Concept word (Playfair, 60pt, Gold) + language origin note (Raleway, 14pt, italic)
3. Page 2: Gold accent line at top, body text (Cormorant, 22pt, White)
4. Page 3: Split into "The Scenario" (top, italic) + "The Stoic Response" (bottom, bold)
5. Page 4: Numbered list with gold numerals (Raleway, 18pt)
6. Page 5: Block quote styling — large opening quote mark (`#D4AF37`, 72pt)
7. **Save as template** → "Carousel — Stoic Lesson"

---

### Template C3 — Zodiac Element Series (6 pages)

Compare the 3 signs within one element.

| Page | Layout | Content |
|------|--------|---------|
| **1** | Element symbol + name (Fire / Earth / Air / Water) | "THE FIRE SIGNS / Aries · Leo · Sagittarius" |
| **2–4** | One sign per page: symbol, dates, trait | Individual spotlight per sign |
| **5** | Comparison grid | 3-column: shared strengths, shared challenges |
| **6** | Closing insight + CTA | "Which fire sign are you? 🔥" |

**Canva Creation Steps:**
1. New design → 1080×1080 px → 6 pages
2. Element color theme (consistent per element):
   - Fire: warm accent (`#E63946` / `#F4A261` / `#E76F51`)
   - Earth: green/brown accent (`#2D6A4F` / `#95B46A` / `#5C4033`)
   - Air: cool accent (`#E9C46A` / `#B8BEDD` / `#7EC8E3`)
   - Water: blue accent (`#457B9D` / `#6D2E5C` / `#4A8FE4`)
3. Grid page: Use table or 3-column layout, Raleway 14pt for grid text
4. **Save as template** → "Carousel — Element Series"

---

### Template C4 — Quick Quote Carousel (4 pages)

Fast to produce — batch 10 in 30 minutes.

| Page | Layout |
|------|--------|
| **1** | Quote in large serif font, dark background |
| **2** | Philosopher name + era, subtle illustration |
| **3** | "What this means for [SIGN]" + 2-line insight |
| **4** | "Daily practice" + 1 action + CTA |

**Canva Creation Steps:**
1. New design → 1080×1080 px → 4 pages
2. Reuse same background across all 4 for visual consistency
3. Minimal decoration — one accent line or small symbol per page
4. **Save as template** → "Carousel — Quick Quote"

---

## ⚡ Batch Production Workflow

### Manual (in Canva — 90 min → 10 carousels)
```
[ ] 0:00–0:10 — Open carousel template
[ ] 0:10–0:30 — Duplicate pages as needed → Update all content
[ ] 0:30–0:45 — Adjust fonts, colors, spacing per sign
[ ] 0:45–0:60 — Add/swap visual elements (symbols, textures)
[ ] 0:60–0:75 — Review flow → check text fit on mobile
[ ] 0:75–0:90 — Export as PNG sequence → Name correctly
```

### Via Canva App (`canva-app`)
The developer app (`04_TEMPLATES/canva-app/`) provides programmatic image generation. For carousel backgrounds and sign imagery:

```bash
cd "project 1/stoiczodiac/04_TEMPLATES/canva-app"
# Configure .env with your CANVA_APP_ID
npm run build
```

The backend (`/api/queue-image-generation`) can generate themed images for each carousel page. See `canva-app/README.md` for the full API reference.

---

## 📐 Design Specifications

| Property | Value |
|----------|-------|
| Canvas size | 1080 × 1080 px |
| Page count | 5–10 per carousel |
| Safe zone (text) | 120px padding on all sides |
| Minimum text size | 16pt (readable on mobile) |
| Number style | "X/7" bottom-right, Raleway 10pt, opacity 50% |
| Font hierarchy | Playfair Display (titles/quotes), Raleway (labels/body), Cormorant Garamond (elevated text) |
| Color theme per carousel | One accent color per sign (see color palette below) |
| Export format | PNG sequence (individual pages) |
| Image quality | JPEG 90% or PNG (for text-heavy pages) |

---

## 🎨 Color Palette (per sign element)

| Element | Primary | Accent 1 | Accent 2 |
|---------|---------|----------|----------|
| 🔥 Fire | `#0A0A0A` | `#E63946` | `#F4A261` |
| 🌱 Earth | `#0A0A0A` | `#2D6A4F` | `#95B46A` |
| 💨 Air | `#1A1A2E` | `#E9C46A` | `#B8BEDD` |
| 💧 Water | `#1A1A2E` | `#457B9D` | `#7EC8E3` |

**Universal colors**: `#D4AF37` (Stoic Gold), `#F5F5F5` (Marble White), `#C9A96E` (Aged Bronze)

---

## 📁 File Naming Convention

```
carousel_[type]_[sign]_[YYYYMMDD]_page[NN].png
```

Examples:
- `carousel_spotlight_sagittarius_20260813_page01.png`
- `carousel_lesson_amorfati_20260814_page01.png`
- `carousel_element_fire_20260815_page01.png`
- `carousel_quickquote_leo_20260816_page01.png`

---

## ✅ Quality Checklist

Before posting, verify:
- [ ] All text fits within safe zone (no cropping)
- [ ] Font sizes are consistent across pages
- [ ] Sign colors match the correct element palette
- [ ] Page numbers are sequential and correct
- [ ] CTA is on the final page with @ handle
- [ ] No text overlaps with page edges
- [ ] Contrast ratio meets accessibility (light text on dark bg)
- [ ] Brand assets (logo, watermark) present
- [ ] Downloaded files named correctly for upload scheduling