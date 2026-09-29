"""
Upwork Proposal Generator CLI
------------------------------
Tự động phân tích yêu cầu công việc từ khách hàng trên Upwork và tạo bản Cover Letter
sắc bén, chuyên nghiệp, kèm câu hỏi phân loại và link Portfolio Demo thực tế.
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

PROPOSAL_TEMPLATES = {
    "chatbot": {
        "subject": "AI Chatbot & Support Copilot",
        "hook": "Building a customer-facing AI chatbot requires strict grounding to your actual company documentation so it never hallucinates, while booking appointments or escalating to human agents seamlessly.",
        "proof": "I have an active interactive demo running right now that demonstrates this exact flow:\n👉 Live Demo: https://chatbotdemo-hazel.vercel.app",
        "questions": [
            "Which platform is your website built on (Shopify, WordPress, Webflow, custom)?",
            "What CRM or calendar tool should the bot sync conversations and appointments with (Google Calendar, Calendly, HubSpot)?"
        ],
        "turnaround": "3 to 5 business days for full setup, prompt tuning, and CRM integration."
    },
    "automation": {
        "subject": "Make.com & Zapier Pipeline Automation",
        "hook": "Manual data entry between tools is a massive drain on company hours and creates costly data entry mistakes. I design bulletproof Make.com and Zapier pipelines equipped with automatic error-handling and anomaly alerts.",
        "proof": "I've deployed over 15 production automation blueprints handling multi-step webhooks, CRM synchronization, and payment alerts.",
        "questions": [
            "What is your approximate monthly volume of records or events passing through this workflow?",
            "Do you already have API access or admin credentials for the involved applications?"
        ],
        "turnaround": "24 to 48 hours in a staging environment before pushing live."
    },
    "scraping": {
        "subject": "Data Scraping & AI Enrichment Pipeline",
        "hook": "Reliable data extraction requires handling Cloudflare anti-bot checks, dynamic JavaScript rendering, and structured JSON parsing without missing records.",
        "proof": "I build asynchronous Python and Playwright pipelines that extract clean datasets and structure them using OpenAI's structured outputs API.",
        "questions": [
            "What is the target URL or domain directory you need scraped?",
            "What format do you prefer for the final export (Google Sheet, CSV, PostgreSQL database)?"
        ],
        "turnaround": "1 to 2 days including a 10-row sample for your quality validation."
    }
}

def generate_upwork_proposal(job_type="chatbot", client_name="there", custom_notes=""):
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
    print(f"[✓] Created Upwork proposal: {out_file}")
    print("\n--- PROPOSAL PREVIEW ---")
    print(proposal_text.strip())
    print("------------------------\n")
    return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upwork Winning Proposal Generator")
    parser.add_argument("--type", default="chatbot", choices=["chatbot", "automation", "scraping"], help="Job Type")
    parser.add_argument("--client", default="there", help="Client Name if known")
    parser.add_argument("--notes", default="", help="Custom note or requirement mentioned in job description")
    args = parser.parse_args()
    generate_upwork_proposal(args.type, args.client, args.notes)
