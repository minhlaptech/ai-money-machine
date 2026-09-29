/**
 * Serverless Affiliate & Partner Onboarding API
 * -----------------------------------------------
 * Endpoint: POST /api/referral
 * Enrolls new affiliate partners into the MinhLap Systems AI Ecosystem.
 * Dispatches an instant high-priority partner notification to Telegram @Minhpv_bot.
 */

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST.' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {
        body = {};
      }
    }

    const {
      name = 'Anonymous Partner',
      email = '',
      social_url = 'N/A',
      niche = 'AI & Tech',
      audience_size = '1k - 5k',
      payout_method = 'Wise / PayPal',
      referral_tag = ''
    } = body || {};

    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'A valid email address is required.' });
    }

    const cleanTag = (referral_tag || name.toLowerCase().replace(/[^a-z0-9]/g, '') || 'partner').slice(0, 20);
    const botToken = process.env.TELEGRAM_BOT_TOKEN || '7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU';
    const chatId = process.env.TELEGRAM_CHAT_ID || '1624883046';

    const sanitize = (str) => String(str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    const now = new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' });

    const telegramText = `🤝 <b>[NEW AFFILIATE PARTNER ENROLLED! 🚀]</b>\n\n` +
      `👤 <b>Họ tên đối tác:</b> <code>${sanitize(name)}</code>\n` +
      `📧 <b>Email:</b> <code>${sanitize(email)}</code>\n` +
      `🌐 <b>Kênh / Profile:</b> ${sanitize(social_url)}\n` +
      `🎯 <b>Ngách & Tệp khách:</b> <b>${sanitize(niche)}</b> (${sanitize(audience_size)})\n` +
      `💳 <b>Kênh nhận hoa hồng:</b> <code>${sanitize(payout_method)}</code>\n` +
      `🏷️ <b>Mã Ref được cấp:</b> <code>${cleanTag}</code>\n` +
      `⏰ <b>Thời gian:</b> ${now}\n\n` +
      `🔗 <b>Link tiếp thị đã kích hoạt:</b>\n` +
      `https://work-minh-lap.vercel.app/bundle?ref=${cleanTag}\n\n` +
      `👉 <i>Đối tác đã được phê duyệt tự động. Hoa hồng chia sẻ 20% - 50%!</i>`;

    if (botToken && chatId) {
      try {
        await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: chatId,
            text: telegramText,
            parse_mode: 'HTML'
          })
        });
      } catch (tgErr) {
        console.error('Telegram notification error:', tgErr);
      }
    }

    return res.status(200).json({
      success: true,
      message: 'Affiliate partner successfully enrolled and verified.',
      partner: {
        name,
        email,
        referral_tag: cleanTag,
        custom_links: {
          master_bundle: `https://work-minh-lap.vercel.app/bundle?ref=${cleanTag}`,
          synapse_geo: `https://work-minh-lap.vercel.app/synapsegeo?ref=${cleanTag}`,
          roi_calculator: `https://work-minh-lap.vercel.app/calculator?ref=${cleanTag}`,
          resource_hub: `https://work-minh-lap.vercel.app/blog?ref=${cleanTag}`
        }
      },
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('[API Referral Error]', error);
    return res.status(500).json({ error: error.message || 'Internal server error' });
  }
}
