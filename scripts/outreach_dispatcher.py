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
    {"id": 2, "batch": 1, "name": "Pure Radiance MedSpa", "niche": "Aesthetics & Spa", "city": "Miami, FL", "to": "info@pureradiancemedspa.example", "doc": "Sarah", "type": "medspa", "val": 650, "lost": 16},
    {"id": 3, "batch": 1, "name": "Premier 24/7 HVAC", "niche": "Heating & AC Repair", "city": "Dallas, TX", "to": "service@premierairdfw.example", "doc": "Mark", "type": "hvac", "val": 850, "lost": 15},
    {"id": 4, "batch": 1, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Jose, CA", "to": "hello@elitesmilestudio.example", "doc": "Dr. Nguyen", "type": "dental", "val": 950, "lost": 14},
    {"id": 5, "batch": 1, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar", "city": "Phoenix, AZ", "to": "bids@apexroofsolar.example", "doc": "David", "type": "hvac", "val": 3500, "lost": 6},
    {"id": 6, "batch": 1, "name": "Lumina Wellness", "niche": "Regenerative Med", "city": "Seattle, WA", "to": "frontdesk@luminawellness.example", "doc": "Dr. Adams", "type": "medspa", "val": 600, "lost": 18},
    {"id": 7, "batch": 1, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Denver, CO", "to": "team@vanguardluxuryre.example", "doc": "Alex", "type": "realestate", "val": 4000, "lost": 5},
    {"id": 8, "batch": 1, "name": "ProActive Spine & Chiro", "niche": "Chiropractic", "city": "Chicago, IL", "to": "appointments@proactivechiro.example", "doc": "Dr. Davis", "type": "dental", "val": 450, "lost": 22},
    {"id": 9, "batch": 1, "name": "Rapid Response Plumbing", "niche": "24/7 Emergency Plumber", "city": "Atlanta, GA", "to": "dispatch@rapidplumbatl.example", "doc": "Robert", "type": "hvac", "val": 600, "lost": 20},
    {"id": 10, "batch": 1, "name": "Silicon Valley Skin Lab", "niche": "Dermatology & Laser", "city": "Palo Alto, CA", "to": "support@svskinlab.example", "doc": "Dr. Patel", "type": "medspa", "val": 750, "lost": 16},

    # --- BATCH 2: E-Commerce & SaaS ---
    {"id": 11, "batch": 2, "name": "Velora Activewear", "niche": "Athleisure Apparel", "city": "Los Angeles, CA", "to": "hello@veloraactive.example", "doc": "Team Velora", "type": "ecom", "val": 120, "lost": 65},
    {"id": 12, "batch": 2, "name": "NuvoGlow Skincare", "niche": "Clean D2C Beauty", "city": "New York, NY", "to": "partners@nuvoglowbeauty.example", "doc": "Founder", "type": "ecom", "val": 95, "lost": 80},
    {"id": 13, "batch": 2, "name": "PulseMetrics AI", "niche": "B2B Analytics SaaS", "city": "San Francisco, CA", "to": "growth@pulsemetrics.example", "doc": "Founder", "type": "saas", "val": 2200, "lost": 6},
    {"id": 14, "batch": 2, "name": "HydroFlow Bottle", "niche": "Eco Hydration D2C", "city": "Boulder, CO", "to": "support@hydroflowbottle.example", "doc": "Team HydroFlow", "type": "ecom", "val": 75, "lost": 95},
    {"id": 15, "batch": 2, "name": "CloudDesk Help", "niche": "Customer Support SaaS", "city": "Austin, TX", "to": "hello@clouddeskhelp.example", "doc": "Product Lead", "type": "saas", "val": 1200, "lost": 9},
    {"id": 16, "batch": 2, "name": "Artisan Roast Club", "niche": "Subscription Coffee", "city": "Portland, OR", "to": "orders@artisanroastclub.example", "doc": "Founder", "type": "ecom", "val": 85, "lost": 90},
    {"id": 17, "batch": 2, "name": "StackSync Dev", "niche": "Developer Workflows", "city": "Seattle, WA", "to": "founders@stacksyncdev.example", "doc": "Engineering Lead", "type": "saas", "val": 1400, "lost": 8},
    {"id": 18, "batch": 2, "name": "Pawsome Pet Boxes", "niche": "Pet Subscription D2C", "city": "Denver, CO", "to": "hello@pawsomepetbox.example", "doc": "Customer Team", "type": "ecom", "val": 65, "lost": 110},
    {"id": 19, "batch": 2, "name": "LeadFlow CRM", "niche": "SMB Sales CRM SaaS", "city": "Boston, MA", "to": "inquiries@leadflowcrm.example", "doc": "Growth Team", "type": "saas", "val": 1800, "lost": 7},
    {"id": 20, "batch": 2, "name": "ZenSleep Mattress", "niche": "D2C Sleep Wellness", "city": "Chicago, IL", "to": "concierge@zensleepbed.example", "doc": "Marketing Team", "type": "ecom", "val": 850, "lost": 12},

    # --- BATCH 3: High-Ticket Professional Services ---
    {"id": 21, "batch": 3, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "to": "contact@sterlinglegalchi.example", "doc": "David Sterling", "type": "legal", "val": 2500, "lost": 8},
    {"id": 22, "batch": 3, "name": "Summit Crest Luxury Realty", "niche": "Luxury Real Estate", "city": "Aspen, CO", "to": "inquiries@summitcrestrealty.example", "doc": "Victoria Vance", "type": "realestate", "val": 4000, "lost": 5},
    {"id": 23, "batch": 3, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Advisory Firm", "city": "Boston, MA", "to": "tax@beaconhillcpa.example", "doc": "Marcus Brody", "type": "cpa", "val": 1200, "lost": 10},
    {"id": 24, "batch": 3, "name": "Pacific Coast Family Law", "niche": "Divorce & Family Law", "city": "San Diego, CA", "to": "help@pacificfamilylawsd.example", "doc": "Elena Rostova", "type": "legal", "val": 3000, "lost": 6},
    {"id": 25, "batch": 3, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "to": "office@vanguardwealthnyc.example", "doc": "Jonathan Vance", "type": "cpa", "val": 2800, "lost": 5},
    {"id": 26, "batch": 3, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "to": "hello@redwoodcounseltx.example", "doc": "Sarah Jenkins", "type": "legal", "val": 3500, "lost": 5},
    {"id": 27, "batch": 3, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "to": "deals@pinnaclecredfw.example", "doc": "Robert Miller", "type": "realestate", "val": 4500, "lost": 4},
    {"id": 28, "batch": 3, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "to": "info@harborviewestateswa.example", "doc": "Cynthia Thorne", "type": "legal", "val": 2200, "lost": 7},
    {"id": 29, "batch": 3, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "to": "valuation@apexauditadvisory.example", "doc": "Richard Hall", "type": "cpa", "val": 3200, "lost": 5},
    {"id": 30, "batch": 3, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "to": "litigation@metroinjurydefense.example", "doc": "Carlos Mendez", "type": "legal", "val": 4000, "lost": 4}
]

# Dynamically append Batch 4, 5, 6
try:
    from expand_crm_pipeline import NEW_LEADS
    for nl in NEW_LEADS:
        if not any(l["id"] == nl["id"] for l in LEADS):
            LEADS.append(nl)
except Exception:
    pass

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
    niche = lead.get("niche", "")

    ltype = lead.get("type", "dental")

    if stage == 2:
        if ltype == "ecom":
            subject = f"re: {name} cart abandonment & shopper questions (ran the numbers)"
            body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s on-site conversion.

I ran {name}'s estimated shopper volume through our revenue recovery model:
• Estimated monthly abandoned carts from hesitation: ~{lead['lost']} shoppers
• Estimated uncaptured revenue: ~${monthly_loss}/month

You can review your customized performance & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our AI shopping copilot proactively assists shoppers right before drop-off, recovering 8% to 15% of abandoned carts within the first 30 days.

I also prepared a customized 2-page implementation audit for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
E-Commerce Automation Consultant
Live Sandbox: {sandbox_url}"""

        elif ltype == "saas":
            subject = f"re: {name} trial user drop-off & activation (ran the numbers)"
            body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s trial user onboarding experience.

I ran {name}'s estimated user funnel through our activation model:
• Estimated trial signups hitting setup friction: ~{lead['lost']} users/month
• Estimated lost expansion / ARR: ~${monthly_loss}/month

You can review your customized activation & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our conversational AI onboarding agent resolves integration blockers in real-time, accelerating time-to-value and lifting trial conversion by 12% to 20%.

I also prepared a customized 2-page implementation audit for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
SaaS Growth & AI Systems
Live Sandbox: {sandbox_url}"""

        elif ltype in ("legal", "realestate", "cpa"):
            subject = f"re: {name} high-intent client inquiries (ran the numbers)"
            body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s after-hours intake.

I ran {name}'s estimated high-intent inquiry volume through our revenue recovery model:
• Estimated monthly prospective clients seeking help after 6 PM: ~{lead['lost']} qualified leads
• Estimated uncaptured case/client value: ~${monthly_loss}/month

You can review your customized firm performance & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our AI intake copilot pre-qualifies prospective clients and books appointments into your calendar 24/7, paying for itself on the very first retained client.

I also prepared a customized 2-page implementation audit for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
AI Solutions Architect
Live Sandbox: {sandbox_url}"""

        elif ltype == "medical":
            subject = f"re: {name} private patient inquiry triage (ran the numbers)"
            body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s after-hours patient inquiries.

I ran {name}'s estimated high-intent patient volume through our consultation recovery model:
• Estimated monthly patients researching treatments after clinic hours: ~{lead['lost']} qualified patients
• Estimated uncaptured case/procedure revenue: ~${monthly_loss}/month

You can review your customized clinic performance & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our AI patient copilot pre-screens procedure candidacy and books private consultations directly into your clinic calendar 24/7, paying for itself on the first booked procedure.

I also prepared a customized 2-page implementation roadmap for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
Healthcare AI Systems Specialist
Live Sandbox: {sandbox_url}"""

        elif ltype == "contractor":
            subject = f"re: {name} high-value project inquiries (ran the numbers)"
            body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s after-hours project leads.

I ran {name}'s estimated inquiry volume through our contractor revenue model:
• Estimated monthly project inquiries after 6 PM / weekends: ~{lead['lost']} project briefs
• Estimated uncaptured project contract value: ~${monthly_loss}/month

You can review your customized firm performance & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our AI project estimator pre-qualifies project scopes, budget ranges, and books site inspections directly into your schedule 24/7.

I also prepared a customized 2-page implementation plan for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
Construction & High-End Trades AI Systems
Live Sandbox: {sandbox_url}"""

        elif ltype in ("agency", "staffing"):
            subject = f"re: {name} inbound lead qualification (ran the numbers)"
            body = f"""Hi {doc},

Following up briefly on my note from earlier this week regarding {name}'s inbound client qualification.

I ran {name}'s estimated inbound volume through our agency conversion model:
• Estimated monthly inbound briefs lost to delayed response: ~{lead['lost']} qualified accounts
• Estimated uncaptured retainer/deal value: ~${monthly_loss}/month

You can review your customized agency performance & ROI forecast here:
👉 Live Custom ROI Report: {report_url}
👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator
👉 Executive VIP Client Portal: {portal_url}

Our conversational AI agency copilot pre-qualifies budget fit and books qualified discovery calls directly into your calendar 24/7.

I also prepared a customized 2-page workflow audit for {name}. Would you be against me sending it over?

Best regards,
Minh Lap
Agency Automation & Growth Architect
Live Sandbox: {sandbox_url}"""

        else:
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
        if ltype == "ecom":
            subject = f"permission to close out {name}'s conversion audit, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume that recapturing abandoned carts and deploying autonomous shopper assistance isn't a priority for {name} right now.

I'm archiving {name}'s conversion audit so I don't clutter your inbox.

If checkout conversion ever becomes a focus and you'd like to see how similar D2C brands are lifting revenue by 12% to 18% with conversational AI, your live prototype will remain active here:
👉 Live Shopper Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} continued scale and success!

Warm regards,
Minh Lap
E-Commerce Automation Consultant"""

        elif ltype == "saas":
            subject = f"closing out {name}'s onboarding audit, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume accelerating trial user activation and eliminating onboarding friction isn't on your radar for {name} this quarter.

I'm archiving {name}'s copilot file so I don't crowd your inbox.

If trial activation and self-serve retention become a priority down the road, your team can always explore your live interactive copilot here:
👉 Live Copilot Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} massive product growth!

Cheers,
Minh Lap
SaaS Growth & AI Systems"""

        elif ltype in ("legal", "realestate", "cpa"):
            subject = f"permission to archive {name}'s intake file, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume capturing after-hours prospective client inquiries and automating intake isn't a priority for {name} right now.

I'm closing out your firm's file so I don't clutter your inbox. We typically only work with one premier practice in {city} to prevent competitive overlap.

If your team ever decides to explore how AI intake copilots pre-qualify and retain high-value matters 24/7, your prototype remains accessible:
👉 Firm Live Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} continued distinction and growth!

Best regards,
Minh Lap
AI Solutions Architect"""

        elif ltype == "medical":
            subject = f"permission to archive {name}'s patient intake file, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume that automating after-hours patient inquiry triage and consultation booking isn't a priority for {name} right now.

I'm closing out your practice's file so I don't clutter your inbox. We only work with one premier provider in {city} to prevent competitive overlap.

If your team ever decides to explore how AI triage copilots pre-screen and retain high-value private patients 24/7, your prototype remains accessible:
👉 Practice Live Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} continued clinical distinction and patient growth!

Warm regards,
Minh Lap
Healthcare AI Systems Specialist"""

        elif ltype == "contractor":
            subject = f"permission to close {name}'s estimating file, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume that capturing after-hours project briefs and automating consultation bookings isn't a focus for {name} right now.

I'm archiving your firm's file so I don't crowd your inbox. We only partner with one top firm in {city} to prevent competitive overlap.

If you ever want to see how high-end builders and contractors in {city} are capturing high-ticket projects 24/7 without extra estimating staff, your live prototype remains open:
👉 Project Live Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} continued scale on your projects!

Cheers,
Minh Lap
Construction & High-End Trades AI Systems"""

        elif ltype in ("agency", "staffing"):
            subject = f"closing out {name}'s qualification file, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume that automating inbound client pre-qualification and discovery booking isn't a priority for {name} right now.

I'm archiving your agency's file so I don't crowd your inbox.

If inbound lead velocity and pre-qualification become a focus down the road, your team can always test your live interactive copilot here:
👉 Live Copilot Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} continued growth and killer client results!

Best regards,
Minh Lap
Agency Automation & Growth Architect"""

        else:
            subject = f"permission to close your file, {doc}?"
            body = f"""Hi {doc},

I haven't heard back, so I assume that automating after-hours client booking and recapturing missed calls isn't a priority for {name} right now.

I'm closing out your file so I don't clutter your inbox. We only partner with one provider in {city} to avoid competitive overlap.

If priorities ever shift and you'd like to see how similar businesses in {city} are automatically booking clients 24/7 without extra staff, you're always welcome to test your live sandbox prototype:
👉 Live Sandbox: {sandbox_url}
👉 Executive VIP Client Portal: {portal_url}

Wishing {name} continued growth and success!

Warm regards,
Minh Lap
AI Solutions Architect"""

    else: # Stage 1
        ltype = lead.get("type", "dental")
        if ltype in ("dental", "medspa"):
            subject = f"quick question regarding {name}'s after-hours patient inquiries"
            body = f"""Hi {doc},

I was reviewing your website yesterday around 8 PM and noticed that when a patient has an urgent question or wants to book an appointment after closing, their only option is to wait until morning.

In most competitive markets, clinics lose 4 to 8 high-intent new patient inquiries every single week simply because competitors with instant AI booking respond within 30 seconds.

To show you how easy this is to solve, I set up a live interactive sandbox prototype specifically for {name}:
👉 Live Sandbox Demo: {sandbox_url}

It answers common treatment questions, qualifies insurance, and books appointments directly into your calendar 24/7.

Would you be open to a quick 5-minute call this Thursday at 2 PM to see if this makes sense for {name}?

Best regards,
Minh Lap
AI Solutions Architect
Live Sandbox: {sandbox_url}"""

        elif ltype == "medical":
            subject = f"quick question regarding {name}'s after-hours patient inquiries"
            body = f"""Hi {doc},

I was reviewing your website yesterday around 8 PM and noticed that when a prospective patient has questions about high-ticket elective procedures or wants to book a private consultation after clinic hours, their only option is to wait until morning.

In specialized private healthcare, prospective patients typically compare 2 to 3 top clinics in {city}. Practices with instant AI patient triage & scheduling convert 35%+ more high-ticket consultations directly into the calendar.

To show you how this works, I built an interactive patient triage sandbox specifically for {name}:
👉 Live Patient Sandbox: {sandbox_url}

It conducts confidential pre-qualification, answers procedure FAQs, and schedules private consultations 24/7.

Would you be open to a quick 5-minute call this Thursday at 2 PM to explore if this makes sense for {name}?

Best regards,
Minh Lap
Healthcare AI Systems Specialist
Live Sandbox: {sandbox_url}"""

        elif ltype == "contractor":
            subject = f"capturing after-hours project inquiries for {name}"
            body = f"""Hi {doc},

When property owners or developers are researching high-end renovation, construction, or installation projects in the evening or over the weekend, they want immediate answers on project scopes, estimating timelines, and consultation bookings.

When they hit an after-hours contact form or voicemail, over 60% continue browsing and submit project briefs to competitors.

We deploy intelligent intake and estimating copilots that engage prospects immediately, gather project specs, qualify budget ranges, and book design consultations directly into your calendar 24/7.

Check out your firm's customized project intake sandbox here:
👉 Live Project Sandbox: {sandbox_url}

Would you be open to a quick 5-minute conversation this Thursday to see how this captures 3 to 5 additional high-ticket contracts every month?

Cheers,
Minh Lap
Construction & High-End Trades AI Systems
Live Sandbox: {sandbox_url}"""

        elif ltype in ("agency", "staffing"):
            subject = f"streamlining inbound client qualification for {name}"
            body = f"""Hi {doc},

Love what {name} is doing in {niche}.

When high-intent enterprise brands or hiring managers land on your site, they want immediate clarity on service fit, bandwidth, pricing tiers, and case studies before committing to a discovery call.

We deploy conversational AI agency copilots that pre-qualify inbound briefs, verify budget thresholds, showcase relevant case study wins, and book qualified discovery calls 24/7.

Check out your agency's interactive intake copilot here:
👉 Live Sandbox: {sandbox_url}

Open to a brief 5-minute chat this Wednesday to see how this saves your leadership team 10+ hours a week on unqualified calls?

Best,
Minh Lap
Agency Automation & Growth Architect
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
    import html
    for l in filtered[:5]:
        slug = l["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
        safe_name = html.escape(l["name"])
        lines.append(f"• <b>{safe_name}</b> ({l['city']}) — <a href='https://work-minh-lap.vercel.app/portal/{slug}'>VIP Portal</a> | <a href='https://work-minh-lap.vercel.app/sandboxes/{slug}_sandbox.html'>Sandbox</a>")
    
    lines.append("\n👉 <i>1-Click Send available in Command Center at https://work-minh-lap.vercel.app</i>")
    
    html_msg = "\n".join(lines)
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=12) as r:
            if r.status == 200:
                print("[✓] Dispatched Outreach Campaign Digest to Telegram (@Minhpv_bot)!")
                return
    except Exception:
        pass

    # Fallback to curl.exe with temp payload file for 100% reliability on Windows
    try:
        import subprocess
        payload_file = ROOT_DIR / "temp_tg_outreach.json"
        payload_file.write_text(json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}, ensure_ascii=False), encoding="utf-8")
        res = subprocess.run(
            ["curl.exe", "-s", "--connect-timeout", "10", "--max-time", "20", "-X", "POST",
             "-H", "Content-Type: application/json; charset=utf-8",
             "-d", f"@{payload_file.name}",
             f"https://api.telegram.org/bot{bot_token}/sendMessage"],
            capture_output=True, text=True, timeout=22, cwd=str(ROOT_DIR)
        )
        if payload_file.exists():
            payload_file.unlink()
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
    parser.add_argument("--batch", type=int, choices=[1, 2, 3, 4, 5, 6], help="Filter by Batch (1-6: SMBs, E-Com, High-Ticket, Luxury Home, B2B Agencies, Luxury Health)")
    parser.add_argument("--stage", type=int, default=1, choices=[1, 2, 3], help="Stage (1: Day 1 Hook, 2: Day 3 ROI, 3: Day 7 Break-Up)")
    parser.add_argument("--lead", type=int, help="Single Lead ID (1-60)")
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

