"""
Autonomous B2B CRM Pipeline Tracker & State Manager
---------------------------------------------------
Quản lý trạng thái tiếp cận và phễu khách hàng (Pipeline CRM) cho toàn bộ 30 leads.
Theo dõi từng giai đoạn tiếp cận: New -> Day 1 Sent -> Day 3 Follow-Up -> Day 7 Break-Up -> Call Booked -> Won.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
CRM_FILE = ROOT_DIR / "prospects" / "crm_pipeline.json"

INITIAL_LEADS = [
  {"id": 1, "batch": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX", "to": "contact@austindentalco.example", "doc": "Dr. Miller", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 2, "batch": 1, "name": "Pure Radiance MedSpa", "niche": "Aesthetics & Spa", "city": "Miami, FL", "to": "info@pureradiancemedspa.example", "doc": "Sarah", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 3, "batch": 1, "name": "Premier 24/7 HVAC", "niche": "Heating & AC Repair", "city": "Dallas, TX", "to": "service@premierairdfw.example", "doc": "Mark", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 4, "batch": 1, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Jose, CA", "to": "hello@elitesmilestudio.example", "doc": "Dr. Nguyen", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 5, "batch": 1, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar", "city": "Phoenix, AZ", "to": "bids@apexroofsolar.example", "doc": "David", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 6, "batch": 1, "name": "Lumina Wellness", "niche": "Regenerative Med", "city": "Seattle, WA", "to": "frontdesk@luminawellness.example", "doc": "Dr. Adams", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 7, "batch": 1, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Denver, CO", "to": "team@vanguardluxuryre.example", "doc": "Alex", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 8, "batch": 1, "name": "ProActive Spine & Chiro", "niche": "Chiropractic", "city": "Chicago, IL", "to": "appointments@proactivechiro.example", "doc": "Dr. Davis", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 9, "batch": 1, "name": "Rapid Response Plumbing", "niche": "24/7 Emergency Plumber", "city": "Atlanta, GA", "to": "dispatch@rapidplumbatl.example", "doc": "Robert", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 10, "batch": 1, "name": "Silicon Valley Skin Lab", "niche": "Dermatology & Laser", "city": "Palo Alto, CA", "to": "support@svskinlab.example", "doc": "Dr. Patel", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 11, "batch": 2, "name": "Velora Activewear", "niche": "Athleisure Apparel", "city": "Los Angeles, CA", "to": "hello@veloraactive.example", "doc": "Team Velora", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 12, "batch": 2, "name": "NuvoGlow Skincare", "niche": "Clean D2C Beauty", "city": "New York, NY", "to": "partners@nuvoglowbeauty.example", "doc": "Founder", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 13, "batch": 2, "name": "PulseMetrics AI", "niche": "B2B Analytics SaaS", "city": "San Francisco, CA", "to": "growth@pulsemetrics.example", "doc": "Founder", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 14, "batch": 2, "name": "HydroFlow Bottle", "niche": "Eco Hydration D2C", "city": "Boulder, CO", "to": "support@hydroflowbottle.example", "doc": "Team HydroFlow", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 15, "batch": 2, "name": "CloudDesk Help", "niche": "Customer Support SaaS", "city": "Austin, TX", "to": "hello@clouddeskhelp.example", "doc": "Product Lead", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 16, "batch": 2, "name": "Artisan Roast Club", "niche": "Subscription Coffee", "city": "Portland, OR", "to": "orders@artisanroastclub.example", "doc": "Founder", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 17, "batch": 2, "name": "StackSync Dev", "niche": "Developer Workflows", "city": "Seattle, WA", "to": "founders@stacksyncdev.example", "doc": "Engineering Lead", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 18, "batch": 2, "name": "Pawsome Pet Boxes", "niche": "Pet Subscription D2C", "city": "Denver, CO", "to": "hello@pawsomepetbox.example", "doc": "Customer Team", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 19, "batch": 2, "name": "LeadFlow CRM", "niche": "SMB Sales CRM SaaS", "city": "Boston, MA", "to": "inquiries@leadflowcrm.example", "doc": "Growth Team", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 20, "batch": 2, "name": "ZenSleep Mattress", "niche": "D2C Sleep Wellness", "city": "Chicago, IL", "to": "concierge@zensleepbed.example", "doc": "Marketing Team", "status": "new", "value": 1200, "retainer": 650, "last_touch": None},
  {"id": 21, "batch": 3, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "to": "contact@sterlinglegalchi.example", "doc": "David Sterling", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 22, "batch": 3, "name": "Summit Crest Luxury Realty", "niche": "Luxury Real Estate", "city": "Aspen, CO", "to": "inquiries@summitcrestrealty.example", "doc": "Victoria Vance", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 23, "batch": 3, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Advisory Firm", "city": "Boston, MA", "to": "tax@beaconhillcpa.example", "doc": "Marcus Brody", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 24, "batch": 3, "name": "Pacific Coast Family Law", "niche": "Divorce & Family Law", "city": "San Diego, CA", "to": "help@pacificfamilylawsd.example", "doc": "Elena Rostova", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 25, "batch": 3, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "to": "office@vanguardwealthnyc.example", "doc": "Jonathan Vance", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 26, "batch": 3, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "to": "hello@redwoodcounseltx.example", "doc": "Sarah Jenkins", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 27, "batch": 3, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "to": "deals@pinnaclecredfw.example", "doc": "Robert Miller", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 28, "batch": 3, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "to": "info@harborviewestateswa.example", "doc": "Cynthia Thorne", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 29, "batch": 3, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "to": "valuation@apexauditadvisory.example", "doc": "Richard Hall", "status": "new", "value": 1500, "retainer": 750, "last_touch": None},
  {"id": 30, "batch": 3, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "to": "litigation@metroinjurydefense.example", "doc": "Carlos Mendez", "status": "new", "value": 1500, "retainer": 750, "last_touch": None}
]

def load_pipeline():
    if not CRM_FILE.exists():
        CRM_FILE.parent.mkdir(parents=True, exist_ok=True)
        CRM_FILE.write_text(json.dumps(INITIAL_LEADS, indent=2, ensure_ascii=False), encoding="utf-8")
        return INITIAL_LEADS
    try:
        return json.loads(CRM_FILE.read_text(encoding="utf-8"))
    except Exception:
        return INITIAL_LEADS

def save_pipeline(leads):
    CRM_FILE.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

def print_summary():
    leads = load_pipeline()
    total = len(leads)
    new_count = sum(1 for l in leads if l["status"] == "new")
    day1_count = sum(1 for l in leads if l["status"] == "day1")
    day3_count = sum(1 for l in leads if l["status"] == "day3")
    day7_count = sum(1 for l in leads if l["status"] == "day7")
    booked_count = sum(1 for l in leads if l["status"] == "booked")
    won_count = sum(1 for l in leads if l["status"] == "won")

    total_pipeline_val = sum(l["value"] for l in leads)
    closed_val = sum(l["value"] for l in leads if l["status"] == "won")
    mrr_val = sum(l["retainer"] for l in leads if l["status"] == "won")

    print("=" * 70)
    print("📊 B2B CLIENT PIPELINE CRM — EXECUTIVE DASHBOARD")
    print("=" * 70)
    print(f"  • Total Prospects:         {total}")
    print(f"  • ⚪ Untouched (New):       {new_count}")
    print(f"  • 🎯 Day 1 Hook Sent:      {day1_count}")
    print(f"  • 📈 Day 3 Follow-Up Sent: {day3_count}")
    print(f"  • 🚪 Day 7 Break-Up Sent:  {day7_count}")
    print(f"  • 📞 Discovery Calls Booked: {booked_count}")
    print(f"  • 🏆 Won Retainer Clients:  {won_count}")
    print("-" * 70)
    print(f"  💰 Total Pipeline Potential: ${total_pipeline_val:,}")
    print(f"  💵 Closed Upfront Setup:     ${closed_val:,}")
    print(f"  🔄 Recurring Monthly Retainer: ${mrr_val:,}/month")
    print("=" * 70)

def update_lead_status(lead_id, new_status):
    leads = load_pipeline()
    found = False
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    for l in leads:
        if l["id"] == lead_id:
            old = l["status"]
            l["status"] = new_status
            l["last_touch"] = now
            found = True
            print(f"[✓] Lead #{lead_id} ({l['name']}): Status updated from '{old}' -> '{new_status}' at {now}")
            break
            
    if found:
        save_pipeline(leads)
    else:
        print(f"[!] Lead #{lead_id} not found in CRM.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage B2B Client Pipeline CRM")
    parser.add_argument("--summary", action="store_true", help="Print pipeline summary")
    parser.add_argument("--id", type=int, help="Lead ID to update (1-30)")
    parser.add_argument("--status", choices=["new", "day1", "day3", "day7", "booked", "won"], help="New status for lead")

    args = parser.parse_args()

    if args.id and args.status:
        update_lead_status(args.id, args.status)
    else:
        print_summary()
