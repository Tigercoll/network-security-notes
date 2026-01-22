"""Add <!--more--> tag to Day files."""
from __future__ import annotations

from pathlib import Path


def add_more_tag(file_path: Path) -> None:
    """Add <!--more--> tag after 学习目标 section."""
    content = file_path.read_text(encoding="utf-8")

    if "<!--more-->" in content:
        print(f"SKIP: {file_path.name} already has <!--more--> tag")
        return

    patterns = [
        "## 学习内容",
        "## 学习内容（今日要点）",
        "## 学习内容（今日重点）",
        "## 本周知识地图",
        "## 本周知识点回顾",
        "## 一、",
        "## 一.",
        "## 今日重点",
    ]

    for pattern in patterns:
        if pattern in content:
            new_content = content.replace(pattern, f"<!--more-->\n\n{pattern}", 1)
            file_path.write_text(new_content, encoding="utf-8")
            print(f"DONE: {file_path.name} added <!--more--> before '{pattern}'")
            return

    print(f"SKIP: {file_path.name} no matching section found")


def main() -> int:
    """Add <!--more--> tag to all Day files."""
    root = Path(__file__).resolve().parents[1]
    daily_dir = root / "daily"

    day_files = sorted(daily_dir.glob("Day*.md"))

    for day_file in day_files:
        add_more_tag(day_file)

    return 0


if __name__ == "__main__":
    exit(main())
