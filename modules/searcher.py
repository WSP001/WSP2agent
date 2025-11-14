"""
Search stage helper that wraps SerpApi queries for outreach discovery.
"""

import os
import time
from typing import Iterable, List, Optional

# serpapi==0.1.5 exposes GoogleSearch under serpapi.google_search,
# while some builds expose it at the top level. Try both.
try:  # pragma: no cover
    from serpapi import GoogleSearch
except Exception:  # noqa: BLE001 - fallback import path
    from serpapi.google_search import GoogleSearch

DEFAULT_QUERIES = [
    'Winter Haven FL "room for rent" "owner"',
    'Winter Haven FL "for rent by owner" "Winter Haven"',
    'Winter Haven FL "room for rent" "caretaker" OR "care taker"',
    'site:craigslist.org Winter Haven "room for rent"',
    'Winter Haven "home share" "Silvernest" OR "HomeShare Online"',
    'Winter Haven "Meals on Wheels" contact',
    'Winter Haven "senior center" contact email',
    'Winter Haven "public library" "community board" contact',
    'Winter Haven "for rent by owner" "Winter Haven"',
    'Winter Haven "room for rent" owner email',
]


def run_searches(
    api_key: Optional[str] = None,
    queries: Optional[Iterable[str]] = None,
    location: Optional[str] = None,
    num: int = 10,
    pause: float = 1.2,
) -> List[dict]:
    """
    Run SerpApi queries and return a de-duplicated list of organic results.
    """
    if api_key is None:
        api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_KEY not set in environment or .env")

    queries = list(queries or DEFAULT_QUERIES)
    location = location or "Winter Haven, Florida, United States"
    results: List[dict] = []

    for query in queries:
        params = {
            "engine": "google",
            "q": query,
            "location": location,
            "api_key": api_key,
            "num": num,
        }
        try:
            search = GoogleSearch(params)
            data = search.get_dict()
            org = data.get("organic_results") or []
            for item in org:
                results.append(
                    {
                        "title": item.get("title"),
                        "link": item.get("link"),
                        "snippet": item.get("snippet", ""),
                    }
                )
        except Exception as exc:  # noqa: BLE001 - diagnostics only
            print(f"[searcher] query failed: {query} -> {exc}")
        time.sleep(pause)

    # De-duplicate by URL to reduce scraping load.
    deduped: List[dict] = []
    seen_links = set()
    for item in results:
        link = item.get("link")
        if link and link not in seen_links:
            seen_links.add(link)
            deduped.append(item)
    return deduped
