#!/usr/bin/env python3
"""Orchestrate parallel transcription for video directories.

Workflow per video:
1. Extract 16 kHz mono 32 kbps MP3 via ffmpeg.
2. Call transcribe_siliconflow.py to produce Markdown.
3. Prepend metadata header (title, video id, upload date, source URL).
4. Clean up non-Markdown files in the directory.

Max 3 concurrent video directories per the skill rules.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]  # 数据根 = 本脚本上溯 4 级
TRANSCRIBE = ROOT / ".pi/skills/video-transcriber/scripts/transcribe_siliconflow.py"


def log(msg: str) -> None:
    ts = dt.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def find_video_and_info(directory: Path) -> tuple[Path, Path]:
    info_path = None
    video_path = None
    for f in directory.iterdir():
        if f.suffix == ".json" and f.stem.endswith(".info"):
            info_path = f
        elif f.suffix in {".mp4", ".mkv", ".webm", ".m4v"} and not f.stem.startswith("."):
            video_path = f
    if not info_path or not video_path:
        raise RuntimeError(f"missing .info.json or video file in {directory}")
    return video_path, info_path


def extract_audio(video: Path, mp3: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(video),
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-b:a", "32k",
        str(mp3),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_transcribe(mp3: Path, md: Path) -> None:
    cmd = [
        sys.executable,
        str(TRANSCRIBE),
        "--file", str(mp3),
        "--output", str(md),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"transcribe failed: {res.stderr or res.stdout}")


def write_metadata(md: Path, info: dict, title: str, video_id: str) -> None:
    upload_date = info.get("upload_date", "")
    if upload_date and len(upload_date) == 8:
        upload_date_fmt = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    else:
        upload_date_fmt = upload_date or "未知"
    source_url = info.get("webpage_url") or f"https://www.youtube.com/watch?v={video_id}"
    channel = info.get("channel") or info.get("uploader") or ""
    duration = info.get("duration")
    body = md.read_text(encoding="utf-8")
    header = (
        f"# {title}\n\n"
        f"> 来源元信息\n"
        f"> - 视频 ID：{video_id}\n"
        f"> - 频道：{channel}\n"
        f"> - 发布日期：{upload_date_fmt}\n"
        f"> - 时长（秒）：{duration if duration is not None else '未知'}\n"
        f"> - 链接：{source_url}\n\n"
    )
    md.write_text(header + body, encoding="utf-8")


def cleanup(directory: Path, keep_md: Path) -> None:
    for f in directory.iterdir():
        if f == keep_md:
            continue
        try:
            f.unlink()
        except IsADirectoryError:
            pass


def process_one(directory: Path) -> tuple[str, str]:
    log(f"start: {directory.name}")
    try:
        # Skip if already has a non-structured markdown
        for f in directory.iterdir():
            if f.suffix == ".md" and not f.name.endswith("_结构化笔记.md"):
                log(f"skip (already has md): {directory.name}")
                return (directory.name, "skipped")

        video, info_path = find_video_and_info(directory)
        info = json.loads(info_path.read_text(encoding="utf-8"))
        title = info.get("title", directory.name)
        video_id = info.get("id") or directory.name.rsplit("[", 1)[-1].rstrip("]")

        mp3 = directory / (video.stem + ".mp3")
        md = directory / (video.stem + ".md")

        # 1. extract audio
        log(f"  [{directory.name}] extracting audio")
        extract_audio(video, mp3)

        # 2. transcribe
        log(f"  [{directory.name}] transcribing")
        run_transcribe(mp3, md)

        # 3. write metadata header
        write_metadata(md, info, title, video_id)

        # 4. cleanup non-md files
        cleanup(directory, md)
        log(f"done: {directory.name}")
        return (directory.name, "ok")
    except Exception as e:
        log(f"FAIL: {directory.name} -> {e}")
        return (directory.name, f"failed: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="date directory")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    base = ROOT / args.dir
    candidates = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        # Only process directories that contain .info.json + a video
        has_info = any(f.suffix == ".json" and f.stem.endswith(".info") for f in child.iterdir())
        if not has_info:
            continue
        candidates.append(child)

    log(f"videos to process: {len(candidates)}")
    results = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for res in pool.map(process_one, candidates):
            results.append(res)
    log(f"finished. results: {results}")
    ok = sum(1 for _, s in results if s == "ok")
    fail = sum(1 for _, s in results if s.startswith("failed"))
    skip = sum(1 for _, s in results if s == "skipped")
    log(f"summary: ok={ok} skipped={skip} failed={fail}")
    if fail:
        for name, status in results:
            if status.startswith("failed"):
                print(f"  FAILED: {name} -> {status}")


if __name__ == "__main__":
    main()