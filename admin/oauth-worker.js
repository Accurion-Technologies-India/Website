/**
 * Accurion Technologies — GitHub OAuth Bridge for Decap CMS
 * Deploy this on Cloudflare Workers (Free tier)
 * 
 * Required Environment Variables / Secrets on Cloudflare:
 * - GITHUB_CLIENT_ID: The Client ID from your GitHub OAuth App
 * - GITHUB_CLIENT_SECRET: The Client Secret from your GitHub OAuth App
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // 1. Initial Authorization Request from Decap CMS
    if (url.pathname === '/auth') {
      const state = crypto.randomUUID();
      const redirectUri = `https://github.com/login/oauth/authorize?client_id=${env.GITHUB_CLIENT_ID}&scope=repo&state=${state}`;
      return Response.redirect(redirectUri, 302);
    }

    // 2. OAuth Callback from GitHub
    if (url.pathname === '/callback') {
      const code = url.searchParams.get('code');
      if (!code) {
        return new Response('Missing authorization code', { status: 400 });
      }

      // Exchange code for GitHub access token
      const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'User-Agent': 'Accurion-CMS-OAuth'
        },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code: code
        })
      });

      const tokenData = await tokenResponse.json();

      if (tokenData.error) {
        return new Response(`Authentication Error: ${tokenData.error_description || tokenData.error}`, { status: 400 });
      }

      // Post back token to Decap CMS popup window
      const responseBody = `
        <!doctype html>
        <html>
        <head><title>Authorizing...</title></head>
        <body>
          <script>
            (function() {
              function receiveMessage(e) {
                window.opener.postMessage(
                  'authorization:github:success:${JSON.stringify({
                    token: tokenData.access_token,
                    provider: 'github'
                  })}',
                  e.origin
                );
                window.removeEventListener("message", receiveMessage, false);
                window.close();
              }
              window.addEventListener("message", receiveMessage, false);
              window.opener.postMessage("authorizing:github", "*");
            })();
          </script>
          <p style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            Authentication successful! Closing window...
          </p>
        </body>
        </html>
      `;

      return new Response(responseBody, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
      });
    }

    return new Response('Accurion CMS OAuth Bridge is operational.', { status: 200 });
  }
};
