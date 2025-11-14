# 🚀 Deploy WSP2AGENT to Streamlit Cloud

## Prerequisites
✅ GitHub account  
✅ Streamlit account (free at https://streamlit.io/)  
✅ This repository pushed to GitHub

---

## 🎯 OPTION 1: Drag-and-Drop Method (Easiest!)

### Step 1: Push Your Code to GitHub
```powershell
# In WSP2AGENT directory
git add -A
git commit -m "V3: Mission Control UI ready for deployment"
git push origin main
```

### Step 2: Connect Streamlit Cloud
1. Go to **https://share.streamlit.io/**
2. Click **"New app"**
3. Select your GitHub repository: `WSP001/WSP2agent`
4. Set **Main file path:** `streamlit_app/app_mission_control.py`
5. Click **"Deploy!"**

✅ **Done!** Your app will be live at: `https://your-app-name.streamlit.app`

---

## 🔧 OPTION 2: Full Manual Setup

### 1. Create `requirements.txt`
Already included in this repo:
```txt
streamlit>=1.28.0
pandas>=2.0.0
google-search-results>=2.4.2
google-api-python-client>=2.100.0
google-auth-httplib2>=0.1.1
google-auth-oauthlib>=1.1.0
selenium>=4.15.0
webdriver-manager>=4.0.1
PyPDF2>=3.0.1
reportlab>=4.0.7
```

### 2. Create `packages.txt` (for system dependencies)
Already included:
```txt
chromium
chromium-driver
```

### 3. Add Secrets (if needed)
In Streamlit Cloud dashboard:
- Go to **Settings** → **Secrets**
- Add:
```toml
[serpapi]
api_key = "your_serpapi_key_here"

[gmail]
# Leave empty - OAuth will be done via local setup
```

### 4. Deploy
Click **"Deploy"** in Streamlit Cloud dashboard

---

## ⚙️ Configuration for Cloud

### Update `config.toml` for Production
```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## 🔐 OAuth Note for Cloud Deployment

⚠️ **Gmail OAuth (`token.json`) cannot be used in Streamlit Cloud** due to file system restrictions.

**Workaround:**
1. Deploy the app **without** sending functionality (search/scrape/curate only)
2. Use **dry-run mode** to demonstrate workflow
3. For live sending, run locally with OAuth

Or use **Streamlit Secrets** with a service account (advanced).

---

## 📦 What Gets Deployed

✅ Deployed:
- `streamlit_app/` (UI code)
- `modules/` (Python modules)
- `config/` (profiles & queries)
- `templates/` (email templates)
- `prompts/` (composer prompts)
- `requirements.txt`, `packages.txt`

❌ NOT deployed (per `.gitignore`):
- `token.json` (OAuth)
- `credentials.json` (Gmail API)
- `data/sandbox/` (local logs)
- `out/` (generated PDFs)
- `__pycache__/`

---

## 🧪 Test Your Deployment

### Local Test (Before Deploying)
```powershell
streamlit run streamlit_app/app_mission_control.py --server.port 8502
```

### After Deployment
1. Open your Streamlit Cloud URL
2. Test **Tab 1:** Run pipeline (use demo mode toggle)
3. Test **Tab 2:** Review approvals
4. **Skip Tab 2 "Send"** (OAuth not available in cloud)

---

## 🐛 Troubleshooting

### App Won't Start
- Check **Logs** in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `streamlit_app/app_mission_control.py` exists

### Missing Modules
- Add missing packages to `requirements.txt`
- Redeploy

### Selenium Errors
- `packages.txt` must include `chromium` and `chromium-driver`
- Use headless mode (toggle in sidebar)

---

## 🎉 Success Checklist

- [x] Code pushed to GitHub
- [x] Streamlit Cloud app created
- [x] App loads without errors
- [x] Demo mode works (search/scrape/curate)
- [ ] OAuth setup (local only)
- [ ] Live sending (local only)

---

## 🌐 Your Live App

**URL Pattern:** `https://[repo-name]-[branch]-[random-id].streamlit.app`

**Example:** `https://wafc-business-main-abc123.streamlit.app`

**Share with:** Anyone with the link!

---

**Built for the commons** 🌍  
**WSP2AGENT Mission Control v1.0**
