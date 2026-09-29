/**
 * Serverless Newsletter & Lead Magnet Subscription API
 * -----------------------------------------------------
 * Endpoint: POST /api/subscribe
 * Captures email subscribers from the AI Automation Blog and Resource Hub.
 * Dispatches an instant notification to Telegram @Minhpv_bot and delivers
 * the download URL for 'The AI Money Blueprint' PDF.
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

    const email = body?.email ? String(body.email).trim() : '';
    const ref = body?.ref ? String(body.ref).trim() : '';
    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Invalid email address' });
    }

    const botToken = process.env.TELEGRAM_BOT_TOKEN || '7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU';
    const chatId = process.env.TELEGRAM_CHAT_ID || '1624883046';

    const now = new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' });
    const text = `🎉 <b>[NEW LEAD MAGNET SUBSCRIBER]</b>\n\n` +
      `📧 <b>Email:</b> <code>${email}</code>\n` +
      (ref ? `🤝 <b>Đối tác giới thiệu (Partner Ref):</b> <code>${ref}</code>\n` : '') +
      `⏰ <b>Thời gian:</b> ${now}\n` +
      `🌐 <b>Nguồn:</b> AI Automation Resource Hub (work-minh-lap.vercel.app)\n` +
      `🎁 <b>Sản phẩm đã cấp:</b> The AI Money Blueprint (Free 16K-word PDF Guide)\n\n` +
      `👉 <i>Lead đã được ghi nhận tự động vào phễu Email Nurture!</i>`;

    if (botToken && chatId) {
      try {
        await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: chatId,
            text: text,
            parse_mode: 'HTML'
          })
        });
      } catch (tgErr) {
        console.error('Telegram notification error:', tgErr);
      }
    }

    return res.status(200).json({
      success: true,
      message: 'Subscription successful! Your guide is ready.',
      downloadUrl: '/downloads/The_AI_Money_Blueprint.pdf'
    });
  } catch (error) {
    console.error('Subscribe handler error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
