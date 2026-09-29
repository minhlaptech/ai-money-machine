"""
YouTube SEO & Metadata Suite Generator
---------------------------------------
Tự động tạo bộ Tiêu đề giật gân (CTR-optimized), Mô tả chuẩn SEO kèm mốc thời gian (Timestamps),
Thẻ Tags tìm kiếm và Bình luận ghim (Pinned Comment) cho từng video trong kênh Faceless YouTube.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

VIDEO_METADATA_PRESETS = {
    "video_001": {
        "title": "5 AI Tools That Can Make You $1000/Month in 2026 (No Experience Needed)",
        "summary": "Discover 5 high-income AI tools you can start using today to build an extra $1,000/month in digital cash flow. No coding, no big audience, and no prior experience needed.",
        "alt_titles": [
            "How to Make $1,000/Month with AI in 2026 (5 Free Tools)",
            "5 AI Tools That Pay You in 2026 (Beginner's Blueprint)",
            "How I Make $1,000/Mo with Free AI Tools (Full Guide)"
        ],
        "timestamps": [
            "00:00 - The $1,000/Mo AI Opportunity in 2026",
            "01:15 - Tool 1: AI Prompt Engineering Packs",
            "03:40 - Tool 2: Autonomous Local SEO Audits (SynapseGEO)",
            "06:10 - Tool 3: 24/7 AI Customer Support Chatbots",
            "08:35 - Tool 4: Viral Social Media Repurposing",
            "10:50 - Tool 5: Micro-SaaS Software Distribution",
            "12:30 - How to Package All 5 into One AI Money Machine"
        ],
        "links": [
            ("🎁 The AI Empire Master Bundle ($39)", "https://work-minh-lap.vercel.app/bundle"),
            ("⚡ SynapseGEO AI SEO Audit Tool", "https://work-minh-lap.vercel.app/synapsegeo"),
            ("🤖 Interactive Chatbot Portfolio Demo", "https://work-minh-lap.vercel.app/chatbotdemo"),
            ("📚 AI Resource Hub & Free Guides", "https://work-minh-lap.vercel.app/blog"),
            ("🤝 Affiliate Partner Program (50% RevShare)", "https://work-minh-lap.vercel.app/referral")
        ],
        "tags": [
            "ai tools 2026", "make money with ai", "ai side hustles", "chatgpt business ideas",
            "passive income ai", "indie hacker tools", "how to make money with chatgpt", "ai automation",
            "best ai tools 2026", "ai freelancing", "work from home ai", "digital products ai"
        ],
        "pinned_comment": "🎁 Claim the complete AI Empire Master Bundle & 15 automation blueprints here: https://work-minh-lap.vercel.app/bundle\n\nTest the live SynapseGEO AI audit tool: https://work-minh-lap.vercel.app/synapsegeo\n\nWhich of these 5 tools are you most excited to try this week? Drop a comment below! 👇"
    },
    "video_002": {
        "title": "I Built an AI Chatbot in 15 Minutes That Handles 1000 Customer Questions",
        "summary": "Watch me build a production-grade AI support and appointment booking chatbot in 15 minutes that handles thousands of customer inquiries 24/7 with zero human latency.",
        "alt_titles": [
            "How to Build an AI Chatbot for Small Business (15 Mins)",
            "Zero-Code AI Chatbot That Books Appointments 24/7",
            "How I Charge $500 for a 15-Minute AI Chatbot Setup"
        ],
        "timestamps": [
            "00:00 - The 24/7 AI Support Problem",
            "01:20 - Step 1: Knowledge Base Ingestion & Training",
            "03:50 - Step 2: Designing Guardrails & Booking Triggers",
            "07:10 - Step 3: 1-Line Embed Code Installation",
            "09:40 - Step 4: Testing Live Conversions & Telegram Alerts",
            "11:30 - How to Sell This to Local Businesses for $500+"
        ],
        "links": [
            ("🤖 Test the Live Interactive Chatbot Demo", "https://work-minh-lap.vercel.app/chatbotdemo"),
            ("🧮 Interactive AI Revenue Recovery Calculator", "https://work-minh-lap.vercel.app/calculator"),
            ("🏛️ Explore 30 Client VIP Portals", "https://work-minh-lap.vercel.app/portal"),
            ("🎁 Grab The Complete AI Bundle", "https://work-minh-lap.vercel.app/bundle")
        ],
        "tags": [
            "ai chatbot tutorial", "how to build an ai chatbot", "botpress tutorial", "voiceflow tutorial",
            "ai receptionist", "small business automation", "lead capture chatbot", "ai customer support",
            "chatgpt api chatbot", "make money with chatbots", "no-code ai"
        ],
        "pinned_comment": "🤖 Test the live interactive chatbot portfolio demo right here: https://work-minh-lap.vercel.app/chatbotdemo\n\nCalculate how much revenue missed inquiries cost your business: https://work-minh-lap.vercel.app/calculator\n\nWhat business niche should we build an AI chatbot for next? Let me know below! 👇"
    },
    "video_003": {
        "title": "How I Automated a Small Business and Made $500 (Step-by-Step with Make.com)",
        "summary": "Real client case study: How I saved a dental clinic 15+ hours a week on patient intake and appointment reminders with Make.com and charged $500 for an afternoon of work.",
        "alt_titles": [
            "Make.com Beginner Tutorial: How I Made $500 in 1 Day",
            "How to Automate Any Small Business with No-Code AI",
            "The $500 Afternoon: Make.com Client Automation Blueprint"
        ],
        "timestamps": [
            "00:00 - The $500 Client Automation Case Study",
            "01:45 - The Problem: 3 Hours/Day Lost on Admin Chasing",
            "04:10 - Building the Speed-to-Lead Webhook Trigger",
            "07:20 - Connecting SMS & Calendar Booking API",
            "10:15 - Handing Off the Deliverable to the Client",
            "12:00 - How to Price & Package Automation Services"
        ],
        "links": [
            ("📦 Download All 15 Make.com Automation Blueprints", "https://work-minh-lap.vercel.app/bundle"),
            ("🧮 Dynamic Client ROI Simulator", "https://work-minh-lap.vercel.app/calculator"),
            ("🖥️ 30 Client Sales Pitch Decks Showcase", "https://work-minh-lap.vercel.app/pitches"),
            ("📚 AI Resource Hub & Guides", "https://work-minh-lap.vercel.app/blog")
        ],
        "tags": [
            "make.com tutorial", "make.com for beginners", "business automation", "no-code automation",
            "how to make money with make.com", "zapier alternative", "ai automation agency", "client automation case study",
            "smb automation", "speed to lead"
        ],
        "pinned_comment": "📦 Import all 15 ready-to-run Make.com & n8n JSON blueprints into your account: https://work-minh-lap.vercel.app/bundle\n\nRun the client ROI numbers: https://work-minh-lap.vercel.app/calculator\n\nHave you tried building on Make.com yet? Drop any questions below! 👇"
    },
    "video_004": {
        "title": "I Built 3 AI Products in One Day — Here's How (and How Much They'll Earn)",
        "summary": "Watch me build, package, and launch 3 complete digital products in 24 hours: a 16,000-word eBook, an AI prompt pack, and an automation template kit.",
        "alt_titles": [
            "Building 3 Digital Products in 24 Hours with AI",
            "How to Create & Sell Digital Products with AI in 2026",
            "From $0 to 3 Digital Assets in 1 Day (Full Income Breakdown)"
        ],
        "timestamps": [
            "00:00 - The 24-Hour Digital Product Challenge",
            "02:00 - Product 1: The 16,000-Word eBook Blueprint",
            "05:15 - Product 2: The 110+ High-Converting Prompt Pack",
            "08:30 - Product 3: The 15 Make.com Automation Bundle",
            "11:45 - Packaging on Lemon Squeezy & Setting Up Global Payments",
            "14:10 - Projected Monthly Revenue Breakdown"
        ],
        "links": [
            ("🎁 The AI Empire Master Bundle ($39)", "https://work-minh-lap.vercel.app/bundle"),
            ("🤝 Earn 50% Commission as an Affiliate Partner", "https://work-minh-lap.vercel.app/referral"),
            ("📚 Read Free Chapters on the AI Hub", "https://work-minh-lap.vercel.app/blog")
        ],
        "tags": [
            "digital products ai", "build in public", "create digital products with chatgpt", "sell ebooks online",
            "gumroad digital products", "lemon squeezy tutorial", "passive income digital products",
            "make money selling prompts", "ai templates", "solopreneur 2026"
        ],
        "pinned_comment": "🎁 Claim the 3-in-1 Master Bundle built in this video: https://work-minh-lap.vercel.app/bundle\n\nWant to promote this bundle and earn 50% commission? Join our partner program: https://work-minh-lap.vercel.app/referral\n\nWhich digital product idea are you creating this weekend? Tell me below! 👇"
    },
    "video_006": {
        "title": "How to Start an AI Automation Agency (AAA) in 2026 ($0 to $3,000/mo Retainers)",
        "summary": "Step-by-step roadmap to start your own AI Automation Agency in 2026 with zero coding, land high-ticket local business clients, and build recurring monthly retainers ($1,500 setup + $650/mo).",
        "alt_titles": [
            "How I Built an AI Agency with Zero Coding ($3,000/Month Retainers)",
            "The AI Automation Agency (AAA) Blueprint for 2026: Step-by-Step",
            "How to Make $3,000/Month with AI Chatbots (Beginner's Guide)"
        ],
        "timestamps": [
            "00:00 - The $3,000/Month Agency Opportunity in 2026",
            "02:00 - Why Most AI Agencies Fail (The Pain Point Pivot)",
            "04:30 - Building Your Proof-of-Work Demo (Under 30 Mins)",
            "07:15 - The 3 High-Ticket Niches That Pay Fast",
            "10:00 - The 1-Click Cold Email Framework (35% Reply Rate)",
            "12:40 - Pricing Strategy: $1,500 Setup + $750/Mo Retainer",
            "14:30 - Free Starter Kit & Automation Templates"
        ],
        "links": [
            ("🤖 Interactive Chatbot Portfolio Demo", "https://work-minh-lap.vercel.app/chatbotdemo"),
            ("📖 Free eBook 'The AI Money Blueprint' (16,000 words)", "https://work-minh-lap.vercel.app/blog"),
            ("⚡ SynapseGEO AI Search Engine Audit Tool", "https://work-minh-lap.vercel.app/synapsegeo"),
            ("🏛️ Executive VIP Client Portals Hub", "https://work-minh-lap.vercel.app/portal")
        ],
        "tags": [
            "ai automation agency", "how to start an ai agency", "aaa blueprint 2026",
            "make money with ai", "ai chatbot agency", "voiceflow tutorial", "botpress tutorial",
            "smb automation", "cold email for ai agency", "ai freelancing", "ai side hustle",
            "passive income 2026", "chatgpt business ideas", "indie hacker", "microsaas"
        ],
        "pinned_comment": "👉 Test the live interactive client chatbot demo here: https://work-minh-lap.vercel.app/chatbotdemo\n\nDownload our complete 16,000-word eBook & 15 automation templates for free at https://work-minh-lap.vercel.app/blog !\n\nDrop a comment: Which local niche are you planning to target first? 👇"
    },
    "video_005": {
        "title": "How to Build & Monetize a Micro-SaaS with AI in 2026 (No Coding Required)",
        "alt_titles": [
            "I Built a Micro-SaaS in 48 Hours with AI (Step-by-Step)",
            "How to Build a $1,000/Mo Software Business as a Solo Founder",
            "Micro-SaaS with AI: Zero Coding, Free Hosting, Real Revenue"
        ],
        "timestamps": [
            "00:00 - The Micro-SaaS Opportunity in 2026",
            "01:45 - Step 1: Finding High-Intent Problems",
            "04:10 - Step 2: Building the MVP with AI in 60 Mins",
            "07:20 - Step 3: Zero-Cost Hosting & Global Deployment",
            "09:15 - Step 4: Setting Up International Payments",
            "11:00 - Step 5: The 7-Day Distribution Blueprint",
            "12:50 - Free Resource & Next Steps"
        ],
        "links": [
            ("🌐 Live Micro-SaaS Demo (SynapseGEO)", "https://work-minh-lap.vercel.app/synapsegeo"),
            ("📖 The AI Money Blueprint eBook", "https://minhlap.gumroad.com/l/xqckmu"),
            ("📚 AI Resource Hub & Free Guides", "https://ai-automation-guide-omega.vercel.app")
        ],
        "tags": [
            "microsaas", "micro saas ai", "build saas with ai", "chatgpt coding",
            "solo founder", "indie hacker saas", "lemonsqueezy store", "vercel edge",
            "passive income software", "ai money machine", "seo audit tool"
        ],
        "pinned_comment": "🛠️ Test the live Micro-SaaS tool we built in this video: https://work-minh-lap.vercel.app/synapsegeo\n\nGet the complete 16,000-word launch blueprint here: https://minhlap.gumroad.com/l/xqckmu\n\nWhat micro-tool idea are you building next? Let me know below!"
    },
    "video_007": {
        "title": "How to Build a $1,000/Month AI Print-on-Demand Store in 2026 (Etsy + Printify)",
        "alt_titles": [
            "AI Print on Demand in 2026: Step-by-Step for Beginners ($18 Profit per Hoodie)",
            "How I Built a Passive $1,000/Mo Etsy Store Using AI Art & Printify",
            "The 2026 AI Print-on-Demand Blueprint (Zero Inventory, Hands-Off Fulfillment)"
        ],
        "timestamps": [
            "00:00 - The Truth About Print-on-Demand in 2026",
            "01:45 - Step 1: High-Passion, High-Spend Niche Strategy",
            "04:15 - Step 2: Generating Commercial Vector Art with AI",
            "07:00 - Step 3: Setting Up Printify & Margin Optimization ($18 Net)",
            "09:30 - Step 4: The 13-Tag Etsy SEO Algorithm Formula",
            "12:10 - Step 5: Automating Orders to 100% Hands-Off Fulfillment",
            "13:45 - Free Design Templates & Download Links"
        ],
        "links": [
            ("📖 The AI Money Blueprint eBook", "https://minhlap.gumroad.com/l/xqckmu"),
            ("🎯 110+ AI Marketing Prompts Pack", "https://minhlap.gumroad.com"),
            ("🎁 The AI Empire Master Bundle ($39)", "https://minhlap.lemonsqueezy.com"),
            ("📚 AI Resource Hub & Free Guides", "https://ai-automation-guide-omega.vercel.app")
        ],
        "tags": [
            "print on demand ai", "etsy print on demand 2026", "printify tutorial", "midjourney for print on demand",
            "etsy seo tags", "ai side hustle 2026", "how to sell on etsy with ai", "passive income print on demand",
            "tech merchandise", "programmer hoodie", "ai art for commercial use", "etsy digital store"
        ],
        "pinned_comment": "👕 Download our complete Print-on-Demand listing generator & prompt guide inside our free resource vault: https://ai-automation-guide-omega.vercel.app\n\nGrab the 16,000-word launch blueprint eBook: https://minhlap.gumroad.com/l/xqckmu\n\nWhich niche are you building for: Tech, Gaming, or Fitness? Drop a comment below! 👇"
    },
    "video_008": {
        "title": "How to Make $5,000/Month as an AI Freelancer in 2026 (Zero Prior Experience)",
        "alt_titles": [
            "The 2026 AI Freelancing Blueprint: From $0 to $5,000/Month",
            "How to Charge $95/Hour on Upwork as an AI Automation Architect",
            "Make $5,000/Mo Freelancing with AI (No Coding, No Degree Needed)"
        ],
        "timestamps": [
            "00:00 - The $5,000/Month Freelancing Shift in 2026",
            "01:50 - Step 1: The 3 Highest-Paying AI Services in Demand",
            "04:30 - Step 2: The Proof-First Profile Setup on Upwork & Fiverr",
            "07:15 - Step 3: Landing Your First 3 Clients Without Reviews",
            "10:00 - Step 4: The 40% Interview Rate Cover Letter Formula",
            "12:30 - Step 5: Escalating from Hourly to Recurring Retainers",
            "14:20 - Free Freelancing Starter Kit & Tools"
        ],
        "links": [
            ("💼 Upwork Mastery Kit & Cover Letter Templates", "https://ai-automation-guide-omega.vercel.app"),
            ("🤖 Interactive Chatbot Portfolio Demo", "https://work-minh-lap.vercel.app/chatbotdemo"),
            ("📖 The AI Money Blueprint eBook", "https://minhlap.gumroad.com/l/xqckmu"),
            ("🎁 The AI Empire Master Bundle ($39)", "https://minhlap.lemonsqueezy.com")
        ],
        "tags": [
            "ai freelancing", "make money on upwork with ai", "ai automation freelancer", "freelancing in 2026",
            "fiverr ai gigs", "how to freelance with ai", "make.com freelancer", "ai agency freelancer",
            "upwork cover letter 2026", "high paying remote jobs", "chatgpt side hustle", "remote freelance work"
        ],
        "pinned_comment": "💼 Download our Upwork Mastery Kit and 5 winning proposal templates inside our free resource vault: https://work-minh-lap.vercel.app/blog\n\nGrab the 16,000-word launch blueprint eBook: https://minhlap.gumroad.com/l/xqckmu\n\nWhat hourly rate are you aiming for: $50/hr, $75/hr, or $100+/hr? Let's discuss below! 👇"
    },
    "video_009": {
        "title": "How I Built an Autonomous AI Agency in 48 Hours ($3,000/Month Retainers)",
        "alt_titles": [
            "Building a Full AI Agency in 48 Hours (Full Tech Stack Breakdown)",
            "How to Land $650/Mo AI Client Retainers with Zero Employees",
            "The 2026 Autonomous AI Agency Blueprint: Sandboxes to Contracts"
        ],
        "timestamps": [
            "00:00 - The 48-Hour Autonomous AI Agency Experiment",
            "01:45 - The Fatal Flaw of Traditional Agencies (Why Retainers Die)",
            "04:10 - Pillar 1: The Proof-First Live Sandbox Prototype",
            "07:00 - Pillar 2: The 10-Slide Sales Pitch Deck & Speaker Notes",
            "09:45 - Pillar 3: Quantifying ROI ($13,500/Month Recovered Revenue)",
            "12:15 - Pillar 4: The 1-Click Digital Contract (MSA) & $1,850 Invoice",
            "14:30 - Pillar 5: The 5-Day White-Glove Onboarding Sprint",
            "16:00 - Free Agency Monorepo & Code Templates"
        ],
        "links": [
            ("🖥️ Live Client Sales Pitch Showcase Hub", "https://work-minh-lap.vercel.app/pitches"),
            ("🧮 Interactive AI Revenue Recovery Calculator", "https://work-minh-lap.vercel.app/calculator"),
            ("🧪 Live Chatbot Prototype Demo", "https://work-minh-lap.vercel.app/chatbotdemo"),
            ("📦 15 Make.com / n8n Blueprints Bundle", "https://work-minh-lap.vercel.app/bundle"),
            ("📖 The AI Money Blueprint (16,000 words)", "https://minhlap.gumroad.com/l/xqckmu")
        ],
        "tags": [
            "ai automation agency", "build an ai agency", "autonomous ai agency", "ai agency 2026",
            "ai agency retainer", "make money with ai", "smb ai consulting", "how to start an ai agency",
            "voiceflow", "botpress", "make.com agency", "ai client onboarding", "sales pitch deck"
        ],
        "pinned_comment": "🖥️ Explore all 30 live sales pitch decks & prototypes at our showcase hub: https://work-minh-lap.vercel.app/pitches\n\nCalculate your client's revenue recovery in real time: https://work-minh-lap.vercel.app/calculator\n\nWhich niche are you targeting first: Dental, HVAC, Legal, or Real Estate? Let me know below! 👇"
    },
    "video_010": {
        "title": "5 Make.com Automation Blueprints That Make $1,000/Month (Copy-Paste Templates)",
        "alt_titles": [
            "Top 5 Make.com Automations Businesses Pay $1,000 For",
            "Make $1,000/Month with No-Code AI Workflows (Step-by-Step)",
            "5 Copy-Paste Make.com Workflows You Can Sell to Clients in 2026"
        ],
        "timestamps": [
            "00:00 - Why No-Code Automations Command $1,000+ per Build",
            "01:45 - Blueprint 1: 30-Second Speed-to-Lead SMS & Dispatch",
            "04:30 - Blueprint 2: Autonomous AI Review Responder (Google & Yelp)",
            "07:15 - Blueprint 3: Stripe / Lemon Squeezy to Telegram VIP Broadcaster",
            "09:50 - Blueprint 4: Zero-Friction Calendar Lock & No-Show Eliminator",
            "12:10 - Blueprint 5: Autonomous Multi-Channel Social Repurposer",
            "14:00 - How to Package & Sell These Workflows for $1,000/Mo",
            "15:15 - Free Template Download Instructions"
        ],
        "links": [
            ("📦 Download All 15 Make.com Blueprints (.JSON Pack)", "https://work-minh-lap.vercel.app/bundle"),
            ("🤖 Interactive Chatbot Portfolio Demo", "https://work-minh-lap.vercel.app/chatbotdemo"),
            ("📖 The AI Money Blueprint eBook", "https://minhlap.gumroad.com/l/xqckmu"),
            ("📚 AI Resource Hub & Guides", "https://work-minh-lap.vercel.app/blog")
        ],
        "tags": [
            "make.com tutorial", "make.com blueprints", "n8n automation", "zapier vs make",
            "no-code automation", "ai automation agency", "speed to lead automation",
            "review response automation", "telegram bot make.com", "passive income no code", "make.com templates"
        ],
        "pinned_comment": "📦 Grab all 15 ready-to-import Make.com & n8n JSON blueprints here: https://work-minh-lap.vercel.app/bundle\n\nTest the live interactive copilot here: https://work-minh-lap.vercel.app/chatbotdemo\n\nWhich workflow will save your business the most time? Comment below! 👇"
    }
}

def generate_youtube_metadata(video_id="video_009"):
    data = VIDEO_METADATA_PRESETS.get(video_id, VIDEO_METADATA_PRESETS["video_006"])
    out_dir = Path(__file__).resolve().parent.parent / "projects" / "youtube_faceless" / "metadata"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"metadata_{video_id}.md"

    links_text = "\n".join([f"👉 {label}: {url}" for label, url in data["links"]])
    timestamps_text = "\n".join(data["timestamps"])
    tags_text = ", ".join(data["tags"])
    alt_titles_text = "\n".join([f"- Title {i+1}: {t}" for i, t in enumerate(data["alt_titles"])])
    summary_text = data.get("summary", f"In this video, I break down {data['title']}.")

    content = f"""# 📺 YouTube Video Metadata Package: {video_id.upper()}
> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 1. Recommended Video Titles (A/B Testing)
- **Primary Title (Recommended):**  
  `{data['title']}`

**Alternative Variations:**
{alt_titles_text}

---

## 📝 2. Video Description (Copy & Paste to YouTube Studio)
```text
{data['title']}

{summary_text}

📌 RESOURCES & LIVE DEMOS MENTIONED:
{links_text}

⏱️ TIMESTAMPS:
{timestamps_text}

🔔 Subscribe for weekly step-by-step breakdowns on AI business models, Micro-SaaS development, and autonomous automation workflows.

#AIAutomationAgency #MicroSaaS #MakeMoneyWithAI #ChatGPT #SideHustle2026
```

---

## 🏷️ 3. SEO Search Tags (Copy to Tag Box)
```text
{tags_text}
```

---

## 📌 4. Pinned Comment (Pin to Top of Comments)
```text
{data['pinned_comment']}
```
"""

    out_file.write_text(content, encoding="utf-8")
    print(f"[✓] Created YouTube metadata package: {out_file}")
    return out_file

def send_telegram_youtube_digest(vid_list):
    import urllib.request
    import json
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    lines = [
        "📺 <b>[YOUTUBE METADATA SUITE GENERATED]</b>",
        f"📅 <b>Updated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"🎯 <b>Total Episodes:</b> {len(vid_list)} Video Packages Ready",
        "",
        "<b>Catalog:</b>"
    ]

    for vid in vid_list[:6]:
        data = VIDEO_METADATA_PRESETS[vid]
        lines.append(f"• <b>{vid.upper()}:</b> {data['title'][:45]}...")

    if len(vid_list) > 6:
        lines.append(f"<i>...and {len(vid_list) - 6} more episodes in projects/youtube_faceless/metadata/</i>")

    lines.append("\n👉 <i>SEO tags, timestamps & descriptions ready to copy to YouTube Studio!</i>")

    msg = "\n".join(lines)
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot${bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status == 200:
                print("[✓] Dispatched YouTube Catalog Digest to Telegram (@Minhpv_bot)!")
    except Exception as e:
        print(f"[!] Telegram notification error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube SEO & Metadata Package Generator")
    parser.add_argument("--all", action="store_true", help="Generate metadata packages for all presets")
    parser.add_argument("--video", default="video_001", choices=list(VIDEO_METADATA_PRESETS.keys()), help="Video ID")
    parser.add_argument("--telegram", action="store_true", help="Send digest to Telegram")
    args = parser.parse_args()

    generated = []
    if args.all:
        for vid in sorted(VIDEO_METADATA_PRESETS.keys()):
            generate_youtube_metadata(vid)
            generated.append(vid)
    else:
        generate_youtube_metadata(args.video)
        generated.append(args.video)

    if args.telegram:
        send_telegram_youtube_digest(generated)

