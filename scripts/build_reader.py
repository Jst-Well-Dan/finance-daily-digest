#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIEDU Daily Multi-Day Reader Generator
Style: 方案 B · 金融经纬 (Financial Gazette) - 浅色暖调纸刊风格
"""

import pathlib, re
try:
    import markdown
    HAS_MD = True
except:
    HAS_MD = False

root = pathlib.Path(__file__).resolve().parents[1]
daily_root = root / "daily"

def md_to_html(text):
    if HAS_MD:
        return markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])
    import html
    return "<pre>" + html.escape(text) + "</pre>"

def collect_day(d):
    notes = sorted(d.glob("*/*_结构化笔记.md"))
    summary = d / f"{d.name}_解读君视频总结.md"
    if not summary.exists():
        cands = list(d.glob("*_解读君视频总结.md"))
        summary = cands[0] if cands else None
    items = []
    for p in notes:
        txt = p.read_text(encoding="utf-8")
        h = md_to_html(txt)
        m = re.search(r"^#\s+结构化笔记｜(.+)$", txt, re.M)
        title = m.group(1).strip() if m else p.parent.name
        vid_m = re.search(r"\[([A-Za-z0-9_-]{6,})\]$", p.parent.name)
        vid = vid_m.group(1) if vid_m else ""
        if vid.startswith("UC") or "Decoding Finance" in p.parent.name:
            continue
        date_m = re.search(r"发布日期.*?(\d{4}-\d{2}-\d{2})", txt)
        date = date_m.group(1) if date_m else d.name
        items.append({"path": p, "title": title, "vid": vid, "date": date, "html": h})
    items.sort(key=lambda x: x["date"], reverse=True)
    summary_html = md_to_html(summary.read_text(encoding="utf-8")) if summary and summary.exists() else "<p>暂无总结</p>"
    summary_path = summary.relative_to(root).as_posix() if summary and summary.exists() else ""
    return {"dir": d, "notes": items, "summary_html": summary_html, "summary_path": summary_path, "count": len(items)}

# discover all YYYYMMDD dirs
days = [p for p in daily_root.iterdir() if p.is_dir() and re.fullmatch(r"\d{8}", p.name)]
days.sort(key=lambda p: p.name)
days_desc = sorted(days, key=lambda p: p.name, reverse=True)

# collect data
all_data = [collect_day(d) for d in days]
data_by_name = {d["dir"].name: d for d in all_data}
days_desc_data = [data_by_name[d.name] for d in days_desc]

CSS_GAZETTE = """
:root {
  --bg-page: #FBF8F2;
  --bg-surface: #FFFDF9;
  --bg-header: #F4EFE6;
  --bg-subtle: #F0EADF;
  --border-main: #E5DDCD;
  --border-dark: #2B2625;
  --text-main: #231F20;
  --text-muted: #5C554E;
  --text-light: #8E8478;
  --accent-burgundy: #8B261D;
  --accent-amber: #B45309;
  --font-serif: 'Noto Serif SC', Georgia, 'Times New Roman', serif;
  --font-sans: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 15px; }
body {
  background: var(--bg-page);
  color: var(--text-main);
  font-family: var(--font-sans);
  line-height: 1.85;
  -webkit-font-smoothing: antialiased;
}

.wrap {
  max-width: 1300px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 290px 1fr;
  min-height: 100vh;
  border-left: 2px solid var(--border-dark);
  border-right: 2px solid var(--border-dark);
  background: var(--bg-surface);
}

@media (max-width: 1024px) {
  .wrap { grid-template-columns: 1fr; border: none; }
}

/* Sidebar */
.nav {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 32px 24px;
  background: #F7F3EB;
  border-right: 1px solid var(--border-main);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (max-width: 1024px) {
  .nav { position: relative; height: auto; border-right: none; border-bottom: 2px solid var(--border-dark); }
}

.brand {
  padding-bottom: 18px;
  border-bottom: 2px solid var(--border-dark);
}
.brand h1 {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--border-dark);
}
.brand h1 span {
  display: block;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-burgundy);
  margin-top: 4px;
}

.toc h2 {
  font-family: var(--font-serif);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--border-dark);
  border-bottom: 1px solid var(--border-main);
  padding-bottom: 6px;
  margin: 16px 0 10px;
}

.toc a {
  display: flex;
  flex-direction: column;
  padding: 8px 10px;
  text-decoration: none;
  color: var(--text-main);
  border: 1px solid transparent;
  border-radius: 4px;
  transition: all 0.15s;
  font-size: 13px;
  line-height: 1.4;
  margin-bottom: 4px;
}
.toc a:hover {
  background: var(--bg-subtle);
  border-color: var(--border-main);
}
.toc a.active {
  background: #EFE8DA;
  border-color: var(--border-main);
  color: var(--accent-burgundy);
  font-weight: 600;
}
.toc a span {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-muted);
  margin-top: 2px;
}

.nav-desc {
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
  line-height: 1.6;
  padding: 4px 6px;
}

/* Main Area */
.main {
  padding: 40px 48px 80px;
  max-width: 960px;
}

@media (max-width: 768px) {
  .main { padding: 24px 18px 40px; }
}

.gazette-header {
  border-top: 3px double var(--border-dark);
  border-bottom: 1px solid var(--border-dark);
  padding: 20px 0;
  margin-bottom: 36px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 16px;
}
.gazette-header h1 {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--border-dark);
}
.gazette-header .gazette-meta {
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.summary-card, .article {
  background: var(--bg-surface);
  border: 1px solid var(--border-main);
  margin-bottom: 40px;
}

.summary-head, .article-head {
  background: var(--bg-header);
  padding: 20px 26px;
  border-bottom: 1px solid var(--border-main);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.article-head h3, .summary-head h3 {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
}
.article-head h3 a, .summary-head h3 a {
  color: inherit;
  text-decoration: none;
}
.article-head h3 a:hover, .summary-head h3 a:hover {
  color: var(--accent-burgundy);
}

.meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 8px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.meta a {
  color: var(--accent-burgundy);
  text-decoration: none;
  font-weight: 600;
}

.content {
  padding: 32px 36px;
  font-size: 14.5px;
  line-height: 1.9;
  color: #2D2726;
}

@media (max-width: 768px) {
  .content { padding: 20px 18px; }
  .summary-head, .article-head { padding: 16px 18px; }
}

.content h1 {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 18px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-dark);
}

.content h2 {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 700;
  color: var(--accent-burgundy);
  background: var(--bg-header);
  border: 1px solid var(--border-main);
  border-radius: 4px;
  padding: 8px 14px;
  margin: 32px 0 14px;
  letter-spacing: 0.02em;
}

.content h3 {
  font-family: var(--font-serif);
  font-size: 14.5px;
  font-weight: 700;
  margin: 22px 0 10px;
  color: var(--text-main);
}

.content p {
  margin-bottom: 16px;
  text-align: justify;
}

.content strong {
  font-weight: 700;
  color: #1A1616;
}

.content ul, .content ol {
  margin: 12px 0 18px 24px;
}
.content li {
  margin-bottom: 6px;
}

.content blockquote {
  background: #F3ECE0;
  border: 1px solid var(--border-main);
  border-radius: 4px;
  padding: 14px 20px;
  margin: 20px 0;
  font-size: 13.5px;
  font-style: italic;
  color: #523E3B;
}

.content table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 13px;
  border: 1px solid var(--border-main);
}
.content th {
  background: #ECE4D6;
  font-family: var(--font-serif);
  font-weight: 700;
  color: var(--border-dark);
  text-align: left;
  padding: 10px 14px;
  border: 1px solid var(--border-main);
}
.content td {
  padding: 9px 14px;
  border: 1px solid var(--border-main);
}
.content tr:nth-child(even) {
  background: #F8F4EC;
}

.content code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: #EDE6D8;
  padding: 2px 6px;
  border-radius: 3px;
  color: var(--accent-burgundy);
}

.day-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-main);
  padding: 20px 24px;
  margin-bottom: 18px;
}
.day-card h3 {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 6px;
}
.day-card h3 a {
  color: var(--text-main);
  text-decoration: none;
}
.day-card h3 a:hover {
  color: var(--accent-burgundy);
}
.day-card p {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.6;
}

.btn {
  display: inline-flex;
  padding: 8px 14px;
  border: 1px solid var(--border-dark);
  background: var(--bg-surface);
  font-family: var(--font-mono);
  font-size: 12px;
  text-decoration: none;
  color: var(--text-main);
  font-weight: 600;
  transition: all 0.15s;
}
.btn:hover {
  background: var(--bg-subtle);
}
.btn.primary {
  background: var(--border-dark);
  color: #FFFFFF;
}
.btn.primary:hover {
  background: var(--accent-burgundy);
  border-color: var(--accent-burgundy);
}
"""

def render_day_page(data):
    d = data["dir"]
    items = data["notes"]
    title_date = d.name
    nav_history = "".join([
        f'<a href="../{x["dir"].name}/index.html" class="{"active" if x["dir"].name==title_date else ""}">{x["dir"].name} <span>{x["count"]} 篇 · 当日归档</span></a>'
        for x in days_desc_data
    ])
    toc_items = "".join([
        f'<a href="#note-{it["vid"]}">{it["title"]}<span>{it["date"]} · {it["vid"]}</span></a>'
        for it in items
    ])
    summary_block = f"""
<section id="summary" class="summary-card">
  <div class="summary-head">
    <div>
      <h3>每日总结 · {title_date}</h3>
      <div class="meta">{data["summary_path"] or "暂无"}</div>
    </div>
  </div>
  <div class="content">{data["summary_html"]}</div>
</section>
"""
    articles = ""
    for it in items:
        yurl = f"https://www.youtube.com/watch?v={it['vid']}"
        articles += f"""
<article id="note-{it['vid']}" class="article">
  <div class="article-head">
    <div>
      <h3><a href="{yurl}" target="_blank" rel="noreferrer">{it['title']}</a></h3>
      <div class="meta">{it['date']} · {it['vid']} · <a href="{yurl}" target="_blank" rel="noreferrer">观看 YouTube 原片 ↗</a></div>
    </div>
  </div>
  <div class="content">{it['html']}</div>
</article>
"""
    html_out = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>解读君视频日报 · {title_date}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>{CSS_GAZETTE}</style>
</head>
<body>
  <div class="wrap">
    <nav class="nav">
      <div class="brand">
        <h1>解读君视频日报<span>JIEDU DAILY · {title_date}</span></h1>
      </div>
      <div class="toc">
        <h2>全量原文</h2>
        <a href="#summary" class="active">每日核心总结<span>{title_date}</span></a>
        {toc_items}
        <h2>历史归档</h2>
        <a href="../../index.html">← 返回历史总览</a>
        {nav_history}
      </div>
    </nav>
    <main class="main">
      <div class="gazette-header">
        <div>
          <h1>金融经纬 · 每日纪要</h1>
          <div class="gazette-meta">JIEDU DAILY FINANCIAL GAZETTE · VOL. {title_date}</div>
        </div>
        <div class="gazette-meta">{len(items)} ARTICLES ARCHIVED</div>
      </div>
      {summary_block}
      {articles}
      <div class="day-card">
        <p>归档路径 <code>daily/{title_date}/</code> · <a href="../../index.html">返回历史总览</a> · <a href="./index.html">本日目录</a></p>
      </div>
    </main>
  </div>
</body>
</html>
"""
    return html_out

# Render and save daily pages
for d_data in all_data:
    page_html = render_day_page(d_data)
    target = d_data["dir"] / "index.html"
    target.write_text(page_html, encoding="utf-8")
    print(f"Wrote {target}")

# Render Root index.html
latest = days_desc_data[0]
history_cards = ""
for d_item in days_desc_data:
    d = d_item["dir"]
    cnt = d_item["count"]
    titles = " / ".join([n["title"] for n in d_item["notes"]])
    history_cards += f"""
<div class="day-card">
  <h3><a href="daily/{d.name}/index.html">{d.name}</a> <span style="font:400 11px IBM Plex Mono; color:var(--text-muted); margin-left:8px">{cnt} 篇归档</span></h3>
  <p>{titles or "暂无笔记"}</p>
  <div style="margin-top:12px; display:flex; gap:10px;">
    <a class="btn primary" href="daily/{d.name}/index.html">进入当日全量阅读 →</a>
    <a class="btn" href="daily/{d.name}/{d.name}_解读君视频总结.md" target="_blank">总结 Markdown ↗</a>
  </div>
</div>
"""

latest_block = f"""
<div class="article">
  <div class="article-head">
    <div>
      <h3>最新发布 · {latest["dir"].name}</h3>
      <div class="meta">已累计归档 {len(days)} 天 · 最新收录 {latest["count"]} 篇</div>
    </div>
  </div>
  <div class="content">
    {latest["summary_html"][:1400]}
    <p style="margin-top:16px"><a class="btn primary" href="daily/{latest["dir"].name}/index.html">进入 {latest["dir"].name} 全量阅读 →</a></p>
  </div>
</div>
"""

root_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>解读君视频日报 · 历史总览</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>{CSS_GAZETTE}</style>
</head>
<body>
  <div class="wrap">
    <nav class="nav">
      <div class="brand">
        <h1>解读君视频日报<span>JIEDU DAILY · 历史总览</span></h1>
      </div>
      <div class="toc">
        <h2>历史归档目录</h2>
        {"".join([f'<a href="daily/{x["dir"].name}/index.html">{x["dir"].name}<span>{x["count"]} 篇 · 点击查看当日全量 HTML</span></a>' for x in days_desc_data])}
        <h2>归档说明</h2>
        <p class="nav-desc">每日生成独立 <code>daily/YYYYMMDD/index.html</code> 永不覆盖；根 <code>index.html</code> 为历史总览，始终指向最新。</p>
      </div>
    </nav>
    <main class="main">
      <div class="gazette-header">
        <div>
          <h1>金融经纬 · 历史总览</h1>
          <div class="gazette-meta">JIEDU DAILY ARCHIVE · {len(days)} DAYS TOTAL</div>
        </div>
        <div class="gazette-meta">LAST UPDATED: {latest["dir"].name}</div>
      </div>
      {latest_block}
      <div style="margin-top:24px">
        <h2 style="font-family:var(--font-serif); font-size:18px; font-weight:700; margin-bottom:14px; border-bottom:2px solid var(--border-dark); padding-bottom:6px">全部历史归档</h2>
        {history_cards}
      </div>
    </main>
  </div>
</body>
</html>
"""

root_index_target = root / "index.html"
root_index_target.write_text(root_html, encoding="utf-8")
print(f"Wrote root index.html with {len(days)} days")
