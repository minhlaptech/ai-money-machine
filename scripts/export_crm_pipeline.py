"""
Master B2B CRM Pipeline & Deliverables Exporter (CSV & JSON)
------------------------------------------------------------
Exports all 30 curated leads with their complete 7-deliverable digital arsenal URLs:
 1. Proposal & Audit
 2. 10-Slide Sales Pitch Deck
 3. Live Client Sandbox
 4. Master Services Agreement (MSA)
 5. Official B2B Invoice ($1,850)
 6. Monthly Performance & ROI Report
 7. VIP Client Dossier (.zip Package)
 8. Dynamic ROI Simulator & Intake Portal
Outputs:
 - prospects/master_crm_pipeline_export.csv (For Google Sheets / Notion / Airtable)
 - prospects/master_crm_pipeline_export.json (For Make.com / n8n / Webhooks)
"""

import sys
import os
import csv
import json
import urllib.parse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
PROSPECTS_DIR = ROOT_DIR / "prospects"
CSV_OUT = PROSPECTS_DIR / "master_crm_pipeline_export.csv"
JSON_OUT = PROSPECTS_DIR / "master_crm_pipeline_export.json"

BASE_URL = "https://work-minh-lap.vercel.app"

LEADS = [
  {"id": 1, "batch": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX", "to": "contact@austindentalco.example", "contact_person": "Dr. Miller", "val": 750, "lost": 18, "status": "Ready for Outreach"},
  {"id": 2, "batch": 1, "name": "Pure Radiance MedSpa", "niche": "Medical Aesthetics", "city": "Miami, FL", "to": "info@pureradiancemedspa.example", "contact_person": "Sarah Jenkins", "val": 650, "lost": 16, "status": "Ready for Outreach"},
  {"id": 3, "batch": 1, "name": "Premier 24/7 HVAC", "niche": "Emergency HVAC", "city": "Dallas, TX", "to": "service@premierairdfw.example", "contact_person": "Mark Stevens", "val": 850, "lost": 15, "status": "Ready for Outreach"},
  {"id": 4, "batch": 1, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Diego, CA", "to": "hello@elitesmilestudio.example", "contact_person": "Dr. Nguyen", "val": 950, "lost": 14, "status": "Ready for Outreach"},
  {"id": 5, "batch": 1, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar EPC", "city": "Orlando, FL", "to": "bids@apexroofsolar.example", "contact_person": "David Vance", "val": 3500, "lost": 6, "status": "Ready for Outreach"},
  {"id": 6, "batch": 1, "name": "Lumina Wellness", "niche": "Regenerative Medicine", "city": "Miami, FL", "to": "frontdesk@luminawellness.example", "contact_person": "Dr. Adams", "val": 110, "lost": 70, "status": "Ready for Outreach"},
  {"id": 7, "batch": 1, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Beverly Hills, CA", "to": "team@vanguardluxuryre.example", "contact_person": "Alex Hunter", "val": 5000, "lost": 4, "status": "Ready for Outreach"},
  {"id": 8, "batch": 1, "name": "ProActive Spine & Chiro", "niche": "Chiropractic & Wellness", "city": "Denver, CO", "to": "appointments@proactivechiro.example", "contact_person": "Dr. Davis", "val": 450, "lost": 22, "status": "Ready for Outreach"},
  {"id": 9, "batch": 1, "name": "Rapid Response Plumbing", "niche": "Commercial Plumbing", "city": "Atlanta, GA", "to": "dispatch@rapidplumbatl.example", "contact_person": "Robert Briggs", "val": 600, "lost": 20, "status": "Ready for Outreach"},
  {"id": 10, "batch": 1, "name": "Silicon Valley Skin Lab", "niche": "Dermatology Clinic", "city": "Palo Alto, CA", "to": "support@svskinlab.example", "contact_person": "Dr. Patel", "val": 750, "lost": 16, "status": "Ready for Outreach"},
  {"id": 11, "batch": 2, "name": "Velora Activewear", "niche": "Athleisure & Fitness", "city": "Los Angeles, CA", "to": "hello@veloraactive.example", "contact_person": "Team Velora", "val": 120, "lost": 65, "status": "Ready for Outreach"},
  {"id": 12, "batch": 2, "name": "NuvoGlow Skincare", "niche": "Clean Beauty & Cosmetics", "city": "New York, NY", "to": "partners@nuvoglowbeauty.example", "contact_person": "Founder", "val": 95, "lost": 80, "status": "Ready for Outreach"},
  {"id": 13, "batch": 2, "name": "PulseMetrics AI", "niche": "Product Analytics SaaS", "city": "New York, NY", "to": "growth@pulsemetrics.example", "contact_person": "Growth Team", "val": 2200, "lost": 6, "status": "Ready for Outreach"},
  {"id": 14, "batch": 2, "name": "HydroFlow Bottle", "niche": "Smart Hydration & Gear", "city": "Boulder, CO", "to": "support@hydroflowbottle.example", "contact_person": "Team HydroFlow", "val": 75, "lost": 95, "status": "Ready for Outreach"},
  {"id": 15, "batch": 2, "name": "CloudDesk Help", "niche": "Customer Support Platform", "city": "Boston, MA", "to": "hello@clouddeskhelp.example", "contact_person": "Product Lead", "val": 1200, "lost": 9, "status": "Ready for Outreach"},
  {"id": 16, "batch": 2, "name": "Artisan Roast Club", "niche": "Specialty Coffee Subscription", "city": "Seattle, WA", "to": "orders@artisanroastclub.example", "contact_person": "Founder", "val": 85, "lost": 90, "status": "Ready for Outreach"},
  {"id": 17, "batch": 2, "name": "StackSync Dev", "niche": "Developer Tools & SaaS", "city": "San Jose, CA", "to": "founders@stacksyncdev.example", "contact_person": "Engineering Lead", "val": 1400, "lost": 8, "status": "Ready for Outreach"},
  {"id": 18, "batch": 2, "name": "Pawsome Pet Boxes", "niche": "Pet Supplies & Subscriptions", "city": "Austin, TX", "to": "hello@pawsomepetbox.example", "contact_person": "Customer Team", "val": 65, "lost": 110, "status": "Ready for Outreach"},
  {"id": 19, "batch": 2, "name": "LeadFlow CRM", "niche": "B2B Sales Automation", "city": "Chicago, IL", "to": "inquiries@leadflowcrm.example", "contact_person": "Sales Lead", "val": 1800, "lost": 7, "status": "Ready for Outreach"},
  {"id": 20, "batch": 2, "name": "ZenSleep Mattress", "niche": "Sleep Tech & Bedding", "city": "San Francisco, CA", "to": "concierge@zensleepbed.example", "contact_person": "Marketing Team", "val": 850, "lost": 12, "status": "Ready for Outreach"},
  {"id": 21, "batch": 3, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "to": "contact@sterlinglegalchi.example", "contact_person": "David Sterling, Esq.", "val": 2500, "lost": 8, "status": "Ready for Outreach"},
  {"id": 22, "batch": 3, "name": "Summit Crest Luxury Realty", "niche": "High-End Real Estate", "city": "Scottsdale, AZ", "to": "inquiries@summitcrestrealty.example", "contact_person": "Victoria Vance", "val": 4000, "lost": 5, "status": "Ready for Outreach"},
  {"id": 23, "batch": 3, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Wealth Advisory", "city": "Boston, MA", "to": "tax@beaconhillcpa.example", "contact_person": "Marcus Brody, CPA", "val": 1200, "lost": 10, "status": "Ready for Outreach"},
  {"id": 24, "batch": 3, "name": "Pacific Coast Family Law", "niche": "Family Law & Mediation", "city": "Newport Beach, CA", "to": "help@pacificfamilylawsd.example", "contact_person": "Elena Rostova, Esq.", "val": 3000, "lost": 6, "status": "Ready for Outreach"},
  {"id": 25, "batch": 3, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "to": "office@vanguardwealthnyc.example", "contact_person": "Jonathan Vance, CFP", "val": 2800, "lost": 5, "status": "Ready for Outreach"},
  {"id": 26, "batch": 3, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "to": "hello@redwoodcounseltx.example", "contact_person": "Sarah Jenkins, Esq.", "val": 3500, "lost": 5, "status": "Ready for Outreach"},
  {"id": 27, "batch": 3, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "to": "deals@pinnaclecredfw.example", "contact_person": "Robert Miller", "val": 4500, "lost": 4, "status": "Ready for Outreach"},
  {"id": 28, "batch": 3, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "to": "info@harborviewestateswa.example", "contact_person": "Cynthia Thorne, Esq.", "val": 2200, "lost": 7, "status": "Ready for Outreach"},
  {"id": 29, "batch": 3, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "to": "valuation@apexauditadvisory.example", "contact_person": "Richard Hall", "val": 3200, "lost": 5, "status": "Ready for Outreach"},
  {"id": 30, "batch": 3, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "to": "litigation@metroinjurydefense.example", "contact_person": "Carlos Mendez, Esq.", "val": 4000, "lost": 4, "status": "Ready for Outreach"}
]

try:
    from expand_crm_pipeline import NEW_LEADS
    for nl in NEW_LEADS:
        if not any(l["id"] == nl["id"] for l in LEADS):
            LEADS.append({
                "id": nl["id"],
                "batch": nl["batch"],
                "name": nl["name"],
                "niche": nl["niche"],
                "city": nl["city"],
                "to": nl["to"],
                "contact_person": nl["doc"],
                "val": nl["val"],
                "lost": nl["lost"],
                "status": "Ready for Outreach"
            })
except Exception:
    pass

def get_slug(name):
    return name.lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")

BATCH_DESCS = {
    1: "Batch 1 (Local SMBs)",
    2: "Batch 2 (E-Com & SaaS)",
    3: "Batch 3 (High-Ticket Legal & Wealth)",
    4: "Batch 4 (Luxury Contracting & Construction)",
    5: "Batch 5 (B2B Agencies & Tech Search)",
    6: "Batch 6 (Specialized Luxury Healthcare)"
}

def export_pipeline():
    PROSPECTS_DIR.mkdir(parents=True, exist_ok=True)
    records = []

    print("=" * 80)
    print("🚀 EXPORTING MASTER B2B CRM PIPELINE & 8-DELIVERABLE DIGITAL ARSENAL (60 LEADS)")
    print("=" * 80)

    for l in LEADS:
        slug = get_slug(l["name"])
        name_url = urllib.parse.quote_plus(l["name"])
        niche_url = urllib.parse.quote_plus(l["niche"])

        monthly_loss = l["val"] * l["lost"]
        annual_loss = monthly_loss * 12
        setup_fee = 1200 if l["batch"] < 3 else (1500 if l["batch"] == 3 else 1800)
        retainer_fee = 650 if l["batch"] < 3 else (750 if l["batch"] == 3 else 850)

        record = {
            "Lead_ID": l["id"],
            "Batch": BATCH_DESCS.get(l["batch"], f"Batch {l['batch']}"),
            "Business_Name": l["name"],
            "Industry_Niche": l["niche"],
            "City_Location": l["city"],
            "Contact_Person": l.get("contact_person", l.get("doc", "Owner")),
            "Email_Address": l["to"],
            "Average_Deal_Value_USD": l["val"],
            "Monthly_Missed_Inquiries": l["lost"],
            "Monthly_Lost_Revenue_USD": monthly_loss,
            "Annual_Lost_Revenue_USD": annual_loss,
            "Proposed_Setup_Fee_USD": setup_fee,
            "Proposed_Monthly_Retainer_USD": retainer_fee,
            "Initial_Invoice_Total_USD": setup_fee + retainer_fee,
            "Outreach_Status": l["status"],
            "VIP_Client_Portal_URL": f"{BASE_URL}/portal/{slug}",
            "Pitch_Deck_10_Slides_URL": f"{BASE_URL}/pitches/{slug}_pitch.html",
            "Live_Sandbox_Prototype_URL": f"{BASE_URL}/sandboxes/{slug}_sandbox.html",
            "Monthly_ROI_Report_URL": f"{BASE_URL}/reports/{slug}_roi_report.html",
            "Proposal_URL": f"{BASE_URL}/proposals/{slug}_proposal.html",
            "Master_Agreement_MSA_URL": f"{BASE_URL}/agreements/{slug}_agreement.html",
            "B2B_Invoice_URL": f"{BASE_URL}/invoices/{slug}_invoice.html",
            "VIP_Onboarding_ZIP_Dossier_URL": f"{BASE_URL}/client_packages/{slug}_executive_dossier.zip",
            "Interactive_ROI_Simulator_URL": f"{BASE_URL}/calculator?client={name_url}&val={l['val']}&lost={l['lost']}&slug={slug}",
            "Client_Intake_Portal_URL": f"{BASE_URL}/onboarding?name={name_url}&niche={niche_url}"
        }
        records.append(record)

    # 1. Export CSV
    fieldnames = list(records[0].keys())
    with open(CSV_OUT, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # 2. Export JSON
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    total_upfront = sum(r["Proposed_Setup_Fee_USD"] for r in records)
    total_mrr = sum(r["Proposed_Monthly_Retainer_USD"] for r in records)
    total_market_lost = sum(r["Monthly_Lost_Revenue_USD"] for r in records)

    print(f"  [✓] Master CSV Exported:  {CSV_OUT} ({CSV_OUT.stat().st_size / 1024:.1f} KB)")
    print(f"  [✓] Master JSON Exported: {JSON_OUT} ({JSON_OUT.stat().st_size / 1024:.1f} KB)")
    print("-" * 80)
    print(f"  📊 Total Prospects Exported:      {len(records)} High-Intent Businesses")
    print(f"  💸 Total Market Bleed Identified: ${total_market_lost:,} / month")
    print(f"  💵 Total Pipeline Setup Value:    ${total_upfront:,} Upfront Cash")
    print(f"  🔄 Total Recurring Potential:     ${total_mrr:,} / month MRR")
    print("=" * 80)
    print("🎉 Export complete! Ready to import into Google Sheets, Notion, or Airtable.")

if __name__ == "__main__":
    export_pipeline()
