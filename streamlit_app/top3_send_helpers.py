from __future__ import annotations
import json, os
from pathlib import Path
from typing import List, Dict, Any

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))

def read_json_utf8(path: Path) -> Any:
    """Read JSON file with UTF-8 encoding to avoid cp1252 errors on Windows."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None

def load_top3_exports() -> List[Dict[str, Any]]:
    """
    Load automation-ready top-3 drafts from data/top3_emails_export.json.
    Returns empty list if file doesn't exist or can't be parsed.
    """
    js = read_json_utf8(DATA_DIR / "top3_emails_export.json")
    if isinstance(js, list):
        return js
    return []

def has_oauth_token(repo_root: Path = Path(".")) -> bool:
    """Check if Gmail OAuth token.json exists in common locations."""
    return (repo_root / "token.json").exists() or (repo_root / "modules" / "token.json").exists()
