# PHASE 1: ACCOUNT CREATION — Step by Step

## Account 1: Supabase (Database)

**Time: 15 min**

1. Go to https://supabase.com
2. Click **"Start your project"** → **"Sign up"**
3. Sign in with GitHub (easiest) or email
4. Create new project:
   - Name: `astria-db`
   - Region: `us-east-1`
   - Database password: Save this securely (1Password)
5. Click **"Create new project"** (wait ~2 min for initialization)
6. Once ready, go to **Settings** → **API**:
   - Copy **URL** (Project URL)
   - Copy **anon public** API key
   - Copy **service_role** API key (keep private)
7. Save all 3 to 1Password labeled "Supabase - Astria"

**Deliverable:** Supabase project running, 3 API keys saved

---

## Account 2: Claude API (Anthropic)

**Time: 10 min**

1. Go to https://console.anthropic.com
2. Click **"Sign up"** or **"Log in"**
3. Create account with email
4. Go to **Settings** → **API Keys**
5. Click **"Create API Key"**
6. Copy the key immediately (won't show again)
7. Save to 1Password labeled "Claude API - Astria"
8. Optional: Set spend limit ($50/month recommended)

**Deliverable:** Claude API key saved, ready to use

---

## Account 3: Instantly.ai (Email Sending)

**Time: 20 min**

1. Go to https://instantly.ai
2. Click **"Sign up"**
3. Fill in: Email, password, name
4. Verify email (check inbox)
5. Once logged in:
   - Go to **Settings** → **API Keys**
   - Generate new API key
   - Copy and save to 1Password labeled "Instantly API - Astria"
6. Create 3 sending accounts (for warmup + rotation):
   - Go to **Accounts** → **Add New Account**
   - For each account:
     - Domain: Use your sending domain (see below)
     - From name: "Alex from Astria"
     - Email: account1@[yourdomain], account2@[yourdomain], account3@[yourdomain]
     - Verify each email (check each inbox)
   - Wait for warmup to start (should auto-begin)
7. Note the **Campaign ID** (or create a test campaign for reference)

**Note:** Sending domain must be set up first (see below). If not ready, create accounts now, add emails later.

**Deliverable:** Instantly account created, 3 email accounts created, API key saved

---

## Account 4: Cal.com (Appointment Booking)

**Time: 15 min**

1. Go to https://cal.com
2. Click **"Get started"** or **"Sign up"**
3. Create account with email/password
4. Once logged in, go to **Settings** → **Event Types**
5. Create new event type:
   - **Title:** "Discovery Call with Astria"
   - **Description:** "15-minute call to see how Astria finds appointments for your business"
   - **Duration:** 15 minutes
   - **Availability:** Set your actual available hours (honest)
   - **Buffer time:** 15 minutes (between appointments)
   - **Confirmation:** Enable email confirmation + reminder (1 hour before)
6. Save the event
7. Copy your Cal.com event link: `https://cal.com/[yourname]/discovery-call`
8. Save to 1Password or notes

**Deliverable:** Cal.com account created, Discovery Call event set up, booking link copied

---

## Account 5: Stripe (Payments)

**Time: 20 min**

1. Go to https://stripe.com
2. Click **"Start now"**
3. Create account with email/password
4. Verify email
5. Once logged in, go to **Settings** → **API Keys**
6. You'll see:
   - **Publishable key**
   - **Secret key**
7. Enable **Restricted API Key** (more secure):
   - Create restricted key with only needed permissions
   - Copy both keys to 1Password labeled "Stripe API - Astria"
8. Go to **Settings** → **Billing** → **Plans** (optional for now)
   - You'll set up $500/mo subscription later
   - For now, just verify you can create charges

**Deliverable:** Stripe account created, API keys saved

---

## Account 6: n8n (Automation)

**Time: 30 min**

n8n runs locally on your Mac. Install it now.

1. Open Terminal (or use exec below)
2. Install n8n:
   ```bash
   npm install -g n8n
   ```
3. Start n8n:
   ```bash
   n8n start
   ```
4. Once running, open: http://localhost:5678
5. Create admin user:
   - Email: your email
   - Password: strong password (save to 1Password)
6. Dashboard loads → you're ready to build workflows

**Keep this terminal running** (or use `nohup n8n start &` to background it)

**Deliverable:** n8n running locally, accessible at localhost:5678

---

## Account 7: Sending Domain (Email Authentication)

**Time: 45 min** (includes DNS propagation wait)

### Option A: Buy New Domain

1. Go to https://namecheap.com (or Godaddy, Route53, etc.)
2. Search for domain: `astriareach.com` (or similar)
3. Buy for 1 year (~$10)
4. Once purchased, go to **Manage** → **Nameservers**
5. Set nameservers to match your primary domain registrar (if you have one) OR use Namecheap's defaults

### Option B: Use Existing Domain (if you have one)

1. Go to your domain registrar's DNS settings
2. Add these records:

**SPF Record** (prevents spoofing):
```
Type: TXT
Name: @
Value: v=spf1 include:sendingdomain.instantly.ai ~all
```

**DKIM Record** (signs emails):
```
Type: CNAME
Name: default._domainkey
Value: default._domainkey.sendingdomain.instantly.ai
```

(Instantly will give you exact DKIM value once you add the domain)

**DMARC Record** (optional but recommended):
```
Type: TXT
Name: _dmarc
Value: v=DMARC1; p=quarantine; rua=mailto:[your-email]@[yourdomain]
```

3. Wait 24-48 hours for DNS to propagate (usually 5-10 min)
4. Test SPF/DKIM via: https://www.mail-tester.com or Instantly's verification

### Add Domain to Instantly

1. Log into Instantly.ai
2. Go to **Sending Accounts** → **Add Domain**
3. Enter: `astriareach.com` (or your domain)
4. Follow verification prompts (add SPF/DKIM records)
5. Once verified (green checkmark), you're ready to send

**Deliverable:** Sending domain set up, SPF/DKIM verified, ready for emails

---

## Storage: API Keys & Secrets

Create a 1Password vault entry:

```
Title: Astria - All API Keys

---

SUPABASE
URL: [your-project-url]
Anon Key: [anon-key]
Service Role Key: [service-role-key]
DB Password: [strong-password]

---

CLAUDE API
API Key: [sk-ant-...]

---

INSTANTLY.AI
API Key: [your-api-key]
Account 1 Email: account1@astriareach.com
Account 2 Email: account2@astriareach.com
Account 3 Email: account3@astriareach.com

---

CAL.COM
Email: [your-email]
Password: [strong-password]
Event Link: https://cal.com/[yourname]/discovery-call

---

STRIPE
Publishable Key: pk_live_...
Secret Key: sk_live_...
Restricted Key: (optional)

---

SENDING DOMAIN
Domain: astriareach.com
SPF: ✅ Verified
DKIM: ✅ Verified
DMARC: ✅ Configured
```

---

## ACCOUNT CREATION CHECKLIST

- [ ] **Supabase:** Project created, 3 API keys saved
- [ ] **Claude API:** Key generated, saved
- [ ] **Instantly.ai:** Account + 3 email accounts created, API key saved
- [ ] **Cal.com:** Account + Discovery Call event created, link copied
- [ ] **Stripe:** Account created, API keys saved
- [ ] **n8n:** Installed locally, running at localhost:5678
- [ ] **Sending Domain:** Purchased + SPF/DKIM verified (or existing domain set up)
- [ ] **1Password:** All secrets saved in one secure vault

---

## QUICK TEST (5 min)

Once all accounts are created:

1. **Supabase:** Log in, see empty database ✅
2. **Claude API:** Call API from Terminal:
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $CLAUDE_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-3-sonnet-20240229","max_tokens":100,"messages":[{"role":"user","content":"Say hello"}]}'
   ```
   Should return JSON response ✅

3. **Instantly.ai:** Log in, see 3 accounts warming up ✅

4. **Cal.com:** Open your booking link, see event ✅

5. **Stripe:** Log in, see API keys ✅

6. **n8n:** Open localhost:5678, see dashboard ✅

7. **Sending Domain:** Check DNS propagation (https://mxtoolbox.com) ✅

---

## TIMELINE

- **Day 1 Morning:** Create accounts 1-7 (2 hours total)
- **Day 1 Afternoon:** Verify all accounts working
- **Day 2:** Move to Phase 2 (database schema)

**All set? Let me know when accounts are ready → I'll help with Phase 2.**
