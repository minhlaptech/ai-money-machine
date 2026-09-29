#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — Autonomous Video Assembler & Render Engine
--------------------------------------------------------------
Renders production-ready MP4 videos locally using FFmpeg:
1. 30-Day Viral Shorts (9:16 vertical 1080x1920) for YouTube Shorts, TikTok & Reels
   - Sleek dark tech canvas + neon gradient glow
   - Real-time reactive audio visualizer waveform (showwaves)
   - Dynamic Hormozi-style high-contrast burned-in subtitles (.srt)
   - Episode header badge & channel branding

2. 10 Full-Length Faceless YouTube Episodes (16:9 widescreen 1920x1080)
   - High-CTR 4K thumbnail backdrop with ambient visualizer
   - Synchronized lower-third subtitle captions (.srt)
   - Broadcast-quality audio-visual synchronization

Zero external paid APIs required. Powered by static-ffmpeg and Python.
"""

import sys
import os
import re
import argparse
import subprocess
import shutil
import json
from pathlib import Path
from datetime import datetime

try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SHORTS_AUDIO_DIR = ROOT / "projects" / "youtube_faceless" / "audio_shorts"
EPISODES_AUDIO_DIR = ROOT / "projects" / "youtube_faceless" / "audio_episodes"
THUMBNAILS_DIR = ROOT / "projects" / "youtube_faceless" / "thumbnails"
RENDERED_SHORTS_DIR = ROOT / "projects" / "youtube_faceless" / "rendered_shorts"
RENDERED_EPISODES_DIR = ROOT / "projects" / "youtube_faceless" / "rendered_episodes"
SPRINT_FILE = ROOT / "projects" / "youtube_faceless" / "shorts_sprint" / "30_DAYS_SHORTS_SPRINT.md"
SCRIPTS_DIR = ROOT / "projects" / "youtube_faceless" / "scripts"

def get_short_title(day_num):
    """Extract title from 30_DAYS_SHORTS_SPRINT.md"""
    if not SPRINT_FILE.exists():
        return f"Day {day_num}"
    content = SPRINT_FILE.read_text(encoding="utf-8")
    m = re.search(rf"### 🎬 Ngày #{day_num:02d} \| (.*?)\n", content)
    if not m:
        m = re.search(rf"### 🎬 Ngày #{day_num} \| (.*?)\n", content)
    return m.group(1).strip() if m else f"Day {day_num}"

def render_short_video(day_num, force=False):
    """Render 1080x1920 vertical video for Day X Short"""
    RENDERED_SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    mp3_file = SHORTS_AUDIO_DIR / f"day_{day_num:02d}_voiceover.mp3"
    srt_file = SHORTS_AUDIO_DIR / f"day_{day_num:02d}_subtitles.srt"
    out_mp4 = RENDERED_SHORTS_DIR / f"day_{day_num:02d}_short.mp4"

    if not mp3_file.exists() or not srt_file.exists():
        print(f"[!] Day #{day_num:02d} audio or srt file missing.")
        return None

    if not force and out_mp4.exists() and out_mp4.stat().st_size > 500000:
        print(f"[✓] Day #{day_num:02d} Short already rendered ({out_mp4.stat().st_size // 1024} KB). Skipping.")
        return {
            "type": "short",
            "day": day_num,
            "title": get_short_title(day_num),
            "mp4": str(out_mp4),
            "size_kb": out_mp4.stat().st_size // 1024
        }

    title = get_short_title(day_num)
    print(f"[*] Rendering Day #{day_num:02d} Short: '{title[:35]}...'")

    # Copy SRT locally to work around Windows drive colon escaping issues in FFmpeg
    temp_srt = ROOT / f"temp_short_{day_num:02d}.srt"
    shutil.copy2(srt_file, temp_srt)

    # Sanitize subtitle style:
    # Yellow primary text (&H0000FFFF), black outline, Arial bold, 22pt font size, centered
    sub_filter = (
        f"subtitles={temp_srt.name}:force_style="
        "'Fontname=Arial,Bold=1,FontSize=20,PrimaryColour=&H0000FFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=3,Alignment=10,MarginV=120'"
    )

    filter_complex = (
        "[1:a]showwaves=s=880x260:mode=line:colors=#00f2fe@0.85:scale=sqrt[wave];"
        "[0:v][wave]overlay=(W-w)/2:(H-h)/2+260[bg_wave];"
        f"[bg_wave]{sub_filter}[v]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "color=c=#080d1a:s=1080x1920:r=30",
        "-i", str(mp3_file),
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_mp4)
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        if temp_srt.exists():
            temp_srt.unlink()

        if out_mp4.exists() and out_mp4.stat().st_size > 100000:
            sz = out_mp4.stat().st_size // 1024
            print(f"[✓] Rendered Day #{day_num:02d} Short! Size: {sz} KB | File: {out_mp4.name}")
            return {
                "type": "short",
                "day": day_num,
                "title": title,
                "mp4": str(out_mp4),
                "size_kb": sz
            }
        else:
            print(f"[!] FFmpeg error on Day #{day_num:02d}: {res.stderr[-400:]}")
            return None
    except Exception as e:
        if temp_srt.exists():
            temp_srt.unlink()
        print(f"[!] Render exception on Day #{day_num:02d}: {e}")
        return None

def find_thumbnail_for_episode(ep_num):
    """Find matching thumbnail for episode"""
    patterns = [
        f"thumb_{ep_num:03d}_*.jpg",
        f"thumb_{ep_num:03d}_*.png"
    ]
    for p in patterns:
        matches = list(THUMBNAILS_DIR.glob(p))
        if matches:
            return matches[0]
    return None

def render_episode_video(ep_num, force=False):
    """Render 1920x1080 widescreen video for YouTube Episode X"""
    RENDERED_EPISODES_DIR.mkdir(parents=True, exist_ok=True)
    mp3_file = EPISODES_AUDIO_DIR / f"episode_{ep_num:03d}_voiceover.mp3"
    srt_file = EPISODES_AUDIO_DIR / f"episode_{ep_num:03d}_subtitles.srt"
    thumb_file = find_thumbnail_for_episode(ep_num)
    out_mp4 = RENDERED_EPISODES_DIR / f"episode_{ep_num:03d}_video.mp4"

    if not mp3_file.exists() or not srt_file.exists():
        print(f"[!] Episode #{ep_num:03d} audio or srt file missing.")
        return None

    if not force and out_mp4.exists() and out_mp4.stat().st_size > 1000000:
        print(f"[✓] Episode #{ep_num:03d} already rendered ({out_mp4.stat().st_size // 1024} KB). Skipping.")
        return {
            "type": "episode",
            "episode": ep_num,
            "mp4": str(out_mp4),
            "size_kb": out_mp4.stat().st_size // 1024
        }

    print(f"[*] Rendering Full Episode #{ep_num:03d} (1920x1080 widescreen)...")

    temp_srt = ROOT / f"temp_ep_{ep_num:03d}.srt"
    shutil.copy2(srt_file, temp_srt)

    # Subtitle filter: White text with gold border, bottom-centered, 18pt
    sub_filter = (
        f"subtitles={temp_srt.name}:force_style="
        "'Fontname=Arial,Bold=1,FontSize=18,PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,BorderStyle=1,Outline=2.5,Alignment=2,MarginV=45'"
    )

    if thumb_file and thumb_file.exists():
        # Input 0: Image loop, Input 1: MP3 Audio
        filter_complex = (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2[scaled];"
            "[1:a]showwaves=s=1200x120:mode=line:colors=#00f2fe@0.75:scale=sqrt[wave];"
            "[scaled][wave]overlay=(W-w)/2:H-160[bg_wave];"
            f"[bg_wave]{sub_filter}[v]"
        )
        input_args = ["-loop", "1", "-i", str(thumb_file), "-i", str(mp3_file)]
    else:
        # Fallback dark background
        filter_complex = (
            "[1:a]showwaves=s=1200x140:mode=line:colors=#00f2fe@0.8:scale=sqrt[wave];"
            "[0:v][wave]overlay=(W-w)/2:H-180[bg_wave];"
            f"[bg_wave]{sub_filter}[v]"
        )
        input_args = ["-f", "lavfi", "-i", "color=c=#0a0f1d:s=1920x1080:r=30", "-i", str(mp3_file)]

    cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(out_mp4)
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        if temp_srt.exists():
            temp_srt.unlink()

        if out_mp4.exists() and out_mp4.stat().st_size > 500000:
            sz = out_mp4.stat().st_size // 1024
            print(f"[✓] Rendered Episode #{ep_num:03d}! Size: {sz} KB ({sz/1024:.1f} MB) | File: {out_mp4.name}")
            return {
                "type": "episode",
                "episode": ep_num,
                "mp4": str(out_mp4),
                "size_kb": sz
            }
        else:
            print(f"[!] FFmpeg error on Episode #{ep_num:03d}: {res.stderr[-400:]}")
            return None
    except Exception as e:
        if temp_srt.exists():
            temp_srt.unlink()
        print(f"[!] Render exception on Episode #{ep_num:03d}: {e}")
        return None

def send_telegram_render_alert(results):
    """Dispatch video rendering digest to Telegram @Minhpv_bot"""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    total_mb = sum(r["size_kb"] for r in results) / 1024
    vtype = results[0]["type"].capitalize() if results else "Video"

    lines = [
        f"🎬 <b>[AUTONOMOUS VIDEO RENDERING COMPLETE!]</b>",
        f"",
        f"📦 <b>Số lượng xuất bản:</b> <code>{len(results)} {vtype} MP4 Videos</code>",
        f"💾 <b>Tổng dung lượng:</b> <b>{total_mb:.1f} MB</b>",
        f"⚡ <b>Engine:</b> FFmpeg Broadcast H.264 / AAC + Auto Subtitles",
        f"",
        f"<b>Danh mục video vừa xuất xưởng:</b>"
    ]
    for r in results[:8]:
        tag = f"Day #{r['day']:02d}" if "day" in r else f"Ep #{r['episode']:03d}"
        name = Path(r["mp4"]).name
        lines.append(f"• <b>{tag}</b>: <code>{name}</code> ({r['size_kb']//1024:.1f} MB)")
    if len(results) > 8:
        lines.append(f"• <i>...và {len(results)-8} video khác.</i>")

    lines.append(f"\n📂 <b>Vị trí lưu trữ:</b>\n<code>projects/youtube_faceless/rendered_{results[0]['type']}s/</code>")
    lines.append("\n👉 <i>Tất cả video MP4 đã sẵn sàng upload trực tiếp lên YouTube / TikTok / Reels!</i>")

    html_msg = "\n".join(lines)
    # Direct reliable send via curl.exe
    try:
        payload_file = ROOT / "temp_tg_render.json"
        payload_file.write_text(json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}, ensure_ascii=False), encoding="utf-8")
        res = subprocess.run(
            ["curl.exe", "-s", "-X", "POST",
             "-H", "Content-Type: application/json; charset=utf-8",
             "-d", f"@{payload_file.name}",
             f"https://api.telegram.org/bot{bot_token}/sendMessage"],
            capture_output=True, text=True, timeout=10, cwd=str(ROOT)
        )
        if payload_file.exists():
            payload_file.unlink()
        if '"ok":true' in res.stdout:
            print("[✓] Đã gửi báo cáo xuất bản Video MP4 về Telegram (@Minhpv_bot)!")
        else:
            print(f"[!] Telegram alert error: {res.stdout}")
    except Exception as e:
        print(f"[!] Telegram notification error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Video Assembler & Render Engine")
    parser.add_argument("--type", choices=["shorts", "episode"], default="shorts", help="Video type")
    parser.add_argument("--day", type=int, help="Single Day number (1-30)")
    parser.add_argument("--episode", type=int, help="Single Episode number (1-10)")
    parser.add_argument("--all", action="store_true", help="Batch render all videos in category")
    parser.add_argument("--force", action="store_true", help="Force re-render existing videos")
    parser.add_argument("--telegram", action="store_true", help="Send completion digest to Telegram")
    args = parser.parse_args()

    results = []
    print("=" * 70)
    print("🎬 AI MONEY MACHINE — AUTONOMOUS VIDEO ASSEMBLER ENGINE")
    print("=" * 70)

    if args.type == "shorts":
        if args.all:
            print("[*] Batch rendering all 30 days of Viral Shorts (1080x1920)...")
            for d in range(1, 31):
                res = render_short_video(d, force=args.force)
                if res:
                    results.append(res)
        elif args.day:
            res = render_short_video(args.day, force=args.force)
            if res:
                results.append(res)
        else:
            print("[*] Rendering sample Day 01 Short video...")
            res = render_short_video(1, force=args.force)
            if res:
                results.append(res)

    elif args.type == "episode":
        if args.all:
            print("[*] Batch rendering all 10 Full YouTube Episodes (1920x1080)...")
            for ep in range(1, 11):
                res = render_episode_video(ep, force=args.force)
                if res:
                    results.append(res)
        elif args.episode:
            res = render_episode_video(args.episode, force=args.force)
            if res:
                results.append(res)
        else:
            print("[*] Rendering Episode #001 Full Video...")
            res = render_episode_video(1, force=args.force)
            if res:
                results.append(res)

    print("-" * 70)
    print(f"🎉 RENDER COMPLETE: Successfully generated {len(results)} MP4 videos!")
    print("=" * 70)

    if args.telegram and results:
        send_telegram_render_alert(results)

if __name__ == "__main__":
    main()
