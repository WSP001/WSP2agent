"""
WSP2AGENT Mission Control - Streamlit UI
User-friendly 3-tab interface for housing search pipeline
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Optional
import pandas as pd
import streamlit as st

# Import Top-3 helpers
try:
    from streamlit_app.top3_send_helpers import load_top3_exports, has_oauth_token
except ImportError:
    from top3_send_helpers import load_top3_exports, has_oauth_token

# ========== UTF-8 Safe Helpers ==========
DATA_DIR = Path(os.getenv("DATA_DIR", "data"))
CONFIG_DIR = Path("config")


def _safe_read_text(p: Path) -> str:
    """Read text file with UTF-8 encoding."""
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""


def _safe_read_json(p: Path):
    """Read JSON file with UTF-8 encoding."""
    try:
        return json.loads(_safe_read_text(p)) if p.exists() else {}
    except Exception:
        return {}


def _safe_read_csv(p: Path) -> pd.DataFrame:
    """Read CSV with UTF-8 encoding and error handling."""
    if not p.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(p, encoding="utf-8")
    except Exception:
        return pd.read_csv(p, encoding="utf-8", engine="python", on_bad_lines="skip")


# ========== Streamlit App ==========
st.set_page_config(page_title="WSP2AGENT Mission Control", layout="wide", page_icon="🏡")

# ---------- NEW: Data paths ----------
TOP10 = DATA_DIR / "top10_landlords.csv"

# ---------- Sidebar: Runtime Options ----------
with st.sidebar:
    st.subheader("⚙️ Runtime Options")
    use_demo = st.toggle(
        "Use demo seed data",
        value=True,
        help="Skip live search/scrape and use bundled sample data for instant demos."
    )
    headless = st.toggle(
        "Headless browser",
        value=True,
        help="Run Selenium without opening a visible browser window."
    )
    delay = st.slider(
        "Scrape delay (seconds)",
        min_value=0.5, max_value=5.0, value=2.0, step=0.5,
        help="Add a small delay between requests to reduce blocking."
    )
    # Apply env flags for downstream modules / subprocess calls
    os.environ["WSP_USE_DEMO"] = "1" if use_demo else "0"
    os.environ["WSP_SELENIUM_HEADLESS"] = "1" if headless else "0"
    os.environ["WSP_SCRAPE_DELAY_SECONDS"] = str(delay)
with st.sidebar:
    st.subheader("⚙️ Runtime Options")
    use_demo = st.toggle(
        "Use demo seed data",
        value=True,
        help="Skip live search/scrape and use bundled sample data for instant demos."
    )
    headless = st.toggle(
        "Headless browser",
        value=True,
        help="Run Selenium without opening a visible browser window."
    )
    delay = st.slider(
        "Scrape delay (seconds)",
        min_value=0.5, max_value=5.0, value=2.0, step=0.5,
        help="Add a small delay between requests to reduce blocking."
    )
    # Apply env flags for downstream modules / subprocess calls
    os.environ["WSP_USE_DEMO"] = "1" if use_demo else "0"
    os.environ["WSP_SELENIUM_HEADLESS"] = "1" if headless else "0"
    os.environ["WSP_SCRAPE_DELAY_SECONDS"] = str(delay)

st.title("🏡 WSP2AGENT — Mission Control")
st.caption("Config-driven housing search pipeline with human-in-the-loop approvals")

# Create tabs
tab_run, tab_approve, tab_monitor = st.tabs([
    "🔍 Run New Campaign",
    "✅ Approve & Send",
    "📬 Monitor Replies"
])

# =====================================================
# TAB 1: Run New Campaign
# =====================================================
with tab_run:
    st.header("🔍 Run New Campaign")
    
    # Quick Actions Bar
    st.subheader("⚡ Quick Actions")
    qcol1, qcol2, qcol3, qcol4 = st.columns(4)
    
    with qcol1:
        if st.button("🔄 Full Pipeline", use_container_width=True, type="primary"):
            with st.spinner("Running complete pipeline..."):
                cmd = ["python", "run_pipeline.py", "--dry-run"]
                rc = subprocess.call(cmd)
            if rc == 0:
                st.success("✅ Pipeline complete!")
                st.balloons()
            else:
                st.error("❌ Pipeline failed")
    
    with qcol2:
        if st.button("🔍 Preview Queries", use_container_width=True):
            queries_file = CONFIG_DIR / "search_queries_winter_haven.json"
            if queries_file.exists():
                queries = _safe_read_json(queries_file).get("queries", [])
                with st.expander("📋 Active Search Queries", expanded=True):
                    for i, q in enumerate(queries, 1):
                        st.code(f"{i}. {q}", language="text")
            else:
                st.info("Using default queries (no custom file found)")
    
    with qcol3:
        if st.button("📞 Setup OAuth", use_container_width=True):
            st.info("Run this command in terminal:")
            st.code('python -c "import modules.gmailer as g; g.gmail_auth()"', language="bash")
            st.caption("Opens browser to authorize Gmail access")
    
    with qcol4:
        if st.button("🧹 Clear Sandbox", use_container_width=True):
            try:
                import shutil
                sandbox = DATA_DIR / "sandbox"
                for folder in ["outbox", "sent", "failed"]:
                    folder_path = sandbox / folder
                    if folder_path.exists():
                        shutil.rmtree(folder_path)
                        folder_path.mkdir(parents=True, exist_ok=True)
                st.success("✅ Sandbox cleared!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    st.divider()
    
    col_config, col_status = st.columns([2, 1])
    
    with col_config:
        st.subheader("Configuration")
        
        # Profile selector
        profiles = sorted([
            p.name for p in CONFIG_DIR.glob("curation_profile_*.json")
        ])
        if not profiles:
            st.warning("No curator profiles found in config/")
            selected_profile = None
        else:
            default_idx = profiles.index("curation_profile_winter_haven.json") if "curation_profile_winter_haven.json" in profiles else 0
            selected_profile = st.selectbox(
                "Curator Scoring Profile",
                options=profiles,
                index=default_idx,
                help="Weighted scoring profile for ranking matches"
            )
        
        # Queries selector
        queries = sorted([
            p.name for p in CONFIG_DIR.glob("search_queries_*.json")
        ])
        if queries:
            default_q_idx = queries.index("search_queries_winter_haven.json") if "search_queries_winter_haven.json" in queries else 0
            selected_queries = st.selectbox(
                "Search Queries Preset",
                options=["(use default)"] + queries,
                index=default_q_idx + 1 if queries else 0,
                help="Predefined search queries for targeted discovery"
            )
        else:
            selected_queries = "(use default)"
            st.info("No custom queries found, will use defaults")
        
        # Top N
        top_n = st.number_input(
            "Top N Results",
            min_value=5,
            max_value=50,
            value=10,
            step=1,
            help="Number of top-scored results to curate"
        )
        
        # Store in session state
        st.session_state["profile_path"] = str(CONFIG_DIR / selected_profile) if selected_profile else ""
        st.session_state["queries_path"] = str(CONFIG_DIR / selected_queries) if selected_queries != "(use default)" else ""
    
    with col_status:
        st.subheader("📊 Live Status")
        
        # Read current data
        search_results = _safe_read_json(DATA_DIR / "search_results.json")
        raw_contacts = _safe_read_csv(DATA_DIR / "contacts_raw.csv")
        curated = _safe_read_csv(DATA_DIR / "top10_landlords.csv")
        
        search_count = len(search_results) if isinstance(search_results, list) else 0
        raw_count = len(raw_contacts)
        curated_count = len(curated)
        approved_count = 0
        
        if not curated.empty and "approved" in curated.columns:
            approved_count = int(curated["approved"].sum())
        
        # Visual metrics with color coding
        st.metric("🔍 Search Hits", search_count, 
                 delta=f"{search_count} found" if search_count > 0 else "Run pipeline")
        st.metric("📇 Raw Contacts", raw_count,
                 delta=f"{raw_count} scraped" if raw_count > 0 else None)
        st.metric("⭐ Curated", curated_count,
                 delta=f"Top {curated_count}" if curated_count > 0 else None)
        st.metric("✅ Approved", approved_count,
                 delta="Ready to send" if approved_count > 0 else "Approve some",
                 delta_color="normal" if approved_count > 0 else "off")
        
        # OAuth status
        st.divider()
        oauth_status = has_oauth_token(Path("."))
        if oauth_status:
            st.success("🔐 OAuth: ✅ Ready")
        else:
            st.warning("🔐 OAuth: ⚠️ Setup needed")
    
    st.divider()
    
    # Run pipeline button
    if st.button("▶️ Run Full Pipeline (Dry Run)", type="primary", use_container_width=True):
        cmd = ["python", "run_pipeline.py", "--dry-run", "--top-n", str(top_n)]
        
        if st.session_state.get("profile_path"):
            cmd += ["--profile", st.session_state["profile_path"]]
        
        if st.session_state.get("queries_path"):
            cmd += ["--queries", st.session_state["queries_path"]]
        
        with st.spinner(f"Running pipeline... (this may take 2-5 minutes)"):
            st.code(" ".join(cmd), language="bash")
            rc = subprocess.call(cmd, env=os.environ.copy())
        
        if rc == 0:
            st.success("✅ Pipeline complete! Check the 'Approve & Send' tab.")
            st.balloons()
        else:
            st.error(f"❌ Pipeline failed with exit code {rc}. Check terminal logs.")
    
    st.divider()
    
    # Preview raw contacts
    st.subheader("Preview: Raw Contacts")
    raw_preview = _safe_read_csv(DATA_DIR / "contacts_raw.csv")
    if not raw_preview.empty:
        st.dataframe(raw_preview, use_container_width=True, height=240)
    else:
        st.info("No raw contacts yet. Run pipeline to populate.")

# =====================================================
# TAB 2: Approve & Send
# =====================================================
with tab_approve:
    st.header("✅ Approve & Send")
    
    # Quick Actions Bar
    st.subheader("⚡ Quick Actions")
    acol1, acol2, acol3, acol4 = st.columns(4)
    
    df = _safe_read_csv(DATA_DIR / "top10_landlords.csv")
    
    with acol1:
        if st.button("✅ Approve Top 3", use_container_width=True, disabled=df.empty):
            if not df.empty:
                df["approved"] = False
                df.loc[0:2, "approved"] = True
                df.to_csv(DATA_DIR / "top10_landlords.csv", index=False, encoding="utf-8")
                st.success("✅ Top 3 approved!")
                st.rerun()
    
    with acol2:
        if st.button("📥 Export Bundle", use_container_width=True, disabled=df.empty):
            import zipfile
            import io
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                if (DATA_DIR / "top10_landlords.csv").exists():
                    zf.write(DATA_DIR / "top10_landlords.csv", "top10_landlords.csv")
                if (DATA_DIR / "top3_emails_export.json").exists():
                    zf.write(DATA_DIR / "top3_emails_export.json", "top3_emails_export.json")
                if (DATA_DIR / "search_results.json").exists():
                    zf.write(DATA_DIR / "search_results.json", "search_results.json")
            
            st.download_button(
                label="⬇️ Download ZIP",
                data=zip_buffer.getvalue(),
                file_name="wsp2agent_export.zip",
                mime="application/zip"
            )
    
    with acol3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    with acol4:
        if st.button("📊 View Stats", use_container_width=True, disabled=df.empty):
            with st.expander("📈 Data Statistics", expanded=True):
                if not df.empty:
                    st.write(f"**Total Rows:** {len(df)}")
                    st.write(f"**Approved:** {df['approved'].sum() if 'approved' in df.columns else 0}")
                    st.write(f"**Has Email:** {df['emails'].notna().sum() if 'emails' in df.columns else 0}")
                    st.write(f"**Has Phone:** {df['phones'].notna().sum() if 'phones' in df.columns else 0}")
                    st.write(f"**Avg Score:** {df['score'].mean():.1f}" if 'score' in df.columns else "N/A")
    
    st.divider()
    
    # ---------- NEW: Approval Preview (always visible) ----------
    st.subheader("✅ Approved Selection Preview")
    if TOP10.exists():
        try:
            df_preview = _safe_read_csv(TOP10)
            # Check for approved column
            approved_col = None
            for cand in ("approved", "APPROVE", "Approved"):
                if cand in df_preview.columns:
                    approved_col = cand
                    break
            if approved_col:
                approved_rows = df_preview[df_preview[approved_col].astype(str).str.lower().isin(["true", "1", "yes"])]
                if not approved_rows.empty:
                    st.dataframe(approved_rows, use_container_width=True, height=200)
                    st.success(f"✅ {len(approved_rows)} approved contact(s) ready. Next: **📦 Build Packages (Approved)**.")
                else:
                    st.info("ℹ️ No rows are marked approved yet. Use **✅ Approve Top 3** or the editor below to select 1–3.")
            else:
                st.dataframe(df_preview.head(3), use_container_width=True, height=200)
                st.info("ℹ️ This table has no 'approved' column yet. Use the approval editor to add/check approvals.")
        except Exception as e:
            st.error(f"Could not render preview: {e}")
    else:
        st.info("ℹ️ No curated file found yet. Run the pipeline in Tab 1 first to generate `data/top10_landlords.csv`.")
    
    st.divider()
    
    if df.empty:
        st.info("📋 No curated list yet. Run a campaign first (Tab 1).")
    else:
        # Ensure approved column exists
        if "approved" not in df.columns:
            df["approved"] = False
        
        # Approval form
        with st.form("approval_form"):
            st.info("✏️ Check the rows you want to approve (start with 1-3 for testing)")
            
            edited = st.data_editor(
                df,
                column_config={
                    "approved": st.column_config.CheckboxColumn(
                        "APPROVE?",
                        default=False,
                        width="small"
                    ),
                    "score": st.column_config.NumberColumn(
                        "Score",
                        format="%.1f",
                        width="small"
                    ),
                    "organization": st.column_config.TextColumn("Organization", width="medium"),
                    "emails": st.column_config.TextColumn("Emails", width="medium"),
                    "phones": st.column_config.TextColumn("Phones", width="small"),
                },
                use_container_width=True,
                hide_index=True,
                height=360,
                disabled=["organization", "url", "emails", "phones", "snippet", "score", "score_details"]
            )
            
            submitted = st.form_submit_button("💾 Save Approvals", type="primary")
        
        if submitted:
            edited.to_csv(DATA_DIR / "top10_landlords.csv", index=False, encoding="utf-8")
            st.success("✅ Approvals saved successfully!")
        
        st.divider()
        
        # ========== AUTO-PICK TOP-3 + DRAFTS ==========
        st.subheader("🤖 Auto-Generate Email Drafts")
        
        if st.button("🤖 Auto-Pick Top-3 + Generate Drafts", type="primary", use_container_width=True):
            # Select top 3 by score + contact availability
            work = edited.copy()
            work["has_contact"] = (
                work["emails"].fillna("").astype(str).str.len().gt(3) |
                work["phones"].fillna("").astype(str).str.len().gt(3)
            )
            work = work.sort_values(
                by=["approved", "score", "has_contact"],
                ascending=[False, False, False]
            ).head(3)
            
            # Template selector
            def _select_template(row):
                """Auto-select template based on score_details keywords."""
                try:
                    details = json.loads(row.get("score_details", "{}"))
                    pos_hits = [h.lower() for h in details.get("positive_hits", [])]
                    
                    # Keyword sets for each template
                    frbo_kw = {"owner occupied", "for rent by owner", "frbo", "private landlord"}
                    home_kw = {"homeshare", "home share", "silvernest", "senior", "elder", "caregiver", "caretaker"}
                    church_kw = {"church", "community", "bulletin", "senior center", "library"}
                    
                    # Count matches
                    frbo_count = sum(1 for h in pos_hits if any(kw in h for kw in frbo_kw))
                    home_count = sum(1 for h in pos_hits if any(kw in h for kw in home_kw))
                    church_count = sum(1 for h in pos_hits if any(kw in h for kw in church_kw))
                    
                    # Return best match
                    if home_count > frbo_count and home_count > church_count:
                        return "HOMESHARE"
                    elif church_count > frbo_count:
                        return "CHURCH"
                    else:
                        return "FRBO"
                except:
                    return "FRBO"
            
            # Email templates
            TEMPLATES = {
                "FRBO": {
                    "name": "FRBO / Owner-Occupied",
                    "subject": "Room inquiry — reliable tenant, can help with garden & light upkeep",
                    "body": """Hi {contact_name},

I'm Robert, looking for a private room in Winter Haven (33880). Budget $400–$700. I'm tidy, pay on time, and can offer 6–10 hrs/week of garden/yard care (I bring seeds and maintain flower/vegetable beds) plus light home/tech help.

Open to a modest rent credit if helpful. Happy to meet today and share references.

Property listing: {url}

— Robert
📞 678-371-9527
📧 worldseafood@gmail.com"""
                },
                "HOMESHARE": {
                    "name": "Homeshare / Elder Homeowner",
                    "subject": "Homeshare inquiry — quiet tenant + garden care (trial OK)",
                    "body": """Hello {contact_name},

I'm seeking a quiet room in Winter Haven and can assist with garden & yard care and simple home tasks 6–10 hrs/week. I'm reliable, clean, and offer a 30-day trial and references. A small rent credit in exchange is welcome, but I'm flexible.

Could we arrange a brief visit?

Property listing: {url}

— Robert
📞 678-371-9527
📧 worldseafood@gmail.com"""
                },
                "CHURCH": {
                    "name": "Church / Community Admin",
                    "subject": "Room-seek inquiry for bulletin — reliable tenant who can help with grounds",
                    "body": """Hello {org_name} Team,

Could you post or share this request? I'm a responsible adult seeking a small room in Winter Haven (33880). I can help your members with garden/yard care or light tech support 6–10 hrs/week and am open to a rent-credit arrangement. References/background check available.

Thank you kindly,

— Robert
📞 678-371-9527
📧 worldseafood@gmail.com

Property listing: {url}"""
                }
            }
            
            # PDF Flyer text
            PDF_FLYER = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ROOM SEEKER PROFILE — WINTER HAVEN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 SEEKING
• Private room in Winter Haven (33880)
• Budget: $400–$700/month
• Quiet, clean, responsible tenant
• Can start immediately

💼 OFFERING
• Garden & Yard Care: 6–10 hrs/week
  - Flower beds, vegetable gardens
  - Lawn mowing, weeding, trimming
  - Seasonal planting & maintenance
  
• Light Home/Tech Support
  - Basic repairs, maintenance help
  - Computer/phone setup, troubleshooting
  - Reliable assistance for elderly homeowners

💰 WORK-TRADE OPTIONS
• Open to rent credit for garden/yard work
• Flexible arrangements for homeshare programs
• References & background check available
• 30-day trial period welcomed

📞 CONTACT
Robert
Phone: 678-371-9527
Email: worldseafood@gmail.com

✅ ABOUT ME
Tidy, punctual, respectful. Garden enthusiast with 
tech skills. Seeking stable housing with opportunity 
to contribute yard/garden care for rent reduction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            # Generate drafts
            drafts = []
            for idx, (_, row) in enumerate(work.iterrows(), 1):
                template_name = _select_template(row)
                template = TEMPLATES[template_name]
                
                # Extract details
                org_name = str(row.get("organization", "there"))
                contact_name = row.get("contact_name") or org_name
                email = str(row.get("emails", "")).split(",")[0].strip()
                phone = str(row.get("phones", "")).split(",")[0].strip()
                url = str(row.get("url", ""))
                score = float(row.get("score", 0))
                
                # Format email
                subject = template["subject"]
                body = template["body"].format(
                    contact_name=contact_name,
                    org_name=org_name,
                    url=url
                )
                
                draft = {
                    "rank": idx,
                    "template_used": template_name,
                    "template_name": template["name"],
                    "to_email": email or "(no email)",
                    "to_phone": phone or "(no phone)",
                    "organization": org_name,
                    "score": f"{score:.1f}",
                    "listing_url": url,
                    "subject": subject,
                    "body": body,
                    "pdf_flyer_text": PDF_FLYER.strip()
                }
                drafts.append(draft)
            
            st.success(f"✅ Top-{len(drafts)} selected & drafts prepared!")
            
            # Display each draft
            for draft in drafts:
                with st.expander(
                    f"📧 #{draft['rank']} — {draft['organization']} "
                    f"(Score: {draft['score']}, Template: {draft['template_name']})",
                    expanded=(draft['rank'] == 1)
                ):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**📋 Contact Info:**")
                        st.write(f"📧 Email: `{draft['to_email']}`")
                        st.write(f"📞 Phone: `{draft['to_phone']}`")
                        if draft['listing_url']:
                            st.markdown(f"🔗 [View Listing]({draft['listing_url']})")
                    
                    with col2:
                        st.markdown("**🎯 Match Details:**")
                        st.write(f"Score: **{draft['score']}**")
                        st.write(f"Template: **{draft['template_name']}**")
                    
                    st.divider()
                    
                    st.markdown("**📨 Email Subject:**")
                    st.code(draft['subject'], language="text")
                    
                    st.markdown("**✉️ Email Body:**")
                    st.text_area(
                        "Body",
                        value=draft['body'],
                        height=200,
                        key=f"body_{draft['rank']}",
                        label_visibility="collapsed"
                    )
                    
                    st.divider()
                    
                    st.markdown("**📄 PDF Flyer (Attachment):**")
                    st.text_area(
                        "PDF Content",
                        value=draft['pdf_flyer_text'],
                        height=300,
                        key=f"pdf_{draft['rank']}",
                        label_visibility="collapsed"
                    )
            
            # Save to session state
            st.session_state["top3_drafts"] = drafts
            
            # Export JSON
            with st.expander("💾 Export as JSON (for automation)"):
                st.json(drafts)
                st.caption("📋 Copy this JSON to feed into composer.py or worker.py")
        
        st.divider()
        
        # ========== TOP-3 READY-TO-SEND LOADER ==========
        st.subheader("📥 Load Ready-to-Send Top-3 Drafts")
        st.caption("Loads pre-generated drafts from `data/top3_emails_export.json`")
        
        if st.button("📥 Load top3_emails_export.json", use_container_width=True):
            loaded_drafts = load_top3_exports()
            if loaded_drafts:
                st.success(f"✅ Loaded {len(loaded_drafts)} production-ready draft(s)!")
                
                # Display each loaded draft
                for draft in loaded_drafts:
                    with st.expander(
                        f"📧 #{draft['rank']} — {draft['organization']} "
                        f"(Score: {draft['score']}, Template: {draft['template_name']})",
                        expanded=(draft['rank'] == 1)
                    ):
                        col1, col2 = st.columns([1, 1])
                        
                        with col1:
                            st.markdown("**📋 Contact Info:**")
                            st.write(f"📧 Email: `{draft['to_email']}`")
                            st.write(f"📞 Phone: `{draft.get('to_phone', '(none)')}`")
                            if draft.get('listing_url'):
                                st.markdown(f"🔗 [View Listing]({draft['listing_url']})")
                        
                        with col2:
                            st.markdown("**🎯 Match Details:**")
                            st.write(f"Score: **{draft['score']}**")
                            st.write(f"Template: **{draft['template_name']}**")
                            st.write(f"✅ Approved: **{draft.get('approved', True)}**")
                        
                        st.divider()
                        
                        st.markdown("**📨 Email Subject:**")
                        st.code(draft['subject'], language="text")
                        
                        st.markdown("**✉️ Email Body:**")
                        st.text_area(
                            "Body",
                            value=draft['body'],
                            height=200,
                            key=f"loaded_body_{draft['rank']}",
                            label_visibility="collapsed"
                        )
                        
                        st.divider()
                        
                        st.markdown("**📄 PDF Flyer (Attachment):**")
                        st.text_area(
                            "PDF Content",
                            value=draft.get('pdf_flyer_text', ''),
                            height=250,
                            key=f"loaded_pdf_{draft['rank']}",
                            label_visibility="collapsed"
                        )
                
                # Save to session state
                st.session_state["loaded_top3_drafts"] = loaded_drafts
                
                # Export JSON for review
                with st.expander("💾 View Full JSON (for automation)"):
                    st.json(loaded_drafts)
            else:
                st.warning("❌ No drafts found. Generate drafts first or ensure `data/top3_emails_export.json` exists.")
        
        st.divider()
        
        # ========== SEND CONTROLS ==========
        st.subheader("📤 Send Controls (Top-3)")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            dry_run = st.toggle("Dry Run Mode", value=True, help="Simulate send without actually sending")
        
        with col2:
            max_live = st.number_input("Max Live Sends", min_value=1, max_value=3, value=3)
        
        st.write(" ")
        
        col_build, col_send = st.columns([1, 1])
        
        with col_build:
            if st.button("📦 Build Packages (Top-3)", use_container_width=True, type="primary"):
                code = (
                    "from modules.broker import create_packages_from_csv; "
                    "create_packages_from_csv('data/top10_landlords.csv', pdf_dir='out', only_approved=True)"
                )
                with st.spinner("Building packages for approved rows..."):
                    rc = subprocess.call(["python", "-c", code])
                
                if rc == 0:
                    st.success("✅ Packages built successfully! Check `data/sandbox/outbox/`")
                else:
                    st.error("❌ Broker error. Check terminal logs.")
        
        with col_send:
            if st.button("📤 Send (Worker, Top-3)", use_container_width=True, type="primary"):
                # OAuth check
                if not dry_run and not has_oauth_token(Path(".")):
                    st.error("❌ No token.json found. Run Gmail OAuth first:\n\n"
                             "```powershell\npython -c \"import modules.gmailer as g; g.gmail_auth()\"\n```")
                elif not dry_run and max_live < 1:
                    st.error("❌ Safety cap must allow at least 1 live send.")
                else:
                    if not dry_run:
                        st.warning(f"⚠️ LIVE MODE SELECTED. Will send up to {max_live} emails.")
                    
                    with st.spinner("Worker running..."):
                        code = f"import modules.worker as w; w.poll_and_send(dry_run={str(dry_run)})"
                        rc = subprocess.call(["python", "-c", code])
                    
                    if rc == 0:
                        st.success("✅ Worker finished successfully! Check logs for details.")
                        st.balloons()
                    else:
                        st.error("❌ Worker error. Check terminal logs for details.")
            
            code = f"import modules.worker as w; w.poll_and_send(dry_run={str(dry_run)})"
            with st.spinner("Worker running..."):
                rc = subprocess.call(["python", "-c", code])
            
            if rc == 0:
                st.success("✅ Worker finished successfully!")
            else:
                st.error("❌ Worker error. Check terminal logs.")
    
    # ---------- Live Approval Preview ----------
    st.divider()
    st.subheader("✅ Approved Selection Preview")
    TOP10 = DATA_DIR / "top10_landlords.csv"
    if TOP10.exists():
        try:
            df_preview = _safe_read_csv(TOP10)
            # Look for 'approved' column (case-insensitive)
            approved_col = None
            for cand in ("approved", "APPROVE", "Approved"):
                if cand in df_preview.columns:
                    approved_col = cand
                    break
            if approved_col:
                approved_rows = df_preview[
                    df_preview[approved_col].astype(str).str.lower().isin(["true", "1", "yes"])
                ]
                if not approved_rows.empty:
                    st.dataframe(approved_rows, use_container_width=True)
                    st.success(
                        f"{len(approved_rows)} approved contact(s) ready. "
                        "Next: **📦 Build Packages (Approved)**."
                    )
                else:
                    st.info(
                        "No rows are marked approved yet. "
                        "Use **✅ Approve Top 3** or the editor to select 1–3."
                    )
            else:
                st.dataframe(df_preview, use_container_width=True)
                st.info(
                    "This table has no 'approved' column yet. "
                    "Use the approval editor to add/check approvals."
                )
        except Exception as e:
            st.error(f"Could not render preview: {e}")
    else:
        st.info(
            "No curated file found yet. Run the pipeline first to generate `top10_landlords.csv`."
        )

# =====================================================
# TAB 3: Monitor Replies
# =====================================================
with tab_monitor:
    st.header("📬 Monitor Replies")
    
    st.info("💡 Tip: Run Gmail OAuth once in terminal: `python -c \"import modules.gmailer as g; g.gmail_auth()\"`")
    
    if st.button("🔎 Check Gmail for Replies", type="primary", use_container_width=True):
        code = "import modules.replier as r; r.fetch_replies(query=None, out_csv='data/responses.csv')"
        with st.spinner("Polling Gmail..."):
            rc = subprocess.call(["python", "-c", code])
        
        if rc == 0:
            st.success("✅ Reply log updated!")
        else:
            st.error("❌ Replier error. Check terminal logs.")
    
    st.divider()
    
    # Display responses
    responses = _safe_read_csv(DATA_DIR / "responses.csv")
    
    if not responses.empty:
        st.dataframe(responses, use_container_width=True, height=360)
        st.caption(f"📊 Total responses: {len(responses)}")
    else:
        st.info("📭 No responses yet. Run 'Check Gmail' to fetch latest.")

# ========== FOOTER ==========
st.divider()

# System Info
footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption("🏡 WSP2AGENT Mission Control v1.0")

with footer_col2:
    oauth_status = "✅ Ready" if has_oauth_token(Path(".")) else "⚠️ Setup needed"
    st.caption(f"OAuth: {oauth_status}")

with footer_col3:
    curated = _safe_read_csv(DATA_DIR / "top10_landlords.csv")
    approved = int(curated["approved"].sum()) if not curated.empty and "approved" in curated.columns else 0
    st.caption(f"Approved: {approved}/3 recommended")

st.caption("Built for the commons | Config-driven outreach automation")
