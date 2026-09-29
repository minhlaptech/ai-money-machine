/**
 * SynapseGEO Chrome Extension Popup Logic
 * Inspects active tab DOM for Schema JSON-LD, OpenGraph, and semantic tags.
 */

let currentTabUrl = '';

document.addEventListener('DOMContentLoaded', async () => {
  if (typeof chrome !== 'undefined' && chrome.tabs && chrome.tabs.query) {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab && tab.url) {
        currentTabUrl = tab.url;
        const parsed = new URL(tab.url);
        document.getElementById('tab-domain').textContent = parsed.hostname;

        // Execute scanner script inside active tab
        chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: scanPageDOM
        }, (results) => {
          if (results && results[0] && results[0].result) {
            updateUI(results[0].result);
          } else {
            fallbackScan(parsed.hostname);
          }
        });
        return;
      }
    } catch (e) {
      console.warn("Could not query active tab:", e);
    }
  }

  // Fallback for standalone preview
  document.getElementById('tab-domain').textContent = "demo-preview.com";
  fallbackScan("demo-preview.com");
});

function scanPageDOM() {
  const hasSchema = !!document.querySelector('script[type="application/ld+json"]');
  const hasOG = !!document.querySelector('meta[property="og:title"]') || !!document.querySelector('meta[property="og:description"]');
  const h1Elements = document.querySelectorAll('h1');
  const hasGoodH1 = h1Elements.length >= 1 && h1Elements.length <= 2;

  let score = 50;
  if (hasSchema) score += 30;
  if (hasOG) score += 10;
  if (hasGoodH1) score += 10;

  return {
    hasSchema,
    hasOG,
    hasGoodH1,
    score
  };
}

function updateUI(res) {
  const badge = document.getElementById('score-badge');
  badge.textContent = res.score;

  const scoreText = document.getElementById('score-text');
  if (res.score >= 80) {
    scoreText.textContent = "AI Search Ready";
  } else if (res.score >= 60) {
    scoreText.textContent = "Moderate Visibility";
  } else {
    scoreText.textContent = "Optimization Needed";
  }

  // Schema check
  const valSchema = document.getElementById('val-schema');
  valSchema.textContent = res.hasSchema ? "Detected (OK)" : "Missing (Critical)";
  valSchema.className = `check-val ${res.hasSchema ? 'val-good' : 'val-bad'}`;

  // OG check
  const valOG = document.getElementById('val-og');
  valOG.textContent = res.hasOG ? "Configured" : "Incomplete";
  valOG.className = `check-val ${res.hasOG ? 'val-good' : 'val-warn'}`;

  // H1 check
  const valH1 = document.getElementById('val-headers');
  valH1.textContent = res.hasGoodH1 ? "Optimal" : "Check hierarchy";
  valH1.className = `check-val ${res.hasGoodH1 ? 'val-good' : 'val-warn'}`;
}

function fallbackScan(domain) {
  updateUI({
    hasSchema: false,
    hasOG: true,
    hasGoodH1: true,
    score: 65
  });
}

function openWebApp() {
  const target = currentTabUrl ? `https://synapse-geo-audit.vercel.app/?inspect=${encodeURIComponent(currentTabUrl)}` : 'https://synapse-geo-audit.vercel.app/';
  if (typeof chrome !== 'undefined' && chrome.tabs && chrome.tabs.create) {
    chrome.tabs.create({ url: target });
  } else {
    window.open(target, '_blank');
  }
}
