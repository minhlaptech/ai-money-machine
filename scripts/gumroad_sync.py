#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gumroad Automated Sync & Sale Tracker
------------------------------------
Connects to Gumroad API using GUMROAD_ACCESS_TOKEN to:
1. List live products & pricing
2. Fetch recent sales & revenue
3. Push instant sale alerts to Telegram
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"
CACHE_FILE = ROOT_DIR / ".system_cache_sales.json"

def load_env():
    config = {}
    if not ENV_FILE.exists():
        return config
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip().strip('"').strip("'")
    return config

ENV = load_env()
TOKEN = os.environ.get("GUMROAD_ACCESS_TOKEN") or ENV.get("GUMROAD_ACCESS_TOKEN", "")
TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or ENV.get("TELEGRAM_BOT_TOKEN", "")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or ENV.get("TELEGRAM_CHAT_ID", "")

def send_telegram(text):
    if not TG_TOKEN or not TG_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TG_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            pass
    except Exception as e:
        print(f"[!] Telegram alert error: {e}")

def get_gumroad(endpoint):
    if not TOKEN:
        return None, "GUMROAD_ACCESS_TOKEN is not configured in .env"
    url = f"https://api.gumroad.com/v2/{endpoint}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')}"
    except Exception as e:
        return None, str(e)

def sync_gumroad(notify=True):
    print("[*] Checking Gumroad Sales & Products...")
    
    if not TOKEN:
        print("[!] GUMROAD_ACCESS_TOKEN is missing in .env.")
        print("    Get your token at: https://app.gumroad.com/settings/advanced")
        return False

    # Fetch products
    products_res, err = get_gumroad("products")
    if err:
        print(f"[!] Failed to fetch products: {err}")
        return False

    products = products_res.get("products", [])
    print(f"[✓] Found {len(products)} products on Gumroad:")
    for p in products:
        price_usd = (p.get("price", 0) / 100)
        print(f"    - {p.get('name')}: ${price_usd:.2f} ({p.get('sales_count', 0)} sales) -> {p.get('short_url')}")

    # Fetch sales
    sales_res, err = get_gumroad("sales")
    if err:
        print(f"[!] Failed to fetch sales: {err}")
        return False

    sales = sales_res.get("sales", [])
    total_revenue = sum(s.get("price", 0) for s in sales) / 100
    print(f"\n[✓] Total Gumroad Revenue: ${total_revenue:.2f} across {len(sales)} orders")

    # Check for new sales against cache
    known_sale_ids = set()
    if CACHE_FILE.exists():
        try:
            cached_data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            known_sale_ids = set(cached_data.get("known_sale_ids", []))
        except Exception:
            pass

    new_sales = [s for s in sales if s.get("id") not in known_sale_ids]

    if new_sales and notify:
        for s in new_sales:
            p_name = s.get("product_name", "Digital Product")
            price = (s.get("price", 0) / 100)
            email = s.get("email", "Customer")
            country = s.get("country", "Global")
            
            tg_msg = (
                f"🎉 *[NEW GUMROAD SALE!]*\n\n"
                f"📦 *Sản phẩm:* *{p_name}*\n"
                f"💵 *Số tiền:* `${price:.2f} USD`\n"
                f"📧 *Khách hàng:* `{email}` ({country})\n"
                f"⏰ *Thời gian:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                f"🚀 _Doanh thu kỹ thuật số thụ động đã ghi nhận!_"
            )
            send_telegram(tg_msg)
            print(f"[+] Alerted new sale: {p_name} - ${price:.2f}")

    # Update cache
    current_ids = [s.get("id") for s in sales]
    CACHE_FILE.write_text(json.dumps({
        "last_checked": datetime.now().isoformat(),
        "known_sale_ids": current_ids,
        "total_revenue": total_revenue
    }, indent=2), encoding="utf-8")

    return True

if __name__ == "__main__":
    sync_gumroad(notify=True)
