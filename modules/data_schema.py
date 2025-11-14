"""
WSP2AGENT Data Schema Management
Enforces CSV column structure and provides atomic write operations
"""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import pandas as pd


# Locked CSV schema for top10_landlords.csv
TOP10_SCHEMA = {
    "id": "str",  # Unique identifier (hash of URL or row index)
    "organization": "str",
    "url": "str",
    "emails": "str",
    "phones": "str",
    "score": "float",
    "approved": "bool",
    "scrape_status": "str",  # success, failed, skipped, pending
    "scrape_error": "str",  # nullable, error message if failed
    "last_scraped_at": "str",  # ISO timestamp
}


def validate_schema(df: pd.DataFrame, schema: dict) -> bool:
    """
    Validate DataFrame matches expected schema.
    
    Args:
        df: DataFrame to validate
        schema: Dict of {column_name: dtype}
    
    Returns:
        True if valid, False otherwise
    """
    expected_columns = set(schema.keys())
    actual_columns = set(df.columns)
    
    if expected_columns != actual_columns:
        missing = expected_columns - actual_columns
        extra = actual_columns - expected_columns
        
        if missing:
            print(f"⚠️  Missing columns: {missing}")
        if extra:
            print(f"⚠️  Extra columns: {extra}")
        
        return False
    
    return True


def ensure_schema(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """
    Ensure DataFrame has all required columns.
    
    Args:
        df: DataFrame to fix
        schema: Dict of {column_name: dtype}
    
    Returns:
        DataFrame with all schema columns (adds missing with defaults)
    """
    for col, dtype in schema.items():
        if col not in df.columns:
            # Add missing column with default value
            if dtype == "str":
                df[col] = ""
            elif dtype == "float":
                df[col] = 0.0
            elif dtype == "bool":
                df[col] = False
    
    # Reorder columns to match schema
    return df[list(schema.keys())]


def atomic_write_csv(
    df: pd.DataFrame,
    file_path: Path,
    backup: bool = True,
    validate: bool = True,
    schema: Optional[dict] = None
) -> None:
    """
    Write CSV atomically with optional backup.
    
    Args:
        df: DataFrame to write
        file_path: Target CSV path
        backup: Create timestamped backup before overwriting
        validate: Validate schema before writing
        schema: Expected schema (uses TOP10_SCHEMA if None)
    
    Raises:
        ValueError: If schema validation fails
    """
    file_path = Path(file_path)
    schema = schema or TOP10_SCHEMA
    
    # Validate schema
    if validate and not validate_schema(df, schema):
        raise ValueError(f"DataFrame does not match expected schema for {file_path.name}")
    
    # Create backup if file exists
    if backup and file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.with_suffix(f".csv.bak.{timestamp}")
        shutil.copy2(file_path, backup_path)
        print(f"✓ Backup created: {backup_path.name}")
    
    # Atomic write: write to temp file, then rename
    temp_path = file_path.with_suffix(".csv.tmp")
    df.to_csv(temp_path, index=False)
    
    # Rename (atomic on most filesystems)
    temp_path.replace(file_path)
    
    print(f"✓ CSV written atomically: {file_path.name}")


def load_csv_with_schema(file_path: Path, schema: Optional[dict] = None) -> pd.DataFrame:
    """
    Load CSV and ensure it matches schema.
    
    Args:
        file_path: CSV file to load
        schema: Expected schema (uses TOP10_SCHEMA if None)
    
    Returns:
        DataFrame with guaranteed schema
    """
    schema = schema or TOP10_SCHEMA
    
    if not file_path.exists():
        # Create empty DataFrame with schema
        df = pd.DataFrame(columns=list(schema.keys()))
    else:
        df = pd.read_csv(file_path)
        df = ensure_schema(df, schema)
    
    return df


def cleanup_old_backups(file_path: Path, retention_days: int = 7) -> int:
    """
    Delete old backup files.
    
    Args:
        file_path: Main CSV file (backups are named file.csv.bak.*)
        retention_days: Keep backups newer than this many days
    
    Returns:
        Number of backups deleted
    """
    file_path = Path(file_path)
    backup_pattern = f"{file_path.name}.bak.*"
    
    now = datetime.now()
    deleted = 0
    
    for backup_file in file_path.parent.glob(backup_pattern):
        # Parse timestamp from filename
        try:
            timestamp_str = backup_file.suffix[1:]  # Remove leading "."
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            
            age_days = (now - timestamp).days
            if age_days > retention_days:
                backup_file.unlink()
                deleted += 1
        except (ValueError, IndexError):
            continue
    
    if deleted > 0:
        print(f"✓ Deleted {deleted} old backup(s)")
    
    return deleted
