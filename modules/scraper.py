"""
Scraper utilities to fetch result links and extract basic contact info.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Iterable, List, Tuple

import requests
from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}")
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0 Safari/537.36"
)


def page_emails_phones(url: str, timeout: int = 12) -> Tuple[List[str], List[str]]:
    """Fetch a single page and return discovered email + phone lists."""
    try:
        resp = requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
    except Exception as exc:  # noqa: BLE001 - stage should continue
        print(f"[scraper] fetch failed for {url}: {exc}")
        return [], []

    text = resp.text
    emails = {
        email
        for email in EMAIL_RE.findall(text)
        if not email.lower().startswith(("no-reply", "noreply", "donotreply"))
    }
    phones = set(PHONE_RE.findall(text))

    # Attempt to grab contact info from anchor tags for extra context.
    soup = BeautifulSoup(text, "lxml")
    for anchor in soup.select("a[href^='mailto:']"):
        mail = anchor.get("href", "").replace("mailto:", "").strip()
        if mail and not mail.lower().startswith(("no-reply", "noreply", "donotreply")):
            emails.add(mail)
    return sorted(emails), sorted(phones)


def _load_search_results(source: Iterable | str | Path) -> Iterable[dict]:
    if isinstance(source, (list, tuple)):
        return source
    path = Path(source)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def scrape_results(
    search_results_path_or_list,
    out_csv: str | Path = "data/contacts_raw.csv",
) -> List[dict]:
    """Read search results, fetch each page, and write a CSV for curation."""
    results = list(_load_search_results(search_results_path_or_list))
    out_path = Path(out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rows: List[dict] = []

    for entry in results:
        url = entry.get("link") or entry.get("url")
        title = entry.get("title", "")
        snippet = entry.get("snippet", "")
        if not url:
            continue
        emails, phones = page_emails_phones(url)
        rows.append(
            {
                "organization": title,
                "url": url,
                "emails": ";".join(emails),
                "phones": ";".join(phones),
                "snippet": snippet,
            }
        )

    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["organization", "url", "emails", "phones", "snippet"]
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"[scraper] wrote {len(rows)} rows to {out_path}")
    return rows
