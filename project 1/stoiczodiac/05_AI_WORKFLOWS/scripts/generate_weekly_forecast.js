/**
 * Generate the Weekly Stoic Forecast carousel (10 slides) for the week of Sep 7–13.
 * Pillar 4 content. Uses real calendar themes for the week.
 * Matches the visual system of generate_carousels.js.
 */
const fs = require("fs");
const path = require("path");

const GOLD = "#D4AF37";
const GOLD_SOFT = "#C9A96E";
const CREAM = "#F5F5F5";

const ELEMENT_COLORS = { FIRE: "#E63946", EARTH: "#2A9D8F", AIR: "#00B4D8", WATER: "#80CED7" };

// Real daily themes from week4_20260907.md
const DAYS = [
  ["MON 7", "♑ Capricorn", "The weight of responsibility", "Epictetus"],
  ["TUE 8", "♒ Aquarius", "The common good", "Marcus Aurelius"],
  ["WED 9", "♓ Pisces", "The courage to let go", "Seneca"],
  ["THU 10", "♈ Aries", "Choosing your battles", "Epictetus"],
  ["FRI 11", "♉ Taurus", "Nature's rhythm", "Zeno"],
  ["SAT 12", "♊ Gemini", "The power of stillness", "Marcus Aurelius"],
  ["SUN 13", "♋ Cancer", "Resilience of the heart", "Seneca"],
];

const ELEMENTS = [
  {
    name: "EARTH",
    color: ELEMENT_COLORS.EARTH,
    line: "Ground, duty, patience",
    signs: [
      ["♑ Capricorn", "Responsibility is a gift — carry it with virtue, not weight."],
      ["♉ Taurus", "Let nature set your pace. Steady outlasts stubborn."],
      ["♍ Virgo", "Small corrections beat big overhauls this week."],
    ],
  },
  {
    name: "AIR",
    color: ELEMENT_COLORS.AIR,
    line: "Mind, connection, perspective",
    signs: [
      ["♒ Aquarius", "Your best ideas serve the common good."],
      ["♊ Gemini", "Stillness quiets the noise — sit with one thought today."],
      ["♎ Libra", "Weigh what deserves a reply before you speak."],
    ],
  },
  {
    name: "FIRE",
    color: ELEMENT_COLORS.FIRE,
    line: "Energy, courage, right action",
    signs: [
      ["♈ Aries", "Choose your battles — not every spark needs fuel."],
      ["♌ Leo", "Lead with warmth; the light is brighter shared."],
      ["♐ Sagittarius", "Wisdom is a horizon. Keep moving, keep questioning."],
    ],
  },
  {
    name: "WATER",
    color: ELEMENT_COLORS.WATER,
    line: "Emotion, release, resilience",
    signs: [
      ["♓ Pisces", "Letting go is courage, not loss."],
      ["♋ Cancer", "Your heart can bend without breaking — protect, don't armor it."],
      ["♏ Scorpio", "Depth is your power — use it to rebuild, not to hold on."],
    ],
  },
];

function slide(page, total, content, accent = GOLD) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1080 1080" width="1080" height="1080">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#1A1A2E"/>
      <stop offset="100%" stop-color="#0A0A0A"/>
    </radialGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4AF37"/>
      <stop offset="50%" stop-color="#C9A96E"/>
      <stop offset="100%" stop-color="#D4AF37"/>
    </linearGradient>
  </defs>
  <rect width="1080" height="1080" fill="url(#bgGrad)"/>
  <rect x="20" y="20" width="1040" height="1040" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.5"/>
  <rect x="30" y="30" width="1020" height="1020" fill="none" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <line x1="100" y1="45" x2="980" y2="45" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>
  <line x1="100" y1="1034" x2="980" y2="1034" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>
  <path d="M 36 46 L 36 36 L 46 36" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 1044 46 L 1044 36 L 1034 36" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 36 1034 L 36 1044 L 46 1044" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 1044 1034 L 1044 1044 L 1034 1044" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <text x="540" y="115" font-family="Raleway,sans-serif" font-size="13" font-weight="600" letter-spacing="5" fill="#D4AF37" text-anchor="middle" opacity="0.7">STOIC WISDOM</text>
  ${content.header ? `<text x="540" y="250" font-family="'Playfair Display',Georgia,serif" font-size="44" fill="${CREAM}" text-anchor="middle">${content.header}</text>
  <line x1="340" y1="290" x2="740" y2="290" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.2"/>` : ""}
  ${content.body}
  <circle cx="540" cy="1055" r="14" fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.3"/>
  <text x="540" y="1060" font-family="Raleway,sans-serif" font-size="12" font-weight="600" fill="#D4AF37" text-anchor="middle" opacity="0.5">${page}/${total}</text>
</svg>`;
}

function lineBreak(text, n) {
  // simple greedy wrap for long strings
  const words = text.split(" ");
  const lines = [];
  let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > n) { lines.push(cur.trim()); cur = w; }
    else cur = (cur + " " + w).trim();
  }
  if (cur) lines.push(cur);
  return lines;
}

const slides = [];

// 1 — Cover
slides.push(slide(1, 10, {
  header: null,
  body: `
  <text x="540" y="330" font-family="'Playfair Display',Georgia,serif" font-size="30" letter-spacing="8" fill="${GOLD_SOFT}" text-anchor="middle">S E P   7 – 1 3</text>
  <text x="540" y="470" font-family="'Playfair Display',Georgia,serif" font-size="66" fill="${CREAM}" text-anchor="middle">Weekly Stoic</text>
  <text x="540" y="555" font-family="'Playfair Display',Georgia,serif" font-size="66" fill="${GOLD}" text-anchor="middle">Forecast</text>
  <line x1="380" y1="630" x2="700" y2="630" stroke="url(#goldGrad)" stroke-width="1" opacity="0.4"/>
  <text x="540" y="700" font-family="Raleway,sans-serif" font-size="19" letter-spacing="3" fill="#C9A96E" text-anchor="middle" opacity="0.8">A GENTLE GUIDE FOR THE WEEK AHEAD</text>
  <text x="540" y="800" font-family="'Playfair Display',Georgia,serif" font-size="22" font-style="italic" fill="#F5F5F5" text-anchor="middle" opacity="0.55">"The greatest blessings are found in the mind." — Seneca</text>`,
}));

// 2 — The Week Ahead (7 daily themes)
slides.push(slide(2, 10, {
  header: "The Week Ahead",
  body: DAYS.map(([d, sign, theme, phil], i) =>
    `<text x="180" y="${350 + i * 92}" font-family="Raleway,sans-serif" font-size="20" font-weight="700" fill="${GOLD}" text-anchor="middle">${d}</text>
  <text x="330" y="${350 + i * 92}" font-family="Raleway,sans-serif" font-size="20" fill="${CREAM}" text-anchor="middle" opacity="0.9">${sign}</text>
  <text x="540" y="${350 + i * 92}" font-family="Raleway,sans-serif" font-size="18" font-style="italic" fill="${GOLD_SOFT}" text-anchor="middle">${theme}</text>`
  ).join("\n  ") +
  `\n  <text x="540" y="980" font-family="Raleway,sans-serif" font-size="15" fill="#F5F5F5" text-anchor="middle" opacity="0.45">Seven days, one compass.</text>`,
}));

// 3–6 — Element slides
ELEMENTS.forEach((el, i) => {
  const page = i + 3;
  slides.push(slide(page, 10, {
    header: el.name,
    body: `
  <text x="540" y="330" font-family="Raleway,sans-serif" font-size="17" letter-spacing="4" fill="${el.color}" text-anchor="middle" opacity="0.8">${el.line.toUpperCase()}</text>
  ${el.signs.map(([name, advice], s) => {
    const y = 430 + s * 200;
    return `<text x="540" y="${y}" font-family="'Playfair Display',Georgia,serif" font-size="30" fill="${el.color}" text-anchor="middle">${name}</text>
${lineBreak(advice, 44).map((l, li) =>
      `<text x="540" y="${y + 48 + li * 40}" font-family="Raleway,sans-serif" font-size="20" fill="${CREAM}" text-anchor="middle" opacity="0.85">${l}</text>`).join("\n  ")}`;
  }).join("\n  ")}`,
  }));
});

// 7 — Key days
slides.push(slide(7, 10, {
  header: "Three Moments That Matter",
  body: `
  <text x="180" y="${385}" font-family="serif" font-size="24" fill="${GOLD}" text-anchor="middle">I</text>
  <text x="540" y="${385}" font-family="'Playfair Display',Georgia,serif" font-size="24" fill="${CREAM}" text-anchor="middle">Monday — own one duty fully</text>
  <text x="180" y="${485}" font-family="serif" font-size="24" fill="${GOLD}" text-anchor="middle">II</text>
  <text x="540" y="${485}" font-family="'Playfair Display',Georgia,serif" font-size="24" fill="${CREAM}" text-anchor="middle">Wednesday — release one attachment</text>
  <text x="180" y="${585}" font-family="serif" font-size="24" fill="${GOLD}" text-anchor="middle">III</text>
  <text x="540" y="${585}" font-family="'Playfair Display',Georgia,serif" font-size="24" fill="${CREAM}" text-anchor="middle">Saturday — sit in silence, ten minutes</text>
  <line x1="300" y1="660" x2="780" y2="660" stroke="#C9A96E" stroke-width="0.5" opacity="0.25"/>
  <text x="540" y="740" font-family="'Playfair Display',Georgia,serif" font-size="26" font-style="italic" fill="#C9A96E" text-anchor="middle">Small moments, well lived,</text>
  <text x="540" y="790" font-family="'Playfair Display',Georgia,serif" font-size="26" font-style="italic" fill="#C9A96E" text-anchor="middle">make the week.</text>`,
}));

// 8 — Stoic practice of the week
slides.push(slide(8, 10, {
  header: "Practice of the Week",
  body: `
  <text x="540" y="400" font-family="'Playfair Display',Georgia,serif" font-size="36" fill="${GOLD}" text-anchor="middle">The Morning Question</text>
  <text x="540" y="490" font-family="'Playfair Display',Georgia,serif" font-size="26" font-style="italic" fill="${CREAM}" text-anchor="middle">"What is within my</text>
  <text x="540" y="535" font-family="'Playfair Display',Georgia,serif" font-size="26" font-style="italic" fill="${CREAM}" text-anchor="middle">control today?"</text>
  <line x1="380" y1="600" x2="700" y2="600" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.3"/>
  <text x="540" y="670" font-family="Raleway,sans-serif" font-size="21" fill="#F5F5F5" text-anchor="middle" opacity="0.85">Before your phone. Before the news.</text>
  <text x="540" y="715" font-family="Raleway,sans-serif" font-size="21" fill="#F5F5F5" text-anchor="middle" opacity="0.85">Write one answer.</text>
  <text x="540" y="780" font-family="Raleway,sans-serif" font-size="18" fill="${GOLD_SOFT}" text-anchor="middle">At night, ask: "Did I act on it?"</text>`,
}));

// 9 — Challenge of the week
slides.push(slide(9, 10, {
  header: "The Challenge",
  body: `
  <text x="540" y="390" font-family="'Playfair Display',Georgia,serif" font-size="36" fill="${GOLD}" text-anchor="middle">The Impulse Pause</text>
  <text x="540" y="490" font-family="Raleway,sans-serif" font-size="22" fill="${CREAM}" text-anchor="middle" opacity="0.85">Before reacting this week —</text>
  <text x="540" y="540" font-family="Raleway,sans-serif" font-size="22" fill="${CREAM}" text-anchor="middle" opacity="0.85">a message, a comment, a word —</text>
  <text x="540" y="590" font-family="Raleway,sans-serif" font-size="22" fill="${CREAM}" text-anchor="middle" opacity="0.85">breathe once and ask:</text>
  <text x="540" y="680" font-family="'Playfair Display',Georgia,serif" font-size="30" font-style="italic" fill="#C9A96E" text-anchor="middle">"Is this impression, or fact?"</text>
  <text x="540" y="750" font-family="Raleway,sans-serif" font-size="17" fill="#F5F5F5" text-anchor="middle" opacity="0.5">The pause is the power.</text>`,
}));

// 10 — CTA
slides.push(slide(10, 10, {
  header: null,
  body: `
  <text x="540" y="380" font-family="'Playfair Display',Georgia,serif" font-size="38" fill="${CREAM}" text-anchor="middle">Save this forecast</text>
  <text x="540" y="450" font-family="'Playfair Display',Georgia,serif" font-size="38" fill="${GOLD}" text-anchor="middle">for the week ahead ♥</text>
  <line x1="380" y1="510" x2="700" y2="510" stroke="#C9A96E" stroke-width="0.5" opacity="0.25"/>
  <text x="540" y="600" font-family="Raleway,sans-serif" font-size="20" fill="${CREAM}" text-anchor="middle" opacity="0.8">Tag someone who needs</text>
  <text x="540" y="640" font-family="Raleway,sans-serif" font-size="20" fill="${CREAM}" text-anchor="middle" opacity="0.8">grounding this week</text>
  <text x="540" y="740" font-family="Raleway,sans-serif" font-size="21" letter-spacing="3" fill="${GOLD}" text-anchor="middle">FOLLOW @STOICZODIAC</text>
  <text x="540" y="800" font-family="Raleway,sans-serif" font-size="15" fill="#F5F5F5" text-anchor="middle" opacity="0.5">Daily wisdom for every sign</text>`,
}));

// --- MAIN ---
// --- CLI ---

const weekArg = process.argv.find((a) => a.startsWith("--week="));
const weekFolder = weekArg ? weekArg.split("=")[1] : "week_20260907";

const outDir = path.resolve(__dirname, `../../11_MEDIA_LIBRARY/SCHEDULED/${weekFolder}/carousels/weekly_forecast`);
fs.mkdirSync(outDir, { recursive: true });

console.log("=== Weekly Forecast (10 slides) ===");
slides.forEach((svg, i) => {
  const filepath = path.join(outDir, `slide_${i + 1}_of_10.svg`);
  fs.writeFileSync(filepath, svg, "utf8");
  console.log(`  ✓ slide_${i + 1}_of_10.svg`);
});
console.log("\n✅ Weekly forecast done!");