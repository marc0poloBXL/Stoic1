# Reel Voiceover Scripts — Bank of 15 Scripts

**Tool used**: VibeVoice (Microsoft open-source, runs locally — free, unlimited)  
**Voice style**: Calm, deep, authoritative — like a wise mentor  
**Duration**: 15–25 seconds per script  
**Production**: Generate audio → Import to CapCut → Sync with visuals

All 15 voiceover files are **already generated** in `07_AUDIO/voiceover_audio/`. Pre-mixed versions (with ambient music) are in `voiceover_audio/mixed/`.

---

## ⚡ Regenerating with VibeVoice (if needed)

VibeVoice lives in `05_AI_WORKFLOWS/VibeVoice/`. It runs locally — no API costs, no limits.

### One-time setup
```bash
cd 05_AI_WORKFLOWS/VibeVoice
pip install -e .
# Download model weights (see README.md for model source)
```

### Generate a single voiceover
```bash
python generate_voiceover.py \
  --text "Your script text here." \
  --output "outputs/my_voiceover.wav"
```

### Batch-generate all 15 scripts
```bash
python batch_generate_voiceovers.py
```
Output lands in `voiceover_audio/` with the correct file names.

### Mix with background music
```bash
python mix_voiceover.py
```
Combines each voiceover with the ambient piano tracks from `07_AUDIO/music/royalty_free/` and saves to `voiceover_audio/mixed/`.

### ⚠️ Tool change: VibeVoice replaces ElevenLabs
> ElevenLabs has been replaced by **VibeVoice** — self-hosted, unlimited, at no monthly char limit.
> The voiceover scripts below feed into `05_AI_WORKFLOWS/VibeVoice` (see `batch_generate_voiceovers.py`).
> Generate with VibeVoice → Download MP3 → Import into CapCut → Add visuals → Export.

---

## Scripts

### Script 1: Aries — Channel the Fire
```
[0:00] Aries.

[0:02] Marcus Aurelius was a warrior who knew that true strength is controlled, not wild.

[0:10] Your fire is your gift. But fire without direction burns everything.

[0:18] Today, channel your energy into one purposeful act.

[0:25] Follow Stoic Zodiac for your daily wisdom.
```
*11 words, ~20 seconds*

---

### Script 2: Taurus — The Art of Letting Go
```
[0:00] Taurus.

[0:02] Seneca wrote: "It is not the man who has too little, but the man who craves more, who is poor."

[0:12] Your strength is your stability. Your growth is in release.

[0:18] What are you holding onto that's holding you back?

[0:25] Follow Stoic Zodiac for your daily wisdom.
```
*12 words, ~20 seconds*

---

### Script 3: Gemini — Master Your Mind
```
[0:00] Gemini.

[0:02] Epictetus said: "We are not disturbed by what happens to us, but by our thoughts about what happens."

[0:14] Your mind is restless. That's your gift, and your challenge.

[0:20] Today, watch your thoughts. Don't believe every one.

[0:27] Follow Stoic Zodiac for your daily wisdom.
```
*12 words, ~22 seconds*

---

### Script 4: Cancer — Strength Through Vulnerability
```
[0:00] Cancer.

[0:02] Marcus Aurelius knew that strength isn't walls. It's the courage to feel.

[0:10] Your empathy is not weakness. It's your superpower.

[0:17] But even the ocean needs stillness. Protect your energy.

[0:25] Follow Stoic Zodiac for your daily wisdom.
```
*10 words, ~18 seconds*

---

### Script 5: Leo — Lead with Service
```
[0:00] Leo.

[0:02] Seneca advised: "Wherever there is a human being, there is an opportunity for kindness."

[0:10] Your light draws people. But true leaders serve, not shine.

[0:18] Today, give someone else the spotlight.

[0:25] Follow Stoic Zodiac for your daily wisdom.
```
*10 words, ~18 seconds*

---

### Script 6: Virgo — Progress Over Perfection
```
[0:00] Virgo.

[0:02] Epictetus taught: "First say to yourself what you would be; then do what you have to do."

[0:12] Perfection is not the goal. Progress is.

[0:18] Today, finish one thing at eighty percent and call it done.

[0:27] Follow Stoic Zodiac for your daily wisdom.
```
*11 words, ~20 seconds*

---

### Script 7: Libra — Harmony Through Action
```
[0:00] Libra.

[0:02] Marcus Aurelius wrote: "The happiness of your life depends upon the quality of your thoughts."

[0:12] Balance is not found. It's built — one right action at a time.

[0:20] Today, choose peace. Not by avoiding conflict, but by meeting it with wisdom.

[0:30] Follow Stoic Zodiac for your daily wisdom.
```
*13 words, ~22 seconds*

---

### Script 8: Scorpio — The Obstacle Is the Way
```
[0:00] Scorpio.

[0:02] Seneca said: "Sometimes even to live is an act of courage."

[0:10] Your depth is your power. Transformation comes from facing what others run from.

[0:20] Today, look at one thing you've been avoiding. It's your teacher.

[0:28] Follow Stoic Zodiac for your daily wisdom.
```
*12 words, ~22 seconds*

---

### Script 9: Sagittarius — Freedom Through Discipline
```
[0:00] Sagittarius.

[0:02] Epictetus said: "Who is the rich man? He who is content."

[0:10] You chase freedom. But true freedom comes from discipline, not escape.

[0:18] Today, commit to one thing. See it through.

[0:25] Follow Stoic Zodiac for your daily wisdom.
```
*10 words, ~18 seconds*

---

### Script 10: Capricorn — Build with Virtue
```
[0:00] Capricorn.

[0:02] Marcus Aurelius wrote: "Wake up and tell yourself: the people I deal with today will be difficult."

[0:14] Your ambition builds mountains. But what are you building them on?

[0:22] Today, do one thing that no one will see. For character, not credit.

[0:30] Follow Stoic Zodiac for your daily wisdom.
```
*13 words, ~22 seconds*

---

### Script 11: Aquarius — Vision into Action
```
[0:00] Aquarius.

[0:02] Seneca said: "We suffer more often in imagination than in reality."

[0:12] You see the future. But visions without action stay dreams.

[0:20] Today, take one small step toward one big idea.

[0:28] Follow Stoic Zodiac for your daily wisdom.
```
*10 words, ~18 seconds*

---

### Script 12: Pisces — Compassion with Boundaries
```
[0:00] Pisces.

[0:02] Epictetus taught: "Make the best use of what is in your power. Take the rest as it happens."

[0:14] You feel everything. That's beautiful. But not everything is yours to carry.

[0:24] Today, ask yourself: is this my burden, or am I just borrowing it?

[0:32] Follow Stoic Zodiac for your daily wisdom.
```
*14 words, ~24 seconds*

---

### Script 13: The Daily Pause (Universal)
```
[0:00] Between stimulus and response, there is a space.

[0:06] In that space is your power. Your freedom.

[0:12] The stoics knew this. Your zodiac sign doesn't change it.

[0:20] Today, pause before you react. Breathe. Choose.

[0:27] Follow Stoic Zodiac for daily wisdom.
```
*9 words, ~20 seconds*

---

### Script 14: Control vs. Concern (Universal)
```
[0:00] Some things are up to you. Some are not.

[0:06] Your thoughts. Your choices. Your actions.

[0:12] Everything else — the weather, other people, the past — is not yours to control.

[0:22] Today, focus only on what's yours. Let the rest go.

[0:30] Follow Stoic Zodiac for daily wisdom.
```
*10 words, ~22 seconds*

---

### Script 15: Memento Mori (Universal)
```
[0:00] You will die. So will everyone you love.

[0:06] This is not morbid. It's the most liberating truth there is.

[0:14] The stoics called it Memento Mori. Remember you must die.

[0:22] Today, let the shortness of life sharpen your focus.

[0:30] Follow Stoic Zodiac for daily wisdom.
```
*10 words, ~22 seconds*

---

## 🎬 Production Notes

### Files Already Generated
| Location | Contents |
|----------|----------|
| `07_AUDIO/voiceover_audio/` | 15 raw WAV files (signs 01–12 + 3 universal) |
| `07_AUDIO/voiceover_audio/mixed/` | 15 mixed WAV files (voiceover + ambient music) |
| `07_AUDIO/music/royalty_free/` | 2 ambient piano tracks for background |

### Voiceover Settings (VibeVoice)
| Setting | Value |
|---------|-------|
| Model | VibeVoice AR + diffusion |
| Sample rate | 24kHz, mono |
| Duration per script | 15–25 seconds |

### Audio Processing (CapCut)
- Add a **low-pass filter** (reverb simulation) for the "ancient" feel
- Background: **ambient piano** from `07_AUDIO/music/royalty_free/` at -20dB
- Voice: centered, -3dB to -6dB below 0dBFS
- Fade in: 0.5s, Fade out: 1s

### Visual Matching (Per Script)
| Script Type | Visual Style | Stock Sources |
|-------------|-------------|---------------|
| Fire signs (Aries, Leo, Sag) | Sunrises, flames, deserts, warriors | Pexels: "sunset" "fire" |
| Earth signs (Tau, Vir, Cap) | Mountains, forests, soil, marble | Pexels: "nature" "stone" |
| Air signs (Gem, Lib, Aqu) | Clouds, wind, open skies, birds | Pexels: "sky" "clouds" |
| Water signs (Can, Sco, Pis) | Oceans, rain, rivers, mist | Pexels: "ocean" "water" |
| Universal | Marble statues, candles, stars | Pexels: "statue" "stars" |