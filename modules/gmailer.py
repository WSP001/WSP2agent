"""
Gmail helper functions for manual, approved sending.
"""

from __future__ import annotations

import base64
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
CREDENTIALS_PATH = Path(os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json"))
SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL", "worldseafood@gmail.com")


def gmail_auth():
    """Authenticate and return a Gmail API service client."""
    creds = None
    token_file = Path("token.json")
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


def create_message_with_attachment(
    sender: str,
    to: str,
    subject: str,
    body_html: str,
    attachment_path: Path | None = None,
):
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    message.attach(MIMEText(body_html, "html"))

    if attachment_path and attachment_path.exists():
        with attachment_path.open("rb") as handle:
            part = MIMEApplication(handle.read(), Name=attachment_path.name)
        part["Content-Disposition"] = f'attachment; filename="{attachment_path.name}"'
        message.attach(part)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}


def _split_email(value: str) -> str | None:
    if not value:
        return None
    for candidate in value.split(";"):
        candidate = candidate.strip()
        if candidate:
            return candidate
    return None


def send_approved_emails(
    top10_csv: str | Path = DATA_DIR / "top10_landlords.csv",
    dry_run: bool = True,
) -> List[tuple]:
    """
    Send emails for rows flagged approved=True.
    dry_run=True prints actions without sending.
    """
    df = pd.read_csv(top10_csv)
    approved = df[df.get("approved", False) == True]  # noqa: E712 - pandas bool
    approved_count = len(approved)
    print(f"[gmailer] {approved_count} rows approved.")
    if approved_count == 0:
        return []

    if approved_count > 3:
        confirm = input(
            f"[gmailer] {approved_count} emails marked approved. Send anyway? (y/N): "
        ).strip()
        if confirm.lower() != "y":
            print("[gmailer] Aborting send due to safety gate.")
            return []

    service = None if dry_run else gmail_auth()
    sent_results: List[tuple] = []

    for idx, row in approved.iterrows():
        recipient = _split_email(row.get("emails", ""))
        if not recipient:
            print(f"[gmailer] skipping {row.get('organization')} (no email).")
            continue

        subject = f"Seeking Room — {row.get('organization', 'Winter Haven tenant')}"
        body_html = (
            f"<p>Hello {row.get('organization','there')},</p>"
            "<p>My name is Robert. I'm seeking a private room in Winter Haven and can offer "
            "6–10 hrs/week of gardening or light caretaker support (I bring my own seeds) "
            "for a rent credit. I pay on time, respect shared spaces, and can provide references "
            "plus a 30-day trial.</p>"
            f"<p>Listing/URL: {row.get('url','')}</p>"
            "<p>Phone: 678-371-9527<br/>Email: worldseafood@gmail.com</p>"
            "<p>Thank you for your consideration,<br/>Robert</p>"
        )

        attachment = Path(
            f"personal_flyer_{int(idx) + 1}_{row.get('organization','').replace(' ', '_')}.pdf"
        )

        if dry_run:
            print(f"[gmailer] DRY RUN → {recipient} | subj='{subject}' | attach='{attachment.name}'")
            sent_results.append((recipient, subject, "DRY_RUN"))
            continue

        message = create_message_with_attachment(
            SENDER_EMAIL, recipient, subject, body_html, attachment if attachment.exists() else None
        )
        response = (
            service.users().messages().send(userId="me", body=message).execute()
        )
        print(f"[gmailer] sent to {recipient} (msg id {response.get('id')})")
        sent_results.append((recipient, subject, response.get("id")))
    return sent_results
