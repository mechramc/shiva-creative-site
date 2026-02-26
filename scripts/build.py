#!/usr/bin/env python3
from pathlib import Path
import markdown, re, html

root = Path(__file__).resolve().parents[1]
posts_dir = root / 'content' / 'posts'
site_dir = root / 'site'
site_dir.mkdir(exist_ok=True)

STYLE = """
:root {
  --bg: #040812;
  --panel: rgba(12, 20, 42, 0.68);
  --panel-border: rgba(143, 186, 255, 0.28);
  --text: #e7eeff;
  --muted: #9db0d9;
  --accent: #9be7ff;
  --accent-2: #b89dff;
  --code-bg: #0c1430;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: Inter, ui-sans-serif, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color: var(--text);
  min-height: 100vh;
  background: var(--bg);
  overflow-x: hidden;
}

.bg {
  position: fixed;
  inset: 0;
  z-index: -2;
  background:
    radial-gradient(1200px 700px at 10% -10%, rgba(46, 90, 200, 0.45) 0%, transparent 65%),
    radial-gradient(900px 500px at 88% 0%, rgba(114, 56, 211, 0.40) 0%, transparent 60%),
    radial-gradient(1200px 900px at 50% 130%, rgba(18, 30, 72, 0.80) 0%, transparent 70%),
    #040812;
}
.bg::before, .bg::after {
  content: "";
  position: absolute;
  inset: -10%;
  background-repeat: repeat;
  opacity: .45;
  pointer-events: none;
}
.bg::before {
  background-image:
    radial-gradient(2px 2px at 20px 30px, rgba(255,255,255,.9), transparent 60%),
    radial-gradient(1px 1px at 120px 80px, rgba(255,255,255,.85), transparent 60%),
    radial-gradient(1.5px 1.5px at 300px 200px, rgba(173,205,255,.8), transparent 65%),
    radial-gradient(2px 2px at 540px 420px, rgba(187,167,255,.75), transparent 65%);
  background-size: 640px 640px;
  animation: driftA 90s linear infinite;
}
.bg::after {
  background-image:
    radial-gradient(1.5px 1.5px at 40px 100px, rgba(255,255,255,.85), transparent 65%),
    radial-gradient(1px 1px at 260px 60px, rgba(202,228,255,.8), transparent 60%),
    radial-gradient(2px 2px at 500px 300px, rgba(255,255,255,.7), transparent 70%);
  background-size: 780px 780px;
  animation: driftB 140s linear infinite reverse;
}
@keyframes driftA { from { transform: translate3d(0,0,0);} to { transform: translate3d(-120px, 90px,0);} }
@keyframes driftB { from { transform: translate3d(0,0,0);} to { transform: translate3d(110px,-70px,0);} }

.wrap {
  width: min(1080px, 94vw);
  margin: 34px auto 64px;
}
.header {
  padding: 28px 30px;
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  background: var(--panel);
  backdrop-filter: blur(10px);
  box-shadow: 0 12px 42px rgba(0, 0, 0, 0.45);
}
.brand {
  margin: 0;
  font-size: clamp(30px, 4.1vw, 48px);
  line-height: 1.08;
  letter-spacing: 0.2px;
  font-weight: 800;
}
.sub {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: clamp(16px, 1.35vw, 20px);
}
.list {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}
.card {
  display: block;
  text-decoration: none;
  color: inherit;
  border: 1px solid rgba(143, 186, 255, 0.25);
  background: linear-gradient(160deg, rgba(20,31,67,.72), rgba(16,24,48,.64));
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 6px 28px rgba(0,0,0,.32);
  transition: transform .14s ease, border-color .14s ease, box-shadow .14s ease;
}
.card:hover {
  transform: translateY(-2px);
  border-color: rgba(155, 231, 255, .66);
  box-shadow: 0 10px 36px rgba(62, 123, 255, 0.22);
}
.card-title {
  margin: 0;
  font-size: clamp(21px, 2vw, 27px);
  line-height: 1.28;
  font-weight: 700;
}
.card-date {
  margin-top: 9px;
  color: var(--muted);
  font-size: clamp(14px, 1.2vw, 16px);
}

.post-shell {
  margin-top: 18px;
  border: 1px solid var(--panel-border);
  border-radius: 18px;
  background: var(--panel);
  backdrop-filter: blur(10px);
  padding: 30px 34px;
  box-shadow: 0 12px 42px rgba(0,0,0,.45);
}
.post-title {
  margin: 0;
  font-size: clamp(34px, 4.8vw, 58px);
  line-height: 1.08;
  font-weight: 800;
}
.post-date {
  margin: 12px 0 22px;
  color: var(--muted);
  font-size: clamp(15px, 1.2vw, 18px);
}
.post-content h2, .post-content h3 {
  margin: 30px 0 12px;
  line-height: 1.18;
}
.post-content h2 { font-size: clamp(24px, 2.5vw, 34px); }
.post-content h3 { font-size: clamp(20px, 2vw, 28px); }
.post-content p, .post-content li {
  line-height: 1.82;
  color: #e3ebff;
  font-size: clamp(18px, 1.35vw, 22px);
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
  border: 1px solid rgba(143, 186, 255, 0.35);
  border-radius: 12px;
  padding: 14px;
  overflow: auto;
}
.post-content pre code {
  background: transparent;
  padding: 0;
  color: #d6e4ff;
}
.back {
  display: inline-block;
  margin-top: 22px;
  color: var(--accent);
  text-decoration: none;
  font-size: clamp(16px, 1.2vw, 19px);
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


def shell_start(title):
    return f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width, initial-scale=1'/>
  <title>{title}</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class='bg'></div>
  <main class='wrap'>
"""


def shell_end():
    return """  </main>\n</body>\n</html>\n"""


posts = []
for f in sorted(posts_dir.glob('*.md'), reverse=True):
    txt = f.read_text(encoding='utf-8')
    title, date, body = parse_frontmatter(txt)
    if not title:
        title = f.stem

    body_html = markdown.markdown(body, extensions=['fenced_code', 'tables', 'nl2br'])
    out = site_dir / f'{f.stem}.html'

    post_page = (
        shell_start(f"{html.escape(title)} · Shiva Creative")
        + f"""
    <section class='post-shell'>
      <h1 class='post-title'>{html.escape(title)}</h1>
      <p class='post-date'>{html.escape(date)}</p>
      <article class='post-content'>{body_html}</article>
      <a class='back' href='index.html'>← Back to all entries</a>
    </section>
"""
        + shell_end()
    )
    out.write_text(post_page, encoding='utf-8')
    posts.append((title, date, out.name))

cards = '\n'.join(
    f"""<a class='card' href='{html.escape(fn)}'>
  <p class='card-title'>{html.escape(t)}</p>
  <p class='card-date'>{html.escape(d)}</p>
</a>"""
    for t, d, fn in posts
)

index_page = (
    shell_start('Shiva — Creative Endeavours')
    + f"""
    <header class='header'>
      <h1 class='brand'>Shiva — Creative Endeavours</h1>
      <p class='sub'>Nightly artifacts from autonomous creative sprints.</p>
    </header>
    <section class='list'>
      {cards}
    </section>
"""
    + shell_end()
)
(site_dir / 'index.html').write_text(index_page, encoding='utf-8')
print('built', len(posts), 'posts')
