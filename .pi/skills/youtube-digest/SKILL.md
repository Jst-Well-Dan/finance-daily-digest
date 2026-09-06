---
name: youtube-digest
description: 一键完成解读君 YouTube 频道视频的增量下载、转写、结构化笔记与视频总结。用于用户要求"获取YouTube视频并总结""处理解读君视频""下载并转写解读君频道视频""视频日报""一键处理视频"时触发。只处理解读君视频，不涉及小鹅通/蹊涯尊享圈帖子和股票池；如需处理帖子，使用 `xiaoe-fetch-and-summarize` 技能。
---

# 解读君视频获取、转写与总结

## 目标

把"增量下载解读君新视频""转写为文字稿""生成结构化笔记"和"撰写视频总结"串成一个连续工作流，和帖子处理完全独立，可以单独触发、单独排期，不依赖帖子技能是否运行过。

## 依赖

执行前必须读取并遵守这两个本地 skill：

1. `.pi/skills/video-downloader/SKILL.md`
2. `.pi/skills/video-transcriber/SKILL.md`

`video-downloader` 使用 `yt-dlp` 下载频道视频并维护 `--download-archive` 去重；`video-transcriber` 把音轨转成 Markdown 文字稿。不要用脚本或关键词规则自动生成总结正文。

> **脚手架自检（本项目新增）**：若数据根下缺失 `content_paths.json` 或 `scripts/resolve_daily_dir.py`，须先创建（`content_paths.json` 含 `{"daily_dir":"daily"}`，`resolve_daily_dir.py` 支持 `--date YYYYMMDD --ensure` 输出 `<daily_dir>/YYYYMMDD`），再继续流程。禁止假设绝对路径。

## 输出路径配置

每日产出根目录由数据根（pi 会话工作目录，见下）的 `content_paths.json` 中 `daily_dir` 决定（当前值为 `daily`）。以下用 `<daily_dir>` 代称；下载命令应先运行 `python scripts/resolve_daily_dir.py --date YYYYMMDD --ensure` 获取实际目录。

## 默认路径

**路径约定（重要）**：pi 会话的工作目录就是数据根（先运行 `pwd` 确认；数据根下应有 `content_paths.json`、`.pi/skills/`、`scripts/`、`daily/`、`stock_pool.json`）。以下所有路径均为**相对数据根的相对路径**（如 `.pi/skills/...`、`scripts/resolve_daily_dir.py`），不要硬编码或假设绝对位置——开发模式与打包后 exe 的数据根位置不同，绝对路径会在他人机器或打包版上失效。

YouTube 频道：

`https://www.youtube.com/@JIEDU369/videos`

YouTube 下载归档（跨运行去重，按视频 ID）：

`.pi/skills/youtube-digest/.youtube_download_archive.txt`

视频转写脚本：

`.pi/skills/video-transcriber/scripts/transcribe_siliconflow.py`

频道下载编排脚本（必用；启用本机 Node.js 供 YouTube JS 提取，并将 `--break-on-reject` 到达日期下界时的**预期**非零退出码归一为成功；真实下载错误仍会原样失败。已彻底确认 yt-dlp 解析策略：常规方案优先探测 `PATH` 与 `Roaming/Python/.../Scripts/yt-dlp.exe`，若均不存在则一次性回退至 `python -m yt_dlp`，不再重复尝试失败的常规方案；格式已固定为 `bv*+ba/b` 以兼容 YouTube SABR 实验）：

`.pi/skills/youtube-digest/scripts/download_youtube_channel.py`

批量转写编排脚本（推荐，串起提取音频→转写→写元信息→清理，内置最多 3 路并发，并把进度写入 `--status-file` 供外部轮询）：

`.pi/skills/youtube-digest/scripts/process_video_transcripts.py`

> `scripts/orchestrate_transcribe.py` 是同一批处理逻辑的早期版本，功能上被 `process_video_transcripts.py` 覆盖（后者多了状态文件、更严格的产物校验）。暂保留未删除，新流程一律使用 `process_video_transcripts.py`，不要两个都调用。

默认输出目录：

`<daily_dir>/YYYYMMDD`（和帖子技能共享同一日期目录约定，视频各自落在独立子目录，不会冲突）

默认视频目录与转写稿：

`<daily_dir>/YYYYMMDD/视频标题 [视频ID]/视频标题 [视频ID].md`

默认视频结构化笔记：

`<daily_dir>/YYYYMMDD/视频标题 [视频ID]/视频标题 [视频ID]_结构化笔记.md`

默认视频总结文件：

`<daily_dir>/YYYYMMDD/YYYYMMDD_解读君视频总结.md`

## 增量范围策略

本技能不再和帖子技能共用日期范围（两者已解耦，可能各自独立排期）。默认用**滚动回溯窗口**代替"记录上次运行时间"的状态文件：

- 未指定范围时，`--dateafter` = 今天 - 14 天，`--datebefore` = 明天。
- 用户指定 `--start/--end` 或 `--days N` 时按用户范围执行。
- 依赖 `--download-archive` 按视频 ID 去重，14 天的窗口有重叠也不会重复下载或重复转写，代价是每次多扫描几天，可接受。
- 如果用户超过 14 天没有运行本技能，需要显式加大回溯天数，否则会漏掉更早的视频。

## 工作流

1. 读取两个依赖 skill 的 `SKILL.md`，确认 `yt-dlp`、Node.js、`ffmpeg` 和 `SILICONFLOW_API_KEY` 可用。若 `yt-dlp` 报告版本已超过 90 天，先用其所属 Python 环境执行 `python -m pip install --upgrade yt-dlp`；不要把版本警告当作下载成功。
2. 按增量范围策略计算 `--dateafter`/`--datebefore`，**必须**调用频道下载编排脚本增量下载解读君频道视频，而不是手写 `yt-dlp` 命令。例如：
   ```bash
   python .pi/skills/youtube-digest/scripts/download_youtube_channel.py \
     --run-dir "$(python scripts/resolve_daily_dir.py --date YYYYMMDD --ensure)" \
     --dateafter YYYYMMDD --datebefore YYYYMMDD \
     --archive .pi/skills/youtube-digest/.youtube_download_archive.txt \
     --yt-dlp "<yt-dlp 绝对路径>"
   ```
   - 脚本使用 `--download-archive` 防止重复下载、`--lazy-playlist --break-on-reject` 在遇到早于范围的视频时提前停止、`--concurrent-fragments 4` 并发下载单个视频的媒体分片，并保存 `.info.json`；格式固定为 `bv*+ba/b`（原 `best[ext=mp4]/best` 在 SABR 下会报 Requested format is not available，已废弃）。
   - 它会把 Node.js 传给 yt-dlp，避免“未找到支持的 JavaScript runtime”导致 YouTube 格式缺失。
   - yt-dlp 解析：先试 `which yt-dlp`，再探测 `Roaming/Python/.../Scripts/yt-dlp.exe`，均不存在则一次性回退至 `python -m yt_dlp`，不在常规与回退间反复失败。
   - `--break-on-reject` 在到达日期下界时会让 yt-dlp 返回非零码；脚本只将该有明确标记、且不含 `ERROR:` 的预期边界停止视为成功，不能以 `|| exit 0` 等方式吞掉真实下载错误。
   - 保存到本次运行输出目录 `<daily_dir>/YYYYMMDD/视频标题 [视频ID]/视频标题 [视频ID].扩展名`，不要按视频 `upload_date` 分散到历史日期目录；标题已用 `%(title).120B` 限制，不再额外叠加 `--trim-filenames 120` 以避免双重裁剪导致文件名被截为“大摩.md”。
3. 调用 `process_video_transcripts.py` 对本次运行输出目录内每个已有 `.info.json` 且尚无同名 `.md` 的视频批量转写：
   - 最多 3 路并发；单个失败不取消其他任务。
   - 成功后目录内只保留 Markdown（脚本已处理音频/视频/`.info.json`/字幕清理）；失败项保留原始文件供下次重试。
   - 同名 Markdown 已存在时跳过。
4. 判断本次新增数量：如果没有新视频、也没有待补转写的内容，告知用户没有新内容，不要为了生成文件而凭空总结。
5. 枚举本次运行输出目录下"目录名和转写 Markdown 文件名均以 `[视频ID]` 结尾"的视频转写稿；不要把结构化笔记误当成原始转写稿。
6. 每份新转写稿完成后，交给一个独立 subagent（可用 `worker` 或 `delegate`，不可用 `default`）完整阅读并写入同目录的 `视频标题 [视频ID]_结构化笔记.md`；最多同时运行 3 个视频阅读 subagent。
   - 给 subagent 最小必要上下文，只提供转写稿路径、笔记路径和下文“固定结构化笔记结构及写作要求”；不要把当前长对话完整复制给它。每份笔记控制在约 1800-3000 个中文字符。
   - subagent 必须完整阅读转写稿，但不得代写最终每日总结；主 Agent 负责汇总各视频的“核心结论”。初稿应以一次 `write` 写入；后续改稿时先重新读取目标文件，单次 `edit` 的每个 `oldText` 都必须存在于**调用前的同一版本**，且各编辑区间不能重叠。存在前后依赖的改动必须拆成多次 `edit`。这样避免 `Could not find edits[n]` 造成假失败。subagent 失败时由主 Agent 直接阅读该转写稿兜底，不阻塞其他视频。
   - 转写产物命名已修复：`process_video_transcripts.py` 不再用截断的 `media.stem`，改以目录名 `视频标题 [ID]` 确保 `[ID]` 后缀，若遇旧截断产物会自动重命名。
7. 主 Agent 真实阅读全部结构化笔记的“核心结论”；对核心结论中关键、矛盾、含糊或高影响判断回查原始转写稿，并用标题、视频 ID、发布日期和来源 URL 核验来源。
8. 按下面的“固定每日总结结构”撰写 `<daily_dir>/YYYYMMDD/YYYYMMDD_解读君视频总结.md`。本地管线中一句话提炼由 `scripts/generate_tldr_via_pi_print.py` 生成并缓存于同目录 `.tldr.json`，再由 `scripts/build_daily_summary.py` 拼入；交互式执行时主 Agent 可亲写一句话，但须遵守同样的“严格基于本视频核心结论”约束。
9. 保存后回复用户：新视频数、成功转写数、结构化笔记数、总结路径、主要结论；下载或转写失败时列出失败项，说明已保留原始文件供下次重试。

## 固定结构化笔记结构及写作要求

```markdown
# 结构化笔记｜视频标题

## 1. 核心结论
<!-- 3–5 条；每条包含结论及适用条件/边界。此节将被每日总结原样引用。 -->

## 2. 专家观点与逻辑链
### 观点 1：主题名称
- **观点归属：** 嘉宾 / 机构。
- **结论：** 其明确看多、看空、谨慎或中性什么。
- **前提事实：** 支撑观点的视频事实性陈述；标明是否待核验。
- **推导逻辑：** `前提 A → 变化 B → 盈利/估值/风险 C → 观点结论`
- **隐含假设：**
- **反例 / 证伪条件：**

> 排版硬要求：观点标题行（###）与字段列表之间必须空一行；每个字段独立占一行 `- ` 列表；禁止把多个字段合并写进同一段落。

## 3. 投资研究指引
> 记录视频所表达的研究方向，不构成买卖建议；没有明确投资含义时如实写“未给出可执行指引”。

| 主题 / 对象 | 视频隐含或明确的方向 | 为什么 | 正向验证信号 | 风险 / 失效信号 | 需补的证据 |
|---|---|---|---|---|---|
```

写作要求：

- 完整阅读转写稿。清楚区分“嘉宾观点”和“Agent 对其逻辑的整理”；不得将两者写成事实。
- “核心结论”须为可独立阅读的 3–5 条短结论，表达准确、保留条件与不确定性，不包含来源列表；除格式微调外，主 Agent 应将其原样放入每日总结。
- “专家观点与逻辑链”必须展示从前提到结论的推导，并写明隐含假设、反例或证伪条件；不要再按“宏观/策略/行业/公司”机械分类。
- “投资研究指引”只在视频提供了明确的方向与逻辑时填写。公司或资产仅被顺带提及时，不得伪造研究结论；用验证/失效条件替代买入、卖出、目标价或配置比例式建议。
- 转写中的人名、公司名、金额、百分比、政策条文和时间表优先回看原视频或一手文件；发现语义突变、疑似串入文本或转写错误，须从核心结论中剔除。

## 固定每日总结结构

```markdown
# 解读君视频摘要

## 1. 视频标题

> 一句话：本期最值得投资者知道的一句话提炼（管线经 pi 由核心结论生成，缓存于 `.tldr.json`）。

<!-- 原样复制该视频结构化笔记的“核心结论”章节。 -->

## 2. 视频标题

> 一句话：本期最值得投资者知道的一句话提炼。

<!-- 原样复制该视频结构化笔记的“核心结论”章节。 -->
```

每日总结只包含每篇视频的标题、一句话提炼和结构化笔记的“核心结论”。一句话提炼必须严格基于该视频核心结论，不得引入结论之外的信息，更不得跨视频综合；除此之外不得加入统计范围、来源元信息、跨视频综合结论、主题重组、后续跟踪清单、投资研究指引、参考视频段落或其他内容。

## 股票池

本技能不提取股票池。股票池只从帖子来源提取，见 `xiaoe-stock-pool-extractor`；除非用户明确要求把视频纳入股票池来源，否则不要从视频转写稿或结构化笔记生成或合并股票池条目。

## 与帖子技能的关系

`xiaoe-fetch-and-summarize`（帖子+股票池）和本技能相互独立，可以任意顺序、任意时间单独触发，不共享状态，也不互相阻塞。两者的产出都落在同一个 `<daily_dir>/YYYYMMDD/` 目录下，互不覆盖（文件名不同）。
