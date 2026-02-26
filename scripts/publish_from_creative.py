#!/usr/bin/env python3
from pathlib import Path
import re, argparse

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
args = p.parse_args()

src = Path(args.source).expanduser()
text = src.read_text(encoding='utf-8')
entries = [e.strip() for e in text.split('\n---\n') if '- Date:' in e]
# drop template/example blocks
entries = [e for e in entries if re.search(r'- Date:\s*20\d{2}-\d{2}-\d{2}', e)]
if not entries:
    raise SystemExit('No creative entries found')

root = Path(__file__).resolve().parents[1]
out_dir = root / 'content' / 'posts'
out_dir.mkdir(parents=True, exist_ok=True)

def grab(label, block):
    m = re.search(rf"- {re.escape(label)}:\s*(.*)", block)
    return m.group(1).strip() if m else ''

def clean_inline(text):
    # remove markdown markers and quote characters that break frontmatter parsing
    return text.replace('**', '').replace('"', '').strip()

written = []
for entry in entries:
    date = grab('Date', entry) or 'unknown-date'
    exploration = grab('Exploration', entry)
    made = clean_inline(grab('What I made', entry))
    if not made:
        continue
    surprised = grab('What surprised me', entry)
    notes = grab('Notes', entry)

    date_slug = re.sub(r'[^0-9-]+', '-', date).strip('-') or 'date'
    made_slug = re.sub(r'[^a-z0-9]+', '-', made.lower())[:60].strip('-') or 'artifact'
    slug = f"{date_slug}-{made_slug}".strip('-')

    out = out_dir / f'{slug}.md'
    out.write_text(f"""---
title: "{made or 'Creative Artifact'}"
date: "{date}"
---

## Exploration
{exploration}

## What I made
{made}

## What surprised me
{surprised}

## Notes
{notes}
""", encoding='utf-8')
    written.append(out)

print(f"wrote {len(written)} posts")
for w in written:
    print(w)
