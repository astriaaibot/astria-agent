# Railway Deployment Guide - 10 Minutes

Deploy Astria webhook server to Railway (Python + Stripe + Telegram).

---

## Why Railway?
- ✅ Free tier sufficient ($5/month credit)
- ✅ Auto-deploy from GitHub
- ✅ Simple environment variables
- ✅ No credit card needed initially
- ✅ Perfect for Python apps

---

## Step-by-Step Deployment

### Step 1: Sign Up (2 minutes)
1. Go to: https://railway.app
2. Click **Sign Up**
3. Choose: **GitHub** (easiest)
4. Authorize Railway to access your GitHub account

### Step 2: Create New Project (1 minute)
1. Click **New Project**
2. Choose: **Deploy from GitHub repo**
3. Find: `astriaaibot/astria-agent`
4. Select the repo
5. Click **Deploy**

### Step 3: Set Environment Variables (3 minutes)
Railway will ask for environment variables. Set these:

```
STRIPE_SECRET_KEY = sk_test_... (from your Stripe account)
STRIPE_WEBHOOK_SECRET = whsec_... (from Stripe webhook setup)
SUPABASE_URL = https://...supabase.co (you'll provide after setup)
SUPABASE_SERVICE_ROLE_KEY = eyJ... (you'll provide after setup)
TELEGRAM_BOT_TOKEN = 8394189992:AAF59O_hq9T1Fi_sTcfRUpks8X72t_nsrHc
TELEGRAM_CHAT_ID = (your chat ID - get from @Astriapeoplebot)
PORT = 5000
```

### Step 4: Deploy (2 minutes)
1. Railway will build automatically
2. Wait for "Build succeeded"
3. Click **View logs** to verify startup
4. You should see: `🚀 Stripe webhook server running on port 5000`

### Step 5: Get Public URL (1 minute)
1. Go to **Settings** tab
2. Under **Domains**, copy your public URL
3. It will look like: `https://astria-webhook-prod.up.railway.app`
4. Send this to me

---

## Environment Variables Reference

### Required (Stripe)
```
STRIPE_SECRET_KEY = Your Stripe secret key (starts with sk_test_)
STRIPE_WEBHOOK_SECRET = Your webhook signing secret (starts with whsec_)
```

### Required (Supabase) - Will get after initialization
```
SUPABASE_URL = Your Supabase project URL
SUPABASE_SERVICE_ROLE_KEY = Your service role key
```

### Required (Telegram)
```
TELEGRAM_BOT_TOKEN = 8394189992:AAF59O_hq9T1Fi_sTcfRUpks8X72t_nsrHc
TELEGRAM_CHAT_ID = Your chat ID (get from @Astriapeoplebot)
```

### Optional
```
PORT = 5000 (default)
ENVIRONMENT = production
```

---

## Troubleshooting

### Build fails
**Check logs:** Click **View logs** in Railway dashboard
**Most common:** Missing environment variables

### Webhook not responding
**Verify:** Public URL is accessible in browser
**Try:** Visit `https://your-url/health` (should return 200 OK)

### Env variables not loading
**Redeploy:** Make change to railway.json and push to GitHub
**Or:** In Railway, click **Redeploy** button

---

## Verify Deployment

Once deployed, verify it's working:

```bash
# Replace with your Railway URL
curl https://your-url/health

# Should return:
{"status": "ok", "service": "astria-stripe-webhook"}
```

---

## Stripe Webhook Registration (I'll do this)

After you send me the public URL, I'll:
1. Register webhook in Stripe Dashboard
2. Point to: `https://your-url/webhook/stripe`
3. Test with demo event
4. Verify Telegram notification fires

---

## Auto-Deploy from GitHub

Once set up:
- Any push to `main` → auto-deploys
- Changes live in 2-3 minutes
- No manual deployment needed

---

## Costs

- **Free tier:** $5/month credit (covers this)
- **Usage:** ~$1-2/month if successful
- **Cancel anytime:** No contract

---

## Quick Checklist

```
☐ Sign up to Railway
☐ Connect GitHub repo
☐ Set environment variables (you'll have 4 from me)
☐ Deploy
☐ Get public URL
☐ Send URL to me
☐ I register webhook
☐ Test Telegram notification
☐ Done!
```

---

## Still Stuck?

Railway support: https://railway.app/support

---

**Estimated Time:** 10 minutes  
**Difficulty:** Easy  
**Help Available:** Yes (I'll guide you)

Ready? Start here: https://railway.app
