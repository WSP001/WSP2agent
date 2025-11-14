# FOR MY GPT - WSP2AGENT V3 Context & Data

## ✅ REPOSITORY STATUS
- **Correct Repo:** https://github.com/WSP001/WSP2agent ✅
- **Branch:** main
- **V3 Pushed:** 63 files, 9,233+ lines
- **Tag:** v3.0.0
- **Status:** Production-ready, awaiting final testing

---

## 📊 OPTION 3: TOP 10 LANDLORDS CSV DATA (FOR EMAIL/PDF CRAFTING)

Here are the **top 9 rows** from `data/top10_landlords.csv`:

```csv
organization,url,emails,phones,snippet,score,approved
Senior House Sharing Is on the Rise,https://seniorplanet.org/senior-house-sharing-is-on-the-rise/,info@seniorplanet.org,,Silvernest can also draw up leases and collect rents. Because the ... I am lookng to purchase a home in WI and would like to home share with ...,11,True
The Caucus Corner - NCBA,https://ncba-aging.org/wp-content/uploads/2023/01/December-November-2022-Caucus-Corner-newsletter-A.pdf,Q@dh.VL;covided@ncba-aging.org,800-272-3900;800-677-1116;855-260-3274,"Companies such as Silvernest and Senior Homeshares provide help with background screening, creating a lease, and matching roommates. Find other resources to ...",11,True
(PDF) PSU Student Housing Insecurity Report,https://www.researchgate.net/publication/382299045_PSU_Student_Housing_Insecurity_Report,,,"... Silvernest and their local partner Oregon Home Share facilitate room rentals by homeowners,. but aren't focused specifically on college students. Such ...",9,True
OLDER ADULT 2020 HOUSING NEEDS ASSESSMENT,https://www.nwccog.org/wp-content/uploads/2021/04/Older-Adult-Housing-Needs-Study_REV2.pdf,1qkY46@oB9LM.MJsU;B@Jh.gEB;QEp@Ue.LX;TN@eM.SPV;V@n7iH.lVoMk;Z+@D.cXEdk,587 293 1000;797 714 1009;992.339 1231,Income and companionship are also attractive for home sharing consideration. Colorado Home Share Program Examples: ▫ Silvernest – Statewide (silvernest.com).,8,False
"Home sharing, backyard cottages and renting out rooms ...",https://www.ocregister.com/2022/10/02/home-sharing-backyard-cottages-and-renting-out-rooms-help-seniors-find-housing-solutions/,JeffCollins@scng.com,,"A website called Silvernest helped Jocelyn McCormick, 78, find a roommate after her husband died last spring. The online site pairs home seekers ...",8,False
March | 2022 - CMCAcorner.com,https://cmcacorner.com/2022/03/,info@camicb.org,,"... Silvernest, which pairs older adults with housemates. The service is ... Home Share Colorado, Bolding found two more housemates. Since ...",8,False
Florida Department of Elder Affairs,https://elderaffairs.org/,information@elderaffairs.org,(239) 652-6900;(305) 670-4357;(352) 378-6649;(407) 514-0019;(561) 684-5885;(727) 217-8111;(800) 262-2243;(800) 336-2226;(813) 740-3888;(850) 414-2000;(850) 488-0055;(850) 494-7101;(866) 413-5337;(866) 467-4624;(866) 531-8011;(866) 684-5885;(888) 242-4464;(904) 391-6600;(954) 745-9779;800-963-5337,Background Screening Contact Information · Exemption from ... Florida Senior Center Survey · 2023 Medicaid Update · Mental Wellness · More Press ...,8,False
For Rent by Owner in Winter Haven FL - 12 Rentals,https://www.forrent.com/find/FL/metro-Tampa+Bay/Winter+Haven/extras-For+Rent+by+Owner-Rentals,,,"12 For rent by owner in Winter Haven, FL. Filter by price, bedrooms and amenities. High-quality photos, virtual tours, and unit level details included.",6,False
"Room for rent in Winter Haven, FL, near hospitals",https://www.facebook.com/groups/TravelNurseHousingUSA/posts/1749713002623853/,,,"Room for rent in Winter Haven, FL $950/mth. Close to both Winter ... Fran Golino ▻ For RENT By Owner FLORIDA. 10w · Public · SNOWBIRDS ...",6,False
```

**Context for GPT:**
- **Searcher Profile:** Robert, looking for housing in Winter Haven, FL (33880), $400-$700/month budget
- **Use Case:** Housing/roommate search (demonstrating modularity beyond seafood)
- **Current Status:** 9 leads found, top 3 have `approved=True`
- **Email Format Needed:** Professional outreach explaining Robert's situation, skills, references available
- **PDF Assets Available:** 
  - Bulletin flyer with tear-off tabs
  - Service-for-housing agreement template
  - Reference form
  - Background check consent
  - Skills resume
  - Business cards

**YOUR GPT'S TASK (Option 3):**
Please **select the best 3 leads** from the above CSV and **craft polished email copy + PDF text inserts** for:

1. **Lead Selection Criteria:**
   - Valid email address (not garbled)
   - Relevant to Winter Haven, FL or Florida housing
   - Score ≥ 8
   - Organization seems legitimate/responsive

2. **Email Template Needed for Each Lead:**
   - Subject line
   - Personalized greeting
   - Robert's introduction (brief, professional)
   - Housing need explanation (Winter Haven area, budget $400-$700)
   - Value proposition (reliable tenant, skills to offer)
   - Call-to-action (view attached PDFs, schedule call)
   - Professional signature

3. **PDF Text Inserts:**
   - Bulletin flyer headline + tear-off tab text
   - Service agreement key terms
   - 3-5 bullet points for skills resume

---

## 🔧 OPTION 2: CHROME & CHROMEDRIVER INFORMATION

**Chrome Installation Status:**
- **Path Found:** `C:\Program Files\Google\Chrome\Application\chrome.exe` ✅
- **Version:** Unable to detect via PowerShell (commands timing out)
- **Manual Check Needed:** User should run `chrome://version` in browser OR check via GUI

**ChromeDriver Status:**
- **Not Found** in common locations:
  - `C:\chromedriver.exe`
  - `C:\WebDriver\chromedriver.exe`
  - `C:\Program Files\ChromeDriver\chromedriver.exe`
  - User's Downloads folder
- **Not in PATH** environment variable

**YOUR GPT'S TASK (Option 2):**
Please provide **tailored Selenium script** with these specifications:

### Questions for User (to fill in script):

1. **Chrome Version:**
   - Where to check: Open Chrome → Three dots menu → Help → About Google Chrome
   - Example: "131.0.6778.86" or "130.x.x.x"
   - Format needed: `CHROME_VERSION = "131.0.6778"`

2. **Preferred ChromeDriver Path:**
   - Option A: `C:\WebDriver\chromedriver.exe` (recommended)
   - Option B: `C:\Users\Roberto002\My Drive\WSP2AGENT\drivers\chromedriver.exe` (in repo)
   - Option C: Custom path (user specifies)
   - Format needed: `CHROME_DRIVER_PATH = r"C:\WebDriver\chromedriver.exe"`

3. **Test URL Parameters:**
   - Example Craigslist listing URL for Winter Haven, FL
   - Expected contact extraction: email and/or phone
   - Format needed: `TEST_URL = "https://...craigslist.org/..."`

4. **CSV Update Mode:**
   - Should script UPDATE existing `data/top10_landlords.csv`? (YES - recommended)
   - Or create new file? (NO)
   - Format needed: `UPDATE_EXISTING_CSV = True`

### Script Requirements:

```python
# scripts/craigslist_reply_scrape.py - TAILORED VERSION NEEDED

# Configuration (GPT: please fill with user's values)
CHROME_VERSION = "___"  # e.g., "131.0.6778"
CHROME_DRIVER_PATH = r"___"  # e.g., r"C:\WebDriver\chromedriver.exe"
TEST_URL = "___"  # Craigslist listing for testing
UPDATE_EXISTING_CSV = True  # Update data/top10_landlords.csv

# Features needed:
# 1. Auto-download chromedriver if not found (using webdriver_manager)
# 2. Headless mode option (for CI/CD)
# 3. Wait for JS-rendered content (implicit/explicit waits)
# 4. Extract: emails (mailto:, text patterns), phones (regex)
# 5. Click "reply" button if present
# 6. Handle CAPTCHA (pause + manual intervention option)
# 7. Write back to CSV (enrich emails/phones columns)
# 8. Logging (success/failure for each URL)
# 9. Error handling (stale elements, timeouts)
# 10. Usage example at bottom with TEST_URL

# GPT: Please provide complete script with:
# - Installation instructions (pip install selenium webdriver-manager)
# - Download ChromeDriver instructions if manual install needed
# - Usage examples (single URL test, batch CSV enrichment)
# - Safety notes (rate limiting, politeness delay)
```

---

## 🎯 INTEGRATION CONTEXT (For GPT Awareness)

**What happens after GPT provides responses:**

### After Option 3 (Emails/PDFs):
1. We'll insert GPT's email copy into `data/top10_outreach_emails.json`
2. Generate PDFs with GPT's text using `scripts/generate_roberts_housing_pdfs.py`
3. Test send (dry-run) to verify formatting
4. Real send to top 3 approved leads
5. Rotate SerpAPI key after campaign

### After Option 2 (Selenium Script):
1. User provides Chrome version + desired path
2. GPT generates tailored `scripts/craigslist_reply_scrape.py`
3. We test with one URL first (dry-run)
4. Batch enrich all CSV rows missing emails/phones
5. Re-run Option 3 with enriched data for better targeting

**Safety Gates in Place:**
- ✅ Dry-run mode for all pipeline stages
- ✅ Human approval required before real sends
- ✅ Max 3 emails per batch (UI warning if >3)
- ✅ Gmail OAuth (no plaintext passwords)
- ✅ `.gitignore` protects credentials.json, token.json
- ✅ Activity logging for audit trail

**Netlify.com Agent Pro Integration (Next Phase):**
- Each pipeline module becomes serverless function
- Button triggers in UI → Netlify function calls
- Environment variables for API keys (secured)
- Dashboard hosted on Netlify (static + functions)
- Webhook triggers for scheduled campaigns

---

## 📋 FORMAT FOR GPT RESPONSE

### If GPT chooses OPTION 3 (Emails + PDFs):

**Please provide in this format:**

#### Selected Leads (3 best):
1. **Lead Name/Organization** - Email - Score - Why chosen
2. **Lead Name/Organization** - Email - Score - Why chosen  
3. **Lead Name/Organization** - Email - Score - Why chosen

#### Email Copy (for each lead):

**LEAD 1: [Organization Name]**
```
Subject: [subject line]

[Email body with personalization]
```

**LEAD 2: [Organization Name]**
```
Subject: [subject line]

[Email body with personalization]
```

**LEAD 3: [Organization Name]**
```
Subject: [subject line]

[Email body with personalization]
```

#### PDF Text Inserts:

**Bulletin Flyer:**
- Headline: [text]
- Tear-off tabs (10x): [text]

**Skills Resume (5 bullet points):**
- [bullet 1]
- [bullet 2]
- [bullet 3]
- [bullet 4]
- [bullet 5]

**Service Agreement Key Terms:**
- [term 1]
- [term 2]
- [term 3]

---

### If GPT chooses OPTION 2 (Selenium Script):

**Please ask user these questions:**

1. What is your Chrome version? (Check: chrome://version)
2. Where should ChromeDriver be installed?
   - A) `C:\WebDriver\chromedriver.exe` (recommended)
   - B) In repo: `C:\Users\Roberto002\My Drive\WSP2AGENT\drivers\`
   - C) Custom path: [specify]
3. Test Craigslist URL (Winter Haven, FL listing)?

**Then provide:**
- Complete `scripts/craigslist_reply_scrape.py` with user's values
- Installation instructions (ChromeDriver download link for their Chrome version)
- Usage examples (single URL test + batch CSV mode)
- Safety notes

---

## ✅ READY FOR GPT

**This file contains:**
- ✅ CSV data (9 rows) for lead selection
- ✅ Chrome/ChromeDriver detection results
- ✅ Use case context (Robert's housing search)
- ✅ Pipeline safety gates documented
- ✅ Netlify integration roadmap
- ✅ Clear format for GPT responses

**Please share this with your GPT and request:**
1. **OPTION 3** response (select 3 leads + craft emails/PDFs), AND/OR
2. **OPTION 2** questions (to tailor Selenium script)

**We can do BOTH** - Option 2 first (get script ready), then Option 3 with enriched data!

For the Commons Good 🌍
