"""
Worker module: consumes sandbox packages and executes sends.
"""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List

from .gmailer import create_message_with_attachment, gmail_auth

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
SANDBOX = DATA_DIR / "sandbox"
OUTBOX = SANDBOX / "outbox"
SENT = SANDBOX / "sent"
FAILED = SANDBOX / "failed"
DB_PATH = DATA_DIR / "packages.db"
SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL", "worldseafood@gmail.com")


def _ensure_dirs() -> None:
    for directory in (OUTBOX, SENT, FAILED):
        directory.mkdir(parents=True, exist_ok=True)


def _update_status(pkg_id: int, status: str, send_result: str | None = None) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE packages SET status=?, updated_at=?, send_result=? WHERE id=?",
            (status, datetime.utcnow().isoformat(), send_result or "", pkg_id),
        )
        conn.commit()


def _pick_email(pkg: dict) -> str | None:
    raw = pkg.get("emails") or ""
    for email in raw.split(";"):
        candidate = email.strip()
        if candidate:
            return candidate
    return None


def _move_package_file(src: Path, destination_folder: Path) -> Path:
    destination_folder.mkdir(parents=True, exist_ok=True)
    target = destination_folder / src.name
    src.replace(target)
    return target


def _send_package(pkg: dict, dry_run: bool, service=None):
    recipient = _pick_email(pkg)
    if not recipient:
        return False, "missing_email"

    message = create_message_with_attachment(
        SENDER_EMAIL,
        recipient,
        pkg.get("subject", "Opportunity"),
        pkg.get("body_html", ""),
        Path(pkg.get("pdf")) if pkg.get("pdf") else None,
    )
    if dry_run:
        preview = (
            f"DRY RUN → to={recipient} subject='{pkg.get('subject')}' "
            f"attach='{pkg.get('pdf', '')}'"
        )
        return True, preview

    if service is None:
        service = gmail_auth()
    response = service.users().messages().send(userId="me", body=message).execute()
    return True, response.get("id")


def poll_and_send(dry_run: bool = True) -> List[str]:
    """
    Process all JSON packages in the outbox.
    Returns the list of processed package filenames.
    """
    _ensure_dirs()
    processed: List[str] = []
    service = None if dry_run else gmail_auth()

    for package_path in sorted(OUTBOX.glob("package_*.json")):
        with package_path.open("r", encoding="utf-8") as handle:
            pkg = json.load(handle)
        pkg_id = pkg.get("id")
        print(f"[worker] processing package {pkg_id}")

        try:
            ok, result = _send_package(pkg, dry_run=dry_run, service=service)
            if ok:
                destination = SENT if dry_run else SENT
                _move_package_file(package_path, destination)
                _update_status(pkg_id, "dry_run" if dry_run else "sent", result)
                print(f"[worker] success: {result}")
            else:
                _move_package_file(package_path, FAILED)
                _update_status(pkg_id, "failed", result)
                print(f"[worker] failed: {result}")
        except Exception as exc:  # noqa: BLE001 - log and continue
            _move_package_file(package_path, FAILED)
            _update_status(pkg_id, "failed", repr(exc))
            print(f"[worker] error: {exc}")
        processed.append(package_path.name)

    if not processed:
        print("[worker] no packages found.")
    return processed


if __name__ == "__main__":
    poll_and_send(dry_run=True)
