import os
import json
import urllib.request
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

ls_key = env.get("LEMON_SQUEEZY_API_KEY", "")

req = urllib.request.Request(
    "https://api.lemonsqueezy.com/v1/products",
    headers={"Authorization": f"Bearer {ls_key}", "Accept": "application/vnd.api+json", "User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(req) as r:
        products = json.loads(r.read().decode()).get("data", [])
        print(f"Total Lemon Squeezy Products: {len(products)}")
        for p in products:
            attr = p.get("attributes", {})
            print(f"- Product ID: {p.get('id')} | Name: {attr.get('name')} | Price: ${attr.get('price', 0)/100:.2f} | Status: {attr.get('status')} | Buy URL: {attr.get('buy_now_url')}")
except Exception as e:
    print("Error fetching products:", e)

# Also check variants
req_var = urllib.request.Request(
    "https://api.lemonsqueezy.com/v1/variants",
    headers={"Authorization": f"Bearer {ls_key}", "Accept": "application/vnd.api+json", "User-Agent": "Mozilla/5.0"}
)
try:
    with urllib.request.urlopen(req_var) as r:
        variants = json.loads(r.read().decode()).get("data", [])
        print(f"\nTotal Lemon Squeezy Variants: {len(variants)}")
        for v in variants:
            attr = v.get("attributes", {})
            print(f"- Variant ID: {v.get('id')} | Name: {attr.get('name')} | Price: ${attr.get('price', 0)/100:.2f} | Status: {attr.get('status')}")
except Exception as e:
    print("Error fetching variants:", e)
