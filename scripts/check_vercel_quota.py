import urllib.request
import urllib.error
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
    print(f"Total deployments in last 100 list: {len(deployments)}")
    if deployments:
        oldest = deployments[-1]
        newest = deployments[0]
        oldest_dt = datetime.fromtimestamp(oldest.get("created")/1000)
        newest_dt = datetime.fromtimestamp(newest.get("created")/1000)
        print(f"Newest deployment: {newest_dt}")
        print(f"Newest state: {newest.get('state')} | errorCode: {newest.get('errorCode')} | commit: {newest.get('meta', {}).get('githubCommitMessage')}")
        print(f"Oldest deployment in list of 100: {oldest_dt}")
        # The rolling 24h window expires when deployments older than 24h drop off!
        now = datetime.now()
        age_hours = (now - oldest_dt).total_seconds() / 3600
        print(f"Oldest was created {age_hours:.1f} hours ago.")
        print(f"Time until oldest drops off 24h window: {max(0, 24 - age_hours):.1f} hours.")
