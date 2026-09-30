import urllib.request
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent

env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

token = env.get("VERCEL_TOKEN")

# Let's inspect the latest 20 deployments across ALL projects to see what ran at 07:22
req = urllib.request.Request(
    "https://api.vercel.com/v6/deployments?limit=30",
    headers={"Authorization": f"Bearer {token}"}
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
    deployments = data.get("deployments", [])

print("Latest deployments across all projects:")
for d in deployments[:20]:
    t = datetime.fromtimestamp(d.get("created")/1000)
    meta = d.get("meta", {})
    sha = meta.get("githubCommitSha", "")[:7]
    print(f"{d.get('name'):25} | {d.get('state'):10} | {t} | {sha} | {meta.get('githubCommitMessage', '')[:35]}")
