"""
Poll Gmail for replies that match the outreach subject template.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDENTIALS_PATH = Path(os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json"))
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))


def _gmail_auth_readonly():
    token_file = Path("token_readonly.json")
    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def fetch_replies(
    query: str = 'subject:("Seeking Room")',
    out_csv: str | Path = DATA_DIR / "responses.csv",
    max_results: int = 50,
) -> List[dict]:
    """Fetch Gmail replies matching a search query and write to CSV."""
    service = _gmail_auth_readonly()
    result = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    messages = result.get("messages", [])
    rows: List[dict] = []

    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"], format="full").execute()
        headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
        rows.append(
            {
                "id": message["id"],
                "from": headers.get("From", ""),
                "subject": headers.get("Subject", ""),
                "date": headers.get("Date", ""),
                "snippet": msg.get("snippet", ""),
            }
        )

    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"[replier] wrote {len(rows)} replies to {out_path}")
    return rows
