/**
 * ReviewGenius AI — Popup Controller & Generator Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // State
  let isProUser = false;
  let usageCount = 0;

  // DOM Elements
  const tierBadge = document.getElementById('tierBadge');
  const reviewInput = document.getElementById('reviewInput');
  const starRating = document.getElementById('starRating');
  const toneSelect = document.getElementById('toneSelect');
  const businessName = document.getElementById('businessName');
  const seoKeywords = document.getElementById('seoKeywords');
  const btnGenerate = document.getElementById('btnGenerate');
  const resultsSection = document.getElementById('resultsSection');
  const variationsContainer = document.getElementById('variationsContainer');
  const proCard = document.getElementById('proCard');
  const btnUpgrade = document.getElementById('btnUpgrade');
  const linkEnterKey = document.getElementById('linkEnterKey');
  const licenseModal = document.getElementById('licenseModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const licenseKeyInput = document.getElementById('licenseKeyInput');
  const btnActivateKey = document.getElementById('btnActivateKey');
  const licenseFeedback = document.getElementById('licenseFeedback');

  // Load Saved State
  initSettings();

  // Generate Responses
  btnGenerate.addEventListener('click', () => {
    executeGeneration();
  });

  // Upgrade Actions
  btnUpgrade.addEventListener('click', () => {
    window.open('https://minhlap.lemonsqueezy.com', '_blank');
  });

  linkEnterKey.addEventListener('click', (e) => {
    e.preventDefault();
    licenseModal.style.display = 'flex';
  });

  btnCloseModal.addEventListener('click', () => {
    licenseModal.style.display = 'none';
  });

  btnActivateKey.addEventListener('click', () => {
    activateLicense(licenseKeyInput.value.trim());
  });

  // --- Functions ---

  function initSettings() {
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.get(['isPro', 'licenseKey', 'usageCount', 'savedBizName', 'savedKeywords'], (res) => {
        if (res.isPro) {
          isProUser = true;
          tierBadge.textContent = 'PRO (UNLIMITED)';
          tierBadge.className = 'badge badge-pro';
          proCard.style.display = 'none';
        } else {
          usageCount = res.usageCount || 0;
          tierBadge.textContent = `FREE (${10 - usageCount}/10 LEFT)`;
        }

        if (res.savedBizName) businessName.value = res.savedBizName;
        if (res.savedKeywords) seoKeywords.value = res.savedKeywords;
      });
    }
  }

  function executeGeneration() {
    const review = reviewInput.value.trim();
    if (!review) {
      alert('Please paste a customer review first.');
      return;
    }

    if (!isProUser && usageCount >= 10) {
      alert('You have reached the 10 free responses limit for this month. Upgrade to Pro for unlimited responses!');
      licenseModal.style.display = 'flex';
      return;
    }

    btnGenerate.disabled = true;
    btnGenerate.innerHTML = '<span>⏳</span><span>Crafting SEO Responses...</span>';

    const stars = parseInt(starRating.value, 10);
    const tone = toneSelect.value;
    const biz = businessName.value.trim() || 'our team';
    const keywords = seoKeywords.value.trim();

    // Save preferences
    if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
      chrome.storage.local.set({
        savedBizName: businessName.value.trim(),
        savedKeywords: seoKeywords.value.trim()
      });
    }

    setTimeout(() => {
      const variations = generateReviewVariations(review, stars, tone, biz, keywords);
      renderVariations(variations);

      btnGenerate.disabled = false;
      btnGenerate.innerHTML = '<span>⚡ Generate 3 AI Responses</span>';

      if (!isProUser) {
        usageCount++;
        tierBadge.textContent = `FREE (${10 - usageCount}/10 LEFT)`;
        if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
          chrome.storage.local.set({ usageCount: usageCount });
        }
      }
    }, 400);
  }

  function generateReviewVariations(reviewText, stars, tone, bizName, keywords) {
    const kwPhrase = keywords ? ` for ${keywords}` : '';
    const isNegative = stars <= 2;

    if (isNegative) {
      return [
        {
          label: 'Option 1: Empathetic & Direct Resolution',
          text: `Dear Customer, thank you for sharing your candid feedback. At ${bizName}, we pride ourselves on delivering top-tier service${kwPhrase}, and we are genuinely sorry to hear that your experience fell short of our high standards. Please reach out to our management team directly so we can understand what occurred and make things right for you.`
        },
        {
          label: 'Option 2: Executive & Professional Apology',
          text: `Thank you for bringing this matter to our attention. Customer satisfaction is our utmost priority at ${bizName}. We are currently investigating the issue mentioned regarding your visit. We would welcome the opportunity to discuss your experience privately and earn back your trust.`
        },
        {
          label: 'Option 3: Constructive & Solution-Oriented',
          text: `Hello, we sincerely apologize for the frustration you experienced. We take all feedback seriously to continually elevate our quality${kwPhrase}. Our director would appreciate the chance to connect with you directly to rectify this situation immediately.`
        }
      ];
    } else if (stars === 3) {
      return [
        {
          label: 'Option 1: Balanced & Inquisitive',
          text: `Hi there, thank you for visiting ${bizName} and taking the time to leave a review. We are pleased you stopped by, but we always strive for a 5-star experience! We would love to know how we can make your next visit even better.`
        },
        {
          label: 'Option 2: Warm & Improvement-Focused',
          text: `Thank you for your feedback! Here at ${bizName}, our mission is to deliver the finest service${kwPhrase}. We appreciate your support and hope to deliver an exceptional 5-star visit next time!`
        },
        {
          label: 'Option 3: Courteous & Receptive',
          text: `Dear Guest, thank you for your honest feedback. We are always working on refining our offerings${kwPhrase}. If you have specific suggestions on how we can improve, please feel free to reach out to us directly.`
        }
      ];
    } else {
      // 4 or 5 stars
      return [
        {
          label: 'Option 1: Warm & Grateful (Highest Engagement)',
          text: `Thank you so much for the glowing 5-star review! The entire team at ${bizName} is thrilled to hear about your great experience. Providing exceptional quality${kwPhrase} is our passion. We look forward to welcoming you back again soon!`
        },
        {
          label: 'Option 2: Local SEO & Service Highlights',
          text: `We are truly grateful for your wonderful recommendation! Whether you need expert assistance${kwPhrase} or friendly service, ${bizName} is always dedicated to going above and beyond. See you again next time!`
        },
        {
          label: 'Option 3: Enthusiastic & Personal',
          text: `Wow, thank you for making our day with your kind words! Knowing that you had such a seamless experience at ${bizName} means the world to our staff. Have a fantastic week ahead and visit us again soon!`
        }
      ];
    }
  }

  function renderVariations(variations) {
    resultsSection.style.display = 'flex';
    variationsContainer.innerHTML = '';

    variations.forEach((v, index) => {
      const card = document.createElement('div');
      card.className = 'variation-card';

      const header = document.createElement('div');
      header.className = 'variation-header';

      const label = document.createElement('span');
      label.className = 'variation-label';
      label.textContent = v.label;

      const btnCopy = document.createElement('button');
      btnCopy.className = 'btn-copy-card';
      btnCopy.textContent = '📋 Copy';
      btnCopy.addEventListener('click', () => {
        navigator.clipboard.writeText(v.text);
        btnCopy.textContent = '✓ Copied!';
        setTimeout(() => { btnCopy.textContent = '📋 Copy'; }, 2000);
      });

      header.appendChild(label);
      header.appendChild(btnCopy);

      const pText = document.createElement('p');
      pText.className = 'variation-text';
      pText.textContent = v.text;

      card.appendChild(header);
      card.appendChild(pText);
      variationsContainer.appendChild(card);
    });
  }

  function activateLicense(key) {
    licenseFeedback.className = 'feedback-text';
    if (!key) {
      licenseFeedback.textContent = 'Please enter a license key.';
      licenseFeedback.className = 'feedback-text error';
      return;
    }

    const isValid = (key.toUpperCase().startsWith('REV-PRO-') && key.length >= 15) || (key.length >= 16 && !key.includes(' '));

    if (isValid) {
      if (typeof chrome !== 'undefined' && chrome.storage && chrome.storage.local) {
        chrome.storage.local.set({ isPro: true, licenseKey: key }, () => {
          licenseFeedback.textContent = '✓ Pro Lifetime License Activated!';
          licenseFeedback.className = 'feedback-text success';
          setTimeout(() => {
            licenseModal.style.display = 'none';
            initSettings();
          }, 1200);
        });
      }
    } else {
      licenseFeedback.textContent = 'Invalid license key format. Please check your purchase confirmation.';
      licenseFeedback.className = 'feedback-text error';
    }
  }
});
