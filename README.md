# WSP2AGENT V3 🚀

![Version](https://img.shields.io/badge/version-3.0.0-blue) ![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen) ![Status](https://img.shields.io/badge/status-production--ready-success) ![License](https://img.shields.io/badge/license-MIT-green)

**Modular Automated Outreach System — For the Commons Good 🌍**

A production-ready, **truly modular** application that works for:
- ✅ **World Seafood Producers** (original use case)
- ✅ **Housing/Roommate searches** (Robert's Winter Haven test case)
- ✅ **B2B lead generation**
- ✅ **Commercial real estate outreach**
- ✅ **Non-profit volunteer recruitment**
- ✅ **ANY automated contact workflow:** Search → Scrape → Curate → Email → Track

**Pipeline:** (1) searches public listings (SerpAPI), (2) scrapes pages for contact info (Selenium), (3) curates candidates with scoring, (4) generates personalized PDFs, (5) composes and sends emails (Gmail API), (6) monitors replies with complete audit trail — all with an intuitive web interface, smart error handling, and human-in-the-loop approval gates.

**🎉 NEW in V3:**
- **60-second quick start** (down from 30 minutes!)
- **Zero-setup demo mode** with sample data
- **Smart error assistant** with auto-repair (5 error types)
- **Activity logging** with complete audit trail
- **Feature voting** (users vote for next AI features)
- **7-tab professional UI** with welcome wizard
- **Cross-platform launcher** with auto-dependency management
- **1800+ lines of documentation**

Built for everyone: from non-technical users to developers. **Modularity proven with test cases!**

---

## ⚡ Quick Start (60 Seconds)

```bash
# Launch the app
python launcher.py

# Choose "Try With Demo Data" for instant demo
# Or "Full Setup" for production use
```

**That's it!** See [GETTING_STARTED_V3.md](GETTING_STARTED_V3.md) for detailed walkthrough.

---

## 📚 Documentation

- **[Getting Started](GETTING_STARTED_V3.md)** - 60-second quick start + first workflow
- **[V3 Features](V3_FEATURES.md)** - Complete feature documentation (500+ lines)
- **[V3 Build Summary](V3_BUILD_SUMMARY.md)** - What we built and why
- **[Version Comparison](V1_V2_V3_COMPARISON.md)** - V1 vs V2 vs V3 differences
- **[Round 2 Summary](ROUND2_SUMMARY.md)** - Round 2 improvements
- **[Quick Start](QUICKSTART.md)** - Original quick start guide

---

## Quick overview

**Core pipeline stages**
1. **Search stage** — run targeted queries and save `search_results.json`.  
2. **Scrape stage** — fetch pages, extract emails/phones, write `data/contacts_raw.csv`.  
3. **Curate stage** — score and produce `data/top10_landlords.csv` (human review).  
4. **PDF stage** — `make_personal_pdfs.py` → `personal_flyer_1..10.pdf`.  
5. **Compose stage** — generate email bodies saved to `data/top10_outreach_emails.txt`.  
6. **Approval** — human inspects `data/top10_landlords.csv` and approves test sends (1–3).  
7. **Send stage** — `send_emails_gmail.py` sends approved emails (Gmail API/OAuth).  
8. **Monitor stage** — `replier.py` polls Gmail for replies and saves `data/responses.csv`.  
9. **Follow-up** — manual or agent-driven follow-up sequences.

---

## Project layout (seed)

```
WSP2AGENT/
├─ README.md
├─ .env.example
├─ requirements.txt
├─ run_pipeline.py
├─ modules/
│  ├─ searcher.py
│  ├─ scraper.py
│  ├─ curator.py
│  ├─ pdfs.py
│  ├─ composer.py
│  ├─ gmailer.py
│  ├─ replier.py
│  ├─ broker.py
│  └─ worker.py
│  └─ utils.py
├─ scripts/
│  ├─ make_personal_pdfs.py
│  ├─ send_emails_gmail.py
│  └─ run_wsp.ps1
├─ data/
│  ├─ contacts_raw.csv
│  ├─ top10_landlords.csv
│  └─ responses.csv
├─ workflows/
│  └─ pipeline.yml
└─ docs/
└─ operation.md
```

---

## Quick start (local)

1. **Clone repo (VS Code recommended)**
   ```bash
   git clone git@github.com:YOUR_USERNAME/WSP2AGENT.git
   cd WSP2AGENT
   code .
   ```

2. **Create a Python virtual env & install deps**

   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Copy `.env.example` → `.env` and set your values**

   * `SERPAPI_KEY` (your SerpApi key)
   * `GMAIL_CREDENTIALS_PATH` (path to your `credentials.json` for Gmail API)
   * `GMAIL_SENDER_EMAIL` (e.g., `worldseafood@gmail.com`)
   * Optionally `DATA_DIR`, `LOG_LEVEL`, `SEARCH_LOCATION`

4. **Run the pipeline (dry-run style)**

   ```bash
   python run_pipeline.py --dry-run
   ```

   The orchestrator will create `data/contacts_raw.csv` and `data/top10_landlords.csv` (if modules present) and stop at the approval checkpoint.

5. **Generate PDFs**

   ```bash
   python scripts/make_personal_pdfs.py
   ```

6. **Test send** (use Gmail sandbox/test email first)

   * Create `credentials.json` following the Gmail API quickstart (Desktop app OAuth).
   * Run `python scripts/send_emails_gmail.py` — it will perform an OAuth flow and save `token.json`.

7. **Package & worker flow (optional, recommended)**

   * Create sandbox packages for rows marked `approved=True`:
     ```bash
     python -c "from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv', pdf_dir='out')"
     ```
   * Inspect `data/sandbox/outbox/` for `package_*.json` files and `data/packages.db` for metadata.
   * Run the worker in dry-run mode to preview sends:
     ```bash
     python -c "import modules.worker as w; w.poll_and_send(dry_run=True)"
     ```
   * When satisfied, rerun with `dry_run=False` to send real emails (requires Gmail OAuth setup from step 6). Packages will move to `data/sandbox/sent/` or `data/sandbox/failed/`.

---

## Environment & secrets

* Use `.env` for local testing (do **not** commit).
* In production / CI use **GitHub Secrets** to store `SERPAPI_KEY` and `GMAIL_CREDENTIALS_BASE64` (or mount secret files).
* Revoke API keys when finished.

---

## Safety & rules

* **Manual approval required** before sending to more than 3 contacts.
* Respect target platforms’ terms of service and rate limits.
* Avoid emailing generic addresses (`webmaster@`, `no-reply@`) unless they are valid admin contacts.
* Always start with a small test batch.

---

## Extending the agent

* Add new search queries via `modules/searcher.py`.
* Improve the curator scoring or add a small ML classifier.
* Swap SerpApi for Bing or another provider by updating `modules/searcher.py`.
* Add a Streamlit UI for one-click runs and approval.

---

## Developing with AI coding assistants

We provide `prompts/` guidance in this repo. Use Copilot/Gemini/Claude to generate module implementations from the prompts.

## Agent-to-agent broker workflow

The repo now includes an optional multi-agent layering:

* **Broker (`modules/broker.py`)** reads curated rows, matches PDFs/drafts, stores canonical packages in `data/packages.db`, and writes JSON packages into `data/sandbox/outbox/`.
* **Worker (`modules/worker.py`)** polls the outbox, performs a dry-run or live Gmail send, logs the result, and moves packages to `sent/` or `failed/`.
* **Audit trail** lives in the sandbox directories plus the sqlite database; you can retry failed packages or hand them off to other delivery channels (SMS/DM adapters).

### One-click helpers

* **VS Code tasks** (`.vscode/tasks.json`) expose buttons such as “WSP: Dry Run Pipeline”, “WSP: Broker → Packages”, and “WSP: Worker (Dry Send)”.
* **PowerShell launcher** (`scripts/run_wsp.ps1`) provides a numbered menu so you can kick off common actions without retyping commands. Create a desktop shortcut to this script for an instant “Click2Kick” experience.

---

## License & contribution

Suggested license: **MIT** (simple, permissive).
Add `CONTRIBUTING.md` and `ISSUE_TEMPLATE` later for team workflows.

---

## Need help?

If you want, I can:

* Seed the repo with working stubs for each module; or
* Run the SerpApi sweep for Winter Haven (with your key) and upload `contacts_raw.csv` and curated top-10; or
* Walk you step-by-step through Gmail API setup and a safe test send.

Choose what you want next and I’ll provide exact commands.

---

## Copilot / Gemini / Claude prompts

### `modules/searcher.py` prompt

```text
Write a Python module `modules/searcher.py` with a function `run_searches(api_key=None, queries=None, location=None)` that uses SerpApi (GoogleSearch) to run a list of search queries. The function should return a list of result dicts (title, link, snippet). Use default queries for "Winter Haven room for rent owner, for rent by owner, home share, caretaker". Include conservative rate limiting and graceful error handling. Do not write any global code; only the function.
```

### `modules/scraper.py` prompt

```text
Write a Python module `modules/scraper.py` with functions:
- `page_emails_phones(url)` -> (emails, phones) using requests + regex/BeautifulSoup
- `scrape_results(search_results_path_or_list, out_csv)` which reads a JSON file or accepts a list of result dicts, fetches each result url, extracts emails/phones/snippet/title and writes a CSV with columns organization,url,emails,phones,snippet.
Add simple retry logic and skip pages that timeout.
```

### `modules/curator.py` prompt

```text
Write a Python module `modules/curator.py` with a function `curate_contacts(input_csv, out_csv, top_n=10)` that:
- reads contacts_raw.csv,
- computes a score by keywords (owner, owner-occupied, caretaker, homeshare, silvernest, senior, library, church),
- penalizes property-management and large corporate keywords,
- sorts by score, and writes top_n rows to out_csv including a 'score' column.
```

### `modules/pdfs.py` prompt

```text
Write a Python module `modules/pdfs.py` with a function `make_personal_pdfs(top10_csv, out_dir)` that reads top10 CSV and creates one PDF per row using reportlab. PDFs should include organization, contact_name, listing URL, notes, a short pitch text, and contact info. Name files personal_flyer_1_<org>.pdf.
```

### `modules/composer.py` prompt

```text
Write a Python module `modules/composer.py` with a function `compose_emails(top10_csv, out_file)` that creates HTML and plain-text email drafts for each row and writes them to out_file (one per line, or as a JSON array). Use context placeholders for organization, contact_name, listing url, and suggested subject.
```

### `modules/gmailer.py` prompt

```text
Write a Python module `modules/gmailer.py` with:
- `gmail_auth(scopes)` to do OAuth flow using credentials.json and produce token.json.
- `send_approved_emails(top10_csv)` that reads CSV rows flagged `approved=TRUE` and sends each email (subject and body composed by composer) attaching matching personal_flyer_<n>.pdf. Add logging and error handling. NEVER send more than 3 emails at once without human confirmation; implement a safety check that asks for input before sending >3.
```

### `modules/replier.py` prompt

```text
Write a Python module `modules/replier.py` with a function `fetch_replies(query, out_csv)` that authenticates with Gmail API, searches for recent messages matching the outreach subject prefix (e.g., "Seeking Room"), extracts From, Subject, Date, and snippet, and appends to responses.csv. Add an optional function `summarize_reply(text)` that calls an LLM (stub) to summarize intent and next action.
```

### `modules/utils.py` prompt

```text
Write small utilities: safe_file_write, read_csv, normalize_email_list, slugify_filename. Keep simple and testable.
```

---

## Suggested license & GitHub Apps

**License**: MIT or Apache 2.0 (MIT is simplest). Create `LICENSE` with chosen license text.

**GitHub Apps to connect** (recommended):

* **GitHub Actions** (builtin) — CI + manual triggers.
* **Dependabot** — auto dependency updates.
* **Codespaces** (optional) — cloud dev environment.
* **Secrets & Encrypted storage** — use GitHub Secrets for `SERPAPI_KEY`, Gmail creds.
* **Code scanning (CodeQL)** — optional security scans.

External integrations:

* **Google Cloud (Gmail API)** — OAuth credentials.
* **SerpApi** — search queries.
* **Google Drive (optional)** — to upload PDFs.
* **Slack / Email** — for status notifications.

---

## What to commit first (starter checklist)

1. Create repo `WSP2AGENT` on GitHub.
2. Add files: `README.md`, `.env.example`, `requirements.txt`, `run_pipeline.py`, `.gitignore` (from above).
3. Create directories: `modules/`, `scripts/`, `data/`, `workflows/`, `docs/`. Add empty `__init__.py` in modules if desired.
4. Commit & push:

   ```bash
   git add .
   git commit -m "Seed WSP2AGENT: readme, env, requirements, run_pipeline"
   git push origin main
   ```
5. Add GitHub Secrets: `SERPAPI_KEY` (if you plan to run Actions), and `GMAIL_CREDENTIALS_BASE64` (optional). Do **not** add private `credentials.json` to the repo.

---

## Next steps I can do for you

Pick any:

* **A.** I will create the repo skeleton and return the GitHub URLs/content for you to copy.
* **B.** I will generate the initial module stubs and push them into the repo (if you give me repo write access or paste back a copy).
* **C.** I will run the SerpApi sweep (you already provided a key earlier) and produce `contacts_raw.csv` and `top10_landlords.csv` and upload them to `worldseafood@gmail.com` (I will only prepare files and not send emails).
* **D.** I will coach you step-by-step to run everything locally in VS Code and test the Gmail API.

Tell me which of A/B/C/D you want next. If A, I’ll push the seed (or paste full file list) so you can create the repo locally. If C, please confirm again that I should use your SerpApi key and upload to `worldseafood@gmail.com` (I will not send any emails).

---

### Final notes

* This skeleton is **reusable**: change `SEARCH_QUERIES` and templates and the same pipeline will work for other outreach tasks.
* We’ll keep all outgoing send actions gated behind an approval step — safety first.
* I’ll be your teacher and implementation partner — tell me **which of A/B/C/D** and I’ll do the next action and provide exact copy/paste commands.

Which option should I run next?
