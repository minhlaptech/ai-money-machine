import urllib.request
import json
import time
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")

token = env.get("VERCEL_TOKEN")

# Trigger deploy hook
hook_url = "https://api.vercel.com/v1/integrations/deploy/prj_lbhieHQYhDehcYvdZ63glPnxB4Ie/hLY0EjD74V"
req = urllib.request.Request(hook_url, data=b"", method="POST")

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print("Deploy hook triggered:", res.get("job", {}).get("id"))

import subprocess
target_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT).decode().strip()[:7]
print(f"Targeting Git Commit SHA: {target_sha}")

# Wait and monitor for READY deployment
deploy_id = None
for i in range(15):
    time.sleep(3)
    req2 = urllib.request.Request(
        "https://api.vercel.com/v6/deployments?projectId=prj_lbhieHQYhDehcYvdZ63glPnxB4Ie&limit=2",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req2) as r2:
        data = json.loads(r2.read().decode())
        deployments = data.get("deployments", [])
        for d in deployments:
            sha = d.get("meta", {}).get("githubCommitSha", "")[:7]
            state = d.get("state")
            uid = d.get("uid")
            print(f"Check {i+1}: Deployment {uid} | sha: {sha} | state: {state}")
            if sha == target_sha and state == "READY":
                deploy_id = uid
                print(f"Target commit {target_sha} is READY! URL: {d.get('url')}")
                break
        if deploy_id:
            break

if deploy_id:
    # Assign production alias
    body = {"alias": "work-minh-lap.vercel.app"}
    req3 = urllib.request.Request(
        f"https://api.vercel.com/v2/deployments/{deploy_id}/aliases",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req3) as r3:
        alias_res = json.loads(r3.read().decode())
        print(f"Production alias assigned successfully: {alias_res.get('alias')}")
else:
    print("Deployment still building or requires more time.")
