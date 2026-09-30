import urllib.request
import urllib.error
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

token = env.get("VERCEL_TOKEN")

req = urllib.request.Request(
    "https://api.vercel.com/v6/deployments?projectId=prj_lbhieHQYhDehcYvdZ63glPnxB4Ie&limit=1",
    headers={"Authorization": f"Bearer {token}"}
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
    latest = data.get("deployments", [])[0]
    deploy_id = latest.get("uid")
    url = latest.get("url")
    print(f"Latest deployment: {deploy_id} ({url})")

# Assign production alias
body = {
    "alias": "work-minh-lap.vercel.app"
}

req2 = urllib.request.Request(
    f"https://api.vercel.com/v2/deployments/{deploy_id}/aliases",
    data=json.dumps(body).encode(),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req2) as r2:
        res = json.loads(r2.read().decode())
        print("Production alias assigned successfully:", res.get("alias"))
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.reason}")
    print("Response body:", e.read().decode())
