# Astria Project State - Critical Context

## Project Summary
Astria is an autonomous AI sales agent for local service businesses. Auto-finds 50+ leads/day, scores them, analyzes websites, writes personalized 3-email sequences, monitors replies, books appointments via Cal.com, sends weekly reports.

## Architecture (All Complete)
- **Backend**: 8 Python scripts (scraper, scoring, analysis, email writer, sender, reply classifier, reporter)
- **Database**: Supabase (9 tables: clients, leads, lead_details, email_sequences, replies, opportunities, errors, activities_log, reports)
- **Website**: Modern landing page + client dashboard + checkout (Vercel: https://astriaaiagent.vercel.app/)
- **Payments**: Stripe (3 products + recurring billing)
- **Calendar**: Cal.com (live API key configured)
- **Email**: Instantly.ai (pending setup)

## Key Credentials & Configuration

### Stripe (Test Mode)
```
Starter: prod_Tucc6p6eVig8mX | Monthly: price_1SwnNcEe7Idz4FdTV32d7gY5 | Setup: price_1SwnNcEe7Idz4FdTadnsi3bq
Standard: prod_TuccUP0JLOtFrv | Monthly: price_1SwnNdEe7Idz4FdT9Qcg5mvi | Setup: price_1SwnNdEe7Idz4FdTPPF4VCf4
Enterprise: prod_TuccnRS7xeXAjD | Monthly: price_1SwnNdEe7Idz4FdTZSP4y7EI | Setup: price_1SwnNeEe7Idz4FdT2IcUSXPQ
```

### Cal.com
- **Live API Key**: cal_live_a335953057662d932bd4b38521999779
- **Auth Method**: Query parameter (`?apiKey=...`), NOT Bearer token
- **User Profile**: username "astria", email "astriaaibot@gmail.com", timezone "America/New_York"
- **Integration Script**: `calcom/setup_integration.py`

## Pricing (3-Tier Hybrid)
- Starter: $299/mo (50 leads/week, 1 sequence, 1 calendar)
- Standard: $699/mo (200 leads/week, 3 sequences, 3 calendars)
- Enterprise: $1,299/mo (500 leads/week, unlimited sequences, unlimited calendars)
- Margins: 70-86% gross, break-even at 3-10 clients

## Live Deployment
- **Website**: https://astriaaiagent.vercel.app/ (GitHub → Vercel auto-deploy)
- **GitHub**: https://github.com/astriaaibot/astria-agent
- **Domain**: astria.fun (primary) + astriareach.com (email domain, needs SPF/DKIM)

## Setup Status

### ✅ Complete
- All 8 Python scripts (scraper, scoring, analysis, email writer/sender, reply classifier, reporter)
- Supabase schema (9 tables with indexes)
- Website: Desktop + Mobile versions (auto-detection + redirect)
  - `index.html` (desktop) + `index-mobile.html` (mobile landing)
  - `checkout.html` (desktop) + `checkout-mobile.html` (mobile payment)
  - Auto-detection redirects users to appropriate version
- Stripe products + pricing
- GitHub repo + Vercel deployment (live auto-deploy)
- Cal.com integration script + authentication verified
- **Stripe webhook handler** → Stripe → Supabase → Telegram (checkout.session.completed)
- n8n installed locally
- Python dependencies installed

### ⏳ Pending
1. **Supabase initialization**: User provides Project URL + Anon Key + Service Role Key → run `database/init_schema.sql` in SQL editor
2. **Instantly.ai setup**: Create 3 email accounts + warmup
3. **astriareach.com SPF/DKIM**: Domain configuration for email deliverability
4. **Stripe webhook handler**: Backend to catch `checkout.session.completed` → create client in Supabase

## Next Steps (Priority Order)
1. Complete Cal.com integration: fetch event types, generate configuration for website booking URLs
2. User provides Supabase keys → initialize schema → create test client
3. Test each Python script individually (scraper → scoring → analysis → emails → sending)
4. 7-day end-to-end test with test client
5. Build Stripe webhook handler + backend server
6. Onboard first real client (discovery → ICP definition → launch)

## Important Notes
- **User**: Yammie, EST timezone, prefers to execute (GitHub, Stripe, etc.), wants token efficiency
- **Tech Choices**: Python scripts (not n8n yet) for modularity/testing; Vercel for website; Stripe for PCI compliance
- **Cal.com Note**: Query parameter auth is required; Bearer token auth fails with 401
- **Pipeline Test Blocked**: Until Supabase API keys provided and schema initialized
- **Timeline**: Fast (14-day launch target); user can self-check to save tokens
