#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autonomous Multi-Touch Cold Outreach Dispatcher & Campaign Engine
-----------------------------------------------------------------
Quản lý và điều hướng toàn bộ 3 chiến dịch Cold Outreach (30 Leads):
- Batch 1: Local SMBs (Nha khoa, MedSpa, HVAC, Chiro, Roofing)
- Batch 2: E-Commerce D2C & B2B SaaS Startups
- Batch 3: High-Ticket Professional Services (Luật sư, Bất động sản, CPA)

Hỗ trợ 3 giai đoạn tiếp cận:
- Stage 1: Day 1 Cold Hook (Nhúng link Live Client Sandbox tương tác)
- Stage 2: Day 3 ROI Value Follow-Up (Nhúng link Custom ROI Report + Calculator)
- Stage 3: Day 7 Break-Up Email (Đóng hồ sơ & link Sandbox lần cuối)
"""

import os
import sys
import re
import argparse
import urllib.parse
import urllib.request
import json
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

LEADS = [
    # --- BATCH 1: Local SMBs ---
    {"id": 1, "batch": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX", "to": "contact@austindentalco.example", "doc": "Dr. Miller", "type": "dental", "val": 750, "lost": 18},
    {"id": 2, "batch": 1, "name": "Pure Radiance MedSpa", "niche": "Aesthetics & Medical Spa", "city": "Miami, FL", "to": "info@pureradiancemedspa.example", "doc": "Sarah", "type": "medspa", "val": 650, "lost": 16},
    {"id": 3, "batch": 1, "name": "Premier 24/7 HVAC Services", "niche": "Emergency Heating & AC", "city": "Dallas, TX", "to": "service@premierairdfw.example", "doc": "Mark", "type": "hvac", "val": 850, "lost": 15},
    {"id": 4, "batch": 1, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "to": "contact@sterlinglegalchi.example", "doc": "David Sterling", "type": "legal", "val": 2500, "lost": 8},
    {"id": 5, "batch": 1, "name": "Summit Crest Luxury Realty", "niche": "High-End Real Estate", "city": "Scottsdale, AZ", "to": "inquiries@summitcrestrealty.example", "doc": "Victoria Vance", "type": "realestate", "val": 4000, "lost": 5},
    {"id": 6, "batch": 1, "name": "ProActive Spine & Chiro", "niche": "Chiropractic & Wellness", "city": "Denver, CO", "to": "appointments@proactivechiro.example", "doc": "Dr. Davis", "type": "dental", "val": 450, "lost": 22},
    {"id": 7, "batch": 1, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Wealth Advisory", "city": "Boston, MA", "to": "tax@beaconhillcpa.example", "doc": "Marcus Brody", "type": "cpa", "val": 1200, "lost": 10},
    {"id": 8, "batch": 1, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Diego, CA", "to": "hello@elitesmilestudio.example", "doc": "Dr. Nguyen", "type": "dental", "val": 950, "lost": 14},
    {"id": 9, "batch": 1, "name": "Rapid Response Plumbing", "niche": "Commercial Plumbing", "city": "Atlanta, GA", "to": "dispatch@rapidplumbatl.example", "doc": "Robert", "type": "hvac", "val": 600, "lost": 20},
    {"id": 10, "batch": 1, "name": "Apex Roofing & Solar Systems", "niche": "Roofing & Solar EPC", "city": "Orlando, FL", "to": "bids@apexroofsolar.example", "doc": "David", "type": "hvac", "val": 3500, "lost": 6},

    # --- BATCH 2: E-Commerce & SaaS ---
    {"id": 11, "batch": 2, "name": "Velora Activewear", "niche": "Athleisure & Fitness", "city": "Los Angeles, CA", "to": "hello@veloraactive.example", "doc": "Team Velora", "type": "ecom", "val": 120, "lost": 65},
    {"id": 12, "batch": 2, "name": "NuvoGlow Skincare", "niche": "Clean Beauty & Cosmetics", "city": "New York, NY", "to": "partners@nuvoglowbeauty.example", "doc": "Founder", "type": "ecom", "val": 95, "lost": 80},
    {"id": 13, "batch": 2, "name": "Artisan Roast Club", "niche": "Specialty Coffee Subscription", "city": "Seattle, WA", "to": "orders@artisanroastclub.example", "doc": "Founder", "type": "ecom", "val": 85, "lost": 90},
    {"id": 14, "batch": 2, "name": "ZenSleep Mattress", "niche": "Sleep Tech & Bedding", "city": "San Francisco, CA", "to": "concierge@zensleepbed.example", "doc": "Marketing Team", "type": "ecom", "val": 850, "lost": 12},
    {"id": 15, "batch": 2, "name": "HydroFlow Bottle", "niche": "Smart Hydration & Gear", "city": "Boulder, CO", "to": "support@hydroflowbottle.example", "doc": "Team HydroFlow", "type": "ecom", "val": 75, "lost": 95},
    {"id": 16, "batch": 2, "name": "Pawsome Pet Boxes", "niche": "Pet Supplies & Subscriptions", "city": "Austin, TX", "to": "hello@pawsomepetbox.example", "doc": "Customer Team", "type": "ecom", "val": 65, "lost": 110},
    {"id": 17, "batch": 2, "name": "Lumina Wellness", "niche": "Nootropics & Supplements", "city": "Miami, FL", "to": "frontdesk@luminawellness.example", "doc": "Dr. Adams", "type": "medspa", "val": 110, "lost": 70},
    {"id": 18, "batch": 2, "name": "StackSync Dev", "niche": "Developer Tools & SaaS", "city": "San Jose, CA", "to": "founders@stacksyncdev.example", "doc": "Engineering Lead", "type": "saas", "val": 1400, "lost": 8},
    {"id": 19, "batch": 2, "name": "LeadFlow CRM", "niche": "B2B Sales Automation", "city": "Chicago, IL", "to": "inquiries@leadflowcrm.example", "doc": "Growth Team", "type": "saas", "val": 1800, "lost": 7},
    {"id": 20, "batch": 2, "name": "CloudDesk Help", "niche": "Customer Support Platform", "city": "Boston, MA", "to": "hello@clouddeskhelp.example", "doc": "Product Lead", "type": "saas", "val": 1200, "lost": 9},

    # --- BATCH 3: High-Ticket Professional Services ---
    {"id": 21, "batch": 3, "name": "PulseMetrics AI", "niche": "Product Analytics SaaS", "city": "New York, NY", "to": "growth@pulsemetrics.example", "doc": "Founder", "type": "saas", "val": 2200, "lost": 6},
    {"id": 22, "batch": 3, "name": "Silicon Valley Skin Lab", "niche": "Dermatology Clinic", "city": "Palo Alto, CA", "to": "support@svskinlab.example", "doc": "Dr. Patel", "type": "medspa", "val": 750, "lost": 16},
    {"id": 23, "batch": 3, "name": "Pacific Coast Family Law", "niche": "Family Law & Mediation", "city": "Newport Beach, CA", "to": "help@pacificfamilylawsd.example", "doc": "Elena Rostova", "type": "legal", "val": 3000, "lost": 6},
    {"id": 24, "batch": 3, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Beverly Hills, CA", "to": "team@vanguardluxuryre.example", "doc": "Alex", "type": "realestate", "val": 5000, "lost": 4},
    {"id": 25, "batch": 3, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "to": "office@vanguardwealthnyc.example", "doc": "Jonathan Vance", "type": "cpa", "val": 2800, "lost": 5},
    {"id": 26, "batch": 3, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "to": "hello@redwoodcounseltx.example", "doc": "Sarah Jenkins", "type": "legal", "val": 3500, "lost": 5},
    {"id": 27, "batch": 3, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "to": "deals@pinnaclecredfw.example", "doc": "Robert Miller", "type": "realestate", "val": 4500, "lost": 4},
    {"id": 28, "batch": 3, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "to": "info@harborviewestateswa.example", "doc": "Cynthia Thorne", "type": "legal", "val": 2200, "lost": 7},
    {"id": 29, "batch": 3, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "to": "valuation@apexauditadvisory.example", "doc": "Richard Hall", "type": "cpa", "val": 3200, "lost": 5},
    {"id": 30, "batch": 3, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "to": "litigation@metroinjurydefense.example", "doc": "Carlos Mendez", "type": "legal", "val": 4000, "lost": 4}
]

def build_email_content(lead, stage=1):
    slug = lead["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
    sandbox_url = f"https://work-minh-lap.vercel.app/sandboxes/{slug}_sandbox.html"
    report_url = f"https://work-minh-lap.vercel.app/reports/{slug}_roi_report.html"
    pitch_url = f"https://work-minh-lap.vercel.app/pitches/{slug}_pitch.html"
    portal_url = f"https://work-minh-lap.vercel.app/portal/{slug}"

    monthly_loss = f"{(lead['lost'] * lead['val']):,}"
    name = lead["name"]
    doc = lead["doc"]
    city = lead["city"]

    if stage == 2:
        subject = f"re: {name} after-hours intake (ran the numbers)"
        body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s after-hours client intake.

I ran {name}'s estimated inquiry volume through our revenue recovery model:
• Estimated monthly inquiries after 6 PM: ~{lead['lost']} prospects
• Estimated missed revenue: ~${monthly_loss}/month

You can review your customized monthly performance & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our AI intake copilot typically recovers 4 to 8 qualified client bookings within the first 30 days, paying for itself several times over.

I also prepared a customized 2-page implementation audit for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
AI Solutions Architect
Live Sandbox: {sandbox_url}"""

    elif stage == 3:
        subject = f"permission to close your file, {doc}?"
        body = f"""Hi {doc},

I haven't heard back, so I assume that automating after-hours client intake and recapturing missed inquiries isn't a priority for {name} right now.

I'm closing out your file so I don't clutter your inbox.

If priorities ever shift and you'd like to see how similar businesses in {city} are automatically booking clients 24/7 without extra staff, you're always welcome to test your live sandbox prototype:
👉 Live Sandbox: {sandbox_url}
👉 Executive VIP Portal: {portal_url}

Wishing {name} continued growth and success!

Warm regards,
Minh Lap
AI Solutions Architect"""

    else: # Stage 1
        ltype = lead.get("type", "dental")
        if ltype == "dental":
            subject = f"quick question regarding {name}'s after-hours patient inquiries"
            body = f"""Hi {doc},

I was reviewing your website yesterday around 8 PM and noticed that when a patient has an urgent dental question or wants to book an appointment after closing, their only option is to wait until morning.

In most competitive markets, clinics lose 4 to 8 high-intent new patient inquiries every single week simply because competitors with instant AI booking respond within 30 seconds.

To show you how easy this is to solve, I set up a live interactive sandbox prototype specifically for {name}:
👉 Live Sandbox Demo: {sandbox_url}

It answers common treatment questions, qualifies insurance, and books appointments directly into your calendar 24/7.

Would you be open to a quick 5-minute call this Thursday at 2 PM to see if this makes sense for {name}?

Best regards,
Minh Lap
AI Solutions Architect
Live Sandbox: {sandbox_url}"""

        elif ltype == "hvac":
            subject = f"noticed your phone line around 7:15pm yesterday"
            body = f"""Hi {doc},

When a homeowner has an emergency leak or broken AC after 6 PM, 85% of them will immediately hang up if they reach a voicemail and call the next contractor on Google.

We implemented an automated 15-second AI text-back workflow: whenever your line is busy or closed, an instant text goes out:
"Hi! We are currently assisting another client. Do you have an urgent service request?"

This single workflow captured $9,200 in recovered emergency jobs for a local contractor last month.

I also set up an interactive test sandbox for {name}:
👉 Live Sandbox: {sandbox_url}

Happy to share a 2-minute video walkthrough showing how this works if you find it helpful.

Cheers,
Minh Lap
AI Workflow Specialist"""

        elif ltype == "ecom":
            subject = f"quick idea on recovering abandoned carts for {name}"
            body = f"""Hi {doc},

Love what you're building at {name}!

Noticed that visitors who leave items in cart often drop off due to sizing, delivery, or return policy questions before checkout.

We build autonomous AI shopper assistants that engage hesitant shoppers right before drop-off, answering questions in real-time and offering personalized incentive bundles.

Take a look at how this operates on your live prototype:
👉 Live Sandbox: {sandbox_url}

Would love to share 2 quick ideas that boosted checkout conversions by 14% for similar D2C brands. Free for a 5-min chat this week?

Best,
Minh Lap
E-Commerce Automation Consultant"""

        elif ltype == "saas":
            subject = f"boosting activation for {name} trial signups"
            body = f"""Hi {doc},

Big fan of {name}!

I noticed that many self-serve SaaS users drop off during the first 48 hours when they hit an integration or setup blocker. Static documentation often isn't enough to prevent churn.

We build conversational onboarding AI copilots trained on your API docs and changelog that proactively assist trial users in hitting their 'Aha!' moment within minutes.

Check out your live prototype here:
👉 Live Sandbox: {sandbox_url}

Open to a quick 5-min feedback chat this Wednesday at 10 AM PST?

Cheers,
Minh Lap
SaaS Growth & AI Systems"""

        elif ltype == "legal":
            subject = f"quick question regarding {name}'s after-hours intake process"
            body = f"""Hi {doc},

I was reviewing your website yesterday evening around 8:30 PM and noticed that potential new clients facing an urgent legal matter only have a standard static form.

In high-stakes cases, 67% of prospective claimants contact 2 to 3 firms simultaneously. The firm that responds, qualifies, and schedules within 3 minutes captures 80% of retained cases.

We built an intelligent legal intake assistant that conducts an empathetic intake questionnaire, screens jurisdiction & merit, and schedules onto your calendar 24/7.

Test your firm's customized sandbox prototype here:
👉 Live Sandbox: {sandbox_url}

Open to a brief 7-minute call this Thursday at 2 PM to explore if this could add 3-5 retained cases/month to {name}?

Best regards,
Minh Lap
AI Legal Workflow Automation"""

        elif ltype == "realestate":
            subject = f"capturing after-hours buyer inquiries for {name} listings"
            body = f"""Hi {doc},

Your active luxury listings look exceptional.

When high-net-worth buyers browse properties on weekends or late at night, they expect instant answers regarding HOA rules, lot dimensions, and private showing availability.

We deploy bespoke AI Concierge agents that answer deep questions from your MLS data, pre-qualify buyers, and coordinate VIP private showings straight into your calendar 24/7.

Test your agency's live concierge sandbox here:
👉 Live Sandbox: {sandbox_url}

Available for a 5-minute conversation this Thursday to see what this looks like with your active listings?

Warm regards,
Minh Lap
High-Ticket Automation Systems"""

        elif ltype == "cpa":
            subject = f"eliminating 15+ hours/week of client document chasing for {name}"
            body = f"""Hi {doc},

As tax season and quarterly filings approach, the single biggest drain on billable partner hours is chasing clients for missing 1099s, W2s, and receipts.

We build autonomous document-collection pipelines using AI OCR and Make.com that send automated reminder loops, verify document clarity with AI vision, and sync files directly into client folders and accounting software.

Firms save an average of 18 hours per accountant every month while accelerating client turnaround by 40%.

Test your firm's intake sandbox here:
👉 Live Sandbox: {sandbox_url}

Would you be against me sending over a 2-minute video walkthrough showing how this workflow operates?

Cheers,
Minh Lap
AI Workflow Automation Consultant"""

        else:
            subject = f"automated consultation booking for {name}"
            body = f"""Hi {doc},

Love the work you do at {name}!

I noticed that you receive a lot of inquiries regarding treatment pricing and booking. Many potential clients browse late at night and drop off before ever booking a consultation.

We build custom AI assistants that engage visitors, recommend treatment options, and lock in paid consultation deposits while you sleep.

Take a look at how seamless the patient experience is on your live sandbox:
👉 Live Sandbox: {sandbox_url}

Would you be against me sending over a 3-minute video showing what this would look like for {name}?

Warm regards,
Minh Lap
AI Client Acquisition Systems"""

    return subject, body

def get_mailto_url(recipient, subject, body):
    params = {
        "subject": subject,
        "body": body
    }
    return f"mailto:{recipient}?{urllib.parse.urlencode(params, quote_via=urllib.parse.quote)}"

def display_campaign(batch=None, stage=1):
    filtered = LEADS if not batch else [l for l in LEADS if l["batch"] == batch]
    stage_titles = {
        1: "🎯 STAGE 1: COLD HOOK (LIVE SANDBOX EMBED)",
        2: "📈 STAGE 2: ROI VALUE FOLLOW-UP (CUSTOM REPORT EMBED)",
        3: "🚪 STAGE 3: BREAK-UP EMAIL (FINAL FOMO CLOSE)"
    }

    print("=" * 80)
    print(f"🚀 AI MONEY MACHINE — OUTREACH DISPATCH ENGINE | {stage_titles[stage]}")
    print(f"📊 Filter: {'All 30 Leads' if not batch else f'Batch {batch} (10 Leads)'}")
    print("=" * 80)

    for l in filtered:
        subj, body = build_email_content(l, stage)
        mailto = get_mailto_url(l["to"], subj, body)
        slug = l["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
        pitch_url = f"https://work-minh-lap.vercel.app/pitches/{slug}_pitch.html"

        print(f"\n[#{l['id']:02d}] {l['name']} ({l['niche']} • {l['city']})")
        print(f"  • To:      {l['to']}")
        print(f"  • Subject: {subj}")
        print(f"  • Pitch:   {pitch_url}")
        print(f"  • Mailto:  {mailto[:85]}...")

    print("\n" + "=" * 80)
    print(f"[✓] Displayed {len(filtered)} targeted outreach records!")

def send_telegram_campaign_digest(filtered, stage):
    stage_titles = {
        1: "Stage 1: Day 1 Cold Hook",
        2: "Stage 2: Day 3 ROI Follow-Up",
        3: "Stage 3: Day 7 Break-Up Email"
    }
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")
    
    lines = [
        "📬 <b>OUTREACH CAMPAIGN DISPATCH READY</b>",
        f"🎯 <b>Sequence:</b> {stage_titles.get(stage, 'Stage 1')}",
        f"📊 <b>Targets:</b> {len(filtered)} Enterprise Accounts",
        "🌐 <b>VIP Portal Hub:</b> <a href='https://work-minh-lap.vercel.app/portal'>Launch Hub</a>",
        "",
        "<b>Top Leads in Queue:</b>"
    ]
    for l in filtered[:5]:
        slug = l["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
        lines.append(f"• <b>{l['name']}</b> ({l['city']}) — <a href='https://work-minh-lap.vercel.app/portal/{slug}'>VIP Portal</a> | <a href='https://work-minh-lap.vercel.app/sandboxes/{slug}_sandbox.html'>Sandbox</a>")
    
    lines.append("\n👉 <i>1-Click Send available in Command Center at https://work-minh-lap.vercel.app</i>")
    
    html_msg = "\n".join(lines)
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=5) as r:
            if r.status == 200:
                print("[✓] Dispatched Outreach Campaign Digest to Telegram (@Minhpv_bot)!")
                return
    except Exception:
        pass

    # Fallback to curl.exe for 100% reliability on Windows
    try:
        import subprocess
        res = subprocess.run(
            ["curl.exe", "-s", "-X", "POST",
             "-H", "Content-Type: application/json; charset=utf-8",
             "-d", json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}),
             f"https://api.telegram.org/bot{bot_token}/sendMessage"],
            capture_output=True, text=True, timeout=10
        )
        if '"ok":true' in res.stdout:
            print("[✓] Dispatched Outreach Campaign Digest to Telegram (@Minhpv_bot) via curl!")
        else:
            print(f"[!] Telegram curl error: {res.stdout}")
    except Exception as e:
        print(f"[!] Telegram notification error: {e}")

def update_pipeline_status(leads_to_update, stage):
    crm_file = ROOT_DIR / "prospects" / "crm_pipeline.json"
    if not crm_file.exists():
        return
    try:
        pipeline = json.loads(crm_file.read_text(encoding="utf-8"))
        stage_map = {1: "day1", 2: "day3", 3: "day7"}
        new_status = stage_map.get(stage, "day1")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        target_ids = {l["id"] for l in leads_to_update}
        updated_count = 0
        for item in pipeline:
            if item["id"] in target_ids:
                item["status"] = new_status
                item["last_touch"] = now
                updated_count += 1

        crm_file.write_text(json.dumps(pipeline, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[✓] Updated CRM pipeline: {updated_count} leads transitioned to status '{new_status}' at {now}")
    except Exception as e:
        print(f"[!] Error updating CRM pipeline: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Touch Outreach Campaign Dispatcher")
    parser.add_argument("--batch", type=int, choices=[1, 2, 3], help="Filter by Batch (1: SMBs, 2: E-Com, 3: High-Ticket)")
    parser.add_argument("--stage", type=int, default=1, choices=[1, 2, 3], help="Stage (1: Day 1 Hook, 2: Day 3 ROI, 3: Day 7 Break-Up)")
    parser.add_argument("--lead", type=int, help="Single Lead ID (1-30)")
    parser.add_argument("--telegram", action="store_true", help="Send campaign digest to Telegram")
    parser.add_argument("--mark-sent", action="store_true", help="Update CRM pipeline status to sent stage (day1/day3/day7)")

    args = parser.parse_args()

    if args.lead:
        target = next((l for l in LEADS if l["id"] == args.lead), None)
        if target:
            subj, body = build_email_content(target, args.stage)
            mailto = get_mailto_url(target["to"], subj, body)
            print("=" * 70)
            print(f"Target Lead: {target['name']} (#{target['id']}) - Stage {args.stage}")
            print(f"To: {target['to']}")
            print(f"Subject: {subj}\n")
            print(body)
            print("-" * 70)
            print(f"Mailto Link:\n{mailto}")
            print("=" * 70)
            if args.mark_sent:
                update_pipeline_status([target], args.stage)
        else:
            print(f"[!] Lead ID #{args.lead} not found.")
    else:
        display_campaign(args.batch, args.stage)
        filtered = LEADS if not args.batch else [l for l in LEADS if l["batch"] == args.batch]
        if args.mark_sent:
            update_pipeline_status(filtered, args.stage)
        if args.telegram:
            send_telegram_campaign_digest(filtered, args.stage)

