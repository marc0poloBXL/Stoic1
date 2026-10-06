import {Client} from "pg";
const c = new Client({connectionString: process.env.DATABASE_URL});
await c.connect();

const wsId = "cmt4clzom000170vevrv5oqrf";
const igId = "cmtocgan5000004kzet71p0ka";

const campaigns = [
  {
    name: "🌿 Wisdom Seeker — Daily Stoic",
    keywords: ["wisdom", "quote", "stoic", "philosophy", "guide", "daily", "today"],
    matchAnyWord: true,
    dmMessage: "Here's a Stoic reflection for you today:\n\n\"The happiness of your life depends upon the quality of your thoughts.\"\n— Marcus Aurelius\n\nTap below for your personalized Stoic wisdom based on your zodiac sign ✨",
    linkButtonLabel: "Get Your Sign's Wisdom",
    openingDmEnabled: true,
    openingDmMessage: "🌟 Thank you for connecting with Stoic Zodiac!\n\nEvery sign has a philosopher who speaks directly to its soul. Which zodiac sign are you? Reply with your sign ✨",
    openingDmButtonLabel: "I'll Tell You",
    requireFollow: true,
    followPromptMessage: "🌀 To unlock your personalized Stoic wisdom, please follow @stoiczodiac first!\n\nTap follow, then come back and tap the button below ✨",
    followPromptButtonLabel: "✅ I Followed!",
    followUpEnabled: true,
    followUpMessage: "🌅 Come back tomorrow for a new Stoic reflection for your sign. Save this chat to get your daily dose of ancient wisdom.\n\n— @stoiczodiac",
    followUpDelayMinutes: 1440, // 24 hours
    publicReplyEnabled: true,
    publicReplyMessages: ["✨ Wisdom sent to your DMs! Check your inbox 🦁", "📬 Check your DMs for a Stoic reflection tailored to you!", "🌿 A Stoic quote is waiting in your messages. Tap to see!"],
    matchAnyPost: true,
    isActive: true,
  },
  {
    name: "♈ Sign-Specific Wisdom",
    keywords: ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces", "my sign", "what sign"],
    matchAnyWord: true,
    dmMessage: "Your sign has a philosopher who speaks directly to your soul.\n\nTap the link below to discover which Stoic philosopher guides your path and what wisdom they have for you today ✨",
    linkButtonLabel: "🔮 My Stoic Guide",
    openingDmEnabled: false,
    requireFollow: false,
    matchAnyPost: true,
    isActive: true,
    wholeWordMatch: true,
  },
  {
    name: "💬 DM — Free Stoic Guide",
    keywords: ["free", "pdf", "ebook", "guide", "download", "resource", "learn"],
    matchAnyWord: true,
    dmMessage: "📖 Here's a free Stoic guide to help you navigate life with ancient wisdom.\n\nTap the link below to access it ✨",
    linkButtonLabel: "📕 Get the Guide",
    dmTriggerEnabled: true,
    openingDmEnabled: false,
    requireFollow: true,
    followPromptMessage: "🌀 Follow @stoiczodiac to unlock your free Stoic guide!\n\nTap follow, then come back ✨",
    followPromptButtonLabel: "✅ Done!",
    followUpEnabled: true,
    followUpMessage: "📚 Did you download your guide? Let me know if you have any questions about Stoic philosophy!\n\n— @stoiczodiac",
    followUpDelayMinutes: 1440,
    matchAnyPost: false,
    isActive: true,
  },
];

let count = 0;
for (const cam of campaigns) {
  await c.query(`
    INSERT INTO "Automation" (id, "workspaceId", "instagramAccountId", name, keywords, "matchAnyWord", "wholeWordMatch", "dmMessage", "linkButtonLabel", "openingDmEnabled", "openingDmMessage", "openingDmButtonLabel", "requireFollow", "followPromptMessage", "followPromptButtonLabel", "followUpEnabled", "followUpMessage", "followUpDelayMinutes", "publicReplyEnabled", "publicReplyMessages", "matchAnyPost", "dmTriggerEnabled", "isActive", "createdAt", "updatedAt")
    VALUES (gen_random_uuid()::text, $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, NOW(), NOW())
  `, [
    wsId, igId, cam.name, cam.keywords, cam.matchAnyWord, cam.wholeWordMatch ?? true,
    cam.dmMessage, cam.linkButtonLabel ?? null,
    cam.openingDmEnabled, cam.openingDmMessage ?? null, cam.openingDmButtonLabel ?? null,
    cam.requireFollow, cam.followPromptMessage ?? null, cam.followPromptButtonLabel ?? null,
    cam.followUpEnabled, cam.followUpMessage ?? null, cam.followUpDelayMinutes ?? 0,
    cam.publicReplyEnabled, cam.publicReplyMessages ?? [],
    cam.matchAnyPost, cam.dmTriggerEnabled ?? false, cam.isActive,
  ]);
  count++;
  console.log(`✅ Created: "${cam.name}"`);
}

console.log(`\n🎉 ${count} campaigns created successfully!`);
await c.end();