#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_daily.py — 本地一键运行「解读君视频日报」全链路，随后自动提交并推送 GitHub。

流程: ① 增量下载 → ② 转写(SiliconFlow) → ③ pi 结构化笔记(LLM) → ④ 确定性总结 → ⑤ HTML → ⑥ git push
用法:
    python run_daily.py                      # 今天; 全量笔记
    python run_daily.py --date 20260903      # 指定日
    python run_daily.py --notes-limit 1      # 本次最多生成 1 篇笔记（验证用）
    python run_daily.py --skip-push          # 只生成不推送
    python run_daily.py --cookies cookies.txt  # 显式指定 YouTube cookies（可省，本地一般无需）

环境变量（均可由 shell 提供）:
    SILICONFLOW_API_KEY   转写必需（已配置）
    PI_MODEL              笔记 LLM 模型，默认 muse-spark-1.2-contributor
    HF_TOKEN / OPENAI_API_KEY / ANTHROPIC_API_KEY  按需

退出码: 0=完全成功, 2=部分步骤失败(已容错), 1=致命错误
"""
import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
SKILLS = ROOT / ".pi" / "skills"

DEFAULT_PI_MODEL = "muse-spark-1.2-contributor"


def sh(cmd, title, check=False, env_extra=None, allow_fail_ok=False):
    """Run a command; print title. Returns (returncode, stdout+stderr tail)."""
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYYMMDD，默认今天")
    ap.add_argument("--notes-limit", type=int, default=0, help="本次最多生成笔记篇数（0=不限）")
    ap.add_argument("--skip-push", action="store_true", help="只生成不外推")
    ap.add_argument("--cookies", type=Path, help="cookies.txt 路径（可选）")
    args = ap.parse_args()

    date_str = args.date or datetime.now().strftime("%Y%m%d")
    dd = ROOT / "daily" / date_str
    if not dd.exists():
        dd.mkdir(parents=True, exist_ok=True)
    print(f"◆ 每日日期: {date_str}  目录: {dd}")

    # ① 增量下载（14 天窗口；本地无云端反爬压力，失败也容错继续）
    dl_cmd = [
        sys.executable, str(SKILLS / "youtube-digest" / "scripts" / "download_youtube_channel.py"),
        "--run-dir", str(dd),
        "--dateafter", _date_days_ago(14),
        "--datebefore", _date_days_ago(-1),
        "--archive", str(SKILLS / "youtube-digest" / ".youtube_download_archive.txt"),
    ]
    if args.cookies and args.cookies.is_file():
        dl_cmd += ["--cookies", str(args.cookies)]
    sh(dl_cmd, "① 增量下载频道视频（14 天窗口）", allow_fail_ok=True)

    # ② 转写（已转写跳过；单条失败降级）
    sh([
        sys.executable, str(SKILLS / "youtube-digest" / "scripts" / "process_video_transcripts.py"),
        "--run-dir", str(dd),
        "--transcriber", str(SKILLS / "video-transcriber" / "scripts" / "transcribe_siliconflow.py"),
        "--status-file", str(dd / ".transcribe_status.json"),
        "--workers", "3",
    ], "② 转写新视频（SiliconFlow）", allow_fail_ok=True)

    # ③ pi 结构化笔记（LLM；默认 muse-spark-1.2-contributor，可用 --notes-limit 限量验证）
    env_notes = {"PI_MODEL": os.environ.get("PI_MODEL", DEFAULT_PI_MODEL)}
    notes_cmd = [
        "node", str(ROOT / "scripts" / "generate_notes_via_pi.mjs"),
        "--daily-dir", str(dd),
    ]
    if args.notes_limit > 0:
        notes_cmd += ["--limit", str(args.notes_limit)]
    sh(notes_cmd, f"③ 生成结构化笔记（pi, model={env_notes['PI_MODEL']}）",
       env_extra=env_notes, allow_fail_ok=True)

    # ④ 确定性每日总结（原样复制核心结论）
    note_dirs = list(dd.glob("*/*_结构化笔记.md"))
    if note_dirs:
        sh([
            sys.executable, str(ROOT / "scripts" / "build_daily_summary.py"),
            "--daily-dir", str(dd),
        ], "④ 生成每日总结（确定性拼接）", allow_fail_ok=True)
    else:
        print("\n◆ 跳过 ④：无结构化笔记，无法聚合总结")

    # ⑤ 构建 HTML（金融经纬多日生成器）
    sh([sys.executable, str(ROOT / "scripts" / "build_reader.py")], "⑤ 构建 HTML（全部历史页）")

    # ⑥ git add & commit & push
    if not args.skip_push:
        status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
        if not status.stdout.strip():
            print("\n◆ 无任何变化，无需推送")
            return 0
        sh(["git", "add", "-A"], "⑥ git add")
        sh(["git", "commit", "-m", f"daily: {date_str} local update"], "⑥ git commit")
        sh(["git", "push", "origin", "main"], "⑥ git push 到 GitHub（Pages 自动更新）", check=True)

    # 结果摘要：统计转写/笔记数量
    trans = list(dd.glob("*/*.md"))
    notes = note_dirs
    print(f"\n{'='*72}\n✔ 完成。当日 {date_str}：转写稿 {len(trans)} 篇，结构化笔记 {len(notes)} 篇")
    print("打开: file://" + str((ROOT / "index.html").resolve()).replace("\\", "/"))
    return 0


def _date_days_ago(days: int) -> str:
    from datetime import timedelta
    return (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")


if __name__ == "__main__":
    raise SystemExit(main())