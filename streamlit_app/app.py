"""
WSP2AGENT Control Panel - User-Friendly Streamlit Interface
All pipeline operations in one place with pre-programmed buttons.
"""

import json
import os
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()


def read_json_safe(path: Path):
    """Read JSON with UTF-8 encoding and error handling."""
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return json.loads(text)
    except Exception:
        try:
            text = path.read_text(encoding="latin-1", errors="replace")
            return json.loads(text)
        except Exception:
            return []


def read_csv_safe(path: Path):
    """Read CSV with error handling."""
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.error(f"Could not read {path.name}: {e}")
        return pd.DataFrame()

DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
TOP10_CSV = DATA_DIR / "top10_landlords.csv"

st.set_page_config(page_title="WSP2AGENT Control Panel", page_icon="🏠", layout="wide")

st.title("🏠 WSP2AGENT Control Panel")
st.markdown("**World Seafood Producers - Automated Outreach System**")

# Sidebar - Environment Status
with st.sidebar:
    st.header("🔧 System Status")
    
    # Check SERPAPI_KEY
    serpapi_key = os.getenv("SERPAPI_KEY", "")
    if serpapi_key:
        st.success("✅ SERPAPI_KEY configured")
    else:
        st.error("❌ SERPAPI_KEY missing")
        new_key = st.text_input("Enter SERPAPI Key:", type="password", key="serpapi_input")
        if st.button("Save SERPAPI Key"):
            os.environ["SERPAPI_KEY"] = new_key
            st.rerun()
    
    # Check credentials.json
    creds_path = Path("credentials.json")
    if creds_path.exists():
        st.success("✅ Gmail credentials.json found")
    else:
        st.warning("⚠️ credentials.json missing")
        st.caption("Upload your OAuth2 credentials file:")
        uploaded_file = st.file_uploader("credentials.json", type=["json"], key="creds_upload")
        if uploaded_file:
            creds_path.write_bytes(uploaded_file.getvalue())
            st.success("✅ Credentials saved!")
            st.rerun()
    
    # Check token.json
    token_path = Path("token.json")
    if token_path.exists():
        st.success("✅ Gmail authenticated")
    else:
        st.info("ℹ️ Gmail auth needed (run once)")

# Main Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Dashboard",
    "🔍 1. Search & Scrape",
    "✅ 2. Review & Approve",
    "📧 3. Send Emails",
    "📥 4. Track Replies",
    "⚙️ Settings"
])

# ========== TAB 1: DASHBOARD ==========
with tab1:
    st.header("Pipeline Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_results = read_json_safe(DATA_DIR / "search_results.json")
        st.metric("Search Results", len(search_results))
    
    with col2:
        contacts_df = read_csv_safe(DATA_DIR / "contacts_raw.csv")
        st.metric("Scraped Contacts", len(contacts_df))
    
    with col3:
        if TOP10_CSV.exists():
            df = read_csv_safe(TOP10_CSV)
            approved_count = df[df.get("approved", False).fillna(False)].shape[0]
            st.metric("Approved Contacts", approved_count)
        else:
            st.metric("Approved Contacts", 0)
    
    st.divider()
    
    # Quick Status
    st.subheader("🚦 Quick Status")
    if (DATA_DIR / "search_results.json").exists():
        st.success("✅ Search completed")
    else:
        st.info("➡️ Run search in tab 2")
    
    if (DATA_DIR / "contacts_raw.csv").exists():
        st.success("✅ Contacts scraped")
    else:
        st.info("➡️ Scrape contacts in tab 2")
    
    if TOP10_CSV.exists() and approved_count > 0:
        st.success(f"✅ {approved_count} contacts approved")
    else:
        st.info("➡️ Approve contacts in tab 3")

# ========== TAB 2: SEARCH & SCRAPE ==========
with tab2:
    st.header("🔍 Step 1: Search & Scrape Listings")
    
    st.markdown("""
    This step:
    1. Searches Craigslist/Roomies.com for "Winter Haven" room listings
    2. Scrapes each listing page for emails & phone numbers
    3. Curates top 10 landlords by score
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Run Full Pipeline (Dry Run)", type="primary", key="dry_run"):
            with st.spinner("Running search → scrape → curate..."):
                try:
                    from modules import searcher, scraper, curator
                    
                    # Search
                    st.info("🔍 Searching listings...")
                    results = searcher.run_searches()
                    DATA_DIR.mkdir(parents=True, exist_ok=True)
                    with open(DATA_DIR / "search_results.json", "w") as f:
                        json.dump(results, f, indent=2)
                    st.success(f"✅ Found {len(results)} listings")
                    
                    # Scrape
                    st.info("🌐 Scraping contact info...")
                    scraper.scrape_results(
                        DATA_DIR / "search_results.json",
                        out_csv=DATA_DIR / "contacts_raw.csv"
                    )
                    st.success("✅ Contacts extracted")
                    
                    # Curate
                    st.info("⭐ Scoring and ranking...")
                    curator.curate_contacts(
                        DATA_DIR / "contacts_raw.csv",
                        out_csv=TOP10_CSV
                    )
                    st.success("✅ Top 10 landlords curated!")
                    st.balloons()
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("📄 View Search Results", key="view_search"):
            if (DATA_DIR / "search_results.json").exists():
                results = json.loads((DATA_DIR / "search_results.json").read_text())
                st.json(results[:3])  # Show first 3
            else:
                st.warning("No search results yet")
    
    st.divider()
    
    # Show contacts_raw.csv if exists
    if (DATA_DIR / "contacts_raw.csv").exists():
        st.subheader("Raw Contacts")
        df_raw = pd.read_csv(DATA_DIR / "contacts_raw.csv")
        st.dataframe(df_raw.head(10), use_container_width=True)
    
    # Show top10_landlords.csv if exists
    if TOP10_CSV.exists():
        st.subheader("Top 10 Curated Landlords")
        df_top = pd.read_csv(TOP10_CSV)
        st.dataframe(df_top, use_container_width=True)

# ========== TAB 3: REVIEW & APPROVE ==========
with tab3:
    st.header("✅ Step 2: Review & Approve Contacts")
    
    if not TOP10_CSV.exists():
        st.warning("⚠️ No contacts to approve. Run search first (Tab 2)")
    else:
        df = pd.read_csv(TOP10_CSV)
        
        st.markdown("**Click checkboxes to approve contacts for email sending:**")
        
        # Create editable table
        edited_data = []
        for idx, row in df.iterrows():
            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 3, 2, 2, 1])
            
            with col1:
                approved = st.checkbox(
                    "✓", 
                    value=row.get("approved", False),
                    key=f"approve_{idx}"
                )
            
            with col2:
                st.write(row.get("organization", "Unknown"))
            
            with col3:
                st.write(row.get("url", "")[:40] + "...")
            
            with col4:
                st.write(row.get("emails", "N/A"))
            
            with col5:
                st.write(f"Score: {row.get('score', 0)}")
            
            with col6:
                st.write(f"#{idx + 1}")
            
            # Update row
            row["approved"] = approved
            edited_data.append(row)
        
        st.divider()
        
        # Save button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 Save Approvals", type="primary"):
                updated_df = pd.DataFrame(edited_data)
                updated_df.to_csv(TOP10_CSV, index=False)
                st.success("✅ Approvals saved!")
                st.rerun()
        
        with col2:
            approved_count = sum(1 for row in edited_data if row.get("approved"))
            st.metric("Approved", approved_count)
        
        # Safety warning
        if approved_count > 3:
            st.warning(f"⚠️ You have {approved_count} contacts approved. Start with 1-3 for testing!")

# ========== TAB 4: SEND EMAILS ==========
with tab4:
    st.header("📧 Step 3: Generate PDFs & Send Emails")
    
    if not TOP10_CSV.exists():
        st.warning("⚠️ No contacts to email. Complete steps 1-2 first.")
    else:
        df = pd.read_csv(TOP10_CSV)
        approved_df = df[df.get("approved", False) == True]
        
        st.metric("Approved for Sending", len(approved_df))
        
        if len(approved_df) == 0:
            st.info("ℹ️ No contacts approved yet. Go to Tab 3 to approve.")
        else:
            st.dataframe(approved_df[["organization", "emails", "url", "score"]], use_container_width=True)
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📄 Generate PDFs")
                if st.button("🖨️ Create Personal Flyers", type="secondary"):
                    with st.spinner("Generating PDFs..."):
                        try:
                            from modules import pdfs
                            pdfs.make_personal_pdfs(TOP10_CSV, out_dir=Path("out"))
                            st.success("✅ PDFs generated in /out folder!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            
            with col2:
                st.subheader("📝 Compose Emails")
                if st.button("✍️ Generate Email Drafts", type="secondary"):
                    with st.spinner("Composing emails..."):
                        try:
                            from modules import composer
                            composer.compose_emails(TOP10_CSV, out_file=DATA_DIR / "top10_outreach_emails.json")
                            st.success("✅ Email drafts created!")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            
            st.divider()
            
            # Gmail Authentication
            st.subheader("🔐 Gmail Authentication")
            if not Path("token.json").exists():
                st.warning("⚠️ Gmail not authenticated")
                if st.button("🔑 Authenticate Gmail (One-Time Setup)"):
                    with st.spinner("Opening browser for OAuth..."):
                        try:
                            from modules import gmailer
                            gmailer.gmail_auth()
                            st.success("✅ Gmail authenticated! Refresh page.")
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
            else:
                st.success("✅ Gmail already authenticated")
            
            st.divider()
            
            # Send Emails
            st.subheader("📮 Send Emails")
            
            dry_run_send = st.checkbox("🧪 Dry Run (don't actually send)", value=True)
            
            if st.button("📤 SEND EMAILS", type="primary", disabled=not Path("token.json").exists()):
                if len(approved_df) > 3 and not dry_run_send:
                    confirm = st.checkbox(f"⚠️ Confirm sending to {len(approved_df)} contacts")
                    if not confirm:
                        st.stop()
                
                with st.spinner("Sending emails..."):
                    try:
                        from modules import gmailer
                        results = gmailer.send_approved_emails(TOP10_CSV, dry_run=dry_run_send)
                        
                        if dry_run_send:
                            st.info(f"🧪 DRY RUN: Would send {len(results)} emails")
                        else:
                            st.success(f"✅ Sent {len(results)} emails!")
                        
                        for recipient, subject, msg_id in results:
                            st.text(f"✉️ {recipient} - {subject}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

# ========== TAB 5: TRACK REPLIES ==========
with tab5:
    st.header("📥 Track Replies & Responses")
    
    st.markdown("""
    Monitor incoming replies from your outreach emails and track engagement.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📬 Fetch New Replies")
        if st.button("🔄 Check Gmail for Replies", type="primary"):
            with st.spinner("Checking inbox..."):
                try:
                    from modules import replier
                    replies = replier.fetch_replies(
                        query="subject:(Seeking Room) OR subject:(RE:)",
                        out_csv=DATA_DIR / "responses.csv"
                    )
                    st.success(f"✅ Found {len(replies)} new replies!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    
    with col2:
        st.subheader("📊 Reply Statistics")
        responses_file = DATA_DIR / "responses.csv"
        if responses_file.exists():
            responses_df = read_csv_safe(responses_file)
            st.metric("Total Replies", len(responses_df))
            st.metric("This Week", "Coming soon...")
        else:
            st.info("No replies tracked yet")
    
    st.divider()
    
    # Show recent replies
    if responses_file.exists():
        st.subheader("Recent Replies")
        responses_df = read_csv_safe(responses_file)
        if len(responses_df) > 0:
            st.dataframe(
                responses_df[["from", "subject", "date", "snippet"]].head(10),
                use_container_width=True
            )
        else:
            st.info("No replies yet. Run 'Check Gmail' above.")
    
    st.divider()
    
    # Future features section
    st.subheader("🚀 Future Features (Coming Soon)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 AI Reply Suggestions", disabled=True):
            st.info("Will use AI to suggest reply templates")
        
        if st.button("📈 A/B Test Results", disabled=True):
            st.info("Compare different email templates")
    
    with col2:
        if st.button("📧 Email Preview", disabled=True):
            st.info("Preview emails before sending")
        
        if st.button("📅 Schedule Sends", disabled=True):
            st.info("Schedule emails for optimal send times")
    
    with col3:
        if st.button("🎯 Lead Scoring", disabled=True):
            st.info("AI-powered lead quality scoring")
        
        if st.button("📊 Campaign Analytics", disabled=True):
            st.info("Detailed open/reply/conversion rates")

# ========== TAB 6: SETTINGS ==========
with tab6:
    st.header("⚙️ Settings & Configuration")
    
    st.subheader("🔑 API Keys")
    
    current_serpapi = os.getenv("SERPAPI_KEY", "")
    new_serpapi = st.text_input("SERPAPI Key", value=current_serpapi[:20] + "..." if current_serpapi else "", type="password")
    
    if st.button("Update SERPAPI Key"):
        # Update .env file
        env_path = Path(".env")
        if env_path.exists():
            content = env_path.read_text()
            if "SERPAPI_KEY" in content:
                content = "\n".join([line if not line.startswith("SERPAPI_KEY") else f"SERPAPI_KEY={new_serpapi}" for line in content.split("\n")])
            else:
                content += f"\nSERPAPI_KEY={new_serpapi}"
            env_path.write_text(content)
        else:
            env_path.write_text(f"SERPAPI_KEY={new_serpapi}")
        st.success("✅ SERPAPI key updated!")
    
    st.divider()
    
    st.subheader("📁 Data Directory")
    st.code(str(DATA_DIR.absolute()))
    
    if st.button("🗑️ Clear All Data (Reset)"):
        confirm = st.checkbox("⚠️ Confirm deletion of all search/contact data")
        if confirm:
            import shutil
            if DATA_DIR.exists():
                shutil.rmtree(DATA_DIR)
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            st.success("✅ Data cleared!")
            st.rerun()
    
    st.divider()
    
    st.subheader("📋 System Info")
    st.code(f"""
Python: {sys.version.split()[0]}
Working Dir: {Path.cwd()}
Data Dir: {DATA_DIR}
    """)

# Footer
st.divider()
st.caption("WSP2AGENT v1.0 | Built for World Seafood Producers")
