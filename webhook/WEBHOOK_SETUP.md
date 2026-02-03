# Stripe Webhook Setup for Astria

## What It Does
- ✅ Listens for `checkout.session.completed` events from Stripe
- ✅ Creates client record in Supabase `clients` table
- ✅ Sends Telegram notification when new customer signs up
- ✅ Logs activity to `activities_log` for tracking

## Prerequisites
1. **Stripe Account** - test or live keys
2. **Supabase** - Project URL + Service Role Key (webhook uses this)
3. **Telegram Bot Token** - from BotFather on Telegram
4. **Telegram Chat ID** - your personal chat with the bot

## Environment Variables

Add these to `.env`:
```bash
# Stripe
STRIPE_SECRET_KEY=sk_test_...  # Your Stripe secret key
STRIPE_WEBHOOK_SECRET=whsec_...  # Generated after registering webhook

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...  # Service role key (NOT anon key)

# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11  # BotFather token
TELEGRAM_CHAT_ID=987654321  # Your chat ID with bot

# Server
PORT=5000  # Or any port
```

## Step 1: Create Telegram Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Follow prompts to create a bot
4. Copy the bot token and add to `.env` as `TELEGRAM_BOT_TOKEN`

## Step 2: Get Your Telegram Chat ID

1. Start a chat with your new bot (search by name in Telegram)
2. Send any message to the bot
3. Go to: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4. Look for `"chat":{"id":YOUR_CHAT_ID}` 
5. Copy the ID and add to `.env` as `TELEGRAM_CHAT_ID`

## Step 3: Install Dependencies

```bash
pip install flask stripe supabase requests python-dotenv
```

## Step 4: Run Webhook Server

### Local Testing
```bash
python webhook/stripe_webhook.py
```
Server runs on `http://localhost:5000`

### Production Deployment (Heroku/Railway/Fly.io)
1. Deploy the server to a public URL (e.g., `https://astria-webhook.fly.dev`)
2. See deployment section below

## Step 5: Register Webhook with Stripe

1. Go to Stripe Dashboard → **Developers** → **Webhooks**
2. Click **Add endpoint**
3. **Endpoint URL:** `https://your-domain.com/webhook/stripe` (or your server URL)
4. **Events to send:** Select only `checkout.session.completed`
5. Click **Add endpoint**
6. Copy the signing secret (starts with `whsec_`)
7. Add to `.env` as `STRIPE_WEBHOOK_SECRET`

## Step 6: Test Webhook

### Test in Stripe Dashboard
1. Go to webhook details page
2. Scroll to **Events** section
3. Find `checkout.session.completed` event
4. Click **Send test event**
5. Check Telegram for notification

### Test Live
1. Complete a test checkout on your Astria website
2. Wait 2-5 seconds for webhook to fire
3. Check Telegram and Supabase `clients` table

## Webhook Response Format

When a new customer signs up, Telegram will receive:
```
🎉 New Astria Client!

Name: John's Plumbing
Email: john@plumbing.local
Plan: Standard
Client ID: 123

✨ Ready to onboard!
```

## Troubleshooting

### Webhook not firing?
- ❌ Check Stripe Dashboard → Webhooks → Events tab for error details
- ❌ Verify endpoint URL is publicly accessible
- ❌ Check server logs: `python webhook/stripe_webhook.py`

### Telegram notification not sending?
- ❌ Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- ❌ Test bot manually: `https://api.telegram.org/bot<TOKEN>/getUpdates`
- ❌ Make sure bot has permission to send messages (start the bot first)

### Client not created in Supabase?
- ❌ Verify `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are correct
- ❌ Check that `clients` table exists (run `database/init_schema.sql` first)
- ❌ Check Supabase logs for errors

### "Invalid signature"?
- ❌ Webhook secret mismatch - re-copy from Stripe Dashboard
- ❌ Make sure you're using `STRIPE_WEBHOOK_SECRET`, not `STRIPE_SECRET_KEY`

## Production Deployment

### Option 1: Fly.io (Recommended)
```bash
# Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/

# Create fly.toml in workspace root
cat > fly.toml << 'EOF'
app = "astria-webhook"
primary_region = "iad"

[env]
  STRIPE_SECRET_KEY = "sk_test_..."
  SUPABASE_URL = "https://..."
  SUPABASE_SERVICE_ROLE_KEY = "..."
  TELEGRAM_BOT_TOKEN = "..."
  TELEGRAM_CHAT_ID = "..."

[processes]
  api = "gunicorn -w 2 webhook.stripe_webhook:app"

[http_service]
  internal_port = 8080
  force_https = true
EOF

# Deploy
fly launch
fly deploy
```

### Option 2: Heroku
```bash
# Create Procfile
echo "web: gunicorn webhook.stripe_webhook:app" > Procfile

# Deploy
heroku create astria-webhook
heroku config:set STRIPE_SECRET_KEY=sk_test_...
heroku config:set SUPABASE_URL=...
heroku config:set SUPABASE_SERVICE_ROLE_KEY=...
heroku config:set TELEGRAM_BOT_TOKEN=...
heroku config:set TELEGRAM_CHAT_ID=...
git push heroku main
```

### Option 3: Railway
1. Connect GitHub repo
2. Add environment variables in Railway dashboard
3. Set start command: `gunicorn webhook.stripe_webhook:app`
4. Deploy

## Next Steps

After webhook is live:
1. ✅ Stripe webhook registered
2. ✅ Telegram notifications working
3. **Next:** Build client onboarding flow → trigger pipeline when client signs up
4. **Then:** Auto-generate ICP questionnaire and send to client

---

Questions? Check `/webhook/stripe_webhook.py` source code for implementation details.
