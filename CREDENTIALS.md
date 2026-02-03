# Astria - Credentials & Access Reference

⚠️ **CONFIDENTIAL** - Keep secure. Never commit to Git. Only share via secure channels.

---

## Account Access

### Primary Email
- **Email:** astriaaibot@gmail.com
- **Password:** *[Keep in 1Password or secure password manager]*
- **Recovery Email:** yammieai@icloud.com
- **MFA:** Enabled (via authenticator app)

---

## Platform Credentials

### GitHub
- **Repo:** https://github.com/astriaaibot/astria-agent
- **Username:** astriaaibot
- **Access:** Public repo, push access via SSH key
- **SSH Key:** Stored in ~/.ssh/id_rsa (on Yammie's machine)
- **Purpose:** Source code, CI/CD pipeline, deployment

### Vercel (Website Hosting)
- **Account:** astriaaibot@gmail.com
- **Project:** astriaaiagent
- **URL:** https://astriaaiagent.vercel.app/
- **Status:** Auto-deploys from GitHub main branch
- **Domain:** astria.fun (primary), astriareach.com (email)
- **SSL:** Auto-renewed, configured

### Stripe (Payment Processing)
- **Account:** astriaaibot@gmail.com
- **Status:** Test mode (development)
- **Products:**
  - Starter: prod_Tucc6p6eVig8mX ($299/mo)
  - Standard: prod_TuccUP0JLOtFrv ($699/mo)
  - Enterprise: prod_TuccnRS7xeXAjD ($1,299/mo)
- **API Keys:**
  - **Publishable Key:** pk_test_51Swn4OEe7Idz4FdTKqCt8Qaz8OiR9F3OmMH0f4n3C0aAp5pKp5cC5cC5cC5cC5cC (for website)
  - **Secret Key:** sk_test_... *[Stored in .env]*
  - **Webhook Secret:** whsec_... *[Stored in .env]*
- **Webhooks:** Configured to listen for checkout.session.completed
- **Purpose:** Billing, subscription management, customer checkout

### Cal.com (Calendar & Booking)
- **Account:** astriaaibot@gmail.com
- **Status:** Live (production)
- **Calendar:** astria (username)
- **Timezone:** America/New_York
- **API Key:** cal_live_a335953057662d932bd4b38521999779
- **Auth Method:** Query parameter (?apiKey=...)
- **Purpose:** Customer booking integration, appointment management

### Supabase (Database)
- **Status:** Awaiting initialization
- **Project URL:** *[To be provided by user]*
- **Anon Key:** *[To be provided by user]*
- **Service Role Key:** *[To be provided by user]*
- **Database:** PostgreSQL (9 tables, schema ready)
- **Tables:**
  - clients, leads, lead_details, email_sequences
  - replies, opportunities, errors, activities_log, reports
- **Purpose:** Customer data, lead management, pipeline tracking

### Telegram (Notifications)
- **Status:** Setup needed
- **Bot Name:** @astriaaibot or @astria_bot (TBD)
- **Bot Token:** *[To be generated via BotFather]*
- **Chat ID:** 8516106442 (Yammie's ID)
- **Purpose:** Webhook notifications (new customers, errors, weekly reports)

### Instantly.ai (Email)
- **Status:** Setup needed
- **Email Accounts:** 3 warm accounts (TBD)
- **Domain:** astriareach.com
- **Purpose:** Email delivery, warmup, outbound emails
- **Integration:** Python script (emails/send_emails.py)

---

## Third-Party Services (No Direct Access Needed)

### Anthropic Claude API
- **Status:** Connected via GitHub (Yammie's account)
- **Model:** Claude 3.5 Sonnet (default)
- **Purpose:** Lead scoring, email generation, reply analysis
- **Rate Limits:** Standard tier

### Google Maps API
- **Status:** TBD (used in scraper)
- **Key:** *[To be configured if needed]*
- **Purpose:** Lead generation, location data

---

## Local Environment Variables (.env)

Keep in workspace root (never commit):

```bash
# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Supabase
SUPABASE_URL=https://...supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Cal.com
CAL_COM_API_KEY=cal_live_...

# Telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=8516106442

# Claude API
ANTHROPIC_API_KEY=... (via GitHub, no local needed)

# Other
ENVIRONMENT=development
DEBUG=false
```

---

## Domains

### Primary Domain
- **Domain:** astria.fun
- **Registrar:** *[To be configured]*
- **DNS:** Pointed to Vercel
- **SSL:** Auto-managed by Vercel
- **Purpose:** Website (astria.fun, www.astria.fun)

### Email Domain
- **Domain:** astriareach.com
- **Registrar:** *[To be configured]*
- **DNS Records Needed:**
  - **SPF:** v=spf1 include:sendingservice.com ~all
  - **DKIM:** (provided by Instantly.ai)
  - **DMARC:** v=DMARC1; p=quarantine
- **Purpose:** Customer email outreach (noreply@astriareach.com)
- **Status:** Setup pending

---

## Access Levels

### Admin (Yammie)
- GitHub repo (push)
- Vercel dashboard
- Stripe account
- Cal.com calendar
- Supabase (once keys provided)
- Domain registrars
- Email accounts
- Telegram bot

### Assistant (AI Agent - me)
- GitHub (read: source code)
- Vercel (read: deployment logs)
- File system (read/write: workspace)
- Stripe API (read: product info, webhook)
- Cal.com API (read: integration setup)
- Supabase API (read/write: once keys provided)
- Telegram API (write: notifications)

---

## Security Notes

### ✅ Best Practices
- API keys stored in .env (never commit)
- Environment-specific configs (dev/staging/production)
- SSH keys for GitHub (not password auth)
- MFA on all user-facing accounts
- Webhook secrets verified before processing
- Rate limiting on APIs

### ⚠️ Caution
- Never share API keys in Telegram/Slack/email
- Rotate keys quarterly
- Use service accounts for integrations
- Monitor API usage for unusual activity
- Backup .env file securely (not in Git)

### 🔒 Secret Management
For production:
- Use 1Password or AWS Secrets Manager
- Never hardcode credentials
- Rotate on employee departure
- Audit access logs

---

## Maintenance Schedule

### Weekly
- Check Stripe webhook logs (errors/retries)
- Monitor Vercel deployments
- Review Telegram notifications for errors

### Monthly
- Verify all API keys are working
- Check SSL certificate expiry (Vercel auto-renews)
- Review Cal.com bookings/integration

### Quarterly
- Rotate API keys (archive old ones)
- Audit third-party access
- Update credentials documentation

---

## Emergency Access

**If Yammie is unavailable:**
1. Credentials are stored in 1Password vault (ask for access)
2. GitHub access via SSH key (backup on secure drive)
3. Stripe test mode (no production data exposed)
4. Supabase backups (daily)
5. Domain registrar (recovery email: yammieai@icloud.com)

---

## Deprecation & Cleanup

Once production is live:
- [ ] Move from Stripe test mode to live keys
- [ ] Update Supabase keys in production
- [ ] Configure SSL certificates for astriareach.com
- [ ] Set up monitoring & alerting (DataDog/Sentry)
- [ ] Archive old API keys
- [ ] Update this document with production URLs

---

**Last Updated:** February 3, 2026  
**Next Review:** March 3, 2026
