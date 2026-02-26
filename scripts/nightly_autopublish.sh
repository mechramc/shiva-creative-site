#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/Users/murai-labs/github/shiva-creative-site"
SOURCE_CREATIVE="/Users/murai-labs/.openclaw/workspace-shiva/CREATIVE.md"

cd "$REPO_DIR"

# Ensure local venv exists
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q markdown

# Publish latest creative entry + rebuild site
python scripts/publish_from_creative.py --source "$SOURCE_CREATIVE"
python scripts/build.py

# Commit and push only if changed
if ! git diff --quiet || ! git diff --cached --quiet; then
  git add content/posts site
  if ! git diff --cached --quiet; then
    git commit -m "chore: nightly creative auto-publish"
    git push origin main
    echo "published"
  else
    echo "no staged changes"
  fi
else
  echo "no changes"
fi
