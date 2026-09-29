#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate professional PDF files for Gumroad products using Edge headless print-to-pdf.
"""

import os
import sys
import base64
import subprocess
from pathlib import Path
import markdown

ROOT_DIR = Path("d:/Project/work")
EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

def find_edge():
    for p in EDGE_PATHS:
        if os.path.exists(p):
            return p
    return None

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

@page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
    @bottom-center {
        content: counter(page);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 9pt;
        color: #888;
    }
}

body {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.7;
    color: #1e293b;
    background: #ffffff;
    font-size: 11pt;
    margin: 0;
    padding: 0;
}

.cover-page {
    page-break-after: always;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 90vh;
    text-align: center;
    padding: 20px;
}

.cover-image {
    max-width: 450px;
    max-height: 550px;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    margin-bottom: 30px;
}

.cover-title {
    font-size: 28pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 10px;
    line-height: 1.2;
}

.cover-subtitle {
    font-size: 14pt;
    color: #475569;
    margin-bottom: 30px;
    max-width: 600px;
}

.cover-badge {
    display: inline-block;
    background: #0ea5e9;
    color: white;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 10pt;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

h1 {
    font-size: 22pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 8px;
    margin-top: 36px;
    margin-bottom: 16px;
    page-break-before: always;
}

h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 15pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 24px;
    margin-bottom: 12px;
}

h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #334155;
    margin-top: 18px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 14px;
}

ul, ol {
    margin-bottom: 16px;
    padding-left: 24px;
}

li {
    margin-bottom: 6px;
}

code {
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 9.5pt;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    color: #0369a1;
}

pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 9pt;
    line-height: 1.5;
    margin: 16px 0;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    color: #e2e8f0;
    padding: 0;
}

blockquote {
    border-left: 4px solid #0ea5e9;
    background: #f8fafc;
    padding: 12px 18px;
    margin: 16px 0;
    border-radius: 0 8px 8px 0;
    color: #334155;
    font-style: italic;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    page-break-inside: avoid;
    font-size: 9.5pt;
}

th, td {
    border: 1px solid #cbd5e1;
    padding: 10px 12px;
    text-align: left;
}

th {
    background: #f1f5f9;
    font-weight: 700;
    color: #0f172a;
}

tr:nth-child(even) td {
    background: #f8fafc;
}

hr {
    border: 0;
    border-top: 1px solid #e2e8f0;
    margin: 30px 0;
}
"""

def md_to_pdf(md_file: Path, cover_img: Path, output_pdf: Path, title: str, subtitle: str):
    edge_exe = find_edge()
    if not edge_exe:
        print("[!] Microsoft Edge not found, skipping PDF generation.")
        return False
        
    print(f"Reading {md_file}...")
    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()
        
    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_text,
        extensions=['extra', 'tables', 'fenced_code', 'codehilite', 'toc']
    )
    
    # Read cover image as base64
    cover_html = ""
    if cover_img.exists():
        with open(cover_img, "rb") as img_f:
            b64 = base64.b64encode(img_f.read()).decode('utf-8')
            cover_html = f"""
            <div class="cover-page">
                <img class="cover-image" src="data:image/jpeg;base64,{b64}" alt="Cover" />
                <div class="cover-badge">Official Digital Edition</div>
                <h1 class="cover-title" style="page-break-before: avoid; border: none;">{title}</h1>
                <p class="cover-subtitle">{subtitle}</p>
            </div>
            """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
{CSS}
</style>
</head>
<body>
{cover_html}
<div class="content-container">
{html_body}
</div>
</body>
</html>
"""
    html_file = output_pdf.with_suffix(".html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    print(f"Saved intermediate HTML: {html_file}")
    
    # Call Edge headless to print to PDF
    cmd = [
        edge_exe,
        "--headless=new",
        "--disable-gpu",
        "--allow-file-access-from-files",
        f"--print-to-pdf={str(output_pdf)}",
        f"file:///{str(html_file).replace(os.sep, '/')}"
    ]
    
    print(f"Generating PDF with Edge: {output_pdf.name}...")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if output_pdf.exists() and output_pdf.stat().st_size > 1000:
        size_kb = output_pdf.stat().st_size / 1024
        print(f"SUCCESS: {output_pdf.name} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"Failed to generate PDF. Return code: {proc.returncode}")
        print("Stderr:", proc.stderr)
        return False

def main():
    # 1. eBook PDF
    ebook_md = ROOT_DIR / "projects/digital_products/products/ebook_ai_money_blueprint/FULL_EBOOK_COMPILED.md"
    ebook_cover = ROOT_DIR / "projects/digital_products/products/ebook_ai_money_blueprint/cover.jpg"
    ebook_pdf = ROOT_DIR / "projects/digital_products/products/ebook_ai_money_blueprint/The_AI_Money_Blueprint.pdf"
    
    md_to_pdf(
        ebook_md,
        ebook_cover,
        ebook_pdf,
        title="The AI Money Blueprint",
        subtitle="Uncovering Proven Strategies to Leverage AI for Financial Freedom, Freelancing & Automation"
    )
    
    # 2. Prompt Pack PDF
    prompt_md = ROOT_DIR / "projects/digital_products/products/prompt_pack_marketing/FULL_PROMPT_PACK_COMPILED.md"
    prompt_cover = ROOT_DIR / "projects/digital_products/products/prompt_pack_marketing/cover.jpg"
    prompt_pdf = ROOT_DIR / "projects/digital_products/products/prompt_pack_marketing/AI_Marketing_Prompt_Pack_110.pdf"
    
    md_to_pdf(
        prompt_md,
        prompt_cover,
        prompt_pdf,
        title="110+ AI Marketing Prompts Pack",
        subtitle="Ready-to-Use High-Converting Prompts for Strategy, Content, Copywriting, SEO, Ads & Social Media"
    )

if __name__ == "__main__":
    main()
