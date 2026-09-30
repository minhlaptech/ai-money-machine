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
deploy_id = "dpl_CLiSy6sNcPPaQZmPZnLQwsX6cXkx"

# Assign alias to deployment
body = {
    "alias": "work-minh-lap.vercel.app"
}

req = urllib.request.Request(
    f"https://api.vercel.com/v2/deployments/{deploy_id}/aliases",
    data=json.dumps(body).encode(),
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode())
        print("Alias assigned successfully:", res)
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.reason}")
    print("Response body:", e.read().decode())
