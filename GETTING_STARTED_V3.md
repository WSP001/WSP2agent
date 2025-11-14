# 🚀 WSP2AGENT V3 - Getting Started

## Welcome!

WSP2AGENT V3 is a **production-ready automated outreach system** that makes finding and contacting affordable housing property managers effortless.

---

## ⚡ Quick Start (60 Seconds)

### Option 1: Try Demo Mode (No Setup Required!)

```bash
# 1. Launch the app
python launcher.py

# 2. When welcome wizard appears, click:
"Try With Demo Data"

# 3. Explore all features with sample data!
```

**That's it!** You can now explore the entire workflow with realistic demo data.

### Option 2: Full Setup

```bash
# 1. Launch
python launcher.py

# 2. Click "Full Setup"

# 3. Follow the 4-step wizard:
   - Environment check (auto-repairs)
   - Gmail connection (optional, can skip)
   - Quick tour
   - Launch!
```

---

## 📋 Prerequisites

### Required:
- **Python 3.8+** (Check: `python --version`)
- **Internet connection** (for package downloads)

### Optional (for full features):
- **SERPAPI_KEY** - For automated contact search ([Get free key](https://serpapi.com/))
- **Gmail credentials.json** - For sending emails ([Setup guide](https://developers.google.com/gmail/api/quickstart/python))

**Don't have these?** No problem! Demo mode works without them.

---

## 🎯 Your First Workflow

### Step 1: Launch
```bash
python launcher.py
```

The launcher automatically:
- ✅ Checks Python version
- ✅ Creates virtual environment if missing
- ✅ Installs/updates dependencies
- ✅ Diagnoses environment
- ✅ Launches the app

### Step 2: Choose Mode

**Demo Mode** (Recommended for first time):
- ✅ No setup required
- ✅ See everything work instantly
- ✅ Realistic sample data
- ✅ Safe to experiment

**Full Setup**:
- 🔧 Connect real services
- 📧 Send actual emails
- 📊 Use your own data

### Step 3: Explore Tabs

#### 📊 Dashboard
- View quick stats
- See recent activity
- Quick action buttons

#### 🔍 Search & Scrape
1. Enter search query (e.g., "affordable housing managers")
2. Set number of results
3. Click "Run Full Pipeline"
4. Wait for completion (search → scrape → curate)

#### ✅ Approve Contacts
1. Review curated contacts
2. Check boxes to approve
3. Click "Save Changes"

#### 📧 Send Emails
1. Check "Dry Run" (recommended first time)
2. Click "Send Emails"
3. Review output (no actual emails sent in dry run)
4. Uncheck "Dry Run" when ready for real sends

#### 📬 Track Replies
- View placeholder AI features
- Vote for features you want built
- See most-wanted features in sidebar

#### 📋 Activity Log
- Complete history of all actions
- Filter to show errors only
- Export logs for analysis

#### ⚙️ Settings
- Check environment status
- Auto-repair issues
- Connect Gmail
- Set API keys
- Reset welcome wizard

---

## 🔧 Common Tasks

### Task: Run a Test Search

```
1. Go to "Search & Scrape" tab
2. Enter: "affordable housing property managers"
3. Set results: 10
4. Click "Run Full Pipeline"
5. Check "Approve Contacts" tab for results
```

### Task: Send Test Emails (Dry Run)

```
1. Go to "Approve Contacts" tab
2. Check boxes next to 2-3 contacts
3. Click "Save Changes"
4. Go to "Send Emails" tab
5. ✅ Check "Dry Run" box
6. Click "Send Emails"
7. Review output (shows what would happen)
```

### Task: Connect Gmail

```
1. Go to Settings tab
2. Under "Gmail Setup":
   - Click documentation link
   - Download credentials.json from Google Cloud Console
   - Place in project root directory
3. Return to app
4. Status shows: ✅ credentials.json found
```

### Task: Fix Environment Issues

```
1. Go to Settings tab
2. Under "Environment Status":
   - Review missing items
   - Click "Auto-Repair Environment"
3. Wait for repairs to complete
4. Green checkmarks show success
```

### Task: Export Activity Log

```
1. Go to "Activity Log" tab
2. Click "Export Log" button
3. File saved to: data/sandbox/logs/activity_export_[timestamp].json
4. Open in text editor or JSON viewer
```

---

## ❓ Troubleshooting

### Issue: "Python not found"
**Solution:**
```bash
# Windows:
python --version
# If error, download from python.org

# Mac/Linux:
python3 --version
```

### Issue: "Module not found" errors
**Solution:**
```bash
# Run launcher (auto-installs):
python launcher.py

# Or manual install:
pip install -r requirements.txt
```

### Issue: "credentials.json not found"
**Solution:**
- You can still use dry-run mode!
- Or download credentials from [Google Cloud Console](https://console.cloud.google.com/)
- Place in project root
- See Settings tab for verification

### Issue: "SERPAPI_KEY not set"
**Solution:**
```bash
# Windows:
setx SERPAPI_KEY "your-key-here"

# Mac/Linux:
export SERPAPI_KEY="your-key-here"

# Or set in app Settings tab
```

### Issue: App crashes on startup
**Solution:**
1. Delete `.venv` folder
2. Run `python launcher.py` again
3. Launcher recreates environment
4. If still fails, check Activity Log for details

### Issue: "Can't save changes in demo mode"
**Solution:**
- Demo mode is read-only
- Click "Switch to Real Data" in sidebar
- Or restart and choose "Full Setup"

---

## 🎓 Learning Path

### Day 1: Explore (Demo Mode)
- ✅ Launch with demo data
- ✅ Click through all tabs
- ✅ Try "Run Pipeline" button
- ✅ Approve sample contacts
- ✅ Test dry-run email send
- ✅ Vote for features you want

### Day 2: Setup (Real Data)
- ✅ Get SERPAPI_KEY ([free account](https://serpapi.com/))
- ✅ Set environment variable
- ✅ Switch to real data mode
- ✅ Run real search
- ✅ Review real results

### Day 3: Deploy (Production)
- ✅ Download Gmail credentials
- ✅ Connect Gmail in Settings
- ✅ Approve real contacts
- ✅ Send real emails
- ✅ Monitor Activity Log

### Week 2+: Optimize
- ✅ Refine search queries
- ✅ Build email templates
- ✅ Track response rates
- ✅ Request top-voted features

---

## 📚 Additional Resources

### Documentation Files:
- `README.md` - Project overview
- `QUICKSTART.md` - Original quick start
- `V3_FEATURES.md` - Complete feature guide
- `V1_V2_V3_COMPARISON.md` - Version comparison
- `ROUND2_SUMMARY.md` - Round 2 improvements

### In-App Help:
- Click "Need Help?" in sidebar
- Smart Error Assistant (appears on errors)
- Contextual tooltips throughout UI

### Code Examples:
- `tests/test_pipeline.py` - Full workflow examples
- `modules/` - Core functionality reference

---

## 🎉 Success Checklist

You've successfully started when you can:

- [ ] Launch app with `python launcher.py`
- [ ] See welcome wizard
- [ ] Choose demo or full setup
- [ ] Navigate all 7 tabs
- [ ] Run a pipeline (demo or real)
- [ ] Approve contacts with checkboxes
- [ ] Send dry-run emails
- [ ] View activity log
- [ ] Vote for a feature
- [ ] Access help system

**All checked?** Congratulations! You're ready to automate your outreach! 🚀

---

## 💡 Pro Tips

1. **Always start with dry-run** until confident
2. **Check Activity Log** for errors before asking for help
3. **Use demo mode** for training new team members
4. **Vote for features** you actually need
5. **Export logs regularly** for compliance
6. **Auto-repair** fixes most environment issues
7. **Reset wizard** in Settings if setup gets confusing

---

## 🆘 Getting More Help

### Built-in Help:
1. Click "Need Help?" in sidebar
2. Check Smart Error Assistant when errors occur
3. Review Activity Log → Show errors only

### Documentation:
- Read `V3_FEATURES.md` for complete feature list
- Check `V1_V2_V3_COMPARISON.md` for what's new
- Review test files for code examples

### Community:
- Submit feature requests via in-app voting
- Report issues with exported Activity Log
- Share success stories with team

---

## 🎯 What's Next?

### Immediate:
1. **Complete setup** (demo or full)
2. **Run first pipeline**
3. **Send first email** (dry-run)

### This Week:
1. **Refine search queries** for better contacts
2. **Build email templates** in modules/composer.py
3. **Track results** in Activity Log

### This Month:
1. **Automate workflow** with scheduled tasks
2. **Train team members** using demo mode
3. **Request top features** via voting system

---

**Ready to transform your outreach?**

```bash
python launcher.py
```

**Let's go! 🚀**

---

*WSP2AGENT V3 - Built for the World Seafood Producers community*  
*Making affordable housing outreach accessible to everyone*
