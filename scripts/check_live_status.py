import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

env = {}
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

print("=" * 60)
print("1. CHECKING LEMON SQUEEZY REAL EARNINGS & ORDERS")
print("=" * 60)
ls_key = env.get("LEMON_SQUEEZY_API_KEY", "")
if ls_key:
    # 1. Store details
    req_store = urllib.request.Request(
        "https://api.lemonsqueezy.com/v1/stores",
        headers={"Authorization": f"Bearer {ls_key}", "Accept": "application/vnd.api+json", "User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req_store) as r:
            stores = json.loads(r.read().decode()).get("data", [])
            for s in stores:
                attr = s.get("attributes", {})
                print(f"Store: {attr.get('name')} (ID: {s.get('id')}) - URL: {attr.get('url')}, Currency: {attr.get('currency')}, Total Sales: {attr.get('total_sales', 'N/A')}")
    except Exception as e:
        print(f"Store fetch error: {e}")

    # 2. Orders
    req_orders = urllib.request.Request(
        "https://api.lemonsqueezy.com/v1/orders",
        headers={"Authorization": f"Bearer {ls_key}", "Accept": "application/vnd.api+json", "User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req_orders) as r:
            orders = json.loads(r.read().decode()).get("data", [])
            print(f"Real Orders Count: {len(orders)}")
            total_real_cents = sum(o.get("attributes", {}).get("total", 0) for o in orders if o.get("attributes", {}).get("status") == "paid")
            print(f"Real Paid Revenue (USD): ${total_real_cents / 100:.2f}")
            for o in orders:
                attr = o.get("attributes", {})
                print(f"  - Order #{o.get('id')}: {attr.get('status')} | Total: ${attr.get('total', 0)/100:.2f} | Customer: {attr.get('user_email')} | Date: {attr.get('created_at')}")
    except Exception as e:
        print(f"Orders fetch error: {e}")

print("\n" + "=" * 60)
print("2. CHECKING VERCEL DEPLOYMENT STATUS & QUOTA")
print("=" * 60)
v_token = env.get("VERCEL_TOKEN", "")
if v_token:
    req_v = urllib.request.Request(
        "https://api.vercel.com/v6/deployments?limit=10",
        headers={"Authorization": f"Bearer {v_token}"}
    )
    try:
        with urllib.request.urlopen(req_v) as r:
            dpls = json.loads(r.read().decode()).get("deployments", [])
            print(f"Recent Deployments Count: {len(dpls)}")
            for d in dpls:
                created_dt = datetime.fromtimestamp(d.get('created', 0)/1000).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  - {d.get('name')} | State: {d.get('state')} | URL: https://{d.get('url')} | Created: {created_dt}")
    except urllib.error.HTTPError as e:
        print(f"Vercel HTTP Error: {e.code} - {e.read().decode()[:300]}")
    except Exception as e:
        print(f"Vercel fetch error: {e}")

    # Check project aliases
    req_alias = urllib.request.Request(
        "https://api.vercel.com/v4/aliases",
        headers={"Authorization": f"Bearer {v_token}"}
    )
    try:
        with urllib.request.urlopen(req_alias) as r:
            aliases = json.loads(r.read().decode()).get("aliases", [])
            print("\nVercel Aliases:")
            for a in aliases[:10]:
                print(f"  - {a.get('alias')} -> deployment: {a.get('deploymentId')}")
    except Exception as e:
        print(f"Aliases fetch error: {e}")

print("\n" + "=" * 60)
print("3. CHECKING HTTP STATUS OF ALL REPORTED LINKS")
print("=" * 60)
links_to_check = [
    ("Attribution Ledger", "https://work-minh-lap.vercel.app/attribution"),
    ("Live Unified Inbox", "https://work-minh-lap.vercel.app/inbox"),
    ("Agent Studio", "https://work-minh-lap.vercel.app/knowledge"),
    ("SLA Guarantee Hub", "https://work-minh-lap.vercel.app/guarantee"),
    ("Benchmarks Index", "https://work-minh-lap.vercel.app/benchmarks"),
    ("Trust Center", "https://work-minh-lap.vercel.app/trust"),
    ("Master Dashboard", "https://work-minh-lap.vercel.app")
]

for name, url in links_to_check:
    req_l = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req_l, timeout=5) as resp:
            print(f"  [✓] {name}: HTTP {resp.status} -> {url}")
    except urllib.error.HTTPError as e:
        print(f"  [!] {name}: HTTP {e.code} {e.reason} -> {url}")
    except Exception as e:
        print(f"  [!] {name}: Error {e} -> {url}")
