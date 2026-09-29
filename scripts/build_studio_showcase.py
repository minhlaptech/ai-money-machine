#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — Studio Showcase Hub Builder
------------------------------------------------
Generates projects/youtube_faceless/studio.html and studio/index.html with:
- 10 Full YouTube Episodes (4K Thumbnails, Video Previews, Audio Players, SRTs, Teleprompter Scripts)
- 30-Day Viral Shorts Sprint (Video Previews, Audio Players, Hooks, CTAs, Weekly Filter)
- Integrated HTML5 Broadcast Video Modal Player (Instant preview across all 40 rendered MP4s)
- 10 Multi-Platform Social Repurposing Kits (1-Click Copy for LinkedIn, X, TikTok, Reddit)
"""

import sys
import os
import re
import json
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
STUDIO_HTML = ROOT / "projects" / "youtube_faceless" / "studio.html"
STUDIO_ROOT = ROOT / "studio" / "index.html"
SCRIPTS_DIR = ROOT / "projects" / "youtube_faceless" / "scripts"
AUDIO_EP_DIR = ROOT / "projects" / "youtube_faceless" / "audio_episodes"
AUDIO_SHORTS_DIR = ROOT / "projects" / "youtube_faceless" / "audio_shorts"
THUMBS_DIR = ROOT / "projects" / "youtube_faceless" / "thumbnails"
SPRINT_FILE = ROOT / "projects" / "youtube_faceless" / "shorts_sprint" / "30_DAYS_SHORTS_SPRINT.md"
SOCIAL_HUB = ROOT / "projects" / "ai_content_social" / "social_content_hub.json"

EPISODES = [
    {"num": 1, "title": "5 AI Tools That Can Make You $1000/Month", "dur": "9.9 min", "words": 1206, "thumb": "thumb_001_5_ai_tools.jpg", "slug": "video_001_5_ai_tools_1000_month"},
    {"num": 2, "title": "How to Build an AI Chatbot in 15 Minutes", "dur": "6.2 min", "words": 861, "thumb": "thumb_002_chatbot_15min.jpg", "slug": "video_002_ai_chatbot_15_minutes"},
    {"num": 3, "title": "How to Automate a Local Business for $500", "dur": "9.1 min", "words": 1176, "thumb": "thumb_003_automate_500.jpg", "slug": "video_003_automate_business_500"},
    {"num": 4, "title": "I Built 3 AI Products in 1 Day", "dur": "8.7 min", "words": 1159, "thumb": "thumb_004_3_products_1_day.jpg", "slug": "video_004_3_products_1_day"},
    {"num": 5, "title": "How to Build & Monetize a Micro-SaaS with AI", "dur": "6.0 min", "words": 736, "thumb": "thumb_005_microsaas.jpg", "slug": "video_005_build_microsaas_ai"},
    {"num": 6, "title": "Starting an AI Automation Agency in 2026", "dur": "7.6 min", "words": 962, "thumb": "thumb_006_ai_agency.jpg", "slug": "video_006_ai_automation_agency"},
    {"num": 7, "title": "AI + Print on Demand: The Automated Merch Store", "dur": "6.4 min", "words": 790, "thumb": "thumb_007_pod_ai.jpg", "slug": "video_007_print_on_demand_ai"},
    {"num": 8, "title": "The $0 to $3,000/Month AI Freelancing Roadmap", "dur": "8.2 min", "words": 963, "thumb": "thumb_008_upwork_ai.jpg", "slug": "video_008_ai_freelancing_roadmap"},
    {"num": 9, "title": "How to Build an AI Agency in 48 Hours", "dur": "7.9 min", "words": 976, "thumb": "thumb_009_agency_48h.jpg", "slug": "video_009_build_ai_agency_48h"},
    {"num": 10, "title": "5 Make.com Automation Blueprints That Make $1000/Month", "dur": "7.6 min", "words": 886, "thumb": "thumb_010_blueprints.jpg", "slug": "video_010_make_automation_blueprints"},
]

def load_shorts():
    if not SPRINT_FILE.exists():
        return []
    content = SPRINT_FILE.read_text(encoding="utf-8")
    pattern = r"### 🎬 Ngày #(\d+) \| (.*?)\n(.*?)(?=\n### 🎬 Ngày #|\n## 🛠️|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    shorts = []
    for num_str, title, body in matches:
        day_num = int(num_str)
        hook_m = re.search(r"Hook.*?:\s*(?:\[.*?\]\s*)?[\*\"']*(.*?)[\*\"']*\n", body)
        hook = hook_m.group(1).strip().strip('"').strip("'").strip("*") if hook_m else ""
        content_m = re.search(r"Nội dung chính.*?:[\s\n]*>[\s\n]*[\"']*(.*?)[\"']*\n", body)
        main_text = content_m.group(1).strip().strip('"').strip("'") if content_m else ""
        cta_m = re.search(r"Kêu gọi hành động.*?:[\s\n]*>[\s\n]*[\"']*(.*?)[\"']*\n", body)
        cta = cta_m.group(1).strip().strip('"').strip("'") if cta_m else ""
        week = (day_num - 1) // 7 + 1
        shorts.append({
            "day": day_num,
            "week": week,
            "title": title.strip(),
            "hook": hook,
            "content": main_text,
            "cta": cta
        })
    return shorts

def load_social_kits():
    if not SOCIAL_HUB.exists():
        return []
    try:
        return json.loads(SOCIAL_HUB.read_text(encoding="utf-8"))
    except Exception:
        return []

def build_html():
    shorts = load_shorts()
    social_kits = load_social_kits()

    episodes_cards_html = ""
    for ep in EPISODES:
        mp3_rel = f"/studio/audio_episodes/episode_{ep['num']:03d}_voiceover.mp3"
        srt_rel = f"/studio/audio_episodes/episode_{ep['num']:03d}_subtitles.srt"
        txt_rel = f"/studio/audio_episodes/episode_{ep['num']:03d}_script.txt"
        thumb_rel = f"/studio/thumbnails/{ep['thumb']}"
        video_rel = f"/studio/rendered_episodes/episode_{ep['num']:03d}_video.mp4"

        episodes_cards_html += f"""
        <div class="ep-card">
          <div class="ep-thumb-wrap" onclick="openStudioVideo('{ep['title']}', '{video_rel}', '1080p 16:9 Broadcast Episode')">
            <img src="{thumb_rel}" alt="{ep['title']}" class="ep-thumb" loading="lazy">
            <span class="ep-badge">EPISODE #{ep['num']:02d}</span>
            <span class="ep-dur-badge">⏱️ {ep['dur']}</span>
            <div class="ep-play-overlay">
              <div class="play-btn-circle">▶</div>
              <span>Watch Video Preview</span>
            </div>
          </div>
          <div class="ep-body">
            <h3 class="ep-title">{ep['title']}</h3>
            <div class="ep-meta">
              <span>🗣️ Studio AI Narration</span>
              <span>•</span>
              <span>📝 {ep['words']:,} words</span>
              <span>•</span>
              <span>⚡ 1080p Broadcast</span>
            </div>
            
            <div class="audio-player-box">
              <audio controls preload="none" class="custom-audio">
                <source src="{mp3_rel}" type="audio/mpeg">
                Your browser does not support the audio element.
              </audio>
            </div>

            <div class="ep-actions">
              <button class="btn-action btn-watch-act" onclick="openStudioVideo('{ep['title']}', '{video_rel}', '1080p 16:9 Broadcast Episode')">▶ Watch</button>
              <a href="{video_rel}" download class="btn-action">📥 Video</a>
              <a href="{mp3_rel}" download class="btn-action">🎧 Audio</a>
              <a href="{srt_rel}" target="_blank" class="btn-action">📄 SRT</a>
            </div>
          </div>
        </div>
        """

    shorts_cards_html = ""
    for sh in shorts:
        day_str = f"{sh['day']:02d}"
        mp3_rel = f"/studio/audio_shorts/day_{day_str}_voiceover.mp3"
        srt_rel = f"/studio/audio_shorts/day_{day_str}_subtitles.srt"
        txt_rel = f"/studio/audio_shorts/day_{day_str}_script.txt"
        video_rel = f"/studio/rendered_shorts/day_{day_str}_short.mp4"

        shorts_cards_html += f"""
        <div class="short-card" data-week="{sh['week']}">
          <div class="short-header">
            <div class="short-badge">DAY #{day_str} • WEEK {sh['week']}</div>
            <span class="short-pill">9:16 Vertical</span>
          </div>
          <h4 class="short-title">{sh['title']}</h4>
          
          <div class="short-hook-box">
            <div class="box-label">🎯 HOOK:</div>
            <p>"{sh['hook']}"</p>
          </div>

          <div class="short-content-box">
            <div class="box-label">💡 VALUE & SCRIPT:</div>
            <p>{sh['content'][:140]}...</p>
          </div>

          <div class="short-cta-box">
            <div class="box-label">🚀 CALL TO ACTION:</div>
            <p>"{sh['cta']}"</p>
          </div>

          <div class="audio-player-box">
            <audio controls preload="none" class="custom-audio">
              <source src="{mp3_rel}" type="audio/mpeg">
            </audio>
          </div>

          <div class="short-footer">
            <button class="btn-mini btn-watch-act" onclick="openStudioVideo('{sh['title']}', '{video_rel}', '9:16 Vertical Reel (1080x1920)')">▶ Watch</button>
            <a href="{video_rel}" download class="btn-mini">📥 MP4</a>
            <a href="{mp3_rel}" download class="btn-mini">🎧 Audio</a>
            <a href="{srt_rel}" target="_blank" class="btn-mini">📄 SRT</a>
          </div>
        </div>
        """

    social_kits_json_escaped = json.dumps(social_kits, ensure_ascii=False).replace("</script>", "<\\/script>")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Media & Video Studio Hub | Autonomous Content Machine</title>
  <meta name="description" content="Production hub for 10 Full YouTube Faceless Episodes, 30-Day Viral Shorts Sprint, and Multi-Platform Social Repurposing Kits.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #070913;
      --bg-card: rgba(13, 17, 34, 0.75);
      --bg-card-hover: rgba(22, 28, 54, 0.85);
      --border: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(0, 242, 254, 0.3);
      --cyan: #00f2fe;
      --accent: #7c5cfc;
      --accent-glow: rgba(124, 92, 252, 0.35);
      --emerald: #00e676;
      --amber: #ffb74d;
      --rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'Inter', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
      line-height: 1.6;
    }}

    /* Glow backdrop background */
    .bg-mesh {{
      position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: 
        radial-gradient(circle at 15% 15%, rgba(124, 92, 252, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 25%, rgba(0, 242, 254, 0.10) 0%, transparent 35%),
        radial-gradient(circle at 50% 85%, rgba(0, 230, 118, 0.06) 0%, transparent 40%);
      pointer-events: none; z-index: 0;
    }}

    /* Header */
    header {{
      position: sticky; top: 0; z-index: 100;
      background: rgba(7, 9, 19, 0.88); backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--border); padding: 14px 28px;
      display: flex; justify-content: space-between; align-items: center;
    }}
    .brand-wrap {{ display: flex; align-items: center; gap: 14px; text-decoration: none; color: inherit; }}
    .logo-badge {{
      width: 40px; height: 40px; border-radius: 12px;
      background: linear-gradient(135deg, var(--rose), var(--accent));
      display: flex; align-items: center; justify-content: center;
      font-size: 20px; box-shadow: 0 0 25px rgba(244, 63, 94, 0.4);
    }}
    .brand-text h1 {{
      font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800;
      letter-spacing: -0.5px;
    }}
    .brand-text span {{ font-size: 11px; color: var(--text-muted); font-family: var(--font-mono); }}

    .nav-actions {{ display: flex; align-items: center; gap: 12px; }}
    .btn-nav {{
      text-decoration: none; padding: 7px 16px; border-radius: 10px;
      font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px;
      transition: all 0.2s;
    }}
    .btn-nav-primary {{
      background: linear-gradient(135deg, var(--accent), var(--cyan));
      color: #000; font-weight: 700;
    }}
    .btn-nav-secondary {{
      background: rgba(255, 255, 255, 0.06); border: 1px solid var(--border);
      color: var(--text);
    }}
    .btn-nav:hover {{ transform: translateY(-1px); opacity: 0.95; }}

    /* Container */
    .container {{
      max-width: 1340px; margin: 0 auto; padding: 32px 24px 80px;
      position: relative; z-index: 1;
    }}

    /* Hero Banner */
    .studio-hero {{
      text-align: center; margin-bottom: 40px; padding: 32px 20px;
      background: linear-gradient(180deg, rgba(124, 92, 252, 0.08) 0%, transparent 100%);
      border-radius: 24px; border: 1px solid var(--border);
    }}
    .hero-badge {{
      display: inline-flex; align-items: center; gap: 8px;
      background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.35);
      color: #fb7185; padding: 5px 14px; border-radius: 30px; font-size: 12px; font-weight: 700;
      margin-bottom: 16px; letter-spacing: 0.5px; text-transform: uppercase;
    }}
    .studio-hero h2 {{
      font-family: 'Outfit', sans-serif; font-size: 38px; font-weight: 900;
      letter-spacing: -1px; margin-bottom: 12px;
      background: linear-gradient(135deg, #fff 40%, var(--cyan) 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}
    .studio-hero p {{
      max-width: 720px; margin: 0 auto 24px; color: var(--text-muted); font-size: 16px;
    }}

    /* Stat Counters */
    .stat-row {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px; margin-bottom: 36px;
    }}
    .stat-box {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 16px; padding: 18px 22px; text-align: center;
      backdrop-filter: blur(12px);
    }}
    .stat-num {{
      font-family: 'Outfit', sans-serif; font-size: 32px; font-weight: 800; color: #fff;
    }}
    .stat-lbl {{ font-size: 12px; text-transform: uppercase; color: var(--text-muted); font-weight: 600; letter-spacing: 0.8px; margin-top: 4px; }}

    /* Main Navigation Tabs */
    .studio-tabs {{
      display: flex; gap: 12px; border-bottom: 1px solid var(--border);
      padding-bottom: 14px; margin-bottom: 32px; overflow-x: auto;
    }}
    .studio-tab-btn {{
      background: rgba(255, 255, 255, 0.04); border: 1px solid var(--border);
      color: var(--text-muted); padding: 10px 22px; border-radius: 12px;
      font-size: 14px; font-weight: 600; cursor: pointer; white-space: nowrap;
      transition: all 0.25s; display: flex; align-items: center; gap: 8px;
    }}
    .studio-tab-btn.active {{
      background: linear-gradient(135deg, rgba(124, 92, 252, 0.25), rgba(0, 242, 254, 0.2));
      border-color: var(--cyan); color: #fff; box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    }}
    .studio-tab-btn:hover:not(.active) {{
      background: rgba(255, 255, 255, 0.08); color: var(--text);
    }}

    /* Panels */
    .studio-panel {{ display: none; }}
    .studio-panel.active {{ display: block; animation: fadeIn 0.3s ease; }}
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    /* Episodes Grid */
    .episodes-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap: 26px;
    }}
    .ep-card {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 20px; overflow: hidden; display: flex; flex-direction: column;
      backdrop-filter: blur(12px); transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .ep-card:hover {{
      border-color: var(--cyan); transform: translateY(-4px);
      box-shadow: 0 12px 35px rgba(0, 242, 254, 0.15);
    }}
    .ep-thumb-wrap {{
      position: relative; aspect-ratio: 16 / 9; overflow: hidden; background: #000;
      cursor: pointer;
    }}
    .ep-thumb {{
      width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease;
    }}
    .ep-card:hover .ep-thumb {{ transform: scale(1.04); }}
    .ep-badge {{
      position: absolute; top: 12px; left: 12px;
      background: rgba(0, 0, 0, 0.75); border: 1px solid rgba(255,255,255,0.2);
      backdrop-filter: blur(8px); padding: 4px 10px; border-radius: 8px;
      font-size: 11px; font-weight: 700; color: #fff; font-family: var(--font-mono);
      z-index: 2;
    }}
    .ep-dur-badge {{
      position: absolute; bottom: 12px; right: 12px;
      background: rgba(0, 0, 0, 0.85); border: 1px solid rgba(0, 242, 254, 0.4);
      padding: 4px 10px; border-radius: 8px; font-size: 11px; font-weight: 700; color: var(--cyan);
      z-index: 2;
    }}

    .ep-play-overlay {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.55); backdrop-filter: blur(3px);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 8px; opacity: 0; transition: opacity 0.25s ease; z-index: 3;
    }}
    .ep-thumb-wrap:hover .ep-play-overlay {{ opacity: 1; }}
    .play-btn-circle {{
      width: 48px; height: 48px; border-radius: 50%;
      background: linear-gradient(135deg, var(--rose), var(--accent));
      display: flex; align-items: center; justify-content: center;
      color: #fff; font-size: 18px; box-shadow: 0 0 25px rgba(244, 63, 94, 0.6);
      transform: scale(0.9); transition: transform 0.2s;
    }}
    .ep-thumb-wrap:hover .play-btn-circle {{ transform: scale(1.05); }}
    .ep-play-overlay span {{ font-size: 12px; font-weight: 700; color: #fff; letter-spacing: 0.5px; text-transform: uppercase; }}

    .ep-body {{ padding: 22px; display: flex; flex-direction: column; flex: 1; justify-content: space-between; }}
    .ep-title {{
      font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 700;
      line-height: 1.35; margin-bottom: 8px; color: #fff;
    }}
    .ep-meta {{
      font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 8px;
      margin-bottom: 16px;
    }}
    .audio-player-box {{
      background: rgba(0, 0, 0, 0.35); border: 1px solid var(--border);
      border-radius: 12px; padding: 10px 14px; margin-bottom: 16px;
    }}
    audio.custom-audio {{
      width: 100%; height: 36px; outline: none;
    }}

    .ep-actions {{
      display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 6px;
    }}
    .btn-action {{
      text-align: center; text-decoration: none; padding: 8px 6px;
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      border-radius: 8px; font-size: 11px; font-weight: 600; color: var(--text);
      transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center;
    }}
    .btn-action:hover {{
      background: linear-gradient(135deg, var(--accent), var(--cyan));
      border-color: transparent; color: #000;
    }}
    .btn-watch-act {{
      background: linear-gradient(135deg, var(--rose), var(--accent)) !important;
      color: #fff !important; font-weight: 700 !important; border-color: transparent !important;
      cursor: pointer;
    }}
    .btn-watch-act:hover {{
      box-shadow: 0 0 15px rgba(244, 63, 94, 0.5); transform: translateY(-1px);
    }}

    /* Shorts Filter & Grid */
    .filter-bar {{
      display: flex; gap: 8px; margin-bottom: 24px; align-items: center;
      background: var(--bg-card); padding: 10px 16px; border-radius: 14px; border: 1px solid var(--border);
      overflow-x: auto;
    }}
    .filter-btn {{
      background: transparent; border: none; color: var(--text-muted);
      padding: 6px 14px; border-radius: 8px; font-size: 13px; font-weight: 600;
      cursor: pointer; transition: all 0.2s; white-space: nowrap;
    }}
    .filter-btn.active {{
      background: var(--accent); color: #fff;
    }}

    .shorts-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
    }}
    .short-card {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 18px; padding: 20px; display: flex; flex-direction: column;
      justify-content: space-between; backdrop-filter: blur(12px);
      transition: all 0.25s ease;
    }}
    .short-card:hover {{
      border-color: var(--cyan); transform: translateY(-3px);
    }}
    .short-header {{
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
    }}
    .short-badge {{
      font-size: 11px; font-weight: 700; color: var(--cyan); font-family: var(--font-mono);
      background: rgba(0, 242, 254, 0.1); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(0, 242, 254, 0.25);
    }}
    .short-pill {{
      font-size: 10px; color: var(--text-muted); text-transform: uppercase; font-weight: 600;
    }}
    .short-title {{
      font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; margin-bottom: 14px;
    }}
    .box-label {{ font-size: 10px; font-weight: 700; color: var(--text-muted); letter-spacing: 0.5px; margin-bottom: 4px; }}
    .short-hook-box, .short-content-box, .short-cta-box {{
      background: rgba(0, 0, 0, 0.25); border: 1px solid var(--border);
      border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; font-size: 12px;
    }}
    .short-hook-box p {{ color: #ffe600; font-weight: 600; }}
    .short-cta-box p {{ color: var(--emerald); font-weight: 600; }}

    .short-footer {{
      display: grid; grid-template-columns: 1.2fr 1fr 1fr 1fr; gap: 6px; margin-top: 12px;
    }}
    .btn-mini {{
      text-align: center; text-decoration: none; padding: 7px 6px;
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      border-radius: 6px; font-size: 11px; font-weight: 600; color: var(--text);
      transition: all 0.2s; display: inline-flex; align-items: center; justify-content: center;
    }}
    .btn-mini:hover {{
      background: var(--cyan); color: #000; border-color: transparent;
    }}

    /* Social Repurposing UI */
    .social-kit-box {{
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 20px; padding: 28px; backdrop-filter: blur(14px);
    }}
    .topic-selector-wrap {{
      display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 24px;
    }}
    .topic-pill {{
      background: rgba(255, 255, 255, 0.05); border: 1px solid var(--border);
      color: var(--text-muted); padding: 8px 16px; border-radius: 30px;
      font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .topic-pill.active {{
      background: linear-gradient(135deg, var(--accent), var(--cyan));
      color: #000; border-color: transparent; font-weight: 700;
    }}
    .social-quad-grid {{
      display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 20px;
    }}
    .quad-card {{
      background: rgba(0, 0, 0, 0.35); border: 1px solid var(--border);
      border-radius: 14px; padding: 20px; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .quad-header {{
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;
    }}
    .quad-header h4 {{ font-family: 'Outfit', sans-serif; font-size: 16px; font-weight: 700; display: flex; align-items: center; gap: 8px; }}
    .btn-copy {{
      background: rgba(255, 255, 255, 0.08); border: 1px solid var(--border);
      color: var(--text); padding: 5px 12px; border-radius: 6px; font-size: 11px;
      font-weight: 600; cursor: pointer; transition: all 0.2s;
    }}
    .btn-copy:hover {{ background: var(--emerald); color: #000; }}
    .quad-content {{
      background: rgba(7, 9, 19, 0.6); border: 1px solid var(--border);
      border-radius: 10px; padding: 14px; font-size: 13px; line-height: 1.5;
      max-height: 320px; overflow-y: auto; white-space: pre-wrap; font-family: 'Inter', sans-serif;
    }}

    /* Video Player Modal */
    .video-modal-backdrop {{
      display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
      background: rgba(0, 0, 0, 0.90); backdrop-filter: blur(14px);
      z-index: 1000; align-items: center; justify-content: center; padding: 20px;
    }}
    .video-modal-backdrop.open {{ display: flex; animation: fadeIn 0.25s ease; }}
    .video-modal-box {{
      background: #0d1124; border: 1px solid var(--border-accent);
      border-radius: 24px; padding: 24px; max-width: 900px; width: 100%;
      position: relative; box-shadow: 0 25px 60px rgba(0,0,0,0.85);
      display: flex; flex-direction: column; gap: 16px;
    }}
    .video-modal-header {{
      display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;
    }}
    .video-format-pill {{
      font-size: 11px; font-weight: 700; color: var(--cyan); font-family: var(--font-mono);
      background: rgba(0, 242, 254, 0.12); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(0, 242, 254, 0.3);
      display: inline-block; margin-bottom: 6px; text-transform: uppercase;
    }}
    .video-modal-title {{ font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 800; color: #fff; line-height: 1.3; }}
    .video-modal-close {{
      background: rgba(255,255,255,0.08); border: 1px solid var(--border); color: #fff;
      width: 36px; height: 36px; border-radius: 50%; font-size: 18px; cursor: pointer;
      display: flex; align-items: center; justify-content: center; transition: all 0.2s; flex-shrink: 0;
    }}
    .video-modal-close:hover {{ background: var(--rose); border-color: transparent; }}

    .video-screen-container {{
      background: #000; border-radius: 16px; overflow: hidden;
      aspect-ratio: 16 / 9; display: flex; align-items: center; justify-content: center;
      position: relative; border: 1px solid var(--border);
    }}
    .video-screen-container.vertical {{ aspect-ratio: 9 / 16; max-height: 60vh; margin: 0 auto; }}
    .video-screen-player {{ width: 100%; height: 100%; outline: none; }}

    .video-modal-footer {{
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;
      padding-top: 10px; border-top: 1px solid var(--border);
    }}
    .video-engine-status {{
      font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 8px;
    }}
    .status-bulb {{
      width: 8px; height: 8px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 10px var(--emerald);
    }}
    .btn-download-mp4 {{
      background: linear-gradient(135deg, var(--accent), var(--cyan)); color: #000;
      text-decoration: none; padding: 9px 18px; border-radius: 10px; font-size: 13px; font-weight: 700;
      display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;
    }}
    .btn-download-mp4:hover {{ opacity: 0.95; transform: translateY(-1px); }}

    @media (max-width: 768px) {{
      .studio-hero h2 {{ font-size: 28px; }}
      .episodes-grid, .social-quad-grid {{ grid-template-columns: 1fr; }}
      .ep-actions, .short-footer {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="bg-mesh"></div>

  <header>
    <a href="/" class="brand-wrap">
      <div class="logo-badge">🎬</div>
      <div class="brand-text">
        <h1>AI MEDIA STUDIO</h1>
        <span>AUTONOMOUS BROADCAST CENTER</span>
      </div>
    </a>
    <div class="nav-actions">
      <a href="/" class="btn-nav btn-nav-secondary">← Command Center</a>
      <a href="/tools" class="btn-nav btn-nav-secondary">SaaS Suite ↗</a>
      <a href="/portal" class="btn-nav btn-nav-secondary">VIP Portals ↗</a>
      <a href="/bundle" class="btn-nav btn-nav-primary">Master Bundle ($39) ↗</a>
    </div>
  </header>

  <div class="container">
    <div class="studio-hero">
      <span class="hero-badge">⚡ 100% Autonomous Studio Engine</span>
      <h2>Broadcast-Quality Media & Content Empire</h2>
      <p>40 rendered broadcast MP4 videos, instant browser video previews, full audio narrations, subtitle downloads, and 1-click social distribution packages across all 8 monetization streams.</p>
      
      <div class="stat-row">
        <div class="stat-box">
          <div class="stat-num">40 / 40</div>
          <div class="stat-lbl">Rendered MP4 Videos</div>
        </div>
        <div class="stat-box">
          <div class="stat-num">77.6 mins</div>
          <div class="stat-lbl">Full Episodes Audio</div>
        </div>
        <div class="stat-box">
          <div class="stat-num">10 / 10</div>
          <div class="stat-lbl">4K Photorealistic Thumbnails</div>
        </div>
        <div class="stat-box">
          <div class="stat-num">30 Days</div>
          <div class="stat-lbl">Viral Shorts Synthesized</div>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="studio-tabs">
      <button class="studio-tab-btn active" onclick="switchStudioTab('tab-episodes', this)">
        <span>🎬</span> 10 Full YouTube Episodes
      </button>
      <button class="studio-tab-btn" onclick="switchStudioTab('tab-shorts', this)">
        <span>📱</span> 30-Day Viral Shorts Sprint
      </button>
      <button class="studio-tab-btn" onclick="switchStudioTab('tab-social', this)">
        <span>🔄</span> Social Media Repurposing (10 Kits)
      </button>
    </div>

    <!-- Panel 1: Full Episodes -->
    <div id="tab-episodes" class="studio-panel active">
      <div class="episodes-grid">
        {episodes_cards_html}
      </div>
    </div>

    <!-- Panel 2: 30-Day Shorts Sprint -->
    <div id="tab-shorts" class="studio-panel">
      <div class="filter-bar">
        <span style="font-size:12px; font-weight:700; color:var(--text-muted); margin-right:8px;">FILTER WEEK:</span>
        <button class="filter-btn active" onclick="filterShorts('all', this)">All (30 Days)</button>
        <button class="filter-btn" onclick="filterShorts('1', this)">Week 1 (Day 1-7)</button>
        <button class="filter-btn" onclick="filterShorts('2', this)">Week 2 (Day 8-14)</button>
        <button class="filter-btn" onclick="filterShorts('3', this)">Week 3 (Day 15-21)</button>
        <button class="filter-btn" onclick="filterShorts('4', this)">Week 4 (Day 22-30)</button>
      </div>
      <div class="shorts-grid">
        {shorts_cards_html}
      </div>
    </div>

    <!-- Panel 3: Social Repurposing Kits -->
    <div id="tab-social" class="studio-panel">
      <div class="social-kit-box">
        <h3 style="font-family:'Outfit', sans-serif; font-size:20px; font-weight:800; margin-bottom:8px;">10 Multi-Platform Distribution Kits</h3>
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:20px;">Select a core topic below to copy pre-formatted content packages for LinkedIn, X (Twitter Threads), TikTok scripts, and Reddit communities.</p>

        <div class="topic-selector-wrap" id="topicPillsWrap"></div>

        <div class="social-quad-grid">
          <div class="quad-card">
            <div class="quad-header">
              <h4>💼 LinkedIn Authority Post</h4>
              <button class="btn-copy" onclick="copyQuad('liContent', this)">Copy Post</button>
            </div>
            <div class="quad-content" id="liContent">Loading...</div>
          </div>

          <div class="quad-card">
            <div class="quad-header">
              <h4>🐦 X / Twitter Thread (3-5 Tweets)</h4>
              <button class="btn-copy" onclick="copyQuad('twContent', this)">Copy Thread</button>
            </div>
            <div class="quad-content" id="twContent">Loading...</div>
          </div>

          <div class="quad-card">
            <div class="quad-header">
              <h4>📱 TikTok / Shorts Video Script</h4>
              <button class="btn-copy" onclick="copyQuad('ttContent', this)">Copy Script</button>
            </div>
            <div class="quad-content" id="ttContent">Loading...</div>
          </div>

          <div class="quad-card">
            <div class="quad-header">
              <h4>👽 Reddit Discussion Starter</h4>
              <button class="btn-copy" onclick="copyQuad('rdContent', this)">Copy Discussion</button>
            </div>
            <div class="quad-content" id="rdContent">Loading...</div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <!-- Video Player Preview Modal -->
  <div class="video-modal-backdrop" id="studioVideoModal" onclick="closeVideoModalOnBackdrop(event)">
    <div class="video-modal-box">
      <div class="video-modal-header">
        <div>
          <span class="video-format-pill" id="studioModalFormat">1080p 16:9 Broadcast Episode</span>
          <h3 class="video-modal-title" id="studioModalTitle">Episode Video Preview</h3>
        </div>
        <button class="video-modal-close" onclick="closeStudioVideo()">✕</button>
      </div>

      <div class="video-screen-container" id="videoScreenContainer">
        <video id="studioVideoPlayer" controls playsinline preload="metadata" class="video-screen-player">
          <source id="studioVideoPlayerSrc" src="" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>

      <div class="video-modal-footer">
        <div class="video-engine-status">
          <span class="status-bulb"></span>
          <span>100% Autonomous Render Engine • Ready to Broadcast</span>
        </div>
        <div style="display:flex; gap:10px;">
          <a id="studioModalDownloadBtn" href="" download class="btn-download-mp4">📥 Download Full MP4</a>
          <button onclick="closeStudioVideo()" class="btn-action" style="padding:9px 16px; cursor:pointer;">Close</button>
        </div>
      </div>
    </div>
  </div>

  <footer style="text-align:center; padding:40px 24px; color:var(--text-muted); font-size:13px; border-top:1px solid var(--border);">
    <p>AI Media & Video Studio Hub — Faceless Production Machine. © 2026 AI Money Machine.</p>
    <p style="margin-top:8px;">
      <a href="/" style="color:var(--cyan); text-decoration:none;">Command Center</a> • 
      <a href="/tools" style="color:var(--cyan); text-decoration:none;">Micro-SaaS Suite</a> • 
      <a href="/bundle" style="color:var(--cyan); text-decoration:none;">Master Bundle ($39)</a> • 
      <a href="/portal" style="color:var(--cyan); text-decoration:none;">VIP Portals Hub</a> • 
      <a href="/referral" style="color:var(--cyan); text-decoration:none;">Affiliate Program</a>
    </p>
  </footer>

  <script>
    const SOCIAL_KITS = {social_kits_json_escaped};

    function switchStudioTab(tabId, btn) {{
      document.querySelectorAll('.studio-tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.studio-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
    }}

    function filterShorts(week, btn) {{
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const cards = document.querySelectorAll('.short-card');
      cards.forEach(card => {{
        if (week === 'all' || card.dataset.week === week) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    function initSocialPills() {{
      const wrap = document.getElementById('topicPillsWrap');
      if (!wrap || !SOCIAL_KITS.length) return;
      wrap.innerHTML = '';
      SOCIAL_KITS.forEach((k, idx) => {{
        const pill = document.createElement('button');
        pill.className = 'topic-pill' + (idx === 0 ? ' active' : '');
        pill.textContent = k.topic.replace(/_/g, ' ').toUpperCase();
        pill.onclick = () => selectTopic(idx, pill);
        wrap.appendChild(pill);
      }});
      renderTopicContent(0);
    }}

    function selectTopic(idx, pill) {{
      document.querySelectorAll('.topic-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      renderTopicContent(idx);
    }}

    function renderTopicContent(idx) {{
      const kit = SOCIAL_KITS[idx];
      if (!kit) return;
      document.getElementById('liContent').textContent = kit.linkedin || 'No LinkedIn post available.';
      document.getElementById('twContent').textContent = (kit.tweets || []).join('\\n\\n---\\n\\n') || 'No tweets available.';
      document.getElementById('ttContent').textContent = kit.tiktok || 'No TikTok script available.';
      document.getElementById('rdContent').textContent = kit.reddit || 'No Reddit starter available.';
    }}

    function copyQuad(elementId, btn) {{
      const text = document.getElementById(elementId).textContent;
      navigator.clipboard.writeText(text).then(() => {{
        const oldText = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.style.background = 'var(--emerald)';
        btn.style.color = '#000';
        setTimeout(() => {{
          btn.textContent = oldText;
          btn.style.background = '';
          btn.style.color = '';
        }}, 2000);
      }});
    }}

    /* Video Player Modal Logic */
    function openStudioVideo(title, src, format) {{
      const modal = document.getElementById('studioVideoModal');
      const player = document.getElementById('studioVideoPlayer');
      const playerSrc = document.getElementById('studioVideoPlayerSrc');
      const modalTitle = document.getElementById('studioModalTitle');
      const modalFormat = document.getElementById('studioModalFormat');
      const downloadBtn = document.getElementById('studioModalDownloadBtn');
      const container = document.getElementById('videoScreenContainer');

      modalTitle.textContent = title;
      modalFormat.textContent = format;
      downloadBtn.href = src;
      playerSrc.src = src;

      if (format.includes('Vertical') || format.includes('9:16')) {{
        container.classList.add('vertical');
      }} else {{
        container.classList.remove('vertical');
      }}

      player.load();
      modal.classList.add('open');
      player.play().catch(e => console.log('Autoplay deferred:', e));
    }}

    function closeStudioVideo() {{
      const modal = document.getElementById('studioVideoModal');
      const player = document.getElementById('studioVideoPlayer');
      if (player) {{
        player.pause();
        player.currentTime = 0;
      }}
      if (modal) modal.classList.remove('open');
    }}

    function closeVideoModalOnBackdrop(e) {{
      if (e.target.id === 'studioVideoModal') closeStudioVideo();
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeStudioVideo();
    }});

    document.addEventListener('DOMContentLoaded', () => {{
      initSocialPills();
    }});
  </script>
</body>
</html>
"""

    STUDIO_HTML.parent.mkdir(parents=True, exist_ok=True)
    STUDIO_HTML.write_text(html_content, encoding="utf-8")
    print(f"[✓] Generated Studio Showcase: {STUDIO_HTML} ({len(html_content):,} bytes)")

    STUDIO_ROOT.parent.mkdir(parents=True, exist_ok=True)
    STUDIO_ROOT.write_text(html_content, encoding="utf-8")
    print(f"[✓] Generated Studio Root: {STUDIO_ROOT} ({len(html_content):,} bytes)")

if __name__ == "__main__":
    build_html()
