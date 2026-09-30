import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
index_path = ROOT / "index.html"
txt = index_path.read_text(encoding="utf-8")

# 1. Remove duplicated old metric cards from lines 500-522
duplicate_cards = """      <div class="metric-card">
        <div class="metric-label">Production Apps & Tools</div>
        <div class="metric-val">27 Flagship Hubs</div>
        <div class="metric-sub">🌐 Vercel Edge + Serverless APIs</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Ready-to-Sell Assets</div>
        <div class="metric-val">6 Products + 6 POD</div>
        <div class="metric-sub">📦 LemonSqueezy + Printify</div>
      </div>
      <div class="metric-card">
        <div class="metric-label">Client Outreach Pipeline</div>
        <div class="metric-val">95 VIP Portals Live</div>
        <div class="metric-sub">✉️ 4 Tiers · 95 Production Deployments</div>
      </div>
      <div class="metric-card" style="border-color: rgba(255, 215, 0, 0.35); background: linear-gradient(180deg, rgba(255, 215, 0, 0.06) 0%, rgba(18, 18, 36, 0.7) 100%);">
        <div class="metric-label" style="color: #ffd700;">Closed Retainers (MRR)</div>
        <div class="metric-val" style="color: #ffd700;">$260,600 · $83,550/mo</div>
        <div class="metric-sub" style="color: #ffd700; font-weight: 700;">🏆 95 Won Deals · 60 Base + 15 Ent + 8 Sov + 12 Syn ($1.00M ARR)</div>
      </div>
    </div>"""

if duplicate_cards in txt:
    txt = txt.replace(duplicate_cards, "")
    print("✓ Removed duplicated old KPI cards!")
else:
    print("Warning: duplicate_cards block not found exactly as string, attempting fuzzy match")

# 2. Fix Master Billing card description in saas-grid
old_billing_desc = "<p>Official legal contracts (MSAs), wire receipts, and automated billing ledgers for all 95 active client accounts. $260,600 settled cash and $83,550/mo MRR ($83,550/mo Target Pipeline).</p>"
new_billing_desc = "<p>Official legal contracts (MSAs), invoicing templates, and automated billing ledgers for 95 client accounts. Realized cash: $0.00 · Target pipeline: $83,550/mo ($1.00M ARR Target).</p>"
if old_billing_desc in txt:
    txt = txt.replace(old_billing_desc, new_billing_desc)
    print("✓ Fixed billing card description!")

# 3. Fix Tab 12 Upfront Settled Cash header
old_tab12 = """            <div style="font-size:11px; text-transform:uppercase; color:#ffd700;">Upfront Settled Cash</div>
            <div style="font-size:20px; font-weight:800; color:#fff;">$260,600 USD <span style="font-size:13px; color:#4ade80;">(100% Collected)</span></div>"""
new_tab12 = """            <div style="font-size:11px; text-transform:uppercase; color:#ffd700;">Doanh Thu Thực Thu</div>
            <div style="font-size:20px; font-weight:800; color:#fff;">$0.00 <span style="font-size:12px; color:#ffd700;">(Pipeline: $83,550/mo)</span></div>"""
if old_tab12 in txt:
    txt = txt.replace(old_tab12, new_tab12)
    print("✓ Fixed tab 12 upfront cash!")

index_path.write_text(txt, encoding="utf-8")
print("Done updating index.html!")
