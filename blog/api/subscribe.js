export default async function handler(req, res) {
  // Set CORS headers
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
        body = {};
      }
    }

    const email = body?.email ? String(body.email).trim() : '';
    if (!email || !email.includes('@')) {
      return res.status(400).json({ error: 'Invalid email address' });
    }

    const botToken = process.env.TELEGRAM_BOT_TOKEN || '7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU';
    const chatId = process.env.TELEGRAM_CHAT_ID || '1624883046';

    const now = new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' });
    const text = `🎉 *[NEW LEAD CAPTURED]*\n\n📧 *Khách hàng:* \`${email}\`\n⏰ *Thời gian:* ${now}\n🌐 *Trang:* ai-automation-guide-omega.vercel.app\n🎁 *Sản phẩm:* The AI Money Blueprint (Free Download)`;

    // Notify Telegram asynchronously
    if (botToken && chatId) {
      try {
        await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            chat_id: chatId,
            text: text,
            parse_mode: 'Markdown'
          })
        });
      } catch (tgErr) {
        console.error('Telegram notification error:', tgErr);
      }
    }

    return res.status(200).json({
      success: true,
      message: 'Subscription successful!',
      downloadUrl: '/downloads/The_AI_Money_Blueprint.pdf'
    });
  } catch (error) {
    console.error('Handler error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
