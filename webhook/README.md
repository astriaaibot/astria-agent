# Stripe → Supabase → Telegram Webhook

**What this does:**
```
Stripe Checkout → Webhook Receives Event → Client Created in Supabase → Telegram Notification Sent to You
```

## Files

- **`stripe_webhook.py`** - Flask server that handles Stripe webhook events
- **`WEBHOOK_SETUP.md`** - Complete setup guide (10 min, step-by-step)
- **`TELEGRAM_QUICK_SETUP.md`** - Fast Telegram bot setup (2 min)
- **`requirements.txt`** - Python dependencies

## Quick Start (5 min)

### Step 1: Telegram (2 min)
```bash
# 1. Talk to @BotFather on Telegram → Create bot → Copy token
# 2. Message your bot → Visit: https://api.telegram.org/bot<TOKEN>/getUpdates
# 3. Copy chat ID
```

### Step 2: Environment
```bash
# Add to .env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...  # Will get from Stripe
SUPABASE_URL=https://...
SUPABASE_SERVICE_ROLE_KEY=...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

### Step 3: Run Locally
```bash
pip install -r requirements.txt
python stripe_webhook.py
# Server running on http://localhost:5000
```

### Step 4: Register with Stripe
1. Stripe Dashboard → Developers → Webhooks → Add endpoint
2. URL: `https://your-webhook-server.com/webhook/stripe`
3. Events: `checkout.session.completed`
4. Copy signing secret → Add to `.env` as `STRIPE_WEBHOOK_SECRET`

### Step 5: Test
- Complete a test checkout on your Astria website
- Check Telegram for notification
- Verify client created in Supabase

## Features

✅ **Automatic Client Onboarding**
- Detects which plan customer purchased (Starter/Standard/Enterprise)
- Creates client record with email, name, plan tier
- Stores Stripe IDs for future billing interactions

✅ **Telegram Notifications**
- Real-time alerts when new customer signs up
- Includes: name, email, plan, client ID
- Rich formatting for easy scanning

✅ **Activity Logging**
- Logs "client_created" event to `activities_log` table
- Tracks Stripe session ID for debugging
- Full audit trail of customer lifecycle

✅ **Error Handling**
- Verifies Stripe signature (prevents spoofing)
- Graceful degradation if Telegram fails
- Logs all errors to console

## Deployment

For production, deploy to Fly.io, Heroku, Railway, or any cloud platform that runs Python + Flask.

See **WEBHOOK_SETUP.md** → "Production Deployment" section for complete instructions.

## What's Next

After webhook is live:

1. **Client Onboarding Flow** - Send ICP questionnaire when customer signs up
2. **Pipeline Trigger** - Auto-launch lead scraping/scoring when onboarded
3. **Slack/Discord Webhooks** - Bonus: Add notifications to other platforms

---

**Need help?** Check WEBHOOK_SETUP.md for troubleshooting.
