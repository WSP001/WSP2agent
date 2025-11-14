"""
WSP2AGENT Structured Logging
JSON-based logging for observability and traceability
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class StructuredLogger:
    """Structured JSON logger for pipeline events."""
    
    def __init__(self, log_dir: Path, run_id: str, env: str = "dev"):
        """
        Initialize logger.
        
        Args:
            log_dir: Directory for log files
            run_id: Unique identifier for this run
            env: Environment (dev/staging/prod)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.run_id = run_id
        self.env = env
        
        # Log file paths
        today = datetime.now().strftime("%Y%m%d")
        self.log_file = self.log_dir / f"scraper_{today}.log"
        self.run_report_file = self.log_dir / f"run_report_{run_id}.json"
        
        # Run-level stats
        self.stats = {
            "run_id": run_id,
            "env": env,
            "started_at": datetime.now().isoformat(),
            "processed": 0,
            "success": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
    
    def _log(self, level: str, event: str, **kwargs):
        """Write structured log entry."""
        entry = {
            "ts": datetime.now().isoformat(),
            "run_id": self.run_id,
            "env": self.env,
            "level": level,
            "event": event,
            **kwargs
        }
        
        # Write to file (JSON lines)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
        
        # Also print to console (for interactive runs)
        if level in ["ERROR", "WARN"]:
            print(f"[{level}] {event}: {kwargs}", file=sys.stderr)
        elif level == "INFO":
            print(f"[INFO] {event}")
    
    def info(self, event: str, **kwargs):
        """Log INFO level event."""
        self._log("INFO", event, **kwargs)
    
    def warn(self, event: str, **kwargs):
        """Log WARN level event."""
        self._log("WARN", event, **kwargs)
    
    def error(self, event: str, **kwargs):
        """Log ERROR level event."""
        self._log("ERROR", event, **kwargs)
        self.stats["errors"].append({
            "ts": datetime.now().isoformat(),
            "event": event,
            **kwargs
        })
    
    def record_processed(self):
        """Increment processed counter."""
        self.stats["processed"] += 1
    
    def record_success(self):
        """Increment success counter."""
        self.stats["success"] += 1
    
    def record_failed(self, reason: str):
        """Increment failed counter and record reason."""
        self.stats["failed"] += 1
        self.stats["errors"].append({
            "ts": datetime.now().isoformat(),
            "reason": reason
        })
    
    def record_skipped(self):
        """Increment skipped counter."""
        self.stats["skipped"] += 1
    
    def finalize(self) -> Dict[str, Any]:
        """
        Finalize run and write report.
        
        Returns:
            Run statistics dict
        """
        self.stats["completed_at"] = datetime.now().isoformat()
        
        # Write run report
        with open(self.run_report_file, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, indent=2)
        
        self.info("run_complete", **self.stats)
        
        return self.stats
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current run statistics."""
        return self.stats.copy()


def create_logger(log_dir: str = "logs", run_id: Optional[str] = None, env: str = "dev") -> StructuredLogger:
    """
    Create a new structured logger.
    
    Args:
        log_dir: Directory for log files
        run_id: Unique run ID (auto-generated if None)
        env: Environment name
    
    Returns:
        StructuredLogger instance
    """
    if run_id is None:
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return StructuredLogger(Path(log_dir), run_id, env)
