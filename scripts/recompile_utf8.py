#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recompile markdown source files with strict UTF-8 encoding and regenerate PDFs.
"""

import os
import subprocess
from pathlib import Path

ROOT = Path("d:/Project/work")

def recompile_ebook():
    ebook_dir = ROOT / "projects/digital_products/products/ebook_ai_money_blueprint"
    ordered_files = [
        "EBOOK_OUTLINE.md",
        "chapter_01_ai_freelancer.md",
        "chapter_02_automation_consulting.md",
        "chapter_03_digital_products.md",
        "chapter_04_youtube.md",
        "chapter_05_micro_saas.md",
        "chapters_06_07_affiliate_pod.md",
        "chapters_08_09_10_bonus.md",
    ]
    
    combined = []
    for fname in ordered_files:
        fpath = ebook_dir / fname
        if fpath.exists():
            print(f"Adding eBook file: {fname}")
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                combined.append(content)
                
    output_path = ebook_dir / "FULL_EBOOK_COMPILED.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(combined))
    print(f"Recompiled eBook written to: {output_path} ({len(combined)} sections)")

def recompile_prompt_pack():
    pack_dir = ROOT / "projects/digital_products/products/prompt_pack_marketing"
    ordered_files = [
        "AI_Marketing_Prompt_Pack.md",
        "section_02_email_marketing.md",
        "section_03_seo_blog.md",
        "section_04_05_ads_sales.md",
        "section_06_07_brand_analytics.md",
    ]
    
    combined = []
    for fname in ordered_files:
        fpath = pack_dir / fname
        if fpath.exists():
            print(f"Adding Prompt Pack file: {fname}")
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                combined.append(content)
                
    output_path = pack_dir / "FULL_PROMPT_PACK_COMPILED.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n\n---\n\n".join(combined))
    print(f"Recompiled Prompt Pack written to: {output_path} ({len(combined)} sections)")

if __name__ == "__main__":
    recompile_ebook()
    recompile_prompt_pack()
