#!/usr/bin/env python3
from pathlib import Path
import markdown, re

root = Path(__file__).resolve().parents[1]
posts_dir = root/'content'/'posts'
site_dir = root/'site'
site_dir.mkdir(exist_ok=True)

posts=[]
for f in sorted(posts_dir.glob('*.md'), reverse=True):
    txt=f.read_text(encoding='utf-8')
    body=txt.split('---\n',2)[-1] if txt.startswith('---') else txt
    title_match=re.search(r'title:\s*"([^"]+)"',txt)
    date_match=re.search(r'date:\s*"([^"]+)"',txt)
    title=title_match.group(1) if title_match else f.stem
    date=date_match.group(1) if date_match else ''
    html=markdown.markdown(body, extensions=['fenced_code', 'tables', 'nl2br'])
    out=site_dir/(f.stem+'.html')
    out.write_text(f"<html><body style='max-width:760px;margin:40px auto;font-family:Inter,Arial;background:#0b1020;color:#e8ecff'><h1>{title}</h1><p>{date}</p>{html}<p><a href='index.html'>← back</a></p></body></html>",encoding='utf-8')
    posts.append((title,date,out.name))

index=''.join([f"<li><a href='{fn}'>{t}</a> <small>{d}</small></li>" for t,d,fn in posts])
(site_dir/'index.html').write_text(f"<html><body style='max-width:760px;margin:40px auto;font-family:Inter,Arial;background:#0b1020;color:#e8ecff'><h1>Shiva — Creative Endeavours</h1><p>Nightly artifacts.</p><ul>{index}</ul></body></html>",encoding='utf-8')
print('built',len(posts),'posts')
