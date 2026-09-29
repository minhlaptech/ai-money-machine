/**
 * Serverless Telegram Lead Capture API
 * -------------------------------------
 * Endpoint: POST /api/contact
 * Handles inbound lead forms, onboarding submissions, and consultation requests.
 * Dispatches an instant high-priority alert directly to Telegram @Minhpv_bot.
 */

export default async function handler(req, res) {
  // Enable CORS for all frontends (work-minh-lap, ai-automation-guide-omega, etc.)
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {
        body = { message: body };
      }
    }

    const {
      name = 'Anonymous Prospect',
      email = 'N/A',
      phone = 'N/A',
      website = 'N/A',
      service = 'AI Consultation / Onboarding',
      source = 'Command Center / Webhook',
      calendar = 'N/A',
      escalation = 'N/A',
      ref = '',
      message = ''
    } = body || {};

    const botToken = process.env.TELEGRAM_BOT_TOKEN || '7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU';
    const chatId = process.env.TELEGRAM_CHAT_ID || '1624883046';

    const now = new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' });

    const sanitize = (str) => String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    const telegramText = `🔥 <b>[NEW INBOUND LEAD CAPTURED!]</b>\n\n` +
      `👤 <b>Khách hàng:</b> <code>${sanitize(name)}</code>\n` +
      `📧 <b>Email:</b> <code>${sanitize(email)}</code>\n` +
      `📞 <b>Số điện thoại:</b> <code>${sanitize(phone)}</code>\n` +
      `🌐 <b>Website:</b> ${sanitize(website)}\n` +
      `⚙️ <b>Dịch vụ quan tâm:</b> <b>${sanitize(service)}</b>\n` +
      `📍 <b>Nguồn (Source):</b> <i>${sanitize(source)}</i>\n` +
      (ref ? `🤝 <b>Đối tác giới thiệu (Partner Ref):</b> <code>${sanitize(ref)}</code> (20% RevShare: $300 - $700)\n` : '') +
      (calendar !== 'N/A' ? `📅 <b>Lịch hẹn:</b> ${sanitize(calendar)}\n` : '') +
      (escalation !== 'N/A' ? `🚨 <b>Khẩn cấp / SMS:</b> ${sanitize(escalation)}\n` : '') +
      (message ? `\n📝 <b>Chi tiết tin nhắn:</b>\n<i>${sanitize(message)}</i>\n` : '') +
      `\n⏰ <b>Thời gian:</b> ${now}\n` +
      `👉 <i>Phản hồi khách trong 5 phút để tối đa tỷ lệ chốt hợp đồng!</i>`;

    if (botToken && chatId) {
      const telegramUrl = `https://api.telegram.org/bot${botToken}/sendMessage`;
      await fetch(telegramUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: telegramText,
          parse_mode: 'HTML'
        })
      });
    }

    return res.status(200).json({
      success: true,
      message: 'Inquiry successfully received and routed to Telegram.',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('[API Contact Error]', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Internal server error'
    });
  }
}
