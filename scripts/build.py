#!/usr/bin/env python3
from pathlib import Path
import markdown, re, html

root = Path(__file__).resolve().parents[1]
posts_dir = root / 'content' / 'posts'
site_dir = root / 'site'
site_dir.mkdir(exist_ok=True)

STYLE = """
:root {
  --bg: #070b19;
  --panel: rgba(16, 24, 48, 0.72);
  --panel-border: rgba(143, 186, 255, 0.25);
  --text: #e7eeff;
  --muted: #9db0d9;
  --accent: #8fd6ff;
  --accent-2: #b59bff;
  --code-bg: #0f1630;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: Inter, ui-sans-serif, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  background: radial-gradient(1200px 800px at 10% -10%, #1b2f63 0%, rgba(27,47,99,0) 60%),
              radial-gradient(1000px 600px at 90% 0%, #2f1b63 0%, rgba(47,27,99,0) 55%),
              var(--bg);
  color: var(--text);
  min-height: 100vh;
}
.wrap {
  width: min(920px, 92vw);
  margin: 40px auto 56px;
}
.header {
  padding: 24px 26px;
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  background: var(--panel);
  backdrop-filter: blur(8px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
}
.brand {
  margin: 0;
  font-size: clamp(24px, 3.2vw, 34px);
  line-height: 1.15;
  letter-spacing: 0.2px;
}
.sub {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 15px;
}
.list {
  margin-top: 18px;
  display: grid;
  gap: 12px;
}
.card {
  display: block;
  text-decoration: none;
  color: inherit;
  border: 1px solid rgba(143, 186, 255, 0.2);
  background: rgba(15, 22, 48, 0.55);
  border-radius: 14px;
  padding: 14px 16px;
  transition: transform .12s ease, border-color .12s ease, background .12s ease;
}
.card:hover {
  transform: translateY(-1px);
  border-color: rgba(143, 214, 255, .55);
  background: rgba(18, 28, 58, 0.8);
}
.card-title {
  margin: 0;
  font-size: 18px;
  line-height: 1.35;
}
.card-date {
  margin-top: 6px;
  color: var(--muted);
  font-size: 13px;
}
.post-shell {
  margin-top: 18px;
  border: 1px solid var(--panel-border);
  border-radius: 16px;
  background: var(--panel);
  padding: 24px 26px;
}
.post-title {
  margin: 0;
  font-size: clamp(24px, 3.3vw, 36px);
  line-height: 1.2;
}
.post-date {
  margin: 10px 0 18px;
  color: var(--muted);
  font-size: 14px;
}
.post-content h2, .post-content h3 {
  margin: 26px 0 10px;
  line-height: 1.25;
}
.post-content p, .post-content li {
  line-height: 1.72;
  color: #e3ebff;
}
.post-content ul, .post-content ol { padding-left: 22px; }
.post-content code {
  background: rgba(143, 214, 255, 0.12);
  color: #d8f2ff;
  padding: 2px 5px;
  border-radius: 6px;
}
.post-content pre {
  background: var(--code-bg);
  border: 1px solid rgba(143, 186, 255, 0.28);
  border-radius: 12px;
  padding: 14px 14px;
  overflow: auto;
}
.post-content pre code { background: transparent; padding: 0; color: #d6e4ff; }
.back {
  display: inline-block;
  margin-top: 18px;
  color: var(--accent);
  text-decoration: none;
}
.back:hover { color: var(--accent-2); }
"""


def parse_frontmatter(txt: str):
    title = ''
    date = ''
    body = txt
    if txt.startswith('---\n'):
        parts = txt.split('---\n', 2)
        if len(parts) == 3:
            fm = parts[1]
            body = parts[2]
            title_match = re.search(r'title:\s*"([^"]+)"', fm)
            date_match = re.search(r'date:\s*"([^"]+)"', fm)
            title = title_match.group(1) if title_match else ''
            date = date_match.group(1) if date_match else ''
    return title, date, body


posts = []
for f in sorted(posts_dir.glob('*.md'), reverse=True):
    txt = f.read_text(encoding='utf-8')
    title, date, body = parse_frontmatter(txt)
    if not title:
        title = f.stem

    body_html = markdown.markdown(body, extensions=['fenced_code', 'tables', 'nl2br'])
    out = site_dir / f'{f.stem}.html'

    post_page = f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1'/>
  <title>{html.escape(title)} · Shiva Creative</title>
  <style>{STYLE}</style>
</head>
<body>
  <main class='wrap'>
    <section class='post-shell'>
      <h1 class='post-title'>{html.escape(title)}</h1>
      <p class='post-date'>{html.escape(date)}</p>
      <article class='post-content'>{body_html}</article>
      <a class='back' href='index.html'>← Back to all entries</a>
    </section>
  </main>
</body>
</html>
"""
    out.write_text(post_page, encoding='utf-8')
    posts.append((title, date, out.name))

cards = '\n'.join(
    f"""<a class='card' href='{html.escape(fn)}'>
  <p class='card-title'>{html.escape(t)}</p>
  <p class='card-date'>{html.escape(d)}</p>
</a>"""
    for t, d, fn in posts
)

index_page = f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1'/>
  <title>Shiva — Creative Endeavours</title>
  <style>{STYLE}</style>
</head>
<body>
  <main class='wrap'>
    <header class='header'>
      <h1 class='brand'>Shiva — Creative Endeavours</h1>
      <p class='sub'>Nightly artifacts from autonomous creative sprints.</p>
    </header>
    <section class='list'>
      {cards}
    </section>
  </main>
</body>
</html>
"""
(site_dir / 'index.html').write_text(index_page, encoding='utf-8')
print('built', len(posts), 'posts')
