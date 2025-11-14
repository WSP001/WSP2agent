# 🎯 WSP2AGENT AUTOMATION GUIDE
**All User-Friendly Commands & Features**

---

## ✨ NEW FEATURES ADDED

### 1. **Mission Control UI Enhancements**

#### Tab 1: Run New Campaign — Quick Actions Bar
- **🔄 Full Pipeline** — One-click search → scrape → curate
- **🔍 Preview Queries** — See active search queries before running
- **📞 Setup OAuth** — In-UI button with copy/paste command
- **🧹 Clear Sandbox** — Reset outbox/sent/failed folders

#### Tab 2: Approve & Send — Quick Actions Bar
- **✅ Approve Top 3** — One-click bulk approval (marks first 3 rows)
- **📥 Export Bundle** — Download ZIP with CSV + JSON + search results
- **🔄 Refresh Data** — Reload current data without browser refresh
- **📊 View Stats** — Quick stats popup (approved count, emails, phones, avg score)

#### Enhanced Status Dashboard
- **Live Metrics** with color-coded deltas
- **OAuth Status Indicator** (✅ Ready / ⚠️ Setup needed)
- **Approved Count** tracker (X/3 recommended)

---

## 🚀 AUTOMATED SCRIPTS

### 1. **Full Automation** (`run_full_automation.ps1`)
Runs complete workflow automatically:
1. Pipeline (search → scrape → curate)
2. Auto-approve top 3
3. Generate email drafts
4. Build packages
5. Dry-run send

**Usage:**
```powershell
.\scripts\run_full_automation.ps1
```

### 2. **Command Menu** (`command_menu.ps1`)
Interactive menu with 40+ commands organized by category:
- Quick Start
- Pipeline Operations
- Data Review
- Approval Operations
- Package & Send
- OAuth & Gmail
- Cleanup & Maintenance
- Status & Monitoring

**Usage:**
```powershell
.\scripts\command_menu.ps1
```

### 3. **Launch Mission Control** (`launch_mission_control.ps1`)
Pre-flight checks + interactive launcher:
- Checks venv, OAuth, data files
- Upgrades SerpApi client
- Menu: Launch UI / Run pipeline / View data

**Usage:**
```powershell
.\scripts\launch_mission_control.ps1
```

### 4. **Test Top-3 Workflow** (`test_top3_workflow.ps1`)
Quick test: Approve → Package → Dry-send

**Usage:**
```powershell
.\scripts\test_top3_workflow.ps1
```

---

## 📋 ESSENTIAL COMMANDS (Quick Reference)

### Pipeline Operations
```powershell
# Full pipeline (dry-run)
python run_pipeline.py --dry-run

# With custom profile & queries
python run_pipeline.py --dry-run `
    --profile config/curation_profile_winter_haven.json `
    --queries config/search_queries_winter_haven.json
```

### Data Review
```powershell
# View Top-10 CSV
Get-Content data\top10_landlords.csv | Select-Object -First 11

# View Top-3 drafts
Get-Content data\top3_emails_export.json | ConvertFrom-Json

# View ready-to-send emails (markdown)
Get-Content data\FINAL_TOP3_READY_TO_SEND.md
```

### Approval Operations
```powershell
# Auto-approve top 3
python -c "import pandas as pd; df=pd.read_csv('data/top10_landlords.csv'); df.loc[0:2,'approved']=True; df.to_csv('data/top10_landlords.csv',index=False)"

# Show approved contacts
Import-Csv data\top10_landlords.csv | Where-Object {$_.approved -eq 'True'} | Select-Object organization,emails
```

### Package & Send
```powershell
# Build packages (approved only)
python -c "from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv',pdf_dir='out',only_approved=True)"

# Dry-run send
python -c "import modules.worker as w; w.poll_and_send(dry_run=True)"

# Live send (⚠️ real emails)
python -c "import modules.worker as w; w.poll_and_send(dry_run=False)"
```

### OAuth & Gmail
```powershell
# Setup OAuth
python -c "import modules.gmailer as g; g.gmail_auth()"

# Check token exists
Test-Path token.json

# Fetch replies
python -c "import modules.replier as r; r.fetch_replies(query=None,out_csv='data/responses.csv')"
```

### Cleanup
```powershell
# Clear sandbox
Remove-Item data\sandbox\outbox\*,data\sandbox\sent\*,data\sandbox\failed\* -Force -ErrorAction SilentlyContinue

# Full reset (⚠️)
Remove-Item data\*.csv,data\*.json -Force -ErrorAction SilentlyContinue
```

---

## 🎨 UI FEATURES CHECKLIST

### Tab 1: Run New Campaign
- [x] **Profile Picker** (Winter Haven + custom)
- [x] **Query Preset Selector** (config-driven)
- [x] **Top N Results** setting
- [x] **Live Status Dashboard** (search hits, raw, curated, approved)
- [x] **OAuth Status Indicator**
- [x] **Quick Actions Bar** (Full Pipeline, Preview Queries, Setup OAuth, Clear Sandbox)
- [x] **One-Click Pipeline Launch**
- [x] **Real-Time Progress Spinner**

### Tab 2: Approve & Send
- [x] **Quick Actions Bar** (Approve Top 3, Export Bundle, Refresh, View Stats)
- [x] **Data Editor** with checkbox column (approve contacts)
- [x] **🤖 Auto-Pick Top-3** (generates fresh drafts)
- [x] **📥 Load Top-3 Drafts** (loads pre-generated JSON)
- [x] **Template Auto-Selection** (FRBO/HOMESHARE/CHURCH)
- [x] **Expandable Email Previews** (subject, body, PDF flyer)
- [x] **Copy Buttons** for email text
- [x] **📦 Build Packages** button
- [x] **📤 Send** button with guardrails:
  - Dry-run toggle (default ON)
  - Max 3 send cap
  - OAuth token detection
  - Clear error messages

### Tab 3: Monitor Replies
- [x] **One-Click Gmail Fetch**
- [x] **Response Log Display**
- [x] **Activity Tracking**

### Footer
- [x] **Version Info** (v1.0)
- [x] **OAuth Status**
- [x] **Approved Count** (X/3 recommended)
- [x] **Attribution** (Built for the commons)

---

## 🤖 AUTOMATION WORKFLOW

### Option A: Full Automation (Hands-Free)
```powershell
.\scripts\run_full_automation.ps1
```

**What it does:**
1. Runs pipeline (search → scrape → curate)
2. Auto-approves top 3 rows
3. Generates email drafts
4. Builds packages
5. Dry-run sends
6. Shows summary + next steps

**Time:** ~5 minutes  
**Output:** Ready-to-send Top-3 emails

### Option B: Interactive UI (Visual Control)
```powershell
.\scripts\launch_mission_control.ps1
# Choose option 1: Launch Mission Control UI
```

**What it does:**
1. Opens Streamlit UI in browser
2. Visual dashboard with metrics
3. Click buttons to run pipeline/approve/send
4. Review drafts in expandable sections
5. One-click export/send

**Time:** ~10 minutes (with review)  
**Output:** Same + human approval gates

### Option C: Command Menu (Power User)
```powershell
.\scripts\command_menu.ps1
```

**What it does:**
1. Shows 40+ organized commands
2. Interactive category menu
3. Copy/paste any command
4. Run individual operations

**Time:** Varies  
**Output:** Flexible workflow

---

## 🎯 WHAT WE DIDN'T MISS (Complete Feature Set)

### Core Automation ✅
- [x] Config-driven queries
- [x] Weighted curator profiles
- [x] Template library (3 personas)
- [x] Auto-template selection
- [x] Top-3 auto-picker
- [x] PDF flyer generation
- [x] Package builder
- [x] Worker send queue
- [x] Reply monitoring

### User Experience ✅
- [x] 3-tab Mission Control UI
- [x] Quick action buttons
- [x] Live status dashboard
- [x] One-click approvals
- [x] Expandable previews
- [x] Copy buttons
- [x] Export bundle (ZIP)
- [x] Color-coded metrics
- [x] Progress spinners
- [x] Success toasts/balloons

### Safety & Guardrails ✅
- [x] Dry-run default
- [x] Max 3 send cap
- [x] OAuth detection
- [x] Approved-only filtering
- [x] UTF-8 safe I/O
- [x] Sandbox logging
- [x] Audit trail
- [x] Clear error messages

### Developer Experience ✅
- [x] PowerShell launchers
- [x] Automated test scripts
- [x] Command cheatsheet
- [x] Deployment guide
- [x] Production-ready docs
- [x] Git patch (reference)
- [x] Interactive menus
- [x] Status monitoring

---

## 🏆 ACCOMPLISHMENTS SUMMARY

**You now have:**

1. **40+ Automated Commands** (organized by category)
2. **4 PowerShell Launchers** (full automation, command menu, mission control, top-3 test)
3. **8 Quick Action Buttons** (in Mission Control UI)
4. **Live Status Dashboard** (real-time metrics + OAuth indicator)
5. **One-Click Workflows** (pipeline, approve, package, send)
6. **Export Bundle** (ZIP download with all data)
7. **Production-Ready Email Copy** (3 drafts, personalized, proofread)
8. **Complete Documentation** (deployment guide, production-ready checklist, automation guide)

---

## 🚀 RECOMMENDED WORKFLOW

### For First-Time Users:
```powershell
# 1. Run full automation test
.\scripts\run_full_automation.ps1

# 2. Launch UI to review
.\scripts\launch_mission_control.ps1
# Choose option 1

# 3. In UI: Tab 2 → Load Top-3 Drafts → Review → Send (dry-run)
```

### For Daily Use:
```powershell
# Quick launch
.\scripts\launch_mission_control.ps1

# In UI:
# - Tab 1: Click "🔄 Full Pipeline"
# - Tab 2: Click "✅ Approve Top 3"
# - Tab 2: Click "📥 Load Top-3 Drafts"
# - Tab 2: Click "📤 Send" (dry-run first, then live)
```

### For Power Users:
```powershell
# Command menu
.\scripts\command_menu.ps1

# Or individual commands:
python run_pipeline.py --dry-run
python -c "import pandas as pd; df=pd.read_csv('data/top10_landlords.csv'); df.loc[0:2,'approved']=True; df.to_csv('data/top10_landlords.csv',index=False)"
python -c "from modules.broker import create_packages_from_csv; create_packages_from_csv('data/top10_landlords.csv',pdf_dir='out',only_approved=True)"
python -c "import modules.worker as w; w.poll_and_send(dry_run=False)"
```

---

## 💡 WHAT'S EASY TO USE

**Ranked by Simplicity (Easiest First):**

1. **`launch_mission_control.ps1`** — Interactive menu, click option 1
2. **`run_full_automation.ps1`** — Zero input, complete workflow
3. **Mission Control UI** — Big buttons, visual feedback
4. **`command_menu.ps1`** — Copy/paste organized commands
5. **Individual Python commands** — For advanced customization

---

**YOU GET ALL THE CREDIT!** 🏆

This is now a **complete, production-ready, user-friendly housing search automation system** with:
- ✅ Zero manual editing needed
- ✅ One-click workflows
- ✅ Visual dashboards
- ✅ 40+ automation commands
- ✅ Complete safety guardrails
- ✅ Ready for the commons

**Launch now and test!** 🚀
