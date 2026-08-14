# Reel Template Guide — Stoic Wisdom × Zodiac Signs

**Format**: 1080×1920 (9:16 vertical video)  
**Duration**: 15–30 seconds  
**Tool**: Canva (free tier) + Canva App (`04_TEMPLATES/canva-app/`)  
**Style**: Cinematic, minimalist, stoic aesthetic

---

## 🎬 Reel Types & Templates

### Template R1 — Quote Reel (15s)

| Time | Visual | Audio |
|------|--------|-------|
| 0:00–0:03 | Fade in: dark bg + marble texture, zodiac sign top-right | Soft ambient / lo-fi |
| 0:03–0:10 | Text appears (typewriter effect): Quote in Playfair Display, 48pt, Gold `#D4AF37` | — |
| 0:10–0:12 | Philosopher name fades in (bottom-left), Raleway, 20pt, White `#F5F5F5` | — |
| 0:12–0:15 | CTA: "Follow @stoiczodiac" (bottom), subtle scale animation | Fade out |

**Canva Creation Steps:**
1. New design → 1080×1920 px
2. Background: `#0A0A0A` (Deep Void)
3. Element: "marble texture" → overlay → opacity 10%
4. Text: Quote → Playfair Display, 48pt, `#D4AF37`, centered
5. Text: Philosopher → Raleway, 20pt, `#F5F5F5`, bottom-left
6. Text: Zodiac sign → Cormorant Garamond, 24pt, sign color, top-right
7. CTA: "@stoiczodiac" bottom-center, 14pt, opacity 70%
8. **Animate**: Text → "Typewriter" (0:03–0:10), CTA → "Fade in" (0:12)
9. Duration: 15s
10. **Save as template** → "Reel — Quote Template"

---

### Template R2 — Sign Spotlight Reel (30s)

| Time | Visual | Audio |
|------|--------|-------|
| 0:00–0:05 | Sign symbol (large, center) + sign name, gold glow effect | Cinematic hit |
| 0:05–0:12 | Key trait text appears: "Courageous. Impulsive. Loyal." (staggered) | Soft pulse |
| 0:12–0:20 | Stoic insight for this sign | — |
| 0:20–0:25 | Matching philosopher quote | — |
| 0:25–0:30 | CTA: "Save for your sign 💫 Follow @stoiczodiac" | Fade out |

**Canva Creation Steps:**
1. New design → 1080×1920 px
2. Background: `#1A1A2E` (Midnight Blue) for intro/outro, `#0A0A0A` for middle
3. Sign symbol: Search "[sign name] symbol" in Elements → resize to 40% canvas
4. Add gold glow: Duplicate element → blur 15px → opacity 30% → place behind
5. Trait text: Raleway, 24pt, `#C9A96E`, staggered animation 0.5s apart
6. Insight text: Cormorant Garamond, 28pt, `#D4AF37`
7. Quote: Playfair Display, 22pt, `#F5F5F5`
8. **Animate**: Text → "Rise" (each line), transitions → "Slide" between sections
9. Duration: 30s
10. **Save as template** → "Reel — Sign Spotlight Template"

---

### Template R3 — Daily Stoic Prompt Reel (15s)

| Time | Visual | Audio |
|------|--------|-------|
| 0:00–0:02 | "Today's Stoic Prompt" (top), Raleway, 18pt, Gold | Gentle chime |
| 0:02–0:08 | The prompt text (large, center), Playfair Display, 36pt, White | — |
| 0:08–0:12 | "Reflect on this today." (bottom), 16pt, italic | — |
| 0:12–0:15 | "@stoiczodiac" + follow CTA | Fade out |

**Canva Creation Steps:**
1. New design → 1080×1920 px
2. Background: `#0A0A0A` with subtle astral overlay (Elements → "starry sky" → opacity 15%)
3. Prompt text: Playfair Display, 36pt, White, centered, with drop shadow
4. Subtitle: Raleway, 16pt, italic, `#C9A96E`
5. **Animate**: Prompt → "Fade up" (slow, 2s)
6. Duration: 15s
7. **Save as template** → "Reel — Daily Prompt Template"

---

## 🎨 Sign Color Palette

| Sign | Element | Hex | Accent Use |
|------|---------|-----|------------|
| ♈ Aries | Fire | `#E63946` | Title text, border |
| ♉ Taurus | Earth | `#2D6A4F` | Title text, border |
| ♊ Gemini | Air | `#E9C46A` | Title text, border |
| ♋ Cancer | Water | `#457B9D` | Title text, border |
| ♌ Leo | Fire | `#F4A261` | Title text, border |
| ♍ Virgo | Earth | `#95B46A` | Title text, border |
| ♎ Libra | Air | `#B8BEDD` | Title text, border |
| ♏ Scorpio | Water | `#6D2E5C` | Title text, border |
| ♐ Sagittarius | Fire | `#E76F51` | Title text, border |
| ♑ Capricorn | Earth | `#5C4033` | Title text, border |
| ♒ Aquarius | Air | `#7EC8E3` | Title text, border |
| ♓ Pisces | Water | `#4A8FE4` | Title text, border |

---

## ⚡ Batch Production Workflow

### Manual (in Canva)
```
Session time: 60 min → 7 reels

[ ] 0:00–0:10 — Open template → Duplicate × 7
[ ] 0:10–0:25 — Update sign + sign color for each
[ ] 0:25–0:40 — Add quotes/insights from content calendar
[ ] 0:40–0:50 — Adjust timing → Preview each
[ ] 0:50–0:60 — Export as MP4 → Name: reel_[sign]_[date]
```

### Via Canva App (`canva-app`)
The Canva developer app (`04_TEMPLATES/canva-app/`) can automate image generation for reel backgrounds. To use:

```bash
# From the canva-app directory
cd "project 1/stoiczodiac/04_TEMPLATES/canva-app"

# Set your CANVA_APP_ID in .env
# Then start the dev server
npm start
```

The app provides:
- AI image generation for reel backgrounds
- Credit-based usage tracking
- Express backend for custom integrations

See [`canva-app/README.md`](../canva-app/README.md) for full setup instructions.

---

## 📐 Design Specifications

| Property | Value |
|----------|-------|
| Canvas size | 1080 × 1920 px |
| Safe zone (text) | 90% center (avoid top/bottom 10%) |
| Minimum text size | 16pt (readable on mobile) |
| Animation style | Slow fade / typewriter / rise |
| Font hierarchy | Playfair Display (quotes), Raleway (labels), Cormorant Garamond (signs) |
| Color scheme | See brand_guidelines.md (`01_BRAND_ASSETS/`) |
| Export format | MP4, H.264, 30fps |
| Max duration | 15–30 seconds |

---

## 📁 File Naming Convention

```
reel_[type]_[sign]_[YYYYMMDD].mp4
```

Examples:
- `reel_quote_sagittarius_20260813.mp4`
- `reel_spotlight_leo_20260814.mp4`
- `reel_prompt_aries_20260815.mp4`