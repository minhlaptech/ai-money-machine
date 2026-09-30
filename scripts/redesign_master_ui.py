import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
index_path = ROOT / "index.html"
html = index_path.read_text(encoding="utf-8")

# 1. ENHANCED CSS
new_css = """    /* Enhanced Status Bar & Dropdown Navigation */
    .system-status-bar {
      display: flex; align-items: center; gap: 8px; flex-wrap: nowrap;
    }
    .status-chip {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 6px 12px; border-radius: 20px; font-size: 11.5px; font-weight: 600;
      text-decoration: none; transition: all 0.2s ease;
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: var(--text); white-space: nowrap;
    }
    .status-chip:hover {
      background: rgba(255, 255, 255, 0.08); transform: translateY(-1px);
    }
    .chip-revenue {
      background: rgba(0, 230, 118, 0.08); border-color: rgba(0, 230, 118, 0.3); color: #fff;
    }
    .dot-green {
      width: 7px; height: 7px; border-radius: 50%; background: var(--green);
      box-shadow: 0 0 8px var(--green); display: inline-block;
    }
    .highlight-green { color: var(--green); font-family: var(--font-mono); font-weight: 700; }
    .highlight-cyan { color: var(--cyan); font-family: var(--font-mono); font-weight: 700; }
    .highlight-purple { color: #c084fc; font-family: var(--font-mono); font-weight: 700; }
    
    /* 27 Flagship Hubs Dropdown Trigger & Menu */
    .dropdown-wrapper { position: relative; }
    .btn-hub-toggle {
      display: inline-flex; align-items: center; gap: 8px;
      background: linear-gradient(135deg, rgba(124, 92, 252, 0.25), rgba(0, 242, 254, 0.25));
      border: 1px solid rgba(124, 92, 252, 0.5); color: #fff;
      padding: 7px 15px; border-radius: 20px; font-size: 12px; font-weight: 700;
      cursor: pointer; transition: all 0.2s ease; white-space: nowrap;
    }
    .btn-hub-toggle:hover {
      background: linear-gradient(135deg, rgba(124, 92, 252, 0.4), rgba(0, 242, 254, 0.4));
      box-shadow: 0 0 15px rgba(0, 242, 254, 0.25);
    }
    .dropdown-caret { font-size: 10px; transition: transform 0.2s ease; display: inline-block; }
    .dropdown-caret.open { transform: rotate(180deg); }
    
    .hub-dropdown-menu {
      position: absolute; top: calc(100% + 12px); right: 0;
      width: 940px; max-width: 95vw; max-height: 82vh; overflow-y: auto;
      background: rgba(10, 10, 24, 0.97); backdrop-filter: blur(28px);
      border: 1px solid rgba(124, 92, 252, 0.35); border-radius: 18px;
      padding: 22px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85);
      display: none; z-index: 1000;
    }
    .hub-dropdown-menu.show { display: block; animation: dropFade 0.2s ease-out; }
    @keyframes dropFade { from { opacity: 0; transform: translateY(-8px); } to { opacity: 1; transform: translateY(0); } }
    
    .dropdown-header {
      border-bottom: 1px solid var(--border); padding-bottom: 14px; margin-bottom: 16px;
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    }
    .dropdown-header h4 { font-family: 'Outfit'; font-size: 16px; color: #fff; font-weight: 700; }
    .dropdown-sub { font-size: 11px; color: var(--cyan); font-family: var(--font-mono); }
    
    .dropdown-grid {
      display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
    }
    @media (max-width: 860px) {
      .dropdown-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 520px) {
      .dropdown-grid { grid-template-columns: 1fr; }
    }
    .dropdown-col { display: flex; flex-direction: column; gap: 6px; }
    .col-title {
      font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px;
      color: var(--text-muted); font-weight: 700; margin-bottom: 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 4px;
    }
    .dropdown-item {
      display: flex; justify-content: space-between; align-items: center;
      padding: 6px 9px; border-radius: 8px; text-decoration: none;
      font-size: 11.5px; color: #d0d0ee; background: rgba(255, 255, 255, 0.02);
      border: 1px solid transparent; transition: all 0.15s ease;
    }
    .dropdown-item:hover {
      background: rgba(124, 92, 252, 0.15); border-color: rgba(124, 92, 252, 0.3);
      color: #fff; transform: translateX(3px);
    }
    .tag-pill {
      font-size: 10px; padding: 2px 6px; border-radius: 6px;
      background: rgba(255, 255, 255, 0.07); color: var(--cyan); font-family: var(--font-mono);
    }

    /* Top KPI Cards Styling */
    .card-real-revenue {
      border-color: rgba(0, 230, 118, 0.45) !important;
      background: linear-gradient(180deg, rgba(0, 230, 118, 0.08) 0%, rgba(18, 18, 36, 0.85) 100%) !important;
      box-shadow: 0 4px 20px rgba(0, 230, 118, 0.1);
    }
    .metric-header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
    .metric-badge-real {
      font-size: 11px; font-weight: 800; letter-spacing: 1px; color: var(--green); text-transform: uppercase;
    }
    .metric-gateway-live {
      font-size: 10px; background: rgba(0, 230, 118, 0.15); color: var(--green);
      padding: 2px 7px; border-radius: 10px; font-weight: 600;
    }
    .text-real-cash { color: #00e676 !important; font-size: 32px !important; }
    .text-emerald { color: var(--green); }
    .text-cyan { color: var(--cyan); }
    .text-gold { color: #ffd700; }
    .text-muted-sub { color: var(--text-muted); }

    /* SaaS Section Interactive Filter & Search Header */
    .saas-section-header {
      display: flex; justify-content: space-between; align-items: flex-end;
      flex-wrap: wrap; gap: 16px; margin: 36px 0 16px;
    }
    .saas-search-wrap {
      flex: 1; max-width: 380px; min-width: 260px;
    }
    #saas-search-input {
      width: 100%; background: rgba(18, 18, 36, 0.8); border: 1px solid var(--border);
      border-radius: 12px; padding: 11px 16px; color: #fff; font-size: 13px;
      font-family: 'Inter', sans-serif; transition: all 0.2s ease;
    }
    #saas-search-input:focus {
      outline: none; border-color: var(--cyan);
      box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);
    }
    
    .saas-filter-bar {
      display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 22px;
    }
    .saas-filter-btn {
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: var(--text-muted); font-size: 12px; font-weight: 600;
      padding: 7px 16px; border-radius: 20px; cursor: pointer;
      transition: all 0.2s ease;
    }
    .saas-filter-btn:hover {
      background: rgba(255, 255, 255, 0.08); color: #fff;
    }
    .saas-filter-btn.active {
      background: linear-gradient(135deg, var(--accent), var(--cyan));
      border-color: transparent; color: #000; font-weight: 700;
      box-shadow: 0 2px 10px rgba(0, 242, 254, 0.3);
    }
    
    /* Launcher Tabs Scrollable Enhancement */
    .launcher-tabs {
      display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 1px solid var(--border);
      padding-bottom: 12px; overflow-x: auto; white-space: nowrap;
      scrollbar-width: thin; scrollbar-color: var(--border) transparent;
    }
    .launcher-tabs::-webkit-scrollbar { height: 6px; }
    .launcher-tabs::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
"""

# Insert new CSS before </style>
html = html.replace("  </style>", new_css + "\n  </style>")

# 2. NEW HEADER & TOP BAR
new_header = """  <header>
    <div class="brand-wrap">
      <div class="logo-badge">⚡</div>
      <div class="brand-text">
        <h1>AI MONEY MACHINE</h1>
        <span>EXECUTIVE COMMAND CENTER · v3.2</span>
      </div>
    </div>
    
    <div class="system-status-bar">
      <!-- Real Cash Realized Badge -->
      <div class="status-chip chip-revenue" title="Doanh thu thực thu thanh toán qua cổng Lemon Squeezy">
        <span class="dot-green"></span>
        <span>Thực Thu:</span>
        <span class="highlight-green">$0.00</span>
      </div>
      
      <!-- Catalog Ready Badge -->
      <a href="/tools" target="_blank" class="status-chip" title="13 Sản phẩm đã sẵn sàng bán hàng trực tiếp">
        <span>🛍️</span>
        <span>Catalog:</span>
        <span class="highlight-cyan">13 SP</span>
      </a>

      <!-- Blueprints Sandbox Badge -->
      <a href="/sandboxes" target="_blank" class="status-chip" title="95 Hạ tầng đối tác doanh nghiệp ($83,550/mo Pipeline Target)">
        <span>🧪</span>
        <span>Khách Hàng:</span>
        <span class="highlight-purple">95 Nodes</span>
      </a>

      <!-- Cloud Systems Badge -->
      <a href="/telemetry" target="_blank" class="status-chip" title="29/29 Hệ thống Cloud đang hoạt động trên Vercel Edge">
        <span class="pulse-dot"></span>
        <span style="color:var(--green);">29/29 Cloud Live</span>
      </a>

      <!-- 27 Flagship Hubs Dropdown Trigger -->
      <div class="dropdown-wrapper">
        <button id="btn-hub-menu" class="btn-hub-toggle" onclick="toggleHubDropdown(event)">
          <span>🏛️ 27 Flagship Hubs</span>
          <span id="caret-icon" class="dropdown-caret">▾</span>
        </button>
        <div id="flagships-dropdown" class="hub-dropdown-menu">
          <div class="dropdown-header">
            <h4>🏛️ 27 Production Web Applications & Command Centers</h4>
            <span class="dropdown-sub">100% Vercel Edge Live · Byte-for-byte Synchronized</span>
          </div>
          <div class="dropdown-grid">
            <!-- Col 1 -->
            <div class="dropdown-col">
              <div class="col-title">🛍️ Micro-SaaS & Products (6)</div>
              <a href="/tools" target="_blank" class="dropdown-item"><span>⚡ SaaS Suite Hub ($39)</span><span class="tag-pill">Pass</span></a>
              <a href="/synapsegeo" target="_blank" class="dropdown-item"><span>🌐 SynapseGEO v2.4</span><span class="tag-pill">AI SEO</span></a>
              <a href="/reviewgenius" target="_blank" class="dropdown-item"><span>⭐ ReviewGenius AI</span><span class="tag-pill">Reviews</span></a>
              <a href="/headlineiq" target="_blank" class="dropdown-item"><span>🔥 HeadlineIQ</span><span class="tag-pill">Viral CTR</span></a>
              <a href="/bundle" target="_blank" class="dropdown-item"><span>🎁 Empire Master Bundle</span><span class="tag-pill">$39</span></a>
              <a href="/merch" target="_blank" class="dropdown-item"><span>👕 Developer Merch Store</span><span class="tag-pill">6 POD</span></a>
            </div>
            <!-- Col 2 -->
            <div class="dropdown-col">
              <div class="col-title">🏢 Client Ops & Retainers (7)</div>
              <a href="/portal" target="_blank" class="dropdown-item"><span>🏛️ VIP Client Portals Hub</span><span class="tag-pill">95 Portals</span></a>
              <a href="/onboarding" target="_blank" class="dropdown-item"><span>📋 VIP Onboarding Intake</span><span class="tag-pill">48h SLA</span></a>
              <a href="/syndicate" target="_blank" class="dropdown-item"><span>🌐 AI Syndicate Franchise</span><span class="tag-pill">12 Terr</span></a>
              <a href="/fulfillment" target="_blank" class="dropdown-item"><span>🛡️ Autonomous Ops & SLA</span><span class="tag-pill">95 Clusters</span></a>
              <a href="/billing" target="_blank" class="dropdown-item"><span>🧾 Master Billing Center</span><span class="tag-pill">Invoices</span></a>
              <a href="/packages" target="_blank" class="dropdown-item"><span>📦 Deliverables & Dossiers</span><span class="tag-pill">95 ZIPs</span></a>
              <a href="/pitches" target="_blank" class="dropdown-item"><span>🎯 Sales Pitch Decks Hub</span><span class="tag-pill">60 Decks</span></a>
            </div>
            <!-- Col 3 -->
            <div class="dropdown-col">
              <div class="col-title">⚖️ Compliance, SLA & Trust (6)</div>
              <a href="/trust" target="_blank" class="dropdown-item"><span>🛡️ Security & Trust Center</span><span class="tag-pill">SOC2/HIPAA</span></a>
              <a href="/guarantee" target="_blank" class="dropdown-item"><span>⚖️ SLA Financial Guarantee</span><span class="tag-pill">99.9% Credit</span></a>
              <a href="/benchmarks" target="_blank" class="dropdown-item"><span>📊 AI Performance Index</span><span class="tag-pill">Quartiles</span></a>
              <a href="/attribution" target="_blank" class="dropdown-item"><span>📈 Value Attribution Engine</span><span class="tag-pill">CFO ROI</span></a>
              <a href="/calculator" target="_blank" class="dropdown-item"><span>🧮 AI Revenue Calculator</span><span class="tag-pill">Audit Tool</span></a>
              <a href="/docs" target="_blank" class="dropdown-item"><span>⚡ Developer Docs & API</span><span class="tag-pill">OpenAPI 3.1</span></a>
            </div>
            <!-- Col 4 -->
            <div class="dropdown-col">
              <div class="col-title">📡 NOC, Dispatch & Studios (8)</div>
              <a href="/telemetry" target="_blank" class="dropdown-item"><span>📡 Global NOC & Telemetry</span><span class="tag-pill">Radar</span></a>
              <a href="/sandboxes" target="_blank" class="dropdown-item"><span>🧪 Autonomous Sandboxes</span><span class="tag-pill">95 Nodes</span></a>
              <a href="/knowledge" target="_blank" class="dropdown-item"><span>🧠 AI Agent Studio</span><span class="tag-pill">RAG Vector</span></a>
              <a href="/inbox" target="_blank" class="dropdown-item"><span>📥 Omnichannel Live Inbox</span><span class="tag-pill">HITL</span></a>
              <a href="/studio" target="_blank" class="dropdown-item"><span>🎬 AI Video Studio Hub</span><span class="tag-pill">40 MP4s</span></a>
              <a href="/freelance" target="_blank" class="dropdown-item"><span>💼 AI Freelance & Gigs Hub</span><span class="tag-pill">8 Gigs</span></a>
              <a href="/blog" target="_blank" class="dropdown-item"><span>📚 AI Resource Hub & Blog</span><span class="tag-pill">8 Guides</span></a>
              <a href="/referral" target="_blank" class="dropdown-item"><span>🤝 Partner & Affiliate Hub</span><span class="tag-pill">50% Rev</span></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>"""

# Replace existing <header>...</header>
header_pattern = re.compile(r'<header>.*?</header>', re.DOTALL)
html = header_pattern.sub(new_header, html)

# 3. NEW TOP KPI METRICS
new_metrics = """    <!-- Top KPI Cards: 100% Real Cash Earned & Verified Metrics -->
    <div class="metrics-grid">
      <div class="metric-card card-real-revenue">
        <div class="metric-header-row">
          <span class="metric-badge-real">DOANH THU THỰC TẾ</span>
          <span class="metric-gateway-live">🟢 Lemon Squeezy Live</span>
        </div>
        <div class="metric-val text-real-cash">$0.00</div>
        <div class="metric-sub text-emerald">
          <span>💳 Cổng thanh toán sẵn sàng (Store #485872)</span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Đơn Hàng Thực Thu</div>
        <div class="metric-val">0 Đơn Hàng</div>
        <div class="metric-sub text-muted-sub">
          <span>🎯 Đang mở bán 24/7 trực tiếp qua checkout tự động</span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Danh Mục Mở Bán (Catalog)</div>
        <div class="metric-val">13 Sản Phẩm</div>
        <div class="metric-sub text-cyan">
          <span>📦 6 SaaS ($9–$39) + 6 POD + 1 Empire Bundle</span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Hạ Tầng Khách Hàng (Pipeline)</div>
        <div class="metric-val">95 Workspaces</div>
        <div class="metric-sub text-gold">
          <span>💼 $83,550/tháng Pipeline mục tiêu (Chưa thu tiền)</span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-label">Trung Tâm Chỉ Huy Vận Hành</div>
        <div class="metric-val">27 Flagships · 29 Systems</div>
        <div class="metric-sub text-emerald">
          <span>🌐 100% Vercel Edge Live · 99.998% Uptime</span>
        </div>
      </div>
    </div>"""

# Replace metrics grid
metrics_pattern = re.compile(r'<!-- Top KPI Cards -->.*?</div>\s*</div>', re.DOTALL)
html = metrics_pattern.sub(new_metrics, html)

# 4. SAAS SECTION HEADER & INTERACTIVE FILTER
saas_header_new = """    <!-- Section Title & Interactive Category Filter Bar -->
    <div class="saas-section-header">
      <div>
        <h2 class="section-title" style="margin: 0 0 6px 0;">
          🛠️ 27 Flagship Web Applications & Command Centers
        </h2>
        <p style="font-size: 13px; color: var(--text-muted); margin: 0;">
          Tất cả ứng dụng web, công cụ Micro-SaaS và trung tâm điều hành đã kiểm thử và hoạt động trên Vercel Edge.
        </p>
      </div>

      <!-- Live Search Box -->
      <div class="saas-search-wrap">
        <input type="text" id="saas-search-input" placeholder="🔍 Tìm nhanh 27 web apps, công cụ..." oninput="filterSaasCards()">
      </div>
    </div>

    <!-- Category Filter Pills -->
    <div class="saas-filter-bar">
      <button class="saas-filter-btn active" onclick="filterSaasCategory('all', this)">🌟 Tất Cả (27)</button>
      <button class="saas-filter-btn" onclick="filterSaasCategory('products', this)">🛍️ SaaS & Sản Phẩm (6)</button>
      <button class="saas-filter-btn" onclick="filterSaasCategory('clients', this)">🏢 Khách Hàng & Vận Hành (7)</button>
      <button class="saas-filter-btn" onclick="filterSaasCategory('compliance', this)">⚖️ Tuân Thủ & Bảo Hành (6)</button>
      <button class="saas-filter-btn" onclick="filterSaasCategory('operations', this)">📡 NOC & Điều Phối (8)</button>
    </div>"""

# Replace SaaS section title
old_saas_title_pattern = re.compile(r'<!-- Live SaaS Products Grid -->\s*<h2 class="section-title">.*?</h2>', re.DOTALL)
html = old_saas_title_pattern.sub(saas_header_new, html)

# 5. ASSIGN DATA CATEGORIES TO SAAS CARDS
# List mapping keywords to category
categories_map = {
    "Autonomous Micro-SaaS Suite": ("products", "suite tools saas pass lifetime"),
    "SynapseGEO v2.4": ("products", "synapsegeo seo geo generative search"),
    "ReviewGenius AI": ("products", "review genius ai customer responder reviews"),
    "HeadlineIQ": ("products", "headline iq ctr viral clickability generator"),
    "SynapseGEO Chrome Extension": ("products", "extension chrome browser toolbar"),
    "The AI Empire Master Bundle": ("products", "bundle digital products ebook templates 39"),
    "AI & Developer Merch Store": ("products", "merch store apparel printify hoodies tees mugs"),
    
    "Executive Client VIP Portals Hub": ("clients", "vip portals clients 95 accounts enterprise"),
    "VIP Client Onboarding Intake Hub": ("clients", "onboarding intake client form 48h sla"),
    "AI Syndicate Franchise Network": ("clients", "syndicate franchise network 12 territories"),
    "Autonomous Operations & SLA Hub": ("clients", "operations sla fulfillment 95 clusters"),
    "Master Billing & Invoicing Center": ("clients", "billing invoicing msa contracts receipts"),
    "Executive Deliverables & Dossier Hub": ("clients", "dossiers packages zip deliverables 95 accounts"),
    "Interactive AI Chatbot Demo": ("clients", "chatbot demo client portfolio booking"),
    "Sales Pitch Decks Showcase Hub": ("clients", "pitches sales pitch decks presentations"),

    "Security & Trust Center Hub": ("compliance", "trust security compliance soc2 hipaa gdpr"),
    "SLA Incident Response & Financial Guarantee Center": ("compliance", "guarantee sla refund downtime credits incident"),
    "AI Performance & Benchmark Index Hub": ("compliance", "benchmarks speed to lead conversion roi index"),
    "Client Value Realization & Financial Attribution Engine": ("compliance", "attribution roi ledger cfo financial value"),
    "AI Revenue Recovery Calculator": ("compliance", "calculator roi lost revenue simulator"),
    "Developer Documentation & API Hub": ("compliance", "docs api openapi 3.1 developer reference"),

    "Global AI Network Operations Center (NOC)": ("operations", "telemetry noc radar uptime edge ping"),
    "Autonomous Sandbox & Simulation Hub": ("operations", "sandboxes simulation testing uat accounts"),
    "Self-Service Knowledge Base & AI Agent Studio": ("operations", "knowledge agent studio rag vector pdf faq"),
    "Omnichannel Unified Inbox & AI Human-in-the-Loop Dispatch": ("operations", "inbox conversations unified hitl dispatch sms whatsapp"),
    "AI Media & Video Studio Hub": ("operations", "studio video youtube mp4 faceless media"),
    "AI Freelance & Agency Hub": ("operations", "freelance agency gigs upwork fiverr"),
    "AI Resource Hub & Blog": ("operations", "blog resource hub guides ebooks leads"),
    "Affiliate & Partner Program Hub": ("operations", "referral affiliate partners 50 revshare")
}

for title, (cat, kw) in categories_map.items():
    # Find card containing title and add data attributes
    pattern = rf'(<div class="saas-card"[^>]*)(>[\s\S]*?<h3>{re.escape(title)}</h3>)'
    repl = rf'\1 data-category="{cat}" data-keywords="{kw}"\2'
    html = re.sub(pattern, repl, html, count=1)

# 6. ADD JAVASCRIPT FOR DROPDOWN, SEARCH & FILTER
js_snippet = """
    // Hubs Dropdown Toggle
    function toggleHubDropdown(e) {
      if (e) e.stopPropagation();
      const menu = document.getElementById('flagships-dropdown');
      const caret = document.getElementById('caret-icon');
      if (menu) {
        menu.classList.toggle('show');
        if (caret) caret.classList.toggle('open');
      }
    }
    document.addEventListener('click', function(e) {
      const menu = document.getElementById('flagships-dropdown');
      const btn = document.getElementById('btn-hub-menu');
      if (menu && menu.classList.contains('show')) {
        if (!menu.contains(e.target) && !btn.contains(e.target)) {
          menu.classList.remove('show');
          const caret = document.getElementById('caret-icon');
          if (caret) caret.classList.remove('open');
        }
      }
    });

    // SaaS Category & Search Filtering
    let currentSaasCategory = 'all';
    function filterSaasCategory(cat, btn) {
      currentSaasCategory = cat;
      document.querySelectorAll('.saas-filter-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      filterSaasCards();
    }

    function filterSaasCards() {
      const searchVal = (document.getElementById('saas-search-input')?.value || '').toLowerCase().trim();
      const cards = document.querySelectorAll('.saas-card');
      cards.forEach(card => {
        const cat = card.getAttribute('data-category') || 'all';
        const kw = (card.getAttribute('data-keywords') || '').toLowerCase();
        const text = card.innerText.toLowerCase();
        
        const matchesCategory = (currentSaasCategory === 'all' || cat === currentSaasCategory);
        const matchesSearch = !searchVal || kw.includes(searchVal) || text.includes(searchVal);
        
        if (matchesCategory && matchesSearch) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }
"""

html = html.replace("window.addEventListener('DOMContentLoaded', renderLeadsTable);", 
                    "window.addEventListener('DOMContentLoaded', () => { renderLeadsTable(); });\n" + js_snippet)

# 7. CORRECT SIMULATED MONEY TEXT IN TABS
html = html.replace(
    '<div style="font-size:20px; font-weight:800; color:#fff;">$1,002,600 / yr <span style="font-size:13px; color:#4ade80;">($83,550/mo)</span></div>',
    '<div style="font-size:16px; font-weight:800; color:#fff;">Thực Thu: <span style="color:#00e676;">$0.00</span> · <span style="font-size:12px; color:#ffd700;">Target Pipeline: $83,550/mo ($1.00M ARR)</span></div>'
)
html = html.replace(
    '<div style="font-size:13px; color:#4ade80;">$260,600 Cash + $83,550/mo</div>',
    '<div style="font-size:13px; color:#00e676;">Thực Thu: $0.00 <span style="color:var(--text-muted);">(Pipeline: $83,550/mo)</span></div>'
)
html = html.replace(
    '<div style="font-size:18px; font-weight:700; color:#ffd700;">${wonC} ($260,600 + $83,550/mo)</div>',
    '<div style="font-size:16px; font-weight:700; color:#ffd700;">${wonC} Frameworks <span style="font-size:12px; color:#94a3b8;">($83,550/mo Target)</span></div>'
)

index_path.write_text(html, encoding="utf-8")
print("Successfully redesigned index.html!")
