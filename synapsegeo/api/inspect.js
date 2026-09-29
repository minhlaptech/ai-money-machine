export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const { url } = req.query;
  if (!url) {
    return res.status(400).json({ error: 'Missing url query parameter' });
  }

  let targetUrl = decodeURIComponent(String(url).trim());
  if (!targetUrl.startsWith('http://') && !targetUrl.startsWith('https://')) {
    targetUrl = 'https://' + targetUrl;
  }

  let domain = '';
  let baseUrl = '';
  try {
    const parsed = new URL(targetUrl);
    domain = parsed.hostname;
    baseUrl = `${parsed.protocol}//${parsed.hostname}`;
  } catch (e) {
    return res.status(400).json({ error: 'Invalid URL format' });
  }

  const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 SynapseGEO/1.0';

  let gptbotAllowed = true;
  let perplexityAllowed = true;
  let claudebotAllowed = true;
  let googleExtendedAllowed = true;
  let robotsFound = false;

  // 1. Inspect robots.txt for AI bots
  try {
    const robotsController = new AbortController();
    const robotsTimeout = setTimeout(() => robotsController.abort(), 4000);
    const robotsRes = await fetch(`${baseUrl}/robots.txt`, {
      headers: { 'User-Agent': userAgent },
      signal: robotsController.signal
    });
    clearTimeout(robotsTimeout);

    if (robotsRes.ok) {
      robotsFound = true;
      const robotsText = await robotsRes.text();

      const isDisallowed = (botName) => {
        const regex = new RegExp(`User-agent:\\s*${botName}[\\s\\S]*?Disallow:\\s*/\\s*($|\\n)`, 'i');
        return regex.test(robotsText);
      };

      if (isDisallowed('GPTBot')) gptbotAllowed = false;
      if (isDisallowed('PerplexityBot')) perplexityAllowed = false;
      if (isDisallowed('ClaudeBot') || isDisallowed('AnthropicAI')) claudebotAllowed = false;
      if (isDisallowed('Google-Extended')) googleExtendedAllowed = false;
    }
  } catch (err) {
    // Robots.txt fetch timeout or error - default to open
  }

  // 2. Inspect Target Page HTML
  let hasSchema = false;
  let title = '';
  let metaDescription = '';
  let ogTitle = '';
  let wordCount = 0;
  let headingsCount = { h1: 0, h2: 0 };
  let liveFetched = false;

  try {
    const pageController = new AbortController();
    const pageTimeout = setTimeout(() => pageController.abort(), 5000);
    const pageRes = await fetch(targetUrl, {
      headers: { 'User-Agent': userAgent },
      signal: pageController.signal
    });
    clearTimeout(pageTimeout);

    if (pageRes.ok) {
      liveFetched = true;
      const html = await pageRes.text();

      // Check Schema JSON-LD
      if (html.includes('application/ld+json')) {
        hasSchema = true;
      }

      // Title tag
      const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
      if (titleMatch) title = titleMatch[1].trim();

      // Meta Description
      const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["']/i);
      if (descMatch) metaDescription = descMatch[1].trim();

      // OpenGraph Title
      const ogMatch = html.match(/<meta[^>]*property=["']og:title["'][^>]*content=["']([^"']*)["']/i);
      if (ogMatch) ogTitle = ogMatch[1].trim();

      // Simple body text word estimation
      const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
      if (bodyMatch) {
        const stripped = bodyMatch[1].replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
                                     .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
                                     .replace(/<[^>]+>/g, ' ');
        const words = stripped.split(/\s+/).filter(Boolean);
        wordCount = words.length;
      }

      // Headings
      const h1Matches = html.match(/<h1[^>]*>/gi);
      const h2Matches = html.match(/<h2[^>]*>/gi);
      headingsCount.h1 = h1Matches ? h1Matches.length : 0;
      headingsCount.h2 = h2Matches ? h2Matches.length : 0;
    }
  } catch (err) {
    // Target page fetch timeout or error
  }

  return res.status(200).json({
    status: 'success',
    live_fetched: liveFetched,
    target: targetUrl,
    domain,
    title: title || ogTitle || domain,
    meta_description: metaDescription,
    robots_found: robotsFound,
    ai_permissions: {
      gptbot: gptbotAllowed,
      perplexity: perplexityAllowed,
      claudebot: claudebotAllowed,
      google_extended: googleExtendedAllowed
    },
    gptbot_allowed: gptbotAllowed,
    perplexity_allowed: perplexityAllowed,
    has_schema_jsonld: hasSchema,
    word_count: wordCount,
    headings: headingsCount
  });
}
