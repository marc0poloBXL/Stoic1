# Automation

Scheduler et automatisations de posting.

## Stoic Scheduler

- `stoic_scheduler/` — auto-poster Instagram (Playwright + Meta API). Queue par dossiers, captions requises.
- Import depuis les batchs : `python stoic_scheduler/queue_handler.py` (via CLI) — scanne `11_MEDIA_LIBRARY/SCHEDULED/week_*/`.

## Autres

- `openreply/` — DM automation (Next.js).
- `instagram_dm.py`, `create_campaigns.mjs`, `get_fb_token.html` — helpers OpenReply.

## Config

`stoic_scheduler/config.yaml` — horaires de post, dossiers queue, paramètres Meta API.