"""
Synapse Autonomous Auto-Pilot Service
-------------------------------------
Tiến trình chạy nền liên tục (Daemon) tự động:
1. Định kỳ quét thị trường quốc tế (Hacker News, GitHub Trending, Dev.to).
2. Phát hiện các ngách Micro-SaaS mới đang có nhiều người quan tâm.
3. Cập nhật cơ sở dữ liệu cơ hội kinh doanh mà không cần người dùng thao tác.
"""

import time
import sys
import os
from datetime import datetime

# Import scout function
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from market_scout import run_scout

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

POLL_INTERVAL_SECONDS = 3600 * 6  # Quét mỗi 6 tiếng một lần

def start_autopilot():
    print("[*] ===================================================")
    print("[*] SYNAPSE AUTONOMOUS AUTO-PILOT ENGINE ĐANG HOẠT ĐỘNG")
    print(f"[*] Tần suất quét tự động: Mỗi {POLL_INTERVAL_SECONDS // 3600} giờ")
    print("[*] ===================================================")

    iteration = 1
    while True:
        print(f"\n[+] [Chu kỳ #{iteration}] Bắt đầu chu kỳ quét tự động: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            run_scout()
            print(f"[✓] [Chu kỳ #{iteration}] Đã cập nhật xong dữ liệu cơ hội thị trường!")
        except Exception as e:
            print(f"[!] Lỗi trong chu kỳ #{iteration}: {e}")

        iteration += 1
        print(f"[*] Nghỉ ngơi trước chu kỳ tiếp theo ({POLL_INTERVAL_SECONDS}s)...")
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    start_autopilot()
