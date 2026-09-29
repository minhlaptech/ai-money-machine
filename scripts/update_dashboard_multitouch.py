"""
Multi-Touch Follow-Up Outreach Engine Integrator for Dashboard (with CRM State)
-------------------------------------------------------------------------------
Cập nhật bảng điều khiển (dashboard.html & index.html) với:
1. Hệ thống Outreach Đa Chạm 3 Giai Đoạn (Day 1 -> Day 3 -> Day 7).
2. Tích hợp Quản Lý Phễu Bán Hàng Trực Quan (CRM Pipeline) lưu trạng thái vĩnh viễn trên LocalStorage.
3. Thanh KPI thời gian thực (Tổng Leads, Đã gửi Day 1, Đã gửi Day 3, Cuộc gọi đã chốt, Khách hàng ký hợp đồng).
4. Liên kết trực tiếp tới 30 bản Proposal & AI Audit trong proposals/.
"""

import sys
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

STAGE_CONTROLS_HTML = """        <!-- CRM Pipeline Stats Summary Bar -->
        <div id="crm-stats-bar" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:10px; margin-bottom:16px;"></div>

        <!-- Filter Pill Controls & Sequence Switcher -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:12px;">
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button class="batch-pill-btn active" onclick="filterBatch('all', this)" style="background:rgba(255,255,255,0.06); border:1px solid var(--border); color:#fff; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; cursor:pointer;">All Leads (30)</button>
            <button class="batch-pill-btn" onclick="filterBatch('1', this)" style="background:rgba(255,255,255,0.06); border:1px solid var(--border); color:#b794f4; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; cursor:pointer;">🦷 Batch 1: Local SMBs (10)</button>
            <button class="batch-pill-btn" onclick="filterBatch('2', this)" style="background:rgba(255,255,255,0.06); border:1px solid var(--border); color:#00f2fe; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; cursor:pointer;">🛍️ Batch 2: E-Com & SaaS (10)</button>
            <button class="batch-pill-btn" onclick="filterBatch('3', this)" style="background:rgba(255,255,255,0.06); border:1px solid var(--border); color:#ffb74d; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:600; cursor:pointer;">🏛️ Batch 3: High-Ticket Legal/CPA (10)</button>
          </div>
          <div style="display:flex; gap:6px; background:rgba(0,0,0,0.3); padding:4px; border-radius:10px; border:1px solid var(--border);">
            <button class="stage-pill-btn active" onclick="filterStage(1, this)" style="background:linear-gradient(135deg,var(--accent),var(--cyan)); border:none; color:#fff; padding:5px 12px; border-radius:6px; font-size:11px; font-weight:700; cursor:pointer;">🎯 Day 1: Hook</button>
            <button class="stage-pill-btn" onclick="filterStage(2, this)" style="background:transparent; border:none; color:var(--text-muted); padding:5px 12px; border-radius:6px; font-size:11px; font-weight:600; cursor:pointer;">📈 Day 3: ROI Value</button>
            <button class="stage-pill-btn" onclick="filterStage(3, this)" style="background:transparent; border:none; color:var(--text-muted); padding:5px 12px; border-radius:6px; font-size:11px; font-weight:600; cursor:pointer;">🚪 Day 7: Break-Up</button>
          </div>
        </div>"""

LEADS_DATA_JS = r"""const LEADS_DATA = [
  // --- BATCH 1: Local SMBs ---
  { id: 1, batch: 1, name: 'Austin Dental Co', niche: 'Cosmetic Dentistry', city: 'Austin, TX', to: 'contact@austindentalco.example', doc: 'Dr. Miller', type: 'dental', val: 750, lost: 14 },
  { id: 2, batch: 1, name: 'Pure Radiance MedSpa', niche: 'Aesthetics & Spa', city: 'Miami, FL', to: 'info@pureradiancemedspa.example', doc: 'Sarah', type: 'medspa', val: 650, lost: 16 },
  { id: 3, batch: 1, name: 'Premier 24/7 HVAC', niche: 'Heating & AC Repair', city: 'Dallas, TX', to: 'service@premierairdfw.example', doc: 'Mark', type: 'hvac', val: 1200, lost: 10 },
  { id: 4, batch: 1, name: 'Elite Smile Studio', niche: 'Orthodontics', city: 'San Jose, CA', to: 'hello@elitesmilestudio.example', doc: 'Dr. Nguyen', type: 'dental', val: 1500, lost: 8 },
  { id: 5, batch: 1, name: 'Apex Roofing & Solar', niche: 'Roofing & Solar', city: 'Phoenix, AZ', to: 'bids@apexroofsolar.example', doc: 'David', type: 'hvac', val: 2500, lost: 6 },
  { id: 6, batch: 1, name: 'Lumina Wellness', niche: 'Regenerative Med', city: 'Seattle, WA', to: 'frontdesk@luminawellness.example', doc: 'Dr. Adams', type: 'medspa', val: 850, lost: 12 },
  { id: 7, batch: 1, name: 'Vanguard Luxury RE', niche: 'Luxury Real Estate', city: 'Denver, CO', to: 'team@vanguardluxuryre.example', doc: 'Alex', type: 'realestate', val: 4500, lost: 4 },
  { id: 8, batch: 1, name: 'ProActive Spine & Chiro', niche: 'Chiropractic', city: 'Chicago, IL', to: 'appointments@proactivechiro.example', doc: 'Dr. Davis', type: 'dental', val: 400, lost: 18 },
  { id: 9, batch: 1, name: 'Rapid Response Plumbing', niche: '24/7 Emergency Plumber', city: 'Atlanta, GA', to: 'dispatch@rapidplumbatl.example', doc: 'Robert', type: 'hvac', val: 800, lost: 15 },
  { id: 10, batch: 1, name: 'Silicon Valley Skin Lab', niche: 'Dermatology & Laser', city: 'Palo Alto, CA', to: 'support@svskinlab.example', doc: 'Dr. Patel', type: 'medspa', val: 950, lost: 11 },

  // --- BATCH 2: E-Commerce & SaaS ---
  { id: 11, batch: 2, name: 'Velora Activewear', niche: 'Athleisure Apparel', city: 'Los Angeles, CA', to: 'hello@veloraactive.example', doc: 'Team Velora', type: 'ecom', val: 120, lost: 65 },
  { id: 12, batch: 2, name: 'NuvoGlow Skincare', niche: 'Clean D2C Beauty', city: 'New York, NY', to: 'partners@nuvoglowbeauty.example', doc: 'Founder', type: 'ecom', val: 85, lost: 90 },
  { id: 13, batch: 2, name: 'PulseMetrics AI', niche: 'B2B Analytics SaaS', city: 'San Francisco, CA', to: 'growth@pulsemetrics.example', doc: 'Founder', type: 'saas', val: 1800, lost: 7 },
  { id: 14, batch: 2, name: 'HydroFlow Bottle', niche: 'Eco Hydration D2C', city: 'Boulder, CO', to: 'support@hydroflowbottle.example', doc: 'Team HydroFlow', type: 'ecom', val: 60, lost: 110 },
  { id: 15, batch: 2, name: 'CloudDesk Help', niche: 'Customer Support SaaS', city: 'Austin, TX', to: 'hello@clouddeskhelp.example', doc: 'Product Lead', type: 'saas', val: 2200, lost: 6 },
  { id: 16, batch: 2, name: 'Artisan Roast Club', niche: 'Subscription Coffee', city: 'Portland, OR', to: 'orders@artisanroastclub.example', doc: 'Founder', type: 'ecom', val: 45, lost: 140 },
  { id: 17, batch: 2, name: 'StackSync Dev', niche: 'Developer Workflows', city: 'Seattle, WA', to: 'founders@stacksyncdev.example', doc: 'Engineering Lead', type: 'saas', val: 3000, lost: 5 },
  { id: 18, batch: 2, name: 'Pawsome Pet Boxes', niche: 'Pet Subscription D2C', city: 'Denver, CO', to: 'hello@pawsomepetbox.example', doc: 'Customer Team', type: 'ecom', val: 70, lost: 85 },
  { id: 19, batch: 2, name: 'LeadFlow CRM', niche: 'SMB Sales CRM SaaS', city: 'Boston, MA', to: 'inquiries@leadflowcrm.example', doc: 'Growth Team', type: 'saas', val: 1500, lost: 8 },
  { id: 20, batch: 2, name: 'ZenSleep Mattress', niche: 'D2C Sleep Wellness', city: 'Chicago, IL', to: 'concierge@zensleepbed.example', doc: 'Marketing Team', type: 'ecom', val: 650, lost: 22 },

  // --- BATCH 3: High-Ticket Professional Services ---
  { id: 21, batch: 3, name: 'Sterling & Partners Legal', niche: 'Personal Injury Law', city: 'Chicago, IL', to: 'contact@sterlinglegalchi.example', doc: 'David Sterling', type: 'legal', val: 3500, lost: 5 },
  { id: 22, batch: 3, name: 'Summit Crest Luxury Realty', niche: 'Luxury Real Estate', city: 'Aspen, CO', to: 'inquiries@summitcrestrealty.example', doc: 'Victoria Vance', type: 'realestate', val: 6000, lost: 3 },
  { id: 23, batch: 3, name: 'Beacon Hill CPA & Tax', niche: 'Tax & Advisory Firm', city: 'Boston, MA', to: 'tax@beaconhillcpa.example', doc: 'Marcus Brody', type: 'cpa', val: 2000, lost: 7 },
  { id: 24, batch: 3, name: 'Pacific Coast Family Law', niche: 'Divorce & Family Law', city: 'San Diego, CA', to: 'help@pacificfamilylawsd.example', doc: 'Elena Rostova', type: 'legal', val: 2800, lost: 6 },
  { id: 25, batch: 3, name: 'Vanguard Wealth & Accounting', niche: 'Family Office & CPA', city: 'New York, NY', to: 'office@vanguardwealthnyc.example', doc: 'Jonathan Vance', type: 'cpa', val: 4000, lost: 4 },
  { id: 26, batch: 3, name: 'Redwood Corporate Counsel', niche: 'Corporate & M&A', city: 'Austin, TX', to: 'hello@redwoodcounseltx.example', doc: 'Sarah Jenkins', type: 'legal', val: 5000, lost: 3 },
  { id: 27, batch: 3, name: 'Pinnacle Commercial RE', niche: 'Commercial Brokerage', city: 'Dallas, TX', to: 'deals@pinnaclecredfw.example', doc: 'Robert Miller', type: 'realestate', val: 8000, lost: 2 },
  { id: 28, batch: 3, name: 'Harborview Estate Planning', niche: 'Trusts & Estates', city: 'Seattle, WA', to: 'info@harborviewestateswa.example', doc: 'Cynthia Thorne', type: 'legal', val: 2400, lost: 7 },
  { id: 29, batch: 3, name: 'Apex Audit & Valuation', niche: 'Audit & Valuation', city: 'Atlanta, GA', to: 'valuation@apexauditadvisory.example', doc: 'Richard Hall', type: 'cpa', val: 3200, lost: 5 },
  { id: 30, batch: 3, name: 'Metro Injury Defense Group', niche: 'Insurance Litigation', city: 'Miami, FL', to: 'litigation@metroinjurydefense.example', doc: 'Carlos Mendez', type: 'legal', val: 4500, lost: 4 }
];

let currentBatchFilter = 'all';
let currentStageFilter = 1;

function getLeadStatus(id) {
  return localStorage.getItem('lead_crm_status_' + id) || 'new';
}

function setLeadStatus(id, st) {
  localStorage.setItem('lead_crm_status_' + id, st);
  renderLeadsTable();
}

function handleLeadDispatch(id, stage) {
  const nextStatus = stage === 1 ? 'day1' : stage === 2 ? 'day3' : 'day7';
  localStorage.setItem('lead_crm_status_' + id, nextStatus);
  setTimeout(renderLeadsTable, 400);
}

function filterBatch(batch, btn) {
  currentBatchFilter = batch;
  document.querySelectorAll('.batch-pill-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  renderLeadsTable();
}

function filterStage(stage, btn) {
  currentStageFilter = stage;
  document.querySelectorAll('.stage-pill-btn').forEach(b => {
    b.classList.remove('active');
    b.style.background = 'transparent';
    b.style.color = 'var(--text-muted)';
    b.style.fontWeight = '600';
  });
  btn.classList.add('active');
  btn.style.background = 'linear-gradient(135deg,var(--accent),var(--cyan))';
  btn.style.color = '#fff';
  btn.style.fontWeight = '700';
  renderLeadsTable();
}

function buildMailto(lead, stage) {
  let subj = '', body = '';
  let slug = lead.name.toLowerCase().replace(/ /g, '_').replace(/&/g, 'and').replace(/\\//g, '-').replace(/\\\\/g, '-').replace(/,/g, '').replace(/\\./g, '');
  let sandboxUrl = 'https://work-minh-lap.vercel.app/sandboxes/' + slug + '_sandbox.html';
  let reportUrl = 'https://work-minh-lap.vercel.app/reports/' + slug + '_roi_report.html';
  
  if (stage === 2) {
    const monthlyLoss = (lead.lost * lead.val).toLocaleString();
    subj = 're: ' + lead.name + ' after-hours intake (ran the numbers)';
    body = 'Hi ' + lead.doc + ',\\n\\n' +
      'Following up briefly on my note from earlier this week regarding ' + lead.name + \"'s after-hours client intake.\\n\\n\" +
      'I ran ' + lead.name + \"'s estimated inquiry volume through our revenue recovery model:\\n\" +
      '• Estimated monthly inquiries after 6 PM: ~' + lead.lost + ' prospects\\n' +
      '• Estimated missed revenue: ~$' + monthlyLoss + '/month\\n\\n' +
      'You can review your customized monthly performance & ROI forecast here:\\n' +
      '👉 Live Custom ROI Report: ' + reportUrl + '\\n' +
      '👉 Interactive ROI Calculator: https://work-minh-lap.vercel.app/calculator\\n\\n' +
      'Our AI intake copilot typically recovers 4 to 8 qualified client bookings within the first 30 days, paying for itself several times over.\\n\\n' +
      'I also prepared a customized 2-page implementation audit for ' + lead.name + '. Would you be against me sending it over?\\n\\n' +
      'Best regards,\\nMinh Lap\\nAI Solutions Architect\\nLive Sandbox: ' + sandboxUrl;
  } else if (stage === 3) {
    subj = 'permission to close your file, ' + lead.doc + '?';
    body = 'Hi ' + lead.doc + ',\\n\\n' +
      'I haven\\'t heard back, so I assume that automating after-hours client intake and recapturing missed inquiries isn\\'t a priority for ' + lead.name + ' right now.\\n\\n' +
      'I\\'m closing out your file so I don\\'t clutter your inbox.\\n\\n' +
      'If priorities ever shift and you\\'d like to see how similar businesses in ' + lead.city + ' are automatically booking clients 24/7 without extra staff, you\\'re always welcome to test your live sandbox prototype:\\n' +
      '👉 ' + sandboxUrl + '\\n\\n' +
      'Wishing ' + lead.name + ' continued growth and success!\\n\\n' +
      'Warm regards,\\nMinh Lap\\nAI Solutions Architect';
  } else {
    if (lead.type === 'dental') {
      subj = 'quick question regarding ' + lead.name + \"'s after-hours patient inquiries\";
      body = 'Hi ' + lead.doc + ',\\n\\nI was reviewing your website yesterday around 8 PM and noticed that when a patient has an urgent dental question or wants to book an appointment after closing, their only option is to wait until morning.\\n\\nIn most competitive markets, clinics lose 4 to 8 high-intent new patient inquiries every single week simply because competitors with instant AI booking respond within 30 seconds.\\n\\nTo show you how easy this is to solve, I set up a live interactive sandbox prototype specifically for ' + lead.name + ':\\n👉 Live Sandbox Demo: ' + sandboxUrl + '\\n\\nIt answers common treatment questions, qualifies insurance, and books appointments directly into your calendar 24/7.\\n\\nWould you be open to a quick 5-minute call this Thursday at 2 PM to see if this makes sense for ' + lead.name + '?\\n\\nBest regards,\\nMinh Lap\\nAI Solutions Architect\\nLive Sandbox: ' + sandboxUrl;
    } else if (lead.type === 'hvac') {
      subj = 'noticed your phone line around 7:15pm yesterday';
      body = 'Hi ' + lead.doc + ',\\n\\nWhen a homeowner has an emergency leak or broken AC after 6 PM, 85% of them will immediately hang up if they reach a voicemail and call the next contractor on Google.\\n\\nWe implemented an automated 15-second AI text-back workflow: whenever your line is busy or closed, an instant text goes out:\\n\"Hi! We are currently assisting another client. Do you have an urgent service request?\"\\n\\nThis single workflow captured $9,200 in recovered emergency jobs for a local contractor last month.\\n\\nI also set up an interactive test sandbox for ' + lead.name + ':\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nHappy to share a 2-minute video walkthrough showing how this works if you find it helpful.\\n\\nCheers,\\nMinh Lap\\nAI Workflow Specialist';
    } else if (lead.type === 'ecom') {
      subj = 'quick idea on recovering abandoned carts for ' + lead.name;
      body = 'Hi ' + lead.doc + ',\\n\\nLove what you\\'re building at ' + lead.name + '!\\n\\nNoticed that visitors who leave items in cart often drop off due to sizing, delivery, or return policy questions before checkout.\\n\\nWe build autonomous AI shopper assistants that engage hesitant shoppers right before drop-off, answering questions in real-time and offering personalized incentive bundles.\\n\\nTake a look at how this operates on your live prototype:\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nWould love to share 2 quick ideas that boosted checkout conversions by 14% for similar D2C brands. Free for a 5-min chat this week?\\n\\nBest,\\nMinh Lap\\nE-Commerce Automation Consultant';
    } else if (lead.type === 'saas') {
      subj = 'boosting activation for ' + lead.name + ' trial signups';
      body = 'Hi ' + lead.doc + ',\\n\\nBig fan of ' + lead.name + '!\\n\\nI noticed that many self-serve SaaS users drop off during the first 48 hours when they hit an integration or setup blocker. Static documentation often isn\\'t enough to prevent churn.\\n\\nWe build conversational onboarding AI copilots trained on your API docs and changelog that proactively assist trial users in hitting their \\'Aha!\\' moment within minutes.\\n\\nCheck out your live prototype here:\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nOpen to a quick 5-min feedback chat this Wednesday at 10 AM PST?\\n\\nCheers,\\nMinh Lap\\nSaaS Growth & AI Systems';
    } else if (lead.type === 'legal') {
      subj = 'quick question regarding ' + lead.name + \"'s after-hours intake process\";
      body = 'Hi ' + lead.doc + ',\\n\\nI was reviewing your website yesterday evening around 8:30 PM and noticed that potential new clients facing an urgent legal matter only have a standard static form.\\n\\nIn high-stakes cases, 67% of prospective claimants contact 2 to 3 firms simultaneously. The firm that responds, qualifies, and schedules within 3 minutes captures 80% of retained cases.\\n\\nWe built an intelligent legal intake assistant that conducts an empathetic intake questionnaire, screens jurisdiction & merit, and schedules onto your calendar 24/7.\\n\\nTest your firm\\'s customized sandbox prototype here:\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nOpen to a brief 7-minute call this Thursday at 2 PM to explore if this could add 3-5 retained cases/month to ' + lead.name + '?\\n\\nBest regards,\\nMinh Lap\\nAI Legal Workflow Automation';
    } else if (lead.type === 'realestate') {
      subj = 'capturing after-hours buyer inquiries for ' + lead.name + ' listings';
      body = 'Hi ' + lead.doc + ',\\n\\nYour active luxury listings look exceptional.\\n\\nWhen high-net-worth buyers browse properties on weekends or late at night, they expect instant answers regarding HOA rules, lot dimensions, and private showing availability.\\n\\nWe deploy bespoke AI Concierge agents that answer deep questions from your MLS data, pre-qualify buyers, and coordinate VIP private showings straight into your calendar 24/7.\\n\\nTest your agency\\'s live concierge sandbox here:\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nAvailable for a 5-minute conversation this Thursday to see what this looks like with your active listings?\\n\\nWarm regards,\\nMinh Lap\\nHigh-Ticket Automation Systems';
    } else if (lead.type === 'cpa') {
      subj = 'eliminating 15+ hours/week of client document chasing for ' + lead.name;
      body = 'Hi ' + lead.doc + ',\\n\\nAs tax season and quarterly filings approach, the single biggest drain on billable partner hours is chasing clients for missing 1099s, W2s, and receipts.\\n\\nWe build autonomous document-collection pipelines using AI OCR and Make.com that send automated reminder loops, verify document clarity with AI vision, and sync files directly into client folders and accounting software.\\n\\nFirms save an average of 18 hours per accountant every month while accelerating client turnaround by 40%.\\n\\nTest your firm\\'s intake sandbox here:\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nWould you be against me sending over a 2-minute video walkthrough showing how this workflow operates?\\n\\nCheers,\\nMinh Lap\\nAI Workflow Automation Consultant';
    } else {
      subj = 'automated consultation booking for ' + lead.name;
      body = 'Hi ' + lead.doc + ',\\n\\nLove the work you do at ' + lead.name + '!\\n\\nI noticed that you receive a lot of inquiries regarding treatment pricing and booking. Many potential clients browse late at night and drop off before ever booking a consultation.\\n\\nWe build custom AI assistants that engage visitors, recommend treatment options, and lock in paid consultation deposits while you sleep.\\n\\nTake a look at how seamless the patient experience is on your live sandbox:\\n👉 Live Sandbox: ' + sandboxUrl + '\\n\\nWould you be against me sending over a 3-minute video showing what this would look like for ' + lead.name + '?\\n\\nWarm regards,\\nMinh Lap\\nAI Client Acquisition Systems';
    }
  }
  return 'mailto:' + lead.to + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(body);
}

function renderCRMStats() {
  const statsEl = document.getElementById('crm-stats-bar');
  if (!statsEl) return;
  
  let newC = 0, day1C = 0, day3C = 0, day7C = 0, bookedC = 0, wonC = 0;
  LEADS_DATA.forEach(l => {
    const st = getLeadStatus(l.id);
    if (st === 'won') wonC++;
    else if (st === 'booked') bookedC++;
    else if (st === 'day7') day7C++;
    else if (st === 'day3') day3C++;
    else if (st === 'day1') day1C++;
    else newC++;
  });

  statsEl.innerHTML = `
    <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border); padding:10px 14px; border-radius:8px;">
      <div style="font-size:11px; color:var(--text-muted); text-transform:uppercase;">Total Pipeline</div>
      <div style="font-size:18px; font-weight:700; color:#fff;">\${LEADS_DATA.length} Leads</div>
    </div>
    <div style="background:rgba(124,92,252,0.08); border:1px solid rgba(124,92,252,0.3); padding:10px 14px; border-radius:8px;">
      <div style="font-size:11px; color:#b794f4; text-transform:uppercase;">🎯 Day 1 Sent</div>
      <div style="font-size:18px; font-weight:700; color:#b794f4;">\${day1C}</div>
    </div>
    <div style="background:rgba(0,242,254,0.08); border:1px solid rgba(0,242,254,0.3); padding:10px 14px; border-radius:8px;">
      <div style="font-size:11px; color:#00f2fe; text-transform:uppercase;">📈 Day 3 Follow-Up</div>
      <div style="font-size:18px; font-weight:700; color:#00f2fe;">\${day3C}</div>
    </div>
    <div style="background:rgba(52,211,153,0.08); border:1px solid rgba(52,211,153,0.3); padding:10px 14px; border-radius:8px;">
      <div style="font-size:11px; color:#34d399; text-transform:uppercase;">📞 Calls Booked</div>
      <div style="font-size:18px; font-weight:700; color:#34d399;">\${bookedC}</div>
    </div>
    <div style="background:rgba(255,215,0,0.08); border:1px solid rgba(255,215,0,0.3); padding:10px 14px; border-radius:8px;">
      <div style="font-size:11px; color:#ffd700; text-transform:uppercase;">🏆 Won Retainers</div>
      <div style="font-size:18px; font-weight:700; color:#ffd700;">\${wonC} ($\${(wonC * 1200).toLocaleString()})</div>
    </div>
  `;
}

function renderLeadsTable() {
  const tbody = document.getElementById('leads-table-body');
  if (!tbody) return;
  const filtered = currentBatchFilter === 'all' 
    ? LEADS_DATA 
    : LEADS_DATA.filter(l => l.batch === parseInt(currentBatchFilter));
  
  const countEl = document.getElementById('leads-count-label');
  const stageNames = { 1: 'Day 1: Cold Hook', 2: 'Day 3: ROI Value Follow-Up', 3: 'Day 7: Break-Up Email' };
  if (countEl) countEl.innerHTML = `Showing <strong>\${filtered.length}</strong> Leads • Sequence: <span style="color:#fff;">\${stageNames[currentStageFilter]}</span>`;

  renderCRMStats();

  tbody.innerHTML = filtered.map(l => {
    let batchBadge = l.batch === 1 
      ? '<span style="background:rgba(124,92,252,0.18); color:#b794f4; padding:2px 8px; border-radius:4px; font-size:11px;">Batch 1: SMB</span>'
      : l.batch === 2
      ? '<span style="background:rgba(0,242,254,0.18); color:#00f2fe; padding:2px 8px; border-radius:4px; font-size:11px;">Batch 2: E-Com</span>'
      : '<span style="background:rgba(255,183,77,0.18); color:#ffb74d; padding:2px 8px; border-radius:4px; font-size:11px;">Batch 3: High-Ticket</span>';
      
    let slug = l.name.toLowerCase().replace(/ /g, '_').replace(/&/g, 'and').replace(/\\//g, '-').replace(/\\\\/g, '-').replace(/,/g, '').replace(/\\./g, '');
    let proposalLink = `proposals/\${slug}_proposal.html`;
    let pitchLink = `pitches/\${slug}_pitch.html`;
    let sandboxLink = `sandboxes/\${slug}_sandbox.html`;
    let agreementLink = `agreements/\${slug}_agreement.html`;
    let invoiceLink = `invoices/\${slug}_invoice.html`;
    let reportLink = `reports/\${slug}_roi_report.html`;
    let intakeLink = `https://work-minh-lap.vercel.app/onboarding?name=\${encodeURIComponent(l.name)}&niche=\${encodeURIComponent(l.niche)}`;
    
    let btnText = currentStageFilter === 1 ? '✉️ Send Day 1' : currentStageFilter === 2 ? '📈 Send Day 3' : '🚪 Send Day 7';
    let btnGradient = currentStageFilter === 1 
      ? 'linear-gradient(135deg,var(--accent),var(--cyan))' 
      : currentStageFilter === 2 
      ? 'linear-gradient(135deg,#00f2fe,#4facfe)' 
      : 'linear-gradient(135deg,#f5576c,#f093fb)';

    const st = getLeadStatus(l.id);

    return `
    <tr style="border-bottom:1px solid rgba(255,255,255,0.05); transition:background 0.15s;" onmouseover="this.style.background='rgba(255,255,255,0.02)'" onmouseout="this.style.background='transparent'">
      <td style="padding:12px 10px; color:var(--text-muted); font-family:var(--font-mono);">#\${l.id}</td>
      <td style="padding:12px 10px; font-weight:600; color:#fff;">
        \${l.name}
        <div style="margin-top:3px;">\${batchBadge}</div>
      </td>
      <td style="padding:12px 10px; color:var(--text-muted); font-size:12px;">\${l.niche} • <span style="color:var(--cyan);">\${l.city}</span></td>
      <td style="padding:12px 10px; text-align:center;">
        <select onchange="setLeadStatus(\${l.id}, this.value)" style="background:rgba(255,255,255,0.06); border:1px solid var(--border); color:#e2e8f0; border-radius:6px; padding:4px 6px; font-size:11px; cursor:pointer;">
          <option value="new" \${st === 'new' ? 'selected' : ''}>⚪ New</option>
          <option value="day1" \${st === 'day1' ? 'selected' : ''}>🎯 Day 1 Sent</option>
          <option value="day3" \${st === 'day3' ? 'selected' : ''}>📈 Day 3 Sent</option>
          <option value="day7" \${st === 'day7' ? 'selected' : ''}>🚪 Day 7 Sent</option>
          <option value="booked" \${st === 'booked' ? 'selected' : ''}>📞 Booked</option>
          <option value="won" \${st === 'won' ? 'selected' : ''}>🏆 Won ($1,200)</option>
        </select>
      </td>
      <td style="padding:10px 4px; text-align:center; white-space:nowrap;">
        <a href="\${proposalLink}" target="_blank" style="display:inline-block; background:rgba(255,255,255,0.06); border:1px solid var(--border); color:#cbd5e1; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; margin-right:2px; transition:all 0.15s;" onmouseover="this.style.borderColor='var(--cyan)'; this.style.color='#fff';" onmouseout="this.style.borderColor='var(--border)'; this.style.color='#cbd5e1';">📄 Proposal</a>
        <a href="\${pitchLink}" target="_blank" style="display:inline-block; background:rgba(244,63,94,0.12); border:1px solid rgba(244,63,94,0.3); color:#fb7185; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; margin-right:2px; transition:all 0.15s;" onmouseover="this.style.borderColor='#f43f5e'; this.style.color='#fff';" onmouseout="this.style.borderColor='rgba(244,63,94,0.3)'; this.style.color='#fb7185';">🎯 Pitch</a>
        <a href="\${sandboxLink}" target="_blank" style="display:inline-block; background:rgba(0,242,254,0.1); border:1px solid rgba(0,242,254,0.3); color:#00f2fe; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; margin-right:2px; transition:all 0.15s;" onmouseover="this.style.borderColor='#00f2fe'; this.style.color='#fff';" onmouseout="this.style.borderColor='rgba(0,242,254,0.3)'; this.style.color='#00f2fe';">🧪 Sandbox</a>
        <a href="\${agreementLink}" target="_blank" style="display:inline-block; background:rgba(124,92,252,0.12); border:1px solid rgba(124,92,252,0.3); color:#b794f4; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; margin-right:2px; transition:all 0.15s;" onmouseover="this.style.borderColor='#7c5cfc'; this.style.color='#fff';" onmouseout="this.style.borderColor='rgba(124,92,252,0.3)'; this.style.color='#b794f4';">📑 Contract</a>
        <a href="\${invoiceLink}" target="_blank" style="display:inline-block; background:rgba(16,185,129,0.12); border:1px solid rgba(16,185,129,0.3); color:#34d399; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; margin-right:2px; transition:all 0.15s;" onmouseover="this.style.borderColor='#10b981'; this.style.color='#fff';" onmouseout="this.style.borderColor='rgba(16,185,129,0.3)'; this.style.color='#34d399';">💳 Invoice</a>
        <a href="\${reportLink}" target="_blank" style="display:inline-block; background:rgba(255,183,77,0.12); border:1px solid rgba(255,183,77,0.3); color:#ffb74d; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; margin-right:2px; transition:all 0.15s;" onmouseover="this.style.borderColor='#ffb74d'; this.style.color='#fff';" onmouseout="this.style.borderColor='rgba(255,183,77,0.3)'; this.style.color='#ffb74d';">📊 ROI</a>
        <a href="\${intakeLink}" target="_blank" style="display:inline-block; background:rgba(236,72,153,0.12); border:1px solid rgba(236,72,153,0.3); color:#f472b6; text-decoration:none; padding:3px 5px; border-radius:5px; font-size:10.5px; font-weight:600; transition:all 0.15s;" onmouseover="this.style.borderColor='#ec4899'; this.style.color='#fff';" onmouseout="this.style.borderColor='rgba(236,72,153,0.3)'; this.style.color='#f472b6';">🚀 Intake</a>
      </td>
      <td style="padding:12px 10px; text-align:right;">
        <a href="\${buildMailto(l, currentStageFilter)}" onclick="handleLeadDispatch(\${l.id}, currentStageFilter)" style="display:inline-block; background:\${btnGradient}; color:#fff; text-decoration:none; padding:6px 14px; border-radius:6px; font-size:12px; font-weight:700; box-shadow: 0 2px 8px rgba(0,0,0,0.3); transition:transform 0.15s;" onmouseover="this.style.transform='scale(1.04)'" onmouseout="this.style.transform='none'">\${btnText}</a>
      </td>
    </tr>
  `}).join('');
}
window.addEventListener('DOMContentLoaded', renderLeadsTable);"""

def update_files():
    root = Path(__file__).resolve().parent.parent
    files = [root / "dashboard.html", root / "index.html"]
    
    for f in files:
        if not f.exists():
            continue
        content = f.read_text(encoding='utf-8')
        
        # 1. Replace the controls in direct-leads tab
        old_controls_start = '        <!-- Filter Pill Controls -->'
        old_controls_end = '        </div>\n        </div>'
        if old_controls_start in content:
            idx1 = content.find(old_controls_start)
            idx2 = content.find(old_controls_end, idx1) + len(old_controls_end)
            content = content[:idx1] + STAGE_CONTROLS_HTML + content[idx2:]
        elif '<!-- CRM Pipeline Stats Summary Bar -->' in content:
            pass # already replaced
            
        # 2. Update table header to include CRM Status column
        old_th = '<th style="padding:10px;">Target Email</th>'
        new_th = '<th style="padding:10px; text-align:center;">CRM Pipeline Status</th>'
        if old_th in content:
            content = content.replace(old_th, new_th)
            
        # 3. Replace LEADS_DATA and JS functions
        js_start = 'const LEADS_DATA = ['
        js_end = "window.addEventListener('DOMContentLoaded', renderLeadsTable);"
        if js_start in content and js_end in content:
            p1 = content.find(js_start)
            p2 = content.find(js_end) + len(js_end)
            content = content[:p1] + LEADS_DATA_JS + content[p2:]
            
        f.write_text(content, encoding='utf-8')
        print(f"[✓] Successfully updated {f.name} with CRM Pipeline tracking & LocalStorage state!")

if __name__ == "__main__":
    update_files()
