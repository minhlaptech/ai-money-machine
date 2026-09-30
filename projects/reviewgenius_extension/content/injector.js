/**
 * ReviewGenius AI — Content Script Injector
 * Detects Google Reviews / Yelp / TripAdvisor response boxes and provides 1-click AI generation.
 */

(function () {
  const BUTTON_CLASS = 'review-genius-injected-btn';

  function initReviewObserver() {
    // Run initial scan
    scanAndInjectButtons();

    // Observe dynamic DOM changes for newly loaded reviews (pagination, infinite scroll)
    const observer = new MutationObserver(() => {
      scanAndInjectButtons();
    });

    observer.observe(document.body, { childList: true, subtree: true });
  }

  function scanAndInjectButtons() {
    // Target Google Business Profile and Google Search review reply dialogs/buttons
    const replyButtons = document.querySelectorAll('button[aria-label*="Reply"], button[aria-label*="Phản hồi"], [data-review-id] button, div[role="dialog"] textarea');

    replyButtons.forEach(target => {
      if (target.dataset.rgInjected) return;
      target.dataset.rgInjected = 'true';

      if (target.tagName === 'TEXTAREA') {
        injectAiHelperNearTextarea(target);
      }
    });
  }

  function injectAiHelperNearTextarea(textarea) {
    if (textarea.parentElement.querySelector(`.${BUTTON_CLASS}`)) return;

    const btn = document.createElement('button');
    btn.className = BUTTON_CLASS;
    btn.type = 'button';
    btn.innerHTML = '⚡ AI Smart Reply';
    btn.style.cssText = `
      background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%);
      color: #041021;
      font-weight: 700;
      font-size: 11px;
      padding: 5px 12px;
      border-radius: 6px;
      border: none;
      cursor: pointer;
      margin-top: 6px;
      margin-bottom: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3);
      z-index: 1000;
    `;

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();

      // Find review text in parent container
      const container = textarea.closest('div[role="dialog"], [data-review-id], div[class*="review"]') || document.body;
      const reviewTextElem = container.querySelector('[class*="review-text"], [data-expandable-section], span[dir="ltr"]') || container;
      const reviewText = reviewTextElem ? reviewTextElem.innerText.slice(0, 300) : '';

      // Generate context-aware response
      const response = generateSmartReply(reviewText);
      textarea.value = response;
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
      textarea.dispatchEvent(new Event('change', { bubbles: true }));
    });

    textarea.parentElement.insertBefore(btn, textarea);
  }

  function generateSmartReply(customerReview) {
    const isNegative = /bad|terrible|horrible|rude|slow|worst|dirty|broken|tệ|kém|chậm|dở|thất vọng/i.test(customerReview);
    
    if (isNegative) {
      return `Dear Valued Guest, thank you for bringing this to our attention. We take your feedback seriously and apologize that your experience did not meet our high standards. Please contact our management team directly so we can resolve this matter and make things right for you. We appreciate your patience.`;
    } else {
      return `Thank you so much for your wonderful review! We are delighted to hear that you had a great experience with our team. Providing top-quality service is our highest priority, and we look forward to welcoming you back soon!`;
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initReviewObserver);
  } else {
    initReviewObserver();
  }
})();
