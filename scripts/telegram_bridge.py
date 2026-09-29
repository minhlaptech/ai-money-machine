#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Bridge for AI Money Machine
Allows two-way interaction between the AI assistant and the user via Telegram.
- Send status notifications & alerts
- Ask questions and wait for user reply
- Read recent incoming messages from the user
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"

def load_env():
    """Loads TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from .env."""
    config = {}
    if not ENV_FILE.exists():
        return config
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, v = line.split("=", 1)
                config[k.strip()] = v.strip().strip('"').strip("'")
    return config

ENV = load_env()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN") or ENV.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID") or ENV.get("TELEGRAM_CHAT_ID", "")

def _call_api(method: str, payload: dict = None):
    if not BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not configured in .env or environment")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    if payload:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    else:
        req = urllib.request.Request(url)
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def send_message(text: str, parse_mode: str = "Markdown") -> dict:
    """Send a message to the user's Telegram."""
    if not CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is not configured in .env")
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    try:
        return _call_api("sendMessage", payload)
    except Exception as e:
        # Fallback to plain text if Markdown parsing fails
        if parse_mode:
            payload.pop("parse_mode")
            return _call_api("sendMessage", payload)
        raise e

def get_updates(offset=None, timeout=5) -> list:
    """Fetch updates from Telegram."""
    payload = {"timeout": timeout}
    if offset is not None:
        payload["offset"] = offset
    res = _call_api("getUpdates", payload)
    if res.get("ok"):
        return res.get("result", [])
    return []

def clear_pending_updates():
    """Acknowledge all existing updates so we only process new ones."""
    updates = get_updates(timeout=1)
    if updates:
        highest_id = max(u["update_id"] for u in updates)
        get_updates(offset=highest_id + 1, timeout=1)

def get_latest_user_messages(limit: int = 5) -> list:
    """Get the most recent messages sent by the user to the bot."""
    updates = get_updates(timeout=2)
    messages = []
    for u in updates:
        msg = u.get("message")
        if msg and str(msg.get("chat", {}).get("id")) == str(CHAT_ID):
            messages.append({
                "update_id": u["update_id"],
                "message_id": msg.get("message_id"),
                "date": msg.get("date"),
                "text": msg.get("text", ""),
            })
    return messages[-limit:]

def ask(question: str, timeout_sec: int = 180) -> str:
    """
    Sends question to Telegram, then waits up to timeout_sec for user reply.
    Returns the replied text, or None if timed out.
    """
    # 1. Clear old pending updates
    clear_pending_updates()
    
    # 2. Send the question
    prompt_text = f"❓ *CẦN THÔNG TIN BỔ SUNG:*\n\n{question}\n\n_(Vui lòng trả lời trực tiếp tin nhắn này trên Telegram)_"
    send_message(prompt_text)
    print(f"[Telegram Bridge] Question sent. Waiting up to {timeout_sec}s for reply...")

    # 3. Poll for response
    start_time = time.time()
    last_update_id = None
    
    while time.time() - start_time < timeout_sec:
        updates = get_updates(offset=last_update_id, timeout=5)
        for u in updates:
            last_update_id = u["update_id"] + 1
            msg = u.get("message")
            if msg and str(msg.get("chat", {}).get("id")) == str(CHAT_ID):
                reply_text = msg.get("text")
                if reply_text:
                    # Acknowledge by calling once more with next offset
                    get_updates(offset=last_update_id, timeout=1)
                    # Send confirmation back
                    send_message(f"✅ *Đã nhận thông tin:*\n\"{reply_text}\"\n\n_Đang tiếp tục xử lý công việc..._")
                    return reply_text
        time.sleep(2)
        
    print("[Telegram Bridge] Timed out waiting for reply.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python telegram_bridge.py send \"<message>\"")
        print("  python telegram_bridge.py ask \"<question>\" [timeout_seconds]")
        print("  python telegram_bridge.py read [limit]")
        print("  python telegram_bridge.py clear")
        sys.exit(1)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "send":
        if len(sys.argv) < 3:
            print("Error: Missing message argument")
            sys.exit(1)
        msg = sys.argv[2]
        res = send_message(msg)
        print("Sent successfully! Message ID:", res.get("result", {}).get("message_id"))
        
    elif cmd == "ask":
        if len(sys.argv) < 3:
            print("Error: Missing question argument")
            sys.exit(1)
        question = sys.argv[2]
        timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 180
        answer = ask(question, timeout_sec=timeout)
        if answer:
            print("\n=== USER REPLY RECEIVED ===")
            print(answer)
        else:
            print("\n=== NO REPLY (TIMED OUT) ===")
            sys.exit(2)
            
    elif cmd == "read":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        msgs = get_latest_user_messages(limit)
        print(json.dumps(msgs, ensure_ascii=False, indent=2))
        
    elif cmd == "clear":
        clear_pending_updates()
        print("Cleared all pending updates.")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
