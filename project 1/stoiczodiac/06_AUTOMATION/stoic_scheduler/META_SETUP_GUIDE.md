# Meta Graph API Setup Guide

To post **carousels, reels, and stories** automatically, your Instagram account needs to be a **Professional (Creator) account** linked to a **Facebook Page**, and you need a **Meta developer app** to generate access tokens.

⏱️ **One-time setup** — about 30 minutes. After this, posting is fully automatic.

---

## Step 1: Switch Instagram to Professional (Creator)

1. Open the **Instagram app** on your phone
2. Go to your **Profile** → tap **☰ (menu)** → **Settings**
3. Tap **Account type and tools** → **Switch to professional account**
4. Choose **Creator**
5. Pick a category (e.g., "Blogger" or "Education")
6. Follow the prompts to finish
   > *You can switch back anytime, but the Meta API won't work without a professional account.*

---

## Step 2: Create a Facebook Page and link Instagram

> **You need a personal Facebook account** to manage a Page. If you don't have one, create one first at facebook.com.

1. Log in to **Facebook**
2. Go to your **Profile** → **Pages** → **Create Page**
3. Name it "Stoic Wisdom × Zodiac" (or similar) — it can stay unpublished
4. Open **Instagram app** → Profile → **Edit Profile**
5. Tap **Public Business Information** → **Page**
6. Select the Page you just created
7. Confirm linking

> After linking, your Instagram shows as *"Professional account linked to a Page"*.

---

## Step 3: Create a Meta Developer App

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Log in with your Facebook account
3. Click **My Apps** → **Create App**
4. Choose **"Business"** as the app type → click **Next**
5. Enter:
   - **App name**: `Stoic Scheduler`
   - **App contact email**: your email
6. Click **Create App**
7. In the dashboard, click **Add Product** → find **Instagram Graph API** → click **Set Up**

---

## Step 4: Get the Access Tokens

### A. Short-lived User Token

1. In your Meta app dashboard, find the **Instagram Graph API** section
2. Click **Generate Token**
3. Log in with your Facebook/Instagram
4. Accept the permissions dialog
5. Copy the **token** (looks like a long string of letters and numbers)

> If "Generate Token" isn't available, use the Graph API Explorer:
> 1. Go to `developers.facebook.com/tools/explorer`
> 2. Select your app from the dropdown
> 3. Add permissions: `instagram_basic`, `instagram_content_publish`, `pages_show_list`, `business_management`
> 4. Click **Generate Access Token**
> 5. Authorize → copy the token

### B. Exchange for a Long-Lived Token

Open this URL in your browser (replace `APP_ID` and `APP_SECRET` with yours):

```
https://graph.facebook.com/v20.0/oauth/access_token?
  grant_type=fb_exchange_token
  &client_id=APP_ID
  &client_secret=APP_SECRET
  &fb_exchange_token=SHORT_LIVED_TOKEN
```

Copy the `access_token` from the response — this is your **long-lived Page token** (good for ~60 days).

> In 60 days when it expires, repeat step 4 (A and B). Mark your calendar.

### C. Get App ID and App Secret

In your Meta app dashboard:
- **App ID** is on the dashboard home page
- **App Secret** is under **Settings → Basic** → **Show**

---

## Step 5: Save Everything to .env

Copy these into your `06_AUTOMATION/stoic_scheduler/.env` file:

```
INSTAGRAM_USERNAME=stoiczodiac
INSTAGRAM_PASSWORD=your_ig_password

META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_PAGE_ACCESS_TOKEN=the_long_lived_token

# Leave empty — the tool will auto-detect it:
META_IG_USER_ID=
```

---

## Step 6: Create a Vercel Blob Store

1. Log into [vercel.com](https://vercel.com)
2. Go to **Storage** → **Create Database**
3. Choose **Blob**
4. Give it a name (e.g., `stoic-scheduler-media`)
5. Choose a region (any is fine)
6. Click **Create**
7. In the Blob store dashboard, copy the **`BLOB_READ_WRITE_TOKEN`**
8. Add it to your `.env`:
   ```
   BLOB_READ_WRITE_TOKEN=your_blob_token
   ```

No Vercel project needed — the token alone is enough for the scheduler to upload files.

---

## Step 7: Run the Verification

```bash
cd 06_AUTOMATION/stoic_scheduler
python scheduler.py --meta-verify
```

This should print:
```
✅ Access OK — @stoiczodiac (id: 12345678901234567)
✅ Resolved IG Business Account ID: 12345678901234567
```

If it says it resolved the ID, copy that ID into your `.env` as `META_IG_USER_ID`.

---

## When Does the Token Expire?

| Token | Lifetime | What to do |
|-------|----------|-----------|
| Page Access Token | ~60 days | Repeat Step 4 (A + B), update .env |
| Blob Token | Never | OK as-is |

Mark a calendar reminder 50 days from now to refresh the token.

---

## ℹ️ Notes

- **Development mode works for self-posting.** In dev mode, your app can publish to your own Instagram account. Meta's App Review is only required to publish for *other* people's accounts.
- **All media is hosted temporarily on Vercel Blob.** The tool uploads each image/video, posts it, then deletes it. Nothing stays hosted longer than a few minutes.
- **Carousels are slides in folders.** Export your Canva carousel as "PNG pages" and drop them into `queued_carousels/<name>/` or `week_<date>/carousels/<name>/`. Each folder needs `1.png, 2.png,...` plus a `caption.txt`.
- **Reels are MP4 videos.** Drop them into `queued_reels/` directly or into `week_<date>/reels/`.
- **Stories are PNG/JPG images.** Drop them into `queued_stories/` or `week_<date>/stories/`.