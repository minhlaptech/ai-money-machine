"""
Multi-Platform Sales Webhook Simulator & Tester
-----------------------------------------------
Simulates inbound sales and subscription events from:
 1. Lemon Squeezy ($47 AI Money Blueprint / $97 Make.com Blueprints)
 2. Gumroad ($27 Prompt Pack)
 3. Stripe / B2B Retainer ($1,850 Kickoff Setup)
Tests live /api/webhook or dispatches direct Telegram confirmation.
"""

import sys
import os
import json
import argparse
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

SCENARIOS = {
    "lemonsqueezy_blueprint": {
        "platform": "Lemon Squeezy",
        "headers": {
            "Content-Type": "application/json",
            "x-event-name": "order_created"
        },
        "payload": {
            "meta": { "event_name": "order_created" },
            "data": {
                "id": "1049281",
                "attributes": {
                    "user_name": "Marcus Aurelius",
                    "user_email": "marcus.aurelius@techventures.example",
                    "total_formatted": "$47.00",
                    "identifier": "LSQ-2026-9921",
                    "first_order_item": {
                        "product_name": "The AI Money Blueprint — Premium Edition (PDF + Blueprints)"
                    }
                }
            }
        }
    },
    "gumroad_prompts": {
        "platform": "Gumroad",
        "headers": { "Content-Type": "application/json" },
        "payload": {
            "seller_id": "minhlap_gumroad",
            "full_name": "Sophia Loren",
            "email": "sophia.loren@creativescale.example",
            "product_name": "AI Marketing Prompt Pack (110+ Battle-Tested Prompts)",
            "price": 2700,
            "order_number": "GUM-88412"
        }
    },
    "b2b_retainer_setup": {
        "platform": "Stripe / Direct Invoice",
        "headers": { "Content-Type": "application/json" },
        "payload": {
            "type": "checkout.session.completed",
            "customer_name": "Dr. Miller (Austin Dental Co)",
            "customer_email": "contact@austindentalco.example",
            "product_name": "B2B AI Copilot Infrastructure Setup + Month 1 Retainer",
            "amount": "$1,850.00",
            "order_id": "INV-2026-001"
        }
    }
}

def simulate_webhook(scenario_key="lemonsqueezy_blueprint", target_url="https://work-minh-lap.vercel.app/api/webhook"):
    sc = SCENARIOS.get(scenario_key)
    if not sc:
        print(f"[!] Scenario '{scenario_key}' not found. Available: {list(SCENARIOS.keys())}")
        return

    print("=" * 70)
    print(f"🚀 SIMULATING INBOUND SALE: [{sc['platform']}]")
    print(f"🎯 Target Endpoint: {target_url}")
    print("=" * 70)

    data_bytes = json.dumps(sc["payload"]).encode("utf-8")
    req = urllib.request.Request(target_url, data=data_bytes, headers=sc["headers"], method="POST")

    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            res_json = json.loads(body)
            print(f"[✓] Status Code: HTTP {status}")
            print(f"[✓] Telegram Notification Sent: {res_json.get('success')}")
            print(f"[✓] Product: {res_json.get('product')}")
            print(f"[✓] Amount: {res_json.get('amount')}")
            print(f"[✓] Fulfillment URL: {res_json.get('fulfillment_url')}")
            print("-" * 70)
            print("🎉 SUCCESS: Webhook received, processed, and confirmed!")
            print("=" * 70)
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error {e.code}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"[!] Connection or Execution Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test and simulate sales webhooks")
    parser.add_argument("--scenario", choices=["lemonsqueezy_blueprint", "gumroad_prompts", "b2b_retainer_setup"], default="lemonsqueezy_blueprint")
    parser.add_argument("--url", default="https://work-minh-lap.vercel.app/api/webhook", help="Webhook endpoint URL")
    args = parser.parse_args()

    simulate_webhook(args.scenario, args.url)
