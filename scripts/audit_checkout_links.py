import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

files_to_check = [
    ROOT / "tools/index.html",
    ROOT / "products/geo_audit_engine/index.html",
    ROOT / "products/review_genius/index.html",
    ROOT / "products/headline_iq/index.html",
    ROOT / "projects/digital_products/bundle_showcase.html",
    ROOT / "merch/index.html",
    ROOT / "freelance/index.html",
    ROOT / "projects/affiliate_blog/website/index.html",
    ROOT / "projects/affiliate_blog/website/referrals.html"
]

print("=== CHECKOUT LINKS AUDIT ===")
for p in files_to_check:
    if p.exists():
        content = p.read_text(encoding="utf-8")
        links = re.findall(r'href=["\'](https?://[^"\']+)["\']', content)
        checkout_links = [l for l in links if any(k in l.lower() for k in ["lemonsqueezy", "gumroad", "stripe", "buy", "checkout", "paypal"])]
        rel = p.relative_to(ROOT)
        print(f"\n[{rel}] (Total links: {len(links)})")
        if checkout_links:
            for cl in set(checkout_links):
                print(f"  ✓ Checkout URL: {cl}")
        else:
            print("  ⚠️ NO PAYMENT/CHECKOUT URL FOUND!")
    else:
        print(f"\n[MISSING FILE]: {p}")
