/**
 * MinhLap AI Money Machine — Universal Affiliate & Referral Attribution Tracker
 * -------------------------------------------------------------------------------
 * Tracks affiliate referral tags across all ecosystem pages, persists them
 * across 30 days via LocalStorage + Cookies, injects them into Lemon Squeezy checkout
 * URLs, and automatically appends them to lead capture forms and serverless APIs.
 *
 * Usage:
 * <script src="/ref-tracker.js" defer></script>
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'minhlap_ref';
  const COOKIE_KEY = 'minhlap_ref';
  const PARAM_KEYS = ['ref', 'aff', 'via', 'partner', 'r'];
  const COOKIE_MAX_AGE = 30 * 24 * 60 * 60; // 30 Days in seconds

  // 1. Helper to get cookie
  function getCookie(name) {
    const match = document.cookie.match(new RegExp('(^|;\\s*)(' + name + ')=([^;]*)'));
    return match ? decodeURIComponent(match[3]) : null;
  }

  // 2. Helper to set cookie
  function setCookie(name, value, seconds) {
    const expires = new Date(Date.now() + seconds * 1000).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
  }

  // 3. Extract referral code from URL query string
  function getRefFromUrl() {
    try {
      const params = new URLSearchParams(window.location.search);
      for (const key of PARAM_KEYS) {
        const val = params.get(key);
        if (val && val.trim().length > 0) {
          return val.trim().toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 32);
        }
      }
    } catch (e) {
      console.warn('[RefTracker] URL parsing error:', e);
    }
    return null;
  }

  // 4. Resolve Active Referral (URL takes precedence, then LocalStorage, then Cookie)
  const urlRef = getRefFromUrl();
  let activeRef = null;

  if (urlRef) {
    activeRef = urlRef;
    try {
      localStorage.setItem(STORAGE_KEY, urlRef);
      setCookie(COOKIE_KEY, urlRef, COOKIE_MAX_AGE);
    } catch (e) {
      // LocalStorage might be disabled in private mode
    }
  } else {
    try {
      activeRef = localStorage.getItem(STORAGE_KEY) || getCookie(COOKIE_KEY);
    } catch (e) {
      activeRef = getCookie(COOKIE_KEY);
    }
  }

  // Expose global attribution helper
  window.MinhLapPartner = {
    getRef: function () {
      return activeRef;
    },
    setRef: function (code) {
      activeRef = code;
      try {
        localStorage.setItem(STORAGE_KEY, code);
        setCookie(COOKIE_KEY, code, COOKIE_MAX_AGE);
      } catch (e) {}
      applyAttribution();
    }
  };

  // 5. Update Lemon Squeezy links with custom checkout parameters
  function patchLemonSqueezyLinks() {
    if (!activeRef) return;
    const links = document.querySelectorAll('a[href*="lemonsqueezy.com"]');
    links.forEach(function (link) {
      try {
        const href = link.getAttribute('href');
        if (!href) return;
        const url = new URL(href, window.location.origin);
        // Lemon Squeezy custom checkout payload
        url.searchParams.set('checkout[custom][ref]', activeRef);
        url.searchParams.set('checkout[custom][referral]', activeRef);
        link.setAttribute('href', url.toString());
      } catch (err) {
        // Fallback simple append
        if (!link.href.includes('checkout[custom][ref]')) {
          const sep = link.href.includes('?') ? '&' : '?';
          link.href += `${sep}checkout[custom][ref]=${encodeURIComponent(activeRef)}`;
        }
      }
    });
  }

  // 6. Inject hidden input into all forms for lead attribution
  function patchForms() {
    if (!activeRef) return;
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
      let refInput = form.querySelector('input[name="ref"], input[name="referral"]');
      if (refInput) {
        if (!refInput.value) refInput.value = activeRef;
      } else {
        refInput = document.createElement('input');
        refInput.type = 'hidden';
        refInput.name = 'ref';
        refInput.value = activeRef;
        form.appendChild(refInput);
      }
    });
  }

  // 7. Monkey-patch window.fetch to automatically append referral tag to lead/subscribe APIs
  function patchFetch() {
    if (!activeRef || typeof window.fetch !== 'function') return;
    const originalFetch = window.fetch;
    window.fetch = function (resource, options) {
      if (options && options.method && options.method.toUpperCase() === 'POST') {
        const urlStr = typeof resource === 'string' ? resource : resource?.url || '';
        if (
          urlStr.includes('/api/contact') ||
          urlStr.includes('/api/subscribe') ||
          urlStr.includes('/api/referral')
        ) {
          if (options.body && typeof options.body === 'string') {
            try {
              const parsed = JSON.parse(options.body);
              if (!parsed.ref) {
                parsed.ref = activeRef;
                options = Object.assign({}, options, {
                  body: JSON.stringify(parsed)
                });
              }
            } catch (e) {
              // Not valid JSON, leave as-is
            }
          }
        }
      }
      return originalFetch.apply(this, [resource, options]);
    };
  }

  // 8. Subtle badge notification if user arrived with active ref parameter
  function displayAffiliateNotice() {
    if (!urlRef) return;
    console.log(`%c[MinhLap Partner Network] Active Referral Code: ${urlRef} (Attribution Verified)`, 'background: #7c5cfc; color: #fff; padding: 4px 8px; border-radius: 4px; font-weight: bold;');
  }

  function applyAttribution() {
    if (!activeRef) return;
    patchLemonSqueezyLinks();
    patchForms();
    patchFetch();
  }

  // Execute upon DOM ready and after dynamic changes
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      applyAttribution();
      displayAffiliateNotice();
    });
  } else {
    applyAttribution();
    displayAffiliateNotice();
  }

  // Re-run periodically for single-page dynamic render updates
  setTimeout(applyAttribution, 1500);
  setTimeout(applyAttribution, 4000);
})();
