# 🚀 WSP2AGENT Netlify Deployment Requirements

**FOR NETLIFY AGENT:** Complete deployment specification for WSP2AGENT V3 production dashboard.

---

## 📋 PROJECT OVERVIEW

**App Name:** WSP2AGENT V3  
**Type:** Streamlit Web Application (Python)  
**Purpose:** Modular automated outreach system with beautiful user-friendly dashboard  
**Current Status:** Production-ready, tested locally, needs cloud deployment  
**GitHub Repo:** https://github.com/WSP001/WSP2agent (branch: main, tag: v3.0.0)

**Quality Standard:** "For the Commons Good 🌍" - High-quality, user-friendly, intuitive interface

---

## 🎯 DEPLOYMENT GOALS

1. **Deploy Streamlit dashboard** to Netlify with custom domain
2. **Enable one-button workflows** (Search → Scrape → Curate → Email)
3. **Integrate Selenium scraper** into UI (housing search prototype use case)
4. **Handle environment variables** securely (API keys, OAuth credentials)
5. **Support background tasks** (email sending, reply monitoring)
6. **Provide public demo mode** + authenticated production mode

---

## 📦 APPLICATION DETAILS

### Tech Stack
- **Framework:** Streamlit 1.28.0+
- **Language:** Python 3.8+
- **Dependencies:** See `requirements.txt` (15 packages)
  - Core: `streamlit`, `pandas`, `python-dotenv`
  - APIs: `serpapi`, `google-api-python-client`, `google-auth-oauthlib`
  - Automation: `selenium`, `beautifulsoup4`, `requests`
  - PDF Generation: `reportlab`
  - Testing: `pytest`, `pytest-cov`

### Entry Point
- **Main app:** `streamlit_app/app.py` (6-tab dashboard)
- **Launcher:** `LAUNCH_APP.ps1` (local Windows launcher)
- **Run command:** `streamlit run streamlit_app/app.py`

### Port Configuration
- **Default port:** 8501 (Streamlit default)
- **Custom port option:** `--server.port=<PORT>`
- **Headless mode:** `--server.headless=true` (for cloud deployment)

---

## 🔑 ENVIRONMENT VARIABLES NEEDED

### Required for Full Functionality
```bash
# SerpAPI (search functionality)
SERPAPI_KEY="your_serpapi_key_here"

# Gmail OAuth (email sending)
GMAIL_CREDENTIALS_PATH="credentials.json"  # OAuth2 credentials file
GMAIL_SENDER_EMAIL="your-email@gmail.com"

# Data directory
DATA_DIR="data"  # Default, can override

# Search defaults
SEARCH_LOCATION="Winter Haven, FL"  # Optional, can override in UI
```

### File-Based Secrets (Not Environment Variables)
These need special handling:

1. **credentials.json** (Gmail OAuth2 client secret)
   - Generated from Google Cloud Console
   - Contains: client_id, client_secret, redirect_uris
   - Currently uploaded via UI (Sidebar → Upload credentials.json)
   - **Question for Netlify agent:** How to store this securely? (Build secret? Function env?)

2. **token.json** (Gmail OAuth2 access token)
   - Generated on first Gmail auth
   - Contains: refresh_token, access_token, expiry
   - Auto-refreshed by google-auth library
   - **Question for Netlify agent:** How to persist this across deployments? (Writable volume? Database?)

---

## 🏗️ DEPLOYMENT ARCHITECTURE QUESTIONS

### 1. Streamlit Hosting on Netlify
**Question:** Does Netlify support Streamlit apps natively, or do we need:
- **Option A:** Netlify Functions (serverless)?
- **Option B:** Docker container deployment?
- **Option C:** External hosting (e.g., Streamlit Community Cloud) + Netlify for landing page?
- **Option D:** Other recommended approach?

**Context:** Streamlit requires a persistent Python process. Current UI has 6 tabs with interactive buttons.

---

### 2. Selenium/ChromeDriver for Web Scraping
**Question:** How to run Selenium on Netlify Functions?

**Current setup (local):**
- ChromeDriver binary at `C:\WebDriver\chromedriver.exe`
- Chrome browser installed locally
- Selenium 4 with headless mode

**Files involved:**
- `modules/selenium_driver.py` - WebDriver factory
- `scripts/craigslist_contact_enricher.py` - Scraper script

**Options I'm aware of:**
- **Puppeteer** in Netlify Functions?
- **Playwright** serverless?
- **External service** (ScrapingBee, BrightData)?
- **Separate worker service** (not on Netlify)?

**Question:** What's your recommended approach for Selenium/scraping on Netlify?

---

### 3. Background Tasks & Long-Running Processes
**Question:** How to handle operations that take >10 seconds?

**Operations that may exceed function timeout:**
- Search (SerpAPI) - 10-30 seconds (multiple queries)
- Scrape - 30-120 seconds (fetching 10-50 URLs)
- Selenium enrichment - 60-180 seconds (clicking reply buttons, waiting for page loads)
- Email sending - 5-15 seconds (OAuth + SMTP)

**Current workflow:**
1. User clicks "Run Full Pipeline (Dry Run)"
2. App runs: Search → Scrape → Curate (with progress spinner)
3. Shows results in dashboard table

**Options:**
- **Netlify Functions** (10 sec limit)?
- **Netlify Background Functions** (15 min limit)?
- **Queue system** (Redis, Pub/Sub)?
- **Split into multiple button clicks** (user triggers each step)?

**Question:** What's the best pattern for these workflows on Netlify?

---

### 4. File Storage & Persistence
**Question:** Where to store generated files and databases?

**Current file structure:**
```
data/
  ├── search_results.json         # Search API responses
  ├── contacts_raw.csv            # Scraped contacts
  ├── top10_landlords.csv         # Curated leads (with 'approved' flag)
  ├── top10_outreach_emails.json  # Email drafts
  ├── responses.csv               # Reply tracking
  ├── packages.db                 # SQLite database (broker/worker system)
  └── sandbox/
      ├── outbox/                 # Pending email packages
      ├── sent/                   # Completed packages
      ├── failed/                 # Failed packages
      └── logs/                   # Activity logs
out/
  └── personal_flyer_1..10.pdf    # Generated PDFs
```

**Requirements:**
- CSV/JSON files read/written by multiple tabs
- PDFs generated and attached to emails
- SQLite database for package tracking
- Files need to persist between user sessions (not ephemeral)

**Options:**
- **Netlify Blob Storage**?
- **External storage** (AWS S3, Google Cloud Storage, Supabase)?
- **User uploads** (download results, upload next session)?
- **Database** (PostgreSQL, MongoDB) instead of CSV files?

**Question:** What's your recommended file storage strategy?

---

### 5. Authentication & Security
**Question:** How to secure the production dashboard?

**Current state:**
- No authentication (anyone with URL can access)
- API keys in `.env` file (not committed to git)
- OAuth credentials uploaded via UI

**Security needs:**
- Protect API keys (SERPAPI_KEY, Gmail credentials)
- Restrict access to production dashboard (password/login)
- Public demo mode with sample data (no real API calls)

**Options:**
- **Netlify Identity** (user login)?
- **Password protection** (simple Streamlit auth)?
- **Environment-based** (public demo vs. private production)?
- **OAuth** (Google Sign-In)?

**Question:** What's the simplest way to add authentication for production while keeping demo public?

---

### 6. Domain & SSL
**Question:** Custom domain setup steps?

**Desired setup:**
- Primary domain: `wsp2agent.netlify.app` (or custom domain if we have one)
- SSL certificate (auto via Netlify?)
- Redirect HTTP → HTTPS

**Question:** Any special configuration needed for Streamlit on custom domain?

---

### 7. CI/CD & GitHub Integration
**Question:** Auto-deploy from GitHub on push?

**Current GitHub setup:**
- Repo: `WSP001/WSP2agent`
- Branch: `main`
- Tag: `v3.0.0`

**Desired workflow:**
1. Push to `main` branch
2. Netlify auto-builds and deploys
3. Run tests before deploy (`pytest tests/test_pipeline.py`)
4. Rollback on failure

**Question:** Can we configure this via Netlify UI, or do we need `netlify.toml` config?

---

## 📋 SPECIFIC IMPLEMENTATION QUESTIONS

### A. Build Configuration
**Question:** What should our build settings be?

**Current guess:**
```toml
[build]
  command = "pip install -r requirements.txt"
  publish = "streamlit_app"
  
[build.environment]
  PYTHON_VERSION = "3.11"
```

**Questions:**
- Is there a Streamlit-specific build command?
- How to specify `streamlit run streamlit_app/app.py` as the start command?
- Do we need a `Procfile` or `netlify.toml`?

---

### B. Requirements & Dependencies
**Question:** Any issues with our dependencies on Netlify?

**Potentially problematic packages:**
- `selenium` - Requires Chrome/ChromeDriver binaries
- `reportlab` - May need system fonts
- `google-api-python-client` - Large dependency tree

**Question:** Will these install cleanly, or do we need custom buildpacks/Docker?

---

### C. Streamlit Configuration
**Question:** Streamlit config for production?

**Current local settings** (not in repo):
```toml
# .streamlit/config.toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

**Question:** Should we commit this to repo, or set via environment variables?

---

### D. Demo Mode vs. Production Mode
**Question:** How to implement two deployment modes?

**Demo Mode (Public):**
- Uses sample data from `data/top10_landlords.csv` (committed to repo)
- Buttons show simulated results (no real API calls)
- No authentication needed
- URL: `demo.wsp2agent.com` or `wsp2agent.netlify.app/demo`

**Production Mode (Private):**
- Uses real SERPAPI_KEY and Gmail OAuth
- Actually sends emails and fetches data
- Requires login
- URL: `app.wsp2agent.com` or `wsp2agent.netlify.app/app`

**Question:** How to deploy two versions? (Separate sites? Environment variable switch? Branch-based?)

---

## 🧪 TESTING & VALIDATION CHECKLIST

**Before going live, we need to verify:**

- [ ] All dependencies install successfully
- [ ] Streamlit UI loads (homepage, all 6 tabs)
- [ ] Environment variables accessible (`os.getenv("SERPAPI_KEY")`)
- [ ] File read/write works (`data/` directory)
- [ ] Demo mode works (using sample CSV data)
- [ ] Search button works (calls SerpAPI, saves JSON)
- [ ] Scrape button works (fetches URLs, extracts contacts)
- [ ] CSV tables display correctly (pandas dataframes)
- [ ] PDF generation works (`reportlab` library)
- [ ] Email composition works (templates + variables)
- [ ] Gmail OAuth flow works (credentials.json → token.json)
- [ ] Logs are viewable (activity log tab)
- [ ] Mobile responsive (Streamlit default responsive layout)
- [ ] SSL certificate active (HTTPS)
- [ ] Custom domain resolves (if applicable)

---

## 🎨 UI/UX FEATURES TO PRESERVE

**Our dashboard is "beautiful and user-friendly" - please ensure:**

1. **6-tab layout** (Dashboard, Search & Scrape, Review & Approve, Send Emails, Track Replies, Settings)
2. **Colored progress indicators** (✅ green success, ⚠️ yellow warnings, ❌ red errors)
3. **Real-time spinners** ("Running search → scrape → curate...")
4. **Metric cards** (Search Results count, Scraped Contacts count, Approved Contacts count)
5. **Interactive tables** (sortable, filterable dataframes)
6. **One-button workflows** ("Run Full Pipeline", "Generate PDFs", "Send Emails")
7. **Safety gates** (confirmation prompts before sending >3 emails)
8. **Status checks** (sidebar shows SERPAPI_KEY, credentials.json, token.json status)

**These make it "pre-programmed button options execute and result show up on the same beautifully created front facing intuitive" interface.**

---

## 🚨 CRITICAL SAFETY REQUIREMENTS

**MUST preserve these safety features:**

1. **Email send limit:** Never send >3 emails without explicit user confirmation
2. **Dry-run mode:** All buttons have dry-run option (shows preview without executing)
3. **Approval workflow:** Users must check boxes in "Review & Approve" tab before emails are sent
4. **Audit trail:** All actions logged to `data/sandbox/logs/` with timestamps
5. **API key validation:** Show error if SERPAPI_KEY missing (don't crash silently)
6. **OAuth flow:** Safe redirect back to app after Gmail authentication
7. **Error handling:** User-friendly error messages (not Python stack traces)

---

## 🔄 BONUS: SELENIUM INTEGRATION (Housing Search Use Case)

**Context:** We built a working Selenium scraper prototype for Craigslist contact enrichment.

**Files:**
- `modules/selenium_driver.py` - Chrome WebDriver factory
- `scripts/craigslist_contact_enricher.py` - Scraper with CLI args
- `test_workflow.ps1` - PowerShell test script (local only)
- `CHROMEDRIVER_SETUP.md` - Installation guide

**Current workflow (local):**
1. User runs `test_workflow.ps1`
2. Script checks Chrome version, ChromeDriver installation
3. Runs Selenium scraper on CSV file (clicks "reply" buttons, extracts hidden emails)
4. Shows enriched results in terminal

**Ideal Netlify integration:**
- Add "Enrich Contacts (Selenium)" button to "Search & Scrape" tab
- Button triggers Netlify Function that:
  1. Loads `data/top10_landlords.csv`
  2. Runs headless Chrome/Selenium on each URL
  3. Extracts hidden emails/phones from "reply" modals
  4. Updates CSV with new contacts
  5. Shows progress spinner → Success message

**Question:** Is this feasible on Netlify, or should Selenium run elsewhere (separate worker, external service)?

**Use case importance:** This proves WSP2AGENT modularity beyond housing search - it's a "prototype around THIS USE WORKFLOW case" that demonstrates value for any web scraping task.

---

## 📝 NEXT STEPS AFTER YOUR RESPONSE

**Once you answer these questions, I will:**

1. **Create `netlify.toml`** with your recommended build configuration
2. **Update `requirements.txt`** if needed (Docker, buildpacks, etc.)
3. **Add environment variable template** (`.env.example.netlify`)
4. **Configure authentication** (Netlify Identity, password, etc.)
5. **Set up file storage** (Netlify Blobs, S3, Supabase, etc.)
6. **Deploy to staging** (test all features)
7. **Set up custom domain** (if applicable)
8. **Enable CI/CD** (GitHub auto-deploy)
9. **Add demo mode toggle** (public vs. private)
10. **Test Selenium integration** (or alternative scraping solution)

---

## 🎯 SUMMARY OF QUESTIONS FOR NETLIFY AGENT

### Must-Answer (Blockers):
1. **How to host Streamlit on Netlify?** (Functions, Docker, external?)
2. **How to run Selenium?** (Puppeteer, Playwright, external service?)
3. **How to handle long-running tasks?** (Background Functions, queues, split workflows?)
4. **Where to store files?** (Blobs, S3, databases?)
5. **How to persist OAuth tokens?** (token.json across deploys)

### Should-Answer (Quality):
6. **How to add authentication?** (Netlify Identity, simple password?)
7. **Build configuration?** (netlify.toml, Procfile, environment?)
8. **Auto-deploy from GitHub?** (CI/CD setup steps)

### Nice-to-Answer (Enhancements):
9. **Demo vs. Production modes?** (Separate sites, branches, env vars?)
10. **Custom domain setup?** (DNS, SSL, redirects)

---

## 📚 REFERENCE FILES TO REVIEW

If you need more context, please ask to see:
- `streamlit_app/app.py` - Main UI code (500+ lines)
- `requirements.txt` - All dependencies
- `README.md` - Project overview and architecture
- `modules/selenium_driver.py` - Selenium setup
- `LAUNCH_APP.ps1` - Local launcher (shows startup flow)
- `.gitignore` - What we're NOT deploying

---

## 🌟 VISION STATEMENT

**Goal:** Deploy a production-quality dashboard that:
- ✅ Works for **any automated outreach workflow** (not just housing search)
- ✅ Looks **beautiful and professional** ("For the Commons Good" quality)
- ✅ Has **one-button execution** with smart defaults
- ✅ Runs **safely and securely** (API keys protected, approval gates)
- ✅ Scales to **Netlify.com Agent Pro integration** (serverless functions, webhooks)

**Robert's vision:** "User friendly dashboard pre-programmed button options execute and result show up on the same beautifully created front facing intuitive interface."

**This is the foundation for "miraculous things" we'll build next with Netlify.com Agent Pro!** 🚀🌍

---

**END OF REQUIREMENTS DOC**

*Generated: 2025-01-13*  
*WSP2AGENT V3.0.0*  
*For: Netlify Deployment Agent*
