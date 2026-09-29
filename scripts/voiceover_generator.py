#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — Autonomous Voiceover & Subtitle Generator
--------------------------------------------------------------
Generates studio-quality AI voiceover (.mp3) and synchronized (.srt)
captions for both:
1. The 30-Day Viral Shorts, TikTok & Reels Content Sprint
2. The 10 Full-Length Faceless YouTube Channel Episodes

Powered by gTTS & pydub. Zero external paid API required.
"""

import sys
import os
import re
import argparse
import urllib.request
import json
from pathlib import Path
from datetime import datetime
from gtts import gTTS

try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

from pydub import AudioSegment

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
SHORTS_DIR = ROOT / "projects" / "youtube_faceless" / "audio_shorts"
EPISODES_DIR = ROOT / "projects" / "youtube_faceless" / "audio_episodes"
SPRINT_FILE = ROOT / "projects" / "youtube_faceless" / "shorts_sprint" / "30_DAYS_SHORTS_SPRINT.md"
SCRIPTS_DIR = ROOT / "projects" / "youtube_faceless" / "scripts"

def format_srt_time(ms):
    """Format milliseconds into SRT timestamp format: HH:MM:SS,mmm"""
    total_seconds = int(ms // 1000)
    millis = int(ms % 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

def generate_subtitles(text, duration_seconds):
    """Split text into 3-6 word bite-sized caption cues and assign proportional timestamps"""
    # Split into sentences or clauses first
    raw_sentences = re.split(r'([.?!,;—]+)', text)
    chunks = []
    current_chunk = ""
    for piece in raw_sentences:
        if not piece:
            continue
        if re.match(r'^[.?!,;—]+$', piece):
            if current_chunk:
                chunks.append((current_chunk + piece).strip())
                current_chunk = ""
        else:
            words = piece.strip().split()
            # If piece is long, break it into 4-6 word segments
            while len(words) > 6:
                sub = " ".join(words[:5])
                chunks.append(sub)
                words = words[5:]
            if words:
                current_chunk = " ".join(words)
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Filter empty chunks
    cues = [c for c in chunks if len(c.strip()) > 0]
    if not cues:
        cues = [text]

    total_chars = sum(len(c) for c in cues)
    if total_chars == 0:
        total_chars = 1

    srt_lines = []
    current_ms = 0
    total_ms = duration_seconds * 1000

    for idx, cue in enumerate(cues, start=1):
        ratio = len(cue) / total_chars
        cue_duration = max(800, ratio * total_ms)
        end_ms = min(total_ms, current_ms + cue_duration)
        if idx == len(cues):
            end_ms = total_ms

        start_str = format_srt_time(current_ms)
        end_str = format_srt_time(end_ms)

        srt_lines.append(f"{idx}\n{start_str} --> {end_str}\n{cue}\n")
        current_ms = end_ms

    return "\n".join(srt_lines)

def clean_speech_text(text):
    """Normalize text for crisp, natural TTS pronunciation"""
    t = text.strip()
    # Currency symbols: $1,500 -> 1,500 dollars
    t = re.sub(r'\$(\d+(?:,\d+)?(?:\.\d+)?)', r'\1 dollars', t)
    # /month -> per month, /mo -> per month
    t = re.sub(r'/month\b', ' per month', t, flags=re.IGNORECASE)
    t = re.sub(r'/mo\b', ' per month', t, flags=re.IGNORECASE)
    # 24/7 -> twenty-four seven
    t = re.sub(r'\b24/7\b', 'twenty-four seven', t)
    # Emojis and visual bracket notes [like this]
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'[\U00010000-\U0010ffff]', '', t)
    # Hashtags
    t = re.sub(r'#\w+', '', t)
    # Excess whitespace
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def parse_shorts_sprint():
    """Extract all 30 days from 30_DAYS_SHORTS_SPRINT.md"""
    if not SPRINT_FILE.exists():
        return {}
    content = SPRINT_FILE.read_text(encoding="utf-8")
    pattern = r"### 🎬 Ngày #(\d+) \| (.*?)\n(.*?)(?=\n### 🎬 Ngày #|\n## 🛠️|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)
    data = {}
    for num_str, title, body in matches:
        day_num = int(num_str)
        hook_m = re.search(r"Hook.*?:\s*(?:\[.*?\]\s*)?[\*\"']*(.*?)[\*\"']*\n", body)
        hook = hook_m.group(1).strip().strip('"').strip("'").strip("*") if hook_m else ""
        content_m = re.search(r"Nội dung chính.*?:[\s\n]*>[\s\n]*[\"']*(.*?)[\"']*\n", body)
        main_text = content_m.group(1).strip().strip('"').strip("'") if content_m else ""
        cta_m = re.search(r"Kêu gọi hành động.*?:[\s\n]*>[\s\n]*[\"']*(.*?)[\"']*\n", body)
        cta = cta_m.group(1).strip().strip('"').strip("'") if cta_m else ""
        data[day_num] = {
            "title": title.strip(),
            "hook": hook,
            "content": main_text,
            "cta": cta,
            "raw": f"{hook} {main_text} {cta}".strip()
        }
    return data

def generate_short_voiceover(day_num, tld="com"):
    """Generate audio MP3, SRT subtitles, and teleprompter TXT for Day X short"""
    SHORTS_DIR.mkdir(parents=True, exist_ok=True)
    all_days = parse_shorts_sprint()
    if day_num not in all_days:
        print(f"[!] Day #{day_num} not found in sprint file.")
        return None

    item = all_days[day_num]
    speech = clean_speech_text(item["raw"])
    if not speech:
        print(f"[!] Day #{day_num} has empty speech content.")
        return None

    mp3_path = SHORTS_DIR / f"day_{day_num:02d}_voiceover.mp3"
    srt_path = SHORTS_DIR / f"day_{day_num:02d}_subtitles.srt"
    txt_path = SHORTS_DIR / f"day_{day_num:02d}_script.txt"

    print(f"[*] Synthesizing voiceover for Day #{day_num:02d} ({tld.upper()} accent)...")
    tts = gTTS(text=speech, lang='en', tld=tld)
    tts.save(str(mp3_path))

    # Read duration via pydub
    audio = AudioSegment.from_file(str(mp3_path))
    duration = audio.duration_seconds

    # Generate subtitles
    srt_content = generate_subtitles(speech, duration)
    srt_path.write_text(srt_content, encoding="utf-8")

    # Generate teleprompter text
    txt_content = f"DAY #{day_num:02d}: {item['title']}\nDuration: {duration:.1f}s\n\nHOOK:\n{item['hook']}\n\nCONTENT:\n{item['content']}\n\nCTA:\n{item['cta']}\n\nCLEAN SPEECH:\n{speech}\n"
    txt_path.write_text(txt_content, encoding="utf-8")

    print(f"[✓] Day #{day_num:02d} Complete! Audio: {duration:.1f}s ({mp3_path.stat().st_size // 1024} KB) | Subtitles: {len(srt_content.splitlines())//4} cues")
    return {
        "type": "short",
        "day": day_num,
        "title": item["title"],
        "duration": duration,
        "mp3": str(mp3_path),
        "srt": str(srt_path),
        "words": len(speech.split())
    }

def get_episode_files():
    """List all available episode script markdown files"""
    return sorted(list(SCRIPTS_DIR.glob("video_*.md")))

def generate_episode_voiceover(episode_num, tld="com"):
    """Generate audio MP3, SRT subtitles, and teleprompter TXT for YouTube Episode X"""
    EPISODES_DIR.mkdir(parents=True, exist_ok=True)
    files = get_episode_files()
    target_file = None
    for f in files:
        if f.name.startswith(f"video_{episode_num:03d}"):
            target_file = f
            break

    if not target_file or not target_file.exists():
        print(f"[!] Episode #{episode_num} script file not found.")
        return None

    content = target_file.read_text(encoding="utf-8")
    script_part = content.split("## 📝 FULL SCRIPT")[-1] if "## 📝 FULL SCRIPT" in content else content
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", script_part, re.DOTALL)
    spoken_raw = " ".join([b.strip() for b in code_blocks if not b.strip().startswith("http")])
    if not spoken_raw:
        spoken_raw = script_part

    speech = clean_speech_text(spoken_raw)
    words = speech.split()

    mp3_path = EPISODES_DIR / f"episode_{episode_num:03d}_voiceover.mp3"
    srt_path = EPISODES_DIR / f"episode_{episode_num:03d}_subtitles.srt"
    txt_path = EPISODES_DIR / f"episode_{episode_num:03d}_script.txt"

    print(f"[*] Synthesizing full episode voiceover #{episode_num:03d} ({len(words)} words, ~{len(words)/140:.1f} mins)...")
    tts = gTTS(text=speech, lang='en', tld=tld)
    tts.save(str(mp3_path))

    audio = AudioSegment.from_file(str(mp3_path))
    duration = audio.duration_seconds

    srt_content = generate_subtitles(speech, duration)
    srt_path.write_text(srt_content, encoding="utf-8")

    title_m = re.search(r"##\s*[\"']?(.*?)[\"']?\n", content)
    ep_title = title_m.group(1).strip() if title_m else target_file.stem

    txt_content = f"EPISODE #{episode_num:03d}: {ep_title}\nTotal Words: {len(words)} | Duration: {duration/60:.1f} minutes\n\nSPEECH NARRATION:\n{speech}\n"
    txt_path.write_text(txt_content, encoding="utf-8")

    print(f"[✓] Episode #{episode_num:03d} Complete! Audio: {duration/60:.1f} mins ({mp3_path.stat().st_size // 1024} KB) | Subtitles: {len(srt_content.splitlines())//4} cues")
    return {
        "type": "episode",
        "episode": episode_num,
        "title": ep_title,
        "duration": duration,
        "mp3": str(mp3_path),
        "srt": str(srt_path),
        "words": len(words)
    }

def send_telegram_alert(results):
    """Dispatch generation summary to Telegram @Minhpv_bot"""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "1624883046")

    total_duration = sum(r["duration"] for r in results)
    total_words = sum(r["words"] for r in results)
    item_type = results[0]["type"].capitalize() if results else "Media"

    items_list = ""
    for r in results[:8]:
        tag = f"Day #{r['day']:02d}" if "day" in r else f"Ep #{r['episode']:03d}"
        items_list += f"• <b>{tag}</b>: <i>{r['title'][:32]}...</i> ({r['duration']:.1f}s, {r['words']} w)\n"
    if len(results) > 8:
        items_list += f"• <i>...và {len(results)-8} tệp âm thanh khác.</i>\n"

    html_msg = f"""🎙️ <b>[VOICEOVER & SUBTITLE PRODUCTION COMPLETE!]</b>

📦 <b>Danh mục:</b> <code>{len(results)} {item_type} Voiceovers & SRTs</code>
⏱️ <b>Tổng thời lượng audio:</b> <b>{total_duration/60:.1f} phút</b> ({total_words:,} từ)
🗣️ <b>Công nghệ:</b> Studio TTS Engine (En-US High-Fidelity)

📋 <b>Danh sách sản phẩm vừa sinh:</b>
{items_list}
📂 <b>Vị trí lưu trữ:</b>
<code>projects/youtube_faceless/audio_{results[0]['type']}s/</code>

👉 <i>Tất cả file .mp3 và phụ đề .srt đã sẵn sàng kéo thả trực tiếp vào CapCut / Premiere để xuất video!</i>"""

    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"chat_id": chat_id, "text": html_msg, "parse_mode": "HTML"}).encode("utf-8")
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print(f"[✓] Đã gửi báo cáo sản xuất Voiceover ({len(results)} items) về Telegram!")
    except Exception as e:
        print(f"[!] Lỗi gửi Telegram: {e}")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Voiceover & Subtitle Generator")
    parser.add_argument("--type", choices=["shorts", "episode"], default="shorts", help="Generation target")
    parser.add_argument("--day", type=int, help="Single Day number (1-30)")
    parser.add_argument("--episode", type=int, help="Single Episode number (1-10)")
    parser.add_argument("--all", action="store_true", help="Batch generate all items in chosen category")
    parser.add_argument("--tld", default="com", choices=["com", "co.uk", "ca"], help="TTS Voice Accent")
    parser.add_argument("--telegram", action="store_true", help="Send summary digest to Telegram")
    args = parser.parse_args()

    results = []
    print("=" * 70)
    print("🎙️ AI MONEY MACHINE — STUDIO VOICEOVER & SUBTITLE GENERATOR")
    print("=" * 70)

    if args.type == "shorts":
        if args.all:
            print("[*] Batch generating all 30 days of Viral Shorts...")
            for d in range(1, 31):
                res = generate_short_voiceover(d, tld=args.tld)
                if res:
                    results.append(res)
        elif args.day:
            res = generate_short_voiceover(args.day, tld=args.tld)
            if res:
                results.append(res)
        else:
            print("[*] Generating sample Day 01 Short voiceover...")
            res = generate_short_voiceover(1, tld=args.tld)
            if res:
                results.append(res)

    elif args.type == "episode":
        if args.all:
            print("[*] Batch generating all 10 Full YouTube Episodes...")
            for ep in range(1, 11):
                res = generate_episode_voiceover(ep, tld=args.tld)
                if res:
                    results.append(res)
        elif args.episode:
            res = generate_episode_voiceover(args.episode, tld=args.tld)
            if res:
                results.append(res)
        else:
            print("[*] Generating Episode #001 voiceover...")
            res = generate_episode_voiceover(1, tld=args.tld)
            if res:
                results.append(res)

    print("-" * 70)
    print(f"🎉 SUCCESS: Generated {len(results)} voiceovers and subtitles!")
    print("=" * 70)

    if args.telegram and results:
        send_telegram_alert(results)

if __name__ == "__main__":
    main()
