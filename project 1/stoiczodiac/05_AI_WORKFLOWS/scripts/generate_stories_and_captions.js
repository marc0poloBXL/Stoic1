/**
 * Generate 7 daily story SVGs + 7 captions for the current week.
 */
const fs = require("fs");
const path = require("path");

const signData = JSON.parse(
  fs.readFileSync(path.resolve(__dirname, "../sign_master_data.json"), "utf8")
);
const signMap = {};
signData.signs.forEach((s) => { signMap[s.id] = s; });

const week = [
  {
    day: "Monday", date: "Sep 7", sign_id: "capricorn", philosopher: "Epictetus",
    theme: "The weight of responsibility",
    story_prompt: "What responsibility are you avoiding today?",
    caption: `♑ CAPRICORN — Your duty is not your burden.

"We are not responsible for the impressions that come to us, but we are responsible for how we respond to them." — Epictetus

Capricorn, your ambition is a gift — but only when tethered to virtue. Take on one task today not for reward, but because it is right.

Save this for your daily reminder. Follow @stoiczodiac for more wisdom.`,
    hashtags: "#Capricorn #Stoicism #Epictetus #DailyWisdom #StoicZodiac #CapricornSeason #Mindset #AncientWisdom #SelfMastery #PersonalGrowth"
  },
  {
    day: "Tuesday", date: "Sep 8", sign_id: "aquarius", philosopher: "Marcus Aurelius",
    theme: "The common good",
    story_prompt: "What did you do today for someone else?",
    caption: `♒ AQUARIUS — The whole is greater than the part.

"What is good for the hive is good for the bee." — Marcus Aurelius

Aquarius, your vision for a better world begins with small acts of kindness today. The future is built in the present.

Do one thing today that benefits someone else without them knowing.

Save this. Follow @stoiczodiac for daily wisdom.`,
    hashtags: "#Aquarius #MarcusAurelius #Stoicism #CommonGood #StoicZodiac #AquariusSeason #Wisdom #Humanity #DailyStoic #Mindfulness"
  },
  {
    day: "Wednesday", date: "Sep 9", sign_id: "pisces", philosopher: "Seneca",
    theme: "The courage to let go",
    story_prompt: "What are you holding onto that you need to release?",
    caption: `♓ PISCES — Letting go is not giving up.

"Sometimes even to live is an act of courage. But to let go of what harms you — that is wisdom." — Seneca

Pisces, you feel deeply — but not everything you feel must be carried. Release one attachment today that no longer serves your peace.

Save this. Follow @stoiczodiac for daily wisdom.`,
    hashtags: "#Pisces #Seneca #Stoicism #LettingGo #StoicZodiac #PiscesSeason #Healing #Wisdom #InnerPeace #DailyStoic"
  },
  {
    day: "Thursday", date: "Sep 10", sign_id: "aries", philosopher: "Epictetus",
    theme: "Choosing your battles",
    story_prompt: "Is this worth your fire today?",
    caption: `♈ ARIES — Choose your battles wisely.

"No man is free who is not master of himself." — Epictetus

Aries, your fire is powerful — but power without direction burns everything. Before reacting today, pause and ask: is this worth my fire?

Save this. Follow @stoiczodiac for daily wisdom.`,
    hashtags: "#Aries #Epictetus #Stoicism #ChooseYourBattles #StoicZodiac #AriesSeason #SelfControl #Wisdom #Discipline #DailyStoic"
  },
  {
    day: "Friday", date: "Sep 11", sign_id: "taurus", philosopher: "Zeno",
    theme: "Nature's rhythm",
    story_prompt: "What natural rhythm can you match today?",
    caption: `♉ TAURUS — Flow with nature, not against it.

"The end of life is to live in accordance with nature." — Zeno

Taurus, your stubbornness is strength when aligned with nature's flow. Notice one natural rhythm today — sunrise, breath, silence — and match its pace.

Save this. Follow @stoiczodiac for daily wisdom.`,
    hashtags: "#Taurus #Zeno #Stoicism #Nature #StoicZodiac #TaurusSeason #Grounding #Wisdom #Patience #DailyStoic"
  },
  {
    day: "Saturday", date: "Sep 12", sign_id: "gemini", philosopher: "Marcus Aurelius",
    theme: "The power of stillness",
    story_prompt: "When was the last time you sat in complete silence?",
    caption: `♊ GEMINI — Stillness is the birthplace of clarity.

"Nowhere can you find a quieter retreat than in your own soul." — Marcus Aurelius

Gemini, your mind thrives on movement — but wisdom is born in stillness. Spend 5 minutes today in complete silence. No input. No output. Just being.

Save this. Follow @stoiczodiac for daily wisdom.`,
    hashtags: "#Gemini #MarcusAurelius #Stoicism #Stillness #StoicZodiac #GeminiSeason #Mindfulness #Wisdom #InnerPeace #DailyStoic"
  },
  {
    day: "Sunday", date: "Sep 13", sign_id: "cancer", philosopher: "Seneca",
    theme: "Resilience of the heart",
    story_prompt: "Name one thing you're feeling and choose how to respond.",
    caption: `♋ CANCER — Resilience is not hardness. It is flexibility.

"The tough tree bends in the wind but does not break." — Seneca

Cancer, your sensitivity is not weakness — it is your compass. Name one thing you're feeling today, then choose how to respond — not react.

Save this. Follow @stoiczodiac for daily wisdom.`,
    hashtags: "#Cancer #Seneca #Stoicism #Resilience #StoicZodiac #CancerSeason #EmotionalStrength #Wisdom #Heart #DailyStoic"
  },
];

function generateStorySVG(sign, prompt) {
  const color = sign.color;
  const symbol = sign.symbol;
  const signName = sign.name.toUpperCase();

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1920" width="1080" height="1920">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="40%" r="80%">
      <stop offset="0%" stop-color="#1A1A2E"/>
      <stop offset="100%" stop-color="#0A0A0A"/>
    </radialGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37"/>
      <stop offset="50%" stop-color="#C9A96E"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
    <linearGradient id="bottomFade" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0A0A0A" stop-opacity="0"/>
      <stop offset="100%" stop-color="#0A0A0A" stop-opacity="0.9"/>
    </linearGradient>
    <filter id="marble"><feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="5" seed="7" result="noise"/><feColorMatrix type="saturate" values="0" in="noise" result="gray"/><feComponentTransfer in="gray" result="faded"><feFuncA type="linear" slope="0.05"/></feComponentTransfer><feBlend in="faded" in2="SourceGraphic" mode="overlay"/></filter>
    <filter id="textShadow"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#000" flood-opacity="0.5"/></filter>
  </defs>
  <rect width="1080" height="1920" fill="url(#bgGrad)" filter="url(#marble)"/>
  <circle cx="540" cy="800" r="300" fill="#D4AF37" opacity="0.03"/>
  <rect x="25" y="25" width="1030" height="1870" fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.5"/>
  <rect x="35" y="35" width="1010" height="1850" fill="none" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <rect x="340" y="50" width="400" height="1.5" fill="url(#goldGrad)" opacity="0.4"/>
  <rect x="340" y="1860" width="400" height="1.5" fill="url(#goldGrad)" opacity="0.4"/>
  <path d="M 41 52 L 41 41 L 52 41" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 1039 52 L 1039 41 L 1028 41" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 41 1868 L 41 1879 L 52 1879" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 1039 1868 L 1039 1879 L 1028 1879" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <polygon points="540,1845 548,1853 540,1861 532,1853" fill="#D4AF37" opacity="0.25"/>
  <text x="540" y="110" font-family="Raleway,sans-serif" font-size="13" font-weight="500" letter-spacing="5" fill="#D4AF37" text-anchor="middle" opacity="0.7">TODAY'S STOIC PROMPT</text>
  <text x="540" y="180" font-family="serif" font-size="48" fill="${color}" text-anchor="middle" opacity="0.9">${symbol}</text>
  <text x="540" y="210" font-family="Raleway,sans-serif" font-size="16" font-weight="600" fill="${color}" text-anchor="middle" letter-spacing="3" opacity="0.6">${signName}</text>
  <line x1="340" y1="260" x2="740" y2="260" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.2"/>
  <text x="540" y="560" font-family="'Playfair Display',Georgia,serif" font-size="44" fill="#F5F5F5" text-anchor="middle" filter="url(#textShadow)">"${prompt}"</text>
  <rect x="0" y="1380" width="1080" height="540" fill="url(#bottomFade)"/>
  <text x="540" y="1520" font-family="serif" font-size="26" font-style="italic" fill="#C9A96E" text-anchor="middle">Sit with this question today.</text>
  <line x1="420" y1="1580" x2="660" y2="1580" stroke="#C9A96E" stroke-width="0.5" opacity="0.2"/>
  <rect x="390" y="1650" width="300" height="50" rx="25" fill="none" stroke="#D4AF37" stroke-width="1.5" opacity="0.6"/>
  <text x="540" y="1680" font-family="Raleway,sans-serif" font-size="16" font-weight="600" letter-spacing="3" fill="#D4AF37" text-anchor="middle">@STOICZODIAC</text>
  <text x="540" y="1800" font-family="Raleway,sans-serif" font-size="11" fill="#F5F5F5" text-anchor="middle" opacity="0.3">Reply with your answer</text>
  <line x1="25" y1="800" x2="45" y2="800" stroke="#D4AF37" stroke-width="1" opacity="0.3"/>
  <line x1="25" y1="1120" x2="45" y2="1120" stroke="#D4AF37" stroke-width="1" opacity="0.3"/>
  <line x1="1035" y1="800" x2="1055" y2="800" stroke="#D4AF37" stroke-width="1" opacity="0.3"/>
  <line x1="1035" y1="1120" x2="1055" y2="1120" stroke="#D4AF37" stroke-width="1" opacity="0.3"/>
</svg>`;
}

// --- MAIN ---

// --- CLI ---

const weekArg = process.argv.find((a) => a.startsWith("--week="));
const weekFolder = weekArg ? weekArg.split("=")[1] : "week_20260907";

// Generate stories
const storiesDir = path.resolve(__dirname, `../../11_MEDIA_LIBRARY/SCHEDULED/${weekFolder}/stories`);
fs.mkdirSync(storiesDir, { recursive: true });

// Generate captions
const captionsDir = path.resolve(__dirname, `../../11_MEDIA_LIBRARY/SCHEDULED/${weekFolder}/captions`);
fs.mkdirSync(captionsDir, { recursive: true });

console.log("=== Stories ===");
week.forEach((day) => {
  const sign = signMap[day.sign_id];
  const slug = `${day.date.replace(/\s/g, "_")}_${day.sign_id}`.toLowerCase();
  const svg = generateStorySVG(sign, day.story_prompt);
  fs.writeFileSync(path.join(storiesDir, `story_${slug}.svg`), svg, "utf8");
  console.log(`  ✓ story_${slug}.svg`);
});

console.log("\n=== Captions ===");
week.forEach((day) => {
  const slug = `${day.date.replace(/\s/g, "_")}_${day.sign_id}`.toLowerCase();
  const caption = `${day.caption}\n\n${day.hashtags}`;
  fs.writeFileSync(path.join(captionsDir, `caption_${slug}.txt`), caption, "utf8");
  console.log(`  ✓ caption_${slug}.txt`);
});

console.log("\n✅ All done!");