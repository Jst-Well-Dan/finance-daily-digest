#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
env_loader.py — 极简 .env 加载器（零依赖，自包含）。

为什么不用 python-dotenv：本项目的脚本会被 `run_daily.py` 以子进程、也会被
pi subagent 直接在任意 cwd 调用，多一个第三方依赖就多一个装不上的失败点。
本实现只支持 .env 的常用子集，够用且不会误伤。

支持语法:
    KEY=value
    KEY="value with spaces"      # 双引号内的 \\n \\t \\" 会被转义
    KEY='literal $value'         # 单引号内完全字面量
    export KEY=value             # 前缀 export 可有可无
    # 注释行、空行
    KEY=value   # 行尾注释（未加引号时生效）

查找顺序（第一个存在的生效，仅加载一次）：
    1. 调用方显式传入的 root 参数
    2. 环境变量 YOUTUBE_ENV_FILE 指向的文件
    3. 从当前文件向上逐级查找，找到仓库根（含 content_paths.json 或 .git）下的 .env

关键约定：**不覆盖已存在的环境变量**。这样命令行显式 `FOO=bar python x.py`
永远优先于 .env，便于临时试验，不会被文件悄悄盖掉。
"""
from __future__ import annotations

import os
import re
from pathlib import Path

_LOADED = False

_RE_DOUBLE = re.compile(r'\\([nrt"\\])')
_ESCAPES = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}


def _unescape_double(value: str) -> str:
    return _RE_DOUBLE.sub(lambda m: _ESCAPES[m.group(1)], value)


def _strip_inline_comment(value: str) -> str:
    """未加引号时，剥离 ` #` 起的行尾注释。"""
    idx = value.find(" #")
    if idx >= 0:
        return value[:idx].rstrip()
    idx = value.find("\t#")
    if idx >= 0:
        return value[:idx].rstrip()
    return value


def parse_dotenv(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if not key or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            quote = value[0]
            value = value[1:-1]
            if quote == '"':
                value = _unescape_double(value)
        else:
            value = _strip_inline_comment(value)
        out[key] = value
    return out


def find_repo_root(start: Path | None = None) -> Path | None:
    """向上找仓库根：优先认 content_paths.json，其次 .git。"""
    cur = (start or Path(__file__).resolve()).resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in [cur, *cur.parents]:
        if (candidate / "content_paths.json").is_file() or (candidate / ".git").exists():
            return candidate
    return None


def find_env_file(root: Path | None = None) -> Path | None:
    explicit = os.environ.get("YOUTUBE_ENV_FILE", "").strip()
    if explicit:
        p = Path(explicit).expanduser()
        if p.is_file():
            return p
    base = Path(root).resolve() if root else find_repo_root()
    if not base:
        return None
    p = base / ".env"
    return p if p.is_file() else None


def load_env(root: Path | None = None, *, override: bool = False, force: bool = False) -> Path | None:
    """加载 .env 到 os.environ。返回实际加载的文件路径（没找到则为 None）。

    默认幂等：同进程内重复调用只会真正加载一次（force=True 可强制重载）。
    默认不覆盖已有环境变量（override=True 可覆盖）。
    """
    global _LOADED
    if _LOADED and not force and not override:
        return find_env_file(root)
    path = find_env_file(root)
    if not path:
        _LOADED = True
        return None
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError:
        return None
    for key, value in parse_dotenv(text).items():
        if override or key not in os.environ:
            os.environ[key] = value
    _LOADED = True
    return path


def get(key: str, default: str = "", *, root: Path | None = None) -> str:
    """读环境变量（先确保 .env 已加载）。空字符串视为未设置。"""
    load_env(root)
    return (os.environ.get(key) or "").strip() or default


def get_chain(*keys: str, default: str = "", root: Path | None = None) -> str:
    """按顺序取第一个非空值，全部为空则返回 default。用于模型优先级回落。"""
    load_env(root)
    for key in keys:
        value = (os.environ.get(key) or "").strip()
        if value:
            return value
    return default


if __name__ == "__main__":  # 便于人工自检：python scripts/env_loader.py
    found = load_env()
    print(f".env: {found or '（未找到）'}")
    for k in sorted(os.environ):
        if k.startswith(("YOUTUBE_", "SILICONFLOW_")):
            v = os.environ[k]
            if "KEY" in k and v:
                v = v[:6] + "…" + v[-4:] if len(v) > 12 else "***"
            print(f"  {k}={v}")
