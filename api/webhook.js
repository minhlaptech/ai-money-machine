/**
 * Serverless Multi-Platform Payment & Order Webhook Dispatcher
 * -------------------------------------------------------------
 * Endpoint: POST /api/webhook
 * Integrates: Lemon Squeezy, Gumroad, Stripe, and Direct Inbound Payments.
 * Actions:
 *  1. Parses order/subscription payload.
 *  2. Dispatches real-time VIP sale alert directly to Telegram @Minhpv_bot.
 *  3. Resolves automated digital product download / onboarding URLs.
 *  4. Returns instant JSON receipt & fulfillment confirmation.
 */

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, X-Signature, X-Event-Name');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed. Use POST for webhook ingestion.' });
  }

  try {
    let body = req.body;
    if (typeof body === 'string') {
      try {
        body = JSON.parse(body);
      } catch (e) {
        body = { raw: body };
      }
    }

    const headers = req.headers || {};
    let platform = 'Generic / Direct Checkout';
    let eventName = 'order_created';
    let customerName = 'Valued Customer';
    let customerEmail = 'customer@example.com';
    let productName = 'AI Digital Asset Bundle';
    let amountStr = '$47.00';
    let orderId = `ORD-${Date.now().toString().slice(-6)}`;

    // 1. Detect Lemon Squeezy Webhook
    if (headers['x-event-name'] || (body.meta && body.meta.event_name)) {
      platform = 'Lemon Squeezy';
      eventName = headers['x-event-name'] || body.meta.event_name;
      const dataAttr = (body.data && body.data.attributes) || {};
      
      customerName = dataAttr.user_name || dataAttr.customer_name || 'Lemon Squeezy Buyer';
      customerEmail = dataAttr.user_email || dataAttr.customer_email || 'N/A';
      productName = dataAttr.first_order_item?.product_name || dataAttr.order_item?.product_name || 'AI Software / Guide';
      
      if (dataAttr.total_formatted) {
        amountStr = dataAttr.total_formatted;
      } else if (dataAttr.total) {
        amountStr = `$${(dataAttr.total / 100).toFixed(2)}`;
      }
      orderId = dataAttr.identifier || dataAttr.order_number || body.data?.id || orderId;
    }
    // 2. Detect Gumroad Webhook
    else if (body.seller_id || body.permalink) {
      platform = 'Gumroad';
      eventName = 'sale';
      customerName = body.full_name || body.name || 'Gumroad Customer';
      customerEmail = body.email || 'N/A';
      productName = body.product_name || 'Gumroad AI Product';
      amountStr = body.price ? `$${(body.price / 100).toFixed(2)}` : '$27.00';
      orderId = body.order_number || orderId;
    }
    // 3. Detect Stripe Webhook
    else if (body.type && body.type.startsWith('checkout.')) {
      platform = 'Stripe';
      eventName = body.type;
      const obj = body.data?.object || {};
      customerName = obj.customer_details?.name || 'Stripe Customer';
      customerEmail = obj.customer_details?.email || 'N/A';
      productName = obj.metadata?.product_name || 'AI Money Machine Solution';
      amountStr = obj.amount_total ? `$${(obj.amount_total / 100).toFixed(2)}` : '$1,850.00';
      orderId = obj.id || orderId;
    }
    // 4. Custom Simulation or Generic Form
    else if (body.customer_email || body.email) {
      platform = body.platform || 'Direct Checkout Portal';
      eventName = body.event || 'payment_confirmed';
      customerName = body.customer_name || body.name || 'Direct Buyer';
      customerEmail = body.customer_email || body.email;
      productName = body.product_name || body.product || 'AI Automation Suite';
      amountStr = body.amount ? (body.amount.startsWith('$') ? body.amount : `$${body.amount}`) : '$1,850.00';
      orderId = body.order_id || orderId;
    }

    // Resolve Automated Fulfillment URL based on purchased product
    let fulfillmentUrl = 'https://work-minh-lap.vercel.app/bundle';
    const pLower = productName.toLowerCase();

    if (pLower.includes('money blueprint') || pLower.includes('guide')) {
      fulfillmentUrl = 'https://work-minh-lap.vercel.app/guides/The_AI_Money_Blueprint.pdf';
    } else if (pLower.includes('prompt')) {
      fulfillmentUrl = 'https://work-minh-lap.vercel.app/guides/AI_Marketing_Prompt_Pack_110.pdf';
    } else if (pLower.includes('extension') || pLower.includes('geo')) {
      fulfillmentUrl = 'https://work-minh-lap.vercel.app/synapsegeo';
    } else if (pLower.includes('review')) {
      fulfillmentUrl = 'https://work-minh-lap.vercel.app/reviewgenius';
    } else if (pLower.includes('headline')) {
      fulfillmentUrl = 'https://work-minh-lap.vercel.app/headlineiq';
    } else if (pLower.includes('setup') || pLower.includes('retainer') || pLower.includes('copilot') || pLower.includes('msa') || pLower.includes('invoice')) {
      fulfillmentUrl = 'https://work-minh-lap.vercel.app/onboarding';
    }

    const nowVn = new Date().toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' });

    // Format rich Telegram message in HTML
    const telegramText = `🎉 <b>[NEW PAYMENT / ORDER CAPTURED! 💰]</b>\n\n` +
      `💵 <b>Doanh thu (Revenue):</b> <code>${amountStr} USD</code>\n` +
      `📦 <b>Sản phẩm (Product):</b> <b>${productName}</b>\n` +
      `👤 <b>Khách hàng:</b> <code>${customerName}</code>\n` +
      `📧 <b>Email:</b> <code>${customerEmail}</code>\n` +
      `📍 <b>Nền tảng (Platform):</b> <i>${platform}</i> (${eventName})\n` +
      `🆔 <b>Mã giao dịch (Order ID):</b> <code>#${orderId}</code>\n` +
      `⏰ <b>Thời gian:</b> ${nowVn}\n\n` +
      `🎁 <b>Link tự động bàn giao tài sản:</b>\n${fulfillmentUrl}\n\n` +
      `👉 <i>Đơn hàng đã được ghi nhận tự động. Tiền về tài khoản thương gia!</i>`;

    const botToken = process.env.TELEGRAM_BOT_TOKEN || '7756122540:AAErx-TV78dUcB0ch7IlZW10R0nIpt1pBhU';
    const chatId = process.env.TELEGRAM_CHAT_ID || '1624883046';

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
      message: 'Payment webhook processed and Telegram alert dispatched.',
      platform,
      event: eventName,
      order_id: orderId,
      customer: {
        name: customerName,
        email: customerEmail
      },
      amount: amountStr,
      product: productName,
      fulfillment_url: fulfillmentUrl,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('[Webhook Error]', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Internal server error while processing webhook.'
    });
  }
}
