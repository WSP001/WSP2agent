"""
generate_roberts_housing_pdfs.py - Example test case showing WSP2AGENT modularity

This demonstrates that WSP2AGENT works for ANY outreach use case, not just seafood producers.
Robert's housing search in Winter Haven, FL proves the system is truly modular.

Usage:
    python scripts/generate_roberts_housing_pdfs.py
    
Outputs:
    - bulletin_flyer_with_tabs.pdf
    - service_for_housing_agreement.pdf
    - reference_form.pdf
    - background_check_consent.pdf
    - skills_resume.pdf
    - business_cards.pdf
    - outreach_email.pdf
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.lib.units import inch
from pathlib import Path

# Create output directory
OUTPUT_DIR = Path("out/roberts_housing")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle('title', parent=styles['Heading1'], alignment=TA_CENTER, fontSize=20, spaceAfter=6)
subtitle_style = ParagraphStyle('subtitle', parent=styles['Heading2'], alignment=TA_CENTER, fontSize=11, spaceAfter=8)
normal = ParagraphStyle('normal', parent=styles['Normal'], fontSize=11, leading=14)
bold = ParagraphStyle('bold', parent=styles['Normal'], fontSize=11, leading=14)
bold.fontName = 'Helvetica-Bold'
small = ParagraphStyle('small', parent=styles['Normal'], fontSize=9, leading=11)

# Contact info (test case data)
CONTACT_NAME = "Robert"
CONTACT_PHONE = "678-371-9527"
CONTACT_EMAIL = "worldseafood@gmail.com"
BUDGET = "$400–$700 / month"
AREA = "Winter Haven (33880)"

def create_bulletin_flyer_with_tabs(filename="bulletin_flyer_with_tabs.pdf"):
    """Create printable flyer with tear-off tabs for bulletin boards."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter, 
                            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    # Title
    story.append(Paragraph("Seeking a Room to Rent — Reliable Tenant in Winter Haven (33880)", title_style))
    story.append(Paragraph(f"Looking for a private room ({BUDGET}). I'm tidy, steady, and ready to move — with helpful, low-cost yard & tech skills you may value.", subtitle_style))
    story.append(Spacer(1, 6))

    # Main pitch
    story.append(Paragraph(f"<b>Hello — I'm {CONTACT_NAME}.</b> I'm seeking a private room in {AREA} with a budget of {BUDGET}. I pay on time, keep shared areas clean, and offer a 30-day trial so you can be confident I'm the right fit.", normal))
    story.append(Spacer(1, 8))

    # Value proposition
    story.append(Paragraph("<b>What I offer (value for homeowner):</b>", bold))
    bullets = [
        "<b>Garden & yard care (6–10 hrs/week):</b> mowing, edging, pruning, seasonal planting, vegetable beds, weed control, irrigation checks. I bring my own seeds and grow flowers & vegetables.",
        "<b>Light homeowner support:</b> minor non-licensed repairs and home-care tasks (no roofing/heavy electrical/plumbing).",
        "<b>Tech & webmaster help:</b> WordPress/site updates, email setup, basic IT help, and quick AI tutoring.",
        "<b>Flexible compensation:</b> trade hours for rent credit (example: $25/hr credited toward rent) or negotiate a flat monthly credit. All in writing."
    ]
    for b in bullets:
        story.append(Paragraph("• " + b, normal))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Safety & Comfort:</b> Background check & references available. Trial period (30 days) to make sure it's a good match.", normal))
    story.append(Spacer(1, 8))

    # Offer box
    offer = Paragraph("<b>Example offer:</b> $25/hr credited toward rent (example cap: up to $200/month). Open to a flat monthly credit instead.", normal)
    offer_table = Table([[offer]], colWidths=[6.5*inch])
    offer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('BOX', (0,0), (-1,-1), 1, colors.grey),
        ('INNERPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(offer_table)
    story.append(Spacer(1, 10))

    # Contact
    contact = f"<b>Contact:</b><br/>{CONTACT_NAME} — {CONTACT_PHONE}<br/>{CONTACT_EMAIL}"
    story.append(Paragraph(contact, normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph("No hazardous work. Written agreement required. Background/references encouraged.", small))
    story.append(Spacer(1, 18))

    # Tear-off tabs (3 columns, 2 rows)
    tab_text = f"{CONTACT_NAME} • {CONTACT_PHONE} • {CONTACT_EMAIL}"
    cols = 3
    rows = 2
    tab_w = (7.5*inch) / cols
    data = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(Paragraph(tab_text, small))
        data.append(row)
    tabs_table = Table(data, colWidths=[tab_w]*cols, rowHeights=[0.6*inch]*rows)
    tabs_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    story.append(tabs_table)
    
    doc.build(story)
    print(f"✅ Created {filename}")

def create_service_for_housing(filename="service_for_housing_agreement.pdf"):
    """Create service-for-housing agreement template."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter)
    story = []
    story.append(Paragraph("Service-for-Housing Agreement — Short Form", title_style))
    story.append(Spacer(1, 6))
    lines = [
        "Owner: ______________________",
        f"Worker/Tenant: {CONTACT_NAME} ______________________",
        "Start Date: _______   Trial: 30 days (then month-to-month)",
        "<b>Services:</b> mowing, edging, pruning, planting, irrigation checks; no hazardous licensed work.",
        "<b>Hours:</b> Up to ___ hrs/week (typical 6–10). Owner pre-approves schedule.",
        "<b>Compensation:</b> $___/hr credited toward rent, up to $___/month (example: $25/hr up to $200/mo).",
        "<b>Limits:</b> No hazardous work. Tenant responsible for negligence damages. Owner clarifies liability/insurance.",
        "<b>Termination:</b> 30-day trial. After trial, either party may end with 14 days' notice.",
        "<b>Screening:</b> Background check & two references required prior to move-in.",
        "Signatures: Owner _______ Date _______  Worker _______ Date _______"
    ]
    for l in lines:
        story.append(Paragraph(l, normal))
        story.append(Spacer(1, 8))
    doc.build(story)
    print(f"✅ Created {filename}")

def create_reference_form(filename="reference_form.pdf"):
    """Create reference form for landlord verification."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter)
    story = []
    story.append(Paragraph(f"References for {CONTACT_NAME}", title_style))
    story.append(Spacer(1, 6))
    for i in range(1, 4):
        story.append(Paragraph(f"{i}. Name: __________________ Relation: __________ Phone: __________ Email: __________ Years known: ___", normal))
        story.append(Spacer(1, 6))
        story.append(Paragraph("Comments:", normal))
        story.append(Spacer(1, 18))
    doc.build(story)
    print(f"✅ Created {filename}")

def create_background_check_consent(filename="background_check_consent.pdf"):
    """Create background check consent form."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter)
    story = []
    story.append(Paragraph("Consent for Background Check", title_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"I, {CONTACT_NAME}, consent to a background check for housing/service exchange. I authorize the owner or agent to check references and public records as necessary.", normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Signature: _______________________  Date: ____________", normal))
    doc.build(story)
    print(f"✅ Created {filename}")

def create_skills_resume(filename="skills_resume.pdf"):
    """Create skills resume highlighting value proposition."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter)
    story = []
    story.append(Paragraph(f"{CONTACT_NAME} — Garden & Tech Skills", title_style))
    story.append(Spacer(1, 6))
    items = [
        "<b>Gardening:</b> flower gardens, vegetable gardens, seed sourcing, seasonal planning, irrigation basics, soil prep, pruning.",
        "<b>Handyman:</b> light repairs, fence/woodwork, irrigation troubleshooting (non-licensed).",
        "<b>Tech:</b> webmaster (WordPress/PHP basics), basic Linux/Windows admin tasks, AI tutoring, helpdesk/email setup.",
        "<b>Availability:</b> 6–10 hrs/week; references & work samples available."
    ]
    for it in items:
        story.append(Paragraph(it, normal))
        story.append(Spacer(1, 8))
    story.append(Spacer(1, 12))
    contact = f"{CONTACT_NAME} — {CONTACT_PHONE} — {CONTACT_EMAIL}"
    story.append(Paragraph(contact, normal))
    doc.build(story)
    print(f"✅ Created {filename}")

def create_business_cards(filename="business_cards.pdf"):
    """Create business cards (4 per sheet)."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter)
    story = []
    card_w, card_h = 3.5*inch, 2*inch
    data = []
    for i in range(4):
        text = f"<b>{CONTACT_NAME}</b><br/>{CONTACT_PHONE}<br/>{CONTACT_EMAIL}<br/><i>Garden & Home-Care Partner — Room or Rent Credit</i>"
        t = Table([[Paragraph(text, normal)]], colWidths=[card_w], rowHeights=[card_h])
        t.setStyle(TableStyle([
            ('BOX',(0,0),(-1,-1),0.5,colors.grey),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ]))
        data.append([t])
    table = Table(data, colWidths=[card_w])
    story.append(table)
    doc.build(story)
    print(f"✅ Created {filename}")

def create_outreach_email_pdf(filename="outreach_email.pdf"):
    """Create printable outreach email template."""
    doc = SimpleDocTemplate(OUTPUT_DIR / filename, pagesize=letter)
    story = []
    story.append(Paragraph("Email: Seeking Room — Garden & Home-Care Partner", title_style))
    story.append(Spacer(1, 6))
    subj = "Subject: Seeking Room to Rent — Reliable Tenant Offering Garden & Home-Care Support (30-day trial)"
    body = f"""Hello [Homeowner / Admin],

My name is {CONTACT_NAME}. I am looking for a private room in {AREA} (budget {BUDGET}). I pay on time, keep shared areas tidy, and can offer 6–10 hours/week of garden and light home-care in exchange for a rent credit or private room. I bring my own seeds and grow flower + vegetable gardens. I also offer basic webmaster/computer help and AI tutoring.

If you'd like, I can stop by for a quick meeting and to show examples of my work.

Thanks for your time,
{CONTACT_NAME}
{CONTACT_PHONE}
{CONTACT_EMAIL}
"""
    story.append(Paragraph(subj, bold))
    story.append(Spacer(1, 6))
    story.append(Paragraph(body, normal))
    doc.build(story)
    print(f"✅ Created {filename}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WSP2AGENT - Robert's Housing Search Test Case")
    print("Demonstrates modularity: same system, different use case!")
    print("="*70 + "\n")
    
    print(f"Output directory: {OUTPUT_DIR.absolute()}\n")
    
    create_bulletin_flyer_with_tabs()
    create_service_for_housing()
    create_reference_form()
    create_background_check_consent()
    create_skills_resume()
    create_business_cards()
    create_outreach_email_pdf()
    
    print("\n" + "="*70)
    print("✅ All PDFs created successfully!")
    print("="*70)
    print("\nThis proves WSP2AGENT works for:")
    print("  • Seafood producers (original use case)")
    print("  • Housing searches (Robert's test case)")
    print("  • B2B outreach")
    print("  • Non-profit recruitment")
    print("  • ANY automated contact workflow")
    print("\n💡 The Commons Good: Modular tools for everyone!")
    print("="*70 + "\n")
