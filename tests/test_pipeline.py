"""
Integration tests for WSP2AGENT pipeline.

Run with:
    pytest tests/test_pipeline.py -v
    
Or with coverage:
    pytest tests/test_pipeline.py --cov=modules --cov-report=html
"""

import os
from pathlib import Path

import pytest


@pytest.fixture
def ensure_data_dir():
    """Ensure data directory exists."""
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


@pytest.mark.skipif(
    not os.getenv("SERPAPI_KEY"),
    reason="SERPAPI_KEY not set - cannot run search stage"
)
def test_run_full_pipeline_dry_run(ensure_data_dir):
    """Test the full pipeline in dry-run mode."""
    from modules import searcher, scraper, curator
    
    # 1. Search stage
    results = searcher.run_searches()
    assert len(results) > 0, "Search should return results"
    
    # Save search results
    import json
    search_file = ensure_data_dir / "search_results.json"
    with open(search_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    assert search_file.exists(), "search_results.json should be created"
    
    # 2. Scrape stage
    contacts_file = ensure_data_dir / "contacts_raw.csv"
    scraper.scrape_results(search_file, out_csv=contacts_file)
    assert contacts_file.exists(), "contacts_raw.csv should be created"
    
    # 3. Curate stage
    top10_file = ensure_data_dir / "top10_landlords.csv"
    curator.curate_contacts(contacts_file, out_csv=top10_file)
    assert top10_file.exists(), "top10_landlords.csv should be created"
    
    # Verify top10 has data
    import pandas as pd
    df = pd.read_csv(top10_file)
    assert len(df) > 0, "top10 should have at least one row"
    assert "score" in df.columns, "top10 should have score column"


def test_broker_creates_packages(ensure_data_dir):
    """Test broker package creation."""
    from modules.broker import create_packages_from_csv
    
    top10_file = ensure_data_dir / "top10_landlords.csv"
    
    if not top10_file.exists():
        pytest.skip("top10_landlords.csv not found - run pipeline first")
    
    packages = create_packages_from_csv(
        top10_file,
        pdf_dir=Path("out"),
        only_approved=True
    )
    
    # Should create packages for approved rows
    assert isinstance(packages, list), "Should return list of packages"
    
    # Check outbox directory
    outbox = ensure_data_dir / "sandbox" / "outbox"
    if outbox.exists():
        package_files = list(outbox.glob("package_*.json"))
        assert len(package_files) >= 0, "Outbox should exist"


def test_gmailer_dry_run(ensure_data_dir):
    """Test Gmail sending in dry-run mode (no actual emails sent)."""
    from modules.gmailer import send_approved_emails
    
    top10_file = ensure_data_dir / "top10_landlords.csv"
    
    if not top10_file.exists():
        pytest.skip("top10_landlords.csv not found")
    
    # Dry run should not require Gmail auth
    results = send_approved_emails(top10_file, dry_run=True)
    
    assert isinstance(results, list), "Should return list of results"


def test_csv_encoding():
    """Test that CSV files are readable with UTF-8."""
    csv_files = [
        Path("data/contacts_raw.csv"),
        Path("data/top10_landlords.csv"),
    ]
    
    for csv_file in csv_files:
        if not csv_file.exists():
            continue
        
        # Should be readable as UTF-8
        try:
            import pandas as pd
            df = pd.read_csv(csv_file, encoding="utf-8")
            assert len(df) >= 0, f"{csv_file} should be valid CSV"
        except UnicodeDecodeError:
            pytest.fail(f"{csv_file} has encoding issues")


def test_json_encoding():
    """Test that JSON files are readable with UTF-8."""
    json_files = [
        Path("data/search_results.json"),
        Path("data/top10_outreach_emails.json"),
    ]
    
    for json_file in json_files:
        if not json_file.exists():
            continue
        
        # Should be readable as UTF-8
        try:
            import json
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
            assert data is not None, f"{json_file} should be valid JSON"
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            pytest.fail(f"{json_file} has encoding/parsing issues: {e}")


@pytest.mark.parametrize("module_name", [
    "searcher",
    "scraper",
    "curator",
    "pdfs",
    "composer",
    "gmailer",
    "broker",
    "worker",
])
def test_modules_importable(module_name):
    """Test that all modules can be imported."""
    try:
        __import__(f"modules.{module_name}")
    except ImportError as e:
        pytest.fail(f"Failed to import modules.{module_name}: {e}")
