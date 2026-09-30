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

PROPOSAL_TEMPLATES = {
    "chatbot": {
        "subject": "AI Chatbot & Support Copilot",
        "hook": "Building a customer-facing AI chatbot requires strict grounding to your actual company documentation so it never hallucinates, while booking appointments or escalating to human agents seamlessly.",
        "proof": "I have an active interactive demo running right now that demonstrates this exact flow:\n👉 Live Demo: https://work-minh-lap.vercel.app/chatbotdemo\n👉 VIP Client Hub: https://work-minh-lap.vercel.app/portal",
        "questions": [
            "Which platform is your website built on (Shopify, WordPress, Webflow, custom)?",
            "What CRM or calendar tool should the bot sync conversations and appointments with (Google Calendar, Calendly, HubSpot)?"
        ],
        "turnaround": "3 to 5 business days for full setup, prompt tuning, and CRM integration."
    },
    "automation": {
        "subject": "Make.com & Zapier Pipeline Automation",
        "hook": "Manual data entry between tools is a massive drain on company hours and creates costly data entry mistakes. I design bulletproof Make.com and Zapier pipelines equipped with automatic error-handling and anomaly alerts.",
        "proof": "I've deployed over 15 production automation blueprints handling multi-step webhooks, CRM synchronization, and payment alerts.\n👉 Interactive Automation ROI Calculator: https://work-minh-lap.vercel.app/calculator",
        "questions": [
            "What is your approximate monthly volume of records or events passing through this workflow?",
            "Do you already have API access or admin credentials for the involved applications?"
        ],
        "turnaround": "24 to 48 hours in a staging environment before pushing live."
    },
    "scraping": {
        "subject": "Data Scraping & AI Enrichment Pipeline",
        "hook": "Reliable data extraction requires handling Cloudflare anti-bot checks, dynamic JavaScript rendering, and structured JSON parsing without missing records.",
        "proof": "I build asynchronous Python and Playwright pipelines that extract clean datasets and structure them using OpenAI's structured outputs API.\n👉 Live Micro-SaaS Suite & Tools: https://work-minh-lap.vercel.app/tools",
        "questions": [
            "What is the target URL or domain directory you need scraped?",
            "What format do you prefer for the final export (Google Sheet, CSV, PostgreSQL database)?"
        ],
        "turnaround": "1 to 2 days including a 10-row sample for your quality validation."
    },
    "geo_seo": {
        "subject": "AI Search & GEO (Generative Engine Optimization) Audit",
        "hook": "Traditional SEO alone is losing ground to AI search engines (ChatGPT, Perplexity, Claude). Making your brand visible to LLMs requires precise robots.txt permissions and deep JSON-LD Knowledge Graph Schemas.",
        "proof": "I built and deployed SynapseGEO, an autonomous Generative Engine Optimization inspector:\n👉 Live Audit Engine: https://work-minh-lap.vercel.app/synapsegeo\n👉 Full SaaS Suite: https://work-minh-lap.vercel.app/saas",
        "questions": [
            "Do you already have access to edit your website's robots.txt and DNS records?",
            "Are you targeting local search recommendations or national B2B software queries?"
        ],
        "turnaround": "2 business days for a complete AI visibility audit and custom JSON-LD schema deployment."
    },
    "review_management": {
        "subject": "Autonomous AI Customer Review Management & Sentiment Responder",
        "hook": "Unanswered 1-star reviews on Google Maps and Yelp drastically cut organic conversions. My system uses sentiment analysis and LLM guardrails to draft empathetic, de-escalating replies and voucher offers in under 5 seconds.",
        "proof": "You can test the actual review responder interface live on the web:\n👉 Live Demo: https://work-minh-lap.vercel.app/reviewgenius\n👉 Agency Hub: https://work-minh-lap.vercel.app/freelance",
        "questions": [
            "Which review platforms do you need integrated (Google Business Profile, Yelp, Trustpilot)?",
            "Should replies post automatically or require 1-click human approval first?"
        ],
        "turnaround": "3 to 5 business days for webhook integration and custom tone calibration."
    },
    "client_portal": {
        "subject": "Enterprise AI Copilot Deployment & White-Label Client Portal",
        "hook": "Rather than just delivering a simple script or widget, I deploy a branded executive management portal for your team, featuring real-time 99.98% SLA monitoring, conversation logs, and 1-click embed tags for WordPress/Webflow/Shopify.",
        "proof": "You can explore our central VIP Client Portal Command Hub showcasing 84 enterprise accounts:\n👉 Live VIP Hub: https://work-minh-lap.vercel.app/portal\n👉 VIP Onboarding Intake: https://work-minh-lap.vercel.app/onboarding",
        "questions": [
            "Which web CMS will the AI copilot be embedded onto?",
            "Do you require role-based access for multiple team members or clients?"
        ],
        "turnaround": "5-day white-glove implementation sprint (Kickoff -> Calibration -> Testing -> Go-Live)."
    },
    "ai_voice_caller": {
        "subject": "AI Voice Receptionist & Inbound/Outbound Calling Agent",
        "hook": "Traditional voicemail loses 80% of inbound callers. I deploy conversational AI voice agents (Vapi/Bland.ai + Twilio) that answer incoming phone calls with sub-800ms latency, qualify prospects, check calendar availability, and book appointments directly.",
        "proof": "Our AI intake systems handle real-time customer dialogues, two-way Google Calendar synchronization, and speed-to-lead SMS routing.\n👉 Live Voice Pitch Demos: https://work-minh-lap.vercel.app/pitches\n👉 Freelance Services: https://work-minh-lap.vercel.app/freelance",
        "questions": [
            "Do you already have a Twilio or phone number account set up, or should we provision one?",
            "What specific FAQs or qualification criteria should the voice agent check before transferring to your team?"
        ],
        "turnaround": "3 to 4 business days including live phone number provisioning, prompt engineering, and test call calibration."
    },
    "content_repurposing": {
        "subject": "Autonomous Multi-Platform Social Content Repurposing Engine",
        "hook": "Repurposing long-form YouTube videos, podcasts, or blog posts manually takes 10+ hours a week. I build automated content engines that ingest your media and automatically output viral Twitter threads, LinkedIn thought leadership posts, 60-second TikTok/Shorts scripts, and Reddit community discussions.",
        "proof": "I built and deployed an autonomous multi-platform content engine powering 10 distinct content formats across social media.\n👉 Live Media Studio (40 Videos Vault): https://work-minh-lap.vercel.app/studio\n👉 Content & Resource Hub: https://work-minh-lap.vercel.app/blog",
        "questions": [
            "What is your primary source format (YouTube video URLs, audio podcasts, or blog articles)?",
            "Which social media platforms do you want the final formatted copy pushed to?"
        ],
        "turnaround": "48 hours to build, test, and deliver your automated repurposing workflow."
    },
    "rag_knowledge_base": {
        "subject": "Custom Enterprise RAG (Retrieval-Augmented Generation) & Knowledge Base",
        "hook": "Generic ChatGPT answers don't know your company's proprietary SOPs, PDF contracts, or internal wiki. I build private RAG assistants using vector embeddings (Pinecone/Chroma/Supabase) that cite exact document pages and maintain strict factual grounding.",
        "proof": "I specialize in grounded LLM architectures with strict context injection and anti-hallucination guardrails.\n👉 Live Grounded AI Assistant: https://work-minh-lap.vercel.app/chatbotdemo\n👉 AI Architecture Blueprints: https://work-minh-lap.vercel.app/bundle",
        "questions": [
            "What format are your source documents in (PDFs, Notion workspaces, Google Docs, CSVs)?",
            "Where will the assistant be accessed by your team (Slack, internal web dashboard, Discord)?"
        ],
        "turnaround": "4 to 6 business days including vector database setup, chunking strategy optimization, and evaluation testing."
    },
    "ecommerce_ai_agent": {
        "subject": "Shopify & E-Commerce AI Sales Concierge & Cart Recovery Agent",
        "hook": "Most online shoppers abandon carts because their sizing, shipping, or compatibility questions aren't answered instantly. I deploy proactive AI shopping concierges that recommend personalized products, answer stock questions, and trigger high-converting SMS recovery discounts.",
        "proof": "Our e-commerce AI prototypes simulate instant order lookups, inventory checks, and checkout parameter generation.\n👉 Live Agency Portfolio: https://work-minh-lap.vercel.app/freelance\n👉 VIP Client Portals: https://work-minh-lap.vercel.app/portal",
        "questions": [
            "What e-commerce platform are you running (Shopify, WooCommerce, Magento)?",
            "Do you already have Klaviyo or an SMS provider (Twilio, Attentive) connected for checkout recovery?"
        ],
        "turnaround": "3 to 5 business days including product catalog ingestion, conversational testing, and tracking integration."
    }
}

def send_telegram_proposal_preview(job_type, proposal_text):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    preview_snippet = proposal_text[:400].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html_msg = f"""💼 <b>[UPWORK WINNING PROPOSAL READY]</b>

🎯 <b>Job Category:</b> <code>{job_type}</code>

📝 <b>Proposal Snippet:</b>
<pre>{preview_snippet}...</pre>

👉 <i>Toàn văn đã được lưu tại projects/ai_freelancing/proposals/upwork_proposal_{job_type}.md</i>"""

    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status == 200:
                print(f"[✓] Đã gửi bản Cover Letter '{job_type}' về Telegram!")
    except Exception as e:
        print(f"[!] Lỗi gửi Telegram: {e}")

def generate_upwork_proposal(job_type="chatbot", client_name="there", custom_notes="", send_telegram=False):
    data = PROPOSAL_TEMPLATES.get(job_type, PROPOSAL_TEMPLATES["chatbot"])
    out_dir = Path(__file__).resolve().parent.parent / "projects" / "ai_freelancing" / "proposals"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"upwork_proposal_{job_type}.md"

    questions_formatted = "\n".join([f"{i+1}. {q}" for i, q in enumerate(data["questions"])])

    proposal_text = f"""Hi {client_name},

Saw your posting regarding the {data['subject'].lower()}.

{data['hook']}

{data['proof']}

A couple of quick questions to ensure we scope this accurately:
{questions_formatted}
"""

    if custom_notes:
        proposal_text += f"\nRegarding your specific requirement: {custom_notes}\n"

    proposal_text += f"""
Estimated Delivery: {data['turnaround']}

I am available to start immediately and would love to jump on a quick 10-minute discovery call to map out the implementation.

Best regards,
Minh Lap
AI Solutions Architect | Upwork Specialist
"""

    out_file.write_text(proposal_text.strip(), encoding="utf-8")
    print(f"[✓] Created Upwork proposal: {out_file.name}")
    if send_telegram:
        send_telegram_proposal_preview(job_type, proposal_text.strip())
    return out_file

def generate_all_proposals(send_telegram=False):
    print("=" * 75)
    print("🚀 GENERATING ALL 10 UPWORK WINNING PROPOSALS")
    print("=" * 75)
    for k in PROPOSAL_TEMPLATES.keys():
        generate_upwork_proposal(k, send_telegram=send_telegram)
    print("-" * 75)
    print("🎉 SUCCESS: All 10 Upwork proposals generated in projects/ai_freelancing/proposals/")
    print("=" * 75)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upwork Winning Proposal Generator")
    parser.add_argument("--type", default="chatbot", choices=list(PROPOSAL_TEMPLATES.keys()), help="Job Type")
    parser.add_argument("--all", action="store_true", help="Generate all 10 proposals at once")
    parser.add_argument("--client", default="there", help="Client Name if known")
    parser.add_argument("--notes", default="", help="Custom note or requirement mentioned in job description")
    parser.add_argument("--telegram", action="store_true", help="Send proposal preview to Telegram")
    args = parser.parse_args()

    if args.all:
        generate_all_proposals(send_telegram=args.telegram)
    else:
        generate_upwork_proposal(args.type, args.client, args.notes, send_telegram=args.telegram)
