#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate 4 distinct light-theme prototypes for JIEDU Daily Reader:
1. 🏛️ Institutional Dossier (研报档案 · 纯净投行白)
2. 📰 Financial Gazette (金融经纬 · 暖调纸刊)
3. ⚡ Modern Studio (极简工坊 · 现代科技白)
4. 🌿 Kyoto Serif (典雅文澜 · 护眼茶白)

Plus an interactive selector / comparison hub: prototypes/index.html
"""

import pathlib, re, html, json
import markdown

root = pathlib.Path(__file__).resolve().parents[1]
daily_dir = root / "daily" / "20260903"
out_dir = root / "prototypes"
out_dir.mkdir(parents=True, exist_ok=True)

# Parse Markdown
def render_md(text):
    return markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])

# Collect Day Data
summary_file = daily_dir / "20260903_解读君视频总结.md"
summary_text = summary_file.read_text(encoding="utf-8") if summary_file.exists() else ""
summary_html = render_md(summary_text)

note_files = sorted(daily_dir.glob("*/*_结构化笔记.md"))
items = []
for p in note_files:
    txt = p.read_text(encoding="utf-8")
    h = render_md(txt)
    m = re.search(r"^#\s+结构化笔记｜(.+)$", txt, re.M)
    title = m.group(1).strip() if m else p.parent.name
    vid_m = re.search(r"\[([A-Za-z0-9_-]{6,})\]$", p.parent.name)
    vid = vid_m.group(1) if vid_m else ""
    if vid.startswith("UC") or "Decoding Finance" in p.parent.name:
        continue
    date_m = re.search(r"发布日期.*?(\d{4}-\d{2}-\d{2})", txt)
    date = date_m.group(1) if date_m else "2026-09-03"
    items.append({"title": title, "vid": vid, "date": date, "html": h, "path": p})

items.sort(key=lambda x: x["date"], reverse=True)

def make_articles_html(items):
    out = ""
    for it in items:
        yurl = f"https://www.youtube.com/watch?v={it['vid']}"
        out += f"""
<article id="note-{it['vid']}" class="article-card">
  <header class="article-header">
    <div class="article-title-wrap">
      <h2 class="article-title"><a href="{yurl}" target="_blank" rel="noreferrer">{it['title']}</a></h2>
      <div class="article-meta">
        <span class="meta-date">{it['date']}</span>
        <span class="meta-sep">/</span>
        <span class="meta-vid">ID: {it['vid']}</span>
        <span class="meta-sep">/</span>
        <a class="meta-link" href="{yurl}" target="_blank" rel="noreferrer">观看 YouTube 原片 ↗</a>
      </div>
    </div>
  </header>
  <div class="article-body markdown-content">
    {it['html']}
  </div>
</article>
"""
    return out

articles_html = make_articles_html(items)

def make_toc_html(items):
    out = '<a href="#summary" class="toc-item active"><span class="toc-num">00</span><span class="toc-text">今日核心总结</span></a>\n'
    for idx, it in enumerate(items, 1):
        out += f'<a href="#note-{it["vid"]}" class="toc-item"><span class="toc-num">{idx:02d}</span><span class="toc-text">{it["title"]}<small>{it["date"]} · {it["vid"]}</small></span></a>\n'
    return out

toc_html = make_toc_html(items)

# =========================================================================
# PROTOTYPE 1: 🏛️ Institutional Dossier (研报档案 · 纯净投行白)
# =========================================================================
CSS_DOSSIER = """
:root {
  --bg-page: #F8FAFC;
  --bg-surface: #FFFFFF;
  --bg-subtle: #F1F5F9;
  --border-main: #E2E8F0;
  --border-strong: #CBD5E1;
  --text-main: #0F172A;
  --text-muted: #64748B;
  --text-light: #94A3B8;
  --accent-primary: #1D4ED8;
  --accent-surface: #EFF6FF;
  --accent-border: #BFDBFE;
  --accent-warm: #B45309;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
  --font-serif: 'Noto Serif SC', 'Source Serif Pro', Georgia, serif;
  --font-mono: 'IBM Plex Mono', 'SFMono-Regular', monospace;
  --shadow-card: 0 1px 3px 0 rgba(15, 23, 42, 0.05);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 15px; }
body {
  background: var(--bg-page);
  color: var(--text-main);
  font-family: var(--font-sans);
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}

.app-container {
  max-width: 1320px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
  border-left: 1px solid var(--border-main);
  border-right: 1px solid var(--border-main);
  background: var(--bg-surface);
}

@media (max-width: 1024px) {
  .app-container { grid-template-columns: 1fr; border: none; }
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 28px 20px;
  background: #FAFCFE;
  border-right: 1px solid var(--border-main);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (max-width: 1024px) {
  .sidebar { position: relative; height: auto; border-right: none; border-bottom: 1px solid var(--border-main); }
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-main);
}
.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 6px;
  background: var(--accent-primary);
  color: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 0.05em;
}
.brand-text h1 {
  font-size: 15px;
  font-weight: 700;
  font-family: var(--font-serif);
  color: var(--text-main);
}
.brand-text span {
  display: block;
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--text-light);
  margin-bottom: 10px;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toc-item {
  display: flex;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  text-decoration: none;
  color: var(--text-main);
  border: 1px solid transparent;
  transition: all 0.15s ease;
}
.toc-item:hover {
  background: var(--bg-subtle);
  border-color: var(--border-main);
}
.toc-item.active {
  background: var(--accent-surface);
  border-color: var(--accent-border);
  color: var(--accent-primary);
}
.toc-num {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--text-light);
  margin-top: 2px;
}
.toc-item.active .toc-num {
  color: var(--accent-primary);
}
.toc-text {
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
}
.toc-text small {
  display: block;
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
  margin-top: 2px;
  font-weight: 400;
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid var(--border-main);
  font-size: 11px;
  color: var(--text-light);
  font-family: var(--font-mono);
  line-height: 1.5;
}

.main-content {
  padding: 36px 44px 80px;
  max-width: 960px;
}

@media (max-width: 768px) {
  .main-content { padding: 20px 16px 40px; }
}

.dossier-hero {
  background: var(--bg-surface);
  border: 1px solid var(--border-main);
  border-top: 3px solid var(--accent-primary);
  border-radius: 8px;
  padding: 24px 28px;
  margin-bottom: 32px;
  box-shadow: var(--shadow-card);
}
.hero-header-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-main);
  margin-bottom: 16px;
}
.hero-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent-primary);
}
.hero-date-box {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
}
.dossier-hero h1 {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
  margin-bottom: 8px;
}
.dossier-hero p {
  color: var(--text-muted);
  font-size: 13.5px;
  line-height: 1.6;
}

.summary-card, .article-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-main);
  border-radius: 8px;
  margin-bottom: 36px;
  box-shadow: var(--shadow-card);
  overflow: hidden;
}

.summary-header, .article-header {
  background: #F8FAFC;
  padding: 18px 24px;
  border-bottom: 1px solid var(--border-main);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.article-title {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  line-height: 1.4;
  color: var(--text-main);
}
.article-title a {
  color: inherit;
  text-decoration: none;
}
.article-title a:hover {
  color: var(--accent-primary);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 6px;
}
.meta-sep { color: var(--border-strong); }
.meta-link { color: var(--accent-primary); text-decoration: none; font-weight: 500; }
.meta-link:hover { text-decoration: underline; }

.article-body {
  padding: 28px 32px 36px;
}

@media (max-width: 768px) {
  .article-body { padding: 18px 16px; }
  .summary-header, .article-header { padding: 14px 16px; }
}

.markdown-content {
  font-size: 14px;
  line-height: 1.85;
  color: #1E293B;
}

.markdown-content h1 {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-main);
  color: var(--text-main);
}

.markdown-content h2 {
  font-family: var(--font-sans);
  font-size: 14px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--accent-primary);
  background: var(--accent-surface);
  border: 1px solid var(--accent-border);
  padding: 8px 14px;
  margin: 28px 0 14px;
  border-radius: 6px;
}

.markdown-content h3 {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-main);
  margin: 20px 0 8px;
}

.markdown-content p {
  margin-bottom: 14px;
}

.markdown-content strong {
  color: #0F172A;
  font-weight: 600;
}

.markdown-content ul, .markdown-content ol {
  margin: 10px 0 16px 20px;
}
.markdown-content li {
  margin-bottom: 6px;
}

.markdown-content blockquote {
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  padding: 12px 18px;
  margin: 18px 0;
  border-radius: 6px;
  font-size: 13.5px;
  color: #92400E;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 13px;
  border: 1px solid var(--border-main);
}
.markdown-content th {
  background: #F8FAFC;
  font-weight: 600;
  color: var(--text-main);
  text-align: left;
  padding: 10px 14px;
  border: 1px solid var(--border-main);
}
.markdown-content td {
  padding: 9px 14px;
  border: 1px solid var(--border-main);
  color: #334155;
}
.markdown-content tr:nth-child(even) {
  background: #F8FAFC;
}

.markdown-content code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--bg-subtle);
  border: 1px solid var(--border-main);
  padding: 2px 5px;
  border-radius: 4px;
  color: var(--accent-warm);
}

.prototype-bar {
  background: #FFFFFF;
  border-bottom: 1px solid var(--border-main);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}
.prototype-links {
  display: flex;
  gap: 12px;
}
.prototype-links a {
  color: var(--text-muted);
  text-decoration: none;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: var(--font-mono);
}
.prototype-links a:hover, .prototype-links a.active {
  background: var(--accent-surface);
  color: var(--accent-primary);
  font-weight: 600;
}
"""

# =========================================================================
# PROTOTYPE 2: 📰 Financial Gazette (金融经纬 · 暖调纸刊)
# =========================================================================
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
  --font-sans: 'Noto Sans SC', -apple-system, sans-serif;
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

.app-container {
  max-width: 1280px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 290px 1fr;
  min-height: 100vh;
  border-left: 2px solid var(--border-dark);
  border-right: 2px solid var(--border-dark);
  background: var(--bg-surface);
}

@media (max-width: 1024px) {
  .app-container { grid-template-columns: 1fr; border: none; }
}

.sidebar {
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
  .sidebar { position: relative; height: auto; border-right: none; border-bottom: 2px solid var(--border-dark); }
}

.brand-block {
  padding-bottom: 18px;
  border-bottom: 2px solid var(--border-dark);
}
.brand-text h1 {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--border-dark);
}
.brand-text span {
  display: block;
  font-family: var(--font-mono);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--accent-burgundy);
  margin-top: 4px;
}

.nav-section-title {
  font-family: var(--font-serif);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--border-dark);
  border-bottom: 1px solid var(--border-main);
  padding-bottom: 6px;
  margin-bottom: 12px;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toc-item {
  display: flex;
  gap: 12px;
  padding: 10px 12px;
  text-decoration: none;
  color: var(--text-main);
  border: 1px solid transparent;
  border-radius: 4px;
  background: transparent;
  transition: all 0.15s;
}
.toc-item:hover {
  background: var(--bg-subtle);
  border-color: var(--border-main);
}
.toc-item.active {
  background: #EFE8DA;
  border-color: var(--border-main);
  color: var(--accent-burgundy);
}
.toc-num {
  font-family: var(--font-serif);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-light);
}
.toc-item.active .toc-num {
  color: var(--accent-burgundy);
}
.toc-text {
  font-family: var(--font-serif);
  font-size: 13.5px;
  font-weight: 600;
  line-height: 1.4;
}
.toc-text small {
  display: block;
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-muted);
  font-weight: 400;
  margin-top: 3px;
}

.main-content {
  padding: 40px 48px 80px;
  max-width: 940px;
}

@media (max-width: 768px) {
  .main-content { padding: 24px 18px 40px; }
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

.summary-card, .article-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-main);
  margin-bottom: 40px;
}

.summary-header, .article-header {
  background: var(--bg-header);
  padding: 20px 26px;
  border-bottom: 1px solid var(--border-main);
}
.article-title {
  font-family: var(--font-serif);
  font-size: 20px;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.35;
}
.article-title a {
  color: inherit;
  text-decoration: none;
}
.article-title a:hover {
  color: var(--accent-burgundy);
}

.article-meta {
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
.meta-sep { color: var(--border-main); }
.meta-link { color: var(--accent-burgundy); text-decoration: none; font-weight: 600; }

.article-body {
  padding: 32px 36px;
}

@media (max-width: 768px) {
  .article-body { padding: 20px 18px; }
  .summary-header, .article-header { padding: 16px 18px; }
}

.markdown-content {
  font-size: 14.5px;
  line-height: 1.9;
  color: #2D2726;
}

.markdown-content h1 {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 18px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-dark);
}

.markdown-content h2 {
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

.markdown-content h3 {
  font-family: var(--font-serif);
  font-size: 14.5px;
  font-weight: 700;
  margin: 22px 0 10px;
  color: var(--text-main);
}

.markdown-content p {
  margin-bottom: 16px;
  text-align: justify;
}

.markdown-content strong {
  font-weight: 700;
  color: #1A1616;
}

.markdown-content ul, .markdown-content ol {
  margin: 12px 0 18px 24px;
}
.markdown-content li {
  margin-bottom: 6px;
}

.markdown-content blockquote {
  background: #F3ECE0;
  border: 1px solid var(--border-main);
  border-radius: 4px;
  padding: 14px 20px;
  margin: 20px 0;
  font-size: 13.5px;
  font-style: italic;
  color: #523E3B;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 13px;
  border: 1px solid var(--border-main);
}
.markdown-content th {
  background: #ECE4D6;
  font-family: var(--font-serif);
  font-weight: 700;
  color: var(--border-dark);
  text-align: left;
  padding: 10px 14px;
  border: 1px solid var(--border-main);
}
.markdown-content td {
  padding: 9px 14px;
  border: 1px solid var(--border-main);
}
.markdown-content tr:nth-child(even) {
  background: #F8F4EC;
}

.markdown-content code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: #EDE6D8;
  padding: 2px 6px;
  border-radius: 3px;
  color: var(--accent-burgundy);
}

.prototype-bar {
  background: #F4EFE6;
  border-bottom: 1px solid var(--border-main);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}
.prototype-links {
  display: flex;
  gap: 12px;
}
.prototype-links a {
  color: var(--text-muted);
  text-decoration: none;
  padding: 4px 8px;
  font-family: var(--font-mono);
}
.prototype-links a:hover, .prototype-links a.active {
  color: var(--accent-burgundy);
  font-weight: 700;
}
"""

# =========================================================================
# PROTOTYPE 3: ⚡ Modern Studio (极简工坊 · 现代科技白)
# =========================================================================
CSS_STUDIO = """
:root {
  --bg-page: #FFFFFF;
  --bg-surface: #FAFAFA;
  --bg-card: #FFFFFF;
  --bg-subtle: #F4F4F5;
  --border-light: #F4F4F5;
  --border-main: #E4E4E7;
  --border-strong: #D4D4D8;
  --text-main: #09090B;
  --text-muted: #71717A;
  --text-light: #A1A1AA;
  --accent-blue: #0284C7;
  --accent-cyan: #06B6D4;
  --accent-bg: #F0F9FF;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', system-ui, sans-serif;
  --font-mono: 'SFMono-Regular', Menlo, Monaco, Consolas, monospace;
  --radius-md: 10px;
  --radius-lg: 14px;
  --shadow-subtle: 0 1px 3px rgba(0,0,0,0.03), 0 1px 2px rgba(0,0,0,0.02);
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 15px; }
body {
  background: var(--bg-page);
  color: var(--text-main);
  font-family: var(--font-sans);
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}

.app-container {
  max-width: 1340px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 270px 1fr;
  min-height: 100vh;
}

@media (max-width: 1024px) {
  .app-container { grid-template-columns: 1fr; }
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 30px 20px;
  background: var(--bg-surface);
  border-right: 1px solid var(--border-main);
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (max-width: 1024px) {
  .sidebar { position: relative; height: auto; border-right: none; border-bottom: 1px solid var(--border-main); }
}

.brand-block {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--border-main);
}
.brand-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: var(--accent-blue);
}
.brand-text h1 {
  font-size: 14.5px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text-main);
}
.brand-text span {
  display: block;
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-light);
  margin-bottom: 8px;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.toc-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  text-decoration: none;
  color: var(--text-muted);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.15s;
}
.toc-item:hover {
  background: var(--bg-subtle);
  color: var(--text-main);
}
.toc-item.active {
  background: var(--bg-subtle);
  color: var(--text-main);
  font-weight: 600;
}
.toc-num {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-light);
  margin-top: 1px;
}
.toc-item.active .toc-num {
  color: var(--accent-blue);
}
.toc-text {
  flex: 1;
  line-height: 1.4;
}
.toc-text small {
  display: block;
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-light);
  margin-top: 2px;
}

.main-content {
  padding: 36px 48px 80px;
  max-width: 980px;
}

@media (max-width: 768px) {
  .main-content { padding: 20px 16px 40px; }
}

.studio-hero {
  background: var(--bg-surface);
  border: 1px solid var(--border-main);
  border-radius: var(--radius-lg);
  padding: 24px 28px;
  margin-bottom: 32px;
}
.hero-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--accent-blue);
  background: var(--accent-bg);
  padding: 3px 8px;
  border-radius: 999px;
  display: inline-block;
  margin-bottom: 12px;
}
.studio-hero h1 {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.02em;
  color: var(--text-main);
  margin-bottom: 6px;
}
.studio-hero p {
  color: var(--text-muted);
  font-size: 13.5px;
}

.summary-card, .article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-main);
  border-radius: var(--radius-lg);
  margin-bottom: 32px;
  box-shadow: var(--shadow-subtle);
  transition: border-color 0.2s;
}
.summary-card:hover, .article-card:hover {
  border-color: var(--border-strong);
}

.summary-header, .article-header {
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-light);
}

.article-title {
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.01em;
  line-height: 1.4;
}
.article-title a {
  color: var(--text-main);
  text-decoration: none;
}
.article-title a:hover {
  color: var(--accent-blue);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 6px;
}
.meta-sep { color: var(--border-main); }
.meta-link { color: var(--accent-blue); text-decoration: none; font-weight: 500; }

.article-body {
  padding: 28px 32px;
}

@media (max-width: 768px) {
  .article-body { padding: 18px 16px; }
  .summary-header, .article-header { padding: 16px 18px; }
}

.markdown-content {
  font-size: 13.5px;
  line-height: 1.8;
  color: #27272A;
}

.markdown-content h1 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-main);
  color: var(--text-main);
}

.markdown-content h2 {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text-main);
  background: var(--bg-subtle);
  border: 1px solid var(--border-main);
  padding: 6px 12px;
  border-radius: 6px;
  margin: 26px 0 12px;
}

.markdown-content h3 {
  font-size: 13.5px;
  font-weight: 600;
  margin: 18px 0 8px;
  color: var(--text-main);
}

.markdown-content p {
  margin-bottom: 14px;
}

.markdown-content strong {
  font-weight: 600;
  color: #09090B;
}

.markdown-content ul, .markdown-content ol {
  margin: 10px 0 14px 20px;
}
.markdown-content li {
  margin-bottom: 5px;
}

.markdown-content blockquote {
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  padding: 10px 16px;
  margin: 16px 0;
  border-radius: 6px;
  font-size: 13px;
  color: #166534;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0;
  font-size: 12.5px;
  border: 1px solid var(--border-main);
  border-radius: 6px;
  overflow: hidden;
}
.markdown-content th {
  background: var(--bg-subtle);
  font-weight: 600;
  text-align: left;
  padding: 8px 12px;
  border: 1px solid var(--border-main);
}
.markdown-content td {
  padding: 8px 12px;
  border: 1px solid var(--border-main);
}

.markdown-content code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: var(--bg-subtle);
  padding: 2px 6px;
  border-radius: 4px;
  color: #BE185D;
}

.prototype-bar {
  background: #FAFAFA;
  border-bottom: 1px solid var(--border-main);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}
.prototype-links {
  display: flex;
  gap: 10px;
}
.prototype-links a {
  color: var(--text-muted);
  text-decoration: none;
  padding: 3px 8px;
  border-radius: 6px;
  font-family: var(--font-mono);
}
.prototype-links a:hover, .prototype-links a.active {
  background: var(--border-main);
  color: var(--text-main);
}
"""

# =========================================================================
# PROTOTYPE 4: 🌿 Kyoto Serif (典雅文澜 · 护眼茶白)
# =========================================================================
CSS_ZENITH = """
:root {
  --bg-page: #F6F5F0;
  --bg-surface: #FAF9F5;
  --bg-card: #FCFBF9;
  --bg-subtle: #EFECE3;
  --border-main: #E3DEC3;
  --border-light: #EBE7DE;
  --text-main: #2C2C2A;
  --text-muted: #6B6860;
  --text-light: #9C988F;
  --accent-pine: #2D5A43;
  --accent-chestnut: #784435;
  --font-serif: 'Noto Serif SC', 'Songti SC', SimSun, Georgia, serif;
  --font-sans: 'Noto Sans SC', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; font-size: 15px; }
body {
  background: var(--bg-page);
  color: var(--text-main);
  font-family: var(--font-serif);
  line-height: 1.9;
  -webkit-font-smoothing: antialiased;
}

.app-container {
  max-width: 1260px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
  background: var(--bg-surface);
  border-left: 1px solid var(--border-main);
  border-right: 1px solid var(--border-main);
}

@media (max-width: 1024px) {
  .app-container { grid-template-columns: 1fr; border: none; }
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  padding: 36px 24px;
  background: #F4F2EC;
  border-right: 1px solid var(--border-main);
  display: flex;
  flex-direction: column;
  gap: 28px;
}

@media (max-width: 1024px) {
  .sidebar { position: relative; height: auto; border-right: none; border-bottom: 1px solid var(--border-main); }
}

.brand-block {
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-main);
}
.brand-text h1 {
  font-size: 18px;
  font-weight: 700;
  color: var(--accent-pine);
  letter-spacing: 0.08em;
}
.brand-text span {
  display: block;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-light);
  letter-spacing: 0.1em;
  margin-top: 4px;
}

.nav-section-title {
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: var(--accent-pine);
  margin-bottom: 12px;
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toc-item {
  display: flex;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 4px;
  text-decoration: none;
  color: var(--text-main);
  border: 1px solid transparent;
  transition: all 0.2s;
}
.toc-item:hover {
  background: var(--bg-subtle);
  border-color: var(--border-main);
}
.toc-item.active {
  background: #EAE6DB;
  border-color: var(--border-main);
  color: var(--accent-pine);
  font-weight: 700;
}
.toc-num {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-light);
  margin-top: 3px;
}
.toc-item.active .toc-num {
  color: var(--accent-pine);
}
.toc-text {
  font-size: 13.5px;
  line-height: 1.5;
}
.toc-text small {
  display: block;
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-muted);
  font-weight: 400;
  margin-top: 3px;
}

.main-content {
  padding: 40px 48px 80px;
  max-width: 920px;
}

@media (max-width: 768px) {
  .main-content { padding: 24px 18px 40px; }
}

.zenith-hero {
  background: var(--bg-card);
  border: 1px solid var(--border-main);
  padding: 28px 32px;
  margin-bottom: 36px;
  border-radius: 4px;
}
.zenith-hero h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--accent-pine);
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}
.zenith-hero p {
  color: var(--text-muted);
  font-size: 14px;
}

.summary-card, .article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-main);
  border-radius: 4px;
  margin-bottom: 38px;
}

.summary-header, .article-header {
  background: #F7F5EE;
  padding: 20px 28px;
  border-bottom: 1px solid var(--border-main);
}

.article-title {
  font-size: 19px;
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.4;
}
.article-title a {
  color: inherit;
  text-decoration: none;
}
.article-title a:hover {
  color: var(--accent-pine);
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 8px;
}
.meta-sep { color: var(--border-main); }
.meta-link { color: var(--accent-pine); text-decoration: none; font-weight: 600; }

.article-body {
  padding: 32px 36px;
}

@media (max-width: 768px) {
  .article-body { padding: 20px 18px; }
  .summary-header, .article-header { padding: 16px 18px; }
}

.markdown-content {
  font-size: 14.5px;
  line-height: 1.95;
  color: #31302E;
}

.markdown-content h1 {
  font-size: 21px;
  font-weight: 700;
  margin: 0 0 18px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-main);
  color: var(--accent-pine);
}

.markdown-content h2 {
  font-size: 15px;
  font-weight: 700;
  color: var(--accent-pine);
  border: 1px solid var(--border-main);
  padding: 6px 12px;
  background: #F2EFE7;
  border-radius: 4px;
  margin: 30px 0 14px;
}

.markdown-content h3 {
  font-size: 14px;
  font-weight: 700;
  margin: 22px 0 10px;
  color: var(--accent-chestnut);
}

.markdown-content p {
  margin-bottom: 16px;
}

.markdown-content strong {
  font-weight: 700;
  color: #1F1F1D;
}

.markdown-content ul, .markdown-content ol {
  margin: 12px 0 18px 24px;
}
.markdown-content li {
  margin-bottom: 6px;
}

.markdown-content blockquote {
  background: #F1ECE1;
  border: 1px solid var(--border-main);
  border-radius: 4px;
  padding: 12px 18px;
  margin: 20px 0;
  font-size: 13.5px;
  color: #5C382C;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 22px 0;
  font-size: 13px;
  border: 1px solid var(--border-main);
}
.markdown-content th {
  background: #EFECE3;
  font-weight: 700;
  color: var(--text-main);
  text-align: left;
  padding: 9px 14px;
  border: 1px solid var(--border-main);
}
.markdown-content td {
  padding: 9px 14px;
  border: 1px solid var(--border-main);
}
.markdown-content tr:nth-child(even) {
  background: #FAF8F2;
}

.markdown-content code {
  font-family: var(--font-mono);
  font-size: 12px;
  background: #ECE8DD;
  padding: 2px 6px;
  border-radius: 3px;
  color: var(--accent-chestnut);
}

.prototype-bar {
  background: #F4F2EC;
  border-bottom: 1px solid var(--border-main);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}
.prototype-links {
  display: flex;
  gap: 12px;
}
.prototype-links a {
  color: var(--text-muted);
  text-decoration: none;
  padding: 4px 8px;
  font-family: var(--font-mono);
}
.prototype-links a:hover, .prototype-links a.active {
  color: var(--accent-pine);
  font-weight: 700;
}
"""

PROTOS_CONFIG = [
    {
        "id": "1-dossier",
        "name": "方案 A · 🏛️ 研报档案 Institutional Dossier",
        "tagline": "国际顶级投行与宏观智库白皮书风",
        "bg_desc": "纯净高白 #F8FAFC / #FFFFFF",
        "accent_desc": "投行深海蓝 #1D4ED8 + 结构化分区",
        "css": CSS_DOSSIER,
        "hero_html": """
<div class="dossier-hero">
  <div class="hero-header-line">
    <span class="hero-tag">Macro Research Dossier</span>
    <span class="hero-date-box">2026-09-03 · 归档 3 篇</span>
  </div>
  <h1>解读君财经 · 每日视频深度研报</h1>
  <p>以事实边界与逻辑链条为核心，全量呈现宏观周期、顶级投行策略及金融历史研析。</p>
</div>
""",
    },
    {
        "id": "2-gazette",
        "name": "方案 B · 📰 金融经纬 Financial Gazette",
        "tagline": "《金融时报》(FT) / 彭博社经典纸刊排版",
        "bg_desc": "暖调米纸底色 #FBF8F2 + 双实线边框",
        "accent_desc": "勃艮第红 #8B261D + 衬线大标题",
        "css": CSS_GAZETTE,
        "hero_html": """
<div class="gazette-header">
  <div>
    <h1>金融经纬 · 每日纪要</h1>
    <div class="gazette-meta">JIEDU DAILY FINANCIAL GAZETTE · VOL. 2026-09-03</div>
  </div>
  <div class="gazette-meta">3 ARTICLES ARCHIVED</div>
</div>
""",
    },
    {
        "id": "3-studio",
        "name": "方案 C · ⚡ 现代极简 Modern Studio",
        "tagline": "Linear / Apple 现代高科技极简浅色",
        "bg_desc": "雪白 #FFFFFF + 柔和灰卡 #FAFAFA",
        "accent_desc": "电光蓝 #0284C7 + 极细 Hairline",
        "css": CSS_STUDIO,
        "hero_html": """
<div class="studio-hero">
  <span class="hero-tag">DAILY DIGEST · 2026.09.03</span>
  <h1>解读君视频日报</h1>
  <p>全量结构化笔记与核心结论速览，零干扰沉浸式研读。</p>
</div>
""",
    },
    {
        "id": "4-zenith",
        "name": "方案 D · 🌿 典雅文澜 Kyoto Serif",
        "tagline": "东方文人笔记与日式书籍装帧美学",
        "bg_desc": "温润护眼淡茶白 #F6F5F0",
        "accent_desc": "松柏青绿 #2D5A43 + 舒适宋体排版",
        "css": CSS_ZENITH,
        "hero_html": """
<div class="zenith-hero">
  <h1>文澜研析 · 解读君每日纪要</h1>
  <p>二〇二六年九月三日 · 全量收录洪灏最新周期研判、大摩闭门会策略与付鹏金融史解析。</p>
</div>
""",
    },
]

def render_prototype_page(proto):
    pid = proto["id"]
    nav_proto_links = "".join([
        f'<a href="{p["id"]}.html" class="{"active" if p["id"]==pid else ""}">{p["name"].split(" · ")[0]}</a>'
        for p in PROTOS_CONFIG
    ])
    
    top_bar = f"""
<div class="prototype-bar">
  <div>
    <strong>{proto["name"]}</strong> <span style="color:var(--text-muted); margin-left:8px">[{proto["tagline"]}]</span>
  </div>
  <div class="prototype-links">
    <a href="index.html">← 全部方案对比</a>
    {nav_proto_links}
  </div>
</div>
"""
    
    page_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{proto["name"]} · 解读君视频日报</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700;900&display=swap" rel="stylesheet">
  <style>
    {proto["css"]}
  </style>
</head>
<body>
  {top_bar}
  <div class="app-container">
    <aside class="sidebar">
      <div class="brand-block">
        <div class="brand-icon">JIE</div>
        <div class="brand-text">
          <h1>解读君视频日报</h1>
          <span>JIEDU DAILY · 20260903</span>
        </div>
      </div>
      
      <div>
        <div class="nav-section-title">本日目录</div>
        <nav class="toc-list">
          {toc_html}
        </nav>
      </div>
      
      <div class="sidebar-footer">
        <div>归档日期: 2026-09-03</div>
        <div>共收录 3 篇结构化笔记</div>
      </div>
    </aside>

    <main class="main-content">
      {proto["hero_html"]}
      
      <section id="summary" class="summary-card">
        <header class="summary-header">
          <h2 class="article-title">今日核心结论汇总</h2>
          <div class="article-meta">
            <span class="meta-date">2026-09-03</span>
            <span class="meta-sep">/</span>
            <span>3 篇笔记萃取</span>
          </div>
        </header>
        <div class="article-body markdown-content">
          {summary_html}
        </div>
      </section>

      {articles_html}
    </main>
  </div>
</body>
</html>
"""
    out_file = out_dir / f"{pid}.html"
    out_file.write_text(page_html, encoding="utf-8")
    print(f"Wrote prototype: {out_file}")

# Write all 4 prototypes
for proto in PROTOS_CONFIG:
    render_prototype_page(proto)

# =========================================================================
# Write Selector / Index Page: prototypes/index.html
# =========================================================================
INDEX_HTML = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>解读君视频日报 · 4套浅色设计原型对比与选型</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;700;900&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #F8FAFC;
      --card-bg: #FFFFFF;
      --border: #E2E8F0;
      --text: #0F172A;
      --muted: #64748B;
      --primary: #1E40AF;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Noto Sans SC', sans-serif;
      padding: 40px 24px 80px;
      line-height: 1.6;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    .header {{
      text-align: center;
      margin-bottom: 40px;
    }}
    .header h1 {{
      font-family: 'Noto Serif SC', serif;
      font-size: 28px;
      font-weight: 900;
      color: var(--text);
      margin-bottom: 8px;
    }}
    .header p {{
      color: var(--muted);
      font-size: 15px;
      max-width: 600px;
      margin: 0 auto;
    }}
    
    .grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 28px;
      margin-bottom: 40px;
    }}
    @media (max-width: 860px) {{
      .grid {{ grid-template-columns: 1fr; }}
    }}

    .proto-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
      display: flex;
      flex-direction: column;
      transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }}
    .proto-card:hover {{
      transform: translateY(-3px);
      box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
      border-color: var(--primary);
    }}

    .proto-preview {{
      height: 220px;
      background: #F1F5F9;
      border-bottom: 1px solid var(--border);
      position: relative;
      overflow: hidden;
    }}
    .proto-preview iframe {{
      width: 200%;
      height: 200%;
      border: none;
      transform: scale(0.5);
      transform-origin: 0 0;
      pointer-events: none;
    }}

    .proto-info {{
      padding: 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .proto-title {{
      font-family: 'Noto Serif SC', serif;
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .proto-tag {{
      font-family: 'IBM Plex Mono', monospace;
      font-size: 11px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 4px;
      background: #EFF6FF;
      color: #1D4ED8;
    }}
    .proto-desc {{
      font-size: 13.5px;
      color: var(--muted);
      margin-bottom: 16px;
    }}
    .proto-specs {{
      background: #F8FAFC;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 12px 14px;
      font-size: 12px;
      margin-bottom: 20px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-family: 'IBM Plex Mono', monospace;
    }}
    .spec-item {{
      display: flex;
      justify-content: space-between;
    }}
    .spec-label {{
      color: var(--muted);
    }}
    .spec-value {{
      font-weight: 600;
      color: var(--text);
    }}

    .proto-btn {{
      margin-top: auto;
      display: block;
      text-align: center;
      background: var(--text);
      color: #FFFFFF;
      text-decoration: none;
      padding: 12px;
      border-radius: 8px;
      font-weight: 600;
      font-size: 14px;
      transition: background 0.15s;
    }}
    .proto-btn:hover {{
      background: var(--primary);
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>解读君视频日报 · 4套浅色设计方案</h1>
      <p>全部遵循浅色/纸面舒适背景、彻底去除侧边深色栏、无徽章视觉噪点、全量原文呈现。请点击查看各方案实际效果并选定：</p>
    </div>

    <div class="grid">
      <!-- Prototype A -->
      <div class="proto-card">
        <div class="proto-preview">
          <iframe src="1-dossier.html" loading="lazy"></iframe>
        </div>
        <div class="proto-info">
          <div class="proto-title">
            <span>方案 A · 研报档案</span>
            <span class="proto-tag">Institutional</span>
          </div>
          <div class="proto-desc">国际顶级投行与宏观智库白皮书风。纯白底色配深海青蓝结构线，适合严谨的数据逻辑与结论核验。</div>
          <div class="proto-specs">
            <div class="spec-item"><span class="spec-label">主背景色</span><span class="spec-value">#F8FAFC / #FFFFFF</span></div>
            <div class="spec-item"><span class="spec-label">视觉基调</span><span class="spec-value">投行海蓝 #1D4ED8 / 严谨克制</span></div>
            <div class="spec-item"><span class="spec-label">核心排版</span><span class="spec-value">系统无衬线 + Noto Serif 标号分层</span></div>
          </div>
          <a class="proto-btn" href="1-dossier.html">打开方案 A (研报档案) ↗</a>
        </div>
      </div>

      <!-- Prototype B -->
      <div class="proto-card">
        <div class="proto-preview">
          <iframe src="2-gazette.html" loading="lazy"></iframe>
        </div>
        <div class="proto-info">
          <div class="proto-title">
            <span>方案 B · 金融经纬</span>
            <span class="proto-tag">Gazette</span>
          </div>
          <div class="proto-desc">《金融时报》(FT) 与彭博社经典纸刊排版。暖调米纸底色配勃艮第酒红与经典报刊衬线体。</div>
          <div class="proto-specs">
            <div class="spec-item"><span class="spec-label">主背景色</span><span class="spec-value">#FBF8F2 (暖调米纸)</span></div>
            <div class="spec-item"><span class="spec-label">视觉基调</span><span class="spec-value">勃艮第红 #8B261D / 报章经纬</span></div>
            <div class="spec-item"><span class="spec-label">核心排版</span><span class="spec-value">Noto Serif SC 经典社论字距</span></div>
          </div>
          <a class="proto-btn" href="2-gazette.html">打开方案 B (金融经纬) ↗</a>
        </div>
      </div>

      <!-- Prototype C -->
      <div class="proto-card">
        <div class="proto-preview">
          <iframe src="3-studio.html" loading="lazy"></iframe>
        </div>
        <div class="proto-info">
          <div class="proto-title">
            <span>方案 C · 极简工坊</span>
            <span class="proto-tag">Modern Studio</span>
          </div>
          <div class="proto-desc">Linear / Apple 风格高科技极简浅色。雪白背景与极细微边框，微动效目录，现代感最强。</div>
          <div class="proto-specs">
            <div class="spec-item"><span class="spec-label">主背景色</span><span class="spec-value">#FFFFFF / #FAFAFA</span></div>
            <div class="spec-item"><span class="spec-label">视觉基调</span><span class="spec-value">电光蓝 #0284C7 / 极简科技</span></div>
            <div class="spec-item"><span class="spec-label">核心排版</span><span class="spec-value">Modern Sans + 等宽代码流</span></div>
          </div>
          <a class="proto-btn" href="3-studio.html">打开方案 C (极简工坊) ↗</a>
        </div>
      </div>

      <!-- Prototype D -->
      <div class="proto-card">
        <div class="proto-preview">
          <iframe src="4-zenith.html" loading="lazy"></iframe>
        </div>
        <div class="proto-info">
          <div class="proto-title">
            <span>方案 D · 典雅文澜</span>
            <span class="proto-tag">Kyoto Serif</span>
          </div>
          <div class="proto-desc">东方文人笔记与日式书籍装帧美学。温润淡茶白背景配松柏绿与落栗色，护眼沉浸式研读。</div>
          <div class="proto-specs">
            <div class="spec-item"><span class="spec-label">主背景色</span><span class="spec-value">#F6F5F0 (淡茶护眼白)</span></div>
            <div class="spec-item"><span class="spec-label">视觉基调</span><span class="spec-value">松柏绿 #2D5A43 + 落栗 #784435</span></div>
            <div class="spec-item"><span class="spec-label">核心排版</span><span class="spec-value">宋体/明体长文排版 · 疏朗从容</span></div>
          </div>
          <a class="proto-btn" href="4-zenith.html">打开方案 D (典雅文澜) ↗</a>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""

index_file = out_dir / "index.html"
index_file.write_text(INDEX_HTML, encoding="utf-8")
print(f"Wrote prototype index: {index_file}")
