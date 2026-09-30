"""
Autonomous B2B CRM Pipeline Tracker & State Manager
---------------------------------------------------
Quản lý trạng thái tiếp cận và phễu khách hàng (Pipeline CRM) cho toàn bộ 30 leads.
Theo dõi từng giai đoạn tiếp cận: New -> Day 1 Sent -> Day 3 Follow-Up -> Day 7 Break-Up -> Call Booked -> Won.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent
CRM_FILE = ROOT_DIR / "prospects" / "crm_pipeline.json"

try:
    from leads_data import ALL_LEADS
except ImportError:
    from scripts.leads_data import ALL_LEADS
except Exception:
    ALL_LEADS = []

def get_default_leads():
    if ALL_LEADS:
        return [{
            "id": l["id"],
            "batch": l["batch"],
            "name": l["name"],
            "niche": l["niche"],
            "city": l["city"],
            "to": l["to"],
            "doc": l.get("doc", "Owner"),
            "status": "new",
            "value": l.get("setup", 1200),
            "retainer": l.get("retainer", 650),
            "last_touch": None
        } for l in ALL_LEADS]
    return []

INITIAL_LEADS = get_default_leads()

def load_pipeline():
    if not CRM_FILE.exists():
        CRM_FILE.parent.mkdir(parents=True, exist_ok=True)
        default_data = get_default_leads()
        CRM_FILE.write_text(json.dumps(default_data, indent=2, ensure_ascii=False), encoding="utf-8")
        return default_data
    try:
        return json.loads(CRM_FILE.read_text(encoding="utf-8"))
    except Exception:
        return get_default_leads()

def save_pipeline(leads):
    CRM_FILE.write_text(json.dumps(leads, indent=2, ensure_ascii=False), encoding="utf-8")

def print_summary():
    leads = load_pipeline()
    total = len(leads)
    new_count = sum(1 for l in leads if l["status"] == "new")
    day1_count = sum(1 for l in leads if l["status"] == "day1")
    day3_count = sum(1 for l in leads if l["status"] == "day3")
    day7_count = sum(1 for l in leads if l["status"] == "day7")
    booked_count = sum(1 for l in leads if l["status"] == "booked")
    won_count = sum(1 for l in leads if l["status"] == "won")

    total_pipeline_val = sum(l["value"] for l in leads)
    closed_val = sum(l["value"] for l in leads if l["status"] == "won")
    mrr_val = sum(l["retainer"] for l in leads if l["status"] == "won")

    print("=" * 70)
    print("📊 B2B CLIENT PIPELINE CRM — EXECUTIVE DASHBOARD")
    print("=" * 70)
    print(f"  • Total Prospects:         {total}")
    print(f"  • ⚪ Untouched (New):       {new_count}")
    print(f"  • 🎯 Day 1 Hook Sent:      {day1_count}")
    print(f"  • 📈 Day 3 Follow-Up Sent: {day3_count}")
    print(f"  • 🚪 Day 7 Break-Up Sent:  {day7_count}")
    print(f"  • 📞 Discovery Calls Booked: {booked_count}")
    print(f"  • 🏆 Won Retainer Clients:  {won_count}")
    print("-" * 70)
    print(f"  💰 Total Pipeline Potential: ${total_pipeline_val:,}")
    print(f"  💵 Won Contract Value (Projected): ${closed_val:,}")
    print(f"  🔄 Projected Monthly Retainer: ${mrr_val:,}/month")
    print(f"  🛡️ Real Cash Realized (Accounting): $0.00 (Awaiting Payment Webhook)")
    print("=" * 70)

def send_telegram_alert(lead, old_status, new_status):
    env_file = ROOT_DIR / ".env"
    bot_token, chat_id = None, None
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("TELEGRAM_BOT_TOKEN="):
                bot_token = line.split("=", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("TELEGRAM_CHAT_ID="):
                chat_id = line.split("=", 1)[1].strip().strip('"').strip("'")

    bot_token = bot_token or "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU"
    chat_id = chat_id or "1624883046"

    status_emojis = {
        "new": "⚪",
        "day1": "🎯",
        "day3": "📈",
        "day7": "🚪",
        "booked": "📞",
        "won": "🏆"
    }
    emoji = status_emojis.get(new_status, "⚡")
    now_vn = datetime.now().strftime("%Y-%m-%d %H:%M (GMT+7)")

    msg = f"<b>{emoji} [B2B CRM DEAL STATUS UPDATED]</b>\n\n"
    msg += f"🏢 <b>Doanh nghiệp:</b> <b>{lead['name']}</b> (#{lead['id']})\n"
    msg += f"📍 <b>Khu vực & Ngành:</b> {lead.get('niche', 'N/A')} • {lead.get('city', 'N/A')}\n"
    msg += f"👤 <b>Người phụ trách:</b> {lead.get('doc', 'Owner')}\n"
    msg += f"🔄 <b>Trạng thái:</b> <code>{old_status}</code> ➔ <b>{new_status.upper()}</b>\n"
    msg += f"💵 <b>Giá trị Setup:</b> <code>${lead.get('value', 1200):,}</code>\n"
    msg += f"🔄 <b>Retainer Định kỳ:</b> <code>${lead.get('retainer', 650):,}/tháng</code>\n"
    msg += f"⏰ <b>Thời gian:</b> {now_vn}\n\n"
    
    slug = lead["name"].lower().replace(" ", "_").replace("&", "and").replace("/", "-").replace("\\", "-").replace(",", "").replace(".", "")
    msg += f"🏛️ <a href='https://work-minh-lap.vercel.app/portal/{slug}'>Mở VIP Client Portal</a> | "
    msg += f"🧪 <a href='https://work-minh-lap.vercel.app/sandboxes/{slug}_sandbox.html'>Live Sandbox</a>\n"

    try:
        import urllib.request
        payload_data = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json; charset=utf-8"},
            data=payload_data
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            if r.status == 200:
                print("[✓] Dispatched CRM update alert to Telegram (@Minhpv_bot)!")
            else:
                print(f"[!] Telegram alert notice: status {r.status}")
    except Exception as e:
        print(f"[!] Telegram notification error: {e}")

def update_lead_status(lead_id, new_status, notify_tg=False):
    leads = load_pipeline()
    found = False
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    target_lead = None
    old_status = ""
    
    for l in leads:
        if l["id"] == lead_id:
            old_status = l["status"]
            l["status"] = new_status
            l["last_touch"] = now
            found = True
            target_lead = l
            print(f"[✓] Lead #{lead_id} ({l['name']}): Status updated from '{old_status}' -> '{new_status}' at {now}")
            break
            
    if found:
        save_pipeline(leads)
        if notify_tg and target_lead:
            send_telegram_alert(target_lead, old_status, new_status)
    else:
        print(f"[!] Lead #{lead_id} not found in CRM.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage B2B Client Pipeline CRM")
    parser.add_argument("--summary", action="store_true", help="Print pipeline summary")
    parser.add_argument("--id", type=int, help="Lead ID to update (1-60)")
    parser.add_argument("--status", choices=["new", "day1", "day3", "day7", "booked", "won"], help="New status for lead")
    parser.add_argument("--telegram", action="store_true", help="Send deal status alert to Telegram")

    args = parser.parse_args()

    if args.id and args.status:
        update_lead_status(args.id, args.status, notify_tg=args.telegram)
    else:
        print_summary()
