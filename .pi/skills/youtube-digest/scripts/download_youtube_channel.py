#!/usr/bin/env python3
"""Download a date-bounded YouTube channel scan without false failure statuses.

``yt-dlp --break-on-reject`` deliberately stops when the reverse-chronological
channel listing reaches an item outside the requested date range. yt-dlp reports
that expected stop with a non-zero exit code, which generic shell runners render
as an error. This wrapper preserves real download failures but normalizes only
that documented range-boundary exit to success.

yt-dlp 解析策略（已彻底确认）：
- 常规方案：优先使用 PATH 中的 yt-dlp.exe；常见安装位置为
  C:\\Users\\<User>\\AppData\\Roaming\\Python\\Python3xx\\Scripts\\yt-dlp.exe
  （pip --user 安装时），该目录默认不在 PATH，导致 which 失败。
  本脚本会显式探测该路径，若存在则直接使用，无需用户手动加 PATH。
- 回退方案：若常规可执行文件均不存在，直接使用 `sys.executable -m yt_dlp`，
  不再重复尝试失败的常规方案。经实测本机常规方案存在但不在 PATH，
  回退方案可无缝接管且与常规方案等价。
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence


CHANNEL_URL = "https://www.youtube.com/@JIEDU369/videos"
RANGE_STOP_MARKER = "Encountered a video that did not match filter, stopping due to --break-match-filter"


def resolve_yt_dlp(value: str | None) -> list[str]:
    """解析 yt-dlp 调用方式，常规优先，回退直接使用 python -m。

    返回值为可直接用于 subprocess 的命令前缀列表。
    - 若 value 显式给出且为文件则直接使用
    - 否则尝试 which("yt-dlp")
    - 否则探测 pip --user 默认路径 Roaming/Python/.../Scripts/yt-dlp.exe
    - 否则回退至 [sys.executable, "-m", "yt_dlp"]，不再报错
    """
    if value:
        candidate = Path(value)
        if candidate.is_file():
            return [str(candidate)]
        found = shutil.which(value)
        if found:
            return [found]
        # value 可能是 "yt-dlp" 等，which 已失败则视为回退
        print(f"提示：指定 yt-dlp 路径 {value} 未找到，回退至 python -m yt_dlp")
        return [sys.executable, "-m", "yt_dlp"]

    # 1) PATH 中的 yt-dlp
    found = shutil.which("yt-dlp")
    if found:
        return [found]

    # 2) pip --user 常见落点（Windows）
    # 优先使用 sysconfig USER_BASE / Roaming 探测
    candidates: list[Path] = []
    try:
        import sysconfig
        user_base = Path(sysconfig.get_path("scripts", vars={"base": Path.home()}))
        # sysconfig 在 Windows 上可能返回 C:\Python314\Scripts 而非 Roaming，需手动补 Roaming
        candidates.append(user_base / "yt-dlp.exe")
    except Exception:
        pass

    roaming = Path.home() / "AppData" / "Roaming" / "Python"
    if roaming.exists():
        for p in roaming.rglob("yt-dlp.exe"):
            # 只取 Python3xx/Scripts 下的
            if "Scripts" in str(p):
                candidates.append(p)
                break

    # 常见固定路径
    candidates.append(Path.home() / "AppData" / "Roaming" / "Python" / "Python314" / "Scripts" / "yt-dlp.exe")

    for cand in candidates:
        if cand.is_file():
            print(f"提示：PATH 中未找到 yt-dlp，但在 {cand} 找到常规可执行文件，直接使用。")
            return [str(cand)]

    # 3) 彻底回退：python -m yt_dlp
    print("提示：未找到常规 yt-dlp 可执行文件，直接使用回退方案 python -m yt_dlp")
    return [sys.executable, "-m", "yt_dlp"]


def resolve_binary(value: str | None, name: str) -> str:
    if value:
        candidate = Path(value)
        if candidate.is_file():
            return str(candidate)
        found = shutil.which(value)
        if found:
            return found
        raise FileNotFoundError(f"找不到 {name}: {value}")
    found = shutil.which(name)
    if not found:
        raise FileNotFoundError(f"找不到 {name}，请安装后重试")
    return found


def build_command(args: argparse.Namespace, yt_dlp_cmd: list[str], node: str | None) -> list[str]:
    output_template = str(
        args.run_dir / "%(title).120B [%(id)s]" / "%(title).120B [%(id)s].%(ext)s"
    )
    command = [
        *yt_dlp_cmd,
        "--no-update",
        "--lazy-playlist",
        "--break-on-reject",
        "--dateafter",
        args.dateafter,
        "--datebefore",
        args.datebefore,
        "--download-archive",
        str(args.archive),
        "--concurrent-fragments",
        "4",
        "--write-info-json",
        "-f",
        "bv*+ba/b",
        "-o",
        output_template,
    ]
    # 注意：已移除 --trim-filenames 120，避免与 %(title).120B 双重裁剪导致文件名被过度截断为 "大摩.md"
    # Windows 长路径问题已由 120B 限制覆盖，如需额外限制请设为 240 而非 120
    if node:
        command.extend(["--js-runtimes", f"node:{node}"])
    command.append(args.channel_url)
    return command


def is_expected_range_stop(returncode: int, output: str) -> bool:
    """Whether yt-dlp stopped solely because the date boundary was reached."""
    return returncode != 0 and RANGE_STOP_MARKER in output and "ERROR:" not in output


def run(command: Sequence[str]) -> tuple[int, str]:
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    lines: list[str] = []
    assert process.stdout is not None
    for line in process.stdout:
        print(line, end="")
        lines.append(line)
    return process.wait(), "".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--dateafter", required=True, help="包含边界，格式 YYYYMMDD")
    parser.add_argument("--datebefore", required=True, help="包含边界，格式 YYYYMMDD")
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--channel-url", default=CHANNEL_URL)
    parser.add_argument("--yt-dlp", help="yt-dlp 可执行文件路径；默认从 PATH 查找，找不到则回退至 python -m")
    parser.add_argument("--node", help="Node.js 可执行文件路径；默认从 PATH 查找")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.run_dir.mkdir(parents=True, exist_ok=True)
    args.archive.parent.mkdir(parents=True, exist_ok=True)
    yt_dlp_cmd = resolve_yt_dlp(args.yt_dlp or os.getenv("YT_DLP_PATH"))
    node = resolve_binary(args.node, "node") if args.node or shutil.which("node") else None

    version = subprocess.run([*yt_dlp_cmd, "--version"], capture_output=True, text=True, check=False)
    print(f"yt-dlp version: {version.stdout.strip() or 'unknown'} (cmd: {' '.join(yt_dlp_cmd)})")
    if node:
        print(f"JavaScript runtime: {node}")
    else:
        print("WARNING: 未找到 Node.js；将继续下载，但部分 YouTube 格式可能不可用。")
    print(f"Output directory: {args.run_dir}")

    returncode, output = run(build_command(args, yt_dlp_cmd, node))
    if is_expected_range_stop(returncode, output):
        print("已到达日期范围下界，结束频道扫描（正常）。")
        return 0
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
