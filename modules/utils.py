"""
Utility helpers shared across modules.
Enhanced with demo data, activity logging, error assistance, and diagnostics.
"""

from __future__ import annotations

import csv
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def safe_file_write(path: str | Path, data: str, encoding: str = "utf-8") -> None:
    """Write text data to a file, creating parent directories if needed."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(data, encoding=encoding)


def read_csv(path: str | Path) -> List[dict]:
    """Read a CSV into a list of dictionaries without bringing in pandas."""
    rows: List[dict] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows.extend(reader)
    return rows


def normalize_email_list(value: str | Iterable[str]) -> List[str]:
    """Take a semicolon string or iterable and return a sanitized list."""
    if isinstance(value, str):
        candidates = [part.strip() for part in value.split(";")]
    else:
        candidates = [str(part).strip() for part in value]
    return [c for c in candidates if c]


def slugify_filename(value: str, max_length: int = 120) -> str:
    """Return a filename-safe slug derived from value."""
    value = (value or "").strip().replace(" ", "_")
    value = re.sub(r"[^A-Za-z0-9_.-]", "", value)
    return value[:max_length] or "contact"


# ============================================================================
# NEW: Demo Data & Enhanced Features
# ============================================================================

def get_sample_data() -> Dict[str, Any]:
    """
    Returns realistic demo data for testing the pipeline without setup.
    Users can experience the full workflow before connecting Gmail or uploading real files.
    """
    return {
        "contacts": [
            {
                "organization": "Demo Property Management LLC",
                "url": "https://example.com/demo-property",
                "emails": "demo@example.com",
                "phones": "555-123-4567",
                "snippet": "We manage affordable housing units across the city. Always looking for partnerships.",
                "score": 12,
                "approved": False
            },
            {
                "organization": "Sample Senior Housing Co-op",
                "url": "https://example.com/senior-coop",
                "emails": "info@seniorcoop.example",
                "phones": "555-987-6543",
                "snippet": "Non-profit cooperative providing housing for seniors. Community-focused approach.",
                "score": 10,
                "approved": False
            },
            {
                "organization": "Test Affordable Homes Foundation",
                "url": "https://example.com/affordable-homes",
                "emails": "contact@ahf.example",
                "phones": "555-555-5555",
                "snippet": "Building and managing affordable housing since 1995. Over 500 units managed.",
                "score": 9,
                "approved": False
            }
        ],
        "search_results": {
            "total_results": 3,
            "query": "affordable housing property managers",
            "timestamp": datetime.now().isoformat()
        }
    }


class ActivityLogger:
    """
    Tracks all user actions with timestamps for activity log and undo functionality.
    """
    def __init__(self, log_file: str = "data/sandbox/logs/activity.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
    def log_action(self, action_type: str, details: Dict[str, Any], status: str = "success") -> None:
        """Log an action with timestamp and details."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "details": details,
            "status": status
        }
        
        # Read existing log
        logs = self._read_logs()
        logs.append(entry)
        
        # Write updated log
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def _read_logs(self) -> List[Dict[str, Any]]:
        """Read existing activity logs."""
        if not os.path.exists(self.log_file):
            return []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent log entries."""
        logs = self._read_logs()
        return logs[-limit:][::-1]  # Reverse to show newest first
    
    def get_errors_only(self) -> List[Dict[str, Any]]:
        """Get only error/failure log entries."""
        logs = self._read_logs()
        return [log for log in logs if log.get("status") in ["error", "failure"]]
    
    def export_logs(self, output_path: str) -> bool:
        """Export logs to a file."""
        try:
            logs = self._read_logs()
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False


class ErrorAssistant:
    """
    Provides contextual error messages and suggested fixes.
    """
    ERROR_SOLUTIONS = {
        "missing_credentials": {
            "title": "Gmail Credentials Missing",
            "message": "The file 'credentials.json' was not found.",
            "solutions": [
                "Go to the Settings tab and click 'Connect Gmail Account'",
                "Download credentials.json from Google Cloud Console",
                "Place credentials.json in the project root directory"
            ],
            "docs_link": "https://developers.google.com/gmail/api/quickstart/python"
        },
        "unicode_decode": {
            "title": "File Encoding Issue",
            "message": "Unable to read file due to encoding mismatch.",
            "solutions": [
                "The file may contain non-UTF-8 characters",
                "Try saving the file with UTF-8 encoding",
                "Check if file was created on a different system (Windows vs Mac/Linux)"
            ],
            "docs_link": None
        },
        "missing_api_key": {
            "title": "API Key Not Set",
            "message": "SERPAPI_KEY environment variable is missing.",
            "solutions": [
                "Get your API key from https://serpapi.com/",
                "Set environment variable: setx SERPAPI_KEY \"your-key-here\"",
                "Restart the application after setting the key"
            ],
            "docs_link": "https://serpapi.com/manage-api-key"
        },
        "file_not_found": {
            "title": "File Not Found",
            "message": "Required file is missing from the project.",
            "solutions": [
                "Check if the file path is correct",
                "Ensure the file hasn't been moved or deleted",
                "Try running the setup/repair tool"
            ],
            "docs_link": None
        },
        "gmail_auth_failed": {
            "title": "Gmail Authentication Failed",
            "message": "Unable to authenticate with Gmail API.",
            "solutions": [
                "Delete token.pickle and try authenticating again",
                "Ensure credentials.json is valid and not expired",
                "Check that Gmail API is enabled in Google Cloud Console"
            ],
            "docs_link": "https://developers.google.com/gmail/api/auth/about-auth"
        }
    }
    
    @classmethod
    def get_help(cls, error_type: str) -> Optional[Dict[str, Any]]:
        """Get contextual help for a specific error type."""
        return cls.ERROR_SOLUTIONS.get(error_type)
    
    @classmethod
    def diagnose_error(cls, exception: Exception) -> str:
        """Diagnose an exception and return error type."""
        error_msg = str(exception).lower()
        
        if "credentials.json" in error_msg or "file not found" in error_msg:
            if "credentials" in error_msg:
                return "missing_credentials"
            return "file_not_found"
        elif "codec" in error_msg or "decode" in error_msg or "utf" in error_msg:
            return "unicode_decode"
        elif "serpapi" in error_msg or "api_key" in error_msg:
            return "missing_api_key"
        elif "auth" in error_msg or "token" in error_msg:
            return "gmail_auth_failed"
        else:
            return "unknown"


def check_environment() -> Dict[str, Any]:
    """
    Comprehensive environment check for setup/diagnostic purposes.
    Returns status and missing items.
    """
    checks = {
        "credentials_json": os.path.exists("credentials.json"),
        "serpapi_key": bool(os.getenv("SERPAPI_KEY")),
        "data_directory": os.path.exists("data"),
        "sandbox_directory": os.path.exists("data/sandbox"),
        "virtualenv": os.path.exists(".venv"),
        "requirements_txt": os.path.exists("requirements.txt"),
        "streamlit_app": os.path.exists("streamlit_app/app.py")
    }
    
    missing = [key for key, value in checks.items() if not value]
    all_good = len(missing) == 0
    
    return {
        "checks": checks,
        "missing": missing,
        "status": "ready" if all_good else "needs_setup",
        "message": "All systems ready!" if all_good else f"Missing: {', '.join(missing)}"
    }


def auto_repair_environment() -> Dict[str, Any]:
    """
    Attempt to automatically repair common environment issues.
    Returns results of repair attempts.
    """
    results = {
        "repaired": [],
        "failed": [],
        "messages": []
    }
    
    # Create missing directories
    directories = ["data", "data/sandbox", "data/sandbox/logs", 
                   "data/sandbox/outbox", "data/sandbox/sent", "data/sandbox/failed"]
    
    for dir_path in directories:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                results["repaired"].append(f"Created directory: {dir_path}")
            except Exception as e:
                results["failed"].append(f"Failed to create {dir_path}: {str(e)}")
    
    # Create empty files if missing (but don't overwrite)
    files_to_create = {
        "data/sandbox/logs/activity.json": "[]",
        "data/top10_landlords.csv": "organization,url,emails,phones,snippet,score,approved\n"
    }
    
    for file_path, default_content in files_to_create.items():
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(default_content)
                results["repaired"].append(f"Created file: {file_path}")
            except Exception as e:
                results["failed"].append(f"Failed to create {file_path}: {str(e)}")
    
    # Summary message
    if results["repaired"]:
        results["messages"].append(f"✅ Repaired {len(results['repaired'])} items")
    if results["failed"]:
        results["messages"].append(f"⚠️ {len(results['failed'])} items need manual attention")
    
    return results


# Feature voting storage
FEATURE_VOTES_FILE = "data/sandbox/logs/feature_votes.json"


def get_feature_votes() -> Dict[str, int]:
    """Get current feature vote counts."""
    if not os.path.exists(FEATURE_VOTES_FILE):
        return {
            "AI Reply Suggestions": 0,
            "Email Preview": 0,
            "A/B Testing": 0,
            "Scheduled Sending": 0,
            "Lead Scoring": 0,
            "Analytics Dashboard": 0
        }
    try:
        with open(FEATURE_VOTES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}


def vote_for_feature(feature_name: str) -> bool:
    """Cast a vote for a feature."""
    try:
        votes = get_feature_votes()
        if feature_name in votes:
            votes[feature_name] += 1
        else:
            votes[feature_name] = 1
        
        os.makedirs(os.path.dirname(FEATURE_VOTES_FILE), exist_ok=True)
        with open(FEATURE_VOTES_FILE, 'w', encoding='utf-8') as f:
            json.dump(votes, f, indent=2)
        return True
    except:
        return False


def get_top_voted_features(limit: int = 3) -> List[tuple]:
    """Get top voted features as list of (name, votes) tuples."""
    votes = get_feature_votes()
    sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
    return sorted_votes[:limit]
