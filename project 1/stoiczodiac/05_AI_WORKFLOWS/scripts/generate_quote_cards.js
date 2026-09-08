/**
 * Generate 7 finished quote card SVGs for the current week.
 * Reads sign_master_data.json and the weekly brief, outputs to
 * 11_MEDIA_LIBRARY/SCHEDULED/week_YYYYMMDD/quotes/
 */

const fs = require("fs");
const path = require("path");

// Load sign data
const signData = JSON.parse(
  fs.readFileSync(
    path.resolve(__dirname, "../sign_master_data.json"),
    "utf8"
  )
);

const signMap = {};
signData.signs.forEach((s) => {
  signMap[s.id] = s;
});

const philosopherMap = {};
signData.philosophers.forEach((p) => {
  philosopherMap[p.name] = p;
});

// This week's schedule from WEEKLY_BATCH_BRIEF
const week = [
  {
    day: "Monday",
    date: "Sep 7",
    sign_id: "capricorn",
    philosopher: "Epictetus",
    theme: "The weight of responsibility",
    quote:
      "We are not responsible for the impressions that come to us, but we are responsible for how we respond to them.",
    application:
      "Capricorn, your ambition is a gift — but only when tethered to virtue. Respond to every duty as if it were your last.",
    challenge: "Take on one task today not for reward, but because it is right.",
  },
  {
    day: "Tuesday",
    date: "Sep 8",
    sign_id: "aquarius",
    philosopher: "Marcus Aurelius",
    theme: "The common good",
    quote:
      "What is good for the hive is good for the bee. What is good for the whole is good for the part.",
    application:
      "Aquarius, your vision for a better world begins with the small acts of kindness today. The future is built in the present.",
    challenge: "Do one thing today that benefits someone else without them knowing.",
  },
  {
    day: "Wednesday",
    date: "Sep 9",
    sign_id: "pisces",
    philosopher: "Seneca",
    theme: "The courage to let go",
    quote:
      "Sometimes even to live is an act of courage. But to let go of what harms you — that is wisdom.",
    application:
      "Pisces, you feel deeply — but not everything you feel must be carried. Let the weight of what isn't yours fall away.",
    challenge: "Release one attachment today that no longer serves your peace.",
  },
  {
    day: "Thursday",
    date: "Sep 10",
    sign_id: "aries",
    philosopher: "Epictetus",
    theme: "Choosing your battles",
    quote:
      "No man is free who is not master of himself. The wise warrior chooses his battles with care.",
    application:
      "Aries, your fire is powerful — but power without direction burns everything. Channel your impulse where it matters most.",
    challenge: "Before reacting today, pause and ask: 'Is this worth my fire?'",
  },
  {
    day: "Friday",
    date: "Sep 11",
    sign_id: "taurus",
    philosopher: "Zeno",
    theme: "Nature's rhythm",
    quote:
      "The end of life is to live in accordance with nature. The steady river outlasts the raging storm.",
    application:
      "Taurus, your stubbornness is strength when aligned with nature's flow. Resist less, endure wisely.",
    challenge: "Notice one natural rhythm today — sunrise, breath, silence — and match its pace.",
  },
  {
    day: "Saturday",
    date: "Sep 12",
    sign_id: "gemini",
    philosopher: "Marcus Aurelius",
    theme: "The power of stillness",
    quote:
      "Nowhere can you find a quieter retreat than in your own soul. Constant motion exhausts the spirit.",
    application:
      "Gemini, your mind thrives on movement — but wisdom is born in stillness. Let silence sharpen your thoughts.",
    challenge: "Spend 5 minutes today in complete silence. No input. No output. Just being.",
  },
  {
    day: "Sunday",
    date: "Sep 13",
    sign_id: "cancer",
    philosopher: "Seneca",
    theme: "Resilience of the heart",
    quote:
      "The tough tree bends in the wind but does not break. The heart armored in virtue withstands all storms.",
    application:
      "Cancer, your sensitivity is not weakness — it is your compass. Protect your heart with wisdom, not walls.",
    challenge: "Name one thing you're feeling today, then choose how to respond — not react.",
  },
];

// Template SVG — uses the sample_finished_quote_card.svg structure
function generateQuoteSVG(sign, philosopher, theme, quote, application, challenge) {
  const color = sign.color;
  const symbol = sign.symbol;
  const signName = sign.name.toUpperCase();
  const element = sign.element;
  // Map philosopher to era for subtitle
  const phil = philosopherMap[philosopher] || { era: "" };
  const philLabel = `— ${philosopher}`;
  // Element badge
  const elementUpper = element.toUpperCase();

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
    <filter id="marble">
      <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="4" seed="3" result="noise"/>
      <feColorMatrix type="saturate" values="0" in="noise" result="gray"/>
      <feComponentTransfer in="gray" result="faded">
        <feFuncA type="linear" slope="0.06"/>
      </feComponentTransfer>
      <feBlend in="faded" in2="SourceGraphic" mode="overlay"/>
    </filter>
    <filter id="textGlow">
      <feGaussianBlur stdDeviation="1" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1080" height="1080" fill="url(#bgGrad)" filter="url(#marble)"/>

  <!-- Outer gold border -->
  <rect x="30" y="30" width="1020" height="1020" fill="none" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.7"/>
  <rect x="40" y="40" width="1000" height="1000" fill="none" stroke="#D4AF37" stroke-width="0.5" opacity="0.3"/>

  <!-- Top accent line -->
  <line x1="240" y1="60" x2="840" y2="60" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.5"/>
  <line x1="240" y1="1018" x2="840" y2="1018" stroke="url(#goldGrad)" stroke-width="1.5" opacity="0.5"/>

  <!-- Corner ornaments -->
  <path d="M 46 60 L 46 46 L 60 46" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.6"/>
  <path d="M 1034 60 L 1034 46 L 1020 46" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.6"/>
  <path d="M 46 1020 L 46 1034 L 60 1034" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.6"/>
  <path d="M 1034 1020 L 1034 1034 L 1020 1034" fill="none" stroke="url(#goldGrad)" stroke-width="2" opacity="0.6"/>

  <!-- Diamond accent -->
  <polygon points="540,975 545,980 540,985 535,980" fill="#D4AF37" opacity="0.35"/>

  <!-- ========== CONTENT ========== -->

  <!-- Stoic Wisdom badge (top-center) -->
  <rect x="330" y="100" width="420" height="44" rx="22" fill="none" stroke="url(#goldGrad)" stroke-width="1" opacity="0.5"/>
  <text x="540" y="127" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="15" font-weight="600" letter-spacing="5" fill="#D4AF37" text-anchor="middle" opacity="0.85">STOIC WISDOM</text>

  <!-- Sign badge — top-right -->
  <text x="940" y="190" font-family="serif" font-size="56" fill="${color}" text-anchor="end" opacity="0.9">${symbol}</text>
  <text x="940" y="220" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="18" font-weight="600" fill="${color}" text-anchor="end" letter-spacing="3" opacity="0.7">${signName}</text>
  <text x="940" y="240" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="11" fill="${color}" text-anchor="end" letter-spacing="1" opacity="0.4">${elementUpper}</text>

  <!-- Pill badge: theme -->
  <rect x="380" y="175" width="320" height="32" rx="16" fill="none" stroke="#C9A96E" stroke-width="0.8" opacity="0.4"/>
  <text x="540" y="196" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="12" font-weight="500" letter-spacing="2" fill="#C9A96E" text-anchor="middle" opacity="0.6">${theme.toUpperCase()}</text>

  <!-- Decorative line before quote -->
  <line x1="250" y1="310" x2="830" y2="310" stroke="url(#goldGrad)" stroke-width="0.5" opacity="0.2"/>

  <!-- Large quote mark (background) -->
  <text x="160" y="500" font-family="Georgia, serif" font-size="200" fill="url(#goldGrad)" opacity="0.06">"</text>

  <!-- MAIN QUOTE — split into lines of ~50 characters -->
  ${wrapQuote(quote)}

  <!-- Attribution -->
  <line x1="400" y1="610" x2="680" y2="610" stroke="#D4AF37" stroke-width="0.5" opacity="0.2"/>
  <text x="540" y="650" font-family="'Cormorant Garamond', 'Times New Roman', serif" font-size="24" font-style="italic" fill="#F5F5F5" text-anchor="middle" opacity="0.85">${philLabel}</text>

  <!-- Application line -->
  <line x1="200" y1="780" x2="880" y2="780" stroke="#C9A96E" stroke-width="0.5" opacity="0.15"/>
  <text x="540" y="820" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="16" fill="#F5F5F5" text-anchor="middle" opacity="0.6">${application}</text>

  <!-- Daily challenge pill -->
  <rect x="340" y="870" width="400" height="38" rx="19" fill="none" stroke="#D4AF37" stroke-width="1" opacity="0.5"/>
  <text x="540" y="895" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="13" font-weight="600" fill="#D4AF37" text-anchor="middle" letter-spacing="1">TODAY: ${challenge}</text>

  <!-- CTA watermark -->
  <text x="540" y="1010" font-family="Raleway, 'Helvetica Neue', sans-serif" font-size="12" fill="#F5F5F5" text-anchor="middle" opacity="0.3" letter-spacing="2">@STOICZODIAC</text>
</svg>`;
}

/** Split a long quote into ~50-char lines for the SVG */
function wrapQuote(quote) {
  const maxLineLen = 48;
  const words = quote.split(" ");
  const lines = [];
  let current = "";
  for (const w of words) {
    if ((current + " " + w).trim().length <= maxLineLen) {
      current = (current + " " + w).trim();
    } else {
      if (current) lines.push(current);
      current = w;
    }
  }
  if (current) lines.push(current);

  // Build the SVG text lines
  // Quote starts at y=410, line height ~65px
  const startY = 410 - ((lines.length - 2) * 34); // center vertically
  let yPos = startY;
  let svgLines = "";
  lines.forEach((line) => {
    svgLines +=
      `  <text x="540" y="${yPos}" font-family="'Playfair Display', Georgia, serif" font-size="48" fill="#D4AF37" text-anchor="middle" filter="url(#textGlow)">"${escapeXml(line)}"</text>\n`;
    yPos += 65;
  });

  // Remove the extra quotes — only the first and last line get them
  svgLines = svgLines.replace(
    /<text[^>]*>"(.*?)"<\/text>/g,
    (match, content) => {
      return match.replace(`"${content}"`, `${content}`);
    }
  );
  // First line gets opening quote, last line gets closing quote
  const firstLineMatch = svgLines.match(/<text[^>]*>([^<]+)<\/text>/);
  const linesArr = svgLines.trim().split("\n");
  if (linesArr.length > 0) {
    const firstLine = linesArr[0];
    const lastLine = linesArr[linesArr.length - 1];
    linesArr[0] = firstLine.replace(
      /<text([^>]*)>([^<]+)<\/text>/,
      '<text$1>"$2</text>'
    );
    linesArr[linesArr.length - 1] = lastLine.replace(
      /<text([^>]*)>([^<]+)<\/text>/,
      '<text$1>$2"</text>'
    );
  }
  return linesArr.join("\n");
}

function escapeXml(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// --- MAIN ---

// --- CLI ---

const weekArg = process.argv.find((a) => a.startsWith("--week="));
const weekFolder = weekArg ? weekArg.split("=")[1] : "week_20260907";

const outDir = path.resolve(
  __dirname,
  `../../11_MEDIA_LIBRARY/SCHEDULED/${weekFolder}/quotes`
);
fs.mkdirSync(outDir, { recursive: true });

week.forEach((day) => {
  const sign = signMap[day.sign_id];
  if (!sign) {
    console.error(`  ✗ Unknown sign: ${day.sign_id}`);
    return;
  }
  const slug = `${day.date.replace(/\s/g, "_")}_${day.sign_id}_${day.philosopher.replace(/\s/g, "_")}`
    .toLowerCase();
  const filename = `quote_${slug}.svg`;
  const filepath = path.join(outDir, filename);

  const svg = generateQuoteSVG(
    sign,
    day.philosopher,
    day.theme,
    day.quote,
    day.application,
    day.challenge
  );

  fs.writeFileSync(filepath, svg, "utf8");
  console.log(`  ✓ ${filename}`);
});

console.log(`\n✅ Generated ${week.length} quote cards in ${outDir}`);