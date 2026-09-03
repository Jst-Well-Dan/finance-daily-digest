#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_daily.py — 本地一键运行「解读君视频日报」全链路，随后自动提交并推送 GitHub。

流程: ① 增量下载 → ①.5 按【发布日期(upload_date)】归档分发到 daily/YYYYMMDD
      → ② 转写(补全部缺档日期) → ③ pi 结构化笔记 → ④ 确定性总结 → ⑤ HTML → ⑥ git push

特点：支持【隔几天补一次】。上次更新是 9/3，今天 9/5 运行，将自动把 9/4、9/5 的视频
按发布日期落进各自 daily 目录，并逐日补转写/笔记/总结，全部日期一起生成。

用法:
    python run_daily.py                      # 今天; 全量笔记
    python run_daily.py --notes-limit 1      # 本次最多生成 1 篇笔记（验证用）
    python run_daily.py --skip-push          # 只生成不推送
    python run_daily.py --cookies cookies.txt  # 显式指定 YouTube cookies（可省）

环境变量:
    SILICONFLOW_API_KEY   转写必需（已配置）
    PI_MODEL              笔记 LLM 模型，默认 muse-spark-1.3-contributor

退出码: 0=完全成功, 2=部分步骤失败(已容错), 1=致命错误
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
SKILLS = ROOT / ".pi" / "skills"
DAILY = ROOT / "daily"

DEFAULT_PI_MODEL = "muse-spark-1.3-contributor"
VID_DIR_RE = re.compile(r"^(.+)\s*\[([A-Za-z0-9_-]{6,})\]$")


def sh(cmd, title, check=False, env_extra=None, allow_fail_ok=False):
    print(f"\n{'='*72}\n▶ {title}\n  $ {' '.join(str(c) for c in cmd)}")
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    try:
        p = subprocess.run(cmd, cwd=ROOT, env=env)
    except FileNotFoundError as e:
        print(f"  ✗ 找不到可执行文件: {e}")
        return 127, ""
    if p.returncode != 0 and check and not allow_fail_ok:
        print(f"  ✗ 失败 (exit {p.returncode})")
        sys.exit(1)
    if p.returncode != 0:
        print(f"  ⚠ 非零退出码 {p.returncode}" + ("（已按容错策略继续）" if allow_fail_ok else ""))
    return p.returncode, ""


def existing_daily_dates() -> set[str]:
    """daily/ 下已有的 YYYYMMDD 目录。"""
    return {p.name for p in DAILY.iterdir() if p.is_dir() and re.fullmatch(r"\d{8}", p.name)}


def get_upload_date(d: Path) -> str:
    """优先读 info.json 的 upload_date；已转写目录无 info.json 时，从转写稿 metadata 的「发布日期」提取。"""
    info_files = list(d.glob("*.info.json"))
    if info_files:
        try:
            info = json.loads(info_files[0].read_text(encoding="utf-8"))
            up = str(info.get("upload_date") or "")
            if re.fullmatch(r"\d{8}", up):
                return up
        except Exception:
            pass
    for md in d.glob("*.md"):
        if md.name.endswith("_结构化笔记.md"):
            continue
        try:
            txt = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        m = re.search(r"发布日期[：:]\s*\**\s*(\d{4})-(\d{2})-(\d{2})", txt)
        if m:
            return m.group(1) + m.group(2) + m.group(3)
    return ""


def distribute_by_upload_date(dd: Path) -> list[Path]:
    """
    把 dd 下刚下载/已有的视频目录按 upload_date 分发到 daily/YYYYMMDD。
    返回：本次涉及的所有日期目录名。
    """
    moved: dict[str, Path] = {}
    for d in sorted(dd.iterdir()):
        if not d.is_dir():
            continue
        m = VID_DIR_RE.match(d.name)
        if not m or m.group(2).startswith("UC"):
            continue
        upload = get_upload_date(d)
        if re.fullmatch(r"\d{8}", upload):
            target = DAILY / upload
        else:
            target = dd  # 无日期信息则留在下载日
        if target != d.parent:
            target.mkdir(parents=True, exist_ok=True)
            dest = target / d.name
            if dest.exists():
                # 目标已存在同名目录（重复下载）→ 保现有，删除本次冗余
                import shutil
                shutil.rmtree(d, ignore_errors=True)
            else:
                d.rename(dest)
            print(f"  ↳ {d.name[:44]}… → daily/{target.name}/")
        moved[target.name] = target
    moved[dd.name] = dd
    return sorted(moved.keys())


def run_tx_notes_summary(date_dirs: list[str], notes_limit: int) -> None:
    """对每个日期目录依次：转写 → 笔记 → 总结（全部幂等，可重复跑）。"""
    env_notes = {"PI_MODEL": os.environ.get("PI_MODEL", DEFAULT_PI_MODEL)}
    for idx, date_name in enumerate(date_dirs):
        d = DAILY / date_name
        print(f"\n{'#'*72}\n# 处理日期 {date_name}  ({d})")
        # ② 转写（已转写自动跳过）
        sh([
            sys.executable, str(SKILLS / "youtube-digest" / "scripts" / "process_video_transcripts.py"),
            "--run-dir", str(d),
            "--transcriber", str(SKILLS / "video-transcriber" / "scripts" / "transcribe_siliconflow.py"),
            "--status-file", str(d / ".transcribe_status.json"),
            "--workers", "3",
        ], f"② 转写 {date_name}（SiliconFlow）", allow_fail_ok=True)

        # ③ 结构化笔记：limit>0 时只对第一个日期目录限量生效，其余日期跳过（防意外消耗额度）
        if notes_limit > 0 and idx > 0:
            print(f"  ※ --notes-limit 只作用于首个日期，跳过 {date_name} 的笔记生成")
        else:
            notes_cmd = [
                "node", str(ROOT / "scripts" / "generate_notes_via_pi.mjs"),
                "--daily-dir", str(d),
            ]
            if notes_limit > 0:
                notes_cmd += ["--limit", str(notes_limit)]
            sh(notes_cmd, f"③ 生成结构化笔记 {date_name}（pi, model={env_notes['PI_MODEL']}）",
               env_extra=env_notes, allow_fail_ok=True)

        # ④ 每日总结（有笔记才生成）
        if list(d.glob("*/*_结构化笔记.md")):
            sh([
                sys.executable, str(ROOT / "scripts" / "build_daily_summary.py"),
                "--daily-dir", str(d),
            ], f"④ 生成每日总结 {date_name}", allow_fail_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYYMMDD，默认今天（仅作下载暂存目录起点）")
    ap.add_argument("--notes-limit", type=int, default=0, help="本次最多生成笔记篇数（0=不限）")
    ap.add_argument("--skip-push", action="store_true", help="只生成不外推")
    ap.add_argument("--cookies", type=Path, help="cookies.txt 路径（可选）")
    args = ap.parse_args()

    date_str = args.date or datetime.now().strftime("%Y%m%d")
    dd = DAILY / date_str
    if not dd.exists():
        dd.mkdir(parents=True, exist_ok=True)
    print(f"◆ 今天: {date_str}  下载暂存目录: {dd}")

    # 上次更新日 = 已有日期目录中的最大值（如 20260903）
    existing = existing_daily_dates()
    last_updated = max(existing) if existing else None
    print(f"◆ 上次更新日: {last_updated or '（无，全量初始化）'}")

    # ① 增量下载：窗口从「上次更新日-2 天」到今天（保 1 天余量），不再固定 14 天
    if last_updated:
        last_dt = datetime.strptime(last_updated, "%Y%m%d")
        window_start = (last_dt - timedelta(days=2)).strftime("%Y%m%d")
    else:
        window_start = _date_days_ago(14)
    dl_cmd = [
        sys.executable, str(SKILLS / "youtube-digest" / "scripts" / "download_youtube_channel.py"),
        "--run-dir", str(dd),
        "--dateafter", window_start,
        "--datebefore", _date_days_ago(-1),
        "--archive", str(SKILLS / "youtube-digest" / ".youtube_download_archive.txt"),
    ]
    if args.cookies and args.cookies.is_file():
        dl_cmd += ["--cookies", str(args.cookies)]
    sh(dl_cmd, f"① 增量下载频道视频（窗口 {window_start} → {_date_days_ago(-1)}）", allow_fail_ok=True)

    # ①.5 按 upload_date 归档分发（核心：隔几天补时自动补齐中间日期）
    date_dirs = distribute_by_upload_date(dd)
    print(f"◆ 需处理的日期目录: {date_dirs}")

    # ②③④ 逐日转写 / 笔记 / 总结
    run_tx_notes_summary(date_dirs, args.notes_limit)

    # ⑤ 构建 HTML（全部历史页，含漏掉的日子）
    sh([sys.executable, str(ROOT / "scripts" / "build_reader.py")], "⑤ 构建 HTML（全部历史页）")

    # ⑥ git add & commit & push
    if not args.skip_push:
        status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
        if not status.stdout.strip():
            print("\n◆ 无任何变化，无需推送")
            return 0
        sh(["git", "add", "-A"], "⑥ git add")
        sh(["git", "commit", "-m", f"daily: {date_str} local update (补 {len(date_dirs)} 日)"], "⑥ git commit")
        sh(["git", "push", "origin", "main"], "⑥ git push 到 GitHub（Pages 自动更新）", check=True)

    total_notes = 0
    for dn in date_dirs:
        total_notes += len(list((DAILY / dn).glob("*/*_结构化笔记.md")))
    print(f"\n{'='*72}\n✔ 完成。共处理 {len(date_dirs)} 个日期目录，结构化笔记 {total_notes} 篇")
    print("打开: file://" + str((ROOT / "index.html").resolve()).replace("\\", "/"))
    return 0


def _date_days_ago(days: int) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")


if __name__ == "__main__":
    raise SystemExit(main())