from pathlib import Path

leads_js = """
const LEADS_DATA = [
  { id: 1, name: 'Austin Dental Co', niche: 'Cosmetic Dentistry', city: 'Austin, TX', to: 'contact@austindentalco.example', doc: 'Dr. Miller', type: 'dental' },
  { id: 2, name: 'Pure Radiance MedSpa', niche: 'Aesthetics & Spa', city: 'Miami, FL', to: 'info@pureradiancemedspa.example', doc: 'Sarah', type: 'medspa' },
  { id: 3, name: 'Premier 24/7 HVAC', niche: 'Heating & AC Repair', city: 'Dallas, TX', to: 'service@premierairdfw.example', doc: 'Mark', type: 'hvac' },
  { id: 4, name: 'Elite Smile Studio', niche: 'Orthodontics', city: 'San Jose, CA', to: 'hello@elitesmilestudio.example', doc: 'Dr. Nguyen', type: 'dental' },
  { id: 5, name: 'Apex Roofing & Solar', niche: 'Roofing & Solar', city: 'Phoenix, AZ', to: 'bids@apexroofsolar.example', doc: 'David', type: 'hvac' },
  { id: 6, name: 'Lumina Wellness', niche: 'Regenerative Med', city: 'Seattle, WA', to: 'frontdesk@luminawellness.example', doc: 'Dr. Adams', type: 'medspa' },
  { id: 7, name: 'Vanguard Luxury RE', niche: 'Luxury Real Estate', city: 'Denver, CO', to: 'team@vanguardluxuryre.example', doc: 'Alex', type: 'medspa' },
  { id: 8, name: 'ProActive Spine & Chiro', niche: 'Chiropractic', city: 'Chicago, IL', to: 'appointments@proactivechiro.example', doc: 'Dr. Davis', type: 'dental' },
  { id: 9, name: 'Rapid Response Plumbing', niche: '24/7 Emergency Plumber', city: 'Atlanta, GA', to: 'dispatch@rapidplumbatl.example', doc: 'Robert', type: 'hvac' },
  { id: 10, name: 'Silicon Valley Skin Lab', niche: 'Dermatology & Laser', city: 'Palo Alto, CA', to: 'support@svskinlab.example', doc: 'Dr. Patel', type: 'medspa' }
];

function buildMailto(lead) {
  let subj = '', body = '';
  if (lead.type === 'dental') {
    subj = 'quick question regarding ' + lead.name + \"'s after-hours patient inquiries\";
    body = 'Hi ' + lead.doc + ',\\n\\nI was reviewing your website yesterday around 8 PM and noticed that when a patient has an urgent dental question or wants to book an appointment after closing, their only option is to wait until morning.\\n\\nIn most competitive markets, clinics lose 4 to 8 high-intent new patient inquiries every single week simply because competitors with instant AI booking respond within 30 seconds.\\n\\nTo show you how easy this is to solve, I set up a quick 60-second interactive demo specifically for high-ticket clinics:\\n👉 Live Demo: https://chatbotdemo-hazel.vercel.app\\n\\nIt answers common treatment questions, qualifies insurance, and books appointments directly into your calendar 24/7.\\n\\nWould you be open to a quick 5-minute call this Thursday at 2 PM to see if this makes sense for ' + lead.name + '?\\n\\nBest regards,\\nAI Automation Specialist\\nPortfolio: https://chatbotdemo-hazel.vercel.app';
  } else if (lead.type === 'hvac') {
    subj = 'noticed your phone line around 7:15pm yesterday';
    body = 'Hi ' + lead.doc + ',\\n\\nWhen a homeowner has an emergency leak or broken AC after 6 PM, 85% of them will immediately hang up if they reach a voicemail and call the next contractor on Google.\\n\\nWe implemented an automated 15-second AI text-back workflow: whenever your line is busy or closed, an instant text goes out:\\n\"Hi! We are currently assisting another client. Do you have an urgent service request?\"\\n\\nThis single workflow captured $9,200 in recovered emergency jobs for a local contractor last month.\\n\\nI also ran an AI search audit on your domain to see if voice search (ChatGPT / Perplexity) recommends your business:\\n👉 Audit Engine: https://synapse-geo-audit.vercel.app\\n\\nHappy to share a 2-minute video walkthrough showing how this works if you find it helpful.\\n\\nCheers,\\nAI Workflow Specialist';
  } else {
    subj = 'automated consultation booking for ' + lead.name;
    body = 'Hi ' + lead.doc + ',\\n\\nLove the work you do at ' + lead.name + '!\\n\\nI noticed from your online presence that you receive a lot of inquiries regarding treatment pricing and booking. Many potential clients browse late at night and drop off before ever booking a consultation.\\n\\nWe build custom AI assistants that engage visitors, recommend treatment options, and lock in paid consultation deposits while you sleep.\\n\\nTake a look at how seamless the patient experience is:\\n👉 Interactive Sample: https://chatbotdemo-hazel.vercel.app\\n\\nWould you be against me sending over a 3-minute video showing what this would look like for ' + lead.name + '?\\n\\nWarm regards,\\nAI Client Acquisition Systems';
  }
  return 'mailto:' + lead.to + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
}

function renderLeadsTable() {
  const tbody = document.getElementById('leads-table-body');
  if (!tbody) return;
  tbody.innerHTML = LEADS_DATA.map(l => `
    <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
      <td style="padding:12px 10px; color:var(--text-muted); font-family:var(--font-mono);">#${l.id}</td>
      <td style="padding:12px 10px; font-weight:600; color:#fff;">${l.name}</td>
      <td style="padding:12px 10px; color:var(--text-muted);">${l.niche} • <span style="color:var(--cyan);">${l.city}</span></td>
      <td style="padding:12px 10px; font-family:var(--font-mono); font-size:12px; color:var(--text-sub);">${l.to}</td>
      <td style="padding:12px 10px; text-align:right;">
        <a href="${buildMailto(l)}" style="display:inline-block; background:linear-gradient(135deg,var(--accent),var(--cyan)); color:#fff; text-decoration:none; padding:6px 14px; border-radius:6px; font-size:12px; font-weight:600; transition:opacity 0.2s;">✉️ Open Email</a>
      </td>
    </tr>
  `).join('');
}
window.addEventListener('DOMContentLoaded', renderLeadsTable);
"""

panel_html = """
      <!-- Tab 5: Direct Mailto Leads -->
      <div id="direct-leads" class="copy-panel">
        <p style="font-size:13px; color:var(--text-muted); margin-bottom:16px;">
          🚀 <strong>1-Click Outreach:</strong> Click <strong>"✉️ Open Email"</strong> on any row below to instantly open your email client (Gmail, Outlook, Apple Mail) with the recipient, subject, and tailored AI pitch pre-filled!
        </p>
        <div style="overflow-x:auto;">
          <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
            <thead>
              <tr style="border-bottom:1px solid var(--border); color:var(--text-muted); text-transform:uppercase; font-size:11px; letter-spacing:1px;">
                <th style="padding:10px;">#</th>
                <th style="padding:10px;">Business / Clinic</th>
                <th style="padding:10px;">Niche & City</th>
                <th style="padding:10px;">Target Email</th>
                <th style="padding:10px; text-align:right;">1-Click Dispatch</th>
              </tr>
            </thead>
            <tbody id="leads-table-body"></tbody>
          </table>
        </div>
      </div>
"""

for file_name in ['dashboard.html', 'index.html']:
    p = Path(f'd:/Project/work/{file_name}')
    content = p.read_text(encoding='utf-8')
    
    # 1. Add tab button
    old_btn = '<button class="tab-btn" onclick="switchTab(\'gumroad-links\', this)">📦 Gumroad Store Links</button>'
    new_btn = old_btn + '\n        <button class="tab-btn" onclick="switchTab(\'direct-leads\', this)">🚀 1-Click Send Leads (10)</button>'
    if 'direct-leads' not in content:
        content = content.replace(old_btn, new_btn)
    
    # 2. Add panel
    old_panel_end = '        <button class="btn-copy" onclick="copySnippet(\'text-gumroad\')">📋 Copy Store Info</button>\n      </div>'
    new_panel = old_panel_end + '\n' + panel_html
    if 'id="direct-leads"' not in content:
        content = content.replace(old_panel_end, new_panel)
    
    # 3. Add JS
    old_script_end = '    function copySnippet(id) {'
    new_script = leads_js + '\n\n    function copySnippet(id) {'
    if 'LEADS_DATA' not in content:
        content = content.replace(old_script_end, new_script)
    
    p.write_text(content, encoding='utf-8')
    print(f'Successfully updated {file_name}')
