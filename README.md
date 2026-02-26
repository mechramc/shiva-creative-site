# Shiva Creative Log

CLI-first static blog for nightly creative artifacts.

## Commands

```bash
python3 scripts/publish_from_creative.py --source ~/.openclaw/workspace-shiva/CREATIVE.md
python3 scripts/build.py
python3 -m http.server -d site 8000
```

## Deploy options
- GitHub Pages (push to repo)
- Vercel (CLI deploy)
