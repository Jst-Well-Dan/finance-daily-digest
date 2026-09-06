#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_tldr_via_pi_print.py — 为每日总结生成「每视频一句话 TL;DR」并缓存。

用法:
    python scripts/generate_tldr_via_pi_print.py --daily-dir daily/20260903
    python scripts/generate_tldr_via_pi_print.py --daily-dir daily/20260903 --limit 2

依赖: 本机已安装并配置好 `pi`。无需 npm。
原理: 读取各笔记 ## 1. 核心结论，逐视频起一个 `pi -p --no-session --no-tools`
     提炼一句话，结果写入 <daily-dir>/.tldr.json（随仓库提交，保证可复现）。
     build_daily_summary.py 读取该缓存拼入总结；缺失则跳过，永不阻塞。
环境变量:
    PI_MODEL   可选，透传给 `pi --model`；未设则用 pi 默认模型。
退出码: 0=无待办或全部成功，1=部分失败。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROMPT = """以下是一期财经视频的标题与核心结论，请用一句话（不超过60个汉字）概括本期最值得投资者知道的信息。
只输出这一句话，不要编号、不要 markdown、不要解释、不要加任何前后缀。

标题：{title}
核心结论：
{core}
"""


def extract_core(txt: str) -> str:
    m = re.search(r"## 1\. 核心结论(.*?)(?=\n## \d+\.)", txt, re.S)
    core = m.group(0).strip() if m else txt[:3000]
    return re.sub(r"^## 1\. 核心结论[^\n]*\n?", "", core, count=1).strip()[:4000]


def clean_line(text: str) -> str:
    out = text.strip().strip("\"'“”").strip()
    out = re.sub(r"^(一句话|TL;DR|tldr)[：:]\s*", "", out)
    out = re.sub(r"^[\d.\-、\s]+", "", out).strip()
    out = re.sub(r"\s+", "", out)  # 一句话不应含空白（含换行），顺手压长度
    return out


def generate_one(pi_bin: str, model: str, title: str, core: str, timeout: int) -> str:
    prompt = PROMPT.format(title=title, core=core)
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(prompt)
        prompt_file = f.name
    cmd = [pi_bin, "-p", "--no-session", "--no-tools", f"@{prompt_file}"]
    if model:
        cmd += ["--model", model]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    finally:
        Path(prompt_file).unlink(missing_ok=True)
    if p.returncode != 0:
        raise RuntimeError(f"pi 退出码 {p.returncode}: {(p.stderr or '').strip()[-300:]}")
    out = clean_line(p.stdout or "")
    if not (10 <= len(out) <= 150):
        raise RuntimeError(f"输出长度异常（{len(out)} 字）：{out[:60]}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--daily-dir", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--pi-bin", default="pi")
    args = ap.parse_args()

    pi_bin = args.pi_bin
    if not Path(pi_bin).exists():
        found = shutil.which(pi_bin)
        if not found:
            print(f"✗ 找不到 pi：{pi_bin}")
            return 1
        pi_bin = found

    daily = Path(args.daily_dir)
    notes = sorted(daily.glob("*/*_结构化笔记.md"))
    if not notes:
        print("无笔记，跳过")
        return 0

    cache_file = daily / ".tldr.json"
    cache: dict = {}
    if cache_file.is_file():
        try:
            cache = json.loads(cache_file.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    tasks = []
    for p in notes:
        m = re.search(r"\[([A-Za-z0-9_-]{6,})\]$", p.parent.name)
        vid = m.group(1) if m else ""
        if not vid or vid.startswith("UC") or "Decoding Finance" in p.parent.name:
            continue
        if isinstance(cache.get(vid), dict) and cache[vid].get("tldr"):
            print(f"跳过已有: {vid}")
            continue
        txt = p.read_text(encoding="utf-8")
        title = (re.search(r"^# 结构化笔记｜(.+)", txt, re.M) or [None, p.parent.name])[1]
        tasks.append((vid, title, extract_core(txt)))
    if not tasks:
        print("无待生成 TL;DR")
        return 0
    if args.limit > 0:
        tasks = tasks[: args.limit]
    model = os.environ.get("PI_MODEL", "")
    print(f"待生成 {len(tasks)} 条 TL;DR（pi -p{', model=' + model if model else ''}）...")

    failed = 0
    for vid, title, core in tasks:
        print(f"\n=== {vid} {title[:30]} ===")
        try:
            line = generate_one(pi_bin, model, title, core, args.timeout)
            cache[vid] = {"title": title, "tldr": line}
            cache_file.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"✓ {line}")
        except Exception as e:  # noqa: BLE001 — 单条失败不中断
            print(f"✗ 失败 {vid}: {e}")
            failed += 1
    if failed:
        print(f"\n⚠ {failed}/{len(tasks)} 条失败（下次重试）")
        return 1
    print("\n全部完成")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
