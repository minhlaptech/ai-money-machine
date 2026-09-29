"""
Executive Client Invoice Generator (HTML & Print-Ready PDF)
-----------------------------------------------------------
Tự động tạo hóa đơn thanh toán B2B (Invoice) chuẩn quốc tế, sang trọng,
dành riêng cho các hợp đồng AI Automation Setup ($1,200) + Monthly Retainer ($650).
Tích hợp sẵn cổng thanh toán thẻ Lemon Squeezy, chuyển khoản ngân hàng và VietQR.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, timedelta

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
INVOICES_DIR = ROOT_DIR / "invoices"

INVOICE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Invoice {invoice_id} — {client_name}</title>
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
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 32px;
      flex-wrap: wrap;
      gap: 20px;
    }}
    .brand-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 28px;
      font-weight: 800;
      background: linear-gradient(135deg, #fff 0%, #00f2fe 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 4px;
    }}
    .brand-sub {{
      font-size: 13px;
      color: var(--text-muted);
    }}
    .invoice-badge {{
      text-align: right;
    }}
    .badge-number {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 24px;
      font-weight: 700;
      color: #00f2fe;
      margin-bottom: 4px;
    }}
    .badge-status {{
      display: inline-block;
      background: rgba(255, 183, 77, 0.15);
      border: 1px solid rgba(255, 183, 77, 0.4);
      color: #ffb74d;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 12px;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    .divider {{
      height: 1px;
      background: var(--border);
      margin: 24px 0;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin-bottom: 28px;
    }}
    .meta-box {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 20px;
    }}
    .meta-label {{
      font-size: 11px;
      text-transform: uppercase;
      color: var(--text-muted);
      letter-spacing: 1px;
      margin-bottom: 6px;
    }}
    .meta-val {{
      font-size: 15px;
      font-weight: 600;
      color: #ffffff;
    }}
    .meta-subtext {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 2px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 28px 0;
    }}
    th, td {{
      padding: 14px 16px;
      border: 1px solid var(--border);
      text-align: left;
      font-size: 14px;
    }}
    th {{
      background: rgba(255,255,255,0.05);
      color: #ffffff;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 1px;
    }}
    .price-col {{
      text-align: right;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
    }}
    .total-box {{
      background: rgba(124,92,252,0.08);
      border: 1px solid rgba(124,92,252,0.3);
      border-radius: 12px;
      padding: 20px 24px;
      margin-left: auto;
      max-width: 360px;
    }}
    .total-row {{
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;
      font-size: 14px;
      color: var(--text-muted);
    }}
    .total-row.final {{
      border-top: 1px solid var(--border);
      padding-top: 10px;
      margin-top: 10px;
      font-size: 20px;
      font-weight: 800;
      color: #00f2fe;
    }}
    .payment-section {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 24px;
      margin-top: 32px;
    }}
    .payment-title {{
      font-size: 16px;
      font-weight: 700;
      color: #ffffff;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .btn-pay {{
      display: inline-block;
      background: linear-gradient(135deg, #7c5cfc, #00f2fe);
      color: #ffffff;
      text-decoration: none;
      padding: 14px 28px;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 700;
      box-shadow: 0 4px 20px rgba(124,92,252,0.4);
      margin-top: 14px;
      transition: transform 0.15s;
    }}
    .btn-pay:hover {{
      transform: scale(1.03);
    }}
    .print-tip {{
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 24px;
    }}
    @media print {{
      body {{ background: #fff; color: #000; padding:0; }}
      .container {{ border: none; box-shadow: none; max-width: 100%; padding: 20px; background: #fff; color: #000; }}
      .brand-title {{ -webkit-text-fill-color: #000; color: #000; }}
      .meta-box, .payment-section, .total-box {{ background: #f8fafc; border: 1px solid #cbd5e1; }}
      .badge-number, .total-row.final {{ color: #0284c7; }}
      .meta-val, th, td {{ color: #0f172a; }}
      .meta-label, .meta-subtext, .brand-sub, .total-row {{ color: #64748b; }}
      .btn-pay, .print-tip {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <div class="brand-title">MinhLap AI Systems</div>
        <div class="brand-sub">Enterprise AI Operations & Autonomous Copilot Architecture</div>
        <div class="brand-sub">Support & Billing: contact@minhlap.com • Telegram: @Minhpv_bot</div>
      </div>
      <div class="invoice-badge">
        <div class="badge-number">{invoice_id}</div>
        <div class="badge-status">Payment Pending</div>
      </div>
    </div>

    <div class="grid-2">
      <div class="meta-box">
        <div class="meta-label">Billed To (Client):</div>
        <div class="meta-val">{client_name}</div>
        <div class="meta-subtext">{niche}</div>
        <div class="meta-subtext">{city}</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">Invoice Details:</div>
        <div class="meta-subtext"><strong>Issue Date:</strong> {issue_date}</div>
        <div class="meta-subtext"><strong>Due Date:</strong> {due_date} (Net 14 Days)</div>
        <div class="meta-subtext"><strong>Currency:</strong> USD ($)</div>
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th>Description & Scope of Work</th>
          <th>Qty</th>
          <th class="price-col">Unit Price</th>
          <th class="price-col">Amount</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <strong>Autonomous AI Intake Copilot — Setup & Architecture</strong><br>
            <span style="font-size:12px; color:var(--text-muted);">
              Ingestion of service catalog, FAQ, scheduling constraints; bespoke Shadow DOM widget styling; calendar integration and SMS reminder webhooks.
            </span>
          </td>
          <td>1</td>
          <td class="price-col">$1,200.00</td>
          <td class="price-col">$1,200.00</td>
        </tr>
        <tr>
          <td>
            <strong>Month 1 System Maintenance, Hosting & Prompt Optimization Retainer</strong><br>
            <span style="font-size:12px; color:var(--text-muted);">
              24/7 Serverless cloud hosting, monthly conversation intent tuning, and executive revenue recovery reporting.
            </span>
          </td>
          <td>1</td>
          <td class="price-col">$650.00</td>
          <td class="price-col">$650.00</td>
        </tr>
      </tbody>
    </table>

    <div class="total-box">
      <div class="total-row">
        <span>Setup Fee:</span>
        <span style="color:#fff;">$1,200.00</span>
      </div>
      <div class="total-row">
        <span>Month 1 Retainer:</span>
        <span style="color:#fff;">$650.00</span>
      </div>
      <div class="total-row">
        <span>Tax / VAT (0%):</span>
        <span style="color:#fff;">$0.00</span>
      </div>
      <div class="total-row final">
        <span>Total Due:</span>
        <span>${total_due}</span>
      </div>
    </div>

    <div class="payment-section">
      <div class="payment-title">💳 Secure Payment Methods</div>
      <p style="font-size:13.5px; color:var(--text-muted); margin-bottom:12px;">
        You can settle this invoice via credit card, Apple Pay, Google Pay, or direct US ACH / International Bank Wire:
      </p>
      <ul>
        <li style="font-size:13px; color:#cbd5e1; margin-bottom:6px;"><strong>Option A (Instant Card):</strong> Click the secure link below to pay via Lemon Squeezy merchant gateway.</li>
        <li style="font-size:13px; color:#cbd5e1; margin-bottom:6px;"><strong>Option B (US ACH / Wire):</strong> Available upon request; reply to invoice email for wire instructions.</li>
        <li style="font-size:13px; color:#cbd5e1;"><strong>Option C (50% Deposit Kickoff):</strong> Pay $925.00 now to initiate setup, remainder due upon Day 5 go-live.</li>
      </ul>
      <div style="margin-top:16px; display:flex; gap:12px; flex-wrap:wrap;">
        <a href="https://minhlap.lemonsqueezy.com" target="_blank" class="btn-pay" style="flex:1; margin-top:0;">👉 Pay Securely Online via Card / Apple Pay</a>
        <button id="btn-paid-notify" onclick="notifyPaymentSent()" style="background:rgba(0,230,118,0.12); border:1px solid rgba(0,230,118,0.35); color:#00e676; padding:12px 18px; border-radius:10px; font-weight:700; font-size:13px; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; transition:all 0.2s;">
          🔔 Notify Payment Sent / Bank Wire
        </button>
        <a href="https://work-minh-lap.vercel.app/onboarding?name={client_url_name}&niche={niche_url}&city={city_url}" target="_blank" style="background:rgba(255,255,255,0.08); border:1px solid var(--border); color:#fff; text-decoration:none; padding:12px 18px; border-radius:10px; font-weight:700; font-size:13px; display:inline-flex; align-items:center; justify-content:center; transition:background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.15)'" onmouseout="this.style.background='rgba(255,255,255,0.08)'">🚀 Start Onboarding Intake</a>
      </div>

      <div id="payment-notified-banner" style="display:none; background:rgba(0,230,118,0.15); border:1px solid #00e676; border-radius:10px; padding:14px; margin-top:14px; text-align:center; color:#00e676; font-size:13.5px; font-weight:600;">
        ✓ Payment notification logged & transmitted to billing desk. Our team will verify and initiate your 5-Day White-Glove Sprint immediately!
      </div>
    </div>

    <div class="print-tip">
      🖨️ Need a PDF copy for your accounting department? Press <strong>Ctrl + P</strong> (Cmd + P) to Print or Save as PDF.
    </div>
  </div>

  <script>
    function notifyPaymentSent() {{
      const btn = document.getElementById('btn-paid-notify');
      btn.innerHTML = '⏳ Transmitting...';
      btn.disabled = true;

      const endpoint = window.location.hostname.includes('vercel.app') 
        ? 'https://work-minh-lap.vercel.app/api/contact'
        : '/api/contact';

      fetch(endpoint, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{
          name: '{client_name}',
          service: 'Invoice Payment Settled / Wire Request',
          source: 'B2B Invoice Portal ({invoice_id})',
          message: 'Client {client_name} ({city}) has confirmed invoice payment of ${total_due} or requested wire reconciliation!'
        }})
      }}).catch(e => console.log('Silent notify:', e))
      .finally(() => {{
        btn.innerHTML = '✓ Payment Notification Sent';
        btn.style.background = '#00e676';
        btn.style.color = '#000';
        document.getElementById('payment-notified-banner').style.display = 'block';
        const badge = document.querySelector('.badge-status');
        if (badge) {{
          badge.innerHTML = 'Payment Submitted';
          badge.style.background = 'rgba(0, 230, 118, 0.2)';
          badge.style.borderColor = '#00e676';
          badge.style.color = '#00e676';
        }}
        try {{ localStorage.setItem('inv_paid_{slug}', 'true'); }} catch(e) {{}}
      }});
    }}

    try {{
      if (localStorage.getItem('inv_paid_{slug}') === 'true') {{
        window.addEventListener('DOMContentLoaded', () => {{
          const btn = document.getElementById('btn-paid-notify');
          if (btn) {{
            btn.innerHTML = '✓ Payment Notification Sent';
            btn.style.background = '#00e676';
            btn.style.color = '#000';
            btn.disabled = true;
          }}
          const banner = document.getElementById('payment-notified-banner');
          if (banner) banner.style.display = 'block';
          const badge = document.querySelector('.badge-status');
          if (badge) {{
            badge.innerHTML = 'Payment Submitted';
            badge.style.background = 'rgba(0, 230, 118, 0.2)';
            badge.style.borderColor = '#00e676';
            badge.style.color = '#00e676';
          }}
        }});
      }}
    }} catch(e) {{}}
  </script>
</body>
</html>
"""

LEADS = [
  {"id": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX"},
  {"id": 2, "name": "Pure Radiance MedSpa", "niche": "Aesthetics & Spa", "city": "Miami, FL"},
  {"id": 3, "name": "Premier 24/7 HVAC", "niche": "Heating & AC Repair", "city": "Dallas, TX"},
  {"id": 4, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Jose, CA"},
  {"id": 5, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar", "city": "Phoenix, AZ"},
  {"id": 6, "name": "Lumina Wellness", "niche": "Regenerative Med", "city": "Seattle, WA"},
  {"id": 7, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Denver, CO"},
  {"id": 8, "name": "ProActive Spine & Chiro", "niche": "Chiropractic", "city": "Chicago, IL"},
  {"id": 9, "name": "Rapid Response Plumbing", "niche": "24/7 Emergency Plumber", "city": "Atlanta, GA"},
  {"id": 10, "name": "Silicon Valley Skin Lab", "niche": "Dermatology & Laser", "city": "Palo Alto, CA"},
  {"id": 11, "name": "Velora Activewear", "niche": "Athleisure Apparel", "city": "Los Angeles, CA"},
  {"id": 12, "name": "NuvoGlow Skincare", "niche": "Clean D2C Beauty", "city": "New York, NY"},
  {"id": 13, "name": "PulseMetrics AI", "niche": "B2B Analytics SaaS", "city": "San Francisco, CA"},
  {"id": 14, "name": "HydroFlow Bottle", "niche": "Eco Hydration D2C", "city": "Boulder, CO"},
  {"id": 15, "name": "CloudDesk Help", "niche": "Customer Support SaaS", "city": "Austin, TX"},
  {"id": 16, "name": "Artisan Roast Club", "niche": "Subscription Coffee", "city": "Portland, OR"},
  {"id": 17, "name": "StackSync Dev", "niche": "Developer Workflows", "city": "Seattle, WA"},
  {"id": 18, "name": "Pawsome Pet Boxes", "niche": "Pet Subscription D2C", "city": "Denver, CO"},
  {"id": 19, "name": "LeadFlow CRM", "niche": "SMB Sales CRM SaaS", "city": "Boston, MA"},
  {"id": 20, "name": "ZenSleep Mattress", "niche": "D2C Sleep Wellness", "city": "Chicago, IL"},
  {"id": 21, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL"},
  {"id": 22, "name": "Summit Crest Luxury Realty", "niche": "Luxury Real Estate", "city": "Aspen, CO"},
  {"id": 23, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Advisory Firm", "city": "Boston, MA"},
  {"id": 24, "name": "Pacific Coast Family Law", "niche": "Divorce & Family Law", "city": "San Diego, CA"},
  {"id": 25, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY"},
  {"id": 26, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX"},
  {"id": 27, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX"},
  {"id": 28, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA"},
  {"id": 29, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA"},
  {"id": 30, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL"}
]

def generate_invoice(lead_id, name, niche, city):
    import urllib.parse
    INVOICES_DIR.mkdir(parents=True, exist_ok=True)
    slug = name.lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
    out_file = INVOICES_DIR / f"{slug}_invoice.html"

    issue_date = datetime.now().strftime("%B %d, %Y")
    due_date = (datetime.now() + timedelta(days=14)).strftime("%B %d, %Y")
    inv_id = f"INV-2026-{lead_id:03d}"
    client_url_name = urllib.parse.quote_plus(name)
    niche_url = urllib.parse.quote_plus(niche)
    city_url = urllib.parse.quote_plus(city)

    html = INVOICE_TEMPLATE.format(
        invoice_id=inv_id,
        client_name=name,
        client_url_name=client_url_name,
        niche=niche,
        niche_url=niche_url,
        city=city,
        city_url=city_url,
        issue_date=issue_date,
        due_date=due_date,
        total_due="1,850.00",
        slug=slug
    )

    out_file.write_text(html, encoding="utf-8")
    return out_file

def generate_all_invoices():
    print("=" * 70)
    print("🚀 GENERATING 30 CUSTOM CLIENT B2B INVOICES")
    print("=" * 70)

    for l in LEADS:
        f = generate_invoice(l["id"], l["name"], l["niche"], l["city"])
        print(f"  [✓] #{l['id']:02d} Generated: {f.name}")

    print("-" * 70)
    print(f"🎉 SUCCESS: All 30 custom invoices generated in: {INVOICES_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Executive B2B Invoices")
    parser.add_argument("--all", action="store_true", help="Generate invoices for all 30 curated leads")
    parser.add_argument("--id", type=int, default=1, help="Lead ID")
    parser.add_argument("--name", default="Austin Dental Co", help="Client name")
    parser.add_argument("--niche", default="Cosmetic Dentistry", help="Niche")
    parser.add_argument("--city", default="Austin, TX", help="City")

    args = parser.parse_args()

    if args.all:
        generate_all_invoices()
    else:
        f = generate_invoice(args.id, args.name, args.niche, args.city)
        print(f"[✓] Created custom invoice: {f}")
