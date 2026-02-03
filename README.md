# Astria — Autonomous AI Sales Agent

> Find qualified leads, send personalized emails, handle objections, book appointments—24/7, automatically.

Astria is a complete autonomous sales system for local service businesses. It discovers high-potential prospects, analyzes their websites, writes personalized email campaigns, monitors replies in real-time, and books appointments on your calendar.

## What's Inside

### 🌐 Website
- **Landing page** (`website/index.html`) — Sales + value prop
- **Client dashboard** (`website/dashboard.html`) — Real-time pipeline visibility
  - KPI cards (leads, emails, replies, appointments)
  - Pipeline status (new → qualified → contacted → booked)
  - Weekly activity feed
  - Email performance metrics
  - Upcoming appointments
  - Weekly reports

### 🤖 Backend Scripts (Python)
Complete workflow automation — all 8 daily tasks:

1. **Scrape** (`scraper/scrape_leads.py`) — Find 50+ leads from Google Maps
2. **Score** (`scoring/score_leads.py`) — Rate each lead 1-10 with Claude
3. **Analyze** (`analysis/analyze_websites.py`) — Extract personalization hooks
4. **Write** (`emails/write_sequences.py`) — Generate 3-email campaigns
5. **Send** (`emails/send_emails.py`) — Push emails via Instantly.ai
6. **Monitor** (`replies/classify_replies.py`) — Classify replies + take action
7. **Book** — Cal.com webhook integration
8. **Report** (`reporting/send_weekly_report.py`) — Weekly client summaries

### 📦 Database
- **Schema** (`database/init_schema.sql`) — 9 tables, foreign keys, indexes
- **Tables:** clients, leads, email_sequences, replies, opportunities, errors, activities_log, reports

### 📖 Documentation
- `ASTRIA_SPRINT.md` — 14-day build checklist
- `BUILDOUT.md` — Detailed plan, costs, timeline
- `RUN_PIPELINE.md` — How to execute each script
- `TEST_SETUP.md` — Complete testing guide
- `WORK_COMPLETED.md` — Current build status

---

## Quick Start

### Deploy Website

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from website folder
cd website
vercel --prod

# Add custom domain (astria.fun) in Vercel dashboard
```

**Live in <5 minutes.**

### Setup Backend

```bash
# 1. Install dependencies
pip install anthropic supabase python-dotenv requests

# 2. Create .env from .env.example
cp .env.example .env
# Add your API keys:
# - SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
# - CLAUDE_API_KEY
# - INSTANTLY_API_KEY
# - STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

# 3. Initialize database in Supabase
# - Copy database/init_schema.sql
# - Go to Supabase SQL Editor
# - Paste and run

# 4. Run pipeline (manual test)
python scraper/scrape_leads.py --client-id <client-uuid>
python scoring/score_leads.py --client-id <client-uuid>
# ... etc (see RUN_PIPELINE.md)
```

### Setup with n8n (Automated)

```bash
# Start n8n locally
n8n start

# Create workflows for each task:
# - 6:00 AM: Scrape
# - 6:30 AM: Score
# - 7:00 AM: Analyze
# - 7:30 AM: Write
# - 9:00 AM: Send
# - Real-time: Monitor (webhook)
# - Sundays 8 PM: Report
```

---

## Architecture

```
User (Business Owner)
      ↓
Landing Page (astria.fun) — Book demo
      ↓
Client Dashboard (app.astria.fun/dashboard) — Real-time metrics
      ↓
Astria Backend:
  - Leads: Google Maps scraper
  - Scoring: Claude API (1-10 rating)
  - Emails: Claude (personalized) + Instantly.ai (send)
  - Replies: Claude (classify) + auto-response
  - Bookings: Cal.com + Supabase
      ↓
Supabase Database — All activity logged
      ↓
Reports: Claude (summarize) → Client email (Sundays)
```

---

## Configuration

### ICP (Ideal Customer Profile)
Define per client in `clients` table:
```sql
INSERT INTO clients (business_name, category, service_area_cities)
VALUES ('Your Business', 'HVAC', ARRAY['Fort Lauderdale', 'Miami']);
```

### Email Sending Accounts
Add 3 Instantly.ai accounts (for rotation + warmup):
- `account1@astriareach.com`
- `account2@astriareach.com`
- `account3@astriareach.com`

### Booking Link
Configure Cal.com event:
- Event type: "Discovery Call with Astria"
- Duration: 15 minutes
- Availability: Your actual available hours
- Link: `https://cal.com/yourname/discovery-call`

---

## Metrics to Track

Daily:
- Leads scraped (target: 50+)
- Email open rate (target: >40%)
- Reply rate (target: >3%)
- Bounce rate (target: <2%)

Weekly:
- Appointments booked (target: 1-3)
- Cost per lead (~$3-5)
- Cost per appointment (~$150-250)

---

## Troubleshooting

**"No leads found"**
- Verify search queries are correct
- Check Google Maps is accessible
- Try different keywords

**"Claude API timeout"**
- Check API quota
- Retry in a few seconds
- Verify internet connection

**"Email send failed"**
- Verify Instantly.ai account is warmed up
- Check bounce rate <2%
- Verify email list is clean

**"Dashboard not loading data"**
- Verify Supabase API key
- Check CORS settings
- Inspect browser console for errors

---

## Costs

### Monthly (with 1 client)
- **Supabase:** $0-25 (free tier to $25/mo)
- **Claude API:** ~$50 (pays for itself in day 1)
- **Instantly.ai:** $25 (3 accounts)
- **Cal.com:** $0-99 (free tier to pro)
- **Stripe:** 2.9% + $0.30 per transaction
- **Total:** ~$85-100/mo to run service

### Per Client Revenue
- **Tier 1:** $500/mo ($300 gross margin)
- **Tier 2:** $1,000/mo ($600 gross margin)
- **Tier 3:** $1,500/mo ($850 gross margin)

**20 clients = $10,000-25,000 MRR**

---

## Development

### Adding a New Task
1. Create script in `/task-name/` folder
2. Follow Claude integration pattern (see other scripts)
3. Store results in Supabase
4. Create n8n workflow (if automating)
5. Document in `RUN_PIPELINE.md`

### Modifying Email Template
Edit prompt in `emails/write_sequences.py`:
```python
EMAIL_WRITING_PROMPT = """..."""
```

### Customizing Dashboard
Edit `website/dashboard.html` + `website/dashboard.css`
- Sections are modular (add/remove easily)
- Ready for Supabase API integration

---

## Security

- 🔐 **API keys:** Stored in 1Password + `.env` (never committed)
- 🔐 **Database:** Supabase row-level security (optional)
- 🔐 **Email:** SPF/DKIM configured for domain
- 🔐 **Webhooks:** Verify source before processing

See `.env.example` for required variables.

---

## License

© 2026 Pelican Pointe LLC. All rights reserved.

---

## Support

- **Issues?** Check `TEST_SETUP.md` troubleshooting section
- **Questions?** See `BUILDOUT.md` for detailed documentation
- **Ready to launch?** Follow `ASTRIA_SPRINT.md` checklist

---

**Status:** Building (website ready, backend ready, awaiting API keys for database setup)

**Next:** Deploy website → Initialize database → Run first test pipeline → Go live

---

Made with ⚡ by Astria
