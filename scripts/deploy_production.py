#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Money Machine — Autonomous Vercel Production Deployer
---------------------------------------------------------
Deploys the entire unified monorepo to Vercel production using Vercel CLI.
Ensures zero configuration errors and instant live publishing.
"""

import sys
import os
import subprocess
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent

def get_token():
    env_file = ROOT / ".env"
    if not env_file.exists():
        print("[!] .env not found")
        return None
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("VERCEL_TOKEN="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

def deploy():
    token = get_token()
    if not token:
        print("[!] VERCEL_TOKEN missing in .env")
        sys.exit(1)

    print("=" * 65)
    print("🚀 DEPLOYING AI MONEY MACHINE TO VERCEL PRODUCTION")
    print("=" * 65)

    cmd = [
        "npx.cmd" if os.name == "nt" else "npx",
        "-y",
        "vercel",
        "deploy",
        "--prod",
        "--yes",
        "--token",
        token
    ]

    print(f"[*] Running command: npx -y vercel deploy --prod --yes")
    proc = subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
    
    url = None
    for line in proc.stdout:
        print(line, end="")
        if "https://" in line and "vercel.app" in line:
            for part in line.split():
                if part.startswith("https://") and "vercel.app" in part:
                    url = part.strip()

    proc.wait()
    if proc.returncode == 0:
        print("\n" + "=" * 65)
        print(f"🎉 PRODUCTION DEPLOYMENT SUCCESSFUL!")
        if url:
            print(f"🌐 Live URL: {url}")
        print("=" * 65)
    else:
        print(f"\n[!] Deployment failed with exit code: {proc.returncode}")
        sys.exit(proc.returncode)

if __name__ == "__main__":
    deploy()
