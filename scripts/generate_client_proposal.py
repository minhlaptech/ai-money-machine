"""
Executive AI Proposal & Audit Generator
-----------------------------------------
Tự động tạo bản Đề Xuất & Báo Cáo Kiểm Toán Tự Động Hóa (AI Audit & Proposal)
chuyên nghiệp, sang trọng dưới định dạng HTML (chuẩn in ấn/xuất PDF) dành riêng cho từng khách hàng.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PROPOSAL_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Operations Audit & Proposal: {client_name}</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    :root {{
      --primary: #7c5cfc;
      --secondary: #00f2fe;
      --dark: #070714;
      --card-bg: rgba(255,255,255,0.03);
      --border: rgba(255,255,255,0.1);
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      font-family: 'Inter', -apple-system, sans-serif;
      background: var(--dark);
      color: var(--text);
      line-height: 1.6;
      padding: 40px 20px;
    }}
    .container {{
      max-width: 860px;
      margin: 0 auto;
      background: #0d0d21;
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 48px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}
    .badge {{
      display: inline-block;
      background: rgba(124,92,252,0.15);
      border: 1px solid rgba(124,92,252,0.4);
      color: #b794f4;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 20px;
    }}
    h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 32px;
      line-height: 1.2;
      margin-bottom: 8px;
      background: linear-gradient(135deg, #fff 0%, #00f2fe 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}
    .meta-sub {{
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 32px;
    }}
    .divider {{
      height: 1px;
      background: var(--border);
      margin: 28px 0;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 28px;
    }}
    .stat-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
    }}
    .stat-label {{
      font-size: 12px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}
    .stat-val {{
      font-size: 24px;
      font-weight: 800;
      color: #00f2fe;
      font-family: 'JetBrains Mono', monospace;
    }}
    h2 {{
      font-size: 20px;
      margin: 24px 0 12px;
      color: #fff;
    }}
    p {{
      margin-bottom: 16px;
      font-size: 15px;
      color: #cbd5e1;
    }}
    ul {{
      margin-left: 20px;
      margin-bottom: 20px;
    }}
    li {{
      margin-bottom: 8px;
      font-size: 14px;
    }}
    .roi-box {{
      background: linear-gradient(135deg, rgba(124,92,252,0.1), rgba(0,242,254,0.05));
      border: 1px solid rgba(124,92,252,0.3);
      border-radius: 14px;
      padding: 24px;
      margin: 24px 0;
    }}
    .table {{
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 14px;
    }}
    .table th, .table td {{
      padding: 12px;
      border-bottom: 1px solid var(--border);
      text-align: left;
    }}
    .table th {{
      color: var(--text-muted);
      font-size: 11px;
      text-transform: uppercase;
    }}
    .cta-btn {{
      display: inline-block;
      background: linear-gradient(135deg, #7c5cfc, #00f2fe);
      color: #000;
      font-weight: 700;
      font-size: 15px;
      padding: 14px 32px;
      border-radius: 10px;
      text-decoration: none;
      margin-top: 16px;
    }}
    @media print {{
      body {{ background: #fff; color: #111; padding: 0; }}
      .container {{ border: none; box-shadow: none; padding: 0; background: #fff; }}
      h1 {{ -webkit-text-fill-color: #111; }}
      .stat-card, .roi-box {{ border: 1px solid #ddd; background: #fafafa; }}
      .stat-val {{ color: #7c5cfc; }}
      .cta-btn {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="badge">CONFIDENTIAL AUDIT & IMPLEMENTATION PROPOSAL</div>
    <h1>AI Automated Operations & Client Acquisition</h1>
    <div class="meta-sub">Prepared exclusively for: <strong>{client_name}</strong> ({city}) • Date: {date}</div>

    <div class="grid-2">
      <div class="stat-card">
        <div class="stat-label">Estimated Monthly Lost Inquiries</div>
        <div class="stat-val">{lost_inquiries} Leads / Mo</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Projected Annual Recovered Revenue</div>
        <div class="stat-val">${annual_roi}</div>
      </div>
    </div>

    <h2>1. Executive Summary & Observed Bottlenecks</h2>
    <p>
      An audit of <strong>{client_name}</strong>'s current client intake funnel indicates that high-intent prospects browsing outside standard business hours (between 6:00 PM and 8:30 AM, plus weekends) encounter friction in receiving immediate validation, quotes, or calendar confirmation.
    </p>
    <p>
      <strong>Key Bottlenecks Detected:</strong>
    </p>
    <ul>
      <li><strong>Delayed Response Window:</strong> Average prospect response latency exceeds 4.5 hours outside business hours. 78% of service inquiries choose the provider who answers within 5 minutes.</li>
      <li><strong>Manual Intake Churn:</strong> Staff spends an estimated 12–18 hours/week chasing phone calls, answering repetitive qualifying questions, and manually entering calendar bookings.</li>
      <li><strong>AI Search Visibility Gap:</strong> AI engines (ChatGPT Search, Perplexity) lack structured schema markers to directly recommend {client_name}'s services.</li>
    </ul>

    <div class="divider"></div>

    <h2>2. Recommended Solution: Autonomous Intake Copilot</h2>
    <p>
      We propose deploying a bespoke, lightweight AI Receptionist & Booking Copilot integrated directly into your existing domain and Google/Outlook calendar:
    </p>
    <ul>
      <li><strong>24/7 Real-Time Conversation:</strong> Welcomes visitors, answers pricing & insurance/service questions accurately, and handles triage.</li>
      <li><strong>Instant Calendar Integration:</strong> Verifies real-time practitioner availability and locks in booked appointments with zero human back-and-forth.</li>
      <li><strong>Automated SMS/Email Recovery Loop:</strong> Instantly sends a friendly confirmation and automated reminder 24 hours prior to eliminate no-shows.</li>
    </ul>

    <div class="roi-box">
      <h3 style="color:#00f2fe; margin-bottom:8px; font-size:16px;">📈 Projected Financial Return (ROI Analysis)</h3>
      <p style="font-size:14px; margin-bottom:12px;">Based on conservative recovery rates for {niche}:</p>
      <table class="table" style="margin:0;">
        <tr>
          <td>Conservative Recovered Appointments:</td>
          <td style="font-weight:700; color:#fff;">{recovered_per_month} bookings / month</td>
        </tr>
        <tr>
          <td>Average Value per Retained Client:</td>
          <td style="font-weight:700; color:#fff;">${avg_client_val}</td>
        </tr>
        <tr>
          <td><strong>Estimated Monthly Incremental Revenue:</strong></td>
          <td style="font-weight:700; color:#00f2fe; font-size:16px;">${monthly_recovered} / month</td>
        </tr>
      </table>
    </div>

    <div class="divider"></div>

    <h2>3. Implementation Scope & Deliverables</h2>
    <table class="table">
      <thead>
        <tr>
          <th>Phase</th>
          <th>Milestone Deliverable</th>
          <th>Timeline</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Phase 1: Knowledge Setup</strong></td>
          <td>Ingest services, FAQ, pricing rules, and practitioner constraints into AI Core</td>
          <td>Days 1 – 3</td>
        </tr>
        <tr>
          <td><strong>Phase 2: Live Integration</strong></td>
          <td>Embed non-intrusive widget on website + connect calendar & CRM webhook</td>
          <td>Days 4 – 6</td>
        </tr>
        <tr>
          <td><strong>Phase 3: Testing & Go-Live</strong></td>
          <td>Full end-to-end sandbox testing, staff training walkthrough & public deployment</td>
          <td>Day 7</td>
        </tr>
      </tbody>
    </table>

    <div class="divider"></div>

    <h2>4. Investment & Guarantee</h2>
    <p>
      <strong>One-Time Implementation & Architecture:</strong> ${setup_fee}<br>
      <strong>Monthly System Maintenance & Retainer:</strong> ${monthly_retainer}/month (includes hosting, prompt optimization, and monthly performance reports).
    </p>
    <p style="font-size:13px; color:var(--text-muted);">
      <em>30-Day Performance Assurance: If the copilot does not capture at least 3 qualified client appointments in the first 30 days, we will continue tuning your system for free until it does.</em>
    </p>

    <div style="text-align:center; margin-top:36px;">
      <a href="https://chatbotdemo-hazel.vercel.app" class="cta-btn" target="_blank">👉 Experience Live Demo Here</a>
      <p style="margin-top:14px; font-size:13px; color:var(--text-muted);">
        Or reply directly to schedule your 10-minute implementation briefing.
      </p>
    </div>
  </div>
</body>
</html>
"""

def generate_proposal(client_name, niche, city, avg_val=600, lost_leads=12):
    slug = client_name.lower().replace(" ", "_").replace("&", "and")
    out_dir = Path(__file__).resolve().parent.parent / "proposals"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{slug}_proposal.html"

    recovered = max(3, lost_leads // 3)
    monthly_rev = recovered * avg_val
    annual_rev = monthly_rev * 12

    html = PROPOSAL_TEMPLATE.format(
        client_name=client_name,
        niche=niche,
        city=city,
        date=datetime.now().strftime("%B %d, %Y"),
        lost_inquiries=lost_leads,
        recovered_per_month=recovered,
        avg_client_val=f"{avg_val:,}",
        monthly_recovered=f"{monthly_rev:,}",
        annual_roi=f"{annual_rev:,}",
        setup_fee="1,200",
        monthly_retainer="650"
    )

    out_file.write_text(html, encoding="utf-8")
    print(f"[✓] Created custom proposal: {out_file}")
    return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Custom Client AI Audit & Proposal")
    parser.add_argument("--name", default="Austin Dental Co", help="Client / Business Name")
    parser.add_argument("--niche", default="Cosmetic Dentistry", help="Industry / Niche")
    parser.add_argument("--city", default="Austin, TX", help="City / Region")
    parser.add_argument("--val", type=int, default=750, help="Average Client Lifetime Value ($)")
    parser.add_argument("--lost", type=int, default=14, help="Estimated Monthly Lost Leads")

    args = parser.parse_args()
    generate_proposal(args.name, args.niche, args.city, args.val, args.lost)
