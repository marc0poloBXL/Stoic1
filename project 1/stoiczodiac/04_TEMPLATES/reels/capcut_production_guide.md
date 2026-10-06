# CapCut Production Guide — Stoic Wisdom × Zodiac Signs

**Format**: 1080×1920 (9:16 vertical), MP4, H.264, 30fps
**Duration**: 15–30 seconds per reel
**Tool**: CapCut Desktop (free tier)

---

## Getting Started

### Step 1: Import Assets

1. Open CapCut → **New Project** → Settings: 1080×1920, 30fps
2. **Import Media**:
   - Background video clips (Pexels: dark marble, stars, flames, ocean — slow motion)
   - Voiceover MP3 files (from VibeVoice — self-hosted, replaces ElevenLabs — or TTSMaker)
   - Music track (royalty-free ambient/lo-fi)
3. **Import Text Assets**: (optional, Canva-designed title cards)

### Step 2: Create From Template

CapCut doesn't support project file import, but the three templates below give you the exact timeline structure to build manually. Once built once, **right-click the timeline → "Save as Template"** for reuse.

---

## Template TP1 — Quote Reel (15s, Monday/Wednesday/Friday)

### Timeline Structure

```
 Track    0s        3s        10s       12s       15s
 ───────────────────────────────────────────────────────
 Video 1  [━━━━━━━━ Dark background / marble / slow motion ━━━━━━━━━━━━━━━━━]
 Text 1                        [━━ Typewriter: Quote ━━━━━━]
 Text 2                                     [━ Attribution ━] 
 Text 3                                              [━ CTA ━]
 Audio 1  [━━━━━━━━ Voiceover: read quote + attribution ━━━━━━━━━━]
 Music 1  [━━━━━━━━━━━━━━ Ambient drone / lo-fi ━━━━━━━━━━━━━━━━━━━━━━]
```

### Video Track
- **Clip**: Static or slow-pan dark marble texture — 15s duration
- **Adjustment**: Contrast +15%, Brightness -5%, Slight vignette
- **Effect**: "Film" → "Fade in" (0.5s at start)

### Text Tracks

| Track | Time | Content | Font | Size | Color | Animation |
|-------|------|---------|------|------|-------|-----------|
| Text 1 | 3:00–12:00 | Quote text | Playfair Display | 48pt | `#D4AF37` | Typewriter (0.8s/char) |
| Text 2 | 10:00–12:00 | "— Philosopher" | Raleway | 20pt | `#F5F5F5` | Fade in (0.5s) |
| Text 3 | 12:00–15:00 | "@stoiczodiac" | Raleway | 14pt | `#D4AF37` | Scale up (0.3s) |

### Audio Tracks
- **Voiceover**: Start at 3:00, fade in 0.3s, level -3dB
- **Music**: Full 15s, volume -20dB, fade out last 1s

### Text Design (CapCut)

1. Add text → type quote → **Style** tab:
   - Font: Playfair Display
   - Color: `#D4AF37` (hex input)
   - Alignment: Center
   - Shadow: Opacity 40%, Distance 2, Angle 45°
2. **Animation** → "Typewriter" → speed: 0.8s per character
3. Duplicate text track for attribution:
   - Font: Raleway, Size: 20pt, Color: White
   - Animation: "Fade in"
4. CTA text:
   - Font: Raleway, Size: 14pt, Color: Gold
   - Animation: "Scale up"

### Audio Sync
1. Import voiceover MP3 (from VibeVoice — replaces ElevenLabs)
2. Place at 3:00 on timeline
3. Generate captions: **Text → Auto Captions** → Language: English
4. Style captions: Raleway 14pt, Gold, transparent background
5. Fine-tune caption timing to match spoken words

---

## Template TP2 — Sign Spotlight Reel (30s, Tuesday/Thursday)

### Timeline Structure

```
 Track    0s        5s        12s       25s       30s
 ───────────────────────────────────────────────────────
 Video 1  [━Intro━][━━━━ B-roll / sign imagery ━━━━━━][━CTA━]
 Text 1   [━Symbol━]
 Text 2              [━Traits (staggered)━]
 Text 3                        [━Insight + Quote━]
 Text 4                                        [━CTA━]
 Audio 1  [━Cinematic hit━][━━━━ Voiceover ━━━━━━━━━━━━]
 Music 1  [━━━━━━━━━━━━━━━━ Pulse / ambient ━━━━━━━━━━━━━━━━━]
```

### Scene Breakdown

**Scene 1 (0:00–0:05) — Sign Intro**
- Video: Cinematic B-roll (related to the sign's element)
- Overlay: Canva-exported sign symbol (large, center)
- Effect: Gold glow behind symbol — **Overlay → Glow**, 50% intensity
- Text: Sign name below symbol, Raleway 24pt, Gold
- Audio: Cinematic hit sound effect at 0:00

**Scene 2 (0:05–0:12) — Key Traits**
- Video: Same B-roll continues
- Text: 3 trait words, staggered 0.5s apart
  - Word 1: Appears at 5:00, "Rise" animation
  - Word 2: Appears at 5:05, "Rise" animation
  - Word 3: Appears at 5:10, "Rise" animation
- Color: Use sign's accent hex color (see sign color palette below)
- Audio: Soft pulse beat continues

**Scene 3 (0:12–0:25) — Stoic Insight + Quote**
- Video: Transition to new B-roll (crossfade, 0.5s)
- Text 1: Insight sentence — Cormorant Garamond 28pt, Gold
- Text 2: Philosopher quote — Playfair Display 22pt, White
- Audio: Voiceover reads insight + quote

**Scene 4 (0:25–0:30) — CTA**
- Video: Crossfade to Midnight Blue (`#1A1A2E`) solid color
- Text: "@stoiczodiac" in gold pill badge
- Effect: Sign symbol faded in background, opacity 15%
- Audio: Music fade out 1s

### Transitions in CapCut

| Between | Transition | Duration |
|---------|-----------|----------|
| Scene 1 → 2 | No transition (instant cut) | 0s |
| Scene 2 → 3 | Crossfade (video) + Slide (text) | 0.5s |
| Scene 3 → 4 | Crossfade | 0.5s |

---

## Template TP3 — Daily Prompt Reel (15s, Monday/Wednesday/Friday)

### Timeline Structure

```
 Track    0s        2s        8s        12s       15s
 ───────────────────────────────────────────────────────
 Video 1  [━━━━━━━━━━ Starry / meditative background ━━━━━━━━━━━━━━━]
 Text 1   [━Title━]
 Text 2              [━━━━ Prompt text ━━━━━━]
 Text 3                                   [━Reflection cue━]
 Text 4                                             [━CTA━]
 Audio 1  [━chime━][━━━━ Voiceover ━━━━━━]
 Music 1  [━━━━━━━━━━━━━━ Soft pad background ━━━━━━━━━━━]
```

### Scene Breakdown

**Scene 1 (0:00–0:02) — Title**
- Video: Gentle motion background (starry sky, slow clouds, or marble)
- Text: "Today's Stoic Prompt" — Raleway 18pt, Gold, fade in
- Audio: Gentle chime SFX
- Effect: Slight vignette on video

**Scene 2 (0:02–0:08) — Prompt**
- Text: Large prompt question — Playfair Display 36pt, White, centered
- Animation: Fade up (2s duration)
- Effect: Drop shadow on text (Opacity 50%, Distance 3, Angle 45°)

**Scene 3 (0:08–0:12) — Reflection**
- Text: "Reflect on this today." — Raleway 16pt italic, Bronze `#C9A96E`
- Animation: Fade in (0.5s)
- Previous prompt text scales down slightly (scale 85%)

**Scene 4 (0:12–0:15) — CTA**
- Text: "@stoiczodiac" — Raleway 12pt, Gold
- Effect: All text fades out with 0.5s fade
- Audio: Music fades out over 1s

---

## 🎨 Sign Color Palette (for Reel Text)

| Sign | Hex | Element | Visual B-Roll to Search (Pexels) |
|------|-----|---------|----------------------------------|
| ♈ Aries | `#E63946` | Fire | "volcano", "sunset fire", "desert heat" |
| ♉ Taurus | `#2D6A4F` | Earth | "forest", "moss", "green meadow" |
| ♊ Gemini | `#E9C46A` | Air | "clouds timelapse", "wind", "sky" |
| ♋ Cancer | `#457B9D` | Water | "ocean waves", "moon reflection", "tide" |
| ♌ Leo | `#F4A261` | Fire | "sunrise", "golden hour", "savanna" |
| ♍ Virgo | `#95B46A` | Earth | "wheat field", "harvest", "garden" |
| ♎ Libra | `#B8BEDD` | Air | "cloud formation", "wind leaves", "fog" |
| ♏ Scorpio | `#6D2E5C` | Water | "deep ocean", "thunderstorm", "abyss" |
| ♐ Sagittarius | `#E76F51` | Fire | "arrows", "mountain peak", "horizon" |
| ♑ Capricorn | `#5C4033` | Earth | "mountain stone", "cliff", "ancient ruins" |
| ♒ Aquarius | `#7EC8E3` | Air | "sky timelapse", "rain", "water stream" |
| ♓ Pisces | `#4A8FE4` | Water | "ocean deep", "fish", "biome" |

---

## ⚡ Batch Production Workflow

### First-time Setup (Build Templates, 60 min)

Once built, save each as a **CapCut Template**:

```
[ ] 15 min — Build TP1: Quote Reel (15s)
    → File → Save as Template → "Stoic_Quote_Reel"
[ ] 30 min — Build TP2: Sign Spotlight (30s)
    → File → Save as Template → "Stoic_Spotlight"
[ ] 15 min — Build TP3: Daily Prompt (15s)
    → File → Save as Template → "Stoic_Prompt_Reel"
```

### Weekly Batch (30 min → 3-5 reels)

```
[ ] 0:00–0:02 — Open CapCut template "Stoic_Quote_Reel"
[ ] 0:02–0:08 — Replace B-roll clip with correct sign's visual
[ ] 0:08–0:12 — Update text: sign, quote, philosopher name
[ ] 0:12–0:15 — Update sign accent color in text elements
[ ] 0:15–0:20 — Import new voiceover from VibeVoice (replaces ElevenLabs) → sync
[ ] 0:20–0:25 — Adjust auto-captions timing
[ ] 0:25–0:28 — Add/review hashtag overlay (last frame)
[ ] 0:28–0:30 — Export: MP4, H.264, 30fps, 1080×1920
    → Repeat for remaining reels
```

### Export Settings

| Setting | Value |
|---------|-------|
| Resolution | 1080×1920 |
| Frame Rate | 30fps |
| Bitrate | 10 Mbps (recommended for IG) |
| Codec | H.264 |
| Format | MP4 |
| Audio | AAC, 320kbps, 48kHz |

### 📁 File Naming

```
reel_[type]_[sign]_[YYYYMMDD].mp4
```

- `reel_quote_aries_20260817.mp4`
- `reel_spotlight_leo_20260818.mp4`
- `reel_prompt_gemini_20260819.mp4`

---

## 🎧 Audio Sources

### Voiceover (VibeVoice — self-hosted, replaces ElevenLabs)
> ⚠️ **Tool change**: ElevenLabs has been replaced by **VibeVoice** — self-hosted, unlimited.
> Generate voices via `05_AI_WORKFLOWS/VibeVoice` (see its README), then download MP3.

1. Copy script from `07_AUDIO/voiceover_scripts/reel_voiceover_bank.md`
2. Generate voiceover in VibeVoice (via `05_AI_WORKFLOWS/VibeVoice/batch_generate_voiceovers.py`)
3. Tune voice settings within VibeVoice
4. Download MP3 → Import to CapCut

### Background Music (Royalty-Free)
| Mood | Search Term | Source |
|------|------------|--------|
| Cinematic | "cinematic ambient" | Pixabay Music |
| Meditative | "meditation drone" | Pixabay Music |
| Lo-fi | "lo-fi study" | Pixabay Music |
| Epic | "epic orchestral" | Pixabay Music |
| Calm | "ambient piano" | Pixabay Music |

### Sound Effects
| Moment | Effect | Source |
|--------|--------|--------|
| Scene start | Soft chime | CapCut built-in |
| Spotlight intro | Cinematic hit | CapCut → Audio → Effects |
| Transition | Whoosh | CapCut → Audio → Effects |
| CTA appear | Soft pop | CapCut → Audio → Effects |

---

## ✅ Quality Checklist

Before exporting each reel:

- [ ] Text fits within safe zone (90% center — no cropping on mobile)
- [ ] Voiceover is synced with text appearance (±0.2s)
- [ ] Sign color is correct for the featured zodiac sign
- [ ] Fonts consistent: Playfair (quotes), Raleway (labels), Cormorant (insights)
- [ ] Background B-roll matches the sign's element
- [ ] Audio levels: Voice -3dB, Music -20dB, SFX -10dB
- [ ] CTA visible at end frame (hold ≥2s)
- [ ] Export filename follows convention
- [ ] Preview on phone before posting