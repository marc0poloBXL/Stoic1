/**
 * Generate Sign Spotlight carousels (7 slides each) for the current week.
 * Uses carousel_page_frame structure from the brand system.
 */
const fs = require("fs");
const path = require("path");

const signData = JSON.parse(
  fs.readFileSync(path.resolve(__dirname, "../sign_master_data.json"), "utf8")
);
const signMap = {};
signData.signs.forEach((s) => { signMap[s.id] = s; });

// Two sign spotlights this week: Aquarius (Tue), Taurus (Fri)
const spotlights = [
  {
    sign_id: "aquarius",
    philosopher: "Seneca",
    title: "The Visionary",
    subtitle: "Individuality within the whole",
    gifts: ["Big-picture thinking", "Humanitarian heart", "Original ideas"],
    shadows: ["Detachment that becomes distance", "Rebellion without direction"],
    quote: "As long as you live, keep learning how to live.",
    exercises: [
      "Morning: write one idea that could help others",
      "Midday: question one assumption you hold",
      "Evening: connect with one person outside your circle",
    ],
    practice: "Start each day asking: 'How can I use my mind to serve the whole?'",
  },
  {
    sign_id: "taurus",
    philosopher: "Zeno",
    title: "The Steadfast",
    subtitle: "Nature's rhythm",
    gifts: ["Unshakeable patience", "Sensory appreciation", "Dependable strength"],
    shadows: ["Stubbornness that resists change", "Comfort that becomes complacency"],
    quote: "Well-being is realized by small steps, but is truly no small thing.",
    exercises: [
      "Morning: one minute of slow, deep breathing",
      "Midday: notice one simple pleasure fully",
      "Evening: name one thing you can release",
    ],
    practice: "Let nature set your pace — the steady river outlasts the storm.",
  },
];

function carouselSlide(sign, page, total, content) {
  const color = sign.color;
  const symbol = sign.symbol;
  const signName = sign.name.toUpperCase();
  const phil = content.philosopher;

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
    <filter id="marble"><feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="4" seed="12" result="noise"/><feColorMatrix type="saturate" values="0" in="noise" result="gray"/><feComponentTransfer in="gray" result="faded"><feFuncA type="linear" slope="0.04"/></feComponentTransfer><feBlend in="faded" in2="SourceGraphic" mode="overlay"/></filter>
    <filter id="glow"><feGaussianBlur stdDeviation="6" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1080" height="1080" fill="url(#bgGrad)" filter="url(#marble)"/>
  <rect x="20" y="20" width="1040" height="1040" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.5"/>
  <rect x="30" y="30" width="1020" height="1020" fill="none" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <line x1="100" y1="45" x2="980" y2="45" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>
  <line x1="100" y1="1034" x2="980" y2="1034" stroke="url(#goldGrad)" stroke-width="1" opacity="0.3"/>
  <path d="M 36 46 L 36 36 L 46 36" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 1044 46 L 1044 36 L 1034 36" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 36 1034 L 36 1044 L 46 1044" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <path d="M 1044 1034 L 1044 1044 L 1034 1044" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.5"/>
  <!-- Brand badge -->
  <text x="540" y="115" font-family="Raleway,sans-serif" font-size="13" font-weight="600" letter-spacing="5" fill="#D4AF37" text-anchor="middle" opacity="0.7">STOIC WISDOM</text>
  <!-- Sign top right -->
  <text x="990" y="100" font-family="serif" font-size="40" fill="${color}" text-anchor="end" opacity="0.8">${symbol}</text>
  ${content.header
    ? `<text x="540" y="250" font-family="'Playfair Display',Georgia,serif" font-size="42" fill="#F5F5F5" text-anchor="middle">${content.header}</text>
  <line x1="340" y1="290" x2="740" y2="290" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.2"/>`
    : `<text x="540" y="280" font-family="'Playfair Display',Georgia,serif" font-size="46" fill="${color}" text-anchor="middle" filter="url(#glow)">${symbol}</text>
  <text x="540" y="360" font-family="Raleway,sans-serif" font-size="30" font-weight="700" letter-spacing="6" fill="#D4AF37" text-anchor="middle">${signName}</text>
  <text x="540" y="410" font-family="Raleway,sans-serif" font-size="14" letter-spacing="4" fill="${color}" text-anchor="middle" opacity="0.6">${content.subtitle.toUpperCase()}</text>
  <line x1="340" y1="440" x2="740" y2="440" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.3"/>`}
  ${content.body}
  <!-- Page number -->
  <circle cx="540" cy="1055" r="14" fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.3"/>
  <text x="540" y="1060" font-family="Raleway,sans-serif" font-size="12" font-weight="600" fill="#D4AF37" text-anchor="middle" opacity="0.5">${page}/${total}</text>
</svg>`;
}

function buildSpotlightSlides(sign, info) {
  const color = sign.color;
  const slides = [];

  // Slide 1: Title
  slides.push(carouselSlide(sign, 1, 7, {
    subtitle: info.title,
    body: `<text x="540" y="560" font-family="'Playfair Display',Georgia,serif" font-size="28" fill="#F5F5F5" text-anchor="middle" font-style="italic" opacity="0.8">The Stoic ${info.title.split("The ")[1] || info.title}</text>
  <text x="540" y="620" font-family="'Playfair Display',Georgia,serif" font-size="20" fill="#C9A96E" text-anchor="middle" opacity="0.6">${info.subtitle}</text>
  <line x1="400" y1="670" x2="680" y2="670" stroke="#C9A96E" stroke-width="0.5" opacity="0.2"/>
  <rect x="225" y="720" width="630" height="46" rx="23" fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.4"/>
  <text x="540" y="748" font-family="Raleway,sans-serif" font-size="14" font-weight="500" letter-spacing="2" fill="#D4AF37" text-anchor="middle">ELEMENT: ${sign.element.toUpperCase()}</text>
  <text x="540" y="860" font-family="serif" font-size="18" font-style="italic" fill="#C9A96E" text-anchor="middle" opacity="0.5">Swipe to discover your stoic path →</text>`,
    header: null
  }));

  // Slide 2: Archetype
  slides.push(carouselSlide(sign, 2, 7, {
    subtitle: info.title,
    header: "Natural Gifts",
    body: info.gifts.map((g, i) =>
      `<text x="180" y="${360 + i * 90}" font-family="serif" font-size="24" fill="${color}" text-anchor="middle" opacity="0.7">✦</text>
  <text x="540" y="${360 + i * 90}" font-family="Raleway,sans-serif" font-size="26" font-weight="500" fill="#F5F5F5" text-anchor="middle" opacity="0.85">${g}</text>`
    ).join("\n  ")
  }));

  // Slide 3: Shadow
  slides.push(carouselSlide(sign, 3, 7, {
    subtitle: info.title,
    header: "The Shadow",
    body: `<text x="540" y="380" font-family="serif" font-size="22" font-style="italic" fill="#C9A96E" text-anchor="middle" opacity="0.7">What to watch for</text>
  ${info.shadows.map((s, i) =>
    `<text x="180" y="${470 + i * 90}" font-family="serif" font-size="24" fill="${color}" text-anchor="middle" opacity="0.7">⚠</text>
  <text x="540" y="${470 + i * 90}" font-family="Raleway,sans-serif" font-size="24" fill="#F5F5F5" text-anchor="middle" opacity="0.8">${s}</text>`
  ).join("\n  ")}`
  }));

  // Slide 4: Stoic wisdom quote
  slides.push(carouselSlide(sign, 4, 7, {
    subtitle: info.title,
    header: "Stoic Wisdom",
    body: `<text x="540" y="430" font-family="'Playfair Display',Georgia,serif" font-size="36" fill="#D4AF37" text-anchor="middle">"${info.quote}"</text>
  <text x="540" y="500" font-family="serif" font-size="22" font-style="italic" fill="#F5F5F5" text-anchor="middle" opacity="0.8">— ${info.philosopher}</text>
  <line x1="400" y1="560" x2="680" y2="560" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <text x="540" y="640" font-family="Raleway,sans-serif" font-size="18" fill="#C9A96E" text-anchor="middle" opacity="0.7">This is the medicine for your shadow.</text>`
  }));

  // Slide 5: Application exercises
  slides.push(carouselSlide(sign, 5, 7, {
    subtitle: info.title,
    header: "3 Exercises",
    body: info.exercises.map((e, i) =>
      `<text x="180" y="${380 + i * 110}" font-family="serif" font-size="26" fill="${color}" text-anchor="middle">${["I","II","III"][i]}</text>
  <text x="540" y="${380 + i * 110}" font-family="Raleway,sans-serif" font-size="22" fill="#F5F5F5" text-anchor="middle" opacity="0.85">${e}</text>`
    ).join("\n  ")
  }));

  // Slide 6: Daily practice
  slides.push(carouselSlide(sign, 6, 7, {
    subtitle: info.title,
    header: "Daily Practice",
    body: `<text x="540" y="430" font-family="'Playfair Display',Georgia,serif" font-size="26" font-style="italic" fill="#C9A96E" text-anchor="middle">${info.practice}</text>
  <line x1="400" y1="500" x2="680" y2="500" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <text x="540" y="580" font-family="Raleway,sans-serif" font-size="18" fill="#F5F5F5" text-anchor="middle" opacity="0.6">Repeat daily. Small steps, steady progress.</text>`
  }));

  // Slide 7: CTA
  slides.push(carouselSlide(sign, 7, 7, {
    subtitle: info.title,
    header: "Save This",
    body: `<text x="540" y="400" font-family="'Playfair Display',Georgia,serif" font-size="34" fill="#F5F5F5" text-anchor="middle">Tag a ${sign.name} who</text>
  <text x="540" y="460" font-family="'Playfair Display',Georgia,serif" font-size="34" fill="${color}" text-anchor="middle">needs this today ♥</text>
  <line x1="400" y1="520" x2="680" y2="520" stroke="#C9A96E" stroke-width="0.5" opacity="0.2"/>
  <text x="540" y="600" font-family="Raleway,sans-serif" font-size="20" letter-spacing="2" fill="#D4AF37" text-anchor="middle">FOLLOW @STOICZODIAC</text>
  <text x="540" y="650" font-family="Raleway,sans-serif" font-size="15" fill="#F5F5F5" text-anchor="middle" opacity="0.5">Daily wisdom for every sign</text>`
  }));

  return slides;
}

// --- MAIN ---
// --- CLI ---

const weekArg = process.argv.find((a) => a.startsWith("--week="));
const weekFolder = weekArg ? weekArg.split("=")[1] : "week_20260907";

const outDir = path.resolve(__dirname, `../../11_MEDIA_LIBRARY/SCHEDULED/${weekFolder}/carousels`);
fs.mkdirSync(outDir, { recursive: true });

console.log("=== Sign Spotlights ===");
spotlights.forEach((spot) => {
  const sign = signMap[spot.sign_id];
  const slides = buildSpotlightSlides(sign, spot);
  const dir = path.join(outDir, `spotlight_${spot.sign_id}`);
  fs.mkdirSync(dir, { recursive: true });
  slides.forEach((svg, i) => {
    const filepath = path.join(dir, `slide_${i + 1}_of_7.svg`);
    fs.writeFileSync(filepath, svg, "utf8");
    console.log(`  ✓ spotlight_${spot.sign_id}/slide_${i + 1}_of_7.svg`);
  });
});

console.log("\n✅ Carousels done!");