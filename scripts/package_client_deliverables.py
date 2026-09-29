"""
Executive Client Deliverable Packager (ZIP Dossier Exporter)
-----------------------------------------------------------
Đóng gói trọn bộ 7 ấn phẩm số hóa cao cấp cho từng khách hàng
thành file nén ZIP chuyên nghiệp (client_packages/{slug}_client_dossier.zip)
kèm theo tài liệu hướng dẫn bàn giao VIP (WELCOME_CLIENT_ONBOARDING_GUIDE.md).
"""

import sys
import os
import zipfile
import argparse
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
PACKAGES_DIR = ROOT_DIR / "client_packages"

try:
    from leads_data import ALL_LEADS, get_slug
except ImportError:
    from scripts.leads_data import ALL_LEADS, get_slug

LEADS = ALL_LEADS


WELCOME_GUIDE_TEMPLATE = """# 🌟 EXECUTIVE WELCOME & CLIENT ONBOARDING GUIDE
> **Prepared Exclusively for:** {client_name}
> **Industry:** {niche} • **Location:** {city}
> **Solution Provider:** MinhLap AI Automation Solutions
> **Date:** {date_str}

---

## 👋 Welcome to Your 24/7 AI Client Intake Infrastructure!

Dear {client_name} Executive Team,

Congratulations on initiating your partnership with **MinhLap AI Automation Solutions**. This dossier contains your complete, turnkey digital asset ecosystem designed to capture after-hours inquiries, pre-qualify high-intent prospective clients, and book confirmed consultations onto your calendar 24/7/365.

---

## 📦 What's Inside This Executive Deliverable Package:

1. **`01_AI_Audit_and_Proposal.html`**
   - Your bespoke 2-page implementation audit analyzing {client_name}'s current inquiry response speed, market competitors in {city}, and revenue recovery potential.
2. **`02_Sales_Pitch_Deck.html`**
   - The interactive 10-slide strategy presentation deck used during our executive briefing, complete with the speed-to-lead conversion metrics and ROI forecast.
3. **`03_Client_Live_Sandbox.html`**
   - Your customized sandbox prototype featuring your brand color palette, service catalog, and live AI intake copilot equipped with 5 automated acceptance tests.
4. **`04_Master_Services_Agreement_MSA.html`**
   - Your official service agreement detailing the Net-14 terms, 30-Day Bug-Free Technical Warranty, and HTML5 digital signature pad.
5. **`05_Official_Invoice_INV.html`**
   - Your itemized billing invoice ($1,200 setup + $650 monthly retainer) with multiple international settlement options.
6. **`06_Monthly_ROI_Report.html`**
   - Your quantified monthly performance forecast modeling an estimated **+${monthly_loss}/month** in recovered gross revenue.
7. **`07_Client_VIP_Portal.html`**
   - Your dedicated Executive VIP Command Portal providing real-time AI copilot performance metrics, 99.98% SLA infrastructure health, 5-day white-glove onboarding progress, 1-click script embeds, and direct Telegram VIP engineering escalation.
8. **`08_Weekly_Performance_Statement.html`** (Active Retainer Clients)
   - Real-time quantitative retention statement demonstrating inquiries handled, 68% after-hours inquiries saved, booked appointments, and weekly protected revenue.
9. **`09_Enterprise_Expansion_Proposal.html`** (Enterprise Retainer Clients)
   - Bespoke Voice AI Receptionist & Multi-Location Expansion strategic proposal ($1,450/mo Retainer Tier).

---

## 🗓️ Your 5-Day White-Glove Deployment Schedule:

- **Day 1 (Kickoff & Ingestion):** We ingest your core service pricing, intake FAQs, and operational SOPs.
- **Day 2 (Brand Voice & Guardrails):** Prompt engineering to align with your brand tone and enforce strict zero-hallucination compliance.
- **Day 3 (Integrations Sync):** Webhook connections to your Google Calendar / Calendly / CRM and instant SMS text-back alert routing.
- **Day 4 (Stress Testing & Staff Video):** 50-scenario adversarial QA testing and a 5-minute video walkthrough for your front-desk staff.
- **Day 5 (Production Go-Live):** Insertion of your 1-line script tag into your official website. Instant 24/7 client recapture begins!

---

## 🌐 Instant Cloud Access Links (Live On Vercel):

- ⚡ **Client VIP Portal:** `https://work-minh-lap.vercel.app/portal?client={slug}`
- 🎙️ **Voice AI Demo Hub:** `https://work-minh-lap.vercel.app/voice`
- 🖥️ **Live Pitch Deck:** `https://work-minh-lap.vercel.app/pitches/{slug}_pitch.html`
- 🧪 **Live Sandbox Prototype:** `https://work-minh-lap.vercel.app/sandboxes/{slug}_sandbox.html`
- 📑 **Digital MSA Agreement:** `https://work-minh-lap.vercel.app/agreements/{slug}_agreement.html`
- 💳 **Official Invoice:** `https://work-minh-lap.vercel.app/invoices/{slug}_invoice.html`
- 📊 **Monthly ROI Report:** `https://work-minh-lap.vercel.app/reports/{slug}_roi_report.html`
- 📈 **Weekly Performance Statement:** `https://work-minh-lap.vercel.app/weekly-report/{slug}`
- 🚀 **Intake Form:** `https://work-minh-lap.vercel.app/onboarding?name={client_url_name}&niche={niche_url}`


---

## 📞 Support & Escalation SLA:

- **Lead Solutions Architect:** Minh Lap
- **Email:** `support@work-minh-lap.vercel.app`
- **SLA Commitment:** Critical technical tickets resolved within 4 business hours; routine updates within 24 hours.

We look forward to accelerating {client_name}'s client acquisition and setting the standard for your market!

Warm regards,  
**Minh Lap**  
AI Solutions Architect | MinhLap AI Automation Solutions
"""

def package_client(lead):
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    slug = get_slug(lead["name"])
    zip_path = PACKAGES_DIR / f"{slug}_executive_dossier.zip"

    import urllib.parse
    from datetime import datetime

    date_str = datetime.now().strftime("%B %d, %Y")
    client_url_name = urllib.parse.quote_plus(lead["name"])
    niche_url = urllib.parse.quote_plus(lead["niche"])
    monthly_loss = f"{(lead['lost'] * lead['val']):,}"

    # Generate Welcome Guide text
    welcome_guide = WELCOME_GUIDE_TEMPLATE.format(
        client_name=lead["name"],
        client_url_name=client_url_name,
        niche=lead["niche"],
        niche_url=niche_url,
        city=lead["city"],
        date_str=date_str,
        monthly_loss=monthly_loss,
        slug=slug
    )

    # Deliverables file mapping (8 Key Executive Deliverables)
    file_map = [
        ("01_AI_Audit_and_Proposal.html", ROOT_DIR / "proposals" / f"{slug}_proposal.html"),
        ("02_Sales_Pitch_Deck.html", ROOT_DIR / "pitches" / f"{slug}_pitch.html"),
        ("03_Client_Live_Sandbox.html", ROOT_DIR / "sandboxes" / f"{slug}_sandbox.html"),
        ("04_Master_Services_Agreement_MSA.html", ROOT_DIR / "agreements" / f"{slug}_agreement.html"),
        ("05_Official_Invoice_INV.html", ROOT_DIR / "invoices" / f"{slug}_invoice.html"),
        ("06_Monthly_ROI_Report.html", ROOT_DIR / "reports" / f"{slug}_roi_report.html"),
        ("07_Client_VIP_Portal.html", ROOT_DIR / "portals" / f"{slug}_portal.html"),
        ("08_Weekly_Performance_Statement.html", ROOT_DIR / "client_reports" / f"{slug}_weekly_report.html"),
    ]

    # For Enterprise Expansions: add 09_Enterprise_Expansion_Proposal.html
    enterprise_proposal = ROOT_DIR / "enterprise_upsell_proposals" / f"{slug}_enterprise_expansion.html"
    if enterprise_proposal.exists():
        file_map.append(("09_Enterprise_Expansion_Proposal.html", enterprise_proposal))

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Write welcome guide
        zf.writestr("WELCOME_CLIENT_ONBOARDING_GUIDE.md", welcome_guide)

        # Write each deliverable if it exists
        for arcname, src_file in file_map:
            if src_file.exists():
                zf.write(src_file, arcname)

    size_kb = zip_path.stat().st_size / 1024
    return zip_path, size_kb

def package_all():
    print("=" * 75)
    print(f"📦 PACKAGING {len(LEADS)} COMPLETE CLIENT EXECUTIVE ONBOARDING DOSSIERS (ZIP)")
    print("=" * 75)

    for l in LEADS:
        zp, kb = package_client(l)
        print(f"  [✓] #{l['id']:02d} {l['name']:<35} -> {zp.name} ({kb:.1f} KB)")

    print("-" * 75)
    print(f"🎉 SUCCESS: All {len(LEADS)} client dossiers packaged into: {PACKAGES_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Complete Client Deliverables into ZIP Dossiers")
    parser.add_argument("--all", action="store_true", help="Package all clients")
    parser.add_argument("--lead", type=int, help="Package a single lead ID")

    args = parser.parse_args()

    if args.lead:
        target = next((l for l in LEADS if l["id"] == args.lead), None)
        if target:
            zp, kb = package_client(target)
            print(f"[✓] Successfully packaged: {zp.name} ({kb:.1f} KB)")
        else:
            print(f"[!] Lead ID #{args.lead} not found.")
    else:
        package_all()

