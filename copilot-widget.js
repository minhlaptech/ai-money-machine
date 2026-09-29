/**
 * MinhLap AI Copilot — Turnkey Embeddable 24/7 Client Intake Widget
 * ------------------------------------------------------------------
 * Embeddable script that converts website visitors into booked clients.
 * Zero external dependencies. Self-contained Shadow DOM prevents CSS conflicts.
 *
 * Usage:
 * <script src="https://work-minh-lap.vercel.app/copilot-widget.js"
 *         data-business="Austin Dental Co"
 *         data-color="#7c5cfc"
 *         data-booking="https://chatbotdemo-hazel.vercel.app"
 *         async></script>
 */

(function () {
  if (window.__MINHLAP_COPILOT_LOADED__) return;
  window.__MINHLAP_COPILOT_LOADED__ = true;

  // Retrieve configuration from current script tag
  const currentScript = document.currentScript || (function () {
    const scripts = document.getElementsByTagName('script');
    return scripts[scripts.length - 1];
  })();

  const config = {
    business: currentScript?.getAttribute('data-business') || 'AI Assistant',
    color: currentScript?.getAttribute('data-color') || '#7c5cfc',
    bookingUrl: currentScript?.getAttribute('data-booking') || 'https://work-minh-lap.vercel.app/projects/ai_freelancing/portfolio/demo_chatbot.html',
    endpoint: currentScript?.getAttribute('data-endpoint') || 'https://work-minh-lap.vercel.app/api/contact',
    greeting: currentScript?.getAttribute('data-greeting') || 'Hi there! 👋 How can I help you today? Feel free to ask about our services, pricing, or book an appointment.'
  };

  // Host container
  const host = document.createElement('div');
  host.id = 'minhlap-copilot-container';
  document.body.appendChild(host);

  // Attach Shadow DOM to insulate styles
  const shadow = host.attachShadow({ mode: 'open' });

  // Widget Styles
  const style = document.createElement('style');
  style.textContent = `
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
    
    .copilot-bubble {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 30px;
      background: linear-gradient(135deg, ${config.color}, #00f2fe);
      box-shadow: 0 8px 24px rgba(0,0,0,0.3), 0 0 16px rgba(124,92,252,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 999999;
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .copilot-bubble:hover {
      transform: scale(1.08);
    }
    .copilot-bubble svg {
      width: 28px;
      height: 28px;
      fill: #ffffff;
    }
    .pulse-dot {
      position: absolute;
      top: 2px;
      right: 2px;
      width: 14px;
      height: 14px;
      background: #10b981;
      border: 2px solid #070714;
      border-radius: 7px;
    }

    .copilot-window {
      position: fixed;
      bottom: 96px;
      right: 24px;
      width: 380px;
      max-width: calc(100vw - 32px);
      height: 540px;
      max-height: calc(100vh - 120px);
      background: #0d0d21;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 20px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.6), 0 0 30px rgba(124,92,252,0.25);
      z-index: 999999;
      display: none;
      flex-direction: column;
      overflow: hidden;
      backdrop-filter: blur(16px);
      animation: slideUp 0.25s ease-out forwards;
    }
    .copilot-window.open {
      display: flex;
    }

    @keyframes slideUp {
      from { opacity: 0; transform: translateY(16px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .chat-header {
      background: rgba(255,255,255,0.03);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      padding: 16px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .chat-header-title {
      font-size: 15px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .chat-header-sub {
      font-size: 11px;
      color: #34d399;
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 2px;
    }
    .chat-close-btn {
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 20px;
      cursor: pointer;
      line-height: 1;
      padding: 4px;
    }
    .chat-close-btn:hover { color: #fff; }

    .chat-body {
      flex: 1;
      padding: 16px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .msg {
      max-width: 85%;
      padding: 10px 14px;
      border-radius: 14px;
      font-size: 13.5px;
      line-height: 1.45;
      word-wrap: break-word;
    }
    .msg-bot {
      align-self: flex-start;
      background: rgba(255,255,255,0.06);
      border: 1px solid rgba(255,255,255,0.08);
      color: #e2e8f0;
      border-bottom-left-radius: 4px;
    }
    .msg-user {
      align-self: flex-end;
      background: linear-gradient(135deg, ${config.color}, #00f2fe);
      color: #ffffff;
      border-bottom-right-radius: 4px;
      font-weight: 500;
    }

    .chips-container {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 4px;
    }
    .chip-btn {
      background: rgba(124,92,252,0.12);
      border: 1px solid rgba(124,92,252,0.3);
      color: #b794f4;
      font-size: 11.5px;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 16px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .chip-btn:hover {
      background: ${config.color};
      color: #fff;
      border-color: ${config.color};
    }

    .chat-footer {
      padding: 12px 16px;
      border-top: 1px solid rgba(255,255,255,0.08);
      background: rgba(0,0,0,0.25);
      display: flex;
      gap: 8px;
    }
    .chat-input {
      flex: 1;
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 20px;
      padding: 10px 16px;
      font-size: 13px;
      color: #fff;
      outline: none;
    }
    .chat-input:focus {
      border-color: #00f2fe;
    }
    .chat-send-btn {
      width: 38px;
      height: 38px;
      border-radius: 19px;
      background: linear-gradient(135deg, ${config.color}, #00f2fe);
      border: none;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.15s;
    }
    .chat-send-btn:hover {
      transform: scale(1.05);
    }
    .chat-send-btn svg {
      width: 16px;
      height: 16px;
      fill: #fff;
    }
    .branding-sub {
      text-align: center;
      font-size: 10px;
      color: #64748b;
      padding-bottom: 6px;
    }
    .branding-sub a {
      color: #94a3b8;
      text-decoration: none;
    }
  `;

  shadow.appendChild(style);

  // Widget HTML structure
  const rootDiv = document.createElement('div');
  rootDiv.innerHTML = `
    <!-- Floating Launcher -->
    <div class="copilot-bubble" id="copilot-launcher" title="Chat with ${config.business}">
      <svg viewBox="0 0 24 24">
        <path d="M12 2C6.477 2 2 6.477 2 12c0 1.821.487 3.53 1.338 5L2.5 21.5l4.636-.838A9.957 9.957 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18c-1.612 0-3.118-.455-4.405-1.242l-.316-.194-2.735.494.494-2.735-.194-.316A7.954 7.954 0 014 12c0-4.411 3.589-8 8-8s8 3.589 8 8-3.589 8-8 8z"/>
      </svg>
      <div class="pulse-dot"></div>
    </div>

    <!-- Chat Modal Window -->
    <div class="copilot-window" id="copilot-modal">
      <div class="chat-header">
        <div>
          <div class="chat-header-title">
            <span>✨</span> ${config.business}
          </div>
          <div class="chat-header-sub">
            <span style="display:inline-block; width:6px; height:6px; background:#10b981; border-radius:3px;"></span>
            Online 24/7 • Instant Response
          </div>
        </div>
        <button class="chat-close-btn" id="copilot-close">✕</button>
      </div>

      <div class="chat-body" id="copilot-messages">
        <div class="msg msg-bot">${config.greeting}</div>
        <div class="chips-container" id="copilot-chips">
          <button class="chip-btn" data-action="book">📅 Book Appointment</button>
          <button class="chip-btn" data-action="pricing">💰 Pricing & Services</button>
          <button class="chip-btn" data-action="urgent">🚨 Urgent Request</button>
          <button class="chip-btn" data-action="human">📞 Callback Request</button>
        </div>
      </div>

      <div class="chat-footer">
        <input type="text" class="chat-input" id="copilot-input" placeholder="Type your message or phone number..." />
        <button class="chat-send-btn" id="copilot-send">
          <svg viewBox="0 0 24 24">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </div>
      <div class="branding-sub">
        Powered by <a href="https://work-minh-lap.vercel.app" target="_blank">MinhLap AI Systems</a>
      </div>
    </div>
  `;

  shadow.appendChild(rootDiv);

  // Widget Logic & State
  const launcher = shadow.getElementById('copilot-launcher');
  const modal = shadow.getElementById('copilot-modal');
  const closeBtn = shadow.getElementById('copilot-close');
  const msgContainer = shadow.getElementById('copilot-messages');
  const inputEl = shadow.getElementById('copilot-input');
  const sendBtn = shadow.getElementById('copilot-send');
  const chipsContainer = shadow.getElementById('copilot-chips');

  let leadState = { step: 'idle', name: '', contact: '', note: '' };

  launcher.addEventListener('click', () => {
    modal.classList.toggle('open');
    if (modal.classList.contains('open')) {
      inputEl.focus();
    }
  });

  closeBtn.addEventListener('click', () => modal.classList.remove('open'));

  function addMsg(text, type = 'bot') {
    const el = document.createElement('div');
    el.className = `msg msg-${type}`;
    el.innerHTML = text;
    msgContainer.appendChild(el);
    msgContainer.scrollTop = msgContainer.scrollHeight;
  }

  function dispatchLeadToBackend(lead) {
    fetch(config.endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: lead.name || 'Website Visitor',
        email: lead.contact.includes('@') ? lead.contact : 'N/A',
        phone: !lead.contact.includes('@') ? lead.contact : 'N/A',
        website: window.location.href,
        service: 'Inbound Webhook Inquiry',
        source: `Copilot Widget: ${config.business}`,
        message: lead.note || 'Client requested intake callback via copilot widget.'
      })
    }).catch(err => console.log('Lead notification sent silently.'));
  }

  function handleUserMessage(text) {
    if (!text.trim()) return;
    addMsg(text, 'user');
    inputEl.value = '';

    // Simple conversational intake engine
    setTimeout(() => {
      const lower = text.toLowerCase();

      if (leadState.step === 'ask_contact') {
        leadState.contact = text;
        leadState.step = 'completed';
        addMsg(`🎉 Perfect! I have recorded your contact: <strong>${text}</strong>. A staff member will confirm your requested slot within 15 minutes.<br><br>👉 Need immediate self-service booking? <a href="${config.bookingUrl}" target="_blank" style="color:#00f2fe; font-weight:700;">Click Here to Open Calendar</a>.`);
        dispatchLeadToBackend(leadState);
        return;
      }

      if (leadState.step === 'ask_name') {
        leadState.name = text;
        leadState.step = 'ask_contact';
        addMsg(`Nice to meet you, ${text}! What is the best phone number or email address to confirm your booking?`);
        return;
      }

      if (lower.includes('book') || lower.includes('appointment') || lower.includes('schedule') || lower.includes('lịch')) {
        leadState.step = 'ask_name';
        leadState.note = text;
        addMsg("I would be delighted to help reserve your priority booking. What is your full name?");
      } else if (lower.includes('price') || lower.includes('cost') || lower.includes('fee') || lower.includes('giá')) {
        addMsg(`Our service consultations start with a full diagnostic evaluation. What treatment or service are you interested in so I can provide the accurate quote range?`);
      } else if (lower.includes('urgent') || lower.includes('pain') || lower.includes('emergency') || lower.includes('khẩn')) {
        leadState.step = 'ask_contact';
        leadState.note = `[URGENT REQUEST] ${text}`;
        addMsg("🚨 I am prioritizing your message. Please share your phone number right now so our on-call specialist can reach out immediately.");
      } else {
        addMsg(`Thank you for reaching out to <strong>${config.business}</strong>. Would you like to schedule an appointment or have our front desk call you back?`);
      }
    }, 450);
  }

  // Handle Quick Chips
  chipsContainer.addEventListener('click', (e) => {
    const btn = e.target.closest('.chip-btn');
    if (!btn) return;
    const action = btn.getAttribute('data-action');
    if (action === 'book') {
      handleUserMessage("I would like to book an appointment.");
    } else if (action === 'pricing') {
      handleUserMessage("Can you share pricing and service details?");
    } else if (action === 'urgent') {
      handleUserMessage("I have an urgent request.");
    } else if (action === 'human') {
      handleUserMessage("Can someone please give me a callback?");
    }
  });

  sendBtn.addEventListener('click', () => handleUserMessage(inputEl.value));
  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') handleUserMessage(inputEl.value);
  });
})();
