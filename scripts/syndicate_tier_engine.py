#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — AI Syndicate & Franchise Partner Engine (Phase 4 Expansion)
=============================================================================
Licenses the turnkey AI Money Machine infrastructure to 12 regional agency
licensees worldwide to crack the $1,000,000 / year ARR ($1M ARR) milestone!

Phase 4 Syndicate Franchise Partner Specifications:
- Upfront Private Cloud License & White-Label Setup: $4,950
- Monthly Core Swarm, Retraining & Infrastructure Retainer: $1,250 / month
- Target: 12 Regional Boutique Agencies & Elite Consultancies Worldwide
- Total Syndicate Capacity: +$59,400 Upfront Cash & +$15,000/mo MRR (+$180,000/yr ARR)
- Consolidated Empire Milestone: $260,600 Upfront Cash & $1,002,600 / year ARR!
"""

import sys
import os
import json
import argparse
import urllib.request
import time
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SYNDICATE_DIR = ROOT_DIR / "syndicate_proposals"
PIPELINE_FILE = ROOT_DIR / "prospects" / "syndicate_tier_pipeline.json"

SYNDICATE_PARTNERS = [
    {
        "id": 1,
        "name": "Apex Media Group UK",
        "territory": "London, United Kingdom & Ireland",
        "principal": "Alistair Vance, Managing Partner",
        "current_clients": 42,
        "primary_focus": "Private Wealth, Commercial Real Estate & High-End Medical",
        "slug": "apex_media_group_uk"
    },
    {
        "id": 2,
        "name": "Pacifica Digital Ventures",
        "territory": "Sydney & Melbourne, Australia",
        "principal": "Lachlan Murdoch-Shaw, Principal Consultant",
        "current_clients": 38,
        "primary_focus": "Mining Tech, Commercial Construction & Renewable Energy",
        "slug": "pacifica_digital_ventures"
    },
    {
        "id": 3,
        "name": "SingaTech AI Consulting",
        "territory": "Singapore & ASEAN Regional Hub",
        "principal": "Gerald Tan, Head of Enterprise Transformation",
        "current_clients": 50,
        "primary_focus": "FinTech, Maritime Logistics & Luxury Hospitality",
        "slug": "singatech_ai_consulting"
    },
    {
        "id": 4,
        "name": "MapleCore Digital Systems",
        "territory": "Toronto & Vancouver, Canada",
        "principal": "Evelyn Tremblay, Practice Director",
        "current_clients": 35,
        "primary_focus": "CleanTech, Biopharma & Cross-Border E-Commerce",
        "slug": "maplecore_digital_systems"
    },
    {
        "id": 5,
        "name": "Oasis AI Advisory Group",
        "territory": "Dubai & Abu Dhabi, UAE (GCC)",
        "principal": "Tariq Al-Mansoor, Executive Director",
        "current_clients": 48,
        "primary_focus": "Family Offices, Ultra-Luxury Real Estate & Sovereign Wealth",
        "slug": "oasis_ai_advisory_group"
    },
    {
        "id": 6,
        "name": "Helvetia Private Automation",
        "territory": "Zurich & Geneva, Switzerland",
        "principal": "Marcelle von Bergen, Senior Partner",
        "current_clients": 31,
        "primary_focus": "Private Banking, MedTech & Precision Manufacturing",
        "slug": "helvetia_private_automation"
    },
    {
        "id": 7,
        "name": "Rhine-Main AI Enterprise Solutions",
        "territory": "Frankfurt & Munich, Germany (DACH)",
        "principal": "Dr. Florian Becker, Managing Director",
        "current_clients": 44,
        "primary_focus": "Mittelstand Engineering, Automotive Tech & Industrial Supply",
        "slug": "rhine-main_ai_enterprise_solutions"
    },
    {
        "id": 8,
        "name": "Nippon Autonomous AI Systems",
        "territory": "Tokyo & Osaka, Japan",
        "principal": "Kenji Takahashi, Chief AI Strategist",
        "current_clients": 39,
        "primary_focus": "Robotics Integration, Consumer Electronics & Global Trading",
        "slug": "nippon_autonomous_ai_systems"
    },
    {
        "id": 9,
        "name": "Hudson Capital Automation",
        "territory": "New York Metro & Tri-State Area, USA",
        "principal": "Harrison Brooks, Managing Director",
        "current_clients": 55,
        "primary_focus": "Hedge Funds, Commercial Lending & Institutional Advisory",
        "slug": "hudson_capital_automation"
    },
    {
        "id": 10,
        "name": "BayArea Autonomous Ops",
        "territory": "San Francisco & Silicon Valley, USA",
        "principal": "Priya Nair, Founding Partner",
        "current_clients": 46,
        "primary_focus": "Series B/C SaaS Scaleups, AI Hardware & DeepTech Ventures",
        "slug": "bayarea_autonomous_ops"
    },
    {
        "id": 11,
        "name": "LoneStar Enterprise AI",
        "territory": "Dallas, Austin & Houston, Texas, USA",
        "principal": "Colt Remington, Senior Partner",
        "current_clients": 41,
        "primary_focus": "Energy Infrastructure, Defense Logistics & Enterprise Medical",
        "slug": "lonestar_enterprise_ai"
    },
    {
        "id": 12,
        "name": "SunCoast AI Agency Partners",
        "territory": "Miami & Latin America Cross-Border, USA",
        "principal": "Sofia Valenzuela, Managing Partner",
        "current_clients": 37,
        "primary_focus": "Real Estate Syndicates, Import/Export & Aviation Services",
        "slug": "suncoast_ai_agency_partners"
    }
]

PROSPECTUS_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Syndicate Franchise Prospectus — {partner_name}</title>
  <meta name="description" content="Exclusive Regional AI Agency Franchise License Prospectus for {partner_name} ({territory}). Turnkey Private Cloud AI Infrastructure.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #060612;
      --card-bg: rgba(15, 15, 32, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --border-gold: rgba(255, 215, 0, 0.45);
      --gold: #ffd700;
      --emerald: #10b981;
      --cyan: #00f2fe;
      --accent: #7c5cfc;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      background-image: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(255, 215, 0, 0.12), transparent 70%),
        radial-gradient(circle at 10% 90%, rgba(16, 185, 129, 0.08), transparent 50%),
        radial-gradient(circle at 90% 80%, rgba(124, 92, 252, 0.08), transparent 50%);
      min-height: 100vh;
      padding: 40px 20px 80px;
    }}
    .container {{
      max-width: 1000px;
      margin: 0 auto;
    }}
    .header {{
      text-align: center;
      margin-bottom: 40px;
      padding-bottom: 28px;
      border-bottom: 1px solid var(--border);
    }}
    .badge {{
      display: inline-block;
      background: rgba(255, 215, 0, 0.12);
      border: 1px solid var(--border-gold);
      color: var(--gold);
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 16px;
    }}
    h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 38px;
      font-weight: 900;
      color: #fff;
      margin-bottom: 10px;
      line-height: 1.2;
    }}
    h1 span {{
      background: linear-gradient(135deg, #ffd700 0%, #10b981 50%, #00f2fe 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .subtitle {{
      font-size: 17px;
      color: var(--text-muted);
      max-width: 760px;
      margin: 0 auto;
    }}
    .meta-box {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 36px;
    }}
    .meta-item .label {{
      font-size: 11px;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 1px;
      margin-bottom: 4px;
    }}
    .meta-item .value {{
      font-size: 16px;
      font-weight: 700;
      color: #fff;
    }}
    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .spec-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
      margin-bottom: 36px;
    }}
    .spec-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      position: relative;
      transition: all 0.2s;
    }}
    .spec-card:hover {{
      border-color: rgba(255, 215, 0, 0.4);
      transform: translateY(-2px);
    }}
    .spec-card h3 {{
      font-size: 18px;
      color: #ffd700;
      margin-bottom: 8px;
    }}
    .spec-card p {{
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 12px;
    }}
    .spec-card ul {{
      list-style: none;
      padding: 0;
      font-size: 13px;
    }}
    .spec-card ul li {{
      padding: 4px 0;
      color: #cbd5e1;
    }}
    .spec-card ul li::before {{
      content: "✓ ";
      color: #10b981;
      font-weight: 700;
    }}
    .pricing-box {{
      background: linear-gradient(135deg, rgba(255, 215, 0, 0.08) 0%, rgba(16, 185, 129, 0.08) 100%);
      border: 2px solid var(--border-gold);
      border-radius: 18px;
      padding: 32px;
      text-align: center;
      margin-bottom: 40px;
    }}
    .pricing-headline {{
      font-family: 'Outfit', sans-serif;
      font-size: 28px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 8px;
    }}
    .price-tag {{
      font-size: 44px;
      font-weight: 900;
      color: #ffd700;
      margin: 16px 0 6px;
    }}
    .price-sub {{
      font-size: 14px;
      color: #94a3b8;
      margin-bottom: 24px;
    }}
    .cta-btn {{
      display: inline-block;
      background: linear-gradient(135deg, #ffd700 0%, #f59e0b 100%);
      color: #060612;
      font-family: 'Outfit', sans-serif;
      font-size: 16px;
      font-weight: 800;
      text-decoration: none;
      padding: 14px 36px;
      border-radius: 10px;
      transition: all 0.2s;
      box-shadow: 0 4px 20px rgba(255, 215, 0, 0.3);
    }}
    .cta-btn:hover {{
      transform: scale(1.04);
      box-shadow: 0 6px 28px rgba(255, 215, 0, 0.45);
    }}
    .footer {{
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      border-top: 1px solid var(--border);
      padding-top: 24px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="badge">🌐 PHASE 4 SYNDICATE FRANCHISE LICENSE</div>
      <h1>Regional AI Agency License: <span>{partner_name}</span></h1>
      <p class="subtitle">Confidential Turnkey Infrastructure & Territory Deployment Prospectus for <strong>{territory}</strong>.</p>
    </div>

    <div class="meta-box">
      <div class="meta-item">
        <div class="label">Partner Organization</div>
        <div class="value">{partner_name}</div>
      </div>
      <div class="meta-item">
        <div class="label">Designated Territory</div>
        <div class="value">{territory}</div>
      </div>
      <div class="meta-item">
        <div class="label">Principal Lead</div>
        <div class="value">{principal}</div>
      </div>
      <div class="meta-item">
        <div class="label">Target Client Base</div>
        <div class="value">{current_clients} Active Accounts</div>
      </div>
    </div>

    <h2 class="section-title">⚡ 4 Core Turnkey Infrastructure Deliverables Included</h2>
    <div class="spec-grid">
      <div class="spec-card">
        <h3>1. 60 White-Label Client Sandboxes</h3>
        <p>Full proprietary source code to deploy 60 customized client demo sandboxes under your agency brand.</p>
        <ul>
          <li>Interactive booking simulators</li>
          <li>Live lead intake scoring</li>
          <li>Sub-250ms localized latency</li>
          <li>Instant client acceptance tests</li>
        </ul>
      </div>

      <div class="spec-card">
        <h3>2. Omnichannel Voice AI Engine</h3>
        <p>License our sub-350ms telephone intake and emergency dispatch engine for your regional clients.</p>
        <ul>
          <li>Twilio & WebRTC SIP trunking ready</li>
          <li>Multi-lingual accent tuning</li>
          <li>HIPAA & GDPR privacy compliance</li>
          <li>Automated SMS confirmation loops</li>
        </ul>
      </div>

      <div class="spec-card">
        <h3>3. Autonomous Client ROI Reporter</h3>
        <p>Eliminate churn with automated monthly reports that mathematically prove client ROI.</p>
        <ul>
          <li>Quantifies recovered revenue</li>
          <li>Staff labor hours liberated</li>
          <li>Executive PDF export engine</li>
          <li>Zero-maintenance automation</li>
        </ul>
      </div>

      <div class="spec-card">
        <h3>4. Dedicated VPC Model Swarm</h3>
        <p>Private dedicated LLM fine-tuning cluster calibrated specifically for your territory's primary niche.</p>
        <ul>
          <li>Fine-tuned on {primary_focus}</li>
          <li>0% data leakage guarantee</li>
          <li>Weekly continuous retraining</li>
          <li>99.99% Enterprise uptime SLA</li>
        </ul>
      </div>
    </div>

    <div class="pricing-box">
      <div class="pricing-headline">Territory Franchise Terms & Financial Architecture</div>
      <p style="color:#cbd5e1; max-width:600px; margin:0 auto;">Exclusive rights to deploy and resell the AI Money Machine tech stack across {territory} with zero revenue share clawbacks.</p>
      
      <div class="price-tag">$4,950 <span style="font-size:20px; color:#cbd5e1; font-weight:400;">Setup + $1,250 / mo</span></div>
      <div class="price-sub">Covers full white-label cloud deployment, private LLM routing proxy, and weekly swarm retraining.</div>

      <a href="https://work-minh-lap.vercel.app/onboarding?partner={partner_slug}&type=syndicate" class="cta-btn">
        🚀 Lock Territory & Activate Syndicate License
      </a>
      
      <div style="margin-top:16px; font-size:12px; color:#94a3b8;">
        Protected territory exclusivity guaranteed for 12 months with active retainer.
      </div>
    </div>

    <div class="footer">
      <p>AI Money Machine Autonomous Syndicate • Confidential Territory License Prospectus</p>
      <p style="margin-top:4px;">Verified by Principal AI Architect • All Rights Reserved © 2026</p>
    </div>
  </div>
</body>
</html>
"""

def init_syndicate_pipeline():
    if PIPELINE_FILE.exists():
        try:
            return json.loads(PIPELINE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    # Initialize from default
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    pipeline = []
    for p in SYNDICATE_PARTNERS:
        pipeline.append({
            "id": p["id"],
            "name": p["name"],
            "territory": p["territory"],
            "principal": p["principal"],
            "current_clients": p["current_clients"],
            "primary_focus": p["primary_focus"],
            "slug": p["slug"],
            "syndicate_setup": 4950,
            "syndicate_retainer": 1250,
            "status": "identified",
            "updated_at": now
        })
    PIPELINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    PIPELINE_FILE.write_text(json.dumps(pipeline, indent=2, ensure_ascii=False), encoding="utf-8")
    return pipeline

def generate_syndicate_proposals():
    SYNDICATE_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in SYNDICATE_PARTNERS:
        html = PROSPECTUS_HTML_TEMPLATE.format(
            partner_name=p["name"],
            territory=p["territory"],
            principal=p["principal"],
            current_clients=p["current_clients"],
            primary_focus=p["primary_focus"],
            partner_slug=p["slug"]
        )
        out_file = SYNDICATE_DIR / f"{p['slug']}_syndicate_prospectus.html"
        out_file.write_text(html, encoding="utf-8")
        count += 1
    print(f"[✓] Generated all {count} AI Syndicate Franchise Territory Prospectuses in syndicate_proposals/")

def print_syndicate_summary():
    pipeline = init_syndicate_pipeline()
    won_c = sum(1 for p in pipeline if p.get("status") == "syndicate_won")
    booked_c = sum(1 for p in pipeline if p.get("status") == "interview_booked")
    sent_c = sum(1 for p in pipeline if p.get("status") == "briefing_sent")
    staged_c = sum(1 for p in pipeline if p.get("status") == "identified")

    current_cash = won_c * 4950
    current_mrr = won_c * 1250
    total_won_deals = 83 + won_c
    total_cash = 201200 + current_cash
    total_mrr = 68550 + current_mrr
    total_arr = total_mrr * 12

    print("=" * 80)
    print("🌐 AI SYNDICATE FRANCHISE TIER (PHASE 4 EXPANSION) — EXECUTIVE SUMMARY")
    print("=" * 80)
    print(f"  • Global Territory Licenses:   12 Exclusive Regional Agencies")
    print(f"  • 🎯 Syndicate Briefing Sent:   {sent_c}")
    print(f"  • 📞 Partner Interviews Booked: {booked_c}")
    print(f"  • 🏆 Syndicate Partners Won:    {won_c}")
    print(f"  • ⏳ Identified / Staged:       {staged_c}")
    print("-" * 80)
    print(f"  💰 Current Syndicate Cash:     +${current_cash:,} Upfront Cash")
    print(f"  🔄 Current Syndicate MRR:      +${current_mrr:,} / month MRR")
    print(f"  🚀 Max Syndicate Cash Target:  +$59,400 Upfront Cash (${total_cash:,} Total Empire)")
    print(f"  🌟 Max Syndicate MRR Target:   +$15,000 / mo MRR (${total_mrr:,}/mo Total Empire)")
    print(f"  💎 Max Syndicate ARR Target:   +$180,000 / yr ARR (${total_arr:,}/yr Total Empire)")
    print("=" * 80)

def send_telegram_syndicate_alert(partner_id, name, territory, old_st, new_st, setup, retainer):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    icons = {
        "briefing_sent": "🎯",
        "interview_booked": "📞",
        "syndicate_won": "🏆💎"
    }
    icon = icons.get(new_st, "🌐")

    msg = f"""{icon} <b>[AI SYNDICATE FRANCHISE PARTNER ALERT — #{partner_id}]</b>

🏢 <b>Regional Licensee:</b> <code>{name}</code>
🌍 <b>Designated Territory:</b> <code>{territory}</code>
🔄 <b>Status Update:</b> <code>{old_st.upper()}</code> ➔ <b>{new_st.upper()}</b>
💵 <b>Upfront Setup:</b> <code>+${setup:,} Cash</code>
📈 <b>Monthly Retainer:</b> <code>+${retainer:,} / mo MRR</code>

🚀 <b>Phase 4 AI Syndicate Expansion Active!</b>"""

    try:
        payload = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json; charset=utf-8"},
            data=payload
        )
        for attempt in range(1, 4):
            try:
                with urllib.request.urlopen(req, timeout=12) as r:
                    if r.status == 200:
                        print(f"  [✓] Dispatched Syndicate Alert to Telegram (@Minhpv_bot)!")
                        break
            except Exception as e:
                if attempt == 3:
                    print(f"  [!] Telegram alert error: {e}")
                else:
                    time.sleep(1.0)
    except Exception as e:
        print(f"  [!] Telegram error: {e}")

def update_syndicate_lead(partner_id, new_status, notify_tg=False):
    pipeline = init_syndicate_pipeline()
    found = False
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    target = None
    old_st = ""

    for p in pipeline:
        if p["id"] == partner_id:
            old_st = p.get("status", "identified")
            p["status"] = new_status
            p["updated_at"] = now
            found = True
            target = p
            print(f"[✓] Syndicate #{partner_id} ({p['name']}): status updated from '{old_st}' -> '{new_status}'")
            break

    if found:
        PIPELINE_FILE.write_text(json.dumps(pipeline, indent=2, ensure_ascii=False), encoding="utf-8")
        if notify_tg and target:
            send_telegram_syndicate_alert(partner_id, target["name"], target["territory"], old_st, new_status, target["syndicate_setup"], target["syndicate_retainer"])
    else:
        print(f"[!] Syndicate #{partner_id} not found in Pipeline.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage AI Syndicate Franchise Pipeline (Phase 4)")
    parser.add_argument("--summary", action="store_true", help="Print executive summary")
    parser.add_argument("--generate-all", action="store_true", help="Generate all 12 HTML Syndicate prospectuses")
    parser.add_argument("--id", type=int, help="Partner ID to update")
    parser.add_argument("--status", choices=["identified", "briefing_sent", "interview_booked", "syndicate_won"], help="New status")
    parser.add_argument("--telegram", action="store_true", help="Send alert to Telegram")

    args = parser.parse_args()

    if args.generate_all:
        generate_syndicate_proposals()
    elif args.id and args.status:
        update_syndicate_lead(args.id, args.status, notify_tg=args.telegram)
    else:
        print_syndicate_summary()
