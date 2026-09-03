#!/usr/bin/env python3
"""Transcribe newly downloaded 解读君 videos with bounded concurrency."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


MEDIA_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".webm",
    ".mov",
    ".m4v",
    ".avi",
    ".flv",
    ".wmv",
}


def write_status(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporary.replace(path)


def process_video(video_dir: Path, transcriber: Path) -> dict:
    info_files = list(video_dir.glob("*.info.json"))
    if not info_files:
        return {"dir": str(video_dir), "status": "skipped", "reason": "no_info_json"}

    info_path = info_files[0]
    info = json.loads(info_path.read_text(encoding="utf-8"))
    video_id = str(info.get("id") or "")
    title = str(info.get("title") or video_dir.name)
    upload_date = str(info.get("upload_date") or "")
    source_url = str(info.get("webpage_url") or info.get("original_url") or "")

    media_files = [
        item for item in video_dir.iterdir() if item.is_file() and item.suffix.lower() in MEDIA_EXTENSIONS
    ]
    if not media_files:
        return {
            "dir": str(video_dir),
            "id": video_id,
            "title": title,
            "status": "failed",
            "reason": "no_media_file",
        }

    media_path = max(media_files, key=lambda item: item.stat().st_size)
    # 修复：不再使用 media_path.stem（会因下载阶段双重裁剪被截为“大摩”），改用目录名确保 [ID] 后缀
    # 目录名形如 "标题 [ID]"，已包含正确标题与 ID，是最可靠的基准
    dir_name = video_dir.name
    # 规范化：若目录名已含 [ID]，直接用它；否则回退到 title [id]
    if video_id and re.search(rf"\[{re.escape(video_id)}\]$", dir_name):
        base_name = dir_name
    elif video_id:
        base_name = f"{title} [{video_id}]"
    else:
        base_name = media_path.stem

    # 清理非法字符仅保留 yt-dlp 已处理过的结果，直接使用即可
    markdown_path = video_dir / f"{base_name}.md"
    # 兼容旧截断产物：若已存在截断命名的 .md（如 大摩.md），优先视为已完成
    # 避免重复转写，同时在成功后会统一保留正确命名
    legacy_mds = [
        p for p in video_dir.glob("*.md")
        if p.is_file() and not p.name.endswith("_结构化笔记.md") and p.stat().st_size > 0
    ]
    # 若已存在正确命名的 md，直接跳过
    if markdown_path.exists() and markdown_path.stat().st_size > 0:
        return {
            "dir": str(video_dir),
            "id": video_id,
            "title": title,
            "status": "skipped",
            "reason": "markdown_exists",
            "markdown": str(markdown_path),
        }
    # 若存在旧截断 md 且不存在正确命名，视为已完成但需重命名以符合枚举规范
    if legacy_mds and not markdown_path.exists():
        # 选最大的那个旧 md
        legacy = max(legacy_mds, key=lambda p: p.stat().st_size)
        # 若旧 md 已包含有效转写（有 metadata 头），直接重命名
        try:
            content = legacy.read_text(encoding="utf-8")
            if "## 转写正文" in content and len(content) > 500:
                legacy.rename(markdown_path)
                return {
                    "dir": str(video_dir),
                    "id": video_id,
                    "title": title,
                    "status": "skipped",
                    "reason": "legacy_markdown_renamed",
                    "markdown": str(markdown_path),
                }
        except Exception:
            pass

    # 音频临时文件仍可用 stem 避免过长，但最终 md 用正确命名
    audio_path = video_dir / f"{media_path.stem}.mp3"

    try:
        ffmpeg_result = subprocess.run(
            [
                "ffmpeg",
                "-i",
                str(media_path),
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-b:a",
                "32k",
                str(audio_path),
                "-y",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if ffmpeg_result.returncode != 0 or not audio_path.exists():
            raise RuntimeError(
                f"ffmpeg failed ({ffmpeg_result.returncode}): "
                f"{ffmpeg_result.stderr[-1200:]}"
            )

        transcript_result = subprocess.run(
            [
                sys.executable,
                str(transcriber),
                "--file",
                str(audio_path),
                "--output",
                str(markdown_path),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if transcript_result.returncode != 0:
            raise RuntimeError(
                f"transcriber failed ({transcript_result.returncode}): "
                f"{(transcript_result.stdout + transcript_result.stderr)[-1600:]}"
            )
        if not markdown_path.exists() or markdown_path.stat().st_size == 0:
            raise RuntimeError("transcriber returned success but Markdown is empty")

        transcript = markdown_path.read_text(encoding="utf-8").strip()
        published = upload_date
        if len(upload_date) == 8 and upload_date.isdigit():
            published = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
        metadata = (
            f"# {title}\n\n"
            f"- **视频 ID：** {video_id}\n"
            f"- **发布日期：** {published}\n"
            f"- **来源：** {source_url}\n\n"
            f"## 转写正文\n\n"
        )
        markdown_path.write_text(metadata + transcript + "\n", encoding="utf-8")

        if markdown_path.stat().st_size < len(metadata.encode("utf-8")) + 10:
            raise RuntimeError("Markdown validation failed after metadata insertion")

        for item in video_dir.iterdir():
            if item.is_file() and item.suffix.lower() != ".md":
                item.unlink()
            # 清理旧截断 md（若同时存在）
            if item.is_file() and item != markdown_path and item.suffix == ".md" and not item.name.endswith("_结构化笔记.md"):
                # 保留正确命名的，其余旧 md 删除
                if item.name != markdown_path.name:
                    try:
                        item.unlink()
                    except Exception:
                        pass

        return {
            "dir": str(video_dir),
            "id": video_id,
            "title": title,
            "status": "success",
            "markdown": str(markdown_path),
            "size": markdown_path.stat().st_size,
        }
    except Exception as exc:
        return {
            "dir": str(video_dir),
            "id": video_id,
            "title": title,
            "status": "failed",
            "reason": str(exc),
            "traceback": traceback.format_exc(),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--transcriber", required=True, type=Path)
    parser.add_argument("--status-file", required=True, type=Path)
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    pattern = re.compile(r"\[[A-Za-z0-9_-]{6,}\]$")
    candidates = []
    for directory in args.run_dir.iterdir():
        if not directory.is_dir():
            continue
        if not pattern.search(directory.name):
            continue
        if not list(directory.glob("*.info.json")):
            continue
        # 排除 playlist 元数据目录：id 以 UC 开头（频道）或标题含 Decoding Finance
        m = re.search(r"\[([A-Za-z0-9_-]{6,})\]$", directory.name)
        vid = m.group(1) if m else ""
        if vid.startswith("UC") or vid.startswith("UCl"):
            continue
        if "Decoding Finance - Videos" in directory.name:
            continue
        # 必须至少有一个媒体文件才视为视频目录，否则 skip 而非 failed
        has_media = any(p.suffix.lower() in MEDIA_EXTENSIONS for p in directory.iterdir() if p.is_file())
        if not has_media:
            continue
        candidates.append(directory)
    payload = {
        "started_at": datetime.now().astimezone().isoformat(),
        "finished_at": None,
        "running": len(candidates),
        "results": [],
    }
    write_status(args.status_file, payload)

    with ThreadPoolExecutor(max_workers=min(max(args.workers, 1), 3)) as executor:
        futures = {
            executor.submit(process_video, directory, args.transcriber): directory
            for directory in candidates
        }
        for future in as_completed(futures):
            result = future.result()
            payload["results"].append(result)
            payload["running"] = len(candidates) - len(payload["results"])
            write_status(args.status_file, payload)

    payload["finished_at"] = datetime.now().astimezone().isoformat()
    write_status(args.status_file, payload)
    return 1 if any(item["status"] == "failed" for item in payload["results"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
