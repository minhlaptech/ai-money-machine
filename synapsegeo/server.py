"""
SynapseGEO Web Server & Live URL Inspection API
-----------------------------------------------
Chạy server phục vụ web app và cung cấp API kiểm tra trực tiếp
robots.txt, thẻ meta, và JSON-LD của bất kỳ website nào trên thế giới.
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import json
import re
import os
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 3030
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class GeoAuditHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/inspect?url='):
            target_url = self.path.split('/api/inspect?url=')[1]
            target_url = urllib.parse.unquote(target_url)
            self.handle_inspect(target_url)
        else:
            super().do_GET()

    def handle_inspect(self, target_url):
        if not target_url.startswith('http://') and not target_url.startswith('https://'):
            target_url = 'https://' + target_url

        parsed = urllib.parse.urlparse(target_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = f"{base_url}/robots.txt"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 SynapseGEO/1.0"
        }

        # Kiểm tra robots.txt cho AI Bots
        robots_text = ""
        gptbot_allowed = True
        perplexity_allowed = True
        try:
            req = urllib.request.Request(robots_url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                robots_text = resp.read().decode('utf-8', errors='ignore')
                if re.search(r'User-agent:\s*GPTBot[\s\S]*?Disallow:\s*/\s*$', robots_text, re.MULTILINE):
                    gptbot_allowed = False
                if re.search(r'User-agent:\s*PerplexityBot[\s\S]*?Disallow:\s*/\s*$', robots_text, re.MULTILINE):
                    perplexity_allowed = False
        except Exception:
            pass

        # Lấy trang chủ kiểm tra Schema JSON-LD
        has_schema = False
        title = ""
        meta_desc = ""
        try:
            req = urllib.request.Request(target_url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                if 'application/ld+json' in html:
                    has_schema = True
                m_title = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
                if m_title:
                    title = m_title.group(1).strip()
                m_desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html, re.IGNORECASE)
                if m_desc:
                    meta_desc = m_desc.group(1).strip()
        except Exception as e:
            title = f"Inspected: {parsed.netloc}"

        response_payload = {
            "target": target_url,
            "domain": parsed.netloc,
            "title": title,
            "meta_description": meta_desc,
            "gptbot_allowed": gptbot_allowed,
            "perplexity_allowed": perplexity_allowed,
            "has_schema_jsonld": has_schema,
            "status": "success"
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_payload).encode('utf-8'))

def start_server():
    with socketserver.TCPServer(("", PORT), GeoAuditHandler) as httpd:
        print(f"[*] SynapseGEO Server đang chạy tại: http://localhost:{PORT}")
        print("[*] Sẵn sàng phục vụ người dùng và kiểm tra live websites.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Dừng server.")

if __name__ == '__main__':
    start_server()
