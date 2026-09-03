# Design System: Financial Gazette (金融经纬)

<!-- impeccable:design-schema 1 -->

## Direction

- **Name**: 方案 B · 金融经纬 (Financial Gazette)
- **Concept**: 《金融时报》(Financial Times) 与彭博社经典纸刊排版。暖调米纸底色，勃艮第酒红重点标头，双实线顶边框，经典报刊衬线排版与结构化数据呈现。
- **Theme**: 纯浅色暖调纸面（无深色边栏、无深色背景、无任何 badge 徽章视觉噪点）。

## Colors

- `--bg-page`: `#FBF8F2` (暖调米纸底色)
- `--bg-surface`: `#FFFDF9` (白纸面卡片)
- `--bg-header`: `#F4EFE6` (报章眉首浅底色)
- `--bg-subtle`: `#F0EADF` (浅米灰高亮)
- `--border-main`: `#E5DDCD` (暖纸线框)
- `--border-dark`: `#2B2625` (深炭黑主经纬线)
- `--text-main`: `#231F20` (温润炭黑正文)
- `--text-muted`: `#5C554E` (副标题/元信息深灰)
- `--text-light`: `#8E8478` (页码/编号浅灰)
- `--accent-burgundy`: `#8B261D` (勃艮第酒红主强调色)
- `--accent-amber`: `#B45309` (琥珀金次强调色)

## Typography

- **Serif (Headings & Display)**: `'Noto Serif SC', Georgia, 'Times New Roman', serif`
- **Sans (Body UI)**: `'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif`
- **Monospace (Dates, IDs, Tables)**: `'IBM Plex Mono', monospace`
- **Line Height**: `1.85` (适合长文研读的呼吸感排版)

## Hierarchy & Layout

- **Desktop**: 290px 浅色暖纸侧边栏 + 自适应正文主栏（最大宽度 1300px 居中），左右 2px 实线经纬边界。
- **Header**: 双实线顶栏（`border-top: 3px double var(--border-dark); border-bottom: 1px solid var(--border-dark)`）。
- **TOC**: 包含「全量原文」与「历史归档」，支持单日独立页面与历史总览双向无缝跳转。
- **Tables & Blocks**: 细线经纬网格表格，斜体暖底引用块（`#F3ECE0`）。
