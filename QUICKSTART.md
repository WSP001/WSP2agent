# 🏠 WSP2AGENT - Quick Start Guide

## Simplest Way to Use This System

### ONE-CLICK START (Recommended)

**Windows Users:**
1. Double-click `LAUNCH_APP.ps1`
2. That's it! The web interface opens automatically

**If you get a security warning:**
- Right-click `LAUNCH_APP.ps1` → Properties → Unblock → OK
- Or open PowerShell and run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Using the Web Interface

Once the Streamlit app opens in your browser, you'll see 4 simple tabs:

### 📋 Tab 1: Dashboard
- **What it shows:** Current status of your pipeline
- **What to do:** Just review the summary

### 🔍 Tab 2: Search & Scrape
- **Click:** "Run Full Pipeline (Dry Run)"
- **What happens:** Searches Craigslist → Scrapes emails → Ranks top 10 landlords
- **Time:** 2-3 minutes

### ✅ Tab 3: Review & Approve
- **What it shows:** Your top 10 landlord contacts
- **What to do:** 
  1. Check the boxes next to contacts you want to email (start with 1-3)
  2. Click "Save Approvals"

### 📧 Tab 4: Send Emails
**First-Time Setup (one-time only):**
1. Click "Authenticate Gmail" → Sign in with your Google account
2. Grant permission

**Sending Emails:**
1. Click "Create Personal Flyers" (generates PDFs)
2. Click "Generate Email Drafts" (writes emails)
3. **TEST FIRST:** Keep "Dry Run" checked → Click "SEND EMAILS" to preview
4. **Real Send:** Uncheck "Dry Run" → Click "SEND EMAILS"

---

## What if Something Goes Wrong?

### "File does not exist: streamlit_app\app.py"
You forgot to run from the WSP2AGENT folder. 
**Fix:** Right-click `LAUNCH_APP.ps1` → Edit → Change first line to:
```powershell
cd "C:\Users\Roberto002\My Drive\WSP2AGENT"
```

### "SERPAPI_KEY missing"
The app will show a text box in the sidebar. Paste your key and click Save.

### "credentials.json missing"
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Gmail API
3. Create OAuth 2.0 Desktop credentials
4. Download as `credentials.json`
5. Upload in the sidebar of the Streamlit app

### "No packages found" when trying to send
You didn't approve any contacts! Go to Tab 3 and check some boxes.

---

## Manual Terminal Method (If You Prefer)

```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Run Streamlit
streamlit run streamlit_app/app.py
```

---

## What This Replaces

**OLD WAY (20+ commands):**
```powershell
python run_pipeline.py --dry-run
python scripts/extract_contacts.py
python -c "from modules.broker import ..."
python -c "import modules.worker as w; ..."
python -c "import modules.gmailer as g; g.gmail_auth()"
# ... etc etc etc
```

**NEW WAY (1 double-click):**
- `LAUNCH_APP.ps1` → Click buttons in browser

---

## Pro Tips

1. **Always test with Dry Run first** - See what will be sent before actually sending
2. **Start with 1-3 contacts** - Gmail has daily limits (500/day for new accounts)
3. **Check the Dashboard** - Shows pipeline status at a glance
4. **Save your API key in Settings tab** - So you don't need to re-enter it

---

## Troubleshooting Table

| Problem | Solution |
|---------|----------|
| PowerShell won't run .ps1 | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Streamlit won't start | `pip install streamlit pandas` |
| Can't find Python | Install from [python.org](https://www.python.org/downloads/) |
| Gmail auth fails | Re-download credentials.json from Google Cloud Console |
| No search results | Check SERPAPI_KEY is valid at [serpapi.com](https://serpapi.com/) |

---

## Support

Created for World Seafood Producers' housing outreach automation.
Need help? Check `README.md` for full documentation.
