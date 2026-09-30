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
            "Our audit tool SynapseGEO (https://work-minh-lap.vercel.app/synapsegeo) found that 68% of local businesses have zero structured data for voice assistants.",
            "The fix takes 5 minutes: update robots.txt permissions and embed structured Schema markup."
        ],
        "cta": "Check your domain's AI Search score in 10 seconds: https://work-minh-lap.vercel.app/synapsegeo"
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
        "cta": "Download the complete 15-Blueprint Pack at https://work-minh-lap.vercel.app/bundle",
        "shorts_hook": "Here are 5 automation workflows that businesses happily pay $1,500 for!",
        "shorts_visual": "[Show Make.com canvas with glowing animated webhook nodes connecting to Telegram]",
        "reddit_sub": "r/nocode, r/automation, r/Entrepreneur",
        "reddit_question": "Which tedious task inside your business are you dying to automate next?"
    },
    "affiliate_partner_engine": {
        "title": "How We Pay Creators 50% Instant SaaS & 20% Recurring Retainer Commissions",
        "hook": "Stop promoting $2 Amazon affiliate links that pay 30 cents. The real affiliate money in 2026 is high-ticket AI software and SMB automation retainers.",
        "points": [
            "Most affiliate programs pay 5-10% with 30-day payout delays and high clawbacks.",
            "Our Partner Program pays 50% upfront ($14.50 - $19.50) on digital bundles and SaaS tools.",
            "For SMB retainers, partners earn 20% recurring ($300 - $700 upfront + $100-$300/mo passive MRR) per referred client.",
            "Every partner gets real-time link tracking with 30-day cookie persistence and ready-to-copy promo swipes.",
            "You don't need a massive audience — just send targeted traffic using our 4-platform swipe vault."
        ],
        "cta": "Join the MinhLap AI Partner Network today: https://work-minh-lap.vercel.app/referral",
        "shorts_hook": "How creators are making $300 to $700 per client without doing any fulfillment!",
        "shorts_visual": "[Show Affiliate Hub live calculator slider shifting from 1 to 10 clients]",
        "reddit_sub": "r/AffiliateMarketing, r/passive_income, r/SideProject",
        "reddit_question": "Are you focusing on low-ticket volume or high-ticket B2B software affiliate offers?"
    },
    "pod_developer_merch": {
        "title": "How I Made $2,400 Selling Cynical AI Hoodies & Desk Mats with Zero Inventory",
        "hook": "Tech merch usually sucks: cheesy clip art and corny puns. But when you target hyper-specific developer memes with cyberpunk aesthetics, conversion rates jump to 4.8%.",
        "points": [
            "The secret is extreme specificity: 'Heavy Canvas Automate Or Be Automated Tote' and 'Prompt Engineering Extended Desk Mat'.",
            "Zero inventory risk: We design high-res assets with Midjourney/Flux, then connect Printful to Etsy and Shopify via Make.com.",
            "Net profit margins average $10.00 to $16.50 per unit sold, shipped globally without ever touching a box.",
            "Every garment uses premium ring-spun cotton and structured embroidery for high perceived value.",
            "Automated order routing and tracking numbers eliminate 100% of customer support friction."
        ],
        "cta": "Explore our automated POD line and design mockups at https://work-minh-lap.vercel.app",
        "shorts_hook": "How I built a $2,400/mo print-on-demand store for programmers with zero inventory!",
        "shorts_visual": "[Show high-res cyberpunk deskmat and streetwear hoodie mockups]",
        "reddit_sub": "r/printondemand, r/SideProject, r/webdev",
        "reddit_question": "What's the best programmer inside joke or slogan you'd actually wear on a hoodie?"
    },
    "headline_iq_viral_hook": {
        "title": "Why 80% of Marketing Headlines Fail Before Anyone Reads the Second Line",
        "hook": "You have 1.8 seconds to capture attention on modern feeds. If your hook lacks curiosity, emotional tension, or specificity, your conversion rate is zero.",
        "points": [
            "HeadlineIQ tests your copy across 6 viral emotional vectors: FOMO, Urgency, Authority, Specificity, Story Hook, and Brevity.",
            "Headlines scoring above 85 out-click generic corporate headlines by 3.4x in A/B split tests.",
            "The tool instantly suggests 3 high-converting rewrites trained on top viral creator frameworks.",
            "Zero signup required: paste your draft title and get an instant audit score in 3 seconds.",
            "Use it for YouTube titles, cold email subject lines, Twitter threads, and landing page hero headers."
        ],
        "cta": "Test your headline score for free right now: https://work-minh-lap.vercel.app/headlineiq",
        "shorts_hook": "Your content isn't bad — your headline is just killing 80% of your clicks!",
        "shorts_visual": "[Show HeadlineIQ score gauge shooting from 42 to 94 with instant viral rewrites]",
        "reddit_sub": "r/copywriting, r/ContentMarketing, r/SaaS",
        "reddit_question": "What is the single highest-converting headline formula you've ever tested?"
    },
    "ai_freelancing_retainers": {
        "title": "How to Land $1,500/mo AI Automation Retainers on Upwork Without Writing Code",
        "hook": "Stop bidding $15/hr on data entry. Local clinics, real estate brokers, and law firms are desperately bleeding revenue from missed calls and manual data entry.",
        "points": [
            "Don't sell 'AI services' — sell 'Instant Speed-to-Lead Patient Recovery' or 'Zero-Missed-Call Inbound Router'.",
            "Send prospects a personalized interactive ROI calculator showing they lose $8,400/month from missed after-hours leads.",
            "Include a live sandbox demo link so the business owner tests the bot with their own business data before the call.",
            "Package it into a standard $1,500 setup fee + $500/mo maintenance retainer with a 14-day SLA guarantee.",
            "Our 30-Client Outreach Playbook contains exact swipe templates that achieved a 26% meeting booking rate."
        ],
        "cta": "Access the complete AI Automation Agency kit and ROI calculator at https://work-minh-lap.vercel.app/calculator",
        "shorts_hook": "Stop charging hourly on Upwork. Here is how to package $1,500/mo AI retainers instead!",
        "shorts_visual": "[Show Upwork $1,500 escrow funded notification + ROI calculator simulator]",
        "reddit_sub": "r/freelance, r/Upwork, r/agency",
        "reddit_question": "Have you transitioned from hourly rate billing to fixed-price value retainers yet?"
    }
}

def generate_social_kit(topic_key="geo_audit"):
    data = CONTENT_PRESETS.get(topic_key, CONTENT_PRESETS["geo_audit"])
    out_dir = Path(__file__).resolve().parent.parent / "projects" / "ai_content_social" / "repurposed"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"content_kit_{topic_key}.md"

    shorts_hook = data.get("shorts_hook", f"Here is what 90% of people get completely wrong about {topic_key}!")
    shorts_vis = data.get("shorts_visual", "[Show dynamic screen recording of the platform in action]")
    reddit_sub = data.get("reddit_sub", "r/SaaS, r/Entrepreneur, r/SideProject")
    reddit_q = data.get("reddit_question", "What has been your experience with this trend so far? Let's discuss!")

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

---

**Tweet 3**:
2/ {data['points'][1]}

---

**Tweet 4**:
3/ {data['points'][2]}

---

**Tweet 5**:
4/ {data['points'][3]}

---

**Tweet 6 (Key Takeaway)**:
5/ {data['points'][4]}

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

🔹 1. The Industry Shift:
{data['points'][0]}

🔹 2. The Core Problem:
{data['points'][1]}

🔹 3. The Unfair Advantage:
{data['points'][2]}

💡 Bottom line:
{data['points'][4]}

👉 {data['cta']}

{reddit_q}
```

---

## 🎬 3. 60-Second YouTube Shorts / TikTok Script

- **Visual Hook (0-5s)**: {shorts_vis}  
  **Audio**: "{shorts_hook}"
- **The Problem (5-20s)**: [Show pain point on screen]  
  **Audio**: "{data['hook']}"
- **The Breakdown (20-40s)**: [Demonstrate solution and rapid workflow]  
  **Audio**: "{data['points'][1]} {data['points'][2]}"
- **The Solution & CTA (40-60s)**: [Show instant result & call to action]  
  **Audio**: "{data['points'][4]} Link is pinned in the comments or bio!"

---

## 💬 4. Reddit Discussion Starter ({reddit_sub})

**Title**: {data['title']}

**Body**:
Hey everyone,

I spent the last several weeks analyzing how this market actually operates in 2026.

A few surprising findings:
- {data['points'][0]}
- {data['points'][1]}
- {data['points'][2]}
- {data['points'][3]}

We built a live asset around this: {data['cta']}

{reddit_q}
"""

    out_file.write_text(md, encoding="utf-8")
    print(f"[✓] Created viral content kit: {out_file.name}")
    return out_file

def send_telegram_social_digest(topic_key, data):
    import html
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    title_safe = html.escape(str(data['title']))
    hook_safe = html.escape(str(data['hook']))
    p0_safe = html.escape(str(data['points'][0]))
    p1_safe = html.escape(str(data['points'][1]))
    cta_safe = html.escape(str(data['cta']))

    html_msg = f"""📱 <b>[VIRAL SOCIAL CONTENT KIT READY]</b>

🎯 <b>Chủ đề:</b> <code>{title_safe}</code>
📌 <b>Topic Key:</b> <code>{topic_key}</code>

🐦 <b>Twitter / X Thread Hook:</b>
<i>{hook_safe}</i>

💼 <b>Key Insights:</b>
• {p0_safe}
• {p1_safe}

🔗 <b>Call-to-Action Link:</b>
<code>{cta_safe}</code>

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
    print("🚀 GENERATING ALL 10 MULTI-PLATFORM SOCIAL VIRAL CONTENT KITS")
    print("=" * 75)
    for k in CONTENT_PRESETS.keys():
        generate_social_kit(k)
        if send_telegram:
            send_telegram_social_digest(k, CONTENT_PRESETS[k])
    print("-" * 75)
    print("🎉 SUCCESS: All 10 viral social kits generated in projects/ai_content_social/repurposed/")
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Platform Social Repurposing Engine")
    parser.add_argument("--topic", default="geo_audit", choices=list(CONTENT_PRESETS.keys()), help="Content topic")
    parser.add_argument("--all", action="store_true", help="Generate all 10 viral content kits")
    parser.add_argument("--telegram", action="store_true", help="Send social kit preview to Telegram")
    args = parser.parse_args()

    if args.all:
        generate_all_social_kits(send_telegram=args.telegram)
    else:
        generate_social_kit(args.topic)
        if args.telegram:
            send_telegram_social_digest(args.topic, CONTENT_PRESETS[args.topic])
