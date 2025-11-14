# 📋 Netlify Agent Conversation Checklist

**Quick reference for talking to your Netlify deployment agent**

---

## 🎯 OPENING MESSAGE (Copy-Paste This)

```
Hi! I need help deploying WSP2AGENT V3, a Streamlit web application, to Netlify. 

I've created a detailed requirements document: NETLIFY_DEPLOYMENT_REQUIREMENTS.md

Key details:
- Framework: Streamlit (Python web app)
- GitHub: https://github.com/WSP001/WSP2agent
- Entry point: streamlit_app/app.py
- Dependencies: 15 packages (streamlit, selenium, pandas, google-api-python-client)

I have 10 specific questions about:
1. Hosting Streamlit on Netlify
2. Running Selenium/ChromeDriver
3. Long-running background tasks
4. File storage and persistence
5. OAuth token management
6. Authentication
7. Build configuration
8. CI/CD setup
9. Demo vs Production modes
10. Custom domain

Can you review my requirements doc and answer these questions so I can configure the deployment correctly?
```

---

## ✅ MUST-GET ANSWERS TO THESE 5 QUESTIONS

### Q1: Streamlit Hosting
- [ ] Can Netlify host Streamlit apps natively?
- [ ] Or do I need: Functions? Docker? External hosting?
- [ ] **Answer:** _____________________________________

### Q2: Selenium/Web Scraping
- [ ] How do I run Selenium on Netlify?
- [ ] Should I use: Puppeteer? Playwright? External service?
- [ ] **Answer:** _____________________________________

### Q3: Long-Running Tasks
- [ ] Workflows take 30-180 seconds. How to handle?
- [ ] Options: Background Functions? Queues? Split into steps?
- [ ] **Answer:** _____________________________________

### Q4: File Storage
- [ ] Where to store CSV/JSON/PDF files?
- [ ] Options: Netlify Blobs? S3? Supabase? Database?
- [ ] **Answer:** _____________________________________

### Q5: OAuth Persistence
- [ ] How to persist token.json (Gmail OAuth) across deployments?
- [ ] Need writable storage for auto-refresh tokens
- [ ] **Answer:** _____________________________________

---

## 📝 IMPORTANT CONTEXT TO MENTION

### Current Setup (Local)
✅ Works perfectly on Windows with:
- Streamlit dashboard (6 tabs)
- One-button workflows
- Selenium scraper
- Gmail API integration
- CSV/JSON/PDF generation

### What We Need
🎯 Cloud deployment that preserves:
- Beautiful UI (6-tab dashboard)
- One-button execution
- Real-time progress spinners
- Safety gates (approval before sending emails)
- Demo mode (public) + Production mode (private)

### What Makes This Special
🌟 "For the Commons Good" quality:
- User-friendly (non-technical users can operate)
- Modular (works for ANY outreach workflow, not just housing)
- Safe (dry-run modes, approval gates, audit logs)
- Professional (polished UI, error handling)

---

## 🔑 KEY DECISIONS TO MAKE

Based on Netlify agent's answers, I need to decide:

### Decision 1: Hosting Strategy
- [ ] Option A: Streamlit Community Cloud + Netlify landing page
- [ ] Option B: Dockerize Streamlit, deploy to Netlify
- [ ] Option C: Convert to Netlify Functions (major rewrite)
- [ ] Option D: Other (specify): _____________________
- [ ] **My Choice:** _____________________________________

### Decision 2: Scraping Solution
- [ ] Keep Selenium (with agent's recommended setup)
- [ ] Switch to Puppeteer (Netlify Functions compatible)
- [ ] Use external service (ScrapingBee, BrightData)
- [ ] **My Choice:** _____________________________________

### Decision 3: File Storage
- [ ] Netlify Blobs
- [ ] AWS S3
- [ ] Supabase Storage
- [ ] PostgreSQL database (replace CSV files)
- [ ] **My Choice:** _____________________________________

### Decision 4: Authentication
- [ ] Netlify Identity (user accounts)
- [ ] Simple password (environment variable)
- [ ] No auth (public demo only)
- [ ] **My Choice:** _____________________________________

### Decision 5: Deployment Mode
- [ ] Single site with env variable toggle (DEMO_MODE=true/false)
- [ ] Two separate Netlify sites (demo.wsp2agent.com, app.wsp2agent.com)
- [ ] Branch-based (main=production, demo=demo)
- [ ] **My Choice:** _____________________________________

---

## 📦 FILES TO CREATE AFTER CONVERSATION

Based on agent's guidance, I will create:

### Configuration Files
- [ ] `netlify.toml` - Build and deploy settings
- [ ] `.streamlit/config.toml` - Streamlit production config
- [ ] `.env.netlify.example` - Environment variable template
- [ ] `Procfile` or `runtime.txt` (if needed)
- [ ] `Dockerfile` (if Docker approach chosen)

### Code Changes
- [ ] Update `streamlit_app/app.py` - Add authentication
- [ ] Update `modules/selenium_driver.py` - Cloud ChromeDriver paths
- [ ] Create `modules/storage.py` - File storage abstraction (CSV → Blobs/S3/DB)
- [ ] Create `demo_mode.py` - Toggle for demo vs. production
- [ ] Update `requirements.txt` - Add cloud-specific dependencies

### Documentation
- [ ] `DEPLOYMENT.md` - Deployment instructions
- [ ] `ENVIRONMENT_VARIABLES.md` - Required env vars and setup
- [ ] `TROUBLESHOOTING.md` - Common deployment issues
- [ ] Update `README.md` - Add "Live Demo" and "Deploy Your Own" sections

---

## 🚀 DEPLOYMENT STEPS (After Decisions Made)

### Step 1: Prepare Repository
- [ ] Create `netlify.toml` with agent's recommended config
- [ ] Add Streamlit config files
- [ ] Update `.gitignore` if needed
- [ ] Commit and push to GitHub

### Step 2: Create Netlify Site
- [ ] Connect GitHub repo to Netlify
- [ ] Set build command and publish directory
- [ ] Configure environment variables
- [ ] Set up file storage (Blobs/S3/Supabase)

### Step 3: Configure Secrets
- [ ] Add `SERPAPI_KEY` to Netlify env vars
- [ ] Add `GMAIL_CREDENTIALS_JSON` (base64 encoded)
- [ ] Add `GMAIL_SENDER_EMAIL`
- [ ] Add authentication password (if simple auth chosen)

### Step 4: Test Deployment
- [ ] Deploy to staging URL (*.netlify.app)
- [ ] Test all 6 tabs load correctly
- [ ] Test demo mode (sample data)
- [ ] Test search functionality (SerpAPI call)
- [ ] Test scraping (Selenium or alternative)
- [ ] Test file storage (CSV read/write)
- [ ] Test PDF generation

### Step 5: Production Launch
- [ ] Set up custom domain (if applicable)
- [ ] Configure SSL certificate
- [ ] Enable auto-deploy from GitHub
- [ ] Add authentication (if chosen)
- [ ] Test Gmail OAuth flow
- [ ] Send test email (dry-run)
- [ ] Monitor logs and errors

### Step 6: Documentation & Handoff
- [ ] Update README with live demo link
- [ ] Create deployment guide
- [ ] Document environment variables
- [ ] Create troubleshooting guide
- [ ] Share with team

---

## 💬 FOLLOW-UP QUESTIONS TO ASK

If Netlify agent's answers are unclear:

### About Streamlit Hosting
- "Can you show me an example netlify.toml for a Streamlit app?"
- "Do I need a custom buildpack, or does Netlify detect Python apps automatically?"
- "What's the startup command for a Streamlit app in production?"

### About Selenium
- "If I use Puppeteer instead, can you show me how to convert my Selenium code?"
- "What's the cost/limit of Netlify Functions for web scraping?"
- "Can you recommend a specific scraping service for my use case?"

### About File Storage
- "How do I read/write Netlify Blobs from my Streamlit app?"
- "If I use S3, what's the setup process with AWS credentials?"
- "Can you show me example code for replacing CSV files with database queries?"

### About Authentication
- "How do I add Netlify Identity to my Streamlit app?"
- "Can I use a simple environment variable password instead of full user accounts?"
- "How do I protect specific routes/pages while keeping others public?"

---

## ✨ SUCCESS CRITERIA

My deployment is successful when:

- [ ] **Live demo URL works** (anyone can access demo mode)
- [ ] **All 6 tabs load** without errors
- [ ] **Search button works** (calls SerpAPI, shows results)
- [ ] **Scraping works** (contacts extracted from listings)
- [ ] **CSV tables display** correctly (pandas dataframes render)
- [ ] **PDF generation works** (reportlab creates PDFs)
- [ ] **Gmail OAuth works** (credentials → token flow)
- [ ] **Email sending works** (test send successful)
- [ ] **Files persist** across page refreshes (not ephemeral)
- [ ] **Mobile responsive** (UI works on phone)
- [ ] **SSL enabled** (HTTPS, green padlock)
- [ ] **Auto-deploy works** (push to GitHub → auto-update)
- [ ] **Errors are logged** (can troubleshoot via Netlify dashboard)
- [ ] **Demo mode is safe** (no real API calls, sample data only)
- [ ] **Production mode is secure** (authentication required, API keys hidden)

---

## 🎯 FINAL GOAL

**Robert's Vision:**
> "User friendly dashboard pre-programmed button options execute and result show up on the same beautifully created front facing intuitive interface."

**Measurable Outcome:**
A non-technical user can:
1. Visit demo URL
2. Click "Run Full Pipeline (Dry Run)"
3. See search → scrape → curate happen with progress spinners
4. View results in a beautiful table
5. Click "Generate PDFs" and see success message
6. Feel confident using it without reading documentation

**"For the Commons Good 🌍" Quality Standard Met!**

---

## 📞 EMERGENCY CONTACTS

If deployment fails or gets stuck:

1. **Netlify Status:** https://www.netlifystatus.com/
2. **Streamlit Forums:** https://discuss.streamlit.io/
3. **GitHub Issues:** https://github.com/WSP001/WSP2agent/issues
4. **Our Documentation:** See `TROUBLESHOOTING.md` (create after deployment)

---

**Ready to talk to your Netlify agent! 🚀**

*Use the opening message above to start the conversation.*  
*Check off items as you get answers.*  
*Circle back to this checklist when making implementation decisions.*
