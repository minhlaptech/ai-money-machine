import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

# 1. Upgrade tools/index.html modal
p_tools = ROOT / "tools/index.html"
txt_tools = p_tools.read_text(encoding="utf-8")

old_modal = """    <div class="modal-box">
      <button class="modal-close" onclick="closeModal()">×</button>
      <span class="modal-badge" id="modalBadge">⭐ Lifetime License</span>
      <h3 class="modal-title" id="modalTitle">All-Access Suite Pass</h3>
      <p class="modal-desc" id="modalDesc">Immediate activation across all 3 Micro-SaaS tools.</p>
      
      <div class="modal-price-tag" id="modalPriceTag">$39</div>
      
      <input type="email" id="suite-email" class="modal-input" placeholder="Enter your business email...">
      <button class="btn-modal-checkout" id="suiteCheckoutBtn" onclick="processSuiteCheckout()">Proceed to Secure Activation →</button>
      <p style="font-size:11px; color:var(--text-muted); text-align:center; margin-top:10px;">🔒 256-Bit Encrypted • Immediate Access</p>
    </div>"""

new_modal = """    <div class="modal-box">
      <button class="modal-close" onclick="closeModal()">×</button>
      <span class="modal-badge" id="modalBadge">⭐ Lifetime License</span>
      <h3 class="modal-title" id="modalTitle">All-Access Suite Pass</h3>
      <p class="modal-desc" id="modalDesc">Immediate activation across all 3 Micro-SaaS tools.</p>
      
      <div class="modal-price-tag" id="modalPriceTag">$39</div>

      <!-- Real Direct Checkout Gateways -->
      <div style="display:flex; flex-direction:column; gap:10px; margin-bottom:18px;">
        <a href="https://minhlap.gumroad.com/l/xqckmu" target="_blank" class="btn-modal-checkout" style="text-decoration:none; text-align:center; background:linear-gradient(135deg,#ff90e8,#ffc900); color:#000; font-weight:800; padding:12px; border-radius:10px; display:block;">
          ⚡ Pay via Gumroad Direct Checkout ↗
        </a>
        <a href="https://minhlap.lemonsqueezy.com" target="_blank" class="btn-modal-checkout" style="text-decoration:none; text-align:center; background:linear-gradient(135deg,#ffd700,#ff8c00); color:#000; font-weight:800; padding:12px; border-radius:10px; display:block;">
          🍋 Pay via Lemon Squeezy Store ↗
        </a>
      </div>

      <div style="border-top:1px solid var(--border); padding-top:14px; margin-top:10px;">
        <p style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">Or enter work email to receive an official B2B invoice & wire details:</p>
        <input type="email" id="suite-email" class="modal-input" placeholder="Enter your business email...">
        <button class="btn-modal-checkout" id="suiteCheckoutBtn" onclick="processSuiteCheckout()" style="background:rgba(255,255,255,0.08); border:1px solid var(--border); color:#fff; width:100%;">Request Official B2B Invoice →</button>
      </div>
      
      <p style="font-size:11px; color:var(--text-muted); text-align:center; margin-top:12px;">🔒 256-Bit SSL Encrypted • Instant Product Delivery</p>
    </div>"""

if old_modal in txt_tools:
    txt_tools = txt_tools.replace(old_modal, new_modal)
    # Also update redirect in processSuiteCheckout
    txt_tools = txt_tools.replace(
        'showToast("🎉 Order Processed! Your Pro Founder Pass is now active across all tools.");',
        'showToast("🎉 Request registered! Redirecting to secure checkout portal...");\n        setTimeout(() => { window.location.href = "https://minhlap.gumroad.com/l/xqckmu"; }, 1500);'
    )
    p_tools.write_text(txt_tools, encoding="utf-8")
    print("✓ Updated tools/index.html with real checkout buttons and redirects!")
else:
    print("Warning: old_modal in tools/index.html not matched!")

# 2. Upgrade products/geo_audit_engine/app.js
p_geo = ROOT / "products/geo_audit_engine/app.js"
if p_geo.exists():
    txt_geo = p_geo.read_text(encoding="utf-8")
    old_geo_fn = """    showToast("🎉 License Activated! Full AI Crawlability unlocked.");
  }, 1200);"""
    new_geo_fn = """    showToast("🎉 Redirecting to secure checkout gateway...");
    setTimeout(() => {
      window.location.href = "https://minhlap.gumroad.com/l/xqckmu";
    }, 1200);
  }, 1000);"""
    if old_geo_fn in txt_geo:
        txt_geo = txt_geo.replace(old_geo_fn, new_geo_fn)
        p_geo.write_text(txt_geo, encoding="utf-8")
        print("✓ Updated products/geo_audit_engine/app.js to redirect to real checkout!")

print("\nReal checkout integrations completed!")
