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
        "cta": "Explore the full AI Automation Playbook & blueprints at https://ai-automation-guide-omega.vercel.app"
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
        "cta": "Download the complete 16,000-word AI Money Blueprint eBook at https://minhlap.gumroad.com/l/xqckmu"
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
    print(f"[✓] Created viral content kit: {out_file}")
    return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-Platform Social Repurposing Engine")
    parser.add_argument("--topic", default="geo_audit", choices=["geo_audit", "ai_automation", "microsaas_blueprint"], help="Content topic")
    args = parser.parse_args()
    generate_social_kit(args.topic)
