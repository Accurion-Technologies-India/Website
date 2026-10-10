# Accurion CMS — GitHub OAuth Setup Guide

This guide explains how to connect GitHub OAuth with Decap CMS at `/admin/` in **3 simple steps**.

---

## Architecture Overview

When the client logs into `/admin/`:
1. They click **"Login with GitHub"**.
2. GitHub verifies their credentials and permissions to the `Accurion-Technologies-India/Website` repository.
3. A lightweight serverless OAuth proxy (`oauth-worker.js`) securely exchanges the temporary code for an access token using your private Client Secret.
4. The client is authenticated and can create, edit, duplicate, and publish products.

---

## Step 1: Create a GitHub OAuth App

1. Go to [GitHub Developer Settings &rarr; OAuth Apps](https://github.com/settings/developers).
2. Click **New OAuth App**.
3. Fill in the details:
   - **Application name**: `Accurion Technologies CMS`
   - **Homepage URL**: `https://www.accuriontechnologies.com/admin/`
   - **Application description**: `Content Management System for Accurion Technologies`
   - **Authorization callback URL**: `https://<YOUR-WORKER-NAME>.workers.dev/callback` (or your custom domain)
4. Click **Register application**.
5. Copy your **Client ID**.
6. Click **Generate a new client secret** and copy the secret.

---

## Step 2: Deploy the Free Cloudflare Worker

1. Log into your free [Cloudflare Dashboard](https://dash.cloudflare.com/) and go to **Workers & Pages**.
2. Click **Create Application** &rarr; **Create Worker**.
3. Name it (e.g., `accurion-cms-auth`).
4. Paste the code from [`admin/oauth-worker.js`](./oauth-worker.js) into the worker editor.
5. In the Worker's **Settings &rarr; Variables and Secrets**, add two encrypted secrets:
   - `GITHUB_CLIENT_ID` = *(Your Client ID from Step 1)*
   - `GITHUB_CLIENT_SECRET` = *(Your Client Secret from Step 1)*
6. Click **Deploy**. Note your worker's URL (e.g. `https://accurion-cms-auth.<your-subdomain>.workers.dev`).

---

## Step 3: Link Worker URL in `admin/config.yml`

In [`admin/config.yml`](./config.yml), update the `base_url` under `backend`:

```yaml
backend:
  name: github
  repo: Accurion-Technologies-India/Website
  branch: main
  base_url: https://accurion-cms-auth.<your-subdomain>.workers.dev
  auth_endpoint: auth
```

Commit and push to `main`. Your production OAuth bridge is now live!

---

## Local Development Mode (Zero-Config Testing)

For local development or testing before deploying the OAuth worker:
1. `local_backend: true` is already enabled in [`admin/config.yml`](./config.yml).
2. Run the Decap local proxy server in terminal:
   ```bash
   npx decap-server
   ```
3. Open `http://localhost:8080/admin/` (or your local web server port). Decap CMS connects directly to your local file system with **no login required**!
