#!/usr/bin/env python3
"""Resolve daily output directory."""
import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="Date YYYYMMDD")
    parser.add_argument("--ensure", action="store_true", help="Create directory")
    args = parser.parse_args()

    # Find data root: look for content_paths.json
    cwd = Path.cwd()
    # Also handle being called from any subdirectory
    search = cwd
    for _ in range(5):
        if (search / "content_paths.json").exists():
            data_root = search
            break
        search = search.parent
    else:
        data_root = cwd

    config = json.loads((data_root / "content_paths.json").read_text(encoding="utf-8"))
    daily_dir = config.get("daily_dir", "daily")

    from datetime import datetime
    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now().strftime("%Y%m%d")

    out = data_root / daily_dir / date_str
    if args.ensure:
        out.mkdir(parents=True, exist_ok=True)
    print(str(out))

if __name__ == "__main__":
    raise SystemExit(main())
