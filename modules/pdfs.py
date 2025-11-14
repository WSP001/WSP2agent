"""
Generate lightweight personalized flyers for each curated contact.
"""

from pathlib import Path
from typing import Union

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from .utils import slugify_filename


def make_personal_pdfs(
    top10_csv: Union[str, Path] = "data/top10_landlords.csv",
    out_dir: Union[str, Path] = ".",
    contact_name: str = "Robert",
) -> bool:
    """Create one flyer per approved contact using reportlab."""
    df = pd.read_csv(top10_csv)
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title = ParagraphStyle("title", parent=styles["Heading1"], fontSize=16, spaceAfter=12)
    body = styles["BodyText"]

    for idx, row in df.iterrows():
        org = row.get("organization") or "Contact"
        url = row.get("url", "")
        notes = row.get("snippet", "")
        filename = out_path / f"personal_flyer_{int(idx) + 1}_{slugify_filename(org)}.pdf"

        doc = SimpleDocTemplate(
            str(filename),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        story = [
            Paragraph("Seeking a Room to Rent — Reliable Tenant", title),
            Spacer(1, 8),
            Paragraph(
                (
                    f"Hello {org},<br/><br/>My name is {contact_name}. "
                    "I am seeking a private room in Winter Haven ($400–$700/mo) and can offer "
                    "6–10 hrs/week of gardening or light home-care (I bring my own seeds) in exchange for a rent credit. "
                    "I pay on time, keep shared areas tidy, and can provide references plus a 30-day trial.<br/><br/>"
                    f"Listing/URL: {url}<br/>"
                    f"Notes: {notes}<br/><br/>"
                    f"Contact: {contact_name} — 678-371-9527 • worldseafood@gmail.com<br/><br/>"
                    "Happy to support with light webmaster/tech help if that is useful."
                ),
                body,
            ),
        ]
        doc.build(story)
        print(f"[pdfs] created {filename}")
    return True
