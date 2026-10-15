# 📁 Media Library

Central repository for all visual and audiovisual assets used across the Stoic Zodiac content pipeline.

## Structure

```
11_MEDIA_LIBRARY/
├── IMAGES/           # Static visual assets
│   ├── zodiac/       # Zodiac sign imagery (one folder per sign)
│   ├── backgrounds/  # Backgrounds, textures, gradients
│   ├── stock/        # Licensed stock photography
│   └── quotes/       # Quote card graphics and styled quote images
├── VIDEO/            # Motion content
│   ├── reels/        # Final reel exports (IG, TikTok, YT Shorts)
│   ├── b_roll/       # B-roll footage clips
│   ├── animations/   # Motion graphics, Lottie files, GIFs, AE renders
│   └── intros_outros/ # Channel intro/outro videos
├── GRAPHICS/         # Design elements
│   ├── overlays/     # Text overlays, stickers, frames, watermarks
│   ├── icons/        # Icon sets (zodiac symbols, social media, UI)
│   ├── thumbnails/   # Video/reel thumbnail images
│   └── templates/    # Reusable source files (PSD, AI, Canva links)
├── SCREENSHOTS/      # Reference images
│   ├── app_ui/       # App/dashboard interface screenshots
│   └── analytics/    # Analytics dashboard screenshots
└── SCHEDULED/        # Content in pre/post-production pipeline
    ├── draft/        # Work-in-progress assets
    ├── review/       # Assets pending approval
    ├── approved/     # Final assets ready for posting
    └── week_YYYYMMDD/   # One per week
        ├── quotes/       # Quote PNGs + captions
        ├── quotes_svg/   # SVG quote card sources
        ├── quotes_png/   # PNG quote cards (1080x1080, rendered)
        ├── stories/      # Story PNGs + prompts
        ├── stories_svg/  # SVG story card sources
        ├── stories_png/  # PNG stories (1080x1920, rendered)
        ├── carousels/    # Carousel slides by type (subfolders)
        └── reels/        # Reel videos (MP4)
```

## Related Folders

| Folder | What it holds |
|--------|---------------|
| `01_BRAND_ASSETS/` | Logos, fonts, colors, brand graphics |
| `07_AUDIO/` | Music, sound effects, voiceovers |
| `04_TEMPLATES/` | Canva app templates and reusable design files |