#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""确定性每日总结：原样拼接各笔记 ## 1. 核心结论。
- 标题链向本页全文锚点（## N. [标题](#note-{vid})），根页摘录会剥掉链接。
- 拼入 .tldr.json 缓存中的一句话提炼（缺失则跳过，不阻塞）。
- 把 `**结论N：**` 加粗段统一改写为数字列表，与 `1.` 写法渲染一致。
"""
import json
import pathlib
import re
import sys

daily = pathlib.Path(sys.argv[sys.argv.index("--daily-dir") + 1]) if "--daily-dir" in sys.argv else pathlib.Path("daily") / "20260903"
notes = sorted(daily.glob("*/*_结构化笔记.md"))
if not notes:
    print("no notes")
    sys.exit(0)

tldr: dict = {}
cache = daily / ".tldr.json"
if cache.is_file():
    try:
        tldr = json.loads(cache.read_text(encoding="utf-8"))
    except Exception:
        tldr = {}


def vid_of(p: pathlib.Path) -> str:
    m = re.search(r"\[([A-Za-z0-9_-]{6,})\]$", p.parent.name)
    return m.group(1) if m else ""


def norm_conclusions(core: str) -> str:
    """`**结论N：正文**` 独占段 → `N. 正文`，与数字列表写法统一渲染（编号即序号）。"""
    return re.sub(
        r"^\*\*(结论(\d+)：)(.*?)\*\*[ \t]*$",
        lambda m: f"{m.group(2)}. {m.group(3).strip()}",
        core, flags=re.M,
    )


out = ["# 解读君视频摘要\n"]
for i, p in enumerate(notes, 1):
    txt = p.read_text(encoding="utf-8")
    title = (re.search(r"^# 结构化笔记｜(.+)", txt, re.M) or [None, p.parent.name])[1]
    m = re.search(r"## 1\. 核心结论(.*?)(?=\n## \d+\.)", txt, re.S)
    core = m.group(0).strip() if m else txt[:3000]
    # 去掉标题行（含模型自带的括号说明），保留核心结论内容
    core = re.sub(r"^## 1\. 核心结论[^\n]*\n?", "", core, count=1).strip()
    core = norm_conclusions(core)
    vid = vid_of(p)
    out.append(f"## {i}. [{title}](#note-{vid})\n")
    entry = tldr.get(vid)
    line = (entry or {}).get("tldr", "") if isinstance(entry, dict) else ""
    if line:
        out.append(f"\n> 一句话：{line}\n")
    out.append(f"\n{core}\n")
target = daily / f"{daily.name}_解读君视频总结.md"
target.write_text("\n".join(out), encoding="utf-8")
print(f"Wrote {target}")
