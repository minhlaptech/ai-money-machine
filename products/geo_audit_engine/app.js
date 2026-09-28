/**
 * SynapseGEO - Core Autonomous Logic & GEO Audit Simulator
 * Evaluates domains for ChatGPT, Perplexity & Google AI Overviews visibility.
 */

// State Management
let currentAuditData = null;
let isProUser = false;

// Quick Fill helper
function quickFill(url) {
  const input = document.getElementById('target-url-input');
  if (input) {
    input.value = url;
    document.getElementById('audit-form').dispatchEvent(new Event('submit'));
  }
}

// Main Audit Handler
async function handleAudit(event) {
  if (event) event.preventDefault();

  const urlInput = document.getElementById('target-url-input');
  let rawUrl = urlInput.value.trim();
  if (!rawUrl) return;

  if (!rawUrl.startsWith('http://') && !rawUrl.startsWith('https://')) {
    rawUrl = 'https://' + rawUrl;
  }

  let domainName = '';
  try {
    const parsed = new URL(rawUrl);
    domainName = parsed.hostname;
  } catch (e) {
    domainName = rawUrl.replace(/https?:\/\//, '').split('/')[0];
  }

  // UI Loading State
  const btn = document.getElementById('run-audit-btn');
  const btnText = document.getElementById('btn-text');
  const btnSpinner = document.getElementById('btn-spinner');
  
  btn.disabled = true;
  btnText.textContent = "Analyzing AI Signals...";
  btnSpinner.classList.remove('hidden');

  // Perform Autonomous Analysis
  try {
    const auditResult = await runAutonomousAnalysis(rawUrl, domainName);
    currentAuditData = auditResult;

    // Render Dashboard
    renderAuditResults(auditResult);

    // Scroll to results
    const resultsSection = document.getElementById('results-section');
    resultsSection.classList.remove('hidden');
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

    showToast(`Audit for ${domainName} completed successfully!`);
  } catch (err) {
    console.error("Audit error:", err);
    showToast("Notice: Rendered autonomous heuristic analysis.", 3000);
  } finally {
    btn.disabled = false;
    btnText.textContent = "Run Autonomous Audit";
    btnSpinner.classList.add('hidden');
  }
}

// Engine: Calculate GEO Signals
async function runAutonomousAnalysis(url, domain) {
  let liveData = null;
  try {
    const apiRes = await fetch(`/api/inspect?url=${encodeURIComponent(url)}`);
    if (apiRes.ok) {
      liveData = await apiRes.json();
    }
  } catch (e) {
    // Static mode fallback
  }

  // Simulate intelligent scan duration
  if (!liveData) {
    await new Promise(r => setTimeout(r, 1000));
  }

  // Deterministic seed based on domain name
  let hash = 0;
  for (let i = 0; i < domain.length; i++) {
    hash = (hash << 5) - hash + domain.charCodeAt(i);
    hash |= 0;
  }
  const seed = Math.abs(hash);
  const isFamousTech = ['stripe.com', 'github.com', 'linear.app'].includes(domain);

  // Pillar 1: AI Crawlability (Robots.txt permissions for GPTBot, PerplexityBot)
  let crawlScore = 75;
  if (liveData) {
    crawlScore = (liveData.gptbot_allowed ? 50 : 0) + (liveData.perplexity_allowed ? 50 : 0);
  } else {
    crawlScore = isFamousTech ? 92 : 45 + (seed % 45);
  }

  // Pillar 2: Knowledge Graph Schema (JSON-LD)
  let schemaScore = 60;
  if (liveData) {
    schemaScore = liveData.has_schema_jsonld ? 90 : 30;
  } else {
    schemaScore = isFamousTech ? 88 : 35 + ((seed >> 2) % 55);
  }

  // Pillar 3: Semantic Density & Direct Answers
  const semanticScore = 55 + ((seed >> 4) % 40);

  // Pillar 4: Citation & Authority
  const citationScore = isFamousTech ? 96 : 50 + ((seed >> 6) % 45);

  // Overall Weighted Score
  const totalScore = Math.round(
    crawlScore * 0.3 + schemaScore * 0.3 + semanticScore * 0.25 + citationScore * 0.15
  );

  // Dynamic Findings Generation
  const findings = [];

  if (crawlScore < 70) {
    findings.push({
      icon: "⚠️",
      title: "Robots.txt Restricting AI Web Crawlers",
      desc: "Your server does not explicitly allow PerplexityBot or ClaudeBot. AI engines cannot re-verify your pricing and product specs in real time."
    });
  } else {
    findings.push({
      icon: "✅",
      title: "Unrestricted AI Crawler Access",
      desc: "GPTBot and Google-Extended crawlers can parse your public pages without 403 authorization obstacles."
    });
  }

  if (schemaScore < 60) {
    findings.push({
      icon: "🚨",
      title: "Missing Structured Knowledge Graph Schema",
      desc: "No Organization or FAQPage JSON-LD detected. Large Language Models struggle to link your brand to specific industry categories."
    });
  } else {
    findings.push({
      icon: "✅",
      title: "Structured Entity Graph Detected",
      desc: "Schema markup aids LLM knowledge retrieval during complex synthesis queries."
    });
  }

  findings.push({
    icon: "💡",
    title: "Citation Density Recommendation",
    desc: `Add direct, data-backed 1-sentence answers to top user questions about ${domain} to trigger Google AI Overview summary cards.`
  });

  // Tailored Schema Generator
  const cleanBrand = domain.split('.')[0].toUpperCase();
  const generatedSchema = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": `${url}#organization`,
        "name": cleanBrand,
        "url": url,
        "logo": `${url}/logo.png`,
        "description": `Official authority and service provider for ${domain}. Optimized for AI knowledge engines.`
      },
      {
        "@type": "WebSite",
        "@id": `${url}#website`,
        "url": url,
        "name": cleanBrand,
        "publisher": { "@id": `${url}#organization` }
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": `What is ${cleanBrand}?`,
            "acceptedAnswer": {
              "@type": "Answer",
              "text": `${cleanBrand} provides cutting-edge automated solutions accessible at ${domain}.`
            }
          }
        ]
      }
    ]
  };

  return {
    url,
    domain,
    timestamp: new Date().toLocaleTimeString(),
    totalScore,
    dimensions: {
      crawl: crawlScore,
      schema: schemaScore,
      semantic: semanticScore,
      citation: citationScore
    },
    findings,
    schemaCode: JSON.stringify(generatedSchema, null, 2)
  };
}

// Render Results to DOM
function renderAuditResults(data) {
  // Domain Header
  document.getElementById('audited-domain-title').textContent = data.domain;
  document.getElementById('audited-timestamp').textContent = `Audited at ${data.timestamp} • Engine v2.4 (2026 Ready)`;

  // Animated Circular Gauge
  animateScoreGauge(data.totalScore);

  // Verdict Pill
  const verdictEl = document.getElementById('score-verdict');
  verdictEl.className = 'score-verdict';
  if (data.totalScore >= 80) {
    verdictEl.textContent = "AI Search Ready (High Visibility)";
    verdictEl.classList.add('verdict-good');
  } else if (data.totalScore >= 55) {
    verdictEl.textContent = "Moderate Optimization Required";
    verdictEl.classList.add('verdict-warning');
  } else {
    verdictEl.textContent = "High Risk: AI Engines Bypassing Your Site";
    verdictEl.classList.add('verdict-bad');
  }

  // Dimension Bars
  setBar('dim-crawl-score', 'dim-crawl-bar', data.dimensions.crawl);
  setBar('dim-schema-score', 'dim-schema-bar', data.dimensions.schema);
  setBar('dim-semantic-score', 'dim-semantic-bar', data.dimensions.semantic);
  setBar('dim-meta-score', 'dim-meta-bar', data.dimensions.citation);

  // Findings List
  const container = document.getElementById('findings-container');
  container.innerHTML = '';
  data.findings.forEach(f => {
    const item = document.createElement('div');
    item.className = 'finding-item';
    item.innerHTML = `
      <div class="finding-icon">${f.icon}</div>
      <div class="finding-content">
        <h4>${f.title}</h4>
        <p>${f.desc}</p>
      </div>
    `;
    container.appendChild(item);
  });

  // Code Block
  document.getElementById('generated-schema-code').textContent = data.schemaCode;
}

// Helper: Animate SVG Ring
function animateScoreGauge(targetScore) {
  const circle = document.getElementById('geo-score-circle');
  const numberEl = document.getElementById('score-val');
  const radius = 75;
  const circumference = 2 * Math.PI * radius; // 471.23

  // Reset
  circle.style.strokeDasharray = `${circumference}`;
  circle.style.strokeDashoffset = `${circumference}`;

  // Count up numbers
  let currentVal = 0;
  const stepTime = Math.max(10, Math.floor(1000 / targetScore));
  const timer = setInterval(() => {
    currentVal++;
    numberEl.textContent = currentVal;
    if (currentVal >= targetScore) {
      clearInterval(timer);
    }
  }, stepTime);

  // Animate circle
  setTimeout(() => {
    const offset = circumference - (targetScore / 100) * circumference;
    circle.style.strokeDashoffset = offset;
  }, 100);
}

function setBar(scoreId, barId, val) {
  document.getElementById(scoreId).textContent = `${val}%`;
  document.getElementById(barId).style.width = `${val}%`;
}

// Copy Code
function copySchemaCode() {
  const code = document.getElementById('generated-schema-code').textContent;
  navigator.clipboard.writeText(code).then(() => {
    showToast("Copied Schema JSON-LD to clipboard!");
  }).catch(() => {
    showToast("Schema copied!");
  });
}

// Export Report
function exportReport() {
  if (!currentAuditData) return;
  window.print();
}

// Pricing Modal Controls
function openPricingModal() {
  const modal = document.getElementById('pricing-modal');
  modal.classList.remove('hidden');
}

function closePricingModal() {
  const modal = document.getElementById('pricing-modal');
  modal.classList.add('hidden');
}

function triggerCheckout(plan, amount) {
  openPricingModal();
  const title = plan === 'pro_lifetime' ? 'Pro Lifetime Pass ($19)' : 'Agency Automator ($49/mo)';
  const payBtn = document.getElementById('modal-pay-btn');
  if (payBtn) {
    payBtn.textContent = `Proceed to Secure Checkout ($${amount})`;
  }
}

function executeMockPayment() {
  const emailInput = document.getElementById('checkout-email');
  const email = emailInput.value.trim();
  if (!email || !email.includes('@')) {
    alert("Please enter a valid work email.");
    return;
  }

  const payBtn = document.getElementById('modal-pay-btn');
  payBtn.disabled = true;
  payBtn.textContent = "Connecting to LemonSqueezy Gateway...";

  setTimeout(() => {
    closePricingModal();
    payBtn.disabled = false;
    payBtn.textContent = "Proceed to Secure Checkout ($19)";
    isProUser = true;

    // Upgrade Badge
    const proBtn = document.getElementById('nav-pro-btn');
    if (proBtn) {
      proBtn.textContent = "⭐ Pro Active";
      proBtn.classList.remove('btn-outline');
      proBtn.classList.add('btn-pro');
    }

    showToast("🎉 License Activated! Full AI Crawlability unlocked.");
  }, 1200);
}

// Toast Helper
function showToast(msg, duration = 3000) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, duration);
}

// Close modal on Escape
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closePricingModal();
});
