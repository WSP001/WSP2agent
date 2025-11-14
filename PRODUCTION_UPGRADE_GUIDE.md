# WSP2AGENT Production Upgrade - Testing Guide

## 🎯 What We Built

You now have **production-grade versions** of your Selenium automation:

### New Files (V2 - Production)
- `modules/config.py` - Config management (CLI > ENV > YAML > defaults)
- `modules/logger.py` - JSON structured logging
- `modules/data_schema.py` - CSV schema validation + atomic writes
- `modules/selenium_driver_v2.py` - Resilient WebDriver with explicit waits
- `scripts/contact_enricher_v2.py` - Retry logic + structured errors
- `config/selenium_settings.yaml` - Centralized settings

### Old Files (V1 - Prototype)
- `modules/selenium_driver.py` - Original working prototype
- `scripts/craigslist_contact_enricher.py` - Original enricher

**Both versions coexist** - you can test V2 without breaking V1!

---

## ✅ Step 1: Install Missing Dependency

```powershell
# V2 uses PyYAML for config management
pip install pyyaml
```

---

## ✅ Step 2: Test Production Driver (V2)

```powershell
# Test new resilient WebDriver
python modules/selenium_driver_v2.py
```

**Expected output:**
```
🧪 Selenium Driver Smoke Test
==================================================
✓ Chrome version: 131.0.6778.86
📦 Building WebDriver...
✓ WebDriver initialized
🌐 Testing navigation...
✓ Loaded: Google
🔍 Testing safe_find...
✓ Found search box with explicit wait
✅ All tests passed!
```

---

## ✅ Step 3: Test Config System

```powershell
# Test config loading
python -c "from modules.config import get_config; cfg = get_config(); print(f'Chrome: {cfg.chrome_binary_path}'); print(f'Headless: {cfg.headless_default}')"
```

---

## ✅ Step 4: Test Production Enricher (Dry Run)

```powershell
# Run V2 enricher in dry-run mode (won't modify CSV)
python scripts/contact_enricher_v2.py --csv data/top10_landlords.csv --visible --max-rows 3 --dry-run
```

**What this does:**
- Runs in **visible mode** (see browser in action)
- Processes **3 rows only** (quick test)
- **Dry run** (won't write to CSV)
- Creates **structured logs** in `logs/`
- Shows **preview** of enriched data

**Expected output:**
```
[INFO] enrichment_started
[INFO] csv_loaded
[INFO] listing_processed
[INFO] reply_button_clicked
...
🧪 DRY RUN - Results preview:
  organization              emails         phones  scrape_status
0  Landlord A    landlord@example.com  555-123-4567  success

✅ Enrichment Complete
==================================================
Run ID: 20251113_143022
Processed: 3
Success: 2
Failed: 0
Skipped: 1
Log: logs/run_report_20251113_143022.json
```

---

## ✅ Step 5: Inspect Run Report

```powershell
# View structured JSON run report
Get-Content logs/run_report_*.json | Select-Object -Last 1 | ConvertFrom-Json | ConvertTo-Json
```

---

## ✅ Step 6: Test Real Enrichment (Small Batch)

```powershell
# Real run (writes to CSV with backup)
python scripts/contact_enricher_v2.py --csv data/top10_landlords.csv --headless --max-rows 3
```

**What happens:**
1. Creates backup: `data/top10_landlords.csv.bak.20251113_143500`
2. Enriches 3 rows
3. Writes atomically (temp file → rename)
4. Adds new columns: `scrape_status`, `scrape_error`, `last_scraped_at`

---

## ✅ Step 7: Compare V1 vs V2

| Feature | V1 (Prototype) | V2 (Production) |
|---------|----------------|-----------------|
| Config | Hardcoded | YAML + ENV |
| Waits | `time.sleep()` | `WebDriverWait` |
| Retry | None | 2 retries + backoff |
| Logging | `print()` | JSON structured |
| CSV writes | Direct | Atomic + backup |
| Error handling | Crash | Graceful fail |
| Run tracking | None | JSON reports |
| Schema | Ad-hoc | Validated |

---

## 🚀 Next Steps

### Option A: Keep V1 (It Works!)
```powershell
# Continue using your working prototype
.\test_workflow.ps1
```

### Option B: Migrate to V2 (Production-Ready)
```powershell
# Test V2 thoroughly, then:
# 1. Rename V1 files to _backup
# 2. Rename V2 files (remove _v2 suffix)
# 3. Update imports in other modules
```

### Option C: Hybrid Approach (Recommended)
- Use **V2 for production runs** (headless, logging, backups)
- Keep **V1 for quick tests** (faster, simpler)

---

## 🎯 Key Improvements in V2

1. **Config-driven** - Change behavior without touching code
2. **Resilient** - Handles failures gracefully, doesn't crash
3. **Observable** - JSON logs for debugging and auditing
4. **Safe** - Atomic writes, backups, schema validation
5. **Maintainable** - Centralized selectors, DRY principle
6. **Testable** - Clear separation of concerns

---

## 📊 Environment Profiles

Edit `config/selenium_settings.yaml` to tune for your use case:

### Dev (Current)
- Visible browser
- Small batches (3 rows)
- Fast delays (1-2 sec)

### Staging
- Headless
- Medium batches (10 rows)
- Normal delays (2-4 sec)

### Prod
- Headless
- Large batches (50 rows)
- Polite delays (3-5 sec)
- Respects robots.txt

---

## 🧪 What to Test

- [ ] V2 driver smoke test passes
- [ ] Config loads from YAML
- [ ] Dry-run enrichment works (visible mode)
- [ ] Real enrichment creates backup
- [ ] Run report JSON looks correct
- [ ] CSV has new columns (scrape_status, etc.)
- [ ] Retry logic works (test with bad URL)
- [ ] Logs directory created with JSON lines

---

## ❓ Questions for Your Netlify Agent

When you're ready to deploy, ask:

**"I have a Streamlit dashboard (Python/WebSocket app) that I need to deploy. It's NOT a static site - it requires a continuous Python server. Should I use Streamlit Community Cloud instead of Netlify?"**

For Netlify AI features, ask:

**"My GitHub repo is WSP001/WSP2agent (already connected to Netlify project ID 31168ba9-8c2e-4b96-8abe-a583bbeb9af3). The build is failing because it's expecting a static site but I have a Streamlit app. How do I either: (A) deploy Streamlit to Netlify using custom build commands, OR (B) connect this repo to Streamlit Community Cloud instead?"**

---

## 🌍 For the Commons Good!

You now have production-grade automation that's:
- **Robust** enough to run unattended
- **Observable** enough to debug when things go wrong
- **Maintainable** enough to hand off to teammates
- **Safe** enough to run in production

Test it thoroughly, then show your team what "quality code" looks like! 🎉
