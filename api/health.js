/**
 * Serverless Health & Diagnostics API
 * ------------------------------------
 * Endpoint: GET /api/health
 * Returns JSON status of the AI Money Machine ecosystem.
 */

export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const now = new Date();
  
  return res.status(200).json({
    status: 'operational',
    version: '3.5.0',
    timestamp: now.toISOString(),
    local_time_vn: now.toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' }),
    author: 'Minh Lap',
    ecosystem: {
      saas_tools: 5,
      blueprints: 15,
      curated_leads: 30,
      youtube_episodes: 8,
      blog_guides: 8
    },
    services: [
      { name: 'SynapseGEO', status: 'live', url: 'https://synapse-geo-audit.vercel.app' },
      { name: 'ReviewGenius AI', status: 'live', url: 'https://work-minh-lap.vercel.app/products/review_genius/index.html' },
      { name: 'HeadlineIQ', status: 'live', url: 'https://headlineiq-eta.vercel.app' },
      { name: 'AI Resource Hub', status: 'live', url: 'https://ai-automation-guide-omega.vercel.app' },
      { name: 'Chatbot Demo', status: 'live', url: 'https://work-minh-lap.vercel.app/projects/ai_freelancing/portfolio/demo_chatbot.html' },
      { name: 'Command Center', status: 'live', url: 'https://work-minh-lap.vercel.app' }
    ]
  });
}
