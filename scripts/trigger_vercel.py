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
    "https://api.vercel.com/v9/projects/work",
    headers={"Authorization": f"Bearer {token}"}
)

with urllib.request.urlopen(req) as r:
    data = json.loads(r.read().decode())
    link = data.get("link", {})
    print("Project link info:")
    print(json.dumps(link, indent=2))
    repo_id = link.get("repoId")
    project_id = data.get("id")

if repo_id:
    print(f"Repo ID: {repo_id}, Project ID: {project_id}")
    # Now trigger deployment
    deploy_body = {
        "name": "work",
        "project": project_id,
        "gitSource": {
            "type": "github",
            "repoId": repo_id,
            "ref": "master"
        }
    }
    req2 = urllib.request.Request(
        "https://api.vercel.com/v13/deployments?forceNew=1",
        data=json.dumps(deploy_body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    try:
        with urllib.request.urlopen(req2) as r2:
            res = json.loads(r2.read().decode())
            print("Deployment triggered successfully!")
            print(res.get("id"), res.get("url"), res.get("readyState"))
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code}: {e.reason}")
        print("Response body:", e.read().decode())
