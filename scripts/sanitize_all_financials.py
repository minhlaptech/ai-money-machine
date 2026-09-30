import re
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

def update_file(rel_path, replacements):
    p = ROOT / rel_path
    if not p.exists():
        print(f"File not found: {rel_path}")
        return
    txt = p.read_text(encoding="utf-8")
    original = txt
    for old, new in replacements:
        if old in txt:
            txt = txt.replace(old, new)
        else:
            print(f"Warning: '{old[:40]}...' not found in {rel_path}")
    if txt != original:
        p.write_text(txt, encoding="utf-8")
        print(f"✓ Updated: {rel_path}")
    else:
        print(f"No changes: {rel_path}")

# 1. billing/index.html
update_file("billing/index.html", [
    (
        '<div class="hero-badge">\n        <span>🧾 100% SETTLED & VERIFIED COMMERCIAL CONTRACTS</span>\n      </div>',
        '<div class="hero-badge">\n        <span>🧾 95 PRE-CONFIGURED CLIENT BILLING & INVOICING BLUEPRINTS</span>\n      </div>'
    ),
    (
        '<div class="metric-label">Empire Total ARR</div>\n          <div class="metric-value">$1,002,600</div>\n          <div class="metric-sub">🎉 $1M Milestone Conquered</div>',
        '<div class="metric-label">Pipeline Target ARR</div>\n          <div class="metric-value">$1,002,600</div>\n          <div class="metric-sub">🎯 95 Workspaces Target Pipeline</div>'
    ),
    (
        '<div class="metric-label">Cash Collected & Settled</div>\n          <div class="metric-value">$260,600</div>\n          <div class="metric-sub">100% Upfront Collection Rate</div>',
        '<div class="metric-label">Doanh Thu Thực Thu</div>\n          <div class="metric-value" style="color:#00e676;">$0.00</div>\n          <div class="metric-sub">💳 Sẵn sàng xuất HĐ & thanh toán</div>'
    ),
    (
        '<div class="metric-label">Monthly Retainers (MRR)</div>\n          <div class="metric-value">$83,550 / mo</div>\n          <div class="metric-sub">95 Contracted Accounts</div>',
        '<div class="metric-label">Mục Tiêu MRR Pipeline</div>\n          <div class="metric-value">$83,550 / mo</div>\n          <div class="metric-sub">95 Khung Tài Khoản Doanh Nghiệp</div>'
    ),
    (
        '<div class="metric-label">Executed Contracts (MSAs)</div>\n          <div class="metric-value">95 Active</div>\n          <div class="metric-sub">0 Overdue · 0 A/R Aging</div>',
        '<div class="metric-label">Hợp Đồng Mẫu (MSAs)</div>\n          <div class="metric-value">95 Drafts</div>\n          <div class="metric-sub">Sẵn sàng ký kết & bàn giao</div>'
    )
])

# 2. fulfillment/index.html
update_file("fulfillment/index.html", [
    (
        '<div class="metric-label">Empire Total ARR</div>\n          <div class="metric-value">$1,002,600</div>\n          <div class="metric-sub">🎉 $1M Milestone Conquered</div>',
        '<div class="metric-label">Pipeline Target ARR</div>\n          <div class="metric-value">$1,002,600</div>\n          <div class="metric-sub">🎯 95 Client Clusters Target</div>'
    ),
    (
        '<div class="metric-label">Upfront Cash Realized</div>\n          <div class="metric-value">$260,600</div>\n          <div class="metric-sub">100% Collected & Cleared</div>',
        '<div class="metric-label">Doanh Thu Thực Thu</div>\n          <div class="metric-value" style="color:#00e676;">$0.00</div>\n          <div class="metric-sub">💳 Cổng thanh toán sẵn sàng</div>'
    ),
    (
        '<div class="metric-label">Monthly Retainers (MRR)</div>\n          <div class="metric-value">$83,550</div>\n          <div class="metric-sub">95 Contracted Accounts</div>',
        '<div class="metric-label">Mục Tiêu MRR Pipeline</div>\n          <div class="metric-value">$83,550</div>\n          <div class="metric-sub">95 Workspaces Framework</div>'
    )
])

# 3. portals/index.html
update_file("portals/index.html", [
    (
        '<div class="stat-lbl">Consolidated ARR</div>\n          <div class="stat-val">$1,002,600</div>\n          <div class="stat-sub">🎉 $1M Milestone Conquered</div>',
        '<div class="stat-lbl">Pipeline Target ARR</div>\n          <div class="stat-val">$1,002,600</div>\n          <div class="stat-sub">🎯 95 VIP Portals Pipeline</div>'
    ),
    (
        '<div class="stat-lbl">Cash Realized Upfront</div>\n          <div class="stat-val">$260,600</div>\n          <div class="stat-sub">100% Collected & Cleared</div>',
        '<div class="stat-lbl">Doanh Thu Thực Thu</div>\n          <div class="stat-val" style="color:#00e676;">$0.00</div>\n          <div class="stat-sub">💳 Sẵn sàng thu phí đối tác</div>'
    ),
    (
        '<div class="stat-lbl">Monthly Retainers (MRR)</div>\n          <div class="stat-val">$83,550 / mo</div>\n          <div class="stat-sub">Contracted Recurring Revenue</div>',
        '<div class="stat-lbl">Mục Tiêu MRR Pipeline</div>\n          <div class="stat-val">$83,550 / mo</div>\n          <div class="stat-sub">95 Khách Hàng Tiềm Năng</div>'
    )
])

# 4. docs/index.html
update_file("docs/index.html", [
    (
        'financials: { consolidated_arr: "$1,002,600 / Year", upfront_cash_realized: "$260,600.00" }',
        'financials: { actual_realized_revenue: "$0.00", actual_paid_orders: 0, pipeline_target_potential: "$83,550 / month" }'
    ),
    (
        'across 95 active enterprise accounts ($1,002,600 ARR)',
        'across 95 enterprise accounts ($83,550/mo Target Pipeline)'
    )
])

# 5. attribution/index.html
update_file("attribution/index.html", [
    (
        '95 ACCOUNTS ($1,002,600 ARR)',
        '95 ACCOUNTS ($83,550/mo TARGET PIPELINE)'
    ),
    (
        'protecting $1,002,600 ARR',
        'protecting 95 client accounts ($83,550/mo Target Pipeline)'
    )
])

# 6. benchmarks/index.html
update_file("benchmarks/index.html", [
    (
        'protecting <strong>$1,002,600 ARR</strong>',
        'protecting <strong>95 Client Accounts ($83,550/mo Target Pipeline)</strong>'
    )
])

# 7. inbox/index.html
update_file("inbox/index.html", [
    (
        '<div class="pill pill-gold">💰 $1,002,600 ARR Protected</div>',
        '<div class="pill pill-gold">💼 95 Accounts ($83,550/mo Pipeline)</div>'
    ),
    (
        'protecting $1,002,600 ARR',
        'serving 95 client accounts ($83,550/mo Target Pipeline)'
    )
])

# 8. packages/index.html
update_file("packages/index.html", [
    (
        '<div class="kpi-lbl">Empire Total ARR</div>\n          <div class="kpi-val" style="color: #ffd700;">$1,002,600</div>',
        '<div class="kpi-lbl">Pipeline Target ARR</div>\n          <div class="kpi-val" style="color: #ffd700;">$1,002,600</div>'
    ),
    (
        'across all 95 active client deployments ($1,002,600 ARR)',
        'across all 95 client deployments ($83,550/mo Target Pipeline)'
    )
])

# 9. sandboxes/index.html
update_file("sandboxes/index.html", [
    (
        '<div class="kpi-lbl">Empire Total ARR</div>\n        <div class="kpi-val" style="color:#f59e0b;">$1,002,600</div>',
        '<div class="kpi-lbl">Pipeline Target ARR</div>\n        <div class="kpi-val" style="color:#f59e0b;">$1,002,600</div>'
    ),
    (
        'across all 95 active accounts ($1,002,600 ARR)',
        'across all 95 client accounts ($83,550/mo Target Pipeline)'
    )
])

# 10. telemetry/index.html
update_file("telemetry/index.html", [
    (
        'protecting <strong>$1,002,600 ARR</strong>',
        'protecting <strong>95 Client Accounts ($83,550/mo Target Pipeline)</strong>'
    )
])

# 11. trust/index.html
update_file("trust/index.html", [
    (
        'protecting $1,002,600 ARR',
        'protecting 95 client accounts ($83,550/mo Target Pipeline)'
    )
])

# 12. index.html and dashboard.html
def update_index(path_str):
    p = ROOT / path_str
    txt = p.read_text(encoding="utf-8")
    txt = txt.replace('($1,002,600 ARR)', '($83,550/mo Target Pipeline)')
    txt = txt.replace('$260,600 settled cash and $83,550/mo MRR ($1,002,600 ARR)', 'Thực thu: $0.00 · Mục tiêu Pipeline: $83,550/mo ($1.00M ARR Target)')
    txt = txt.replace('protecting $1,002,600 ARR across all 95 client namespaces', 'protecting 95 client namespaces ($83,550/mo Target Pipeline)')
    txt = txt.replace('Real-time telemetry, edge network ping monitoring, and automated retention radar protecting $1,002,600 ARR', 'Real-time telemetry, edge network ping monitoring, and automated retention radar protecting 95 client workspaces')
    txt = txt.replace('Turnkey ZIP deliverable vaults, SHA-256 cryptographic checksums, and executive PDF handoffs protecting $1,002,600 ARR', 'Turnkey ZIP deliverable vaults, SHA-256 cryptographic checksums, and executive PDF handoffs for 95 client workspaces')
    txt = txt.replace('Real-time interactive acceptance testing, telephony SIP dialers, and conversational telemetry protecting $1,002,600 ARR', 'Real-time interactive acceptance testing, telephony SIP dialers, and conversational telemetry for 95 client workspaces')
    txt = txt.replace('Real-time telemetry, dedicated SIP trunk routing, isolated vector namespaces, and guaranteed 48-hour SLA telemetry across all 95 active client deployments ($1,002,600 ARR)', 'Real-time telemetry, dedicated SIP trunk routing, isolated vector namespaces, and guaranteed 48-hour SLA telemetry across all 95 client workspaces')
    txt = txt.replace('<div style="font-size:20px; font-weight:800; color:#fff;">$260,600 USD <span style="font-size:13px; color:#4ade80;">($83,550/mo MRR)</span></div>', '<div style="font-size:16px; font-weight:800; color:#fff;">Thực Thu: <span style="color:#00e676;">$0.00</span> · <span style="font-size:12px; color:#ffd700;">Target: $83,550/mo</span></div>')
    p.write_text(txt, encoding="utf-8")
    print(f"✓ Sanitized: {path_str}")

update_index("index.html")
update_index("dashboard.html")
print("\nAll files successfully sanitized to 100% real financial values!")
