"""
WSP2AGENT Production Contact Enricher
Selenium-based scraper with retry logic, structured logging, and data integrity
"""

import argparse
import hashlib
import random
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from selenium.webdriver.common.by import By

from modules.config import get_config
from modules.data_schema import (
    atomic_write_csv,
    cleanup_old_backups,
    load_csv_with_schema,
    TOP10_SCHEMA
)
from modules.logger import create_logger
from modules.selenium_driver_v2 import (
    build_chrome_driver,
    ElementNotFoundError,
    safe_click,
    safe_find
)

# Regex patterns for contact extraction
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_PATTERN = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

# Garbage email domains to filter out
GARBAGE_DOMAINS = {'dh.vl', 'example.com', 'test.com'}


def is_valid_email(email: str) -> bool:
    """Check if email is valid (not garbage)."""
    domain = email.split('@')[-1].lower()
    return domain not in GARBAGE_DOMAINS


def extract_contacts_from_page(
    driver,
    url: str,
    selectors: Dict[str, str],
    logger
) -> Tuple[List[str], List[str]]:
    """
    Extract emails and phone numbers from a listing page.
    
    Args:
        driver: Selenium WebDriver instance
        url: Listing URL to scrape
        selectors: Dict of CSS selectors for reply button, body, etc.
        logger: StructuredLogger instance
    
    Returns:
        Tuple of (emails_list, phones_list)
    """
    emails = set()
    phones = set()
    
    try:
        # Navigate to listing
        driver.get(url)
        time.sleep(0.5)  # Brief pause for page load
        
        # Try to click reply button to reveal hidden contacts
        reply_selector = selectors.get('reply_button')
        if reply_selector:
            try:
                clicked = safe_click(driver, By.CSS_SELECTOR, reply_selector, timeout=3)
                if clicked:
                    time.sleep(1)  # Wait for contact reveal
                    logger.info("reply_button_clicked", url=url)
            except Exception:
                pass  # Reply button not critical
        
        # Extract from page body
        body_selector = selectors.get('listing_body', 'body')
        try:
            body_element = safe_find(driver, By.CSS_SELECTOR, body_selector, timeout=5)
            if body_element:
                text = body_element.text
                
                # Find emails
                found_emails = EMAIL_PATTERN.findall(text)
                emails.update([e for e in found_emails if is_valid_email(e)])
                
                # Find phones
                found_phones = PHONE_PATTERN.findall(text)
                phones.update(found_phones)
        
        except ElementNotFoundError:
            logger.warn("listing_body_not_found", url=url)
    
    except Exception as e:
        logger.error("page_extraction_failed", url=url, error=str(e))
    
    return list(emails), list(phones)


def enrich_single_listing(
    driver,
    row: pd.Series,
    selectors: Dict[str, str],
    logger,
    max_retries: int = 2
) -> Dict[str, any]:
    """
    Enrich a single listing with retry logic.
    
    Args:
        driver: Selenium WebDriver
        row: CSV row as pandas Series
        selectors: CSS selectors dict
        logger: StructuredLogger
        max_retries: Number of retry attempts
    
    Returns:
        Dict with enrichment results and status
    """
    url = row.get('url', '')
    config = get_config()
    
    for attempt in range(max_retries + 1):
        try:
            emails, phones = extract_contacts_from_page(driver, url, selectors, logger)
            
            # Generate unique ID from URL
            row_id = hashlib.md5(url.encode()).hexdigest()[:12]
            
            return {
                'id': row_id,
                'organization': row.get('organization', ''),
                'url': url,
                'emails': '; '.join(emails) if emails else row.get('emails', ''),
                'phones': '; '.join(phones) if phones else row.get('phones', ''),
                'score': row.get('score', 0.0),
                'approved': row.get('approved', False),
                'scrape_status': 'success' if (emails or phones) else 'no_contacts',
                'scrape_error': '',
                'last_scraped_at': datetime.now().isoformat()
            }
        
        except Exception as e:
            if attempt < max_retries:
                backoff = config.retry_backoff_seconds * (attempt + 1)
                logger.warn(
                    "retry_attempt",
                    url=url,
                    attempt=attempt + 1,
                    backoff_seconds=backoff,
                    error=str(e)
                )
                time.sleep(backoff)
            else:
                # Final failure
                logger.error("listing_failed_after_retries", url=url, error=str(e))
                row_id = hashlib.md5(url.encode()).hexdigest()[:12]
                
                return {
                    'id': row_id,
                    'organization': row.get('organization', ''),
                    'url': url,
                    'emails': row.get('emails', ''),
                    'phones': row.get('phones', ''),
                    'score': row.get('score', 0.0),
                    'approved': row.get('approved', False),
                    'scrape_status': 'failed',
                    'scrape_error': str(e)[:200],  # Limit error length
                    'last_scraped_at': datetime.now().isoformat()
                }


def enrich_csv_contacts(
    csv_path: Path,
    headless: bool = True,
    max_rows: Optional[int] = None,
    dry_run: bool = False,
    env: str = "dev"
) -> Dict[str, int]:
    """
    Enrich CSV with Selenium scraping (production-grade).
    
    Args:
        csv_path: Path to CSV file
        headless: Run browser in headless mode
        max_rows: Limit number of rows to process (None = all)
        dry_run: Don't write results to CSV
        env: Environment name (dev/staging/prod)
    
    Returns:
        Dict with stats: processed, success, failed, skipped
    """
    # Setup
    config = get_config(env=env)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger = create_logger(log_dir=str(config.log_dir), run_id=run_id, env=env)
    
    logger.info(
        "enrichment_started",
        csv_path=str(csv_path),
        headless=headless,
        max_rows=max_rows,
        dry_run=dry_run,
        env=env
    )
    
    # Load CSV with schema validation
    df = load_csv_with_schema(csv_path, schema=TOP10_SCHEMA)
    
    if max_rows:
        df = df.head(max_rows)
    
    logger.info("csv_loaded", rows=len(df))
    
    # Get selectors from config
    selectors = config.selectors.get('craigslist', {})
    
    # Build WebDriver
    driver = build_chrome_driver(headless=headless)
    
    try:
        enriched_rows = []
        
        for idx, row in df.iterrows():
            logger.record_processed()
            
            # Check if already enriched (has contacts)
            if row.get('emails') or row.get('phones'):
                logger.record_skipped()
                logger.info("listing_skipped_has_contacts", url=row.get('url', ''))
                enriched_rows.append(row.to_dict())
                continue
            
            # Enrich listing with retries
            result = enrich_single_listing(
                driver,
                row,
                selectors,
                logger,
                max_retries=config.max_retries
            )
            
            # Track results
            if result['scrape_status'] == 'success':
                logger.record_success()
            elif result['scrape_status'] == 'failed':
                logger.record_failed(result['scrape_error'])
            else:
                logger.record_skipped()
            
            enriched_rows.append(result)
            
            # Politeness delay (randomized)
            if idx < len(df) - 1:  # Don't delay after last row
                delay = random.uniform(
                    config.politeness_delay_min,
                    config.politeness_delay_max
                )
                time.sleep(delay)
        
        # Write results
        enriched_df = pd.DataFrame(enriched_rows)
        
        if dry_run:
            logger.info("dry_run_complete", message="No CSV written")
            print("\n🧪 DRY RUN - Results preview:")
            print(enriched_df[['organization', 'emails', 'phones', 'scrape_status']].head())
        else:
            atomic_write_csv(
                enriched_df,
                csv_path,
                backup=True,
                validate=True,
                schema=TOP10_SCHEMA
            )
            cleanup_old_backups(csv_path, retention_days=7)
            logger.info("csv_written", path=str(csv_path))
    
    finally:
        driver.quit()
        stats = logger.finalize()
    
    # Print summary
    print("\n✅ Enrichment Complete")
    print("=" * 50)
    print(f"Run ID: {run_id}")
    print(f"Processed: {stats['processed']}")
    print(f"Success: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped: {stats['skipped']}")
    print(f"Log: logs/run_report_{run_id}.json")
    
    return stats


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="WSP2AGENT Contact Enricher (Production)"
    )
    parser.add_argument(
        '--csv',
        type=str,
        default='data/top10_landlords.csv',
        help='Path to CSV file'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )
    parser.add_argument(
        '--visible',
        action='store_true',
        help='Run browser in visible mode (for debugging)'
    )
    parser.add_argument(
        '--max-rows',
        type=int,
        help='Limit number of rows to process'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview results without writing CSV'
    )
    parser.add_argument(
        '--env',
        type=str,
        choices=['dev', 'staging', 'prod'],
        default='dev',
        help='Environment profile'
    )
    
    args = parser.parse_args()
    
    # Determine headless mode
    headless = args.headless or (not args.visible)
    
    enrich_csv_contacts(
        csv_path=Path(args.csv),
        headless=headless,
        max_rows=args.max_rows,
        dry_run=args.dry_run,
        env=args.env
    )


if __name__ == "__main__":
    main()
