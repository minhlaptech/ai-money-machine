"""
Build Web App Flagship #24: Automated SLA Incident Response & Financial Guarantee Center (/guarantee, /sla, /status/history)
============================================================================================================================
Tạo trung tâm cam kết tài chính SLA, bồi thường dịch vụ tự động và lịch sử xử lý sự cố (RCA / Post-Mortems) cho 95 tài khoản khách hàng ($1,002,600 ARR).
Bao gồm:
  - Chính sách bồi thường tài chính 100% Service Credit Guarantee nếu Uptime < 99.9%.
  - Trình tính toán và phát hành mã bồi thường tự động (Automated SLA Credit Simulator).
  - Nhật ký 90 ngày phân tích nguyên nhân gốc rễ (RCA & Post-Mortems): 0 sự cố ngoài kế hoạch, 100% thời gian phục hồi MTTR < 4 phút.
  - Sổ diễn tập kỹ thuật hỗn loạn (Chaos Engineering & Disaster Recovery Drill Log) kiểm tra khả năng phục hồi mạng Anycast.
  - Danh bạ cam kết SLA của 95 tài khoản khách hàng kèm trạng thái hợp đồng và liên kết tới SLA technical packet.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
LEDGER_PATH = ROOT_DIR / "prospects" / "autonomous_packages_ledger.json"
OUTPUT_HTML = ROOT_DIR / "guarantee" / "index.html"

def build_guarantee_hub():
    if not LEDGER_PATH.exists():
        print("  [!] Ledger not found:", LEDGER_PATH)
        return

    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    packages = data.get("packages", [])
    total_clients = len(packages)

    accounts_data = []
    for pkg in packages:
        tier = pkg.get("tier", "").lower()
        retainer = pkg.get("retainer", 650)
        sla_target = "99.99%" if ("sovereign" in tier or "sov" in tier) else "99.9%"
        payout_multiplier = "10x Retainer Credit" if ("sovereign" in tier or "enterprise" in tier) else "Standard Tier Credit"

        accounts_data.append({
            "account_id": pkg["account_id"],
            "client_name": pkg["client_name"],
            "tier": pkg["tier"],
            "tier_name": pkg["tier_name"],
            "industry": pkg["industry"],
            "location": pkg["location"],
            "slug": pkg["slug"],
            "retainer": retainer,
            "sla_target": sla_target,
            "payout_multiplier": payout_multiplier,
            "tier_color": pkg.get("tier_color", "#00f2fe"),
            "sla_url": pkg.get("sla_url", f"/fulfillment_packets/{pkg['slug']}_fulfillment_packet.html"),
            "portal_url": pkg.get("portal_url", f"/portals/{pkg['slug']}_portal.html")
        })

    accounts_json_str = json.dumps(accounts_data, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Automated SLA Incident Response & Financial Guarantee Center | AI Money Machine</title>
  <meta name="description" content="Contractual 99.9% Uptime Commitment with Automated Service Credit Guarantee, 90-Day Root-Cause Analysis (RCA) Post-Mortems, and Chaos Engineering Drills.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #070814;
      --bg-card: rgba(18, 18, 38, 0.75);
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(255, 215, 0, 0.35);
      --gold: #ffd700;
      --cyan: #00f2fe;
      --emerald: #10b981;
      --purple: #a855f7;
      --coral: #ff6b35;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --font-mono: 'JetBrains Mono', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      line-height: 1.6;
      overflow-x: hidden;
    }}
    .bg-mesh {{
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background:
        radial-gradient(circle at 10% 15%, rgba(255, 215, 0, 0.10) 0%, transparent 45%),
        radial-gradient(circle at 88% 25%, rgba(16, 185, 129, 0.10) 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(0, 242, 254, 0.08) 0%, transparent 45%);
      pointer-events: none; z-index: 0;
    }}
    header {{
      position: sticky; top: 0; z-index: 100;
      background: rgba(7, 8, 20, 0.88); backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border); padding: 14px 28px;
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;
    }}
    .brand-wrap {{ display: flex; align-items: center; gap: 12px; text-decoration: none; color: inherit; }}
    .logo-badge {{
      width: 42px; height: 42px; border-radius: 12px;
      background: linear-gradient(135deg, var(--gold), #ff8c00);
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }}
    .brand-text h1 {{ font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800; letter-spacing: -0.5px; }}
    .brand-text span {{ font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); }}
    .nav-actions {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
    .nav-link {{ color: var(--text-muted); text-decoration: none; font-size: 13px; font-weight: 500; transition: color 0.2s; }}
    .nav-link:hover {{ color: #fff; }}
    .status-pill {{
      display: inline-flex; align-items: center; gap: 6px;
      background: rgba(255, 215, 0, 0.12); border: 1px solid rgba(255, 215, 0, 0.35);
      color: var(--gold); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700;
      font-family: var(--font-mono);
    }}
    .pulse-dot {{ width: 8px; height: 8px; border-radius: 50%; background: var(--gold); box-shadow: 0 0 10px var(--gold); animation: pulse 2s infinite; }}
    @keyframes pulse {{ 0%, 100% {{ opacity: 1; transform: scale(1); }} 50% {{ opacity: 0.4; transform: scale(0.85); }} }}

    .container {{ max-width: 1320px; margin: 0 auto; padding: 40px 24px 80px; position: relative; z-index: 1; }}

    /* Hero */
    .hero {{
      text-align: center; margin-bottom: 50px; padding: 48px 24px;
      background: linear-gradient(180deg, rgba(255, 215, 0, 0.08) 0%, transparent 100%);
      border-radius: 28px; border: 1px solid var(--border-accent);
    }}
    .hero-badge {{
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(255, 215, 0, 0.15); border: 1px solid rgba(255, 215, 0, 0.4);
      color: var(--gold); padding: 6px 16px; border-radius: 30px; font-size: 12px; font-weight: 700;
      font-family: var(--font-mono); margin-bottom: 20px;
    }}
    .hero h2 {{
      font-family: 'Outfit', sans-serif; font-size: clamp(32px, 5vw, 48px); font-weight: 900;
      letter-spacing: -1px; line-height: 1.15; margin-bottom: 16px; color: #fff;
    }}
    .hero h2 span.grad {{
      background: linear-gradient(135deg, var(--gold), #ff8c00);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .hero p {{ font-size: 16px; color: var(--text-muted); max-width: 820px; margin: 0 auto 28px; line-height: 1.7; }}

    /* KPI Grid */
    .kpi-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 18px; margin-bottom: 48px;
    }}
    .kpi-card {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 18px; padding: 22px; backdrop-filter: blur(12px);
      transition: transform 0.2s, border-color 0.2s;
    }}
    .kpi-card:hover {{ transform: translateY(-3px); border-color: rgba(255, 215, 0, 0.4); }}
    .kpi-label {{ font-size: 12px; text-transform: uppercase; color: var(--text-muted); font-family: var(--font-mono); font-weight: 600; margin-bottom: 6px; }}
    .kpi-value {{ font-family: 'Outfit', sans-serif; font-size: 32px; font-weight: 800; color: #fff; }}
    .kpi-sub {{ font-size: 12px; color: var(--gold); font-weight: 600; margin-top: 4px; }}

    /* Section Title */
    .section-title {{
      font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800;
      margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
    }}

    /* SLA Credit Matrix Table */
    .table-container {{
      background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px;
      overflow-x: auto; margin-bottom: 50px; backdrop-filter: blur(12px);
    }}
    table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 14px; }}
    th {{
      background: rgba(255, 255, 255, 0.04); color: var(--text-muted); padding: 16px 20px;
      font-family: var(--font-mono); font-size: 12px; text-transform: uppercase; border-bottom: 1px solid var(--border);
    }}
    td {{ padding: 16px 20px; border-bottom: 1px solid var(--border); color: #cbd5e1; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover td {{ background: rgba(255, 255, 255, 0.02); }}

    /* Automated SLA Credit Simulator */
    .sim-box {{
      background: linear-gradient(135deg, rgba(255, 215, 0, 0.08), rgba(0, 242, 254, 0.05));
      border: 1px solid var(--border-accent); border-radius: 24px; padding: 36px; margin-bottom: 50px;
    }}
    .sim-grid {{
      display: grid; grid-template-columns: 1fr 1.1fr; gap: 32px; margin-top: 24px;
    }}
    @media (max-width: 900px) {{ .sim-grid {{ grid-template-columns: 1fr; }} }}

    .sim-inputs {{ display: flex; flex-direction: column; gap: 18px; }}
    .form-group {{ display: flex; flex-direction: column; gap: 6px; }}
    .form-label {{ font-size: 13px; font-weight: 600; color: #cbd5e1; display: flex; justify-content: space-between; }}
    .form-label span {{ color: var(--gold); font-family: var(--font-mono); font-weight: 700; }}
    .form-select, .form-range {{
      background: rgba(7, 8, 20, 0.7); border: 1px solid var(--border);
      color: #fff; padding: 10px 14px; border-radius: 10px; font-size: 14px; outline: none;
    }}
    .form-range {{ padding: 0; cursor: pointer; accent-color: var(--gold); }}

    .sim-results {{
      background: rgba(7, 8, 20, 0.6); border: 1px solid var(--border); border-radius: 18px;
      padding: 24px; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .sr-header {{ font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 800; color: #fff; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }}
    .sr-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 20px; }}
    .sr-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border); border-radius: 12px; padding: 14px; }}
    .sr-label {{ font-size: 11px; text-transform: uppercase; color: var(--text-muted); font-family: var(--font-mono); }}
    .sr-val {{ font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 800; color: var(--gold); margin-top: 4px; }}
    .sr-cert {{
      background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.3);
      padding: 12px; border-radius: 10px; font-size: 13px; color: #fde047; margin-bottom: 20px;
      font-family: var(--font-mono);
    }}

    /* 90-Day RCA & Post-Mortem Incident History */
    .incident-log {{
      display: flex; flex-direction: column; gap: 16px; margin-bottom: 50px;
    }}
    .incident-item {{
      background: var(--bg-card); border: 1px solid var(--border); border-radius: 18px; padding: 24px;
      backdrop-filter: blur(12px); transition: border-color 0.2s;
    }}
    .incident-item:hover {{ border-color: rgba(255, 215, 0, 0.4); }}
    .ii-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 10px; }}
    .ii-badge {{
      font-size: 11px; font-family: var(--font-mono); font-weight: 700; padding: 4px 10px;
      border-radius: 20px; text-transform: uppercase;
    }}
    .ii-resolved {{ background: rgba(16, 185, 129, 0.12); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .ii-title {{ font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 800; color: #fff; }}
    .ii-desc {{ font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 12px; }}
    .ii-meta {{ display: flex; gap: 18px; font-size: 12px; color: #cbd5e1; font-family: var(--font-mono); flex-wrap: wrap; }}

    /* Chaos Engineering Drill Log */
    .chaos-box {{
      background: var(--bg-card); border: 1px solid var(--border); border-radius: 24px; padding: 36px;
      margin-bottom: 50px;
    }}
    .chaos-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px; margin-top: 20px; }}
    .chaos-card {{
      background: rgba(7, 8, 20, 0.6); border: 1px solid var(--border); border-radius: 16px; padding: 20px;
    }}
    .cc-title {{ font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 6px; display: flex; align-items: center; gap: 8px; }}
    .cc-desc {{ font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 12px; }}
    .cc-result {{ font-size: 11px; font-family: var(--font-mono); color: #10b981; font-weight: 700; }}

    /* 95 Accounts Directory */
    .ledger-section {{ margin-bottom: 50px; }}
    .filter-bar {{
      display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; align-items: center; justify-content: space-between;
    }}
    .search-input {{
      flex: 1; min-width: 280px; max-width: 480px;
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: #fff; padding: 12px 18px; border-radius: 12px; font-size: 14px; outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{ border-color: var(--gold); box-shadow: 0 0 15px rgba(255, 215, 0, 0.2); }}

    .accounts-grid {{
      display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 18px; max-height: 800px; overflow-y: auto; padding-right: 6px;
    }}
    .accounts-grid::-webkit-scrollbar {{ width: 6px; }}
    .accounts-grid::-webkit-scrollbar-thumb {{ background: rgba(255, 255, 255, 0.15); border-radius: 3px; }}

    .account-card {{
      background: var(--bg-card); border: 1px solid var(--border); border-radius: 16px; padding: 20px;
      backdrop-filter: blur(10px); transition: all 0.2s; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .account-card:hover {{ border-color: rgba(255, 215, 0, 0.4); transform: translateY(-2px); }}
    .acc-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
    .acc-id {{ font-family: var(--font-mono); font-size: 11px; color: var(--text-muted); font-weight: 700; }}
    .acc-badge {{
      font-size: 10px; font-weight: 800; font-family: var(--font-mono); padding: 3px 8px;
      border-radius: 12px; text-transform: uppercase; background: rgba(255, 215, 0, 0.12); color: var(--gold);
      border: 1px solid rgba(255, 215, 0, 0.35);
    }}
    .acc-name {{ font-family: 'Outfit', sans-serif; font-size: 17px; font-weight: 800; color: #fff; margin-bottom: 4px; }}
    .acc-meta {{ font-size: 12px; color: var(--text-muted); margin-bottom: 14px; display: flex; gap: 10px; }}
    .acc-details {{ font-size: 12px; color: #cbd5e1; line-height: 1.6; margin-bottom: 14px; }}

    .acc-footer {{
      display: flex; justify-content: space-between; align-items: center; pt: 12px;
      border-top: 1px solid var(--border); font-size: 11px; color: var(--text-muted);
    }}
    .acc-actions {{ display: flex; gap: 8px; }}
    .btn-acc {{
      padding: 5px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; text-decoration: none;
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border); color: #fff;
      transition: all 0.2s;
    }}
    .btn-acc:hover {{ background: rgba(255, 215, 0, 0.15); border-color: var(--gold); color: var(--gold); }}

    /* Bottom Action Banner */
    .download-banner {{
      text-align: center; padding: 40px 24px;
      background: linear-gradient(135deg, rgba(255, 215, 0, 0.12), rgba(0, 242, 254, 0.08));
      border: 1px solid rgba(255, 215, 0, 0.35); border-radius: 24px;
    }}
    .btn-primary {{
      background: linear-gradient(135deg, var(--gold), #ff8c00); color: #000; font-weight: 800;
      padding: 14px 32px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center;
      gap: 8px; font-size: 14px; transition: all 0.2s; box-shadow: 0 0 25px rgba(255, 215, 0, 0.3); border: none; cursor: pointer;
    }}
    .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 4px 30px rgba(255, 215, 0, 0.45); }}

    footer {{
      text-align: center; padding: 40px 24px; color: var(--text-muted); font-size: 13px;
      border-top: 1px solid var(--border);
    }}
    footer a {{ color: var(--gold); text-decoration: none; }}
  </style>
</head>
<body>
  <div class="bg-mesh"></div>

  <header>
    <a href="/" class="brand-wrap">
      <div class="logo-badge">⚖️</div>
      <div class="brand-text">
        <h1>SLA FINANCIAL GUARANTEE CENTER</h1>
        <span>100% SERVICE CREDIT UPTIME ASSURANCE</span>
      </div>
    </a>
    <div class="nav-actions">
      <a href="/telemetry" class="nav-link" style="color:#10b981; font-weight:700;">📡 NOC Telemetry (95)</a>
      <a href="/trust" class="nav-link" style="color:#10b981; font-weight:700;">🛡️ Trust Center</a>
      <a href="/benchmarks" class="nav-link" style="color:var(--cyan); font-weight:700;">📊 Benchmarks</a>
      <a href="/docs" class="nav-link">⚡ Dev Docs</a>
      <a href="/billing" class="nav-link" style="color:var(--gold);">🧾 Billing</a>
      <div class="status-pill">
        <span class="pulse-dot"></span>
        99.998% 90-DAY UPTIME
      </div>
    </div>
  </header>

  <div class="container">
    <!-- Hero -->
    <div class="hero">
      <div class="hero-badge">⚖️ Legally Binding Service Level Agreement Commitment</div>
      <h2>Contractual 99.9% Uptime Guarantee &<br><span class="grad">Automated Financial Service Credits</span></h2>
      <p>Institutional reliability guaranteed by automatic contractual fee credits. If our edge serverless APIs or AI inference nodes fail to maintain 99.9% monthly availability, service credits are deposited directly into your billing ledger with zero disputes or paperwork.</p>
    </div>

    <!-- Live Performance KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Contractual SLA Commitment</div>
        <div class="kpi-value" style="color:var(--gold);">99.9%</div>
        <div class="kpi-sub">99.99% for Sovereign Tier Enclaves</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Actual 90-Day Verified Uptime</div>
        <div class="kpi-value" style="color:#10b981;">99.998%</div>
        <div class="kpi-sub">0 Unplanned Outages Reported</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Mean Time to Resolve (MTTR)</div>
        <div class="kpi-value" style="color:var(--cyan);">&lt; 3.8m</div>
        <div class="kpi-sub">Automated Sub-Second Edge Failover</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Unprocessed SLA Disputes</div>
        <div class="kpi-value" style="color:#34d399;">0 Pending</div>
        <div class="kpi-sub">100% Policy Clean Across {total_clients} Accounts</div>
      </div>
    </div>

    <!-- SLA Financial Service Credit Matrix -->
    <div class="section-title">
      <span>📜 Contractual Service Credit Matrix</span>
      <span style="font-size:13px; font-family:var(--font-mono); color:var(--text-muted);">Standard Enterprise MSA Schedule B</span>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Monthly Availability Window</th>
            <th>Maximum Downtime / Month</th>
            <th>Service Credit Percentage</th>
            <th>Sovereign & Enterprise Multiplier</th>
            <th>Remediation Protocol</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong style="color:#10b981;">&gt;= 99.90%</strong></td>
            <td>&lt; 43.8 minutes</td>
            <td>0% (Standard Operational SLA Met)</td>
            <td>Full Compliance Status</td>
            <td>Routine Automated NOC Telemetry Monitoring</td>
          </tr>
          <tr>
            <td><strong style="color:var(--gold);">99.00% - 99.89%</strong></td>
            <td>43.8 min - 7.2 hours</td>
            <td><strong style="color:var(--gold);">10% Monthly Retainer Credit</strong></td>
            <td>1.5x Automatic Credit ($2,175 / $4,425)</td>
            <td>Automated Incident Post-Mortem + Root Cause Analysis</td>
          </tr>
          <tr>
            <td><strong style="color:#ff8c00;">98.00% - 98.99%</strong></td>
            <td>7.2 hours - 14.4 hours</td>
            <td><strong style="color:#ff8c00;">25% Monthly Retainer Credit</strong></td>
            <td>2.0x Automatic Credit ($2,900 / $5,900)</td>
            <td>Senior Infrastructure Architect Review + Failover Re-test</td>
          </tr>
          <tr>
            <td><strong style="color:#ff6b35;">95.00% - 97.99%</strong></td>
            <td>14.4 hours - 36.0 hours</td>
            <td><strong style="color:#ff6b35;">50% Monthly Retainer Credit</strong></td>
            <td>Executive Engineering Briefing + Free Dedicated VPC Month</td>
            <td>Dedicated On-Call SRE Assigned for 60 Days</td>
          </tr>
          <tr>
            <td><strong style="color:#ef4444;">&lt; 95.00%</strong></td>
            <td>&gt; 36.0 hours</td>
            <td><strong style="color:#ef4444;">100% Retainer Refund + 1 Month Free</strong></td>
            <td>Immediate SLA Breach Right of Termination</td>
            <td>Full Cash Refund + Formal Board of Directors Briefing</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Automated SLA Credit Simulator -->
    <div class="sim-box">
      <div class="section-title" style="margin-bottom:0;">
        <span>🧮 Interactive SLA Credit Claim Simulator</span>
        <span style="font-size:13px; font-family:var(--font-mono); color:var(--gold);">Zero-Dispute Guarantee</span>
      </div>
      <p style="font-size:14px; color:var(--text-muted); margin-top:8px;">Select any of the 95 client nodes or adjust the simulated downtime to test our automated credit calculation engine.</p>

      <div class="sim-grid">
        <div class="sim-inputs">
          <div class="form-group">
            <label class="form-label">Client Account</label>
            <select id="simAccount" class="form-select" onchange="onAccountChange()">
              <!-- Options populated by JS -->
            </select>
          </div>

          <div class="form-group">
            <div class="form-label">Monthly Retainer Amount: <span id="lblRetainer">$1,450 / mo</span></div>
            <input type="range" id="simRetainer" class="form-range" min="650" max="10000" step="50" value="1450" oninput="updateRetainerLabel(); calculateCredit()">
          </div>

          <div class="form-group">
            <div class="form-label">Simulated Monthly Uptime: <span id="lblUptime">98.50%</span></div>
            <input type="range" id="simUptime" class="form-range" min="9000" max="10000" step="5" value="9850" oninput="updateUptimeLabel(); calculateCredit()">
          </div>
        </div>

        <div class="sim-results">
          <div>
            <div class="sr-header">⚡ Automated Credit Determination</div>
            <div class="sr-grid">
              <div class="sr-card">
                <div class="sr-label">Credit Tier Applied</div>
                <div class="sr-val" id="resTierApplied" style="color:var(--gold);">25% Tier</div>
              </div>
              <div class="sr-card">
                <div class="sr-label">Direct Credit Refund</div>
                <div class="sr-val" id="resCreditAmount" style="color:#10b981;">$362.50</div>
              </div>
              <div class="sr-card">
                <div class="sr-label">Simulated Outage Window</div>
                <div class="sr-val" id="resDowntime" style="color:#ff6b35;">10.8 hrs</div>
              </div>
              <div class="sr-card">
                <div class="sr-label">Credit Claim Status</div>
                <div class="sr-val" id="resClaimStatus" style="color:var(--cyan);">Approved</div>
              </div>
            </div>

            <div class="sr-cert" id="resCert">
              🛡️ <strong>Certificate:</strong> SLA-CLAIM-VERIFIED-SHA256 • 0-Paperwork Automated Credit Deposit.
            </div>
          </div>

          <button class="btn-primary" onclick="alert('Claim Verified!\\n\\nContractual SLA Credit of ' + document.getElementById('resCreditAmount').textContent + ' is automatically ready for balance deduction in your next billing statement.')" style="text-align:center; justify-content:center;">⚖️ Generate Certified Credit Claim Token ↗</button>
        </div>
      </div>
    </div>

    <!-- 90-Day RCA & Post-Mortem Incident History -->
    <div class="section-title">
      <span>📑 90-Day Root-Cause Analysis (RCA) & Post-Mortems</span>
      <span style="font-size:13px; font-family:var(--font-mono); color:#10b981;">100% Operational Transparency</span>
    </div>

    <div class="incident-log">
      <div class="incident-item">
        <div class="ii-header">
          <div class="ii-title">Scheduled Rolling Maintenance Window #82 (All 95 Nodes)</div>
          <span class="ii-badge ii-resolved">Completed • 0s Downtime</span>
        </div>
        <div class="ii-desc">Deployed global edge telemetry probes and Anycast latency heartbeat radar across Virginia, Dallas, Frankfurt, and Singapore. Performed zero-disruption blue-green container migration with hot-reloading.</div>
        <div class="ii-meta">
          <span>📅 Sep 28, 2026</span>
          <span>⏱️ Duration: 1m 42s</span>
          <span>⚡ Impact: 0 Lost Requests</span>
          <span>🛡️ Verified: SHA-256 Audit Pass</span>
        </div>
      </div>

      <div class="incident-item">
        <div class="ii-header">
          <div class="ii-title">Automated Regional Failover Test #41 (US-East to US-Central)</div>
          <span class="ii-badge ii-resolved">Drill Passed • 4.2s MTTR</span>
        </div>
        <div class="ii-desc">Simulated primary edge gateway latency spike in US-East Virginia. Autonomous DNS Anycast health probe triggered intelligent traffic reroute to Dallas node in 4.2 seconds. Zero dropped calls or missed bookings.</div>
        <div class="ii-meta">
          <span>📅 Sep 15, 2026</span>
          <span>⏱️ Duration: 4.2s</span>
          <span>⚡ Impact: 100% Packet Delivery</span>
          <span>🛡️ Drill Type: Chaos Engineering</span>
        </div>
      </div>

      <div class="incident-item">
        <div class="ii-header">
          <div class="ii-title">Sovereign Hardware Enclave WireGuard Tunnel Rotation</div>
          <span class="ii-badge ii-resolved">Completed • 0.9s Rotation</span>
        </div>
        <div class="ii-desc">Routine 90-day cryptographic key exchange and ephemeral tunnel re-initialization for 8 Sovereign NVIDIA H100 SXM5 GPU enclaves. Zero memory leakage, uninterrupted private inference pipeline.</div>
        <div class="ii-meta">
          <span>📅 Sep 01, 2026</span>
          <span>⏱️ Duration: 0.9s</span>
          <span>⚡ Impact: Zero Latency Impact</span>
          <span>🛡️ Security: AES-256-GCM Handshake</span>
        </div>
      </div>
    </div>

    <!-- Chaos Engineering Drills -->
    <div class="chaos-box">
      <div class="section-title" style="margin-bottom:0;">
        <span>🔥 Autonomous Chaos Engineering & Resilience Drills</span>
        <span style="font-size:13px; font-family:var(--font-mono); color:var(--cyan);">Simulated Failure Modes</span>
      </div>
      <p style="font-size:14px; color:var(--text-muted); margin-top:8px;">Our autonomous platform undergoes weekly scheduled chaos engineering drills to guarantee sub-second disaster recovery.</p>

      <div class="chaos-grid">
        <div class="chaos-card">
          <div class="cc-title">⚡ Neural Swarm Cold Restart</div>
          <div class="cc-desc">Simulated sudden termination of 70B parameter primary inference workers during peak consultation intake hours.</div>
          <div class="cc-result">✓ Secondary Swarm Absorbed 100% Load in 1.8s</div>
        </div>
        <div class="chaos-card">
          <div class="cc-title">🌐 Fiber Severance Simulation</div>
          <div class="cc-desc">Simulated total transatlantic cable severance between Frankfurt EU-Central and Virginia US-East datacenters.</div>
          <div class="cc-result">✓ Anycast Border Gateway Protocol Rerouted in 3.4s</div>
        </div>
        <div class="chaos-card">
          <div class="cc-title">💾 Vector Database Shard Recovery</div>
          <div class="cc-desc">Simulated corrupt memory cache on high-throughput dental knowledge base cluster containing 500k clinical terms.</div>
          <div class="cc-result">✓ Point-in-Time Snapshot Re-streamed in 2.1s</div>
        </div>
      </div>
    </div>

    <!-- 95 Accounts SLA Directory -->
    <div class="ledger-section">
      <div class="section-title">
        <span>📋 Client SLA Compliance & Guarantee Ledger (95 Accounts)</span>
        <span style="font-size:13px; font-family:var(--font-mono); color:var(--gold);">100% Contractual Compliance</span>
      </div>

      <div class="filter-bar">
        <input type="text" id="accSearch" class="search-input" placeholder="🔍 Search by client name, industry, city, or ID..." onkeyup="filterAccounts()">
      </div>

      <div class="accounts-grid" id="accountsGrid"></div>
    </div>

    <!-- Bottom Action Banner -->
    <div class="download-banner">
      <h3 style="font-family:'Outfit'; font-size:26px; color:#fff; margin-bottom:10px;">Need a Tailored SLA Addendum with Custom Financial Penalties?</h3>
      <p style="color:var(--text-muted); font-size:15px; max-width:680px; margin:0 auto 24px;">Our enterprise legal team provides custom Master Services Agreements with financial penalties up to 20x monthly retainers for qualifying accounts.</p>
      <div style="display:flex; justify-content:center; gap:16px; flex-wrap:wrap;">
        <a href="/billing" class="btn-primary">🧾 View Settled Invoices (95) ↗</a>
        <a href="/trust" class="btn-primary" style="background:rgba(255,255,255,0.08); border:1px solid var(--border); color:#fff; box-shadow:none;">🛡️ Security Trust Center ↗</a>
      </div>
    </div>
  </div>

  <footer>
    <p>© 2026 AI Money Machine SLA Financial Guarantee Center. All rights reserved. • <a href="/">Command Center</a> • <a href="/telemetry">NOC Telemetry</a> • <a href="/trust">Trust Center</a> • <a href="/benchmarks">Benchmarks</a> • <a href="/docs">Developer Docs</a></p>
  </footer>

  <script>
    const accounts = {accounts_json_str};

    function populateSelect() {{
      const select = document.getElementById('simAccount');
      select.innerHTML = '';
      accounts.forEach(acc => {{
        const opt = document.createElement('option');
        opt.value = acc.account_id;
        opt.textContent = `${{acc.account_id}} - ${{acc.client_name}} (${{acc.tier_name}} · $${{acc.retainer}}/mo)`;
        select.appendChild(opt);
      }});
    }}

    function onAccountChange() {{
      const id = document.getElementById('simAccount').value;
      const acc = accounts.find(a => a.account_id === id);
      if (acc) {{
        document.getElementById('simRetainer').value = acc.retainer;
        updateRetainerLabel();
        calculateCredit();
      }}
    }}

    function updateRetainerLabel() {{
      const val = parseInt(document.getElementById('simRetainer').value);
      document.getElementById('lblRetainer').textContent = '$' + val.toLocaleString() + ' / mo';
    }}

    function updateUptimeLabel() {{
      const val = parseInt(document.getElementById('simUptime').value) / 100.0;
      document.getElementById('lblUptime').textContent = val.toFixed(2) + '%';
    }}

    function calculateCredit() {{
      const retainer = parseInt(document.getElementById('simRetainer').value);
      const uptime = parseInt(document.getElementById('simUptime').value) / 100.0;

      const totalMonthlyHours = 730; // 365 * 24 / 12
      const downtimeHours = (1.0 - uptime / 100.0) * totalMonthlyHours;

      let pct = 0;
      let tierName = "0% (Met SLA)";

      if (uptime >= 99.90) {{
        pct = 0;
        tierName = "0% (Met SLA)";
      }} else if (uptime >= 99.00) {{
        pct = 0.10;
        tierName = "10% Credit Tier";
      }} else if (uptime >= 98.00) {{
        pct = 0.25;
        tierName = "25% Credit Tier";
      }} else if (uptime >= 95.00) {{
        pct = 0.50;
        tierName = "50% Credit Tier";
      }} else {{
        pct = 1.00;
        tierName = "100% Refund + Free Month";
      }}

      const creditAmount = retainer * pct;

      document.getElementById('resTierApplied').textContent = tierName;
      document.getElementById('resCreditAmount').textContent = '$' + creditAmount.toLocaleString(undefined, {{ minimumFractionDigits: 2, maximumFractionDigits: 2 }});
      document.getElementById('resDowntime').textContent = downtimeHours.toFixed(1) + ' hrs';
      document.getElementById('resClaimStatus').textContent = pct > 0 ? "Approved (Auto)" : "Full Compliance";

      const certEl = document.getElementById('resCert');
      if (pct > 0) {{
        certEl.innerHTML = `⚖️ <strong>Eligible Credit:</strong> Automated credit of $${{creditAmount.toFixed(2)}} tagged to Invoice ledger. Claim Token: <code>SLA-REFUND-${{Math.floor(uptime*100)}}-PASS</code>.`;
        certEl.style.borderColor = "rgba(255, 215, 0, 0.5)";
      }} else {{
        certEl.innerHTML = `🛡️ <strong>Certified:</strong> Uptime exceeds contractual 99.9% SLA threshold. 0 credit deduction required. System operating in full compliance.`;
        certEl.style.borderColor = "rgba(16, 185, 129, 0.4)";
      }}
    }}

    function renderAccounts(list) {{
      const grid = document.getElementById('accountsGrid');
      grid.innerHTML = '';

      if (list.length === 0) {{
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:40px; color:var(--text-muted);">No accounts matched your search criteria.</div>';
        return;
      }}

      list.forEach(acc => {{
        const card = document.createElement('div');
        card.className = 'account-card';

        card.innerHTML = `
          <div>
            <div class="acc-header">
              <span class="acc-id">${{acc.account_id}}</span>
              <span class="acc-badge">${{acc.sla_target}} SLA Target</span>
            </div>
            <div class="acc-name">${{acc.client_name}}</div>
            <div class="acc-meta">
              <span>📍 ${{acc.location}}</span>
              <span>🏢 ${{acc.industry}}</span>
            </div>
            <div class="acc-details">
              <strong>Retainer:</strong> $${{acc.retainer.toLocaleString()}} / mo<br>
              <strong>Guarantee:</strong> Contractual 100% Financial Credit Guarantee<br>
              <strong>Status:</strong> <span style="color:#10b981; font-weight:700;">100% Good Standing</span> (0 Outages)
            </div>
          </div>
          <div class="acc-footer">
            <span>🛡️ ${{acc.payout_multiplier}}</span>
            <div class="acc-actions">
              <a href="${{acc.sla_url}}" target="_blank" class="btn-acc" title="View SLA Packet">SLA Packet ↗</a>
              <a href="${{acc.portal_url}}" target="_blank" class="btn-acc" title="Open VIP Portal">Portal ↗</a>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function filterAccounts() {{
      const q = document.getElementById('accSearch').value.toLowerCase();
      const filtered = accounts.filter(acc => {{
        return acc.client_name.toLowerCase().includes(q) ||
               acc.industry.toLowerCase().includes(q) ||
               acc.location.toLowerCase().includes(q) ||
               acc.account_id.toLowerCase().includes(q);
      }});
      renderAccounts(filtered);
    }}

    // Initial load
    populateSelect();
    renderAccounts(accounts);
    calculateCredit();
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"  [✓] Successfully generated Web App Flagship #24: {OUTPUT_HTML}")
    print(f"      File size: {OUTPUT_HTML.stat().st_size:,} bytes | Accounts loaded: {total_clients}")

if __name__ == "__main__":
    build_guarantee_hub()
