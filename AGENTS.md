# AGENTS.md - Agent Guidelines for Network Security Learning Repository

90-day network security curriculum with daily markdown files (Day001.md ~ Day090.md) and Python scripts for WeChat publishing.

---

## Build / Lint / Test Commands

### Linting
```bash
ruff check .                    # Run linter
ruff check --fix .               # Auto-fix
ruff check scripts/file.py       # Specific file
```

### Running Scripts
```bash
python scripts/generate_preview.py
python scripts/batch_update_days.py
python scripts/generate_daily_content.py [-s YYYY-MM-DD] [-o output_dir]
python test_publish.py           # WeChat (needs .env with credentials)
python scripts/day018_parse_log.py
python scripts/day020_probe_http.py <host> <port>
```

### Testing
No formal test suite. Run scripts directly to verify.

---

## Code Style Guidelines

### Imports
- Standard library → third-party → local
- Prefer `from __future__ import annotations` at top
- Use `pathlib.Path` for file ops

```python
from __future__ import annotations
import json
from pathlib import Path
```

### Type Hints
- Modern syntax: `list[str]` not `List[str]`
- Return types on all functions

```python
def parse_log(path: Path) -> list[dict[str, str]]: ...
```

### Naming
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Classes: `PascalCase`
- Files: `snake_case.py`

```python
ROOT = Path(__file__).resolve().parents[1]
def convert_markdown_to_html(file_path: str) -> str: ...
```

### Encoding
Always specify UTF-8:

```python
with open(filepath, "r", encoding="utf-8") as f: ...
path.read_text(encoding="utf-8")
path.write_text(content, encoding="utf-8")
```

### Error Handling
```python
try:
    with open(filepath, "r", encoding="utf-8") as f: ...
except FileNotFoundError:
    print(f"ERROR: file not found: {filepath}")
    return 1
```

### Docstrings
```python
"""Parse log and extract data.

Args:
    path: Path to log file.

Returns:
    List of dicts with Time, Level, Msg fields.
"""
```

### Markdown Files
- `daily/DayXXX.md` (3-digit zero-padded, UTF-8, Chinese)
- Sections: 学习目标, 学习内容, 实践任务, 巩固练习, 评估标准, 学习成果达成情况

---

## Environment

- Python 3.9+, venv at `.venv/` (`python -m venv .venv`)
- Dependencies: `pip install ruff pillow wordcloud markdown2 requests`
- Config: `.env` for WeChat credentials (DO NOT commit)

---

## Project Structure

```
Network Security/
├── daily/          # Day001.md ~ Day090.md
├── scripts/        # batch_update_days.py, generate_preview.py, day018_parse_log.py, etc.
├── plan/           # Roadmap
├── docs/           # Additional docs
├── test_publish.py # WeChat publishing
├── .env            # Credentials (DO NOT commit)
└── AGENTS.md
```

---

## Git Workflow

```
DayXXX: brief description (Chinese preferred)
- key point 1
- key point 2
```
- Main: `main`
- Features: `update-day022-content`

---

## Important Notes

1. **Security**: Educational/authorized testing only
2. **Chinese**: Most content is Chinese
3. **WeChat**: `test_publish.py` handles MD→HTML conversion
4. **No Tests**: Run scripts directly to verify
5. **Images**: Store in `daily/images/` or root `images/`
