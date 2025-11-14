"""
Broker module: converts curated CSV rows into sandboxed send packages.
"""

from __future__ import annotations

import csv
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from .utils import slugify_filename

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
SANDBOX = DATA_DIR / "sandbox"
OUTBOX = SANDBOX / "outbox"
SENT = SANDBOX / "sent"
FAILED = SANDBOX / "failed"
LOGS = SANDBOX / "logs"
DB_PATH = DATA_DIR / "packages.db"
EMAIL_DRAFTS_PATH = DATA_DIR / "top10_outreach_emails.json"


def _ensure_dirs() -> None:
    for directory in (OUTBOX, SENT, FAILED, LOGS):
        directory.mkdir(parents=True, exist_ok=True)


def _init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                org TEXT,
                contact_name TEXT,
                emails TEXT,
                phones TEXT,
                pdf TEXT,
                subject TEXT,
                body_text TEXT,
                body_html TEXT,
                listing_url TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                send_result TEXT
            );
            """
        )
        conn.commit()


def _load_drafts() -> Dict[int, dict]:
    if not EMAIL_DRAFTS_PATH.exists():
        return {}
    with EMAIL_DRAFTS_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return {entry.get("index"): entry for entry in data}


def _find_pdf_for_row(index: int, org: str, pdf_dir: Path) -> str:
    candidates = list(pdf_dir.glob(f"personal_flyer_{index}_*.pdf"))
    if not candidates:
        slug = slugify_filename(org)
        candidates = list(pdf_dir.glob(f"*{slug}*.pdf"))
    return str(candidates[0]) if candidates else ""


def _insert_package(pkg: dict) -> int:
    now = datetime.utcnow().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO packages (
                org, contact_name, emails, phones, pdf,
                subject, body_text, body_html, listing_url,
                status, created_at, updated_at, send_result
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pkg["org"],
                pkg["contact_name"],
                pkg["emails"],
                pkg["phones"],
                pkg["pdf"],
                pkg["subject"],
                pkg["body_text"],
                pkg["body_html"],
                pkg["listing_url"],
                "pending",
                now,
                now,
                "",
            ),
        )
        conn.commit()
        return cursor.lastrowid


def _write_package_json(pkg_id: int, payload: dict) -> Path:
    payload_with_id = dict(payload)
    payload_with_id["id"] = pkg_id
    out_path = OUTBOX / f"package_{pkg_id}.json"
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(payload_with_id, handle, indent=2)
    return out_path


def create_packages_from_csv(
    top10_csv: str | Path = DATA_DIR / "top10_landlords.csv",
    pdf_dir: str | Path = ".",
    only_approved: bool = True,
) -> List[Tuple[int, Path]]:
    """
    Convert curated rows into sandbox packages (JSON + sqlite row).
    """
    _ensure_dirs()
    _init_db()
    pdf_dir = Path(pdf_dir)
    drafts_by_index = _load_drafts()
    created: List[Tuple[int, Path]] = []

    with open(top10_csv, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader, start=1):
            approved = str(row.get("approved", "")).strip().lower() in {"true", "1", "yes"}
            if only_approved and not approved:
                continue

            draft = drafts_by_index.get(idx)
            org = row.get("organization", "") or "Contact"
            listing_url = row.get("url", "")
            subject = (draft and draft.get("subject")) or f"Seeking Room — {org}"
            body_text = (draft and draft.get("body_text")) or (
                f"Hello {org},\n\n"
                "My name is Robert and I'm looking for a room in Winter Haven. "
                "I can offer 6–10 hours/week of gardening or light caretaking "
                "in exchange for a rent credit. References and a 30-day trial available.\n\n"
                f"Listing: {listing_url}\n"
                "Phone: 678-371-9527\nEmail: worldseafood@gmail.com\n"
            )
            body_html = (draft and draft.get("body_html")) or body_text.replace("\n", "<br/>")

            payload = {
                "org": org,
                "contact_name": row.get("contact_name") or org,
                "emails": row.get("emails", ""),
                "phones": row.get("phones", ""),
                "pdf": _find_pdf_for_row(idx, org, pdf_dir=pdf_dir),
                "subject": subject,
                "body_text": body_text,
                "body_html": body_html,
                "listing_url": listing_url,
            }
            pkg_id = _insert_package(payload)
            pkg_path = _write_package_json(pkg_id, payload)
            created.append((pkg_id, pkg_path))

    print(f"[broker] created {len(created)} packages in {OUTBOX}")
    return created


if __name__ == "__main__":
    create_packages_from_csv()
