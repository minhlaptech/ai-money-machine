"""
Global Canonical URL Synchronizer
---------------------------------
Quét và chuẩn hóa toàn bộ các liên kết trong dự án về tên miền canonical:
- `chatbotdemo-hazel.vercel.app` -> `https://work-minh-lap.vercel.app/chatbotdemo`
- `reviewgenius-beta.vercel.app` -> `https://work-minh-lap.vercel.app/reviewgenius`
Bảo đảm 100% link chào hàng, proposal, YouTube description, và blog card hoạt động vĩnh viễn không bao giờ lỗi 404.
"""

import os
import sys
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent

OLD_NEW_PAIRS = [
    ("https://synapse-geo-audit.vercel.app", "https://work-minh-lap.vercel.app/synapsegeo"),
    ("http://synapse-geo-audit.vercel.app", "https://work-minh-lap.vercel.app/synapsegeo"),
    ("synapse-geo-audit.vercel.app", "work-minh-lap.vercel.app/synapsegeo"),
    ("https://chatbotdemo-hazel.vercel.app", "https://work-minh-lap.vercel.app/chatbotdemo"),
    ("http://chatbotdemo-hazel.vercel.app", "https://work-minh-lap.vercel.app/chatbotdemo"),
    ("chatbotdemo-hazel.vercel.app", "work-minh-lap.vercel.app/chatbotdemo"),
    ("https://reviewgenius-beta.vercel.app", "https://work-minh-lap.vercel.app/reviewgenius"),
    ("http://reviewgenius-beta.vercel.app", "https://work-minh-lap.vercel.app/reviewgenius"),
    ("reviewgenius-beta.vercel.app", "work-minh-lap.vercel.app/reviewgenius"),
]

EXCLUDE_DIRS = {".git", ".vercel", "__pycache__", "node_modules"}
INCLUDE_EXTS = {".html", ".md", ".json", ".js", ".py", ".csv"}

def sync_urls():
    modified_files = []
    
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        
        for fname in filenames:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in INCLUDE_EXTS:
                continue
                
            fpath = Path(dirpath) / fname
            
            # Skip this script itself
            if fpath.name == "unify_canonical_urls.py":
                continue
                
            try:
                content = fpath.read_text(encoding="utf-8")
            except Exception:
                continue
                
            changed = False
            for old_url, new_url in OLD_NEW_PAIRS:
                if old_url in content:
                    content = content.replace(old_url, new_url)
                    changed = True
                    
            if changed:
                fpath.write_text(content, encoding="utf-8")
                modified_files.append(fpath.relative_to(ROOT_DIR))

    print("=" * 70)
    print("🚀 CANONICAL URL SYNCHRONIZATION COMPLETE")
    print("=" * 70)
    print(f"Updated {len(modified_files)} files to canonical domain work-minh-lap.vercel.app:")
    for f in modified_files[:20]:
        print(f"  [✓] {f}")
    if len(modified_files) > 20:
        print(f"  ... and {len(modified_files) - 20} more files.")
    print("=" * 70)

if __name__ == "__main__":
    sync_urls()
