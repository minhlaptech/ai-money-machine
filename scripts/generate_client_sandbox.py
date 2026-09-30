"""
Executive Client Sandbox & Live Acceptance Testing Generator
------------------------------------------------------------
Tự động tạo môi trường thử nghiệm trực tiếp (Sandbox Live Preview)
cho từng khách hàng trong 84 leads B2B mục tiêu.
Cho phép khách hàng trải nghiệm ngay AI Copilot mang thương hiệu của chính họ,
chạy thử 5 kịch bản tương tác (báo giá, đặt lịch, cấp cứu, thanh toán)
và lấy mã nhúng 1 dòng HTML để đưa lên website chính thức.
"""

import sys
import os
import argparse
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
SANDBOXES_DIR = ROOT_DIR / "sandboxes"

SANDBOX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{client_name} — AI Copilot Live Sandbox Preview</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --brand: {brand_color};
      --bg: #070714;
      --card-bg: rgba(255, 255, 255, 0.04);
      --border: rgba(255, 255, 255, 0.1);
      --text: #e2e8f0;
      --text-muted: #94a3b8;
    }}
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      overflow-x: hidden;
    }}
    /* Top Banner */
    .top-bar {{
      background: linear-gradient(90deg, rgba(124,92,252,0.2), rgba(0,242,254,0.2));
      border-bottom: 1px solid var(--border);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
    }}
    .sandbox-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 242, 254, 0.15);
      border: 1px solid rgba(0, 242, 254, 0.4);
      color: #00f2fe;
      padding: 3px 10px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 11px;
      text-transform: uppercase;
    }}
    .nav-actions {{
      display: flex;
      gap: 10px;
      align-items: center;
    }}
    .nav-btn {{
      background: rgba(255,255,255,0.08);
      border: 1px solid var(--border);
      color: #cbd5e1;
      text-decoration: none;
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      transition: all 0.2s;
    }}
    .nav-btn:hover {{ background: rgba(255,255,255,0.15); color: #fff; }}
    .nav-btn.primary {{
      background: linear-gradient(135deg, var(--brand), #00f2fe);
      border: none;
      color: #fff;
    }}

    /* Simulated Client Website Hero */
    .mock-site {{
      max-width: 1000px;
      margin: 40px auto;
      padding: 0 20px;
    }}
    .mock-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 0;
      border-bottom: 1px solid rgba(255,255,255,0.06);
    }}
    .mock-logo {{
      font-family: 'Outfit', sans-serif;
      font-size: 24px;
      font-weight: 800;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .mock-logo span {{
      color: var(--brand);
    }}
    .mock-hero {{
      text-align: center;
      padding: 60px 20px;
      background: radial-gradient(circle at center, rgba(124,92,252,0.1) 0%, transparent 70%);
      border-radius: 24px;
      margin: 30px 0;
      border: 1px solid rgba(255,255,255,0.05);
    }}
    .mock-hero h1 {{
      font-family: 'Outfit', sans-serif;
      font-size: 42px;
      font-weight: 800;
      margin-bottom: 16px;
      color: #fff;
    }}
    .mock-hero p {{
      font-size: 17px;
      color: var(--text-muted);
      max-width: 650px;
      margin: 0 auto 30px;
    }}
    .mock-hero .cta-btn {{
      display: inline-block;
      background: var(--brand);
      color: #fff;
      padding: 14px 32px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 15px;
      text-decoration: none;
      box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }}

    /* Service Cards Grid */
    .services-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      margin-bottom: 50px;
    }}
    .service-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
    }}
    .service-card h3 {{
      font-size: 16px;
      color: #fff;
      margin-bottom: 8px;
    }}
    .service-card p {{
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* Sandbox Testing Dock (Bottom Left Floating Panel) */
    .testing-dock {{
      position: fixed;
      bottom: 24px;
      left: 24px;
      width: 380px;
      background: rgba(13, 13, 33, 0.95);
      border: 1px solid rgba(0, 242, 254, 0.4);
      border-radius: 16px;
      padding: 20px;
      backdrop-filter: blur(20px);
      box-shadow: 0 20px 50px rgba(0,0,0,0.7);
      z-index: 1000;
    }}
    .dock-title {{
      font-size: 13px;
      font-weight: 700;
      color: #00f2fe;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .dock-sub {{
      font-size: 11.5px;
      color: var(--text-muted);
      margin-bottom: 14px;
      line-height: 1.4;
    }}
    .test-btn {{
      display: block;
      width: 100%;
      text-align: left;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border);
      color: #cbd5e1;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      margin-bottom: 6px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .test-btn:hover {{
      background: rgba(0, 242, 254, 0.15);
      border-color: #00f2fe;
      color: #fff;
    }}
    .embed-snippet-box {{
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid rgba(255,255,255,0.08);
    }}
    .snippet-text {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
      color: #a5f3fc;
      background: rgba(0,0,0,0.5);
      padding: 8px;
      border-radius: 6px;
      word-break: break-all;
      margin-bottom: 8px;
    }}
    .btn-copy-dock {{
      width: 100%;
      background: linear-gradient(135deg, var(--brand), #00f2fe);
      border: none;
      color: #000;
      font-weight: 700;
      font-size: 12px;
      padding: 8px;
      border-radius: 6px;
      cursor: pointer;
    }}
    @media (max-width: 768px) {{
      .testing-dock {{ width: calc(100% - 48px); bottom: 12px; left: 12px; }}
      .services-grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <!-- Top Sandbox Bar -->
  <div class="top-bar">
    <div style="display:flex; align-items:center; gap:10px;">
      <span class="sandbox-pill">🧪 Sandbox Mode</span>
      <span style="color:#fff; font-weight:600;">{client_name}</span>
      <span style="color:var(--text-muted); font-size:12px;">• {niche} ({city})</span>
    </div>
    <div class="nav-actions">
      <a href="../proposals/{slug}_proposal.html" class="nav-btn">📄 Proposal</a>
      <a href="../agreements/{slug}_agreement.html" class="nav-btn">📑 Contract</a>
      <a href="../invoices/{slug}_invoice.html" class="nav-btn">💳 Invoice</a>
      <a href="https://work-minh-lap.vercel.app/onboarding?name={client_url_name}&niche={niche_url}" target="_blank" class="nav-btn primary">🚀 Go-Live Intake</a>
    </div>
  </div>

  <!-- Simulated Client Website -->
  <div class="mock-site">
    <div class="mock-header">
      <div class="mock-logo">
        <span>✦</span> {client_name}
      </div>
      <div style="font-size:13px; color:var(--text-muted);">
        {city} • Premium {niche} Services
      </div>
    </div>

    <div class="mock-hero">
      <h1>Elevate Your Experience With {client_name}</h1>
      <p>
        Leading provider of personalized, state-of-the-art {niche} solutions in {city}. Trusted by hundreds of satisfied clients with 24/7 dedicated intake support.
      </p>
      <a href="#chat" onclick="triggerChatWidget()" class="cta-btn">💬 Chat with AI Receptionist</a>
    </div>

    <div class="services-grid">
      <div class="service-card">
        <h3>Comprehensive Solutions</h3>
        <p>Expert diagnostic evaluations, personalized treatment or service plans tailored to your exact timeline.</p>
      </div>
      <div class="service-card">
        <h3>Transparent Investment</h3>
        <p>Upfront pricing with direct insurance, financing options, and zero surprise fees.</p>
      </div>
      <div class="service-card">
        <h3>Instant 24/7 Booking</h3>
        <p>Book emergency appointments or free initial consultations anytime directly with our automated intake copilot.</p>
      </div>
    </div>
  </div>

  <!-- Interactive Sandbox Testing Control Panel -->
  <div class="testing-dock">
    <div class="dock-title">
      <span>⚡ UAT Acceptance Testing Panel</span>
      <span style="font-size:10px; color:#00e676;">● Active Sandbox</span>
    </div>
    <div class="dock-sub">
      Click any test case to simulate a real customer inquiry and verify instant AI qualification:
    </div>

    <button class="test-btn" onclick="simulateTest('Hi! What are your typical pricing rates and services for new clients?')">
      💵 <strong>Test 1:</strong> Pricing & Service Scope
    </button>
    <button class="test-btn" onclick="simulateTest('I need to book an appointment for this Thursday afternoon, do you have openings?')">
      📅 <strong>Test 2:</strong> Booking & Calendar Sync
    </button>
    <button class="test-btn" onclick="simulateTest('This is an urgent situation! Who can I speak with immediately?')">
      🚨 <strong>Test 3:</strong> Emergency Escalation
    </button>
    <button class="test-btn" onclick="simulateTest('What insurance plans or financing options do you accept?')">
      💳 <strong>Test 4:</strong> Insurance / Financing
    </button>
    <button class="test-btn" onclick="simulateTest('Can someone from the office call me back at my number?')">
      📞 <strong>Test 5:</strong> Callback Intake Request
    </button>

    <div class="embed-snippet-box">
      <div style="font-size:11px; color:#fff; font-weight:600; margin-bottom:4px;">📋 Client 1-Line Embed Code:</div>
      <div class="snippet-text" id="snippet-code">&lt;script src="https://work-minh-lap.vercel.app/copilot-widget.js" data-business="{client_name}" data-color="{brand_color}" async&gt;&lt;/script&gt;</div>
      <button class="btn-copy-dock" onclick="copySnippetCode()">Copy Production Script Tag</button>
    </div>
  </div>

  <script>
    function triggerChatWidget() {{
      const container = document.getElementById('minhlap-copilot-container');
      if (container && container.shadowRoot) {{
        const launcher = container.shadowRoot.getElementById('copilot-launcher');
        if (launcher) launcher.click();
      }}
    }}

    function simulateTest(queryText) {{
      const container = document.getElementById('minhlap-copilot-container');
      if (container && container.shadowRoot) {{
        const launcher = container.shadowRoot.getElementById('copilot-launcher');
        const modal = container.shadowRoot.getElementById('copilot-modal');
        if (modal && !modal.classList.contains('open')) {{
          if (launcher) launcher.click();
        }}
        setTimeout(() => {{
          const input = container.shadowRoot.getElementById('copilot-input');
          const sendBtn = container.shadowRoot.getElementById('copilot-send');
          if (input && sendBtn) {{
            input.value = queryText;
            sendBtn.click();
          }}
        }}, 250);
      }}
    }}

    function copySnippetCode() {{
      const txt = document.getElementById('snippet-code').innerText;
      navigator.clipboard.writeText(txt).then(() => {{
        alert('Copied 1-Line Script Tag to Clipboard! Ready for client website.');
      }});
    }}
  </script>

  <!-- Live Embed of Copilot Widget -->
  <script src="https://work-minh-lap.vercel.app/copilot-widget.js" 
          data-business="{client_name}" 
          data-color="{brand_color}" 
          data-booking="https://calendly.com/your-clinic" 
          async></script>
</body>
</html>
"""

LEADS = [
  {"id": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX", "color": "#7c5cfc"},
  {"id": 2, "name": "Pure Radiance MedSpa", "niche": "Medical Aesthetics", "city": "Miami, FL", "color": "#ec4899"},
  {"id": 3, "name": "Premier 24/7 HVAC", "niche": "Emergency HVAC", "city": "Dallas, TX", "color": "#f97316"},
  {"id": 4, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "color": "#3b82f6"},
  {"id": 5, "name": "Summit Crest Luxury Realty", "niche": "High-End Real Estate", "city": "Scottsdale, AZ", "color": "#eab308"},
  {"id": 6, "name": "ProActive Spine & Chiro", "niche": "Chiropractic & Wellness", "city": "Denver, CO", "color": "#10b981"},
  {"id": 7, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Wealth Advisory", "city": "Boston, MA", "color": "#6366f1"},
  {"id": 8, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Diego, CA", "color": "#06b6d4"},
  {"id": 9, "name": "Rapid Response Plumbing", "niche": "Commercial Plumbing", "city": "Atlanta, GA", "color": "#ef4444"},
  {"id": 10, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar EPC", "city": "Orlando, FL", "color": "#f59e0b"},
  {"id": 11, "name": "Velora Activewear", "niche": "Athleisure & Fitness", "city": "Los Angeles, CA", "color": "#a855f7"},
  {"id": 12, "name": "NuvoGlow Skincare", "niche": "Clean Beauty & Cosmetics", "city": "New York, NY", "color": "#f43f5e"},
  {"id": 13, "name": "Artisan Roast Club", "niche": "Specialty Coffee Subscription", "city": "Seattle, WA", "color": "#d97706"},
  {"id": 14, "name": "ZenSleep Mattress", "niche": "Sleep Tech & Bedding", "city": "San Francisco, CA", "color": "#4f46e5"},
  {"id": 15, "name": "HydroFlow Bottle", "niche": "Smart Hydration & Gear", "city": "Boulder, CO", "color": "#0284c7"},
  {"id": 16, "name": "Pawsome Pet Boxes", "niche": "Pet Supplies & Subscriptions", "city": "Austin, TX", "color": "#84cc16"},
  {"id": 17, "name": "Lumina Wellness", "niche": "Nootropics & Supplements", "city": "Miami, FL", "color": "#14b8a6"},
  {"id": 18, "name": "StackSync Dev", "niche": "Developer Tools & SaaS", "city": "San Jose, CA", "color": "#8b5cf6"},
  {"id": 19, "name": "LeadFlow CRM", "niche": "B2B Sales Automation", "city": "Chicago, IL", "color": "#2563eb"},
  {"id": 20, "name": "CloudDesk Help", "niche": "Customer Support Platform", "city": "Boston, MA", "color": "#0ea5e9"},
  {"id": 21, "name": "PulseMetrics AI", "niche": "Product Analytics SaaS", "city": "New York, NY", "color": "#9333ea"},
  {"id": 22, "name": "Silicon Valley Skin Lab", "niche": "Dermatology Clinic", "city": "Palo Alto, CA", "color": "#ec4899"},
  {"id": 23, "name": "Pacific Coast Family Law", "niche": "Family Law & Mediation", "city": "Newport Beach, CA", "color": "#1d4ed8"},
  {"id": 24, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Beverly Hills, CA", "color": "#ca8a04"},
  {"id": 25, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "color": "#4338ca"},
  {"id": 26, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "color": "#b91c1c"},
  {"id": 27, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "color": "#c2410c"},
  {"id": 28, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "color": "#047857"},
  {"id": 29, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "color": "#374151"},
  {"id": 30, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "color": "#dc2626"}
]

def generate_sandbox(lead_id, name, niche, city, color="#7c5cfc"):
    import urllib.parse
    SANDBOXES_DIR.mkdir(parents=True, exist_ok=True)
    slug = name.lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
    out_file = SANDBOXES_DIR / f"{slug}_sandbox.html"

    client_url_name = urllib.parse.quote_plus(name)
    niche_url = urllib.parse.quote_plus(niche)

    html = SANDBOX_TEMPLATE.format(
        client_name=name,
        client_url_name=client_url_name,
        niche=niche,
        niche_url=niche_url,
        city=city,
        brand_color=color,
        slug=slug
    )

    out_file.write_text(html, encoding="utf-8")
    return out_file

def generate_all_sandboxes():
    print("=" * 70)
    print(f"🚀 GENERATING {len(LEADS)} CUSTOM CLIENT LIVE SANDBOX PREVIEWS")
    print("=" * 70)

    for l in LEADS:
        f = generate_sandbox(l["id"], l["name"], l["niche"], l["city"], l.get("color", "#7c5cfc"))
        print(f"  [✓] #{l['id']:02d} Generated: {f.name}")

    print("-" * 70)
    print(f"🎉 SUCCESS: All {len(LEADS)} custom sandboxes generated in: {SANDBOXES_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Executive B2B Live Sandboxes")
    parser.add_argument("--all", action="store_true", help="Generate sandboxes for all 84 curated leads")
    parser.add_argument("--id", type=int, default=1, help="Lead ID")
    parser.add_argument("--name", default="Austin Dental Co", help="Client name")
    parser.add_argument("--niche", default="Cosmetic Dentistry", help="Niche")
    parser.add_argument("--city", default="Austin, TX", help="City")
    parser.add_argument("--color", default="#7c5cfc", help="Brand color hex")

    args = parser.parse_args()

    if args.all:
        generate_all_sandboxes()
    else:
        f = generate_sandbox(args.id, args.name, args.niche, args.city, args.color)
        print(f"[✓] Created custom sandbox: {f}")
