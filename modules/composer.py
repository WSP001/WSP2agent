"""
Compose outreach drafts (HTML + text) for curated contacts.
"""

from pathlib import Path
from typing import List, Union

import pandas as pd
import json


def compose_emails(
    top10_csv: Union[str, Path] = "data/top10_landlords.csv",
    out_file: Union[str, Path] = "data/top10_outreach_emails.json",
) -> List[dict]:
    df = pd.read_csv(top10_csv)
    drafts: List[dict] = []

    for idx, row in df.iterrows():
        org = row.get("organization") or "there"
        contact = org.split(",")[0]
        listing = row.get("url", "")

        subject = f"Seeking Room — {org}"
        body_text = (
            f"Hello {contact},\n\n"
            "My name is Robert and I'm looking for a quiet room in Winter Haven. "
            "I pay on time, keep shared areas tidy, and can offer 6–10 hrs/week of gardening "
            "or light home-care (I bring my own seeds) for a rent credit. "
            "Happy to share references and do a 30-day trial.\n\n"
            f"Listing/URL: {listing}\n"
            "Phone: 678-371-9527\n"
            "Email: worldseafood@gmail.com\n\n"
            "Thank you for considering me,\nRobert"
        )
        body_html = body_text.replace("\n", "<br/>")

        drafts.append(
            {
                "index": int(idx) + 1,
                "organization": org,
                "to": row.get("emails", ""),
                "subject": subject,
                "body_text": body_text,
                "body_html": body_html,
            }
        )

    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as handle:
        json.dump(drafts, handle, indent=2)
    print(f"[composer] wrote {len(drafts)} drafts to {out_path}")
    return drafts
