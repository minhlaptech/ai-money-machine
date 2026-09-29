#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — Autonomous Social Media Post Scheduler & Bulk Exporter
-------------------------------------------------------------------------
Parses the 10 multi-platform repurposed content kits and provides:
1. Universal CSV export for bulk scheduling in Buffer, Metricool, or Hootsuite
2. JSON content database for the Command Center web dashboard
3. 1-Tap mobile publishing to Telegram (@Minhpv_bot) with copy-paste ready text
"""

import sys
import os
import re
import csv
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
REPURPOSED_DIR = ROOT / "projects" / "ai_content_social" / "repurposed"
SOCIAL_DIR = ROOT / "projects" / "ai_content_social"

def parse_all_content_kits():
    """Extract structured data from all 10 content kits"""
    kits = []
    files = sorted(list(REPURPOSED_DIR.glob("content_kit_*.md")))
    for f in files:
        text = f.read_text(encoding="utf-8")
        title_m = re.search(r"#\s*🚀\s*Viral Content Repurposing Kit:\s*(.*?)\n", text)
        topic_m = re.search(r">\s*\*\*Chủ đề chính\*\*:\s*`?(.*?)`?\n", text)
        title = title_m.group(1).strip() if title_m else f.stem
        topic = topic_m.group(1).strip() if topic_m else f.stem

        # Extract Twitter
        tw_sec = text.split("## 🐦 1. Twitter / X Viral Thread")[-1].split("## 💼 2. LinkedIn")[0] if "## 💼 2. LinkedIn" in text else ""
        tweets = []
        tw_matches = re.findall(r"\*\*Tweet \d+.*?\*\*:\n(.*?)(?=\n\*\*Tweet|\n---|\Z)", tw_sec, re.DOTALL)
        for tm in tw_matches:
            c = tm.strip().strip("-").strip()
            if c:
                tweets.append(c)

        # Extract LinkedIn
        li_sec = text.split("## 💼 2. LinkedIn Thought Leadership Post")[-1].split("## 🎬 3. 60-Second")[0] if "## 🎬 3. 60-Second" in text else ""
        li_code = re.search(r"```text\n(.*?)```", li_sec, re.DOTALL)
        linkedin_post = li_code.group(1).strip() if li_code else li_sec.strip()

        # Extract TikTok/Shorts
        tt_sec = text.split("## 🎬 3. 60-Second YouTube Shorts / TikTok Script")[-1].split("## 👾 4. Reddit")[0] if "## 👾 4. Reddit" in text else ""
        tiktok_script = tt_sec.strip()

        # Extract Reddit
        rd_sec = text.split("## 👾 4. Reddit Discussion Starter")[-1] if "## 👾 4. Reddit" in text else ""
        rd_code = re.search(r"```text\n(.*?)```", rd_sec, re.DOTALL)
        reddit_post = rd_code.group(1).strip() if rd_code else rd_sec.strip()

        kits.append({
            "topic": topic,
            "title": title,
            "filename": f.name,
            "tweets": tweets,
            "linkedin": linkedin_post,
            "tiktok": tiktok_script,
            "reddit": reddit_post
        })
    return kits

def export_buffer_csv(kits):
    """Generate Buffer / Metricool compatible bulk schedule CSV"""
    out_csv = SOCIAL_DIR / "buffer_schedule.csv"
    start_date = datetime.now() + timedelta(days=1)
    rows = []

    for idx, kit in enumerate(kits):
        # Day 1: LinkedIn post at 09:00
        post_time_li = (start_date + timedelta(days=idx*3)).strftime("%Y-%m-%d 09:00")
        rows.append({
            "Date": post_time_li,
            "Text": kit["linkedin"],
            "Platform": "LinkedIn",
            "Topic": kit["topic"]
        })

        # Day 2: Twitter Thread Hook at 14:00
        post_time_tw = (start_date + timedelta(days=idx*3 + 1)).strftime("%Y-%m-%d 14:00")
        tw_thread_text = "\n\n---\n\n".join(kit["tweets"])
        rows.append({
            "Date": post_time_tw,
            "Text": tw_thread_text,
            "Platform": "Twitter/X",
            "Topic": kit["topic"]
        })

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Text", "Platform", "Topic"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"[✓] Exported Buffer CSV schedule: {out_csv} ({len(rows)} posts planned across 30 days)")
    return out_csv

def export_json_database(kits):
    """Generate JSON content database for UI dashboard"""
    out_json = SOCIAL_DIR / "social_content_hub.json"
    out_json.write_text(json.dumps(kits, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[✓] Exported Social Content Database: {out_json} ({len(kits)} topics)")
    return out_json

def send_telegram_topic(kit):
    """Send a single topic's copy-paste post package to Telegram"""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    # Format Telegram message
    html_msg = f"""📱 <b>[SOCIAL MEDIA 1-CLICK DISPATCH]</b>
🎯 <b>Chủ đề:</b> <code>{kit['topic']}</code>
📝 <b>Tiêu đề:</b> <i>{kit['title']}</i>

💼 <b>LINKEDIN POST (Chạm để sao chép):</b>
<code>{kit['linkedin'][:1200]}...</code>

🐦 <b>TWITTER HOOK:</b>
<code>{kit['tweets'][0] if kit['tweets'] else ''}</code>

👉 <i>Dán trực tiếp lên LinkedIn / X để kéo traffic tự nhiên về hệ thống!</i>"""

    tmp = ROOT / "temp_social_tg.json"
    tmp.write_text(json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}, ensure_ascii=False), encoding="utf-8")
    try:
        res = subprocess.run(
            ["curl.exe", "-s", "-X", "POST",
             "-H", "Content-Type: application/json; charset=utf-8",
             "--data-binary", f"@{tmp.name}",
             f"https://api.telegram.org/bot{bot_token}/sendMessage"],
            capture_output=True, text=True, timeout=10, cwd=str(ROOT)
        )
        if '"ok":true' in res.stdout:
            print(f"[✓] Đã bắn gói bài viết '{kit['topic']}' về Telegram (@Minhpv_bot)!")
        else:
            print(f"[!] Lỗi gửi Telegram: {res.stdout}")
    except Exception as e:
        print(f"[!] Lỗi: {e}")
    finally:
        if tmp.exists():
            tmp.unlink()

def main():
    parser = argparse.ArgumentParser(description="Autonomous Social Post Scheduler")
    parser.add_argument("--export-csv", action="store_true", help="Generate Buffer / Metricool CSV")
    parser.add_argument("--export-json", action="store_true", help="Generate JSON hub database")
    parser.add_argument("--telegram", action="store_true", help="Send topic to Telegram")
    parser.add_argument("--topic", help="Specific topic name (e.g. geo_audit, microsaas_blueprint)")
    args = parser.parse_args()

    kits = parse_all_content_kits()
    print("=" * 70)
    print(f"📱 AI MONEY MACHINE — SOCIAL CONTENT SCHEDULER ({len(kits)} KITS)")
    print("=" * 70)

    if args.export_csv or (not args.telegram and not args.export_json):
        export_buffer_csv(kits)

    if args.export_json or (not args.telegram and not args.export_csv):
        export_json_database(kits)

    if args.telegram:
        target = None
        if args.topic:
            target = next((k for k in kits if args.topic in k["topic"]), None)
        if not target and kits:
            target = kits[0] # Default to first topic
        if target:
            send_telegram_topic(target)

    print("=" * 70)

if __name__ == "__main__":
    main()
