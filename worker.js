export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const filename = url.pathname.substring(1);
    
    if (!filename) {
      return new Response("OK", { headers: { "Content-Type": "text/plain" } });
    }
    
    // First check the Worker cache
    const cache = caches.default;
    let cached = await cache.match(request);
    if (cached) return cached;
    
    // Fetch from GitHub with CDN cache enabled
    let sourceUrl;
    if (filename === "SLT-290-2024.pdf") {
      sourceUrl = "https://github.com/qingtian1997c-max/ZG-SLGF/releases/download/v1.0/SLT-290-2024.pdf";
    } else {
      sourceUrl = "https://raw.githubusercontent.com/qingtian1997c-max/ZG-SLGF/main/" + filename;
    }
    
    // Use Cloudflare CDN cache for the upstream fetch
    const upstream = await fetch(sourceUrl, {
      cf: { cacheTtl: 86400, cacheEverything: true }
    });
    
    if (!upstream.ok) {
      return new Response("Not found", { status: 404 });
    }
    
    // Build response with PDF headers
    const headers = new Headers();
    headers.set("Content-Type", "application/pdf");
    headers.set("Cache-Control", "public, max-age=86400");
    headers.set("Access-Control-Allow-Origin", "*");
    
    const response = new Response(upstream.body, { status: 200, headers });
    
    // Store in Worker cache for next time
    ctx.waitUntil(cache.put(request, response.clone()));
    
    return response;
  }
};