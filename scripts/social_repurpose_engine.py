"""
Autonomous Multi-Platform Social Content Repurposing Engine
------------------------------------------------------------
Tự động chuyển đổi các bài viết chuyên sâu hoặc chủ đề công nghệ thành:
1. Twitter / X Viral Thread (5-7 tweets)
2. LinkedIn Thought Leadership Post
3. 60-Second YouTube Shorts / TikTok Script
4. Reddit Community Discussion (r/SaaS, r/Entrepreneur)
"""

import sys
import os
import argparse
import urllib.request
import json
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CONTENT_PRESETS = {
    "geo_audit": {
        "title": "Why 90% of Websites are Invisible to ChatGPT and Perplexity Search",
        "hook": "Search is dead. AI Discovery is the new Google. If your robots.txt or schema isn't configured for LLM bots, you are losing 40% of future traffic.",
        "points": [
            "Traditional Google SEO relies on backlinks and H1 tags. Generative engines (ChatGPT Search, Perplexity) rely on LLM crawlers like GPTBot and PerplexityBot.",
            "If your robots.txt inadvertently disallows GPTBot, you are completely omitted from AI citations.",
            "LLMs require deep JSON-LD Schema (Organization, WebSite, FAQPage, SoftwareApplication) to extract factual confidence scores.",
            "Our audit tool SynapseGEO (https://synapse-geo-audit.vercel.app) found that 68% of local businesses have zero structured data for voice assistants.",
            "The fix takes 5 minutes: update robots.txt permissions and embed structured Schema markup."
        ],
        "cta": "Check your domain's AI Search score in 10 seconds: https://synapse-geo-audit.vercel.app"
    },
    "ai_automation": {
        "title": "How a Local Dentist Recovers $8,400/mo Using a 15-Minute AI Bot",
        "hook": "Most clinics lose their highest-value patients between 7 PM and 8 AM. Here is how simple AI workflows fix this instantly.",
        "points": [
            "Patients browsing cosmetic procedures (implants, invisalign) after dinner don't want to wait until 9 AM tomorrow for front desk callback.",
            "If competitors answer and lock down a calendar appointment in 30 seconds, you lose the patient forever.",
            "We deployed a conversational AI assistant that answers pricing, verifies insurance eligibility, and writes directly to Google Calendar.",
            "Result: 14 new booked consultations in month one, with zero manual staff hours.",
            "You can test the exact interactive patient experience here: https://work-minh-lap.vercel.app/chatbotdemo"
        ],
        "cta": "Explore the full AI Automation Playbook & blueprints at https://work-minh-lap.vercel.app/blog"
    },
    "microsaas_blueprint": {
        "title": "How to Build and Launch a Micro-SaaS in 7 Days with Zero Funding",
        "hook": "You don't need a team of 10 engineers or $100k in VC money to launch software that prints $2,000/month.",
        "points": [
            "Find a narrow, unglamorous problem: e.g. Robots.txt audit, review response generation, or headline scoring.",
            "Keep the tech stack dead simple: Vanilla HTML/JS, serverless edge functions on Vercel, and Lemon Squeezy for global payments.",
            "Build in 48 hours: Focus on one killer feature that gives value in under 10 seconds.",
            "Launch on Product Hunt, Hacker News (Show HN), and Reddit r/SaaS with honest, transparent copy.",
            "Turn free users into paying subscribers by offering deep reports, API access, and PDF exports."
        ],
        "cta": "Download the complete 16,000-word AI Money Blueprint eBook & Bundle at https://work-minh-lap.vercel.app/bundle"
    },
    "review_management": {
        "title": "How Local Businesses Turn 1-Star Google Reviews into 5-Star Loyalty with AI",
        "hook": "Unanswered 1-star reviews on Google Maps destroy up to 30% of foot traffic. Here is how autonomous AI review responder workflows solve this in 5 seconds.",
        "points": [
            "88% of consumers read reviews before choosing a local service, doctor, or restaurant.",
            "Leaving negative reviews without prompt empathetic answers signals neglect to potential buyers.",
            "We built ReviewGenius AI — an autonomous responder that validates customer sentiment, crafts de-escalating replies, and offers resolution vouchers in 5 seconds.",
            "It boosts local SEO ranking factors by embedding natural keywords into positive review responses.",
            "You can test ReviewGenius live on the web: https://work-minh-lap.vercel.app/reviewgenius"
        ],
        "cta": "Test ReviewGenius AI live on the web: https://work-minh-lap.vercel.app/reviewgenius"
    },
    "client_vip_portal": {
        "title": "Why We Stopped Sending PDF Proposals and Started Giving Clients Dedicated Software Portals",
        "hook": "PDF proposals get lost in inboxes and compared on price. When you send clients a live branded software portal with real-time AI uptime and a 5-day roadmap, price objections vanish.",
        "points": [
            "Traditional agency proposals take 4 hours to write and have a 15% close rate.",
            "A dedicated VIP Command Portal features live AI Copilot SLA monitoring, a 1-click HTML embed tag, and certified deliverable vaults.",
            "Clients see their own logo, customized industry prompts, and a quantified revenue recovery counter ($13,500/mo bleed).",
            "Retainers transform from a recurring expense into an indispensable software infrastructure asset.",
            "Explore our central VIP Hub with 30 live client portals: https://work-minh-lap.vercel.app/portal"
        ],
        "cta": "Explore the Executive Client VIP Command Hub at https://work-minh-lap.vercel.app/portal"
    },
    "make_automation_secrets": {
        "title": "5 Make.com Automation Blueprints That Make $1,000/Month on Autopilot",
        "hook": "You don't need to write thousands of lines of code to build high-value software systems. Here are 5 no-code automation workflows SMBs eagerly pay $500–$1,500 for.",
        "points": [
            "Workflow 1: Instant Speed-to-Lead SMS (<30s response time).",
            "Workflow 2: Automated Google Review Response & Sentiment Router.",
            "Workflow 3: Multi-Platform Social Content Repurposing (Blog to X, LinkedIn, TikTok).",
            "Workflow 4: Two-Way Calendar Booking & No-Show Eliminator.",
            "Workflow 5: Stripe/Lemon Squeezy Order Fulfillment & Telegram Sales Dispatcher."
        ],
        "cta": "Download the complete 15-Blueprint Pack at https://work-minh-lap.vercel.app/bundle"
    }
}

def generate_social_kit(topic_key="geo_audit"):
    data = CONTENT_PRESETS.get(topic_key, CONTENT_PRESETS["geo_audit"])
    out_dir = Path(__file__).resolve().parent.parent / "projects" / "ai_content_social" / "repurposed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"content_kit_{topic_key}.md"

    md = f"""# 🚀 Viral Content Repurposing Kit: {data['title']}
> **Tạo lúc**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Chủ đề chính**: `{topic_key}`

---

## 🐦 1. Twitter / X Viral Thread (7 Tweets)

**Tweet 1 (Hook)**:
{data['hook']}

Here is the exact breakdown of why this happens (and how to fix it in 5 mins) 🧵👇

---

**Tweet 2**:
1/ {data['points'][0]}

Most founders don't realize Google Search CTR dropped 28% year-over-year as users switch to direct conversational answers.

---

**Tweet 3**:
2/ {data['points'][1]}

Check your `/robots.txt` right now. If it has `User-agent: * Disallow: /`, you are actively telling Perplexity and ChatGPT: "Don't recommend my product."

---

**Tweet 4**:
3/ {data['points'][2]}

Without structured JSON-LD schemas, LLMs hallucinate your pricing and features. With Schema, you become the canonical source.

---

**Tweet 5**:
4/ {data['points'][3]}

The gap between businesses adopting AI search readiness vs traditional SEO is where the biggest traffic arbitrage exists in 2026.

---

**Tweet 6 (Key Takeaway)**:
5/ {data['points'][4]}

Don't wait for your competitors to take the top recommendation slot on voice assistants.

---

**Tweet 7 (Call to Action)**:
{data['cta']}

RT the first tweet if you found this valuable! 🔄

---

## 💼 2. LinkedIn Thought Leadership Post

```text
{data['hook']}

Over the past 6 months, we observed a massive shift in how high-intent buyers discover software and service providers.

Here are 3 critical observations every founder and marketer needs to know:

🔹 1. Search Behavior Shift:
{data['points'][0]}

🔹 2. The Invisible Technical Blocker:
{data['points'][1]}

🔹 3. The Unfair Advantage:
{data['points'][2]}

💡 Bottom line:
{data['points'][4]}

👉 {data['cta']}

What is your take on generative search vs traditional Google SEO? Let's discuss in the comments below.
```

---

## 🎬 3. 60-Second YouTube Shorts / TikTok Script

- **Visual Hook (0-5s)**: [Show screen recording of ChatGPT recommending a business, then pan to camera]  
  **Audio**: "Stop wasting thousands on traditional SEO until you fix this one setting on your website!"
- **The Problem (5-20s)**: [Show red alert on robots.txt audit screen]  
  **Audio**: "{data['hook']}"
- **The Breakdown (20-40s)**: [Show clean, fast UI of SynapseGEO running audit]  
  **Audio**: "When AI crawlers scan your site, they look for structured Schema. If you don't have it, Perplexity and ChatGPT will recommend your competitor instead."
- **The Solution & CTA (40-60s)**: [Show 1-click audit score]  
  **Audio**: "It takes 30 seconds to check your score. Link is pinned in the comments or bio!"

---

## 💬 4. Reddit Discussion Starter (r/SaaS / r/Entrepreneur)

**Title**: {data['title']}

**Body**:
Hey everyone,

I spent the last 3 months analyzing how generative engines like ChatGPT Search and Perplexity actually decide which SaaS tools and services to cite when users ask for recommendations.

A few surprising findings:
- {data['points'][0]}
- {data['points'][1]}
- {data['points'][2]}

We built a lightweight open tool to check this: {data['cta']}

Would love to hear how other founders here are preparing for AI search traffic. Are you noticing a decline in organic Google referrals yet?
"""

    out_file.write_text(md, encoding="utf-8")
    print(f"[✓] Created viral content kit: {out_file.name}")
    return out_file

def send_telegram_social_digest(topic_key, data):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    html_msg = f"""📱 <b>[VIRAL SOCIAL CONTENT KIT READY]</b>

🎯 <b>Chủ đề:</b> <code>{data['title']}</code>
📌 <b>Topic Key:</b> <code>{topic_key}</code>

🐦 <b>Twitter / X Thread Hook:</b>
<i>{data['hook']}</i>

💼 <b>Key Insights:</b>
• {data['points'][0]}
• {data['points'][1]}

🔗 <b>Call-to-Action Link:</b>
<code>{data['cta']}</code>

👉 <i>Trọn bộ 4 định dạng (X, LinkedIn, Shorts, Reddit) đã lưu tại projects/ai_content_social/repurposed/content_kit_{topic_key}.md</i>"""

    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status == 200:
                print(f"[✓] Đã gửi thông báo gói nội dung '{topic_key}' về Telegram!")
    except Exception as e:
        print(f"[!] Lỗi gửi Telegram: {e}")

def generate_all_social_kits(send_telegram=False):
    print("=" * 75)
    print("🚀 GENERATING ALL 6 MULTI-PLATFORM SOCIAL VIRAL CONTENT KITS")
    print("=" * 75)
    for k in CONTENT_PRESETS.keys():
        generate_social_kit(k)
        if send_telegram:
            send_telegram_social_digest(k, CONTENT_PRESETS[k])
    print("-" * 75)
    print("🎉 SUCCESS: All 6 viral social kits generated in projects/ai_content_social/repurposed/")
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Platform Social Repurposing Engine")
    parser.add_argument("--topic", default="geo_audit", choices=list(CONTENT_PRESETS.keys()), help="Content topic")
    parser.add_argument("--all", action="store_true", help="Generate all 6 viral content kits")
    parser.add_argument("--telegram", action="store_true", help="Send social kit preview to Telegram")
    args = parser.parse_args()

    if args.all:
        generate_all_social_kits(send_telegram=args.telegram)
    else:
        generate_social_kit(args.topic)
        if args.telegram:
            send_telegram_social_digest(args.topic, CONTENT_PRESETS[args.topic])
