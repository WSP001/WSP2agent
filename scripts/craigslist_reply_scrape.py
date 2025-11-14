"""
Selenium-based scraper to extract emails from Craigslist reply buttons.

Usage:
    python scripts/craigslist_reply_scrape.py <craigslist_url>

Requirements:
    pip install selenium
    Download ChromeDriver: https://chromedriver.chromium.org/
    Place chromedriver.exe in PATH or same directory
"""

import re
import sys
import time
from pathlib import Path

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    print("ERROR: selenium not installed. Run: pip install selenium")
    sys.exit(1)


def extract_email_from_reply(url: str, timeout: int = 10) -> dict:
    """
    Open a Craigslist listing, click reply button, extract email/phone.
    
    Returns:
        dict with keys: url, email, phone, success, error
    """
    result = {
        "url": url,
        "email": None,
        "phone": None,
        "success": False,
        "error": None
    }
    
    driver = None
    try:
        # Set up headless Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Wait for page to load
        time.sleep(2)
        
        # Find and click reply button
        try:
            reply_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "reply-button"))
            )
            reply_button.click()
            time.sleep(2)
        except Exception:
            # Try alternative selectors
            try:
                reply_button = driver.find_element(By.LINK_TEXT, "reply")
                reply_button.click()
                time.sleep(2)
            except Exception:
                result["error"] = "Could not find reply button"
                return result
        
        # Wait for reply modal/section to appear
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "reply-email"))
            )
        except Exception:
            pass
        
        # Extract email addresses from page source
        page_source = driver.page_source
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, page_source)
        
        # Filter out common non-contact emails
        excluded = {"craigslist.org", "example.com", "test.com"}
        valid_emails = [
            email for email in emails
            if not any(domain in email.lower() for domain in excluded)
        ]
        
        if valid_emails:
            result["email"] = ";".join(set(valid_emails))
            result["success"] = True
        
        # Extract phone numbers (US format)
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phones = re.findall(phone_pattern, page_source)
        
        if phones:
            result["phone"] = ";".join(set(phones))
            result["success"] = True
        
        if not result["email"] and not result["phone"]:
            result["error"] = "No contact info found in reply section"
        
    except Exception as e:
        result["error"] = str(e)
    
    finally:
        if driver:
            driver.quit()
    
    return result


def enrich_csv_with_craigslist_scrape(csv_path: Path, output_path: Path = None):
    """
    Read CSV with URLs, scrape Craigslist reply pages, enrich with emails/phones.
    """
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    output_path = output_path or csv_path
    
    print(f"[scraper] Processing {len(df)} rows from {csv_path}")
    
    for idx, row in df.iterrows():
        url = row.get("url", "")
        
        # Only scrape Craigslist URLs with missing emails
        if "craigslist.org" not in url.lower():
            continue
        
        if row.get("emails"):
            print(f"[{idx+1}] Skipping {url[:50]} (already has email)")
            continue
        
        print(f"[{idx+1}] Scraping {url[:50]}...")
        result = extract_email_from_reply(url)
        
        if result["success"]:
            if result["email"]:
                df.at[idx, "emails"] = result["email"]
                print(f"    ✓ Found email: {result['email']}")
            if result["phone"]:
                df.at[idx, "phones"] = result["phone"]
                print(f"    ✓ Found phone: {result['phone']}")
        else:
            print(f"    ✗ {result['error']}")
        
        # Be polite - rate limit
        time.sleep(3)
    
    df.to_csv(output_path, index=False)
    print(f"\n[scraper] Saved enriched data to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExample: python scripts/craigslist_reply_scrape.py data/top10_landlords.csv")
        sys.exit(1)
    
    csv_file = Path(sys.argv[1])
    
    if not csv_file.exists():
        print(f"ERROR: {csv_file} not found")
        sys.exit(1)
    
    enrich_csv_with_craigslist_scrape(csv_file)
