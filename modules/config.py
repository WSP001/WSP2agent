"""
WSP2AGENT Configuration Management
Centralized settings with precedence: CLI > ENV > YAML > Defaults
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class Config:
    """Config loader with precedence hierarchy."""
    
    def __init__(self, env: Optional[str] = None):
        """
        Initialize config.
        
        Args:
            env: Environment name (dev/staging/prod). Falls back to WSP_ENV env var.
        """
        self.env = env or os.getenv("WSP_ENV", "dev")
        self.config_dir = Path(__file__).parent.parent / "config"
        self.settings_file = self.config_dir / "selenium_settings.yaml"
        
        # Load YAML config if available
        self._yaml_config: Dict[str, Any] = {}
        if YAML_AVAILABLE and self.settings_file.exists():
            with open(self.settings_file, "r") as f:
                self._yaml_config = yaml.safe_load(f) or {}
    
    def get(self, key_path: str, env_var: Optional[str] = None, default: Any = None) -> Any:
        """
        Get config value with precedence.
        
        Args:
            key_path: Dot-separated path (e.g., "chrome.binary_path")
            env_var: Environment variable name to check
            default: Fallback value
        
        Returns:
            Config value following precedence: ENV > YAML > default
        """
        # 1. Check environment variable
        if env_var and env_var in os.environ:
            return os.environ[env_var]
        
        # 2. Check YAML config
        if self._yaml_config:
            keys = key_path.split(".")
            value = self._yaml_config
            try:
                for key in keys:
                    value = value[key]
                return value
            except (KeyError, TypeError):
                pass
        
        # 3. Return default
        return default
    
    def get_env_profile(self) -> Dict[str, Any]:
        """Get environment-specific settings."""
        env_settings = self._yaml_config.get("environments", {}).get(self.env, {})
        return env_settings
    
    # Chrome/ChromeDriver
    @property
    def chrome_binary_path(self) -> str:
        env_profile = self.get_env_profile()
        return self.get(
            "chrome.binary_path",
            env_var="CHROME_BINARY",
            default=env_profile.get("chrome_binary_path", 
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        )
    
    @property
    def chromedriver_path(self) -> str:
        env_profile = self.get_env_profile()
        return self.get(
            "chrome.driver_path",
            env_var="CHROMEDRIVER_PATH",
            default=env_profile.get("chromedriver_path", "C:\\WebDriver\\chromedriver.exe")
        )
    
    # Scraper Settings
    @property
    def headless_default(self) -> bool:
        env_profile = self.get_env_profile()
        return env_profile.get("headless", 
            self.get("scraper.headless_default", default=True))
    
    @property
    def max_rows_default(self) -> int:
        env_profile = self.get_env_profile()
        return env_profile.get("max_rows_default",
            self.get("scraper.max_rows_default", default=10))
    
    @property
    def politeness_delay_min(self) -> float:
        env_profile = self.get_env_profile()
        return env_profile.get("politeness_delay_min",
            self.get("scraper.politeness_delay_min", default=2.0))
    
    @property
    def politeness_delay_max(self) -> float:
        return self.get("scraper.politeness_delay_max", default=4.0)
    
    @property
    def max_retries(self) -> int:
        return self.get("scraper.max_retries", default=2)
    
    @property
    def retry_backoff_seconds(self) -> int:
        return self.get("scraper.retry_backoff_seconds", default=5)
    
    @property
    def timeout_seconds(self) -> int:
        return self.get("scraper.timeout_seconds", default=10)
    
    # Selectors
    @property
    def selectors(self) -> Dict[str, Dict[str, str]]:
        return self.get("selectors", default={
            "craigslist": {
                "reply_button": "button.reply-button, a.reply-button, .reply",
                "email_span": "span.reply-email, .email-address",
                "phone_span": "span.reply-phone, .phone-number",
                "listing_body": "section#postingbody, .posting-body"
            }
        })
    
    # Logging
    @property
    def log_level(self) -> str:
        return self.get("logging.level", env_var="WSP_LOG_LEVEL", default="INFO")
    
    @property
    def log_format(self) -> str:
        return self.get("logging.format", default="json")
    
    @property
    def log_dir(self) -> Path:
        log_dir_str = self.get("logging.output_dir", default="logs")
        return Path(log_dir_str)


# Global config instance
_config: Optional[Config] = None


def get_config(env: Optional[str] = None) -> Config:
    """Get global config instance (singleton)."""
    global _config
    if _config is None or (env and env != _config.env):
        _config = Config(env=env)
    return _config
