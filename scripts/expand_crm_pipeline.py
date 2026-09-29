#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — Enterprise Pipeline Expansion Engine (60 Leads)
------------------------------------------------------------------
Mở rộng cơ sở dữ liệu phễu khách hàng từ 30 leads lên 60 leads (Thêm Batch 4, 5, 6).
Tự động sinh:
1. 30 Live Sandboxes mới trong sandboxes/
2. 30 Custom ROI Reports mới trong reports/
3. 30 Pitch Decks mới trong pitches/
4. Cập nhật prospects/crm_pipeline.json lên 60 doanh nghiệp.
5. Nâng cấp tổng dung lượng phễu B2B lên $84,000+ Upfront & $44,500/tháng MRR.
"""

import sys
import os
import json
import urllib.parse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

# Import generation modules
sys.path.insert(0, str(ROOT_DIR / "scripts"))
try:
    from generate_client_sandbox import generate_sandbox
    from generate_client_roi_report import generate_roi_report
    from generate_client_pitch_deck import generate_pitch_deck
    from generate_client_portal import generate_client_portal
except ImportError as e:
    print(f"[!] Lỗi import modules: {e}")

NEW_LEADS = [
    # --- BATCH 4: High-End Home Services & Luxury Contracting ---
    {"id": 31, "batch": 4, "name": "BlueWave Custom Pools", "niche": "Luxury Pools & Spas", "city": "Phoenix, AZ", "to": "design@bluewavecustompools.example", "doc": "Jason Bennett", "type": "contractor", "val": 5000, "lost": 4, "retainer": 750, "color": "#0284c7", "icon": "🏊"},
    {"id": 32, "batch": 4, "name": "SolarMatrix EPC", "niche": "Commercial & Residential Solar", "city": "Las Vegas, NV", "to": "quotes@solarmatrixepc.example", "doc": "Elena Hayes", "type": "contractor", "val": 6000, "lost": 3, "retainer": 850, "color": "#f59e0b", "icon": "☀️"},
    {"id": 33, "batch": 4, "name": "Elite Artisan Kitchens", "niche": "Luxury Kitchen Remodeling", "city": "Charlotte, NC", "to": "concierge@eliteartisankitchens.example", "doc": "Marcus Sterling", "type": "contractor", "val": 4500, "lost": 4, "retainer": 750, "color": "#b45309", "icon": "🍳"},
    {"id": 34, "batch": 4, "name": "Ironclad Foundation Repair", "niche": "Structural Foundation Engineering", "city": "Nashville, TN", "to": "inspections@ironcladfoundation.example", "doc": "Travis Cole", "type": "contractor", "val": 3800, "lost": 5, "retainer": 700, "color": "#475569", "icon": "🏗️"},
    {"id": 35, "batch": 4, "name": "Sierra Vista Landscape Architecture", "niche": "High-End Hardscaping", "city": "Salt Lake City, UT", "to": "inquiries@sierravistalandscape.example", "doc": "Chloe Davies", "type": "contractor", "val": 3500, "lost": 5, "retainer": 700, "color": "#15803d", "icon": "🌲"},
    {"id": 36, "batch": 4, "name": "Paramount Commercial Roofing", "niche": "Industrial Roofing Systems", "city": "Houston, TX", "to": "estimates@paramountcommroofing.example", "doc": "Robert Lang", "type": "contractor", "val": 7500, "lost": 3, "retainer": 950, "color": "#1e293b", "icon": "🏢"},
    {"id": 37, "batch": 4, "name": "Precision Climate HVAC", "niche": "Commercial Smart HVAC", "city": "Tampa, FL", "to": "service@precisionclimatefl.example", "doc": "Derek Vance", "type": "hvac", "val": 1200, "lost": 12, "retainer": 650, "color": "#0ea5e9", "icon": "❄️"},
    {"id": 38, "batch": 4, "name": "Tri-State Architectural Glass", "niche": "Custom Glazing & Railings", "city": "Philadelphia, PA", "to": "bids@tristateglasspa.example", "doc": "Anthony Russo", "type": "contractor", "val": 4200, "lost": 4, "retainer": 750, "color": "#06b6d4", "icon": "🪟"},
    {"id": 39, "batch": 4, "name": "Benchmark Custom Builders", "niche": "Modern Luxury Custom Homes", "city": "Raleigh, NC", "to": "plans@benchmarkcustomnc.example", "doc": "Jonathan Drake", "type": "contractor", "val": 8000, "lost": 3, "retainer": 1000, "color": "#854d0e", "icon": "🏡"},
    {"id": 40, "batch": 4, "name": "Apex Disaster Restoration", "niche": "24/7 Fire & Water Mitigation", "city": "Minneapolis, MN", "to": "emergency@apexrestorationmn.example", "doc": "Sarah Lindqvist", "type": "hvac", "val": 5500, "lost": 4, "retainer": 800, "color": "#dc2626", "icon": "🚨"},

    # --- BATCH 5: High-Growth B2B Agencies & Tech Staffing ---
    {"id": 41, "batch": 5, "name": "Kinetic Growth Media", "niche": "Paid Acquisition & Performance Ads", "city": "Austin, TX", "to": "growth@kineticgrowthmedia.example", "doc": "Alex Rivera", "type": "agency", "val": 2800, "lost": 6, "retainer": 750, "color": "#8b5cf6", "icon": "📈"},
    {"id": 42, "batch": 5, "name": "HyperScale Search", "niche": "Executive Tech Search & Staffing", "city": "San Francisco, CA", "to": "talent@hyperscalesearch.example", "doc": "Samantha Reed", "type": "agency", "val": 4500, "lost": 4, "retainer": 900, "color": "#6366f1", "icon": "🎯"},
    {"id": 43, "batch": 5, "name": "CinemaCraft Studios", "niche": "B2B SaaS 3D & Product Video", "city": "Los Angeles, CA", "to": "producers@cinemacraftstudios.example", "doc": "Julian Mercer", "type": "agency", "val": 3200, "lost": 5, "retainer": 750, "color": "#ec4899", "icon": "🎥"},
    {"id": 44, "batch": 5, "name": "SearchVelocity AI", "niche": "Enterprise AI Search & SEO", "city": "New York, NY", "to": "strategy@searchvelocityai.example", "doc": "Nathan Ross", "type": "agency", "val": 3000, "lost": 6, "retainer": 800, "color": "#10b981", "icon": "🔍"},
    {"id": 45, "batch": 5, "name": "Fractional CFO Partners", "niche": "Strategic Finance & M&A Advisory", "city": "Chicago, IL", "to": "advisory@fractionalcfochi.example", "doc": "William Thornton", "type": "cpa", "val": 4000, "lost": 4, "retainer": 900, "color": "#334155", "icon": "💼"},
    {"id": 46, "batch": 5, "name": "BrandForge Creative", "niche": "Luxury Brand Identity & Design", "city": "Seattle, WA", "to": "hello@brandforgecreative.example", "doc": "Maya Lin", "type": "agency", "val": 2600, "lost": 7, "retainer": 700, "color": "#d946ef", "icon": "🎨"},
    {"id": 47, "batch": 5, "name": "LeadIgnite B2B", "niche": "Outbound Sales & Lead Gen Engine", "city": "Boston, MA", "to": "pipeline@leadigniteb2b.example", "doc": "Connor Hayes", "type": "agency", "val": 2400, "lost": 8, "retainer": 700, "color": "#f97316", "icon": "🔥"},
    {"id": 48, "batch": 5, "name": "DevSprint Staffing", "niche": "Nearshore Cloud & AI Engineers", "city": "Miami, FL", "to": "engineers@devsprintstaffing.example", "doc": "Ricardo Silva", "type": "agency", "val": 3500, "lost": 5, "retainer": 800, "color": "#3b82f6", "icon": "💻"},
    {"id": 49, "batch": 5, "name": "Quantum Content Lab", "niche": "Technical Writing & Thought Leadership", "city": "Denver, CO", "to": "editors@quantumcontentlab.example", "doc": "Hannah Brooks", "type": "agency", "val": 2200, "lost": 8, "retainer": 650, "color": "#a855f7", "icon": "✍️"},
    {"id": 50, "batch": 5, "name": "RetentionLoop CRM", "niche": "Customer Success & Churn Mitigation", "city": "Atlanta, GA", "to": "success@retentionloopcrm.example", "doc": "Marcus Bell", "type": "saas", "val": 2500, "lost": 7, "retainer": 700, "color": "#14b8a6", "icon": "🔄"},

    # --- BATCH 6: Specialized Luxury Healthcare & Wellness ---
    {"id": 51, "batch": 6, "name": "Beverly Hills Plastic Surgery", "niche": "Aesthetic & Reconstructive Surgery", "city": "Beverly Hills, CA", "to": "vip@bhplasticsurgeryca.example", "doc": "Dr. Katherine Cole", "type": "medical", "val": 6500, "lost": 3, "retainer": 950, "color": "#f43f5e", "icon": "✨"},
    {"id": 52, "batch": 6, "name": "Apex Orthopedic Spine Institute", "niche": "Minimally Invasive Spine Surgery", "city": "Dallas, TX", "to": "intake@apexspineinstitute.example", "doc": "Dr. Gregory Vance", "type": "medical", "val": 5500, "lost": 4, "retainer": 900, "color": "#0284c7", "icon": "🩺"},
    {"id": 53, "batch": 6, "name": "NovoGen Fertility Specialists", "niche": "IVF & Reproductive Genetics", "city": "San Diego, CA", "to": "care@novogenfertility.example", "doc": "Dr. Maria Santos", "type": "medical", "val": 7000, "lost": 3, "retainer": 1000, "color": "#ec4899", "icon": "🧬"},
    {"id": 54, "batch": 6, "name": "Serenity Longevity & Cryo", "niche": "Executive Biohacking & Anti-Aging", "city": "Miami, FL", "to": "concierge@serenitylongevity.example", "doc": "Dr. Lucas Meyer", "type": "medical", "val": 2500, "lost": 8, "retainer": 750, "color": "#06b6d4", "icon": "🧊"},
    {"id": 55, "batch": 6, "name": "Optima Concierge Medicine", "niche": "Private Executive Primary Care", "city": "Scottsdale, AZ", "to": "membership@optimaconciergemed.example", "doc": "Dr. Arthur Pendelton", "type": "medical", "val": 3800, "lost": 5, "retainer": 850, "color": "#059669", "icon": "⚕️"},
    {"id": 56, "batch": 6, "name": "Restore Regenerative Ortho", "niche": "Cellular Therapy & PRP Injections", "city": "Chicago, IL", "to": "appointments@restoreregenortho.example", "doc": "Dr. Steven Choi", "type": "medical", "val": 3200, "lost": 6, "retainer": 800, "color": "#84cc16", "icon": "🩹"},
    {"id": 57, "batch": 6, "name": "ClearVision Lasik Center", "niche": "Contoura Vision & Refractive Surgery", "city": "Atlanta, GA", "to": "consult@clearvisionlasikatl.example", "doc": "Dr. Angela White", "type": "medical", "val": 3500, "lost": 6, "retainer": 800, "color": "#2563eb", "icon": "👁️"},
    {"id": 58, "batch": 6, "name": "PureBreathe Sinus Institute", "niche": "Advanced Balloon Sinuplasty & ENT", "city": "Houston, TX", "to": "relief@purebreathesinus.example", "doc": "Dr. Farhan Qasim", "type": "medical", "val": 2800, "lost": 7, "retainer": 750, "color": "#0891b2", "icon": "💨"},
    {"id": 59, "batch": 6, "name": "Radiance Hair Restoration", "niche": "Robotic ARTAS FUE Transplants", "city": "New York, NY", "to": "evaluations@radiancehairrestoration.example", "doc": "Dr. James Sterling", "type": "medical", "val": 5000, "lost": 4, "retainer": 900, "color": "#d97706", "icon": "💈"},
    {"id": 60, "batch": 6, "name": "Thrive Neuro & Brain Health", "niche": "Deep TMS & Cognitive Optimization", "city": "San Jose, CA", "to": "eval@thriveneurohealth.example", "doc": "Dr. Rachel Green", "type": "medical", "val": 3000, "lost": 6, "retainer": 800, "color": "#7c3aed", "icon": "🧠"}
]

def expand_pipeline():
    crm_file = ROOT_DIR / "prospects" / "crm_pipeline.json"
    existing = json.loads(crm_file.read_text(encoding="utf-8")) if crm_file.exists() else []
    existing_ids = {l["id"] for l in existing}

    added = 0
    for lead in NEW_LEADS:
        if lead["id"] not in existing_ids:
            item = {
                "id": lead["id"],
                "batch": lead["batch"],
                "name": lead["name"],
                "niche": lead["niche"],
                "city": lead["city"],
                "to": lead["to"],
                "doc": lead["doc"],
                "status": "new",
                "value": lead.get("val", 1500),
                "retainer": lead.get("retainer", 750),
                "last_touch": None
            }
            existing.append(item)
            added += 1

    crm_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[✓] Cập nhật CRM Pipeline: Thêm mới {added} doanh nghiệp (Tổng cộng: {len(existing)} leads)")
    return existing

def generate_assets_for_new_leads():
    sandboxes_dir = ROOT_DIR / "sandboxes"
    reports_dir = ROOT_DIR / "reports"
    pitches_dir = ROOT_DIR / "pitches"
    
    sandboxes_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    pitches_dir.mkdir(parents=True, exist_ok=True)

    print("\n[*] KHỞI TẠO TÀI NGUYÊN WEB CHO 30 DOANH NGHIỆP MỚI:")
    for l in NEW_LEADS:
        name = l["name"]
        niche = l["niche"]
        city = l["city"]
        color = l.get("color", "#7c5cfc")
        val = l.get("val", 1200)
        lost = l.get("lost", 10)
        lead_id = l["id"]

        # 1. Sandbox
        sb_file = generate_sandbox(lead_id, name, niche, city, color)

        # 2. ROI Report
        roi_file = generate_roi_report(lead_id, name, niche, city, val, lost)

        # 3. Pitch Deck
        pitch_file = generate_pitch_deck(lead_id, name, niche, city, val, lost)

        # 4. VIP Portal
        portal_file = generate_client_portal(l)

        print(f"  [✓] #{lead_id:02d} {name}: Sandbox, ROI Report, Pitch Deck & VIP Portal Ready")

def send_telegram_expansion_alert(total_leads, added_count, total_pipeline_val, total_mrr):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    msg = f"""🚀 <b>[B2B CRM PIPELINE EXPANSION: 60 LEADS ACTIVATED]</b>

📈 <b>Quy Mô Phễu Mới:</b>
• <b>Tổng Doanh Nghiệp Mục Tiêu:</b> <code>{total_leads} Doanh Nghiệp (+{added_count} Leads Mới)</code>
• <b>Tổng Dung Lượng Upfront:</b> <code>${total_pipeline_val:,}</code>
• <b>Tiềm Năng Dòng Tiền MRR:</b> <code>${total_mrr:,}/tháng</code>

🏢 <b>3 Phân Khúc Mới Bổ Sung (30 Leads):</b>
• <b>Batch 4 (Leads 31-40):</b> High-End Home Services & Luxury Contracting (Pools, Solar EPC, Modern Homes)
• <b>Batch 5 (Leads 41-50):</b> High-Growth B2B Agencies & Tech Search (Ads, Video, Nearshore AI, Fractional CFO)
• <b>Batch 6 (Leads 51-60):</b> Specialized Luxury Healthcare & Surgery (Plastic Surgery, Spine, IVF, Cryo)

🛠️ <b>Tài Nguyên Độc Bản Đã Khởi Tạo:</b>
• 30 Live Sandboxes Demo mới tại <code>/sandboxes/</code>
• 30 Báo cáo kiểm toán ROI mới tại <code>/reports/</code>
• 30 Bản Sales Pitch Decks mới tại <code>/pitches/</code>

👉 <a href="https://work-minh-lap.vercel.app/portal"><b>Mở VIP Client Portals Hub</b></a>
👉 <a href="https://work-minh-lap.vercel.app"><b>Mở Executive Command Center</b></a>
🔥 <i>Hệ thống phễu khách hàng đã sẵn sàng cho chiến dịch phủ sóng tiếp theo!</i>"""

    try:
        import subprocess
        payload_file = ROOT_DIR / "temp_tg_expand.json"
        payload_file.write_text(json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, ensure_ascii=False), encoding="utf-8")
        res = subprocess.run(
            ["curl.exe", "-s", "--connect-timeout", "10", "--max-time", "20", "-X", "POST",
             "-H", "Content-Type: application/json; charset=utf-8",
             "-d", f"@{payload_file.name}",
             f"https://api.telegram.org/bot{bot_token}/sendMessage"],
            capture_output=True, text=True, timeout=22, cwd=str(ROOT_DIR)
        )
        if payload_file.exists():
            payload_file.unlink()
        if '"ok":true' in res.stdout:
            print("[✓] Đã gửi thông báo mở rộng phễu 60 Leads về Telegram (@Minhpv_bot)!")
        else:
            print(f"[!] Telegram curl error: {res.stdout}")
    except Exception as e:
        print(f"[!] Lỗi gửi Telegram: {e}")

def main():
    print("=" * 70)
    print("🏢 ENTERPRISE PIPELINE EXPANSION ENGINE — AI MONEY MACHINE")
    print("=" * 70)

    all_leads = expand_pipeline()
    generate_assets_for_new_leads()

    total_pipeline_val = sum(l.get("value", 1200) for l in all_leads)
    total_mrr = sum(l.get("retainer", 650) for l in all_leads)

    print("\n" + "=" * 70)
    print("📊 BÁO CÁO TỔNG QUAN PHỄU 60 DOANH NGHIỆP:")
    print(f"  • Tổng số khách hàng:       {len(all_leads)} leads")
    print(f"  • Tổng dung lượng Upfront:   ${total_pipeline_val:,}")
    print(f"  • Tiềm năng định kỳ (MRR):  ${total_mrr:,}/tháng")
    print("=" * 70)

    send_telegram_expansion_alert(len(all_leads), len(NEW_LEADS), total_pipeline_val, total_mrr)

if __name__ == "__main__":
    main()
