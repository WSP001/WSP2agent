# WSP2AGENT

**World Seafood Producers — Agent for Outreach & Matchmaking**  
A modular Python agent that: (1) searches public listings (SerpApi/Bing), (2) scrapes pages for contact info, (3) curates candidate landlords, (4) generates personalized PDFs, (5) composes and sends test emails (Gmail API), (6) monitors replies and logs them — all with human-in-the-loop approval gates.

This repo is intentionally modular and reusable for other outreach tasks beyond THIS USE CASE TO STUDY.

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

## FIRST Project layout (seed) EXAMPLE:
WSP2AGENT/
├─ README.md
├─ .env.example
├─ requirements.txt
├─ run_pipeline.py
├─ modules/
│ ├─ searcher.py
│ ├─ scraper.py
│ ├─ curator.py
│ ├─ pdfs.py
│ ├─ composer.py
│ ├─ gmailer.py
│ ├─ replier.py
│ └─ utils.py
├─ scripts/
│ ├─ make_personal_pdfs.py
│ └─ send_emails_gmail.py
├─ data/
│ ├─ contacts_raw.csv
│ ├─ top10_landlords.csv
│ └─ responses.csv
├─ workflows/
│ └─ pipeline.yml
└─ docs/
└─ operation.md

python scripts/make_personal_pdfs.py

