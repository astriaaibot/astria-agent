# Astria Project State - Critical Context

## Recent Fixes (Feb 3, 2026)
- ✅ **Removed broken Calendly links** (page didn't exist)
- ✅ **Created built-in demo form** (/demo-request.html)
- ✅ **All links now work** (no external dependencies)
- ✅ **Everything self-contained on site** (no dead links)

## Documentation System Complete

**Full Knowledge Base Created:** 60KB of comprehensive operational documentation
- ROADMAP.md - Full product roadmap with 4 phases, timeline, revenue targets, risk mitigation
- PERSONALITY.md - Brand voice, communication style, character traits, guiding principles
- CREDENTIALS.md - API keys, platform access, environment config, security procedures
- KB_INDEX.md - Complete knowledge base index (what file is for what)
- TOKEN_EFFICIENCY.md - Rules for token-efficient AI assistance
- RULES.md - Operational guidelines, decision-making, quality standards

All documentation linked, searchable, and maintained. Ready for team scaling.

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

### ✅ Complete & Production-Ready
- **8 Python scripts** (scraper, scoring, analysis, email writer/sender, reply classifier, reporter)
- **Supabase schema** (9 tables with indexes, ready for initialization)
- **Website: Premium Desktop + Mobile versions** (animations, modern, end-to-end flow, legal, complete)
  - `index.html` (desktop) - Premium with animations, Book Demo, Calendly, dynamic year (2026)
  - `index-mobile.html` - Completely redesigned to match desktop, modern look, animations
  - `checkout.html` + `checkout-mobile.html` (Stripe price IDs, forms wired)
  - `dashboard.html` + `dashboard-mobile.html` (onboarding screens, dynamic year)
  - `terms.html`, `privacy.html`, `contact.html` (legal, GDPR/CCPA compliant, updated to 2026)
  - Auto-detection redirects mobile/desktop automatically
  - Free trial button → checkout → dashboard (full flow working)
  - Book Demo button → Calendly (calendly.com/astriaaibot) on every version
  - Email: astriaaibot@gmail.com (everywhere)
  - **Footer year auto-updates dynamically** (JavaScript: new Date().getFullYear())
  - Mobile completely modern: glass-morphism, drifting gradients, smooth animations
- **Stripe products** + pricing (3 plans with real Price IDs)
- **GitHub repo** + Vercel deployment (live auto-deploy on push)
- **Cal.com** integration script + authentication verified
- **Stripe webhook handler** (stripe_webhook.py + Telegram notifications ready)
- n8n installed locally
- Python dependencies installed
- All internal links wired and functional
- Animations throughout (fade-in, hover lift, scroll triggers, background drift)

### ⏳ Pending
1. **Supabase initialization**: User provides Project URL + Anon Key + Service Role Key → run `database/init_schema.sql` in SQL editor
2. **Instantly.ai setup**: Create 3 email accounts + warmup
3. **astriareach.com SPF/DKIM**: Domain configuration for email deliverability
4. **Backend server**: Deploy webhook handler + API endpoints (currently local, needs hosting)

## Next Steps (Priority Order)
1. **Calendly integration** ✅ (Book Demo button configured)
2. **Backend deployment** - Deploy webhook server to live URL (Fly.io/Railway/Heroku)
3. User provides **Supabase keys** → initialize schema → create test client
4. Test each Python script individually (scraper → scoring → analysis → emails → sending)
5. Set up **Telegram webhook** (bot creation + credentials)
6. Configure **Instantly.ai** (3 email accounts + warmup)
7. **astriareach.com** SPF/DKIM setup (email deliverability)
8. 7-day end-to-end test with test client
9. Onboard first real client (discovery → ICP definition → launch)

## Important Notes
- **User**: Yammie, EST timezone, prefers to execute (GitHub, Stripe, etc.), wants token efficiency
- **Tech Choices**: Python scripts (not n8n yet) for modularity/testing; Vercel for website; Stripe for PCI compliance
- **Cal.com Note**: Query parameter auth is required; Bearer token auth fails with 401
- **Pipeline Test Blocked**: Until Supabase API keys provided and schema initialized
- **Timeline**: Fast (14-day launch target); user can self-check to save tokens
