"""
Executive Client Pitch & Demonstration Hub Generator
---------------------------------------------------
Tạo trang tổng quan trực quan cao cấp (pitches/index.html)
tập hợp toàn bộ 30 bộ Sales Pitch Decks và 30 Live Sandboxes.
Cho phép tìm kiếm nhanh, lọc theo ngành nghề, và mở các tài liệu bán hàng
chỉ với 1 cú click chuột.
"""

import sys
import os
import json
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
OUT_FILE = ROOT_DIR / "pitches" / "index.html"

LEADS = [
  # Batch 1
  {"id": 1, "batch": 1, "name": "Austin Dental Co", "niche": "Cosmetic Dentistry", "city": "Austin, TX", "val": 750, "lost": 18, "icon": "🦷"},
  {"id": 2, "batch": 1, "name": "Pure Radiance MedSpa", "niche": "Medical Aesthetics", "city": "Miami, FL", "val": 650, "lost": 16, "icon": "✨"},
  {"id": 3, "batch": 1, "name": "Premier 24/7 HVAC", "niche": "Emergency HVAC", "city": "Dallas, TX", "val": 850, "lost": 15, "icon": "❄️"},
  {"id": 4, "batch": 1, "name": "Sterling & Partners Legal", "niche": "Personal Injury Law", "city": "Chicago, IL", "val": 2500, "lost": 8, "icon": "⚖️"},
  {"id": 5, "batch": 1, "name": "Summit Crest Luxury Realty", "niche": "High-End Real Estate", "city": "Scottsdale, AZ", "val": 4000, "lost": 5, "icon": "🏰"},
  {"id": 6, "batch": 1, "name": "ProActive Spine & Chiro", "niche": "Chiropractic & Wellness", "city": "Denver, CO", "val": 450, "lost": 22, "icon": "🩺"},
  {"id": 7, "batch": 1, "name": "Beacon Hill CPA & Tax", "niche": "Tax & Wealth Advisory", "city": "Boston, MA", "val": 1200, "lost": 10, "icon": "📈"},
  {"id": 8, "batch": 1, "name": "Elite Smile Studio", "niche": "Orthodontics", "city": "San Diego, CA", "val": 950, "lost": 14, "icon": "😁"},
  {"id": 9, "batch": 1, "name": "Rapid Response Plumbing", "niche": "Commercial Plumbing", "city": "Atlanta, GA", "val": 600, "lost": 20, "icon": "🔧"},
  {"id": 10, "batch": 1, "name": "Apex Roofing & Solar", "niche": "Roofing & Solar EPC", "city": "Orlando, FL", "val": 3500, "lost": 6, "icon": "☀️"},

  # Batch 2
  {"id": 11, "batch": 2, "name": "Velora Activewear", "niche": "Athleisure & Fitness", "city": "Los Angeles, CA", "val": 120, "lost": 65, "icon": "🏃"},
  {"id": 12, "batch": 2, "name": "NuvoGlow Skincare", "niche": "Clean Beauty & Cosmetics", "city": "New York, NY", "val": 95, "lost": 80, "icon": "🧴"},
  {"id": 13, "batch": 2, "name": "Artisan Roast Club", "niche": "Specialty Coffee Subscription", "city": "Seattle, WA", "val": 85, "lost": 90, "icon": "☕"},
  {"id": 14, "batch": 2, "name": "ZenSleep Mattress", "niche": "Sleep Tech & Bedding", "city": "San Francisco, CA", "val": 850, "lost": 12, "icon": "🛏️"},
  {"id": 15, "batch": 2, "name": "HydroFlow Bottle", "niche": "Smart Hydration & Gear", "city": "Boulder, CO", "val": 75, "lost": 95, "icon": "💧"},
  {"id": 16, "batch": 2, "name": "Pawsome Pet Boxes", "niche": "Pet Supplies & Subscriptions", "city": "Austin, TX", "val": 65, "lost": 110, "icon": "🐾"},
  {"id": 17, "batch": 2, "name": "Lumina Wellness", "niche": "Nootropics & Supplements", "city": "Miami, FL", "val": 110, "lost": 70, "icon": "🌿"},
  {"id": 18, "batch": 2, "name": "StackSync Dev", "niche": "Developer Tools & SaaS", "city": "San Jose, CA", "val": 1400, "lost": 8, "icon": "💻"},
  {"id": 19, "batch": 2, "name": "LeadFlow CRM", "niche": "B2B Sales Automation", "city": "Chicago, IL", "val": 1800, "lost": 7, "icon": "📊"},
  {"id": 20, "batch": 2, "name": "CloudDesk Help", "niche": "Customer Support Platform", "city": "Boston, MA", "val": 1200, "lost": 9, "icon": "🎧"},

  # Batch 3
  {"id": 21, "batch": 3, "name": "PulseMetrics AI", "niche": "Product Analytics SaaS", "city": "New York, NY", "val": 2200, "lost": 6, "icon": "⚡"},
  {"id": 22, "batch": 3, "name": "Silicon Valley Skin Lab", "niche": "Dermatology Clinic", "city": "Palo Alto, CA", "val": 750, "lost": 16, "icon": "🔬"},
  {"id": 23, "batch": 3, "name": "Pacific Coast Family Law", "niche": "Family Law & Mediation", "city": "Newport Beach, CA", "val": 3000, "lost": 6, "icon": "🏛️"},
  {"id": 24, "batch": 3, "name": "Vanguard Luxury RE", "niche": "Luxury Real Estate", "city": "Beverly Hills, CA", "val": 5000, "lost": 4, "icon": "🏡"},
  {"id": 25, "batch": 3, "name": "Vanguard Wealth & Accounting", "niche": "Family Office & CPA", "city": "New York, NY", "val": 2800, "lost": 5, "icon": "💼"},
  {"id": 26, "batch": 3, "name": "Redwood Corporate Counsel", "niche": "Corporate & M&A", "city": "Austin, TX", "val": 3500, "lost": 5, "icon": "📜"},
  {"id": 27, "batch": 3, "name": "Pinnacle Commercial RE", "niche": "Commercial Brokerage", "city": "Dallas, TX", "val": 4500, "lost": 4, "icon": "🏢"},
  {"id": 28, "batch": 3, "name": "Harborview Estate Planning", "niche": "Trusts & Estates", "city": "Seattle, WA", "val": 2200, "lost": 7, "icon": "🛡️"},
  {"id": 29, "batch": 3, "name": "Apex Audit & Valuation", "niche": "Audit & Valuation", "city": "Atlanta, GA", "val": 3200, "lost": 5, "icon": "📊"},
  {"id": 30, "batch": 3, "name": "Metro Injury Defense Group", "niche": "Insurance Litigation", "city": "Miami, FL", "val": 4000, "lost": 4, "icon": "⚖️"}
]

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Executive Sales Pitch & Demonstration Hub — 30 Curated Client Dossiers</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #070714;
      --card-bg: rgba(255, 255, 255, 0.03);
      --card-border: rgba(255, 255, 255, 0.08);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --accent: #7c5cfc;
      --cyan: #00f2fe;
      --emerald: #34d399;
      --amber: #ffb74d;
      --rose: #f43f5e;
      --font-heading: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      min-height: 100vh;
      line-height: 1.6;
    }

    /* Ambient Glow */
    .ambient-glow {
      position: fixed;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 800px;
      height: 400px;
      background: radial-gradient(circle, rgba(124, 92, 252, 0.15) 0%, rgba(0, 242, 254, 0.05) 50%, transparent 70%);
      pointer-events: none;
      z-index: 0;
    }

    /* Header Nav */
    header {
      position: sticky;
      top: 0;
      background: rgba(7, 7, 20, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--card-border);
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 100;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-family: var(--font-heading);
      font-size: 16px;
      font-weight: 800;
      color: #fff;
    }
    .brand-tag {
      background: linear-gradient(135deg, var(--accent), var(--cyan));
      color: #000;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      font-family: var(--font-mono);
    }

    .nav-links {
      display: flex;
      gap: 12px;
    }
    .nav-link {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 13px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 6px;
      border: 1px solid transparent;
      transition: all 0.2s;
    }
    .nav-link:hover {
      color: #fff;
      border-color: var(--card-border);
      background: rgba(255, 255, 255, 0.04);
    }

    /* Container */
    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 40px 24px 80px;
      position: relative;
      z-index: 1;
    }

    /* Hero */
    .hero {
      text-align: center;
      margin-bottom: 40px;
    }
    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(124, 92, 252, 0.12);
      border: 1px solid rgba(124, 92, 252, 0.3);
      color: #b794f4;
      padding: 4px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      font-family: var(--font-mono);
      margin-bottom: 16px;
    }
    .hero h1 {
      font-family: var(--font-heading);
      font-size: 42px;
      font-weight: 900;
      color: #fff;
      line-height: 1.15;
      margin-bottom: 12px;
    }
    .hero p {
      font-size: 16px;
      color: var(--text-muted);
      max-width: 720px;
      margin: 0 auto 28px;
    }

    /* Filter & Search Bar */
    .control-bar {
      background: rgba(15, 17, 35, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 16px 20px;
      margin-bottom: 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      backdrop-filter: blur(16px);
    }

    .search-box {
      flex: 1;
      min-width: 260px;
      position: relative;
    }
    .search-box input {
      width: 100%;
      background: rgba(0, 0, 0, 0.4);
      border: 1px solid var(--card-border);
      color: #fff;
      font-size: 13px;
      padding: 10px 14px 10px 38px;
      border-radius: 8px;
      outline: none;
      transition: all 0.2s;
    }
    .search-box input:focus {
      border-color: var(--cyan);
      box-shadow: 0 0 12px rgba(0, 242, 254, 0.2);
    }
    .search-icon {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 14px;
      color: var(--text-muted);
    }

    .batch-filters {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .batch-pill {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      color: var(--text-muted);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .batch-pill:hover {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.2);
    }
    .batch-pill.active {
      background: linear-gradient(135deg, var(--accent), var(--cyan));
      color: #000;
      font-weight: 700;
      border-color: transparent;
    }

    /* Cards Grid */
    .leads-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 20px;
    }

    .lead-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s;
    }
    .lead-card:hover {
      border-color: rgba(0, 242, 254, 0.3);
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }
    .card-title {
      font-family: var(--font-heading);
      font-size: 18px;
      font-weight: 700;
      color: #fff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .batch-tag {
      font-size: 10px;
      font-family: var(--font-mono);
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .batch-1 { background: rgba(124, 92, 252, 0.15); color: #b794f4; border: 1px solid rgba(124, 92, 252, 0.3); }
    .batch-2 { background: rgba(0, 242, 254, 0.15); color: #00f2fe; border: 1px solid rgba(0, 242, 254, 0.3); }
    .batch-3 { background: rgba(255, 183, 77, 0.15); color: #ffb74d; border: 1px solid rgba(255, 183, 77, 0.3); }

    .card-meta {
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 16px;
    }
    .card-meta span {
      color: var(--cyan);
    }

    .metrics-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      background: rgba(0, 0, 0, 0.3);
      padding: 10px 12px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.04);
      margin-bottom: 16px;
    }
    .metric-item-val {
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      color: #fff;
    }
    .metric-item-lbl {
      font-size: 10.5px;
      color: var(--text-muted);
      text-transform: uppercase;
    }

    .btn-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-bottom: 8px;
    }
    .btn-full {
      grid-column: span 2;
    }

    .action-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--card-border);
      color: #cbd5e1;
      text-decoration: none;
      font-size: 11.5px;
      font-weight: 600;
      padding: 7px 10px;
      border-radius: 6px;
      transition: all 0.15s;
    }
    .action-btn:hover {
      border-color: var(--cyan);
      color: #fff;
      background: rgba(255, 255, 255, 0.1);
    }
    .action-btn.primary {
      background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(124, 92, 252, 0.2));
      border-color: rgba(244, 63, 94, 0.4);
      color: #fb7185;
      font-weight: 700;
    }
    .action-btn.primary:hover {
      background: rgba(244, 63, 94, 0.3);
      color: #fff;
    }
    .action-btn.sandbox {
      background: rgba(0, 242, 254, 0.1);
      border-color: rgba(0, 242, 254, 0.3);
      color: #00f2fe;
    }
    .action-btn.sandbox:hover {
      background: rgba(0, 242, 254, 0.2);
      color: #fff;
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--card-border);
      padding: 24px;
      text-align: center;
      font-size: 12px;
      color: var(--text-muted);
    }
  </style>
</head>
<body>
  <div class="ambient-glow"></div>

  <!-- Header -->
  <header>
    <div class="brand">
      <span>⚡ SYNAPSE AI ARCHITECTURE</span>
      <span class="brand-tag">SHOWCASE HUB</span>
    </div>
    <nav class="nav-links">
      <a href="../index.html" class="nav-link">← Master Dashboard</a>
      <a href="../onboarding" class="nav-link">Intake Portal</a>
      <a href="../calculator" class="nav-link">ROI Calculator</a>
      <a href="../blog" class="nav-link">Resource Hub</a>
    </nav>
  </header>

  <div class="container">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-badge">30 CLIENT SALES DOSSIERS & LIVE PROTOTYPES</div>
      <h1>Executive Sales Pitch & Demo Hub</h1>
      <p>
        Bespoke 10-slide interactive sales presentations and live sandbox prototypes engineered for 30 high-ticket enterprises. Optimized for Zoom and Google Meet closing calls.
      </p>
    </div>

    <!-- Controls -->
    <div class="control-bar">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="search-input" placeholder="Search by client name, industry, or city..." oninput="handleSearch()">
      </div>
      <div class="batch-filters">
        <button class="batch-pill active" onclick="filterBatch('all', this)">All Leads (30)</button>
        <button class="batch-pill" onclick="filterBatch('1', this)">🦷 Batch 1: SMBs (10)</button>
        <button class="batch-pill" onclick="filterBatch('2', this)">🛍️ Batch 2: E-Com (10)</button>
        <button class="batch-pill" onclick="filterBatch('3', this)">🏛️ Batch 3: High-Ticket (10)</button>
      </div>
    </div>

    <!-- Cards Grid -->
    <div class="leads-grid" id="leads-grid">
      <!-- Injected via JavaScript -->
    </div>
  </div>

  <footer>
    MinhLap AI Automation Solutions • Turnkey 24/7 Client Intake Infrastructure • <a href="https://work-minh-lap.vercel.app" style="color:var(--cyan); text-decoration:none;">Executive Command Center</a>
  </footer>

  <script>
    const LEADS_DATA = """ + json.dumps(LEADS, indent=2) + """;

    let currentBatch = 'all';
    let searchQuery = '';

    function getSlug(name) {
      return name.toLowerCase().replace(/ /g, '_').replace(/&/g, 'and').replace(/\\//g, '-').replace(/\\\\/g, '-').replace(/,/g, '').replace(/\\./g, '');
    }

    function renderCards() {
      const grid = document.getElementById('leads-grid');
      let filtered = LEADS_DATA;

      if (currentBatch !== 'all') {
        filtered = filtered.filter(l => l.batch === parseInt(currentBatch));
      }

      if (searchQuery.trim() !== '') {
        const q = searchQuery.toLowerCase();
        filtered = filtered.filter(l => 
          l.name.toLowerCase().includes(q) || 
          l.niche.toLowerCase().includes(q) || 
          l.city.toLowerCase().includes(q)
        );
      }

      if (filtered.length === 0) {
        grid.innerHTML = `
          <div style="grid-column: 1 / -1; text-align:center; padding:60px 20px; color:var(--text-muted);">
            <div style="font-size:36px; margin-bottom:12px;">🔍</div>
            <div style="font-size:16px; font-weight:600; color:#fff;">No matching clients found</div>
            <div style="font-size:13px; margin-top:4px;">Try searching for a different name, industry, or city.</div>
          </div>
        `;
        return;
      }

      grid.innerHTML = filtered.map(l => {
        const slug = getSlug(l.name);
        const pitchUrl = `${slug}_pitch.html`;
        const sandboxUrl = `../sandboxes/${slug}_sandbox.html`;
        const agreementUrl = `../agreements/${slug}_agreement.html`;
        const invoiceUrl = `../invoices/${slug}_invoice.html`;
        const reportUrl = `../reports/${slug}_roi_report.html`;
        const proposalUrl = `../proposals/${slug}_proposal.html`;

        const batchClass = `batch-${l.batch}`;
        const batchName = l.batch === 1 ? 'SMB' : l.batch === 2 ? 'E-Com' : 'High-Ticket';
        const leadIdStr = String(l.id).padStart(2, '0');

        const monthlyLoss = (l.lost * l.val).toLocaleString();

        return `
          <div class="lead-card">
            <div>
              <div class="card-top">
                <div class="card-title">
                  <span>${l.icon}</span> ${l.name}
                </div>
                <span class="batch-tag ${batchClass}">#${leadIdStr} • ${batchName}</span>
              </div>
              <div class="card-meta">
                ${l.niche} • <span>${l.city}</span>
              </div>

              <div class="metrics-row">
                <div>
                  <div class="metric-item-val" style="color:var(--rose);">$${monthlyLoss}</div>
                  <div class="metric-item-lbl">Missed / Month</div>
                </div>
                <div>
                  <div class="metric-item-val" style="color:var(--emerald);">$${l.val.toLocaleString()}</div>
                  <div class="metric-item-lbl">Avg Deal Value</div>
                </div>
              </div>
            </div>

            <div>
              <div class="btn-grid">
                <a href="${pitchUrl}" target="_blank" class="action-btn primary btn-full">
                  🖥️ Launch Pitch Deck (10 Slides) ↗
                </a>
                <a href="${sandboxUrl}" target="_blank" class="action-btn sandbox">
                  🧪 Live Sandbox
                </a>
                <a href="${proposalUrl}" target="_blank" class="action-btn">
                  📄 Proposal
                </a>
                <a href="${agreementUrl}" target="_blank" class="action-btn">
                  📑 MSA Contract
                </a>
                <a href="${invoiceUrl}" target="_blank" class="action-btn">
                  💳 Invoice ($1,850)
                </a>
              </div>
              <div style="display:flex; flex-direction:column; gap:5px; margin-top:6px;">
                <a href="${reportUrl}" target="_blank" class="action-btn" style="width:100%; justify-content:center; font-size:11px; color:var(--amber);">
                  📊 View Monthly ROI Forecast ↗
                </a>
                <a href="../client_packages/${slug}_executive_dossier.zip" download class="action-btn" style="width:100%; justify-content:center; font-size:11px; color:#c084fc; border-color:rgba(192, 132, 252, 0.35);">
                  📦 Download VIP Onboarding ZIP Dossier 📥
                </a>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterBatch(batch, btn) {
      currentBatch = batch;
      document.querySelectorAll('.batch-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderCards();
    }

    function handleSearch() {
      searchQuery = document.getElementById('search-input').value;
      renderCards();
    }

    window.addEventListener('DOMContentLoaded', renderCards);
  </script>
</body>
</html>
"""

def generate_hub():
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(HTML_CONTENT, encoding="utf-8")
    print(f"[✓] Generated Showcase Hub: {OUT_FILE}")

if __name__ == "__main__":
    generate_hub()
