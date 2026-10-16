# AI Workflows

Données sources et scripts de génération de contenu.

## Source de vérité

- `sign_master_data.json` — 12 signes, 5 philosophes, rotation 90 jours.
- `stoic_quote_library.json` — bibliothèque de citations.

## Scripts

- `run_weekly_batch.py` — routine hebdomadaire en une commande (calendrier + dossiers + brief + tracker).
- `generate_all_svgs.py` — génère les SVG quote/story (option `--png` convertit via Playwright).
- `batch_content_generator.py` — génère les calendriers (semaine par semaine).

## AI

`prompts/master_prompt_library.md` — 10 prompts ChatGPT prêts à copier-coller.