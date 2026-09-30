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

req = urllib.request.Request(
    "https://api.vercel.com/v6/deployments?limit=100",
    headers={"Authorization": f"Bearer {token}"}
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
    deployments = data.get("deployments", [])

work_deps = [d for d in deployments if d.get("name") == "work"]
print(f"Total work deployments in last 100: {len(work_deps)}")
for d in work_deps[:15]:
    t = datetime.fromtimestamp(d.get("created")/1000)
    meta = d.get("meta", {})
    sha = meta.get("githubCommitSha", "")[:7]
    msg = meta.get("githubCommitMessage", "").replace("\n", " ")[:40]
    print(f"{d.get('state'):10} | {t} | {sha} | {d.get('url')} | {msg}")
