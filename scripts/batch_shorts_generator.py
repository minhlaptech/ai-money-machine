"""
30-Day YouTube Shorts, TikTok & Reels Batch Sprint Engine
---------------------------------------------------------
Tự động tạo trọn bộ 30 kịch bản video ngắn (Short-Form Video Scripts 60s)
cho 30 ngày phủ sóng liên tục trên YouTube Shorts, TikTok và Instagram Reels.
Tập trung dẫn traffic về:
- Chatbot Demo: https://work-minh-lap.vercel.app/chatbotdemo
- SynapseGEO: https://work-minh-lap.vercel.app/synapsegeo
- Free Ebook & Guides: https://ai-automation-guide-omega.vercel.app
- Master Bundle ($39): https://minhlap.lemonsqueezy.com
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

SHORTS_DATA = [
    # --- WEEK 1: AI CHATBOTS & AGENCY SECRETS ---
    {"day": 1, "theme": "Agency Secret", "title": "Why local businesses lose 40% of customers after 7 PM", "hook": "Stop pitching ChatGPT. Here is the single sentence that closed a $1,500 client in 24 hours.", "solution": "Local businesses don't care about AI. They care about missed calls. An AI receptionist answers late-night inquiries and books directly into Google Calendar.", "cta": "Check our live 60-second interactive demo in bio!"},
    {"day": 2, "theme": "Chatbot Demo", "title": "I tested this dental AI chatbot on mobile (Mind blown)", "hook": "Look what happens when I ask a local clinic for Invisalign prices at 2 AM.", "solution": "Instead of waiting until 9 AM, the bot quotes prices, checks insurance, and locks down an appointment slot in 20 seconds flat.", "cta": "Link to the exact working template is in the description!"},
    {"day": 3, "theme": "Agency Math", "title": "How to make $3,000/month with only 4 clients", "hook": "You don't need 100 clients to quit your 9-to-5. You only need 4.", "solution": "Charge $1,500 setup once, then $750/month maintenance retainer. 4 clients = $3,000/month recurring revenue for 5 hours of work a week.", "cta": "Grab our 30-lead client outreach playbook for free in bio!"},
    {"day": 4, "theme": "Niche Breakdown", "title": "The #1 richest niche for AI automation in 2026", "hook": "Don't sell AI to coffee shops. Target this high-ticket niche instead.", "solution": "Cosmetic dentists and orthodontists. A single dental implant is worth $4,000. If your bot captures 1 extra patient, the owner makes 400% ROI.", "cta": "Full breakdown inside our 16,000-word blueprint eBook!"},
    {"day": 5, "theme": "Emergency Services", "title": "How this HVAC company recovered $9,200 with 1 automated text", "hook": "What happens when a homeowner's AC breaks in the summer at 8 PM?", "solution": "85% hang up on voicemail. Our 15-second AI text-back captures the emergency job before they call the competitor on Google.", "cta": "Get the Make.com blueprint in our template pack!"},
    {"day": 6, "theme": "Client Acquisition", "title": "The 1-Click cold email that gets 35% reply rates", "hook": "Never send a PDF proposal. Send this 60-second link instead.", "solution": "When you send a customized interactive demo link instead of a boring slide deck, business owners test it on their phone immediately.", "cta": "Copy-paste this exact email script from our free guide!"},
    {"day": 7, "theme": "Overcoming Fear", "title": "Do you need coding skills to start an AI agency?", "hook": "Think you need a computer science degree to sell AI? Absolutely not.", "solution": "You can connect Voiceflow or OpenAI Assistants to webhooks using no-code tools like Make.com in under 30 minutes without writing a single line of code.", "cta": "Follow for daily AI automation blueprints!"},

    # --- WEEK 2: MICRO-SAAS QUICK WINS & GEO SEO ---
    {"day": 8, "theme": "Micro-SaaS", "title": "I built a software tool in 48 hours that charges $19", "hook": "You don't need venture capital to launch a profitable SaaS in 2026.", "solution": "Find one hyper-specific problem like robots.txt AI auditing. We built SynapseGEO in a weekend, deployed on Vercel Edge for zero dollars, and connected Lemon Squeezy.", "cta": "Test the live tool at work-minh-lap.vercel.app/synapsegeo!"},
    {"day": 9, "theme": "AI Search Shift", "title": "Google SEO is declining. Here is what is replacing it.", "hook": "If your site isn't optimized for Perplexity and ChatGPT, you are losing 40% of future traffic.", "solution": "Generative Engine Optimization (GEO) relies on clean JSON-LD Schema and robots.txt bot permissions. If you block GPTBot, you are invisible.", "cta": "Run a free 10-second audit on your domain (link in bio)!"},
    {"day": 10, "theme": "Review Genius", "title": "Turn 1-star angry reviews into 5-star loyal fans", "hook": "Replying to angry Google reviews manually takes hours and emotional stress.", "solution": "ReviewGenius AI analyzes negative sentiment and drafts de-escalation responses that protect your business reputation in 3 seconds.", "cta": "Try ReviewGenius free (link in description)!"},
    {"day": 11, "theme": "Headline IQ", "title": "The psychological secret to viral headlines", "hook": "Why do some articles get 100k views while yours get 12 clicks?", "solution": "Emotional resonance and curiosity gaps. HeadlineIQ scores your headline CTR potential and suggests 10 AI variations backed by copywriting psychology.", "cta": "Check your headline score for free in bio!"},
    {"day": 12, "theme": "Zero-Cost Hosting", "title": "How to host your web apps for $0 forever", "hook": "Stop paying $50/month for cloud servers when you're just starting out.", "solution": "Vercel Edge, GitHub Pages, and Cloudflare Pages allow you to run serverless edge applications with worldwide CDN speed completely free.", "cta": "Full tech stack tutorial inside our free Resource Hub!"},
    {"day": 13, "theme": "Chrome Extension", "title": "How to build a Chrome extension as a lead magnet", "hook": "The smartest way to get 1,000 free SaaS users without paying for ads.", "solution": "Package a simple audit tool into a Manifest V3 Chrome Extension. Users install it for free, see their errors, and click through to your paid web app.", "cta": "Download our open-source extension zip in bio!"},
    {"day": 14, "theme": "SaaS Monetization", "title": "Stripe vs Lemon Squeezy for solo founders", "hook": "Which payment processor should you use for digital products and SaaS?", "solution": "Lemon Squeezy acts as a Merchant of Record (MoR), handling international sales taxes and VAT compliance automatically so you don't have tax headaches.", "cta": "Follow for more indie hacker breakdown!"},

    # --- WEEK 3: NO-CODE AUTOMATION BLUEPRINTS ---
    {"day": 15, "theme": "Make vs Zapier", "title": "Make.com vs Zapier: The brutal truth in 2026", "hook": "Are you wasting $200/month on Zapier? Here is the real difference.", "solution": "Zapier charges per task. Make.com charges per operation and offers visual routers and error-handlers at one-fifth of the price for complex branching.", "cta": "Read our complete in-depth comparison on our blog!"},
    {"day": 16, "theme": "Telegram Alert", "title": "Get an instant phone notification whenever you get a lead", "hook": "Never miss a high-ticket customer inquiry while away from your desk.", "solution": "Connect your website form to a Telegram Bot via webhook. Whenever a lead submits, your phone buzzes within 2 seconds with customer details.", "cta": "Import this blueprint from our 15-pack templates!"},
    {"day": 17, "theme": "OCR Pipeline", "title": "Automating 20 hours of invoice data entry for accountants", "hook": "Chasing receipts and 1099 forms is the biggest waste of billable CPA hours.", "solution": "An automated pipeline with AI Vision extracts vendor, tax ID, and line items, writing them directly into QuickBooks without manual typing.", "cta": "Grab the full blueprint package in our Master Bundle!"},
    {"day": 18, "theme": "Multi-Platform Repurpose", "title": "Turn 1 blog post into 10 social media posts in 60s", "hook": "Stop writing content separately for Twitter, LinkedIn, and TikTok.", "solution": "Use an AI repurposing script that extracts the key hook, formats a 7-tweet thread, a professional LinkedIn carousel, and a 60-second video script.", "cta": "Try our open repurposing engine (link in bio)!"},
    {"day": 19, "theme": "Error Handling", "title": "Why 90% of Make.com scenarios break (And the fix)", "hook": "Ever wake up to find your automation stopped running 3 days ago?", "solution": "Always add an Error Handler route with Resume or Ignore directives and a fallback alert to your Slack or Telegram. Never let an API 429 kill your flow.", "cta": "Full troubleshooting guide in our resource vault!"},
    {"day": 20, "theme": "Airtable CRM", "title": "Build a custom $5,000 CRM in Airtable in 15 minutes", "hook": "Don't pay Salesforce $150/user/month for small businesses.", "solution": "Combine Airtable relational databases with AI automations to score leads, assign tasks, and trigger email sequences automatically.", "cta": "Download our ready-to-use Airtable base template in bio!"},
    {"day": 21, "theme": "AI Agent Future", "title": "The death of static websites: Meet autonomous web agents", "hook": "In 2 years, people won't browse menus and click forms. They will talk to web agents.", "solution": "Websites are shifting from static brochures to interactive conversational copilot interfaces that understand intent and complete actions.", "cta": "Experience the prototype at work-minh-lap.vercel.app/chatbotdemo!"},

    # --- WEEK 4: DIGITAL PRODUCTS, PROMPTS & FREELANCING ---
    {"day": 22, "theme": "Digital Product", "title": "How to create and sell your first digital eBook with AI", "hook": "How we wrote a 16,000-word technical guide in 7 days and listed it on Gumroad.", "solution": "Structure your outline first. Use deep AI prompting for real-world case studies and frameworks. Export to crisp PDF and launch on Gumroad and Lemon Squeezy.", "cta": "Get The AI Money Blueprint eBook in bio!"},
    {"day": 23, "theme": "Prompt Engineering", "title": "Stop writing bad prompts: The 4-step framework", "hook": "99% of people get robotic answers from ChatGPT because of this mistake.", "solution": "Role + Context + Exact Constraint + Desired Output Schema. Never say 'write a blog post'. Say 'Act as an enterprise copywriter, write an H2 section under 200 words with zero passive voice'.", "cta": "Download our 110+ production prompt pack today!"},
    {"day": 24, "theme": "Fiverr Gigs", "title": "3 Fiverr gigs you can offer today with zero portfolio", "hook": "How to get your first 5-star review on Fiverr in week one.", "solution": "1. Custom Chatbot Setup. 2. Zapier/Make Automation Fix. 3. GEO & AI Search Readiness Audit. Deliver within 24 hours with Loom video support.", "cta": "Copy our gig descriptions from our free freelancing guide!"},
    {"day": 25, "theme": "Upwork Strategy", "title": "How to charge $95/hour on Upwork as an AI developer", "hook": "Stop competing on $5 gigs. Here is how to position for high-ticket contracts.", "solution": "Create specialized profiles for AI Automations. Apply to verified clients with $1,000+ budgets within 1 hour of posting. Include a live working demo link.", "cta": "Read our Upwork Mastery Kit on our blog!"},
    {"day": 26, "theme": "Print on Demand", "title": "Can you still make money with Print-on-Demand in 2026?", "hook": "Is POD dead? Not if you target this high-spending niche.", "solution": "Programmers, data scientists, and AI builders love clever, minimalist tech humor. A single hoodie design brings $18.00 in pure profit on Printify + Etsy.", "cta": "Check our POD case study in our Resource Hub!"},
    {"day": 27, "theme": "Gumroad Strategy", "title": "How to get sales on Gumroad with zero social following", "hook": "Listing a product on Gumroad won't get sales by itself. Here is the distribution loop.", "solution": "Build free Micro-SaaS tools or post valuable short tutorials. Offer free lead magnets (prompt packs) and link to your paid Master Bundle inside the downloads.", "cta": "Explore the full AI Empire Bundle in bio!"},
    {"day": 28, "theme": "Client Proposal", "title": "The 2-page AI audit proposal that closes 4 out of 5 clients", "hook": "What does a high-ticket client proposal actually look like?", "solution": "Section 1: Lost Revenue Calculation. Section 2: Recommended Copilot Architecture. Section 3: Projected ROI. Section 4: Fixed Setup Fee + Monthly Maintenance Guarantee.", "cta": "Generate your own custom proposal using our free script!"},

    # --- BONUS: 90-DAY FREEDOM ROADMAP ---
    {"day": 29, "theme": "Roadmap Part 1", "title": "Month 1 vs Month 3: The 90-Day AI Income Roadmap", "hook": "Where should you focus your time during the first 30 days?", "solution": "Month 1: Skills & proof-of-work (build 1 micro-tool and 1 demo). Month 2: Client outreach & digital products. Month 3: Recurring retainers and automated distribution.", "cta": "Read Chapter 10 of The AI Money Blueprint eBook!"},
    {"day": 30, "theme": "Roadmap Part 2", "title": "The 8-stream AI money machine explained in 60 seconds", "hook": "How 8 small income streams combine into $3,500/month recurring cashflow.", "solution": "Micro-SaaS subscriptions + Agency Retainers + Digital Product sales + YouTube AdSense + Affiliate commissions + Freelance gigs. Diversified, resilient, automated.", "cta": "Start your journey today at https://work-minh-lap.vercel.app/blog !"}
]

def generate_batch_shorts():
    out_dir = Path(__file__).resolve().parent.parent / "projects" / "youtube_faceless" / "shorts_sprint"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "30_DAYS_SHORTS_SPRINT.md"

    md = f"""# 📱 30-Day Viral Shorts, TikTok & Reels Content Sprint
> **Tạo lúc**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Kênh phát hành**: YouTube Shorts, TikTok, Instagram Reels, LinkedIn Video  
> **Mục tiêu**: Phủ sóng 30 video trong 30 ngày, kéo lưu lượng truy cập tự nhiên về các công cụ Micro-SaaS và Master Bundle.

---

## 📅 LỊCH TRÌNH 30 NGÀY NỘI DUNG (THE 30-DAY SPRINT)

"""

    for item in SHORTS_DATA:
        md += f"""### 🎬 Ngày #{item['day']:02d} | [{item['theme']}] {item['title']}
- **Hook thị giác (0–3s)**: [Chữ lớn trên màn hình, màu neon] *"{item['hook']}"*
- **Nội dung chính (3–45s)**:
  > "{item['solution']}"
- **Kêu gọi hành động (CTA 45–60s)**:
  > "{item['cta']}"
- **Thẻ Hashtags**: `#AIAutomation #MicroSaaS #MakeMoneyOnline #ChatGPT #IndieHacker #SideHustle2026`

---
"""

    out_file.write_text(md, encoding="utf-8")
    print(f"[✓] Successfully generated 30-day shorts sprint: {out_file}")
    return out_file

def send_telegram_short_script(day_num):
    import urllib.request
    import json
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    item = next((s for s in SHORTS_DATA if s["day"] == day_num), SHORTS_DATA[0])

    msg = (
        f"🎬 <b>[SHORTS SPRINT DISPATCH — DAY #{item['day']:02d}]</b>\n\n"
        f"🏷️ <b>Chủ đề:</b> <code>{item['theme']}</code>\n"
        f"📌 <b>Tiêu đề:</b> <b>{item['title']}</b>\n\n"
        f"⚡ <b>Hook (0-3s):</b>\n<i>\"{item['hook']}\"</i>\n\n"
        f"💡 <b>Kịch bản chính (3-45s):</b>\n{item['solution']}\n\n"
        f"🎯 <b>Kêu gọi hành động (CTA 45-60s):</b>\n<b>{item['cta']}</b>\n\n"
        f"🔖 <b>Hashtags:</b>\n<code>#AIAutomation #MicroSaaS #ChatGPT #SideHustle2026</code>\n\n"
        f"👉 <i>Sẵn sàng quay hoặc nạp vào ElevenLabs + CapCut!</i>"
    )

    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot${bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status == 200:
                print(f"[✓] Dispatched Day #{day_num} Short script to Telegram (@Minhpv_bot)!")
    except Exception as e:
        print(f"[!] Telegram notification error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="30-Day Shorts Sprint Generator")
    parser.add_argument("--day", type=int, choices=range(1, 31), help="Generate/view specific Day (1-30)")
    parser.add_argument("--telegram", action="store_true", help="Send script to Telegram")
    args = parser.parse_args()

    generate_batch_shorts()

    if args.telegram:
        target_day = args.day if args.day else 1
        send_telegram_short_script(target_day)

