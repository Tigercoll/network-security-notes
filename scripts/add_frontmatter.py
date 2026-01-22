"""Add frontmatter to Day files."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path


def generate_abbrlink(title: str) -> str:
    """Generate abbrlink from title."""
    return hashlib.md5(title.encode()).hexdigest()[:8]


def add_frontmatter(file_path: Path) -> None:
    """Add frontmatter to a Day file."""
    content = file_path.read_text(encoding="utf-8")

    if content.startswith("---"):
        print(f"SKIP: {file_path.name} already has frontmatter")
        return

    lines = content.split("\n")

    title = ""
    date = ""
    week = ""

    for line in lines:
        if line.startswith("# Day"):
            title = line.replace("#", "").strip()
        elif line.startswith("- 日期：") or line.startswith("- 日期:"):
            date = line.replace("- 日期：", "").replace("- 日期:", "").strip()
        elif line.startswith("- 周次：") or line.startswith("- 周次:"):
            week = line.replace("- 周次：", "").replace("- 周次:", "").strip()

    if not title or not date:
        print(f"SKIP: {file_path.name} missing title or date")
        return

    abbrlink = generate_abbrlink(title)

    frontmatter = f"""---
title: {title}
tags:
  - 网络
  - 安全
  - 学习计划
categories:
  - 网络安全
abbrlink: {abbrlink}
date: {date} 00:00:00
updated: {date} 00:00:00

---
"""

    new_content = frontmatter + content

    add_more_before = ["## 学习内容", "## 学习内容（今日要点）"]
    for pattern in add_more_before:
        if pattern in new_content:
            new_content = new_content.replace(pattern, f"<!--more-->\n\n{pattern}", 1)
            break

    file_path.write_text(new_content, encoding="utf-8")
    print(f"DONE: {file_path.name}")


def main() -> int:
    """Add frontmatter to all Day files."""
    root = Path(__file__).resolve().parents[1]
    daily_dir = root / "daily"

    day_files = sorted(daily_dir.glob("Day*.md"))

    for day_file in day_files:
        add_frontmatter(day_file)

    return 0


if __name__ == "__main__":
    exit(main())
