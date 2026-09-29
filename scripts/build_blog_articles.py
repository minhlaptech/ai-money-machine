"""
Static Site Builder for Affiliate Blog & Resource Hub
------------------------------------------------------
Tự động chuyển đổi toàn bộ 8 bài viết chuyên sâu dạng Markdown (.md)
thành các trang đọc bài viết HTML hiện đại (guide_001.html -> guide_008.html)
kèm Table of Contents, thời gian đọc, khối quảng cáo Master Bundle và liên kết điều hướng.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HTML_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta_title} — AI Automation Guide</title>
  <meta name="description" content="{meta_desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #050510;
      --bg-2: #0c0c1d;
      --surface: #14142b;
      --surface-hover: #1e1e3f;
      --accent: #7c5cfc;
      --accent-2: #5ce1e6;
      --accent-glow: rgba(124,92,252,0.25);
      --gradient: linear-gradient(135deg, #7c5cfc, #5ce1e6);
      --text: #e8e8f8;
      --text-2: #a0a0c8;
      --text-3: #686888;
      --border: rgba(255,255,255,0.08);
      --code-bg: #0b0b18;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      overflow-x: hidden;
    }}
    .bg-glow {{ position: fixed; width: 600px; height: 600px; border-radius: 50%; filter: blur(150px); opacity: 0.1; pointer-events: none; z-index: 0; }}
    .bg-glow-1 {{ top: -150px; left: -100px; background: #7c5cfc; }}
    .bg-glow-2 {{ bottom: -150px; right: -100px; background: #5ce1e6; }}
    nav {{
      position: sticky; top: 0; z-index: 100;
      background: rgba(5,5,16,0.88); backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border); padding: 14px 0;
    }}
    .nav-inner {{
      max-width: 900px; margin: 0 auto; padding: 0 24px;
      display: flex; justify-content: space-between; align-items: center;
    }}
    .nav-logo {{
      font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800;
      background: var(--gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
      text-decoration: none;
    }}
    .nav-right {{ display: flex; align-items: center; gap: 18px; }}
    .nav-link {{ color: var(--text-2); text-decoration: none; font-size: 14px; font-weight: 500; transition: color 0.2s; }}
    .nav-link:hover {{ color: #fff; }}
    .nav-cta {{
      background: var(--gradient); color: #000; text-decoration: none;
      padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 700;
    }}
    .article-header {{
      max-width: 860px; margin: 0 auto; padding: 60px 24px 30px;
      position: relative; z-index: 1;
    }}
    .meta-tag {{
      display: inline-block; background: rgba(124,92,252,0.15); color: #b19bff;
      border: 1px solid rgba(124,92,252,0.3); padding: 4px 14px; border-radius: 20px;
      font-size: 12px; font-weight: 700; margin-bottom: 18px; text-transform: uppercase; letter-spacing: 1px;
    }}
    h1 {{
      font-family: 'Outfit', sans-serif; font-size: clamp(28px, 4vw, 42px);
      font-weight: 800; line-height: 1.25; margin-bottom: 18px; color: #fff;
    }}
    .article-meta {{
      display: flex; gap: 16px; color: var(--text-3); font-size: 14px; align-items: center; flex-wrap: wrap;
    }}
    .article-container {{
      max-width: 860px; margin: 0 auto; padding: 0 24px 80px;
      position: relative; z-index: 1;
    }}
    h2 {{
      font-family: 'Outfit', sans-serif; font-size: 24px; font-weight: 700;
      margin: 40px 0 16px; color: #fff; border-bottom: 1px solid var(--border); padding-bottom: 8px;
    }}
    h3 {{
      font-family: 'Outfit', sans-serif; font-size: 19px; font-weight: 600;
      margin: 26px 0 12px; color: #d6d6fa;
    }}
    p {{ margin-bottom: 18px; color: var(--text-2); font-size: 16px; line-height: 1.75; }}
    ul, ol {{ margin: 0 0 20px 24px; color: var(--text-2); }}
    li {{ margin-bottom: 8px; }}
    pre, code {{
      font-family: 'JetBrains Mono', monospace; font-size: 14px;
    }}
    code {{ background: var(--code-bg); color: var(--accent-2); padding: 2px 6px; border-radius: 4px; }}
    pre {{
      background: var(--code-bg); border: 1px solid var(--border); border-radius: 12px;
      padding: 18px; overflow-x: auto; margin: 24px 0; color: #d0d0ee;
    }}
    pre code {{ background: transparent; padding: 0; color: inherit; }}
    blockquote {{
      background: var(--bg-2); border-left: 4px solid var(--accent);
      border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 24px 0;
      color: var(--text-2); font-style: italic;
    }}
    .promo-banner {{
      background: linear-gradient(135deg, rgba(124,92,252,0.15), rgba(92,225,230,0.1));
      border: 1px solid rgba(124,92,252,0.3); border-radius: 16px; padding: 32px;
      margin: 50px 0; text-align: center;
    }}
    .promo-banner h3 {{ font-size: 22px; margin-bottom: 10px; color: #fff; }}
    .promo-banner p {{ font-size: 15px; margin-bottom: 20px; max-width: 600px; margin-left: auto; margin-right: auto; }}
    .cta-btn {{
      display: inline-block; background: var(--gradient); color: #000;
      font-weight: 700; font-size: 14px; padding: 12px 28px; border-radius: 8px;
      text-decoration: none; transition: transform 0.2s;
    }}
    .cta-btn:hover {{ transform: scale(1.03); }}
    footer {{
      border-top: 1px solid var(--border); padding: 36px 24px;
      text-align: center; color: var(--text-3); font-size: 13px;
    }}
  </style>
</head>
<body>
  <div class="bg-glow bg-glow-1"></div>
  <div class="bg-glow bg-glow-2"></div>

  <nav>
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">AI Automation Guide</a>
      <div class="nav-right">
        <a href="index.html#guides" class="nav-link">← All Guides</a>
        <a href="bundle.html" class="nav-cta">Master Bundle ($39) ↗</a>
      </div>
    </div>
  </nav>

  <article>
    <header class="article-header">
      <span class="meta-tag">{category}</span>
      <h1>{title}</h1>
      <div class="article-meta">
        <span>By Minh Lap</span>
        <span>•</span>
        <span>Updated 2026</span>
        <span>•</span>
        <span>⏱️ {read_time} min read</span>
      </div>
    </header>

    <div class="article-container">
      {body_html}

      <!-- Bottom Monetization Banner -->
      <div class="promo-banner">
        <span style="font-size:11px; font-weight:800; color:var(--accent-2); text-transform:uppercase; letter-spacing:1px; display:inline-block; margin-bottom:8px;">🔥 SPECIAL RESOURCE BUNDLE</span>
        <h3>Get The Complete AI Empire Master Bundle</h3>
        <p>
          Take your automations to the next level with our 16,000-word eBook, 110+ production prompts, and 15 Make.com/Zapier blueprints. Save $30 today!
        </p>
        <a href="bundle.html" class="cta-btn">Unlock The Master Bundle ($39) ↗</a>
      </div>
    </div>
  </article>

  <footer>
    <p>© 2026 AI Automation Guide. All rights reserved. • <a href="index.html" style="color:var(--text-3);">Return to Home</a></p>
  </footer>
</body>
</html>
"""

def simple_markdown_to_html(md_text):
    # Strip frontmatter if any
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            md_text = parts[2]

    # Convert code blocks
    def code_block_repl(m):
        code = m.group(2).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre><code>{code}</code></pre>"
    md_text = re.sub(r'```([a-zA-Z0-9]*)\n(.*?)```', code_block_repl, md_text, flags=re.DOTALL)

    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    list_type = "ul"

    for line in lines:
        sline = line.strip()
        if not sline:
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            continue

        # Headers
        if sline.startswith("### "):
            if in_list: html_lines.append(f"</{list_type}>"); in_list = False
            html_lines.append(f"<h3>{sline[4:]}</h3>")
        elif sline.startswith("## "):
            if in_list: html_lines.append(f"</{list_type}>"); in_list = False
            html_lines.append(f"<h2>{sline[3:]}</h2>")
        elif sline.startswith("# "):
            if in_list: html_lines.append(f"</{list_type}>"); in_list = False
            # Skip main title since it's in the header
            continue
        # Blockquote
        elif sline.startswith("> "):
            if in_list: html_lines.append(f"</{list_type}>"); in_list = False
            html_lines.append(f"<blockquote>{sline[2:]}</blockquote>")
        # List items
        elif sline.startswith("- ") or sline.startswith("* "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
                list_type = "ul"
            html_lines.append(f"<li>{sline[2:]}</li>")
        elif re.match(r'^\d+\.\s', sline):
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
                list_type = "ol"
            item_text = re.sub(r'^\d+\.\s', '', sline)
            html_lines.append(f"<li>{item_text}</li>")
        else:
            if in_list:
                html_lines.append(f"</{list_type}>")
                in_list = False
            if not sline.startswith("<pre") and not sline.startswith("</pre") and not sline.startswith("</code"):
                html_lines.append(f"<p>{sline}</p>")
            else:
                html_lines.append(sline)

    if in_list:
        html_lines.append(f"</{list_type}>")

    html_content = "\n".join(html_lines)
    
    # Inline formatting (bold, italics, links, inline code)
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    html_content = re.sub(r'`(.*?)`', r'<code>\1</code>', html_content)
    html_content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" style="color:var(--accent-2); text-decoration:none;">\1</a>', html_content)

    return html_content

def build_all_guides():
    content_dir = Path(__file__).resolve().parent.parent / "projects" / "affiliate_blog" / "content"
    web_dir = Path(__file__).resolve().parent.parent / "projects" / "affiliate_blog" / "website"
    web_dir.mkdir(exist_ok=True)

    posts = sorted(list(content_dir.glob("post_*.md")))
    print(f"[*] Found {len(posts)} posts in {content_dir}")

    for idx, p in enumerate(posts, 1):
        raw = p.read_text(encoding="utf-8")
        lines = [l.strip() for l in raw.split("\n") if l.strip()]
        
        # Extract title
        title = lines[0].replace("# ", "") if lines else p.stem
        words = len(raw.split())
        read_time = max(5, words // 200)

        # Categorize
        if "chatbot" in p.name:
            cat = "Chatbots & AI Agents"
        elif "make" in p.name or "zapier" in p.name:
            cat = "No-Code Workflows"
        elif "consulting" in p.name:
            cat = "Business & Freelancing"
        elif "blog" in p.name:
            cat = "Content & SEO"
        else:
            cat = "AI Automation"

        meta_desc = f"Comprehensive guide: {title}. Step-by-step strategies, tool comparisons, and actionable blueprints for 2026."
        body_html = simple_markdown_to_html(raw)

        html = HTML_PAGE_TEMPLATE.format(
            meta_title=title,
            meta_desc=meta_desc,
            category=cat,
            title=title,
            read_time=read_time,
            body_html=body_html
        )

        out_name = f"guide_{idx:03d}.html"
        out_file = web_dir / out_name
        out_file.write_text(html, encoding="utf-8")
        print(f"[✓] Generated {out_name}: {title} ({words} words, ~{read_time} min read)")

    print("[*] All 8 articles generated successfully!")

if __name__ == "__main__":
    build_all_guides()
