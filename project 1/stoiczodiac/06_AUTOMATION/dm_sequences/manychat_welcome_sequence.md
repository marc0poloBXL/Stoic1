# ManyChat DM Automation — Welcome Sequence

> **🔗 Source of truth for sign data**: `05_AI_WORKFLOWS/sign_master_data.json`
> Sign names, symbols, and philosopher mappings should be kept in sync with that file.

**Tool**: ManyChat (Free tier — up to 1,000 contacts)  
**Trigger**: User follows @stoiczodiac  
**Goal**: Convert followers into engaged community → eventual monetization

---

## 🧩 ManyChat Free Setup Steps

1. **Sign up** at [manychat.com](https://manychat.com) (free tier)
2. **Connect Instagram** Business account (convert personal if needed)
3. **Create a new flow**: "Welcome New Followers"
4. **Set trigger**: "User sends first message" (or "User follows" — may require Business)
5. **Build the sequence below** in the flow builder

---

## 💬 Message 1: Welcome (Instant)

**Trigger**: User follows or sends "Hi"

```
[Text]
Hey there 🙏 Welcome to Stoic Wisdom × Zodiac Signs.

I'm here to help you find ancient wisdom for your modern life — tailored to YOUR sign.

Tell me something first:
What's your zodiac sign? ♈♉♊♋♌♍♎♏♐♑♒♓

[Quick Replies]
♈ Aries  ♉ Taurus  ♊ Gemini  ♋ Cancer
♌ Leo    ♍ Virgo   ♎ Libra   ♏ Scorpio
♐ Sagittarius  ♑ Capricorn  ♒ Aquarius  ♓ Pisces
```

---

## 💬 Message 2: Sign-Specific Response (Sent after user picks sign)

**Trigger**: User selects a sign from quick replies  
**Condition**: Branch by sign selection

```
[Text — use the appropriate block below]

=== ♈ ARIES ===
Aries — the warrior. 🔥
Marcus Aurelius himself was a warrior-emperor, and he wrote:
"The soul becomes dyed with the color of its thoughts."
Your fire is your greatest gift, but it needs direction. Today, channel that impulse into action that serves something bigger than yourself.
Save this. Come back tomorrow for your Aries wisdom.

=== ♉ TAURUS ===
Taurus — the steadfast. 🌿
Seneca wrote: "It is not the man who has too little, but the man who craves more, who is poor."
Your strength is your stability. But true freedom comes from letting go, not holding on.
Today, notice one thing you're attached to — and ask yourself: do I own it, or does it own me?
Save this. Come back tomorrow for your Taurus wisdom.

=== ♊ GEMINI ===
Gemini — the thinker. 💨
Epictetus said: "We are not disturbed by what happens to us, but by our thoughts about what happens."
Your mind is a gift — but also your greatest challenge. The stoic path for you is discernment: not every thought needs your attention.
Today, observe your thoughts without judgment. Just watch.
Save this. Come back tomorrow for your Gemini wisdom.

=== ♋ CANCER ===
Cancer — the protector. 🌊
Marcus Aurelius wrote: "The best revenge is to be unlike him who performed the injury."
Your empathy is your superpower. But even the moon needs darkness to rest. Protect your energy as fiercely as you protect others.
Today, set one boundary. Just one.
Save this. Come back tomorrow for your Cancer wisdom.

=== ♌ LEO ===
Leo — the radiant. ☀️
Seneca advised: "Wherever there is a human being, there is an opportunity for kindness."
Your light draws people to you. The stoic path for you is humility — leading with service, not ego. True greatness lifts others.
Today, give someone credit without taking any.
Save this. Come back tomorrow for your Leo wisdom.

=== ♍ VIRGO ===
Virgo — the precise. 🌱
Epictetus taught: "First say to yourself what you would be; then do what you have to do."
Your pursuit of excellence is admirable. But perfection is not the goal — progress is. The stoic path is acting with virtue, not flawlessness.
Today, complete one thing at 80% and call it done.
Save this. Come back tomorrow for your Virgo wisdom.

=== ♎ LIBRA ===
Libra — the harmonizer. ⚖️
Marcus Aurelius wrote: "The happiness of your life depends upon the quality of your thoughts."
You seek balance in all things. The stoic insight: balance is not the absence of conflict — it's choosing the right response to it.
Today, sit with a disagreement instead of resolving it immediately.
Save this. Come back tomorrow for your Libra wisdom.

=== ♏ SCORPIO ===
Scorpio — the transformer. 🔥
Seneca said: "Sometimes even to live is an act of courage."
Your depth is unmatched. The stoic path for you is transformation — not through destruction, but through acceptance. What you resist can teach you.
Today, welcome one thing you've been avoiding.
Save this. Come back tomorrow for your Scorpio wisdom.

=== ♐ SAGITTARIUS ===
Sagittarius — the seeker. 🔥
Epictetus asked: "Who is the rich man? He who is content."
Your freedom is your oxygen. But true freedom comes from discipline, not escape. The stoic path is adventure with purpose.
Today, commit to one thing for 30 days.
Save this. Come back tomorrow for your Sagittarius wisdom.

=== ♑ CAPRICORN ===
Capricorn — the builder. 🏔️
Marcus Aurelius wrote: "Wake up in the morning and tell yourself: the people I deal with today will be meddling, ungrateful, arrogant..."
Your ambition is legendary. The stoic path: align your ambition with virtue. Build not just success, but character.
Today, do one thing that no one will see or applaud.
Save this. Come back tomorrow for your Capricorn wisdom.

=== ♒ AQUARIUS ===
Aquarius — the visionary. 🌬️
Seneca said: "We suffer more often in imagination than in reality."
Your vision is your gift. But the stoic path is grounding that vision in action. The future you imagine starts with what you do today.
Today, take one small step toward one big idea.
Save this. Come back tomorrow for your Aquarius wisdom.

=== ♓ PISCES ===
Pisces — the dreamer. 🌊
Epictetus taught: "Make the best use of what is in your power, and take the rest as it happens."
Your intuition is profound. But the stoic path is boundaries — compassion without losing yourself. You can feel deeply AND act wisely.
Today, ask yourself: "Is this mine to carry?"
Save this. Come back tomorrow for your Pisces wisdom.

=== 🔄 UNRECOGNIZED REPLY ===
[Fallback for when the user types something other than a sign name]
I didn't quite catch your sign! Tap one below and I'll send you personalized Stoic wisdom 🏛️

[Quick Replies — same 12-sign grid as Message 1]
♈ Aries  ♉ Taurus  ♊ Gemini  ♋ Cancer
♌ Leo    ♍ Virgo   ♎ Libra   ♏ Scorpio
♐ Sagittarius  ♑ Capricorn  ♒ Aquarius  ♓ Pisces
```

---

## 💬 Message 3: Free Guide Offer (24 hours later)

**Trigger**: 24-hour delay after Message 2  
**Condition**: User has not yet received a download link

```
[Text]
Hey again 🙌

I've been working on something special — a free "Stoic Guide for [SIGN]" based on the user's sign selection.

It includes:
🧘 3 stoic exercises tailored to your sign
📜 5 quotes that speak to your soul
⚡ Your daily stoic challenge

Want it? Just reply "YES" and I'll send you the PDF.

(No spam. No strings. Just wisdom.)

[Quick Replies]
YES — Send me the guide 🔥
Maybe later
```

---

## 💬 Message 4: Daily Challenge (48 hours later, if no guide requested)

**Trigger**: 48-hour delay after Message 2  
**Condition**: User did NOT request the guide

```
[Text]
Hey [Name] — just dropping in with your daily stoic challenge:

🧠 "Today, notice one thing you can control — and one thing you can't. Release the second. Act on the first."

That's it. Simple, but powerful.

If you ever want personalized wisdom for your sign, just reply with your sign. I'm here.

—
🦁 Stoic Wisdom × Zodiac Signs
```

---

## 🔄 Follow-up Automation Ideas (Free Tier Compatible)

| Trigger | Action | Notes |
|---------|--------|-------|
| User replies "YES" | Send PDF link | Use Google Drive link (free) |
| User replies "Maybe later" | Resend offer in 7 days | Use ManyChat timer |
| User replies with sign | Send sign-specific quote | Branch condition |
| User replies with "Stoic" | Add to "Engaged" tag | Use ManyChat tags |
| User replies 3+ times | Add to "Hot Lead" tag | Manual tag for now |

---

## 📎 Free Guide Setup

1. Create a **Google Doc** with the Stoic Guide content
2. Set sharing to "Anyone with the link can view"
3. Use a **URL shortener** (bit.ly free) for clean tracking
4. Paste the link in ManyChat Message 3

### Guide Content Structure (1 page per sign = 12 pages)
```
Page 1: Welcome + Your Sign's Stoic Archetype
Page 2: 3 Stoic Exercises for Your Sign
Page 3: 5 Quotes That Speak to You
Page 4: Your 30-Day Stoic Challenge
Page 5: Daily Practice Log
```