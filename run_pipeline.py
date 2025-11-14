#!/usr/bin/env python3
"""
run_pipeline.py
Orchestrates the WSP2AGENT pipeline. This is a safe, manual-gate controller.
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))


def safe_import(module_name):
    try:
        module = __import__(module_name, fromlist=["*"])
        return module
    except Exception as e:  # noqa: BLE001 - show friendly warning
        print(f"[WARN] Module {module_name} not found or errored: {e}")
        return None


def main(dry_run=True):
    print("WSP2AGENT pipeline starting. Dry run =", dry_run)
    # 1) Searches
    searcher = safe_import("modules.searcher")
    if searcher:
        print("Running search stage...")
        try:
            results = searcher.run_searches()
            print(f"Collected {len(results)} search hits.")
            # Optionally save search_results.json
            import json

            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(DATA_DIR / "search_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        except Exception as e:  # noqa: BLE001 - show friendly warning
            print("Search stage failed:", e)
    else:
        print("searcher module missing; skipping search stage.")

    # 2) Scrape
    scraper = safe_import("modules.scraper")
    if scraper:
        print("Running scrape stage...")
        try:
            scraper.scrape_results(
                DATA_DIR / "search_results.json",
                out_csv=DATA_DIR / "contacts_raw.csv",
            )
            print("Scrape stage complete: data/contacts_raw.csv")
        except Exception as e:  # noqa: BLE001 - show friendly warning
            print("Scrape stage failed:", e)
    else:
        print("scraper module missing; skipping scrape stage.")

    # 3) Curate
    curator = safe_import("modules.curator")
    if curator:
        print("Running curate stage...")
        try:
            curator.curate_contacts(
                DATA_DIR / "contacts_raw.csv",
                out_csv=DATA_DIR / "top10_landlords.csv",
            )
            print("Curate stage complete: data/top10_landlords.csv")
        except Exception as e:  # noqa: BLE001 - show friendly warning
            print("Curate stage failed:", e)
    else:
        print("curator module missing; skipping curate stage.")

    print("\n=== APPROVAL CHECKPOINT ===")
    print("Please review `data/top10_landlords.csv`. Approve a small test batch (1-3 entries) before sending.")
    if dry_run:
        print("Dry run enabled: stopping after approval checkpoint.")
        return

    approved = input("Have you approved a test batch (y/N)? ").strip().lower()
    if approved != "y":
        print("Human approval not received. Exiting.")
        return

    # 4) PDFs
    pdfs = safe_import("modules.pdfs")
    if pdfs:
        print("Generating personal PDFs...")
        try:
            pdfs.make_personal_pdfs(DATA_DIR / "top10_landlords.csv", out_dir=Path("."))
            print("PDFs generated.")
        except Exception as e:  # noqa: BLE001 - show friendly warning
            print("PDF stage failed:", e)
    else:
        print("pdfs module missing; skipping PDF stage.")

    # 5) Compose & Send
    composer = safe_import("modules.composer")
    gmailer = safe_import("modules.gmailer")
    if composer:
        print("Composing email bodies...")
        try:
            composer.compose_emails(
                DATA_DIR / "top10_landlords.csv",
                out_file=DATA_DIR / "top10_outreach_emails.txt",
            )
            print("Email drafts ready at data/top10_outreach_emails.txt")
        except Exception as e:  # noqa: BLE001 - show friendly warning
            print("Compose stage failed:", e)
    else:
        print("composer module missing; skipping compose stage.")

    if gmailer:
        print("Running email send stage (gmailer.send_approved_emails will be invoked).")
        try:
            gmailer.send_approved_emails(DATA_DIR / "top10_landlords.csv")
        except Exception as e:  # noqa: BLE001 - show friendly warning
            print("Gmail send stage failed:", e)
    else:
        print("gmailer module missing; skipping send stage.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WSP2AGENT pipeline controller")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Stop at approval checkpoint",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
