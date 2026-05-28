export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const filename = url.pathname.substring(1);
    
    if (!filename) {
      return new Response("PDF Proxy OK", { headers: { "content-type": "text/plain" } });
    }
    
    // Map filenames to GitHub raw URLs
    const cache = caches.default;
    const cacheKey = new Request(request.url, request);
    
    // Check cache first
    let response = await cache.match(cacheKey);
    if (response) {
      return response;
    }
    
    // Fetch from GitHub
    let githubUrl;
    if (filename === "SLT-290-2024.pdf") {
      githubUrl = "https://github.com/qingtian1997c-max/ZG-SLGF/releases/download/v1.0/SLT-290-2024.pdf";
    } else {
      githubUrl = `https://raw.githubusercontent.com/qingtian1997c-max/ZG-SLGF/main/${filename}`;
    }
    response = await fetch(githubUrl);
    
    if (response.ok) {
      // Clone and cache
      const toCache = new Response(response.body, response);
      toCache.headers.set("Cache-Control", "public, max-age=86400");
      ctx.waitUntil(cache.put(cacheKey, toCache));
      
      return new Response(response.body, {
        status: response.status,
        headers: {
          "Content-Type": "application/pdf",
          "Cache-Control": "public, max-age=86400",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }
    
    return new Response("File not found", { status: 404 });
  }
};