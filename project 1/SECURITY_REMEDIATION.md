# Security Remediation Summary

**Date**: 2026-10-11
**Status**: Phase 1 complete, Phase 2 pending user action

---

## Phase 1 — Script Cleanup (✅ Done)

### Problem
All debugging scripts in `06_AUTOMATION/openreply/` had **hardcoded Facebook App Secrets** — plaintext credentials committed to the Git history and pushed to a public GitHub repo since ~2026-08-18.

### Exposed Secret
- **App Secret**: `b2708ce0c790783fbf27c0dfcc0e1459`
- **App ID**: `1051360407668084` (Facebook app `stoiczodiac-dm`)
- **Location**: Public GitHub repo, commit history, possible scrapers/archives

### Scripts Fixed (6 total)

| Script | What Changed |
|--------|-------------|
| `try_link2.mjs` | `FB_APP_SECRET` → `process.env.FB_APP_SECRET` |
| `try_link.mjs` | `FB_APP_SECRET` → `process.env.FB_APP_SECRET` |
| `try-bm-fetch.mjs` | Removed hardcoded token references |
| `try-bm.mjs` | Removed hardcoded token references |
| `test_ig_webhook.mjs` | Removed hardcoded credentials |
| `fix_webhooks.mjs` | Removed hardcoded credentials |

All replaced with `process.env` environment variable lookups. The app IDs remain in source — they are public identifiers, not secrets.

---

## Phase 2 — Repository Protection (✅ Done)

### Created root `.gitignore`
File: `C:\Users\marcj\Stoic1\project 1\.gitignore`

Patterns now protected:
- `.env` / `.env.*` — environment files with secrets
- `node_modules/` — dependencies
- `dist/` — build outputs
- `voltagent/` — 3 GB junk clone (accidental)
- `.vercel` — Vercel project config
- OS files (`.DS_Store`, `Thumbs.db`, swap files)
- IDE files (`.vscode/`, `.idea/`)
- Generated carousel PNGs (tracked intentionally, never blindly)
- Python cache (`__pycache__/`, `.pyc`)

### Critical Gap Closed
The `04_TEMPLATES/canva-app/` directory had its own `.gitignore` but it only covered a few patterns. The root `.gitignore` now catches `.env`, `node_modules/`, and `dist/` at every depth.

---

## Phase 3 — Two-App Correction (🔍 Investigation Complete)

**Earlier investigation mistakenly treated all tokens as belonging to a single app.** There are actually **two** Meta apps:

| App | ID | Purpose |
|-----|----|---------|
| **Facebook app** (`stoiczodiac-dm`) | `1051360407668084` | Facebook/Instagram Business Login, webhooks, DMs |
| **Instagram app** | `2616058292165458` | IGAA token exchange, graph.instagram.com |

The exposed App Secret (`b2708ce0c790783fbf27c0dfcc0e1459`) belongs to the Facebook app (`1051360407668084`), but **leaked tokens could belong to either app**.

### Leaked Tokens
1. **IGAA token** (prefix: `IGAA...`) — Instagram app token, powers DMs/inbox/media
2. **Page token** (prefix: `EA...`) — Facebook Page token, works with `graph.facebook.com`
3. **User token** — Long-lived user access token

---

## Phase 4 — Security Action Plan (⏳ Pending User)

### Step 1: Token Debugger — Identify Issuing App(s)
Use Meta's Token Debugger to check each leaked token:

> **https://developers.facebook.com/tools/debug/accesstoken/**

For each token, the debugger will show:
- Which app ID issued it
- Whether it's still valid or expired
- Scopes granted
- Expiration date

**Do not reset any app secret yet** — first determine which app(s) the live tokens belong to.

### Step 2: Reset App Secret(s) — Conditional
- If any token is **still valid**, reset that app's secret immediately:
  - Facebook app: `https://developers.facebook.com/apps/1051360407668084/settings/basic/`
  - Instagram app: `https://developers.facebook.com/apps/2616058292165458/settings/basic/`
- If all tokens are already expired, this is lower urgency but still recommended

### Step 3: Confirm Leaked Tokens Are Dead
After reset, verify via Token Debugger that old tokens return an error.

### Step 4: Check for Abuse
- Review the app's dashboard for unusual API calls
- Check if any unexpected Instagram DMs were sent or media was accessed
- Review webhook logs in OpenReply

### Step 5: Issue Fresh Tokens
- **IGAA token**: Visit `https://openreply-zeta-ruby.vercel.app/api/auth/igaa-token`, click "Connect Instagram"
- **Page token**: Run `fb_token_helper.mjs` locally
- Update `.env` files with fresh tokens

### Step 6: Make Repos Private
- GitHub repos should be made private to prevent future scrapes
- Consider squashing or removing the commit history that contained the secret (or just rotate — history is already public)

---

## Remaining Housekeeping

| Item | Status |
|------|--------|
| Root `.gitignore` created | ✅ Done |
| 6 scripts cleaned | ✅ Done |
| Security summary written | ✅ Done |
| `voltagent/` directory deleted | ⏳ Recommend: `rm -rf voltagent/` |
| `VibeVoice` submodule init | ⏳ Recommend: `git submodule update --init` |
| Token Debugger check | 🔲 User action needed |
| App secret reset | 🔲 User action needed (conditional) |
| Make repo(s) private | 🔲 User action needed |