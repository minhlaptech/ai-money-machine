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
  ⚡ SYNAPSE AI MONEY MACHINE — MASTER COMMAND CENTER CLI v5.0 ⚡
  Tác giả: Minh Lap | 8 Nguồn Thu Nhập Số Độc Lập & Tự Động Hóa
======================================================================
  [1] 🩺 Chạy Kiểm Tra Sức Khỏe Toàn Diện Hệ Thống (Health Check & Ping)
  [2] 📡 Quét Thị Trường & Bắt Xu Hướng AI Nóng (AI Market Scout)
  [3] 🎯 Săn Tìm & Trích Xuất Khách Hàng Địa Phương Mới (Lead Finder)
  [4] 📑 Tạo Bản Đề Xuất & Báo Cáo Kiểm Toán (Tùy Chọn Cá Nhân hoặc Trọn Bộ 30 Leads)
  [5] 🖥️ Tạo Bộ Trình Chiếu Chốt Sale Tương Tác (10-Slide Sales Pitch Deck)
  [6] 🧪 Tạo Môi Trường Thử Nghiệm Tương Tác (Live Client Sandbox & 5 Automated Tests)
  [7] 📝 Tạo Hợp Đồng Dịch Vụ Master Services Agreement (MSA & Chữ Ký Số Trực Tuyến)
  [8] 💳 Xuất Hóa Đơn Khách Hàng B2B Chuyên Nghiệp (Invoices: $1,200 Setup + $650 Retainer)
  [9] 📊 Tạo Báo Cáo Đo Lường ROI Hàng Tháng Khách Hàng (Monthly Performance & ROI Report)
  [10] 📬 Điều Hướng Chiến Dịch Cold Outreach Đa Chạm (Multi-Touch Outreach Dispatcher)
  [11] 💼 Tạo Thư Ứng Tuyển Upwork Thắng Thầu (Upwork Cover Letter)
  [12] 📱 Tái Chế Nội Dung Đa Kênh (Twitter / LinkedIn / TikTok / Reddit)
  [13] 📺 Xuất Trọn Bộ Metadata Video YouTube (Titles, Tags, Timestamps)
  [14] 👕 Tạo Bài Đăng Bán Hàng Print-on-Demand (Etsy / Printify Listing)
  [15] 📦 Đóng Gói Bộ 15 Kịch Bản Tự Động Hóa Make.com/n8n (Blueprint Pack ZIP)
  [16] 📈 Xem Báo Cáo Phễu Khách Hàng B2B CRM (Pipeline Summary & Deal Value)
  [17] ☀️ Chạy Bản Tin Chỉ Huy Sáng (Daily Morning Briefing & Telegram Ping)
  [18] 🎯 Mở Trung Tâm Trình Chiếu Pitch Decks Showcase Hub (/pitches)
  [19] 📦 Đóng Gói Bộ Hồ Sơ Onboarding VIP ZIP Cho Khách Hàng (30 Client Packages)
  [20] 🚀 Mở Executive Command Center Dashboard trên Trình Duyệt Web
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
        choice = input("👉 Nhập số lựa chọn tác vụ của bạn [0-20]: ").strip()

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
            sub = input("Tạo đề xuất cho 1 khách hàng hay toàn bộ 30 leads? (1: Một khách / 30: Trọn bộ 30 leads, mặc định 30): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp khách hàng: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_proposal.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/batch_proposal_generator.py")

        elif choice == '5':
            sub = input("Tạo Pitch Deck cho 1 khách hàng hay toàn bộ 30 leads? (1: Một khách / 30: Trọn bộ 30 leads, mặc định 30): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_pitch_deck.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_pitch_deck.py", ["--all"])

        elif choice == '6':
            sub = input("Tạo Sandbox thử nghiệm cho 1 khách hàng hay toàn bộ 30 leads? (1: Một khách / 30: Trọn bộ 30 leads, mặc định 30): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_sandbox.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_sandbox.py", ["--all"])

        elif choice == '7':
            sub = input("Tạo hợp đồng cho 1 khách hàng hay toàn bộ 30 leads? (1: Một khách / 30: Trọn bộ 30 leads, mặc định 30): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp khách hàng: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_agreement.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_agreement.py", ["--all"])

        elif choice == '8':
            sub = input("Xuất hóa đơn cho 1 khách hàng hay toàn bộ 30 leads? (1: Một khách / 30: Trọn bộ 30 leads, mặc định 30): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp khách hàng: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_invoice.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_invoice.py", ["--all"])

        elif choice == '9':
            sub = input("Tạo báo cáo ROI cho 1 khách hàng hay toàn bộ 30 leads? (1: Một khách / 30: Trọn bộ 30 leads, mặc định 30): ").strip()
            if sub == '1':
                name = input("Nhập tên doanh nghiệp: ").strip() or "Austin Dental Co"
                niche = input("Nhập lĩnh vực: ").strip() or "Cosmetic Dentistry"
                city = input("Nhập thành phố: ").strip() or "Austin, TX"
                run_script("scripts/generate_client_roi_report.py", ["--name", name, "--niche", niche, "--city", city])
            else:
                run_script("scripts/generate_client_roi_report.py", ["--all"])

        elif choice == '10':
            batch = input("Chọn Batch tiếp cận (1: SMBs / 2: E-Com & SaaS / 3: High-Ticket / Enter: Tất cả): ").strip()
            stage = input("Chọn giai đoạn (1: Day 1 Hook / 2: Day 3 ROI / 3: Day 7 Break-Up, mặc định 1): ").strip() or "1"
            args = ["--stage", stage]
            if batch in ['1', '2', '3']:
                args.extend(["--batch", batch])
            run_script("scripts/outreach_dispatcher.py", args)

        elif choice == '11':
            jtype = input("Chọn loại công việc (chatbot / automation / scraping, mặc định chatbot): ").strip() or "chatbot"
            client = input("Tên khách hàng trên Upwork (nếu biết, mặc định there): ").strip() or "there"
            notes = input("Yêu cầu cụ thể từ bài đăng Upwork: ").strip()
            run_script("scripts/upwork_proposal_generator.py", ["--type", jtype, "--client", client, "--notes", notes])

        elif choice == '12':
            topic = input("Chọn chủ đề (geo_audit / ai_automation / microsaas_blueprint, mặc định geo_audit): ").strip() or "geo_audit"
            run_script("scripts/social_repurpose_engine.py", ["--topic", topic])

        elif choice == '13':
            vid = input("Chọn mã video (video_005 / video_006 / video_007 / video_008, mặc định video_008): ").strip() or "video_008"
            run_script("scripts/youtube_seo_generator.py", ["--video", vid])

        elif choice == '14':
            item = input("Chọn sản phẩm (hoodie_coffee_llms / tshirt_it_works / mug_ai_brain, mặc định hoodie_coffee_llms): ").strip() or "hoodie_coffee_llms"
            run_script("scripts/pod_listing_generator.py", ["--item", item])

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
            sub = input("Đóng gói trọn bộ 30 khách hàng hay 1 khách cụ thể? (1-30: Nhập ID khách / Enter: Toàn bộ 30 khách): ").strip()
            if sub.isdigit() and 1 <= int(sub) <= 30:
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

        elif choice == '0':
            print("\n👋 Tạm biệt! Chúc bạn kinh doanh thành công và tạo dòng tiền mạnh mẽ với AI.\n")
            break
        else:
            print("[!] Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 20.")

        input("\n[Nhấn Enter để quay lại menu chính...]")

if __name__ == "__main__":
    main_loop()
