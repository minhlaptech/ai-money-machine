import crypto from 'crypto';

export default async function handler(req, res) {
  // Allow Lemon Squeezy webhooks
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Signature');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    let rawBody = req.body;
    let payload = req.body;
    if (typeof req.body === 'string') {
      try {
        payload = JSON.parse(req.body);
      } catch (e) {
        payload = {};
      }
    } else {
      rawBody = JSON.stringify(req.body);
    }

    const signature = req.headers['x-signature'];
    const secret = process.env.LEMON_SQUEEZY_WEBHOOK_SECRET || 'ls_whsec_f89a3c20d7e54b6183a9e2f41cb8d9e7';

    // Verify HMAC SHA-256 signature if secret is present
    if (secret && signature && typeof rawBody === 'string') {
      try {
        const hmac = crypto.createHmac('sha256', secret);
        const digest = Buffer.from(hmac.update(rawBody).digest('hex'), 'utf8');
        const signatureBuffer = Buffer.from(signature, 'utf8');
        if (digest.length !== signatureBuffer.length || !crypto.timingSafeEqual(digest, signatureBuffer)) {
          console.warn('[LemonSqueezy Webhook] Signature mismatch detected');
        }
      } catch (sigErr) {
        console.warn('[LemonSqueezy Webhook] Signature verification error:', sigErr);
      }
    }

    const eventName = payload?.meta?.event_name || 'order_created';
    const attributes = payload?.data?.attributes || {};
    const customerEmail = attributes.user_email || attributes.customer_email || 'Buyer';
    const totalFormatted = attributes.total_formatted || (attributes.total ? `$${(attributes.total / 100).toFixed(2)}` : '$19.00');
    const orderId = payload?.data?.id || 'N/A';
    const productName = attributes.first_order_item?.product_name || 'SynapseGEO Pro';

    const botToken = process.env.TELEGRAM_BOT_TOKEN || '7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU';
    const chatId = process.env.TELEGRAM_CHAT_ID || '1624883046';

    const now = new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' });
    const text = `💰 *[NEW LEMON SQUEEZY SALE!]*\n\n🎉 *Sự kiện:* \`${eventName}\`\n📦 *Sản phẩm:* *${productName}*\n💵 *Số tiền:* \`${totalFormatted}\`\n📧 *Khách hàng:* \`${customerEmail}\`\n🆔 *Order ID:* \`${orderId}\`\n⏰ *Thời gian:* ${now}\n\n🚀 _Cổng thanh toán tự động ghi nhận doanh thu thành công!_`;

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

    return res.status(200).json({ received: true, event: eventName });
  } catch (error) {
    console.error('Webhook processing error:', error);
    return res.status(500).json({ error: 'Internal server error' });
  }
}
