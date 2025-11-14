# ChromeDriver Setup for WSP2AGENT
# ==================================
# Quick guide to install ChromeDriver for Selenium automation
#
# For the Commons Good 🌍

## ✅ What You Need

ChromeDriver must match your Chrome **MAJOR version**:
- Chrome **131**.0.6778.86 → ChromeDriver **131**.x.x ✅
- Chrome **130**.0.6723.92 → ChromeDriver **130**.x.x ✅

**Only the first number (major version) matters!**

---

## 🔍 Step 1: Check Your Chrome Version

### Option A: In Browser
1. Open Chrome
2. Go to: `chrome://version`
3. Look for: **"Google Chrome 131.0.6778.86"** (example)
4. Note the **first number** (131 in this example)

### Option B: PowerShell
```powershell
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
(Get-Item $chromePath).VersionInfo.ProductVersion
# Output: 131.0.6778.86
```

---

## 📥 Step 2: Download ChromeDriver

1. Go to: **https://googlechromelabs.github.io/chrome-for-testing/**
2. Find your Chrome major version (e.g., 131)
3. Download: **Windows 64-bit** (chromedriver-win64.zip)
4. Extract the ZIP file

---

## 📂 Step 3: Install to Recommended Path

### PowerShell Commands (copy-paste):

```powershell
# Create WebDriver folder
New-Item -ItemType Directory -Path "C:\WebDriver" -Force

# Move downloaded chromedriver.exe to C:\WebDriver
# (Adjust path if you extracted elsewhere)
Move-Item "$env:USERPROFILE\Downloads\chromedriver-win64\chromedriver.exe" "C:\WebDriver\chromedriver.exe" -Force

# Verify installation
Test-Path "C:\WebDriver\chromedriver.exe"
# Should output: True

# Check version
& "C:\WebDriver\chromedriver.exe" --version
# Output: ChromeDriver 131.0.6778.85 (...)
```

---

## ✅ Step 4: Verify Setup

Run the Selenium driver test:

```powershell
cd "C:\Users\Roberto002\My Drive\WSP2AGENT"
python modules\selenium_driver.py
```

**Expected output:**
```
🔍 WSP2AGENT Selenium Driver Factory
==================================================
✓ Chrome version: 131.0.6778.86
✓ ChromeDriver needed: 131.x.x

Testing driver creation (headless mode)...
✓ Driver created successfully
✓ Testing navigation...
✓ Page title: Google
✓ Driver closed cleanly

🎉 All tests passed! Ready for WSP2AGENT integration.
```

---

## 🎯 Step 5: Test Contact Enrichment

Try enriching your CSV with real Craigslist contacts:

```powershell
# Dry-run (first 3 rows, no changes saved)
python scripts\craigslist_contact_enricher.py --max-rows 3 --dry-run --visible

# Real enrichment (all rows, saves to CSV)
python scripts\craigslist_contact_enricher.py --headless
```

---

## 🚨 Troubleshooting

### Error: "ChromeDriver not found"
**Fix:** Make sure `C:\WebDriver\chromedriver.exe` exists
```powershell
Test-Path "C:\WebDriver\chromedriver.exe"
```

### Error: "This version of ChromeDriver only supports Chrome X"
**Fix:** Your Chrome and ChromeDriver major versions don't match
1. Check Chrome version: `chrome://version`
2. Download matching ChromeDriver (same major number)
3. Replace `C:\WebDriver\chromedriver.exe`

### Error: "Chrome binary not found"
**Fix:** Update path in code if Chrome is installed elsewhere
- Common locations:
  - `C:\Program Files\Google\Chrome\Application\chrome.exe`
  - `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`

### Browser window won't close
**Fix:** Use headless mode for automation
```powershell
python scripts\craigslist_contact_enricher.py --headless
```

---

## 📚 Alternative: Auto-Install with webdriver-manager

If you prefer automatic ChromeDriver management:

```powershell
pip install webdriver-manager
```

Then modify `modules/selenium_driver.py`:
```python
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
```

**Note:** Manual installation to `C:\WebDriver` is recommended for production stability.

---

## 🎉 You're Ready!

Once ChromeDriver is installed:
- ✅ `modules/selenium_driver.py` test passes
- ✅ `scripts/craigslist_contact_enricher.py` can scrape contacts
- ✅ Full WSP2AGENT workflow works end-to-end

**Next:** Run the full workflow test:
```powershell
.\test_workflow.ps1
```

For the Commons Good 🌍
