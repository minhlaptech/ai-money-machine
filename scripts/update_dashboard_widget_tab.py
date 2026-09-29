"""
Dashboard Embed Widget Tab & Live Demonstration Integrator
-----------------------------------------------------------
Thêm tab "🧩 Client Widget Generator" vào dashboard.html & index.html,
và nhúng trực tiếp copilot-widget.js vào chân trang để demo tương tác 24/7.
"""

import sys
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

WIDGET_TAB_BTN = '        <button class="tab-btn" onclick="switchTab(\'widget-generator\', this)">🧩 Client Widget Generator</button>'

WIDGET_PANEL_HTML = """      <!-- Tab 6: Widget Generator -->
      <div id="widget-generator" class="copy-panel">
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:16px;">
          🛠️ <strong>Client Deliverable Embed Generator:</strong> Generate the 1-line script tag to install the 24/7 AI Receptionist & Booking Copilot onto any client's website (WordPress, Webflow, Shopify, Wix, custom HTML).
        </p>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; margin-bottom:16px;">
          <div>
            <label style="font-size:11px; text-transform:uppercase; color:var(--text-muted); display:block; margin-bottom:4px;">Client Business Name</label>
            <input type="text" id="cfg-name" value="Austin Dental Co" oninput="updateWidgetSnippet()" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid var(--border); border-radius:6px; padding:8px 12px; color:#fff; font-size:13px;">
          </div>
          <div>
            <label style="font-size:11px; text-transform:uppercase; color:var(--text-muted); display:block; margin-bottom:4px;">Brand Color Theme</label>
            <input type="text" id="cfg-color" value="#7c5cfc" oninput="updateWidgetSnippet()" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid var(--border); border-radius:6px; padding:8px 12px; color:#fff; font-size:13px;">
          </div>
          <div>
            <label style="font-size:11px; text-transform:uppercase; color:var(--text-muted); display:block; margin-bottom:4px;">Calendar / Booking URL</label>
            <input type="text" id="cfg-booking" value="https://calendly.com/your-clinic" oninput="updateWidgetSnippet()" style="width:100%; background:rgba(255,255,255,0.05); border:1px solid var(--border); border-radius:6px; padding:8px 12px; color:#fff; font-size:13px;">
          </div>
        </div>
        <div class="snippet-box" id="text-widget" style="font-family:var(--font-mono); font-size:12px; color:#00f2fe;">&lt;!-- MinhLap AI Copilot 24/7 Intake Widget --&gt;
&lt;script src="https://work-minh-lap.vercel.app/copilot-widget.js" 
        data-business="Austin Dental Co" 
        data-color="#7c5cfc" 
        data-booking="https://calendly.com/your-clinic" 
        async&gt;&lt;/script&gt;</div>
        <button class="btn-copy" onclick="copySnippet('text-widget')">📋 Copy 1-Line Embed Code</button>
      </div>"""

WIDGET_HELPER_JS = """    function updateWidgetSnippet() {
      const name = document.getElementById('cfg-name').value || 'AI Assistant';
      const color = document.getElementById('cfg-color').value || '#7c5cfc';
      const booking = document.getElementById('cfg-booking').value || 'https://calendly.com';
      const code = `<!-- MinhLap AI Copilot 24/7 Intake Widget -->\\n<script src="https://work-minh-lap.vercel.app/copilot-widget.js" \\n        data-business="${name}" \\n        data-color="${color}" \\n        data-booking="${booking}" \\n        async><\\/script>`;
      document.getElementById('text-widget').innerText = code;
    }"""

WIDGET_SCRIPT_TAG = """  <!-- Live 24/7 AI Copilot Widget Demonstration -->
  <script src="copilot-widget.js" data-business="MinhLap AI Systems" data-color="#7c5cfc" async></script>
</body>"""

def update_dashboards():
    root = Path(__file__).resolve().parent.parent
    files = [root / "dashboard.html", root / "index.html"]

    for f in files:
        if not f.exists():
            continue
        content = f.read_text(encoding='utf-8')

        # 1. Add tab button
        old_tab = '<button class="tab-btn" onclick="switchTab(\'direct-leads\', this)">🚀 1-Click Send Leads (30)</button>'
        if old_tab in content and 'widget-generator' not in content:
            content = content.replace(old_tab, old_tab + '\n' + WIDGET_TAB_BTN)

        # 2. Add panel
        old_panel_end = '      </div>\n    </div>\n\n    <!-- Market Scout Live Feed -->'
        if old_panel_end in content and 'id="widget-generator"' not in content:
            new_block = '      </div>\n\n' + WIDGET_PANEL_HTML + '\n    </div>\n\n    <!-- Market Scout Live Feed -->'
            content = content.replace(old_panel_end, new_block)

        # 3. Add helper JS
        old_copy_func = '    function copySnippet(id) {'
        if old_copy_func in content and 'updateWidgetSnippet' not in content:
            content = content.replace(old_copy_func, WIDGET_HELPER_JS + '\n\n' + old_copy_func)

        # 4. Add widget script tag before </body>
        if '</body>' in content and 'copilot-widget.js' not in content:
            content = content.replace('</body>', WIDGET_SCRIPT_TAG)

        f.write_text(content, encoding='utf-8')
        print(f"[✓] Successfully added Widget Generator tab and live copilot-widget.js to {f.name}!")

if __name__ == "__main__":
    update_dashboards()
