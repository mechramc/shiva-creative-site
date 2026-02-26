#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import re, argparse

p = argparse.ArgumentParser()
p.add_argument('--source', required=True)
args = p.parse_args()

src = Path(args.source).expanduser()
text = src.read_text(encoding='utf-8')
entries = [e.strip() for e in text.split('\n---\n') if 'Date:' in e]
if not entries:
    raise SystemExit('No creative entries found')
last = entries[-1]

def grab(label):
    m = re.search(rf"- {label}:\s*(.*)", last)
    return m.group(1).strip() if m else ''

date = grab('Date') or datetime.now().strftime('%Y-%m-%d')
exploration = grab('Exploration')
made = grab('What I made')
surprised = grab('What surprised me')
notes = grab('Notes')
slug = re.sub(r'[^a-z0-9]+','-', f"{date}-{made.lower()[:40]}").strip('-')
out = Path(__file__).resolve().parents[1] / 'content' / 'posts' / f'{slug}.md'
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
print(out)
