# -*- coding: utf-8 -*-
"""
WSP2AGENT Control Panel V3 - Production-Ready User Interface
Includes: Welcome wizard, sample data, error assistant, activity log, feature voting
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import enhanced utilities
from modules.utils import (
    get_sample_data, ActivityLogger, ErrorAssistant,
    check_environment, auto_repair_environment,
    get_feature_votes, vote_for_feature, get_top_voted_features
)

load_dotenv()

# Initialize activity logger
activity_logger = ActivityLogger()


def read_json_safe(path: Path):
    """Read JSON with UTF-8 encoding and error handling."""
    if not path.exists():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return json.loads(text)
    except Exception as e:
        activity_logger.log_action("read_json", {"path": str(path), "error": str(e)}, "error")
        error_type = ErrorAssistant.diagnose_error(e)
        help_info = ErrorAssistant.get_help(error_type)
        if help_info:
            st.error(f"**{help_info['title']}**: {help_info['message']}")
            with st.expander("💡 Solutions"):
                for solution in help_info['solutions']:
                    st.write(f"- {solution}")
        return []


def read_csv_safe(path: Path):
    """Read CSV with error handling."""
    try:
        return pd.read_csv(path)
    except Exception as e:
        activity_logger.log_action("read_csv", {"path": str(path), "error": str(e)}, "error")
        st.error(f"Could not read {path.name}: {e}")
        return pd.DataFrame()


DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
TOP10_CSV = DATA_DIR / "top10_landlords.csv"

st.set_page_config(page_title="WSP2AGENT V3", page_icon="🏠", layout="wide")

# ============================================================================
# WELCOME WIZARD (First Time Setup)
# ============================================================================

if "setup_complete" not in st.session_state:
    st.session_state["setup_complete"] = False
    st.session_state["demo_mode"] = False

if not st.session_state["setup_complete"]:
    st.title("👋 Welcome to WSP2AGENT!")
    st.markdown("### Let's get you set up in less than a minute")
    
    # Progress bar
    setup_step = st.session_state.get("setup_step", 0)
    progress_bar = st.progress(setup_step / 4)
    
    if setup_step == 0:
        st.markdown("""
        **This tool helps you:**
        - 🔍 Search for affordable housing contacts
        - 📧 Send personalized outreach emails
        - 📊 Track responses and manage approvals
        - 🤖 Automate your entire outreach pipeline
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Try With Demo Data", use_container_width=True):
                st.session_state["demo_mode"] = True
                st.session_state["setup_step"] = 4
                st.session_state["setup_complete"] = True
                activity_logger.log_action("setup", {"mode": "demo"}, "success")
                st.rerun()
        
        with col2:
            if st.button("⚙️ Full Setup", use_container_width=True):
                st.session_state["setup_step"] = 1
                st.rerun()
    
    elif setup_step == 1:
        st.markdown("### Step 1: Environment Check")
        env_status = check_environment()
        
        if env_status["status"] == "ready":
            st.success("✅ All systems ready!")
        else:
            st.warning(f"⚠️ {env_status['message']}")
            for item in env_status["missing"]:
                st.write(f"- Missing: `{item}`")
            
            if st.button("🔧 Auto-Repair"):
                with st.spinner("Repairing environment..."):
                    repair_results = auto_repair_environment()
                    for msg in repair_results["repaired"]:
                        st.success(msg)
                    for msg in repair_results["failed"]:
                        st.error(msg)
        
        if st.button("Next →"):
            st.session_state["setup_step"] = 2
            st.rerun()
    
    elif setup_step == 2:
        st.markdown("### Step 2: Connect Gmail (Optional)")
        st.markdown("""
        To send emails, you need to connect your Gmail account:
        1. Download `credentials.json` from [Google Cloud Console](https://console.cloud.google.com/)
        2. Place it in the project root directory
        3. Click "Test Connection" below
        """)
        
        if os.path.exists("credentials.json"):
            st.success("✅ credentials.json found!")
        else:
            st.info("📝 You can skip this and use dry-run mode")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Skip for now"):
                st.session_state["setup_step"] = 3
                st.rerun()
        with col2:
            if st.button("Next →"):
                st.session_state["setup_step"] = 3
                st.rerun()
    
    elif setup_step == 3:
        st.markdown("### Step 3: Quick Tour")
        st.markdown("""
        **Main Features:**
        - **Dashboard**: View metrics and quick stats
        - **Search & Scrape**: Find contacts automatically
        - **Approve Contacts**: Review and approve with checkboxes
        - **Send Emails**: Batch send with dry-run option
        - **Track Replies**: Monitor response rates
        - **Activity Log**: See everything you've done
        """)
        
        if st.button("🎉 Start Using WSP2AGENT!"):
            st.session_state["setup_complete"] = True
            st.session_state["setup_step"] = 4
            activity_logger.log_action("setup", {"mode": "full"}, "success")
            st.rerun()
    
    st.stop()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

st.title("🏠 WSP2AGENT Control Panel V3")
st.markdown("**World Seafood Producers - Automated Outreach System**")

# Demo mode indicator
if st.session_state.get("demo_mode"):
    st.info("🎭 **DEMO MODE** - Using sample data. Switch to real data in Settings.")

# Sidebar with quick stats and help
with st.sidebar:
    st.header("Quick Stats")
    
    # Load data
    if st.session_state.get("demo_mode"):
        demo_data = get_sample_data()
        contacts_data = pd.DataFrame(demo_data["contacts"])
    else:
        contacts_data = read_csv_safe(TOP10_CSV) if TOP10_CSV.exists() else pd.DataFrame()
    
    if not contacts_data.empty:
        total = len(contacts_data)
        approved = contacts_data["approved"].sum() if "approved" in contacts_data.columns else 0
        st.metric("Total Contacts", total)
        st.metric("Approved", approved)
        st.metric("Pending", total - approved)
    else:
        st.info("No contacts yet")
    
    st.divider()
    
    # Top voted features
    st.subheader("🔥 Most Wanted Features")
    top_features = get_top_voted_features(3)
    if any(votes > 0 for _, votes in top_features):
        for feature, votes in top_features:
            if votes > 0:
                st.write(f"**{feature}**: {votes} votes")
    else:
        st.write("Vote for features in Tab 5!")
    
    st.divider()
    
    # Help button
    if st.button("❓ Need Help?", use_container_width=True):
        st.session_state["show_help"] = True
    
    # Reset demo mode
    if st.session_state.get("demo_mode"):
        if st.button("🔄 Switch to Real Data", use_container_width=True):
            st.session_state["demo_mode"] = False
            st.rerun()

# Help panel
if st.session_state.get("show_help"):
    with st.expander("📚 Quick Help Guide", expanded=True):
        st.markdown("""
        **Common Tasks:**
        - **First time?** Run the welcome wizard (Settings → Reset Setup)
        - **Send test email?** Go to Tab 4, enable "Dry Run"
        - **Can't connect Gmail?** Check Settings → Environment Status
        - **Found a bug?** See Activity Log for error details
        
        **Troubleshooting:**
        - **UnicodeDecodeError**: File encoding issue - check Settings → Auto-Repair
        - **Missing credentials**: Download from Google Cloud Console
        - **API errors**: Check SERPAPI_KEY in environment variables
        """)
        if st.button("Close Help"):
            st.session_state["show_help"] = False
            st.rerun()

# ============================================================================
# TABS
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard",
    "🔍 Search & Scrape",
    "✅ Approve Contacts",
    "📧 Send Emails",
    "📬 Track Replies",
    "📋 Activity Log",
    "⚙️ Settings"
])

# TAB 1: DASHBOARD
with tab1:
    st.header("Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not contacts_data.empty:
            st.metric("Total Contacts", len(contacts_data))
        else:
            st.metric("Total Contacts", 0)
    
    with col2:
        if not contacts_data.empty and "approved" in contacts_data.columns:
            approved_count = contacts_data["approved"].sum()
            st.metric("Approved", approved_count)
        else:
            st.metric("Approved", 0)
    
    with col3:
        # Count emails sent (from activity log)
        recent_logs = activity_logger.get_recent_logs(100)
        sent_count = sum(1 for log in recent_logs if log.get("action_type") == "send_email")
        st.metric("Emails Sent", sent_count)
    
    with col4:
        # Count errors
        error_count = len(activity_logger.get_errors_only())
        st.metric("Errors", error_count, delta_color="inverse")
    
    st.divider()
    
    # Recent activity
    st.subheader("Recent Activity")
    recent_logs = activity_logger.get_recent_logs(5)
    if recent_logs:
        for log in recent_logs:
            timestamp = log.get("timestamp", "Unknown")
            action = log.get("action_type", "Unknown")
            status = log.get("status", "unknown")
            
            status_emoji = "✅" if status == "success" else "❌"
            st.write(f"{status_emoji} **{action}** - {timestamp}")
    else:
        st.info("No recent activity")
    
    st.divider()
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Run Search", use_container_width=True):
            st.switch_page("pages/2_Search_Scrape.py") if Path("pages/2_Search_Scrape.py").exists() else st.info("Go to Search & Scrape tab")
    with col2:
        if st.button("✅ Approve Contacts", use_container_width=True):
            st.info("Switch to 'Approve Contacts' tab")
    with col3:
        if st.button("📧 Send Emails", use_container_width=True):
            st.info("Switch to 'Send Emails' tab")

# TAB 2: SEARCH & SCRAPE
with tab2:
    st.header("🔍 Search & Scrape Pipeline")
    st.markdown("Find affordable housing contacts automatically using SerpAPI and web scraping.")
    
    search_query = st.text_input(
        "Search Query",
        value="affordable housing property managers near me",
        help="Enter keywords to search for contacts"
    )
    
    num_results = st.slider("Number of results to fetch", 5, 50, 10)
    
    if st.button("🚀 Run Full Pipeline", type="primary", use_container_width=True):
        with st.spinner("Running search and scrape pipeline..."):
            try:
                from modules.searcher import search_and_save
                from modules.scraper import scrape_urls_batch
                from modules.curator import curate_top_n
                
                # Search
                st.info("Step 1/3: Searching...")
                search_results = search_and_save(search_query, num_results)
                activity_logger.log_action("search", {"query": search_query, "results": len(search_results)}, "success")
                st.success(f"Found {len(search_results)} results")
                
                # Scrape
                st.info("Step 2/3: Scraping websites...")
                urls = [r.get("link") for r in search_results if r.get("link")]
                scraped = scrape_urls_batch(urls[:num_results])
                activity_logger.log_action("scrape", {"urls": len(urls)}, "success")
                st.success(f"Scraped {len(scraped)} websites")
                
                # Curate
                st.info("Step 3/3: Curating top contacts...")
                curated = curate_top_n("data/search_results.json", top_n=10)
                activity_logger.log_action("curate", {"contacts": len(curated)}, "success")
                st.success(f"Curated {len(curated)} top contacts")
                
                st.balloons()
                st.success("✅ Pipeline complete! Check 'Approve Contacts' tab.")
                
            except Exception as e:
                error_type = ErrorAssistant.diagnose_error(e)
                help_info = ErrorAssistant.get_help(error_type)
                activity_logger.log_action("pipeline", {"error": str(e)}, "error")
                
                st.error(f"Pipeline failed: {str(e)}")
                if help_info:
                    with st.expander("💡 Solutions"):
                        for solution in help_info['solutions']:
                            st.write(f"- {solution}")

# TAB 3: APPROVE CONTACTS
with tab3:
    st.header("✅ Approve Contacts")
    st.markdown("Review and approve contacts before sending emails.")
    
    if not contacts_data.empty:
        # Editable dataframe with checkboxes
        edited_df = st.data_editor(
            contacts_data,
            column_config={
                "approved": st.column_config.CheckboxColumn("Approved", default=False),
                "organization": st.column_config.TextColumn("Organization", width="large"),
                "emails": st.column_config.TextColumn("Emails", width="medium"),
                "score": st.column_config.NumberColumn("Score", format="%d"),
            },
            hide_index=True,
            use_container_width=True,
            disabled=["organization", "url", "emails", "phones", "snippet", "score"]
        )
        
        if st.button("💾 Save Changes", type="primary"):
            try:
                if st.session_state.get("demo_mode"):
                    st.warning("Demo mode - changes not saved. Switch to real data first.")
                else:
                    edited_df.to_csv(TOP10_CSV, index=False)
                    activity_logger.log_action("approve_contacts", {"total": len(edited_df), "approved": edited_df["approved"].sum()}, "success")
                    st.success("✅ Changes saved!")
            except Exception as e:
                st.error(f"Failed to save: {e}")
                activity_logger.log_action("approve_contacts", {"error": str(e)}, "error")
    else:
        st.info("No contacts to approve. Run Search & Scrape first!")

# TAB 4: SEND EMAILS
with tab4:
    st.header("📧 Send Emails")
    
    if not contacts_data.empty:
        approved_contacts = contacts_data[contacts_data["approved"] == True]
        
        if len(approved_contacts) > 0:
            st.success(f"Ready to send to {len(approved_contacts)} approved contacts")
            
            dry_run = st.checkbox("🧪 Dry Run (don't actually send)", value=True)
            
            if st.button("📨 Send Emails", type="primary", use_container_width=True):
                with st.spinner("Sending emails..." if not dry_run else "Running dry-run..."):
                    try:
                        from modules.composer import create_packages_from_csv
                        from modules.worker import poll_and_send
                        
                        # Create packages
                        packages = create_packages_from_csv(str(TOP10_CSV), pdf_dir="out")
                        
                        # Send
                        poll_and_send(dry_run=dry_run)
                        
                        activity_logger.log_action("send_email", {"count": len(approved_contacts), "dry_run": dry_run}, "success")
                        
                        if dry_run:
                            st.info("✅ Dry run complete - no emails sent")
                        else:
                            st.success("✅ Emails sent successfully!")
                            st.balloons()
                    
                    except Exception as e:
                        error_type = ErrorAssistant.diagnose_error(e)
                        help_info = ErrorAssistant.get_help(error_type)
                        activity_logger.log_action("send_email", {"error": str(e)}, "error")
                        
                        st.error(f"Failed to send: {str(e)}")
                        if help_info:
                            with st.expander("💡 Solutions"):
                                for solution in help_info['solutions']:
                                    st.write(f"- {solution}")
        else:
            st.warning("No approved contacts. Go to 'Approve Contacts' tab.")
    else:
        st.info("No contacts loaded.")

# TAB 5: TRACK REPLIES & VOTE FOR FEATURES
with tab5:
    st.header("📬 Track Replies")
    
    st.markdown("### 🚀 Coming Soon: AI-Powered Features")
    st.markdown("Vote for the features you want most!")
    
    features = {
        "AI Reply Suggestions": "OpenAI GPT-powered response templates based on email content",
        "Email Preview": "Live HTML preview before sending emails",
        "A/B Testing": "Test different subject lines and measure open rates",
        "Scheduled Sending": "Schedule emails for optimal send times",
        "Lead Scoring": "ML-powered scoring to prioritize best contacts",
        "Analytics Dashboard": "Beautiful charts showing campaign performance"
    }
    
    current_votes = get_feature_votes()
    
    for feature_name, description in features.items():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{feature_name}**")
            st.caption(description)
            votes = current_votes.get(feature_name, 0)
            st.caption(f"🗳️ {votes} votes")
        with col2:
            if st.button("Vote 👍", key=f"vote_{feature_name}"):
                if vote_for_feature(feature_name):
                    activity_logger.log_action("vote_feature", {"feature": feature_name}, "success")
                    st.success("Voted!")
                    st.rerun()

# TAB 6: ACTIVITY LOG
with tab6:
    st.header("📋 Activity Log")
    st.markdown("Complete history of all actions taken in the app.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        show_errors_only = st.checkbox("Show errors only")
    with col2:
        if st.button("📥 Export Log"):
            export_path = f"data/sandbox/logs/activity_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            if activity_logger.export_logs(export_path):
                st.success(f"Exported to {export_path}")
    
    if show_errors_only:
        logs = activity_logger.get_errors_only()
    else:
        logs = activity_logger.get_recent_logs(50)
    
    if logs:
        for log in logs:
            timestamp = log.get("timestamp", "Unknown")
            action = log.get("action_type", "Unknown")
            status = log.get("status", "unknown")
            details = log.get("details", {})
            
            status_color = "green" if status == "success" else "red"
            
            with st.expander(f"[{status.upper()}] {action} - {timestamp}"):
                st.json(details)
    else:
        st.info("No activity logged yet" if not show_errors_only else "No errors logged")

# TAB 7: SETTINGS
with tab7:
    st.header("⚙️ Settings")
    
    # Environment status
    st.subheader("🔍 Environment Status")
    env_status = check_environment()
    
    if env_status["status"] == "ready":
        st.success("✅ All systems operational")
    else:
        st.warning(f"⚠️ {env_status['message']}")
        
        with st.expander("Details"):
            for key, value in env_status["checks"].items():
                status_icon = "✅" if value else "❌"
                st.write(f"{status_icon} {key}: {value}")
        
        if st.button("🔧 Auto-Repair Environment"):
            with st.spinner("Repairing..."):
                results = auto_repair_environment()
                for msg in results["repaired"]:
                    st.success(msg)
                for msg in results["failed"]:
                    st.error(msg)
    
    st.divider()
    
    # Gmail setup
    st.subheader("📧 Gmail Setup")
    if os.path.exists("credentials.json"):
        st.success("✅ credentials.json found")
    else:
        st.warning("❌ credentials.json not found")
        st.markdown("[Download from Google Cloud Console](https://console.cloud.google.com/)")
    
    st.divider()
    
    # API Keys
    st.subheader("🔑 API Keys")
    serpapi_key = os.getenv("SERPAPI_KEY")
    if serpapi_key:
        st.success(f"✅ SERPAPI_KEY set ({serpapi_key[:8]}...)")
    else:
        st.warning("❌ SERPAPI_KEY not set")
        new_key = st.text_input("Enter SERPAPI_KEY", type="password")
        if st.button("Save Key"):
            os.environ["SERPAPI_KEY"] = new_key
            st.success("Key saved for this session (set permanently with: setx SERPAPI_KEY \"your-key\")")
    
    st.divider()
    
    # Reset setup wizard
    st.subheader("🔄 Reset Setup")
    if st.button("Reset Welcome Wizard"):
        st.session_state["setup_complete"] = False
        st.session_state["setup_step"] = 0
        st.rerun()
