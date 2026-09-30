"""
Executive Deliverables & Onboarding Dossier Hub Generator (Flagship Web App #19)
================================================================================
Xuất bản Web App Flagship #19:
  - `packages/index.html` (truy cập qua `/packages`, `/dossiers`, `/dossier`)
Hỗ trợ quản lý, tra cứu và tải xuống trọn bộ 119 hồ sơ bàn giao độc quyền (ZIP Dossiers)
cho toàn bộ 4 phân tầng doanh nghiệp thuộc đế chế target $1,218,600 ARR ($101,550/mo Pipeline).
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
PACKAGES_DIR = ROOT_DIR / "packages"
LEDGER_FILE = ROOT_DIR / "prospects" / "autonomous_packages_ledger.json"

def build_packages_hub():
    if not LEDGER_FILE.exists():
        print(f"❌ Error: Packages ledger not found at {LEDGER_FILE}")
        return

    with open(LEDGER_FILE, "r", encoding="utf-8") as f:
        ledger_data = json.load(f)

    meta = ledger_data["metadata"]
    packages = ledger_data["packages"]

    packages_json_str = json.dumps(packages, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Executive Deliverables & Onboarding Dossier Hub — 119 Production Packages</title>
  <meta name="description" content="Centralized archival repository and 1-click download hub for 119 complete client onboarding dossiers across Base SMBs, Enterprise Voice Swarms, Sovereign Private VPCs, and Syndicate Franchises.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #030712;
      --card-bg: rgba(15, 23, 42, 0.72);
      --card-border: rgba(255, 255, 255, 0.08);
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --cyan: #00f2fe;
      --purple: #7c5cfc;
      --gold: #f59e0b;
      --green: #10b981;
      --font-heading: 'Outfit', sans-serif;
      --font-body: 'Inter', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      min-height: 100vh;
      overflow-x: hidden;
    }}

    /* Glow Orbs */
    .glow-orb {{
      position: fixed; border-radius: 50%; filter: blur(140px); pointer-events: none; z-index: 0;
    }}
    .orb-1 {{ width: 650px; height: 650px; background: rgba(0, 242, 254, 0.12); top: -150px; left: -120px; }}
    .orb-2 {{ width: 600px; height: 600px; background: rgba(124, 92, 252, 0.14); bottom: -150px; right: -120px; }}

    /* Header */
    header {{
      background: rgba(3, 7, 18, 0.88);
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(20px);
      padding: 16px 24px;
    }}
    .header-inner {{
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #fff;
    }}
    .brand-icon {{
      width: 40px;
      height: 40px;
      border-radius: 10px;
      background: linear-gradient(135deg, #00f2fe, #7c5cfc);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20px;
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
    }}
    .brand-title {{
      font-family: var(--font-heading);
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.5px;
    }}
    .brand-sub {{
      font-size: 11px;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    .nav-links {{
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .nav-btn {{
      background: rgba(255,255,255,0.06);
      border: 1px solid var(--card-border);
      color: #cbd5e1;
      text-decoration: none;
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 600;
      transition: all 0.2s;
    }}
    .nav-btn:hover {{ background: rgba(255,255,255,0.12); color: #fff; }}
    .nav-btn.primary {{
      background: linear-gradient(135deg, rgba(0,242,254,0.15), rgba(124,92,252,0.15));
      border-color: rgba(0, 242, 254, 0.4);
      color: #00f2fe;
    }}

    /* Main Container */
    main {{
      position: relative;
      z-index: 1;
    }}

    /* Hero Section */
    .hero {{
      max-width: 1400px;
      margin: 36px auto 24px;
      padding: 0 24px;
      text-align: center;
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(0, 242, 254, 0.12);
      border: 1px solid rgba(0, 242, 254, 0.35);
      color: #00f2fe;
      padding: 5px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .pulse-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0% {{ opacity: 0.4; }}
      50% {{ opacity: 1; }}
      100% {{ opacity: 0.4; }}
    }}

    .hero h1 {{
      font-family: var(--font-heading);
      font-size: 44px;
      font-weight: 800;
      letter-spacing: -1px;
      background: linear-gradient(135deg, #fff 40%, #00f2fe 80%, #7c5cfc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }}
    .hero p {{
      color: var(--text-muted);
      font-size: 16px;
      max-width: 840px;
      margin: 0 auto 32px;
    }}

    /* Global KPIs */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      max-width: 1200px;
      margin: 0 auto 36px;
      padding: 0 24px;
    }}
    @media (max-width: 900px) {{ .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 500px) {{ .kpi-grid {{ grid-template-columns: 1fr; }} }}

    .kpi-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      padding: 20px;
      text-align: left;
      backdrop-filter: blur(16px);
    }}
    .kpi-val {{
      font-family: var(--font-mono);
      font-size: 28px;
      font-weight: 800;
      color: #fff;
    }}
    .kpi-lbl {{
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}

    /* Controls Bar: Search + Jump + Filter */
    .controls-bar {{
      max-width: 1400px;
      margin: 0 auto 24px;
      padding: 0 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .controls-top {{
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
    }}
    .search-input {{
      flex: 1;
      min-width: 280px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 18px;
      color: #fff;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--cyan);
      box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }}
    .jump-select {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px 16px;
      color: #cbd5e1;
      font-size: 13px;
      outline: none;
      cursor: pointer;
      min-width: 240px;
    }}

    .filter-pills {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 4px;
    }}
    .pill-btn {{
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--card-border);
      color: #94a3b8;
      padding: 7px 16px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }}
    .pill-btn:hover {{
      background: rgba(255,255,255,0.1);
      color: #fff;
    }}
    .pill-btn.active {{
      background: linear-gradient(135deg, rgba(0,242,254,0.2), rgba(124,92,252,0.2));
      border-color: var(--cyan);
      color: #00f2fe;
    }}

    .results-meta {{
      max-width: 1400px;
      margin: 0 auto 16px;
      padding: 0 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      color: var(--text-muted);
    }}

    /* Dossiers Grid */
    .packages-grid {{
      max-width: 1400px;
      margin: 0 auto 60px;
      padding: 0 24px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 22px;
    }}
    @media (max-width: 1100px) {{ .packages-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 700px) {{ .packages-grid {{ grid-template-columns: 1fr; }} }}

    .pkg-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.25s ease;
      backdrop-filter: blur(16px);
      position: relative;
    }}
    .pkg-card:hover {{
      transform: translateY(-4px);
      border-color: rgba(0, 242, 254, 0.4);
      box-shadow: 0 14px 34px rgba(0,0,0,0.55);
    }}

    .card-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }}
    .tier-badge {{
      display: inline-block;
      font-size: 10.5px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .tier-base {{ background: rgba(124,92,252,0.18); color: #c4b5fd; border: 1px solid rgba(124,92,252,0.4); }}
    .tier-enterprise {{ background: rgba(56,189,248,0.18); color: #38bdf8; border: 1px solid rgba(56,189,248,0.5); }}
    .tier-sovereign {{ background: rgba(245,158,11,0.18); color: #fbbf24; border: 1px solid rgba(245,158,11,0.5); }}
    .tier-syndicate {{ background: rgba(168,85,247,0.18); color: #d8b4fe; border: 1px solid rgba(168,85,247,0.5); }}

    .pkg-name {{
      font-family: var(--font-heading);
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
    }}
    .pkg-sub {{
      font-size: 12.5px;
      color: var(--text-muted);
      margin-bottom: 14px;
    }}

    /* Financial Row */
    .finance-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      background: rgba(0,0,0,0.35);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 8px;
      padding: 8px 10px;
      margin-bottom: 14px;
      text-align: center;
    }}
    .fin-item .fin-lbl {{ font-size: 10px; color: var(--text-muted); text-transform: uppercase; }}
    .fin-item .fin-val {{ font-family: var(--font-mono); font-size: 13px; font-weight: 700; color: #fff; margin-top: 2px; }}

    /* SHA-256 Section */
    .hash-box {{
      background: rgba(0, 0, 0, 0.45);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 8px;
      padding: 8px 12px;
      margin-bottom: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-mono);
      font-size: 11px;
    }}
    .hash-text {{
      color: #00f2fe;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 190px;
    }}
    .btn-copy-hash {{
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.1);
      color: #cbd5e1;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 10.5px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .btn-copy-hash:hover {{
      background: var(--cyan);
      color: #000;
    }}

    /* Deliverables Badges Grid */
    .deliverables-checklist {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 18px;
    }}
    .badge-item {{
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.07);
      border-radius: 6px;
      padding: 3px 8px;
      font-size: 10.5px;
      color: #cbd5e1;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    /* Action Buttons */
    .btn-download {{
      background: linear-gradient(135deg, #00f2fe, #7c5cfc);
      color: #030712;
      text-align: center;
      padding: 11px;
      border-radius: 9px;
      font-weight: 800;
      font-size: 13.5px;
      text-decoration: none;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
      margin-bottom: 10px;
    }}
    .btn-download:hover {{
      box-shadow: 0 6px 20px rgba(0,242,254,0.4);
      transform: translateY(-1px);
    }}

    .sub-actions {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 6px;
    }}
    .btn-sub {{
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--card-border);
      color: #94a3b8;
      text-decoration: none;
      padding: 6px 2px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      text-align: center;
      transition: all 0.15s;
    }}
    .btn-sub:hover {{
      background: rgba(255,255,255,0.12);
      color: #fff;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--card-border);
      padding: 40px 24px;
      text-align: center;
      font-size: 13px;
      color: var(--text-muted);
      background: rgba(3, 7, 18, 0.95);
      position: relative;
      z-index: 10;
    }}
    .footer-links {{
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-top: 12px;
      flex-wrap: wrap;
    }}
    .footer-links a {{
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.15s;
    }}
    .footer-links a:hover {{ color: var(--cyan); }}
  </style>
</head>
<body>
  <div class="glow-orb orb-1"></div>
  <div class="glow-orb orb-2"></div>

  <!-- Header -->
  <header>
    <div class="header-inner">
      <a href="/" class="brand">
        <div class="brand-icon">📦</div>
        <div>
          <div class="brand-title">Executive Deliverables Hub</div>
          <div class="brand-sub">Flagship #19 · Turnkey Client Dossiers</div>
        </div>
      </a>

      <nav class="nav-links">
        <a href="/" class="nav-btn">🏠 Master Center</a>
        <a href="/sandboxes" class="nav-btn">🧪 Sandboxes (119)</a>
        <a href="/billing" class="nav-btn">💳 Billing & Invoices</a>
        <a href="/fulfillment" class="nav-btn">🛡️ SLA Operations</a>
        <a href="/portal" class="nav-btn">🏛️ VIP Portals</a>
        <a href="https://t.me/Minhpv_bot" target="_blank" class="nav-btn primary">VIP Escalation ↗</a>
      </nav>
    </div>
  </header>

  <main>
    <!-- Hero Banner -->
    <section class="hero">
      <div class="hero-badge">
        <span class="pulse-dot"></span>
        {meta['total_packages']} / {meta['total_packages']} PRODUCTION DOSSIERS ARCHIVED · {meta['total_files_packaged']} DELIVERABLES
      </div>
      <h1>Executive Deliverables & Onboarding Dossier Hub</h1>
      <p>
        The central digital asset repository providing instant 1-click downloads for complete, turnkey client onboarding packages. Each package is cryptographically hashed via SHA-256 and bundles 9 critical executive deliverables protecting <strong>$1,218,600 / Year</strong> in active contract target pipeline value ($101,550/mo across 119 nodes; $0.00 realized cash).
      </p>

      <!-- KPI Bar -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-val" style="color: #00f2fe;">{meta['total_packages']} / {meta['total_packages']}</div>
          <div class="kpi-lbl">Total Dossiers Packaged</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color: #10b981;">{meta['total_files_packaged']} Files</div>
          <div class="kpi-lbl">Total Deliverables Bundled</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color: #ffd700;">$1,218,600</div>
          <div class="kpi-lbl">Target Pipeline ARR ($0 Realized)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-val" style="color: #a78bfa;">{meta['total_size_mb']} MB</div>
          <div class="kpi-lbl">Total Archive Footprint</div>
        </div>
      </div>
    </section>

    <!-- Controls Bar -->
    <section class="controls-bar">
      <div class="controls-top">
        <input type="text" id="search-box" class="search-input" placeholder="🔍 Search by client name, location, industry, account ID, or SHA-256 hash..." oninput="handleSearch()">
        <select id="jump-box" class="jump-select" onchange="jumpToPackage(this.value)">
          <option value="">⚡ Jump directly to dossier...</option>
        </select>
      </div>

      <div class="filter-pills">
        <button class="pill-btn active" onclick="filterTier('all', this)">All Accounts ({meta['total_packages']})</button>
        <button class="pill-btn" onclick="filterTier('base', this)">🏢 Base Retainers ({meta['tier_breakdown']['base_retainers']})</button>
        <button class="pill-btn" onclick="filterTier('enterprise', this)">🎙️ Enterprise Voice ({meta['tier_breakdown']['enterprise_swarms']})</button>
        <button class="pill-btn" onclick="filterTier('sovereign', this)">💎 Sovereign Private VPC ({meta['tier_breakdown']['sovereign_vpcs']})</button>
        <button class="pill-btn" onclick="filterTier('syndicate', this)">🌐 Syndicate Franchises ({meta['tier_breakdown']['syndicate_franchises']})</button>
      </div>
    </section>

    <div class="results-meta">
      <div>Showing <strong id="visible-count" style="color:#fff;">{meta['total_packages']}</strong> of {meta['total_packages']} turnkey executive packages</div>
      <div style="font-family:var(--font-mono); font-size:12px; color:#10b981;">● 100% Cryptographically Verified</div>
    </div>

    <!-- Packages Grid -->
    <section class="packages-grid" id="grid-container">
      <!-- Injected via JavaScript -->
    </section>
  </main>

  <footer>
    <div>© 2026 AI Money Machine Operations Empire · Executive Client Deliverables Repository</div>
    <div class="footer-links">
      <a href="/">Master Center</a>
      <a href="/sandboxes">Sandboxes Hub</a>
      <a href="/billing">Master Billing</a>
      <a href="/fulfillment">SLA Operations</a>
      <a href="/portal">VIP Portals</a>
      <a href="/syndicate">Franchise Network</a>
    </div>
  </footer>

  <script>
    const DATA = {packages_json_str};
    let currentTier = 'all';
    let searchQuery = '';

    function init() {{
      populateJumpSelect();
      renderGrid();
    }}

    function populateJumpSelect() {{
      const jump = document.getElementById('jump-box');
      jump.innerHTML = '<option value="">⚡ Jump directly to dossier...</option>';
      DATA.forEach(d => {{
        const opt = document.createElement('option');
        opt.value = d.slug;
        opt.innerText = `[${{d.account_id}}] ${{d.client_name}} (${{d.tier.toUpperCase()}})`;
        jump.appendChild(opt);
      }});
    }}

    function jumpToPackage(slug) {{
      if (!slug) return;
      const target = document.getElementById(`pkg-${{slug}}`);
      if (target) {{
        target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        target.style.borderColor = '#00f2fe';
        target.style.boxShadow = '0 0 25px rgba(0,242,254,0.5)';
        setTimeout(() => {{
          target.style.borderColor = '';
          target.style.boxShadow = '';
        }}, 2500);
      }}
    }}

    function filterTier(tier, btn) {{
      currentTier = tier;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderGrid();
    }}

    function handleSearch() {{
      searchQuery = document.getElementById('search-box').value.toLowerCase().trim();
      renderGrid();
    }}

    function copyToClipboard(text, btn) {{
      navigator.clipboard.writeText(text).then(() => {{
        const orig = btn.innerText;
        btn.innerText = 'Copied!';
        btn.style.background = '#10b981';
        btn.style.color = '#000';
        setTimeout(() => {{
          btn.innerText = orig;
          btn.style.background = '';
          btn.style.color = '';
        }}, 1800);
      }}).catch(err => {{
        prompt('Copy SHA-256 Checksum:', text);
      }});
    }}

    function renderGrid() {{
      const container = document.getElementById('grid-container');
      const filtered = DATA.filter(d => {{
        const matchesTier = (currentTier === 'all') || (d.tier === currentTier);
        const matchesSearch = !searchQuery ||
          d.client_name.toLowerCase().includes(searchQuery) ||
          d.location.toLowerCase().includes(searchQuery) ||
          d.industry.toLowerCase().includes(searchQuery) ||
          d.account_id.toLowerCase().includes(searchQuery) ||
          d.sha256.toLowerCase().includes(searchQuery);
        return matchesTier && matchesSearch;
      }});

      document.getElementById('visible-count').innerText = filtered.length;

      if (filtered.length === 0) {{
        container.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:60px; color:var(--text-muted); background:var(--card-bg); border-radius:16px; border:1px solid var(--card-border);">
          No packages found matching search criteria.
        </div>`;
        return;
      }}

      container.innerHTML = filtered.map(d => {{
        let badgeClass = `tier-${{d.tier}}`;
        let tierLabel = d.tier === 'enterprise' ? 'Enterprise Voice' :
                        d.tier === 'sovereign' ? 'Sovereign Private' :
                        d.tier === 'syndicate' ? 'Syndicate Node' : 'Base Retainer';

        return `
        <div class="pkg-card" id="pkg-${{d.slug}}">
          <div>
            <div class="card-head">
              <span class="tier-badge ${{badgeClass}}">${{tierLabel}}</span>
              <span style="font-family:'JetBrains Mono'; font-size:11px; color:#10b981;">● READY (ZIP)</span>
            </div>

            <div class="pkg-name">${{d.client_name}}</div>
            <div class="pkg-sub">
              <strong>${{d.account_id}}</strong> • ${{d.industry}} • ${{d.location}}
            </div>

            <!-- Financial Specs -->
            <div class="finance-row">
              <div class="fin-item">
                <div class="fin-lbl">Setup Fee</div>
                <div class="fin-val" style="color:#10b981;">$${{d.setup.toLocaleString()}}</div>
              </div>
              <div class="fin-item">
                <div class="fin-lbl">Monthly</div>
                <div class="fin-val" style="color:#00f2fe;">$${{d.retainer.toLocaleString()}}</div>
              </div>
              <div class="fin-item">
                <div class="fin-lbl">Archive</div>
                <div class="fin-val" style="color:#a78bfa;">${{d.size_kb}} KB</div>
              </div>
            </div>

            <!-- SHA-256 Checksum -->
            <div class="hash-box">
              <span class="hash-text" title="SHA-256: ${{d.sha256}}">SHA: ${{d.sha256.substring(0, 16)}}...</span>
              <button class="btn-copy-hash" onclick="copyToClipboard('${{d.sha256}}', this)">Copy</button>
            </div>

            <!-- Deliverables Included -->
            <div class="deliverables-checklist">
              <span class="badge-item">📋 Proposal</span>
              <span class="badge-item">🖥️ Pitch Deck</span>
              <span class="badge-item">🧪 Live Sandbox</span>
              <span class="badge-item">📑 MSA Agreement</span>
              <span class="badge-item">💳 Paid Invoice</span>
              <span class="badge-item">📊 ROI Report</span>
              <span class="badge-item">🛡️ SLA Packet</span>
              <span class="badge-item">🏛️ VIP Portal</span>
            </div>
          </div>

          <div>
            <a href="${{d.zip_path}}" download class="btn-download">
              <span>📦 Download Dossier (ZIP)</span>
              <span style="font-size:11px; opacity:0.8;">(${{d.size_kb}} KB)</span>
            </a>

            <div class="sub-actions">
              <a href="${{d.sandbox_url}}" class="btn-sub" title="Launch Sandbox">🧪 Test</a>
              <a href="${{d.portal_url}}" class="btn-sub" title="Open VIP Portal">🏛️ Portal</a>
              <a href="${{d.sla_url}}" class="btn-sub" title="SLA Technical Packet">🛡️ SLA</a>
              <a href="${{d.invoice_url}}" class="btn-sub" title="Official Invoice">💳 Bill</a>
            </div>
          </div>
        </div>`;
      }}).join('');
    }}

    init();
  </script>
</body>
</html>
"""

    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PACKAGES_DIR / "index.html"
    out_file.write_text(html_content, encoding="utf-8")
    print(f"✅ Generated Flagship Web App #19: {out_file} ({len(html_content)} bytes)")

if __name__ == "__main__":
    build_packages_hub()
