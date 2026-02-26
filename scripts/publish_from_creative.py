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

def extract_sections(block):
    labels = ['Date', 'Exploration', 'What I made', 'What surprised me', 'Notes']
    sections = {k: '' for k in labels}
    current = None
    for raw in block.splitlines():
        line = raw.rstrip('\n')
        m = re.match(r'^-\s+(Date|Exploration|What I made|What surprised me|Notes):\s*(.*)$', line)
        if m:
            current = m.group(1)
            sections[current] = m.group(2).strip()
            continue
        if current and (line.startswith('  ') or line.startswith('\t')):
            extra = line[2:] if line.startswith('  ') else line.lstrip('\t')
            sections[current] += ('\n' + extra)
    return sections

def clean_inline(text):
    # remove markdown markers and quote characters that break frontmatter parsing
    return text.replace('**', '').replace('"', '').strip()

def format_for_markdown(text):
    if not text:
        return ''
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if i > 0 and (line.lstrip().startswith('- ') or re.match(r'^\s*\d+\.\s', line)):
            if out and out[-1].strip() != '':
                out.append('')
        out.append(line)
    return '\n'.join(out)

written = []
for entry in entries:
    sec = extract_sections(entry)
    date = sec.get('Date', '').strip() or 'unknown-date'
    exploration = format_for_markdown(sec.get('Exploration', '').strip())
    made_raw = format_for_markdown(sec.get('What I made', '').strip())
    made_title = made_raw.splitlines()[0] if made_raw else ''
    made = clean_inline(made_title)
    if not made:
        continue
    surprised = format_for_markdown(sec.get('What surprised me', '').strip())
    notes = format_for_markdown(sec.get('Notes', '').strip())

    date_slug = re.sub(r'[^0-9-]+', '-', date).strip('-') or 'date'
    made_slug = re.sub(r'[^a-z0-9]+', '-', made.lower())[:60].strip('-') or 'artifact'
    slug = f"{date_slug}-{made_slug}".strip('-')

    out = out_dir / f'{slug}.md'
    artifact_block = made_raw.strip()
    out.write_text(f"""---
title: "{made or 'Creative Artifact'}"
date: "{date}"
---

## Exploration
{exploration}

## What I made
{made_raw}

## Actual Artifact (verbatim)
```text
{artifact_block}
```

## What surprised me
{surprised}

## Notes
{notes}
""", encoding='utf-8')
    written.append(out)

print(f"wrote {len(written)} posts")
for w in written:
    print(w)
