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

LEADS = [
  {"id": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX", "val": 750, "lost": 18},
  {"id": 2, "name": "Pure Radiance MedSpa", "niche": "Medical Aesthetics", "city": "Miami, FL", "val": 650, "lost": 16},
  {"id": 3, "name": "Premier 24/7 HVAC", "niche": "Emergency HVAC", "city": "Dallas, TX", "val": 850, "lost": 15},
  {"id": 4, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "val": 2500, "lost": 8},
  {"id": 5, "name": "Summit Crest Luxury Realty", "niche": "High-End Real Estate", "city": "Scottsdale, AZ", "val": 4000, "lost": 5},
  {"id": 6, "name": "ProActive Spine & Chiro", "niche": "Chiropractic & Wellness", "city": "Denver, CO", "val": 450, "lost": 22},
  {"id": 7, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Wealth Advisory", "city": "Boston, MA", "val": 1200, "lost": 10},
  {"id": 8, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Diego, CA", "val": 950, "lost": 14},
  {"id": 9, "name": "Rapid Response Plumbing", "niche": "Commercial Plumbing", "city": "Atlanta, GA", "val": 600, "lost": 20},
  {"id": 10, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar EPC", "city": "Orlando, FL", "val": 3500, "lost": 6},
  {"id": 11, "name": "Velora Activewear", "niche": "Athleisure & Fitness", "city": "Los Angeles, CA", "val": 120, "lost": 65},
  {"id": 12, "name": "NuvoGlow Skincare", "niche": "Clean Beauty & Cosmetics", "city": "New York, NY", "val": 95, "lost": 80},
  {"id": 13, "name": "Artisan Roast Club", "niche": "Specialty Coffee Subscription", "city": "Seattle, WA", "val": 85, "lost": 90},
  {"id": 14, "name": "ZenSleep Mattress", "niche": "Sleep Tech & Bedding", "city": "San Francisco, CA", "val": 850, "lost": 12},
  {"id": 15, "name": "HydroFlow Bottle", "niche": "Smart Hydration & Gear", "city": "Boulder, CO", "val": 75, "lost": 95},
  {"id": 16, "name": "Pawsome Pet Boxes", "niche": "Pet Supplies & Subscriptions", "city": "Austin, TX", "val": 65, "lost": 110},
  {"id": 17, "name": "Lumina Wellness", "niche": "Nootropics & Supplements", "city": "Miami, FL", "val": 110, "lost": 70},
  {"id": 18, "name": "StackSync Dev", "niche": "Developer Tools & SaaS", "city": "San Jose, CA", "val": 1400, "lost": 8},
  {"id": 19, "name": "LeadFlow CRM", "niche": "B2B Sales Automation", "city": "Chicago, IL", "val": 1800, "lost": 7},
  {"id": 20, "name": "CloudDesk Help", "niche": "Customer Support Platform", "city": "Boston, MA", "val": 1200, "lost": 9},
  {"id": 21, "name": "PulseMetrics AI", "niche": "Product Analytics SaaS", "city": "New York, NY", "val": 2200, "lost": 6},
  {"id": 22, "name": "Silicon Valley Skin Lab", "niche": "Dermatology Clinic", "city": "Palo Alto, CA", "val": 750, "lost": 16},
  {"id": 23, "name": "Pacific Coast Family Law", "niche": "Family Law & Mediation", "city": "Newport Beach, CA", "val": 3000, "lost": 6},
  {"id": 24, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Beverly Hills, CA", "val": 5000, "lost": 4},
  {"id": 25, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "val": 2800, "lost": 5},
  {"id": 26, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "val": 3500, "lost": 5},
  {"id": 27, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "val": 4500, "lost": 4},
  {"id": 28, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "val": 2200, "lost": 7},
  {"id": 29, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "val": 3200, "lost": 5},
  {"id": 30, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "val": 4000, "lost": 4}
]

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

---

## 🗓️ Your 5-Day White-Glove Deployment Schedule:

- **Day 1 (Kickoff & Ingestion):** We ingest your core service pricing, intake FAQs, and operational SOPs.
- **Day 2 (Brand Voice & Guardrails):** Prompt engineering to align with your brand tone and enforce strict zero-hallucination compliance.
- **Day 3 (Integrations Sync):** Webhook connections to your Google Calendar / Calendly / CRM and instant SMS text-back alert routing.
- **Day 4 (Stress Testing & Staff Video):** 50-scenario adversarial QA testing and a 5-minute video walkthrough for your front-desk staff.
- **Day 5 (Production Go-Live):** Insertion of your 1-line script tag into your official website. Instant 24/7 client recapture begins!

---

## 🌐 Instant Cloud Access Links (Live On Vercel):

- 🖥️ **Live Pitch Deck:** `https://work-minh-lap.vercel.app/pitches/{slug}_pitch.html`
- 🧪 **Live Sandbox Prototype:** `https://work-minh-lap.vercel.app/sandboxes/{slug}_sandbox.html`
- 📑 **Digital MSA Agreement:** `https://work-minh-lap.vercel.app/agreements/{slug}_agreement.html`
- 💳 **Official Invoice:** `https://work-minh-lap.vercel.app/invoices/{slug}_invoice.html`
- 📊 **Monthly ROI Report:** `https://work-minh-lap.vercel.app/reports/{slug}_roi_report.html`
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
    slug = lead["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
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

    # Deliverables file mapping
    file_map = [
        ("01_AI_Audit_and_Proposal.html", ROOT_DIR / "proposals" / f"{slug}_proposal.html"),
        ("02_Sales_Pitch_Deck.html", ROOT_DIR / "pitches" / f"{slug}_pitch.html"),
        ("03_Client_Live_Sandbox.html", ROOT_DIR / "sandboxes" / f"{slug}_sandbox.html"),
        ("04_Master_Services_Agreement_MSA.html", ROOT_DIR / "agreements" / f"{slug}_agreement.html"),
        ("05_Official_Invoice_INV.html", ROOT_DIR / "invoices" / f"{slug}_invoice.html"),
        ("06_Monthly_ROI_Report.html", ROOT_DIR / "reports" / f"{slug}_roi_report.html"),
    ]

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
    print("📦 PACKAGING 30 COMPLETE CLIENT EXECUTIVE ONBOARDING DOSSIERS (ZIP)")
    print("=" * 75)

    for l in LEADS:
        zp, kb = package_client(l)
        print(f"  [✓] #{l['id']:02d} {l['name']:<30} -> {zp.name} ({kb:.1f} KB)")

    print("-" * 75)
    print(f"🎉 SUCCESS: All 30 client dossiers packaged into: {PACKAGES_DIR}")
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Complete Client Deliverables into ZIP Dossiers")
    parser.add_argument("--all", action="store_true", help="Package all 30 clients")
    parser.add_argument("--lead", type=int, help="Package a single lead ID (1-30)")

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
