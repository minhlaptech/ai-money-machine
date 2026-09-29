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
            ("🤖 Interactive Chatbot Portfolio Demo", "https://chatbotdemo-hazel.vercel.app"),
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
        "pinned_comment": "👉 Test the live interactive client chatbot demo here: https://chatbotdemo-hazel.vercel.app\n\nDownload our complete 16,000-word eBook & 15 automation templates for free at https://ai-automation-guide-omega.vercel.app !\n\nDrop a comment: Which local niche are you planning to target first? 👇"
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
    }
}

def generate_youtube_metadata(video_id="video_006"):
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
    parser.add_argument("--video", default="video_006", choices=["video_006", "video_005"], help="Video ID")
    args = parser.parse_args()
    generate_youtube_metadata(args.video)
