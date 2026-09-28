"""
Autonomous Market Scout & Trend Harvester (Multi-Source)
--------------------------------------------------------
Tự động quét các nguồn công nghệ & khởi nghiệp quốc tế:
1. Hacker News (Ask HN, Show HN, Top Stories)
2. GitHub Trending AI & Micro-SaaS tools
3. Dev.to Tech & SaaS Articles
Phát hiện lỗ hổng thị trường, nhu cầu phần mềm và xu hướng đang bùng nổ.
"""

import json
import urllib.request
import urllib.error
import re
import sys
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

HIGH_INTENT_KEYWORDS = [
    "willing to pay", "need a tool", "looking for", "alternative to",
    "automate", "pain point", "micro saas", "extension", "mrr",
    "seo", "lead", "scraping", "ai agent", "workflow", "monetize"
]

def fetch_hn_stories(endpoint="askstories", limit=15):
    items = []
    try:
        url = f"https://hacker-news.firebaseio.com/v0/{endpoint}.json"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            ids = json.loads(resp.read().decode('utf-8'))[:limit]
            for sid in ids:
                try:
                    item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    ireq = urllib.request.Request(item_url, headers={"User-Agent": USER_AGENT})
                    with urllib.request.urlopen(ireq, timeout=4) as iresp:
                        d = json.loads(iresp.read().decode('utf-8'))
                        if d and d.get("title"):
                            items.append({
                                "source": f"Hacker News ({endpoint.replace('stories','')})",
                                "title": d.get("title", ""),
                                "text": d.get("text", "")[:400] if d.get("text") else "",
                                "score": d.get("score", 0),
                                "comments": len(d.get("kids", [])),
                                "url": f"https://news.ycombinator.com/item?id={sid}"
                            })
                except Exception:
                    continue
    except Exception as e:
        print(f"[!] HN fetch failed: {e}")
    return items

def fetch_github_trending(query="ai-agent+OR+micro-saas", limit=15):
    items = []
    try:
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read().decode('utf-8'))
            for repo in d.get("items", []):
                items.append({
                    "source": "GitHub Trending",
                    "title": f"{repo.get('full_name')} - {repo.get('description') or ''}",
                    "text": repo.get("description", "") or "",
                    "score": repo.get("stargazers_count", 0),
                    "comments": repo.get("forks_count", 0),
                    "url": repo.get("html_url")
                })
    except Exception as e:
        print(f"[!] GitHub fetch failed: {e}")
    return items

def fetch_devto(tag="saas", limit=10):
    items = []
    try:
        url = f"https://dev.to/api/articles?tag={tag}&per_page={limit}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=10) as resp:
            articles = json.loads(resp.read().decode('utf-8'))
            for a in articles:
                items.append({
                    "source": f"Dev.to (#{tag})",
                    "title": a.get("title", ""),
                    "text": a.get("description", "") or "",
                    "score": a.get("positive_reactions_count", 0),
                    "comments": a.get("comments_count", 0),
                    "url": a.get("url")
                })
    except Exception as e:
        print(f"[!] Dev.to fetch failed: {e}")
    return items

def score_item(item):
    text = (item["title"] + " " + item["text"]).lower()
    score = 0
    matched = []
    for kw in HIGH_INTENT_KEYWORDS:
        if kw in text:
            score += 25
            matched.append(kw)
    if item["comments"] > 10:
        score += 15
    if item["score"] > 20:
        score += 10
    item["intent_score"] = score
    item["matched_keywords"] = matched
    return item

def run_scout():
    print("[*] Đang khởi động AI Market Scout...")
    all_data = []

    print(" -> Đang thu thập từ Hacker News (Ask HN & Show HN)...")
    all_data.extend(fetch_hn_stories("askstories", limit=10))
    all_data.extend(fetch_hn_stories("showstories", limit=10))

    print(" -> Đang thu thập từ GitHub Trending Tech & Tools...")
    all_data.extend(fetch_github_trending("micro-saas+OR+seo-tool", limit=10))

    print(" -> Đang thu thập từ Dev.to SaaS...")
    all_data.extend(fetch_devto("saas", limit=10))

    scored = [score_item(it) for it in all_data]
    scored.sort(key=lambda x: x["intent_score"], reverse=True)

    # Save JSON
    result = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_analyzed": len(scored),
        "high_priority_opportunities": [x for x in scored if x["intent_score"] >= 25]
    }

    with open("market_opportunities.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Save Markdown
    md = f"# 🌐 Báo Cáo Phân Tích Cơ Hội Thị Trường Quốc Tế (AI Scout)\n\n"
    md += f"- **Thời gian quét**: {result['updated_at']}\n"
    md += f"- **Số lượng mục phân tích**: {result['total_analyzed']}\n"
    md += f"- **Số cơ hội nhu cầu cao (High Intent)**: {len(result['high_priority_opportunities'])}\n\n"
    md += "## 🎯 Top Cơ Hội & Vấn Đề Nóng Được Phát Hiện:\n\n"

    for i, it in enumerate(result['high_priority_opportunities'][:12], 1):
        md += f"### {i}. [{it['title']}]({it['url']})\n"
        md += f"- **Nguồn**: `{it['source']}` | **Điểm tiềm năng**: `{it['intent_score']}`\n"
        md += f"- **Từ khóa nhu cầu bắt gặp**: `{', '.join(it['matched_keywords'])}`\n"
        if it['text']:
            md += f"- **Tóm tắt mô tả**: {it['text'][:200]}...\n\n"

    with open("market_scout_report.md", "w", encoding="utf-8") as f:
        f.write(md)

    print(f"[✓] Quét hoàn tất! Đã lưu {len(result['high_priority_opportunities'])} cơ hội tiềm năng vào 'market_scout_report.md'.")

if __name__ == "__main__":
    run_scout()
