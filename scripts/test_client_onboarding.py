"""
VIP Client Onboarding Simulator & Inbound Lead Tester
------------------------------------------------------
Kiểm thử và giả lập nộp hồ sơ Onboarding cho Khách hàng VIP qua /api/contact.
Bắn thông báo thời gian thực về Telegram @Minhpv_bot.
"""

import sys
import os
import json
import urllib.request
import argparse
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

LIVE_URL = "https://work-minh-lap.vercel.app/api/contact"

CLIENT_PROFILES = {
    "austin_dental": {
        "name": "Austin Dental Co (Dr. Sarah Jenkins)",
        "email": "dr.sarah@austindental.example.com",
        "phone": "+1 (512) 555-0199",
        "website": "https://work-minh-lap.vercel.app/portal/austin_dental_co",
        "service": "24/7 AI Dental Receptionist & Intake Copilot",
        "source": "VIP Client Onboarding Intake Hub (/onboarding)",
        "calendar": "Google Calendar (Daily 8:00 AM - 5:00 PM CST)",
        "escalation": "+1 (512) 555-0199 (Urgent tooth pain / emergency)",
        "message": "Kickoff agreement and setup invoice confirmed. Ready for 48h Sprint deployment! Please route after-hours dental inquiries directly to calendar."
    },
    "sterling_legal": {
        "name": "Sterling & Partners Legal (David Sterling, Esq.)",
        "email": "david.sterling@sterlinglegal.example.com",
        "phone": "+1 (312) 555-0188",
        "website": "https://work-minh-lap.vercel.app/portal/sterling_and_partners_legal",
        "service": "Bespoke Legal Case Intake & Conflict Check Copilot",
        "source": "VIP Client Onboarding Intake Hub (/onboarding)",
        "calendar": "Clio / Calendly Executive Calendar",
        "escalation": "+1 (312) 555-0188 (Urgent subpoena & litigation alerts)",
        "message": "Retainer agreement signed ($1,500 setup + $750/mo). Looking forward to launching our branded client portal this week."
    },
    "beverly_plastics": {
        "name": "Beverly Hills Plastic Surgery (Dr. Jason Miller)",
        "email": "consultations@beverlyplastics.example.com",
        "phone": "+1 (310) 555-0144",
        "website": "https://work-minh-lap.vercel.app/portal/beverly_hills_plastic_surgery",
        "service": "Concierge VIP Patient Inquiry & Financing Copilot",
        "source": "VIP Client Onboarding Intake Hub (/onboarding)",
        "calendar": "Symplast / PatientNow Calendar Integration",
        "escalation": "+1 (310) 555-0144 (VIP Consult Hotline)",
        "message": "Discovery call scheduled. Inquiring about custom high-ticket financing Q&A prompt tuning for rhinoplasty and facelift consultations."
    }
}

def simulate_onboarding(profile_key="austin_dental"):
    profile = CLIENT_PROFILES.get(profile_key, CLIENT_PROFILES["austin_dental"])
    print("=" * 75)
    print(f"📋 SIMULATING VIP CLIENT ONBOARDING INTAKE: {profile['name']}")
    print("=" * 75)
    print(f"  • Endpoint:    {LIVE_URL}")
    print(f"  • Service:     {profile['service']}")
    print(f"  • Escalation:  {profile['escalation']}")
    print("-" * 75)

    payload_bytes = json.dumps(profile, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        LIVE_URL,
        data=payload_bytes,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "AI-Empire-VIP-Onboarding-Simulator/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            res_body = res.read().decode("utf-8")
            status_code = res.status
            print(f"[✓] Status Code: HTTP {status_code} OK")
            print(f"[✓] Server Response: {res_body}")
            print("🎉 SUCCESS: Inbound VIP Onboarding submission processed and Telegram alert triggered!")
            print("=" * 75)
            return True
    except urllib.error.HTTPError as e:
        print(f"[!] HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"[!] Network or Connection Error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulate VIP Client Onboarding Submissions")
    parser.add_argument("--client", choices=list(CLIENT_PROFILES.keys()), default="austin_dental", help="Client profile to simulate")
    parser.add_argument("--all", action="store_true", help="Simulate all clients in sequence")

    args = parser.parse_args()

    if args.all:
        for k in CLIENT_PROFILES.keys():
            simulate_onboarding(k)
            print()
    else:
        simulate_onboarding(args.client)
