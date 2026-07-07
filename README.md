# gamalkhalaf.github.io

Solution: Deploy a free OAuth proxy on Vercel
Follow these steps:
1. Deploy the proxy (one-click)
Go to this repo and click Deploy to Vercel:
https://github.com/vencax/netlify-cms-github-oauth-provider
Or manually:
- Fork the repo
- Import it into Vercel as a new project
- Vercel will give you a URL like https://your-proxy.vercel.app
2. Create a GitHub OAuth App
Go to GitHub Settings → Developer settings → OAuth Apps → New OAuth App:
- Homepage URL: https://gamalkhalaf.github.io
- Authorization callback URL: https://your-proxy.vercel.app/auth/done
- Generate a Client Secret and note the Client ID
3. Configure the proxy on Vercel
In your Vercel project settings, add these environment variables:
- OAUTH_CLIENT_ID: your GitHub OAuth App Client ID
- OAUTH_CLIENT_SECRET: your GitHub OAuth App Client Secret
- REDIRECT_URL: https://your-proxy.vercel.app/auth/done
- SITE_URL: https://gamalkhalaf.github.io
4. Update Decap CMS config
Replace base_url in docs/admin/config.yml:
backend:
  name: github
  repo: gamalkhalaf/gamalkhalaf.github.io
  branch: main
  base_url: https://your-proxy.vercel.app
Then rebuild and push. The admin panel will redirect to your proxy for GitHub login instead of api.netlify.com