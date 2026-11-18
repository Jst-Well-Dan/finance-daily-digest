# 本地配置说明（`.env`）

所有可变参数集中在一个 **不进版本库** 的 `.env` 里，代码中不再写死模型名、频道、窗口。

## 首次使用

```bash
cp .env.example .env      # Windows: copy .env.example .env
# 编辑 .env，至少填 SILICONFLOW_API_KEY
```

`.env` 已被 `.gitignore` 排除（第 41 行 `.env`），`.env.example` 作为模板提交在仓库里，
方便换机器时一键恢复。**不要把真实 key 写进 `.env.example`。**

## 优先级（高 → 低）

1. 命令行显式赋值：`YOUTUBE_CLEAN_MODEL=xxx python run_daily.py`
2. 命令行参数：`python run_daily.py --channels <url>`
3. `.env` 文件
4. 代码内置默认值（`opendesign/deepseek-v4.1-flash`）

因为 `env_loader.load_env()` **不覆盖已存在的环境变量**，临时试验永远优先于文件，
不会被 `.env` 悄悄盖掉。

## 全部变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `YOUTUBE_NOTES_MODEL` | `opendesign/deepseek-v4.1-flash` | 结构化笔记 + 一句话 TL;DR |
| `YOUTUBE_CLEAN_MODEL` | 跟随 NOTES | 转写稿清洗的 LLM 层 |
| `SILICONFLOW_API_KEY` | 空（必填） | 语音转写 |
| `YOUTUBE_CHANNELS` | `@JIEDU369/videos` | 空格或逗号分隔的频道 URL 列表 |
| `YOUTUBE_BACKFILL_DAYS` | `45` | 下载窗口下界兜底天数 |
| `YOUTUBE_COOKIES` | 空 | cookies.txt 相对路径（可选） |
| `YOUTUBE_CLEAN_RULES_ONLY` | `0` | 设为 `1` 全局跳过清洗的 LLM 层 |
| `YOUTUBE_CLEAN_TIMEOUT` | `900` | 单篇清洗 LLM 超时秒数 |
| `YOUTUBE_ENV_FILE` | 空 | 指定另一个 .env 路径（便于多套配置切换） |

## 换模型

模型名 **必须带 provider 前缀**，否则同名模型会让 pi 报
`Model xxx is ambiguous across providers`（本项目踩过：`deepseek-v4.1-flash`
同时存在于 opencode-go / opencode / opendesign / qwen-token-plan / radius 六个 provider）。

```bash
# 看当前可用模型
pi --list-models

# 换笔记模型：改 .env 后直接跑
python run_daily.py

# 或临时换一次
YOUTUBE_NOTES_MODEL=deepseek/deepseek-v4-pro python run_daily.py --notes-limit 1
```

> 2026-11 已知失效：`muse-spark-1.3-contributor`（openCode Go 订阅返回 403）。
> 当前验证可用：`opendesign/deepseek-v4.1-flash`、`deepseek/deepseek-flash`、
> `deepseek/deepseek-v4-pro`、`opencode-go/gemini-4-argon`。

## 自检

```bash
python scripts/env_loader.py     # 打印实际加载的 .env 与生效变量（key 已打码）
```

## 实现说明

`scripts/env_loader.py` 是零依赖的极简 .env 解析器（不用 `python-dotenv`）。
原因：这些脚本既被 `run_daily.py` 以子进程调用，也可能被 pi subagent 在任意 cwd
直接调用，多一个第三方依赖就多一个「没装上就整条流水线失败」的点。

支持：`KEY=value`、`KEY="带 \\"转义\\" 的值"`、`KEY='字面量 $HOME'`、`export KEY=v`、
行尾 `# 注释`、空值。查找顺序：`YOUTUBE_ENV_FILE` → 从脚本位置向上找仓库根
（认 `content_paths.json` 或 `.git`）下的 `.env`。
