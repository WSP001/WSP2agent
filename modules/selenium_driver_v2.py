"""
WSP2AGENT Production Selenium Driver
Resilient WebDriver with explicit waits and centralized selectors
"""

import platform
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.config import get_config


class ElementNotFoundError(Exception):
    """Custom exception for element not found after wait."""
    pass


def get_chrome_version() -> Optional[str]:
    """
    Detect installed Chrome version.
    
    Returns:
        Version string (e.g., "131.0.6778.86") or None if not found
    """
    config = get_config()
    chrome_path = config.chrome_binary_path
    
    if not Path(chrome_path).exists():
        return None
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ['powershell', '-Command',
                 f'(Get-Item "{chrome_path}").VersionInfo.ProductVersion'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.strip()
            if version and re.match(r'\d+\.\d+', version):
                return version
    except Exception:
        pass
    
    return None


def build_chrome_driver(
    headless: Optional[bool] = None,
    user_agent: Optional[str] = None
) -> webdriver.Chrome:
    """
    Build production-grade Chrome WebDriver with explicit configuration.
    
    Args:
        headless: Run in headless mode (uses config default if None)
        user_agent: Custom user agent string (optional)
    
    Returns:
        Configured Chrome WebDriver instance
    
    Raises:
        FileNotFoundError: If Chrome or ChromeDriver not found
        RuntimeError: If driver initialization fails
    """
    config = get_config()
    
    chrome_binary = Path(config.chrome_binary_path)
    driver_path = Path(config.chromedriver_path)
    
    # Validate paths
    if not chrome_binary.exists():
        raise FileNotFoundError(
            f"Chrome not found at: {chrome_binary}\n\n"
            f"Please install Chrome or update chrome_binary_path in config"
        )
    
    if not driver_path.exists():
        raise FileNotFoundError(
            f"ChromeDriver not found at: {driver_path}\n\n"
            f"See CHROMEDRIVER_SETUP.md for installation instructions"
        )
    
    # Build Chrome options
    options = Options()
    options.binary_location = str(chrome_binary)
    
    # Headless mode
    if headless is None:
        headless = config.headless_default
    if headless:
        options.add_argument("--headless=new")
    
    # Anti-detection and performance
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    
    # Custom user agent
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")
    
    # Remove webdriver property
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Build service
    service = Service(executable_path=str(driver_path))
    
    # Initialize driver
    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        # Remove webdriver flag
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
        )
        
        return driver
    
    except Exception as e:
        raise RuntimeError(
            f"Failed to initialize Chrome WebDriver: {e}\n\n"
            f"Verify ChromeDriver version matches Chrome version"
        ) from e


def safe_find(
    driver: webdriver.Chrome,
    by: By,
    locator: str,
    timeout: Optional[int] = None,
    multiple: bool = False
) -> Optional[any]:
    """
    Find element with explicit wait and error handling.
    
    Args:
        driver: Chrome WebDriver instance
        by: Selenium By locator strategy (e.g., By.CSS_SELECTOR)
        locator: Element locator string
        timeout: Wait timeout in seconds (uses config default if None)
        multiple: Return all matching elements if True
    
    Returns:
        WebElement(s) or None if not found
    
    Raises:
        ElementNotFoundError: If element not found after timeout
    """
    config = get_config()
    timeout = timeout or config.timeout_seconds
    
    try:
        wait = WebDriverWait(driver, timeout)
        
        if multiple:
            condition = EC.presence_of_all_elements_located((by, locator))
        else:
            condition = EC.presence_of_element_located((by, locator))
        
        return wait.until(condition)
    
    except TimeoutException as e:
        raise ElementNotFoundError(
            f"Element not found: {locator} (waited {timeout}s)"
        ) from e


def safe_click(
    driver: webdriver.Chrome,
    by: By,
    locator: str,
    timeout: Optional[int] = None
) -> bool:
    """
    Click element with explicit wait for clickability.
    
    Args:
        driver: Chrome WebDriver instance
        by: Selenium By locator strategy
        locator: Element locator string
        timeout: Wait timeout in seconds
    
    Returns:
        True if clicked successfully, False otherwise
    """
    config = get_config()
    timeout = timeout or config.timeout_seconds
    
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()
        return True
    
    except (TimeoutException, NoSuchElementException):
        return False


# Smoke test
if __name__ == "__main__":
    print("🧪 Selenium Driver Smoke Test")
    print("=" * 50)
    
    # Check Chrome version
    version = get_chrome_version()
    if version:
        print(f"✓ Chrome version: {version}")
    else:
        print("⚠️  Could not detect Chrome version")
    
    # Build driver
    print("\n📦 Building WebDriver...")
    try:
        driver = build_chrome_driver(headless=True)
        print("✓ WebDriver initialized")
        
        # Test navigation
        print("\n🌐 Testing navigation...")
        driver.get("https://www.google.com")
        print(f"✓ Loaded: {driver.title}")
        
        # Test safe_find
        print("\n🔍 Testing safe_find...")
        search_box = safe_find(driver, By.NAME, "q", timeout=5)
        if search_box:
            print("✓ Found search box with explicit wait")
        
        driver.quit()
        print("\n✅ All tests passed!")
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        exit(1)
