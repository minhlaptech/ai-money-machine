"""
Sync Root Web Endpoints for Zero-Rewrite Fail-Safe Architecture
-----------------------------------------------------------------
Copies canonical web applications to root folders so that Vercel Clean URLs
serves them automatically with 100% reliability:
- /synapsegeo/
- /reviewgenius/
- /headlineiq/
- /blog/
- /calculator/
- /referral/
- /bundle/
- /chatbotdemo/
"""

import shutil
import sys
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

MAPPINGS = [
    ("products/geo_audit_engine", "synapsegeo"),
    ("products/review_genius", "reviewgenius"),
    ("products/headline_iq", "headlineiq"),
    ("projects/affiliate_blog/website", "blog"),
    ("projects/ai_freelancing/portfolio/chatbot_demo", "chatbotdemo"),
    ("projects/digital_products/bundle_showcase.html", "bundle/index.html"),
    ("projects/ai_automation_smb/roi_calculator.html", "calculator/index.html"),
    ("projects/affiliate_blog/website/referrals.html", "referral/index.html")
]

def sync_endpoints():
    print("=" * 65)
    print("🔄 SYNCING ZERO-REWRITE ROOT WEB ENDPOINTS")
    print("=" * 65)
    for src_rel, dst_rel in MAPPINGS:
        src = ROOT / src_rel
        dst = ROOT / dst_rel
        if not src.exists():
            print(f"[!] Source missing: {src_rel}")
            continue

        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"[✓] Directory synced: /{dst_rel}/ ({len(list(dst.glob('*')))} items)")
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"[✓] File synced: /{dst_rel}")

    print("-" * 65)
    print("🎉 All canonical web endpoints are synced to root directories!")
    print("=" * 65)

if __name__ == "__main__":
    sync_endpoints()
