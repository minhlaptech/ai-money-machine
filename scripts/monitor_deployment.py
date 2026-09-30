import urllib.request
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

token = env.get("VERCEL_TOKEN")

deploy_id = "dpl_CLiSy6sNcPPaQZmPZnLQwsX6cXkx"

for i in range(15):
    req = urllib.request.Request(
        f"https://api.vercel.com/v13/deployments/{deploy_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read().decode())
        state = data.get("readyState")
        print(f"Check {i+1}: {state}")
        if state in ("READY", "ERROR", "CANCELED"):
            print("Finished:", state)
            print("URL:", data.get("url"))
            break
    time.sleep(3)
