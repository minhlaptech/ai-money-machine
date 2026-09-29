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
    version: '6.5.0',
    timestamp: now.toISOString(),
    local_time_vn: now.toLocaleString('vi-VN', { timeZone: 'Asia/Ho_Chi_Minh' }),
    author: 'Minh Lap',
    monorepo: 'https://github.com/minhlaptech/ai-money-machine',
    ecosystem: {
      saas_tools: 5,
      blueprints: 15,
      curated_leads: 30,
      client_portals: 30,
      pitch_decks: 30,
      youtube_episodes: 8,
      blog_guides: 8,
      upwork_proposals: 6,
      social_repurpose_kits: 6
    },
    services: [
      { name: 'SynapseGEO AI SEO Audit', status: 'live', url: 'https://work-minh-lap.vercel.app/synapsegeo' },
      { name: 'ReviewGenius AI Responder', status: 'live', url: 'https://work-minh-lap.vercel.app/reviewgenius' },
      { name: 'HeadlineIQ Viral Scorer', status: 'live', url: 'https://work-minh-lap.vercel.app/headlineiq' },
      { name: 'AI Resource Hub & Guides', status: 'live', url: 'https://work-minh-lap.vercel.app/blog' },
      { name: 'Interactive Chatbot Demo', status: 'live', url: 'https://work-minh-lap.vercel.app/chatbotdemo' },
      { name: 'Sales Pitch Decks Hub', status: 'live', url: 'https://work-minh-lap.vercel.app/pitches' },
      { name: 'Dynamic ROI Simulator', status: 'live', url: 'https://work-minh-lap.vercel.app/calculator' },
      { name: 'Universal Copilot Embed Tag', status: 'live', url: 'https://work-minh-lap.vercel.app/copilot-widget.js' },
      { name: 'Executive VIP Portals Hub', status: 'live', url: 'https://work-minh-lap.vercel.app/portal' },
      { name: 'Executive Command Center', status: 'live', url: 'https://work-minh-lap.vercel.app' },
      { name: 'Serverless Health API', status: 'live', url: 'https://work-minh-lap.vercel.app/api/health' }
    ]
  });
}
