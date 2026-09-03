#!/usr/bin/env python3
"""Fallback: 原样拼接各笔记的## 1. 核心结论为每日总结（无 LLM 时可用）"""
import pathlib, re, sys
daily = pathlib.Path(sys.argv[sys.argv.index("--daily-dir")+1]) if "--daily-dir" in sys.argv else pathlib.Path("daily")/ "20260903"
notes = sorted(daily.glob("*/*_结构化笔记.md"))
if not notes: print("no notes"); sys.exit(0)
out = ["# 解读君视频摘要\n"]
for i,p in enumerate(notes,1):
    txt=p.read_text(encoding="utf-8")
    title=(re.search(r"^# 结构化笔记｜(.+)",txt,re.M) or [None, p.parent.name])[1]
    m=re.search(r"## 1\. 核心结论(.*?)(?=\n## \d+\.)",txt,re.S)
    core=m.group(0).strip() if m else txt[:3000]
    # 去掉标题行，保留核心结论内容
    core = re.sub(r"^## 1\. 核心结论\s*\n","",core).strip()
    out.append(f"## {i}. {title}\n\n{core}\n")
target = daily / f"{daily.name}_解读君视频总结.md"
target.write_text("\n".join(out), encoding="utf-8")
print(f"Wrote {target}")
