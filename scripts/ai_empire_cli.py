"""
AI Money Machine — Master Executive CLI Orchestrator
-----------------------------------------------------
Trung tâm điều hành dòng lệnh hợp nhất toàn bộ 8 cỗ máy tự động hóa
trong hệ sinh thái AI Money Machine. Cho phép chạy bất kỳ tác vụ nào
bằng 1 phím bấm số duy nhất mà không cần nhớ câu lệnh phức tạp.
"""

import sys
import os
import subprocess
import webbrowser
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print("""
======================================================================
  ⚡ SYNAPSE AI MONEY MACHINE — MASTER COMMAND CENTER CLI v15.0 ⚡
  Tác giả: Minh Lap | 8 Nguồn Thu Nhập Số Độc Lập & Tự Động Hóa
======================================================================
  [1] 🩺 Chạy Kiểm Tra Sức Khỏe Toàn Diện Hệ Thống (Health Check & Ping)
  [2] 📡 Quét Thị Trường & Bắt Xu Hướng AI Nóng (AI Market Scout)
  [3] 🎯 Săn Tìm & Trích Xuất Khách Hàng Địa Phương Mới (Lead Finder)
  [4] 📑 Tạo Bản Đề Xuất & Báo Cáo Kiểm Toán (Tùy Chọn Cá Nhân hoặc Trọn Bộ 60 Leads)
  [5] 🖥️ Tạo Bộ Trình Chiếu Chốt Sale Tương Tác (10-Slide Sales Pitch Deck: 60 Decks)
  [6] 🧪 Tạo Môi Trường Thử Nghiệm Tương Tác (Live Client Sandbox & 5 Automated Tests)
  [7] 📝 Tạo Hợp Đồng Dịch Vụ Master Services Agreement (MSA & Chữ Ký Số Trực Tuyến)
  [8] 💳 Xuất Hóa Đơn Khách Hàng B2B Chuyên Nghiệp (Invoices: $1,200 Setup + $650 Retainer)
  [9] 📊 Tạo Báo Cáo Đo Lường ROI Hàng Tháng Khách Hàng (Monthly Performance & ROI Report)
  [10] 📬 Điều Hướng Chiến Dịch Cold Outreach Đa Chạm (Multi-Touch Outreach: 6 Batches / 60 Leads)
  [11] 💼 Tạo Thư Ứng Tuyển Upwork Thắng Thầu (Upwork Cover Letter)
  [12] 📱 Tái Chế Nội Dung Đa Kênh (Twitter / LinkedIn / TikTok / Reddit)
  [13] 📺 Xuất Trọn Bộ Metadata Video YouTube (Titles, Tags, Timestamps)
  [14] 👕 Tạo Bài Đăng Print-on-Demand (6 Sản Phẩm: Hoodie, Tee, Mug, DeskMat, Tote, Cap)
  [15] 📦 Đóng Gói Bộ 15 Kịch Bản Tự Động Hóa Make.com/n8n (Blueprint Pack ZIP)
  [16] 📈 Xem Báo Cáo Phễu Khách Hàng B2B CRM (Pipeline Summary & Deal Value)
  [17] ☀️ Chạy Bản Tin Chỉ Huy Sáng (Daily Morning Briefing & Telegram Ping)
  [18] 🎯 Mở Trung Tâm Trình Chiếu Pitch Decks Showcase Hub (/pitches - 60 Decks)
  [19] 📦 Đóng Gói Bộ Hồ Sơ Onboarding VIP ZIP Cho Khách Hàng (60 Client Packages)
  [20] 🚀 Mở Executive Command Center Dashboard trên Trình Duyệt Web
  [21] 💰 Bắn Thử Nghiệm Webhook Bán Hàng & Đơn Hàng Mới (Simulate Sales Webhook)
  [22] 📋 Xuất Trọn Bộ Dữ Liệu Phễu B2B CRM Ra File CSV / JSON (Export 60 Leads & Live URLs)
  [23] 🏛️ Mở Executive Client VIP Portal Hub (/portal & 60 Dedicated Portals)
  [24] 🤝 Mở Cổng Quản Lý Đối Tác & Tiếp Thị Liên Kết (/referral - 50% RevShare)
  [25] 🎙️ Studio Sản Xuất Voiceover AI & Phụ Đề SRT (30 Shorts / 10 Full Episodes)
  [26] 🎬 Xưởng Render Video MP4 Tự Động (FFmpeg Broadcast H.264 / 4K Thumbnails / Subtitles)
  [27] 📅 Xuất Lịch Đăng Mạng Xã Hội Buffer CSV & JSON Hub (Social Scheduler)
  [28] 🚀 Mở AI Media & Video Studio Hub trên Trình Duyệt Web (/studio)
  [29] ☁️ Triển Khai Monorepo Lên Vercel Production (Auto Deploy Production)
  [30] 💼 Mở Sàn Dịch Vụ AI Freelance & Agency Hub (/freelance - 8 High-Ticket Gigs)
  [31] 👕 Mở Sàn Thương Mại Merch Đồ Lập Trình Viên POD (/merch - 6 Sản Phẩm)
  [32] 📺 Xuất Lịch Phát Sóng YouTube 40 Video & Gửi Lộ Trình (YouTube Publishing Engine)
  [33] 🚀 Mở Rộng Phễu Doanh Nghiệp Lên 60 Accounts & $161,700 Pipeline (Expand CRM Pipeline)
  [34] ⚡ Kích Hoạt Nhanh Chiến Dịch Cold Outreach Stage 1-3 Kèm Telegram Ping
  [35] ⚡ Khởi Chạy Micro-SaaS Suite Hub & Bộ 3 AI Tools (/tools & /saas - $39 Pass)
  [36] 🚪 Kích Hoạt Chiến Dịch Stage 3 Break-Up Outreach (Day 7 FOMO Close 60 Leads)
  [37] 📦 Mở Trang Bán Hàng Master Bundle Showcase (/bundle - Lemon Squeezy Store ID 485872)
  [38] 📋 Mở VIP Client Onboarding Intake Hub (/onboarding - 48h SLA Sprint)
  [39] 📊 Cập Nhật Trạng Thái Deal B2B CRM & Bắn Cảnh Báo Telegram (CRM Deal Tracker)
  [40] 💳 Giả Lập & Kiểm Thử Doanh Thu Webhook Đa Kênh (/api/webhook Simulator)
  [41] 📋 Giả Lập & Kiểm Thử Nộp Hồ Sơ Onboarding VIP (/api/contact Simulator)
  [42] 📈 Xuất Báo Cáo Hiệu Suất Tuần Khách Hàng Retainer (Weekly Retention Reporter & Telegram Ping)
  [0] Thoát
======================================================================
""")

def run_script(rel_path, args=None):
    script_path = ROOT_DIR / rel_path
    if not script_path.exists():
        print(f"[!] Không tìm thấy script: {script_path}")
        return
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    print(f"\n[*] Đang thực thi: {' '.join(cmd)}\n" + "-"*60)
    subprocess.run(cmd, cwd=str(ROOT_DIR))
    print("-"*60 + "\n[✓] Hoàn thành tác vụ!")

def main_loop():
    while True:
        print_banner()
        choice = input("👉 Nhập số lựa chọn tác vụ của bạn [0-42]: ").strip()

        if choice == '1':
            ping = input("Bạn có muốn gửi báo cáo về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = ["--ping"] if ping != 'n' else []
            run_script("scripts/system_health_check.py", args)

        elif choice == '2':
            run_script("autonomous_agent/market_scout.py")

        elif choice == '3':
            niche = input("Nhập ngành nghề (dentist / doctor / lawyer / cpa / realestate, mặc định dentist): ").strip() or "dentist"
            city = input("Nhập thành phố (Austin / Miami / Chicago / Dallas, mặc định Austin): ").strip() or "Austin"
            limit = input("Số lượng khách cần quét (mặc định 5): ").strip() or "5"
            run_script("scripts/lead_finder.py", ["--niche", niche, "--city", city, "--limit", limit])

        elif choice == '4':
            sub = input("Tạo đề xuất cho 1 khách hàng hay toàn bộ 60 leads? (1: Một khách / 60: Trọn bộ 60 leads, mặc định 60): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp khách hàng: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_proposal.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/batch_proposal_generator.py")

        elif choice == '5':
            sub = input("Tạo Pitch Deck cho 1 khách hàng hay toàn bộ 60 leads? (1: Một khách / 60: Trọn bộ 60 leads, mặc định 60): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_pitch_deck.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_pitch_deck.py", ["--all"])

        elif choice == '6':
            sub = input("Tạo Sandbox thử nghiệm cho 1 khách hàng hay toàn bộ 60 leads? (1: Một khách / 60: Trọn bộ 60 leads, mặc định 60): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_sandbox.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_sandbox.py", ["--all"])

        elif choice == '7':
            sub = input("Tạo hợp đồng cho 1 khách hàng hay toàn bộ 60 leads? (1: Một khách / 60: Trọn bộ 60 leads, mặc định 60): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp khách hàng: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_agreement.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_agreement.py", ["--all"])

        elif choice == '8':
            sub = input("Xuất hóa đơn cho 1 khách hàng hay toàn bộ 60 leads? (1: Một khách / 60: Trọn bộ 60 leads, mặc định 60): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp khách hàng: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_invoice.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_invoice.py", ["--all"])

        elif choice == '9':
            sub = input("Tạo báo cáo ROI cho 1 khách hàng hay toàn bộ 60 leads? (1: Một khách / 60: Trọn bộ 60 leads, mặc định 60): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_roi_report.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_roi_report.py", ["--all"])

        elif choice == '10':
            batch = input("Chọn Batch tiếp cận (1: SMBs / 2: E-Com & SaaS / 3: High-Ticket / 4: Contracting / 5: Agency / 6: Healthcare / Enter: Tất cả): ").strip()
            stage = input("Chọn giai đoạn (1: Day 1 Hook / 2: Day 3 ROI / 3: Day 7 Break-Up, mặc định 1): ").strip() or "1"
            tg = input("Bắn danh sách hàng đợi về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = ["--stage", stage]
            if batch in ['1', '2', '3', '4', '5', '6']:
                args.extend(["--batch", batch])
            if tg != 'n':
                args.append("--telegram")
            run_script("scripts/outreach_dispatcher.py", args)

        elif choice == '11':
            sub = input("Tạo trọn bộ 6 Cover Letters hay 1 loại cụ thể? (all: Trọn bộ 6 / Enter: Chọn 1 loại): ").strip().lower()
            if sub == 'all':
                tg = input("Gửi bản xem trước về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--all"]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/upwork_proposal_generator.py", args)
            else:
                print("Các loại công việc: chatbot / automation / scraping / geo_seo / review_management / client_portal")
                jtype = input("Chọn loại công việc (mặc định chatbot): ").strip() or "chatbot"
                client = input("Tên khách hàng trên Upwork (nếu biết, mặc định there): ").strip() or "there"
                notes = input("Yêu cầu cụ thể từ bài đăng Upwork: ").strip()
                tg = input("Gửi bản xem trước về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--type", jtype, "--client", client, "--notes", notes]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/upwork_proposal_generator.py", args)

        elif choice == '12':
            sub = input("Tạo trọn bộ 6 Viral Kits hay 1 chủ đề cụ thể? (all: Trọn bộ 6 kits / Enter: Chọn 1 chủ đề): ").strip().lower()
            if sub == 'all':
                tg = input("Bắn thông báo về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--all"]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/social_repurpose_engine.py", args)
            else:
                print("Chủ đề: geo_audit / ai_automation / microsaas_blueprint / review_management / client_vip_portal / make_automation_secrets")
                topic = input("Chọn chủ đề (mặc định geo_audit): ").strip() or "geo_audit"
                tg = input("Bắn thông báo về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--topic", topic]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/social_repurpose_engine.py", args)

        elif choice == '13':
            vid = input("Chọn mã video (video_005 đến video_010 / Enter: Toàn bộ tất cả): ").strip()
            if not vid or vid.lower() in ['all', 'tat ca']:
                run_script("scripts/youtube_seo_generator.py", ["--all"])
            else:
                run_script("scripts/youtube_seo_generator.py", ["--video", vid])

        elif choice == '14':
            sub = input("Tạo trọn bộ 6 sản phẩm POD hay 1 sản phẩm cụ thể? (all: Trọn bộ 6 / Enter: Chọn 1): ").strip().lower()
            if sub == 'all':
                tg = input("Bắn tóm tắt lợi nhuận về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--all"]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/pod_listing_generator.py", args)
            else:
                print("Sản phẩm: hoodie_coffee_llms / tshirt_it_works / mug_ai_brain / deskmat_prompt_architect / totebag_automate_or_die / cap_10x_engineer")
                item = input("Chọn sản phẩm (mặc định deskmat_prompt_architect): ").strip() or "deskmat_prompt_architect"
                tg = input("Bắn tóm tắt về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--item", item]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/pod_listing_generator.py", args)

        elif choice == '15':
            run_script("scripts/generate_all_blueprints.py")

        elif choice == '16':
            run_script("scripts/crm_tracker.py", ["--summary"])

        elif choice == '17':
            tg = input("Gửi bản tin chỉ huy sáng về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = ["--telegram"] if tg != 'n' else []
            run_script("scripts/daily_briefing.py", args)

        elif choice == '18':
            hub_url = "https://work-minh-lap.vercel.app/pitches"
            local_hub = ROOT_DIR / "pitches" / "index.html"
            print(f"[*] Đang mở Sales Pitch Decks Showcase Hub trên trình duyệt: {hub_url}")
            try:
                webbrowser.open(hub_url)
            except Exception:
                webbrowser.open(local_hub.as_uri())

        elif choice == '19':
            sub = input("Đóng gói trọn bộ 60 khách hàng hay 1 khách cụ thể? (1-60: Nhập ID khách / Enter: Toàn bộ 60 khách): ").strip()
            if sub.isdigit() and 1 <= int(sub) <= 60:
                run_script("scripts/package_client_deliverables.py", ["--lead", sub])
            else:
                run_script("scripts/package_client_deliverables.py", ["--all"])

        elif choice == '20':
            dash_url = "https://work-minh-lap.vercel.app"
            local_dash = ROOT_DIR / "index.html"
            print(f"[*] Đang mở Executive Dashboard trên trình duyệt: {dash_url}")
            try:
                webbrowser.open(dash_url)
            except Exception:
                webbrowser.open(local_dash.as_uri())

        elif choice == '21':
            print("\nChọn kịch bản mô phỏng giao dịch:")
            print("  [1] Lemon Squeezy — The AI Money Blueprint ($47.00)")
            print("  [2] Gumroad — AI Marketing Prompt Pack ($27.00)")
            print("  [3] Stripe / B2B Retainer — AI Copilot Setup ($1,850.00)")
            sc = input("Nhập lựa chọn (1/2/3, mặc định 1): ").strip() or "1"
            sc_map = {"1": "lemonsqueezy_blueprint", "2": "gumroad_prompts", "3": "b2b_retainer_setup"}
            key = sc_map.get(sc, "lemonsqueezy_blueprint")
            run_script("scripts/test_sales_webhook.py", ["--scenario", key])

        elif choice == '22':
            run_script("scripts/export_crm_pipeline.py")

        elif choice == '23':
            sub = input("Tùy chọn: [1] Mở VIP Portal Hub trên trình duyệt / [2] Tạo lại toàn bộ 60 Portals (mặc định 1): ").strip()
            if sub == '2':
                run_script("scripts/generate_client_portal.py", ["--all"])
            else:
                hub_url = "https://work-minh-lap.vercel.app/portal"
                local_hub = ROOT_DIR / "portals" / "index.html"
                print(f"[*] Đang mở Executive Client VIP Portal Hub trên trình duyệt: {hub_url}")
                try:
                    webbrowser.open(hub_url)
                except Exception:
                    webbrowser.open(local_hub.as_uri())

        elif choice == '24':
            ref_url = "https://work-minh-lap.vercel.app/referral"
            local_ref = ROOT_DIR / "projects" / "affiliate_blog" / "website" / "referrals.html"
            print(f"[*] Đang mở Affiliate & Partner Program Hub trên trình duyệt: {ref_url}")
            try:
                webbrowser.open(ref_url)
            except Exception:
                webbrowser.open(local_ref.as_uri())

        elif choice == '25':
            print("\nChọn định dạng nội dung muốn sản xuất Voiceover & Subtitles:")
            print("  [1] 30-Day Viral Shorts / TikTok Sprint (Kịch bản 30-60s)")
            print("  [2] 10 Full-Length Faceless YouTube Channel Episodes (Video 8-10 phút)")
            sub = input("Nhập lựa chọn (1/2, mặc định 1): ").strip()
            if sub == '2':
                ep = input("Nhập số tập (1-10, hoặc 'all' để làm toàn bộ): ").strip().lower()
                tg = input("Bắn báo cáo về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--type", "episode"]
                if ep == 'all':
                    args.append("--all")
                elif ep.isdigit() and 1 <= int(ep) <= 10:
                    args.extend(["--episode", ep])
                else:
                    args.extend(["--episode", "1"])
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/voiceover_generator.py", args)
            else:
                day = input("Nhập số ngày (1-30, hoặc 'all' để làm toàn bộ): ").strip().lower()
                tg = input("Bắn báo cáo về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--type", "shorts"]
                if day == 'all':
                    args.append("--all")
                elif day.isdigit() and 1 <= int(day) <= 30:
                    args.extend(["--day", day])
                else:
                    args.extend(["--day", "1"])
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/voiceover_generator.py", args)

        elif choice == '26':
            print("\nChọn loại video bạn muốn Render tự động:")
            print("  [1] 30-Day Viral Shorts (9:16 vertical 1080x1920 cho TikTok/Reels/Shorts)")
            print("  [2] 10 Full-Length Faceless YouTube Episodes (16:9 widescreen 1920x1080)")
            sub = input("Nhập lựa chọn (1/2, mặc định 1): ").strip()
            if sub == '2':
                ep = input("Nhập số tập (1-10, hoặc 'all' để render toàn bộ): ").strip().lower()
                tg = input("Bắn báo cáo về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--type", "episode"]
                if ep == 'all':
                    args.append("--all")
                elif ep.isdigit() and 1 <= int(ep) <= 10:
                    args.extend(["--episode", ep])
                else:
                    args.extend(["--episode", "1"])
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/video_assembler.py", args)
            else:
                day = input("Nhập số ngày (1-30, hoặc 'all' để render toàn bộ): ").strip().lower()
                tg = input("Bắn báo cáo về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--type", "shorts"]
                if day == 'all':
                    args.append("--all")
                elif day.isdigit() and 1 <= int(day) <= 30:
                    args.extend(["--day", day])
                else:
                    args.extend(["--day", "1"])
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/video_assembler.py", args)

        elif choice == '27':
            sub = input("Bắn bản tóm tắt nội dung social về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = ["--telegram"] if sub != 'n' else []
            run_script("scripts/social_post_scheduler.py", args)

        elif choice == '28':
            studio_url = "https://work-minh-lap.vercel.app/studio"
            local_studio = ROOT_DIR / "studio" / "index.html"
            print(f"[*] Đang mở AI Media & Video Studio Hub trên trình duyệt: {studio_url}")
            try:
                webbrowser.open(studio_url)
            except Exception:
                webbrowser.open(local_studio.as_uri())

        elif choice == '29':
            print("\n[*] Chuẩn bị deploy hệ thống lên Vercel Production...")
            run_script("scripts/deploy_production.py")

        elif choice == '30':
            freelance_url = "https://work-minh-lap.vercel.app/freelance"
            local_freelance = ROOT_DIR / "freelance" / "index.html"
            print(f"[*] Đang mở AI Freelance & Agency Hub trên trình duyệt: {freelance_url}")
            try:
                webbrowser.open(freelance_url)
            except Exception:
                webbrowser.open(local_freelance.as_uri())

        elif choice == '31':
            merch_url = "https://work-minh-lap.vercel.app/merch"
            local_merch = ROOT_DIR / "merch" / "index.html"
            print(f"[*] Đang mở Sàn Thương Mại Merch Đồ Lập Trình Viên POD trên trình duyệt: {merch_url}")
            try:
                webbrowser.open(merch_url)
            except Exception:
                webbrowser.open(local_merch.as_uri())

        elif choice == '32':
            tg = input("Bắn lịch phát sóng 7 ngày tới về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = ["--manifest"]
            if tg != 'n':
                args.append("--telegram")
            run_script("scripts/youtube_publisher.py", args)

        elif choice == '33':
            print("\n[*] Đang khởi chạy quy trình mở rộng phễu khách hàng lên 60 doanh nghiệp...")
            run_script("scripts/expand_crm_pipeline.py")

        elif choice == '34':
            batch = input("Chọn Batch tiếp cận (1-6 / Enter: Tất cả 60 leads): ").strip()
            stage = input("Chọn giai đoạn (1: Day 1 Hook / 2: Day 3 ROI / 3: Day 7 Break-Up, mặc định 1): ").strip() or "1"
            args = ["--stage", stage, "--mark-sent", "--telegram"]
            if batch in ['1', '2', '3', '4', '5', '6']:
                args.extend(["--batch", batch])
            run_script("scripts/outreach_dispatcher.py", args)

        elif choice == '35':
            saas_url = "https://work-minh-lap.vercel.app/tools"
            local_saas = ROOT_DIR / "tools" / "index.html"
            print(f"[*] Đang mở Micro-SaaS Suite Hub trên trình duyệt: {saas_url}")
            try:
                webbrowser.open(saas_url)
            except Exception:
                webbrowser.open(local_saas.as_uri())

        elif choice == '36':
            batch = input("Chọn Batch tiếp cận Stage 3 Break-Up (1-6 / Enter: Tất cả 60 leads): ").strip()
            tg = input("Bắn thông báo chốt hạ về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = ["--stage", "3", "--mark-sent"]
            if batch in ['1', '2', '3', '4', '5', '6']:
                args.extend(["--batch", batch])
            if tg != 'n':
                args.append("--telegram")
            run_script("scripts/outreach_dispatcher.py", args)

        elif choice == '37':
            bundle_url = "https://work-minh-lap.vercel.app/bundle"
            local_bundle = ROOT_DIR / "bundle" / "index.html"
            print(f"[*] Đang mở Master Bundle Showcase trên trình duyệt: {bundle_url}")
            try:
                webbrowser.open(bundle_url)
            except Exception:
                webbrowser.open(local_bundle.as_uri())

        elif choice == '38':
            onboard_url = "https://work-minh-lap.vercel.app/onboarding"
            local_onboard = ROOT_DIR / "onboarding" / "index.html"
            print(f"[*] Đang mở VIP Client Onboarding Intake Hub trên trình duyệt: {onboard_url}")
            try:
                webbrowser.open(onboard_url)
            except Exception:
                webbrowser.open(local_onboard.as_uri())

        elif choice == '39':
            sub = input("Chọn tác vụ CRM: 1: Xem Dashboard tổng quan / 2: Cập nhật trạng thái deal (1/2, mặc định 1): ").strip()
            if sub == '2':
                lead_id = input("Nhập ID khách hàng cần cập nhật (1-60): ").strip()
                status = input("Chọn trạng thái mới (booked / won / day7 / day3 / day1 / new, mặc định booked): ").strip() or "booked"
                tg = input("Bắn thông báo biến động về Telegram không? (y/n, mặc định y): ").strip().lower()
                args = ["--id", lead_id, "--status", status]
                if tg != 'n':
                    args.append("--telegram")
                run_script("scripts/crm_tracker.py", args)
            else:
                run_script("scripts/crm_tracker.py", ["--summary"])

        elif choice == '40':
            print("\nCác kịch bản giả lập giao dịch doanh thu Webhook:")
            print("  1: Lemon Squeezy - Micro-SaaS All-Access Pass ($39)")
            print("  2: Lemon Squeezy - ReviewGenius Pro Lifetime ($19)")
            print("  3: Lemon Squeezy - Master Bundle ($47)")
            print("  4: Gumroad - Marketing Prompt Pack ($27)")
            print("  5: Stripe - B2B Retainer Setup ($1,850)")
            sc_choice = input("Chọn kịch bản [1-5, mặc định 1]: ").strip()
            sc_map = {
                "1": "microsaas_all_access",
                "2": "reviewgenius_pro",
                "3": "lemonsqueezy_blueprint",
                "4": "gumroad_prompts",
                "5": "b2b_retainer_setup"
            }
            scenario = sc_map.get(sc_choice, "microsaas_all_access")
            run_script("scripts/test_sales_webhook.py", ["--scenario", scenario])

        elif choice == '41':
            print("\nCác kịch bản giả lập nộp hồ sơ Onboarding VIP qua /api/contact:")
            print("  1: Austin Dental Co (Dr. Sarah Jenkins - $1,200 Setup + $650/mo)")
            print("  2: Sterling & Partners Legal (David Sterling, Esq. - $1,500 Setup + $750/mo)")
            print("  3: Beverly Hills Plastic Surgery (Dr. Jason Miller - $4,500 Setup + $1,200/mo)")
            print("  4: Chạy tất cả 3 hồ sơ liên tiếp")
            sc_c = input("Chọn kịch bản [1-4, mặc định 1]: ").strip()
            if sc_c == '2':
                run_script("scripts/test_client_onboarding.py", ["--client", "sterling_legal"])
            elif sc_c == '3':
                run_script("scripts/test_client_onboarding.py", ["--client", "beverly_plastics"])
            elif sc_c == '4':
                run_script("scripts/test_client_onboarding.py", ["--all"])
            else:
                run_script("scripts/test_client_onboarding.py", ["--client", "austin_dental"])

        elif choice == '42':
            sub = input("Tạo báo cáo tuần cho: 1: Tất cả khách hàng Won / 2: Một khách cụ thể theo ID (1/2, mặc định 1): ").strip()
            tg = input("Bắn tóm tắt chỉ huy về Telegram không? (y/n, mặc định y): ").strip().lower()
            args = []
            if sub == '2':
                lead_id = input("Nhập ID khách hàng (1-60): ").strip()
                if lead_id:
                    args.extend(["--id", lead_id])
            else:
                args.append("--all-won")
            if tg != 'n':
                args.append("--telegram")
            run_script("scripts/weekly_client_reporter.py", args)

        elif choice == '0':
            print("\n👋 Tạm biệt! Chúc bạn kinh doanh thành công và tạo dòng tiền mạnh mẽ với AI.\n")
            break
        else:
            print("[!] Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 42.")

        input("\n[Nhấn Enter để quay lại menu chính...]")

if __name__ == "__main__":
    main_loop()
