# Content Calendar

Calendriers hebdomadaires générés (semaine 1 = 17 août 2026).

## Fichiers

- `week1_template.md` — référence de la semaine de lancement.
- `generated/weekN_YYYYMMDD.{csv,md}` — calendriers générés par semaine (convention actuelle).

## Génération

```bash
python 05_AI_WORKFLOWS/scripts/batch_content_generator.py --week N --days 7
```

Les anciens fichiers `content_calendar_YYYYMMDD` (format obsolète) sont archivés dans `_ARCHIVE/03_CONTENT_CALENDAR_generated/`.