#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_notes_via_pi_print.py — 用本机 `pi -p`（print 模式）为 daily 目录生成结构化笔记。

用法:
    python scripts/generate_notes_via_pi_print.py --daily-dir daily/20260903
    python scripts/generate_notes_via_pi_print.py --daily-dir daily/20260903 --limit 1
    python scripts/generate_notes_via_pi_print.py --daily-dir daily/20260903 --timeout 300

依赖: 本机已安装并配置好 `pi`（`pi --list-models` 能看到可用模型）。无需 npm、无需 node。
原理: 每篇转写稿独立起一个 `pi -p --no-session --no-tools` 进程，把「模板+转写稿」
     写进临时 prompt 文件并以 @文件 传入，stdout 即笔记正文。单篇失败不中断。
环境变量:
    PI_MODEL   可选，透传给 `pi --model`（如 muse-spark-1.3-contributor）；未设则用 pi 默认模型。
退出码: 0=无待办或全部成功，1=部分失败。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATE = """# 结构化笔记｜{title}

## 1. 核心结论
<!-- 3–5 条；每条包含结论及适用条件/边界。此节将被每日总结原样引用。 -->

## 2. 专家观点与逻辑链
### 观点 1：主题名称
- **观点归属：**
- **结论：**
- **前提事实：**
- **推导逻辑：** `前提 A → 变化 B → 结论`
- **隐含假设：**
- **反例 / 证伪条件：**
- **原文位置：**

## 3. 投资研究指引
> 记录视频所表达的研究方向，不构成买卖建议；没有明确投资含义时如实写“未给出可执行指引”。
| 主题 / 对象 | 视频隐含或明确的方向 | 为什么 | 正向验证信号 | 风险 / 失效信号 | 需补的证据 |
|---|---|---|---|---|---|

写作要求：完整阅读转写稿，聚焦观点、逻辑链与投资指引，区分“观点”与“整理”；核心结论 3-5 条可独立阅读；观点必须展示推导、隐含假设与证伪条件；无明确方向时写“未给出可执行指引”；发现串入/拼接/错字须从结论剔除。
"""

DIR_RE = re.compile(r"\[[A-Za-z0-9_-]{6,}\]$")
VID_RE = re.compile(r"\[([A-Za-z0-9_-]{6,})\]$")


def build_prompt(transcript: str, title: str) -> str:
    return (
        "你是一名财经研究员。请完整阅读以下转写稿，并按固定模板生成结构化笔记，"
        "直接输出 Markdown 正文，不要解释过程。\n\n"
        "固定模板（严格按此结构输出）：\n"
        f"{TEMPLATE.format(title=title)}\n\n"
        f"转写稿全文如下（标题：{title}）：\n---\n{transcript[:30000]}\n---\n\n"
        "要求：\n"
        "- 完整阅读后按模板输出，不要省略任何一级标题（1-3）。\n"
        "- 核心结论 3-5 条，每条含结论+适用条件/边界，将被每日总结原样引用。\n"
        "- 观点与整理必须分离，不得将观点写成事实。\n"
        "- 发现串入/拼接/错字须从结论剔除。\n"
        "- 直接输出 Markdown，不要包裹代码块。"
    )


def clean_output(text: str) -> str:
    out = text.strip()
    out = re.sub(r"^```markdown\s*", "", out, flags=re.I)
    out = re.sub(r"^```\s*", "", out)
    out = re.sub(r"```\s*$", "", out)
    out = re.sub(r"\n?---\s*$", "", out)
    out = out.replace("\ufeff", "").replace("\u200b", "").strip()
    return out


def collect_tasks(daily: Path) -> list[tuple[Path, Path]]:
    tasks: list[tuple[Path, Path]] = []
    for d in sorted(daily.iterdir()):
        if not d.is_dir() or not DIR_RE.search(d.name):
            continue
        vid = (VID_RE.search(d.name) or [None, ""])[1]
        if vid.startswith("UC") or "Decoding Finance" in d.name:
            continue
        cands = [f for f in sorted(d.iterdir())
                 if f.is_file() and f.suffix == ".md"
                 and not f.name.endswith("_结构化笔记.md") and f"[{vid}]" in f.name]
        if not cands:
            cands = [f for f in sorted(d.iterdir())
                     if f.is_file() and f.suffix == ".md"
                     and not f.name.endswith("_结构化笔记.md")]
        for t in cands:
            if t.stat().st_size < 500:
                continue
            note = t.parent / (t.stem + "_结构化笔记.md")
            if note.exists() and note.stat().st_size > 800:
                print(f"跳过已存在: {note}")
                continue
            tasks.append((t, note))
    return tasks


def generate_one(pi_bin: str, model: str, tpath: Path, note: Path, timeout: int) -> bool:
    transcript = tpath.read_text(encoding="utf-8")
    m = re.search(r"^#\s+(.+)", transcript, flags=re.M)
    title = (m.group(1).strip() if m else re.sub(r"\s*\[[^\]]+\]$", "", tpath.parent.name))
    prompt = build_prompt(transcript, title)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        prompt_file = f.name
    cmd = [pi_bin, "-p", "--no-session", "--no-tools", f"@{prompt_file}"]
    if model:
        cmd += ["--model", model]
    print(f"\n=== 生成 {note.name} ← {tpath.name} ===")
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"✗ 超时（>{timeout}s），已跳过，下次重试")
        return False
    finally:
        Path(prompt_file).unlink(missing_ok=True)
    if p.returncode != 0:
        print(f"✗ pi 退出码 {p.returncode}: {(p.stderr or '').strip()[-500:]}")
        return False
    out = clean_output(p.stdout or "")
    if len(out) < 800:
        print(f"✗ 生成内容过短（{len(out)} 字符），疑似截断，已丢弃")
        return False
    note.write_text(out, encoding="utf-8")
    print(f"✓ 已写入 {note}（{len(out)} 字符）")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--daily-dir", required=True)
    ap.add_argument("--limit", type=int, default=0, help="最多生成篇数（0=不限）")
    ap.add_argument("--timeout", type=int, default=300, help="单篇超时秒数")
    ap.add_argument("--pi-bin", default="pi", help="pi 可执行文件路径")
    args = ap.parse_args()

    pi_bin = args.pi_bin
    if not Path(pi_bin).exists():
        found = shutil.which(pi_bin)
        if not found:
            print(f"✗ 找不到 pi：{pi_bin}（先确认本机已安装并登录 pi）")
            return 1
        pi_bin = found

    daily = Path(args.daily_dir)
    if not daily.is_dir():
        print(f"✗ 目录不存在: {daily}")
        return 1

    tasks = collect_tasks(daily)
    if not tasks:
        print("无待生成笔记")
        return 0
    if args.limit > 0:
        tasks = tasks[: args.limit]
        print(f"本次限制只生成 {len(tasks)} 篇（--limit {args.limit}）")
    model = os.environ.get("PI_MODEL", "")
    print(f"待生成 {len(tasks)} 篇笔记（pi -p{', model=' + model if model else ''}）...")

    failed = 0
    for tpath, note in tasks:
        try:
            if not generate_one(pi_bin, model, tpath, note, args.timeout):
                failed += 1
        except Exception as e:  # noqa: BLE001 — 单篇失败不中断
            print(f"✗ 失败 {note}: {e}")
            failed += 1
    if failed:
        print(f"\n⚠ {failed}/{len(tasks)} 篇失败（已保留现场，下次重试）")
        return 1
    print("\n全部完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
