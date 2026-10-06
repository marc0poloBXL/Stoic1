# 🚀 How to Install the Stoic Scheduler
### (Explained like you're 10 years old)

**Author**: Your robot helper
**For**: @stoiczodiac Instagram page

---

## What is this thing?

This is a robot that posts pictures to your Instagram for you.
It works while you sleep. It works while you're at school or work.
You set it up once, and then it does its job every day.

---

## Step 1: Open the Terminal

The **Terminal** is a black window where you can type commands to
make the computer do things. It looks scary but it's just a chat
with your computer.

1. Press the **Windows key** on your keyboard
2. Type **PowerShell**
3. Click the first result that says **PowerShell** (not VS Code, just PowerShell)
4. A dark blue window opens — that's the Terminal

Now type this and press Enter:

```powershell
cd stoiczodiac/06_AUTOMATION/stoic_scheduler
```

This tells the computer: *"Go to the scheduler folder."*

---

## Step 2: Install the Robot's Brain

The robot needs some parts to work. Type these commands one at a time.
Press **Enter** after each one. Wait for each to finish before typing the next.

**Command 1 — Install the main parts:**

```powershell
pip install -r requirements.txt
```

You'll see a lot of text flying by. That's normal. Wait until it stops.
It might take 2-3 minutes. Go grab a drink.

**Command 2 — Install the hidden browser:**

```powershell
python -m playwright install chromium
```

This downloads a tiny web browser that the robot uses secretly.
It's about the size of a small game. Wait until it finishes.

---

## Step 3: Tell the Robot Your Password

The robot needs to log into Instagram. You need to create a
**secret file** with your password.

**First**, make a copy of the example file:

```powershell
copy .env.example .env
```

You won't see anything happen. That's okay.

**Now**, open the secret file in Notepad:

```powershell
notepad .env
```

Notepad opens. You will see something like this:

```
INSTAGRAM_USERNAME=stoiczodiac
INSTAGRAM_PASSWORD=your_password_here
```

Change it to your actual password:

```
INSTAGRAM_USERNAME=stoiczodiac
INSTAGRAM_PASSWORD=MyRealPassword123
```

> **⚠️ IMPORTANT:** Use your REAL Instagram password.
> Don't use the same password you use for online banking.
> The file stays on YOUR computer. Nobody else can see it.

Click **File → Save**, then close Notepad.

---

## Step 4: Check That Everything Is Okay

Type this and press Enter:

```powershell
python scheduler.py --validate-config
```

You should see: **✅ Config validation passed**

If you see **❌ Config not found**, you're in the wrong folder.
Type `cd stoiczodiac/06_AUTOMATION/stoic_scheduler` again,
then retry.

You might see some yellow ⚠️ warnings about "Meta API" or
"META_PAGE_ACCESS_TOKEN". That's okay! That's only for
advanced features. We'll do that later.

---

## Step 5: Test the Robot (Without Posting)

Let's do a pretend run — no actual posting happens.

```powershell
python scheduler.py --dry-run
```

You should see something like:

```
📅 Today (Thursday, 2026-10-01)
   Scheduled slots: 07:00, 12:00, 18:00
   Current time: 16:54
   Time to post: ❌ NO (Next slot today at 18:00)

Queue is empty.
```

If you see this, the robot is alive! 🎉

---

## Step 6: Give the Robot Something to Post

Create a test post so you can watch it work.

**First**, create a simple test picture and caption:

```powershell
python -c "
from PIL import Image
img = Image.new('RGB', (1080, 1080), color=(20, 20, 30))
img.save('queued/01_test_post.png')
print('Picture created!')
"
```

```powershell
echo "This is a test post from the Stoic Scheduler! 🤖" > queued/01_test_post.txt
```

Now check the queue:

```powershell
python scheduler.py --status
```

You should see:

```
📋 Posting Queue:
  1. ⏳ [image] 01_test_post
     Caption: This is a test post from the Stoic Scheduler! 🤖…
```

The robot is ready! 🚀

---

## Step 7: Watch the Robot Post for Real

**⚠️ This will post to your real Instagram account. Only do this
if you want to test it with a real post.**

```powershell
python scheduler.py --post-now
```

The first time, a browser window will pop up. Watch it!

1. It will go to Instagram.com
2. It will fill in your username and password automatically
3. You might see a **"Enter Your Security Code"** screen
   — this is Instagram's 2FA code
   — if this happens, check your phone for the code,
     type it into the Notepad popup, and press Enter
4. It will click the + button, select your picture,
   write the caption, and click Share

**If the test post shows up on Instagram, everything works! ✅**

> After the first login, the robot saves its session.
> Next time, it won't need to log in again.

To remove the test post, go to Instagram, find it, and delete it.

---

## Step 8: Set Up the Robot to Post Automatically

This is the magic step. The robot will post by itself.
You don't need to do anything.

**Follow these steps carefully:**

1. Press the **Windows key** on your keyboard
2. Type **Task Scheduler**
3. Click the result that says **Task Scheduler**
   (It might say "task scheduler" next to a clock icon)
4. A window opens. On the right side, click **Create Basic Task…**

A wizard starts. Fill in these things:

| Screen | What to write |
|--------|--------------|
| **Name** | `Stoic Scheduler` |
| **Description** | `Posts Instagram content automatically` |
| **Trigger** | Choose **Daily** → click Next |
| **Time** | Any time is fine (we don't use this exact time anyway) |
| **Repeat every** | Check **Repeat every** → `15 minutes` → **Duration:** `Indefinitely` |
| **Action** | Choose **Start a program** → click Next |

Now for the **Program** screen, you need 3 things:

| Field | What to put |
|-------|-------------|
| **Program/script** | Find Python's path |
| **Arguments** | `scheduler.py` |
| **Start in** | The scheduler folder path |

**To find Python's path:**

Open PowerShell and type:

```powershell
where python
```

Copy the result (looks like `C:\Python314\python.exe`).
That goes in **Program/script**.

**To find the scheduler folder path:**

In PowerShell, type:

```powershell
pwd
```

Copy the result (looks like `C:\Users\marcj\Stoic1\project 1\...`).
That goes in **Start in**.

Click **Next** → **Finish**.

---

## Step 9: How to Use It Every Week

Your weekly routine once everything is set up:

### Sunday — Batch Day (1 hour)

1. **Run the batch generator**
   ```powershell
   cd stoiczodiac/05_AI_WORKFLOWS/scripts
   python run_weekly_batch.py
   ```

2. **Design in Canva**
   - Create your 7 quote images (export as PNG → `week_xxx/quotes/`)
   - Create 3 carousels (export as PNG pages → `week_xxx/carousels/<name>/`)
   - Create story images (export as PNG → `week_xxx/stories/`)

3. **Edit Reels in CapCut** → export as MP4 → `week_xxx/reels/`

4. **Import everything into the queue**
   ```powershell
   cd stoiczodiac/06_AUTOMATION/stoic_scheduler
   python scheduler.py --import-only
   ```

5. **Check it's all there**
   ```powershell
   python scheduler.py --status
   ```

That's it! The robot posts one item at each scheduled time
all week long. You don't need to do anything else.

### Every day — Check-in (30 seconds, optional)

```powershell
python scheduler.py --status
```

Shows what's queued and when it will post.

---

## Quick Reference — All Commands

| What you want | Type this |
|--------------|-----------|
| Check what's in the queue | `python scheduler.py --status` |
| See if it's time to post | `python scheduler.py --dry-run` |
| Import from batch folders | `python scheduler.py --import-only` |
| Post something right now | `python scheduler.py --post-now` |
| Check setup is correct | `python scheduler.py --validate-config` |

---

## Troubleshooting — Help!

| Problem | What to do |
|---------|------------|
| **"not recognized" error** | You're in the wrong folder. Run `cd stoiczodiac/06_AUTOMATION/stoic_scheduler` first. |
| **"No saved session"** on first run | Normal. The robot hasn't logged in yet. Run `--post-now` to do the first login. |
| **2FA code screen appears** | Check your Instagram authenticator app (or SMS) for the code, type it in the notepad window. |
| **"Config validation failed"** | Run `python scheduler.py --validate-config` to see what's wrong. |
| **Nothing happens / no posts** | Check if `queued/` has files. Check if it's a scheduled time. Run `--dry-run` to see. |
| **Carousel/reel/story won't post** | You haven't set up the Meta API yet. Read `META_SETUP_GUIDE.md` when you're ready. |
| **Token expired (60 days)** | Repeat the token steps in `META_SETUP_GUIDE.md`. Mark your calendar! |
| **Robot stopped working** | Check the logs: `notepad logs/scheduler_2026-10-01.log` |

---

## Want to Add Carousels, Reels and Stories?

The basic install above only posts **single images**.

To also post **carousels, reels, and stories**, you need:

1. Switch your Instagram to a **Creator account**
2. Connect it to a **Facebook Page**
3. Create a **Meta developer app**
4. Set up **Vercel Blob** (free storage)

All of this is explained step-by-step in **`META_SETUP_GUIDE.md`**
(in the same folder as this document). It takes about 30 minutes.

Without this setup, the robot will post your daily quote images
but skip any carousels, reels, and stories you put in the queue.