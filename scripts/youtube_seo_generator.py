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
    "video_006": {
        "title": "How to Start an AI Automation Agency (AAA) in 2026 ($0 to $3,000/mo Retainers)",
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
            ("📖 Free eBook 'The AI Money Blueprint' (16,000 words)", "https://ai-automation-guide-omega.vercel.app"),
            ("⚡ SynapseGEO AI Search Engine Audit Tool", "https://synapse-geo-audit.vercel.app"),
            ("📦 Gumroad Digital Products & Templates", "https://minhlap.gumroad.com")
        ],
        "tags": [
            "ai automation agency", "how to start an ai agency", "aaa blueprint 2026",
            "make money with ai", "ai chatbot agency", "voiceflow tutorial", "botpress tutorial",
            "smb automation", "cold email for ai agency", "ai freelancing", "ai side hustle",
            "passive income 2026", "chatgpt business ideas", "indie hacker", "microsaas"
        ],
        "pinned_comment": "👉 Test the live interactive client chatbot demo here: https://work-minh-lap.vercel.app/chatbotdemo\n\nDownload our complete 16,000-word eBook & 15 automation templates for free at https://ai-automation-guide-omega.vercel.app !\n\nDrop a comment: Which local niche are you planning to target first? 👇"
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
            ("🌐 Live Micro-SaaS Demo (SynapseGEO)", "https://synapse-geo-audit.vercel.app"),
            ("📖 The AI Money Blueprint eBook", "https://minhlap.gumroad.com/l/xqckmu"),
            ("📚 AI Resource Hub & Free Guides", "https://ai-automation-guide-omega.vercel.app")
        ],
        "tags": [
            "microsaas", "micro saas ai", "build saas with ai", "chatgpt coding",
            "solo founder", "indie hacker saas", "lemonsqueezy store", "vercel edge",
            "passive income software", "ai money machine", "seo audit tool"
        ],
        "pinned_comment": "🛠️ Test the live Micro-SaaS tool we built in this video: https://synapse-geo-audit.vercel.app\n\nGet the complete 16,000-word launch blueprint here: https://minhlap.gumroad.com/l/xqckmu\n\nWhat micro-tool idea are you building next? Let me know below!"
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

In this video, I break down the exact step-by-step roadmap to start your own AI Automation Agency (AAA) in 2026 with zero coding, land high-ticket local business clients, and build recurring monthly retainers ($1,500 setup + $750/mo).

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube SEO & Metadata Package Generator")
    parser.add_argument("--all", action="store_true", help="Generate metadata packages for all presets")
    parser.add_argument("--video", default="video_009", choices=["video_005", "video_006", "video_007", "video_008", "video_009", "video_010"], help="Video ID")
    args = parser.parse_args()

    if args.all:
        for vid in sorted(VIDEO_METADATA_PRESETS.keys()):
            generate_youtube_metadata(vid)
    else:
        generate_youtube_metadata(args.video)
