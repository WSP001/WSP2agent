"""
Curator stage: score scraped contacts and surface top candidates for review.
"""

from pathlib import Path
from typing import List

import pandas as pd

POSITIVE_KEYWORDS = [
    "owner",
    "owner-occupied",
    "for rent by owner",
    "caretaker",
    "care taker",
    "home share",
    "homeshare",
    "silvernest",
    "senior",
    "elder",
    "retire",
    "meals on wheels",
    "library",
    "church",
]
NEGATIVE_KEYWORDS = [
    "apartment",
    "property management",
    "leasing",
    "apartments.com",
    "realtor",
    "zillow",
    "management company",
]


def _score_text(value: str) -> int:
    score = 0
    text = (value or "").lower()
    for kw in POSITIVE_KEYWORDS:
        if kw in text:
            score += 3
    for kw in NEGATIVE_KEYWORDS:
        if kw in text:
            score -= 2
    return score


def curate_contacts(
    input_csv: str | Path = "data/contacts_raw.csv",
    out_csv: str | Path = "data/top10_landlords.csv",
    top_n: int = 10,
) -> pd.DataFrame:
    """Produce a scored shortlist CSV for human approval."""
    input_path = Path(input_csv)
    if not input_path.exists():
        raise FileNotFoundError(f"{input_path} not found; run scraper first.")

    df = pd.read_csv(input_path)
    for column in ("organization", "snippet", "url", "emails"):
        if column not in df.columns:
            df[column] = ""

    df["combined"] = (
        df["organization"].fillna("")
        + " "
        + df["snippet"].fillna("")
        + " "
        + df["url"].fillna("")
    )
    df["score"] = df["combined"].apply(_score_text)
    df["has_email"] = df["emails"].fillna("").astype(bool)
    df["score"] += df["has_email"].astype(int) * 2

    shortlisted = df.sort_values("score", ascending=False).head(top_n).copy()
    shortlisted["approved"] = False
    shortlisted = shortlisted[
        ["organization", "url", "emails", "phones", "snippet", "score", "approved"]
    ]

    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    shortlisted.to_csv(out_path, index=False)
    print(f"[curator] wrote top {len(shortlisted)} rows to {out_path}")
    return shortlisted
