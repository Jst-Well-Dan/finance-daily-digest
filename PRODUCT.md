# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

static HTML/CSS — delegated: plain static HTML + vanilla CSS/JS, no framework, deploy as single file `index.html` at project root for direct open or GitHub Pages

## Users

Primary: 解读君 YouTube 频道的核心观众与研究者 — 在每日复盘场景下，需要快速浏览当日新增视频的核心结论、追溯结构化笔记与原始转写稿，核验来源与边界。次要：团队内部运营/内容审核，需要沉淀可检索的视频档案。

## Product Purpose

将“解读君”YouTube 频道增量下载→转写→结构化笔记→每日总结的 Markdown 产出（落于 `daily/YYYYMMDD/`），以可读、可检索、可追溯的网页形态呈现。成功标准：读者在首屏即可判断今日有无新增、新增视频的核心结论，并在 2 次点击内抵达结构化笔记与转写原文，完整保留“待核验/已核验/转写质量”边界。

## Positioning

唯一机制：以 `daily/` 为单一事实源的静态站 — 不依赖后端，直接读取当日 `YYYYMMDD_解读君视频总结.md` 与各 `*_结构化笔记.md`，保持与本地文件系统一致的增量与去重语义。

## Operating Context

工作流：`download_youtube_channel.py`（日期窗口 + archive 去重）→ `process_video_transcripts.py`（ffmpeg → SiliconFlow）→ 结构化笔记（1800-3000字固定模板）→ 每日总结。产出位于 `daily/20260903/` 等日期目录，当前已有 20260903 三视频（洪灏/大摩/付鹏）及总结。

## Capabilities and Constraints

- 只读展示；不改写 `daily/`，不触 `archive`
- 需解析 Markdown 核心结论与结构化笔记的固定小节，保留表格与引用样式
- 纯静态，可直接双击 `index.html` 打开，无需构建
- 术语：视频ID、结构化笔记、转写正文、核心结论

## Brand Commitments

名称：解读君视频日报 / JIEDU Daily。沿用解读君财经的专业、克制气质，无新增品牌色约束。

## Evidence on Hand

- `daily/20260903/20260903_解读君视频总结.md`（3 视频核心结论）
- `daily/20260903/*/*_结构化笔记.md` ×3
- `daily/20260903/*/*.md` 转写稿 ×3
- 产出规模已验证：单日 3 视频，转写 25-58KB

## Product Principles

1. 事实边界优先 — 待核验/错字/串段必须可见，不美化为事实
2. 结论先行 — 首屏即核心结论，细节按需下钻
3. 零后端保真 — 网页是文件系统的镜像，不创造新数据源

## Accessibility & Inclusion

支持键盘导航与高对比阅读；中文排版遵循 65-75ch 行长。
