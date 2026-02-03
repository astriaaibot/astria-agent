# Astria Knowledge Base Index

Complete reference guide to all Astria documentation, organized by purpose.

---

## 📋 Core Documentation

### Project Overview
- **[ROADMAP.md](./ROADMAP.md)** - Product roadmap, milestones, phases (MVP → Scale → Enterprise)
- **[README.md](./README.md)** - Project overview, getting started
- **[BUILDOUT.md](./BUILDOUT.md)** - Original construction notes and decisions

### This Document
- **[PERSONALITY.md](./PERSONALITY.md)** - Brand voice, personality, communication style
- **[CREDENTIALS.md](./CREDENTIALS.md)** - API keys, platform access, secrets reference
- **[TOKEN_EFFICIENCY.md](./TOKEN_EFFICIENCY.md)** - Rules for efficient token usage
- **[RULES.md](./RULES.md)** - Operational guidelines and best practices

---

## 🏗️ Technical Documentation

### Website & Frontend
- **[website/README.md](./website/README.md)** - Website structure, files, deployment
- **[website/DEPLOY.md](./website/DEPLOY.md)** - Deployment checklist, live URLs
- **[website/MOBILE_DESIGN.md](./website/MOBILE_DESIGN.md)** - Mobile-first strategy, design differences
- **[website/MOBILE_TEST.md](./website/MOBILE_TEST.md)** - Testing guide for mobile/desktop
- **[website/LEGAL_SETUP.md](./website/LEGAL_SETUP.md)** - Legal pages, compliance info

### Backend & Integrations
- **[stripe/STRIPE_SETUP.md](./stripe/STRIPE_SETUP.md)** - Stripe configuration, products, pricing
- **[webhook/README.md](./webhook/README.md)** - Webhook handler overview
- **[webhook/WEBHOOK_SETUP.md](./webhook/WEBHOOK_SETUP.md)** - Stripe webhook setup (complete guide)
- **[webhook/TELEGRAM_QUICK_SETUP.md](./webhook/TELEGRAM_QUICK_SETUP.md)** - Telegram bot setup (2 min)

### Database
- **[database/init_schema.sql](./database/init_schema.sql)** - Supabase schema (9 tables)

### Python Scripts
- **[scraper/scrape_leads.py](./scraper/scrape_leads.py)** - Lead generation from Google Maps
- **[scoring/score_leads.py](./scoring/score_leads.py)** - Claude AI lead scoring (1-10)
- **[analysis/analyze_websites.py](./analysis/analyze_websites.py)** - Website analysis for personalization
- **[emails/write_sequences.py](./emails/write_sequences.py)** - 3-email sequence generation
- **[emails/send_emails.py](./emails/send_emails.py)** - Email sending via Instantly.ai
- **[replies/classify_replies.py](./replies/classify_replies.py)** - Reply classification & response
- **[reporting/send_weekly_report.py](./reporting/send_weekly_report.py)** - Weekly metrics report

### Setup & Configuration
- **[PHASE1_ACCOUNT_CREATION.md](./PHASE1_ACCOUNT_CREATION.md)** - Account setup, initial configuration
- **[QUICK_START.md](./QUICK_START.md)** - Quick reference to get started
- **[TEST_SETUP.md](./TEST_SETUP.md)** - Testing environment setup
- **[RUN_PIPELINE.md](./RUN_PIPELINE.md)** - How to run the full pipeline locally

---

## 📊 Status & Planning

### Current Status
- **[WORK_COMPLETED.md](./WORK_COMPLETED.md)** - What's been built (detailed checklist)
- **[ASTRIA_SPRINT.md](./ASTRIA_SPRINT.md)** - Sprint notes and daily updates

### Memory (Session Context)
- **[memory/astria-project-state.md](./memory/astria-project-state.md)** - Current project state, key decisions, next steps
- **[memory/YYYY-MM-DD.md](./memory/)** - Daily notes (created as needed)

---

## 🎯 Quick Reference

### By Role

**Product Manager (Yammie)**
- Start: [ROADMAP.md](./ROADMAP.md) - Understand the plan
- Next: [CREDENTIALS.md](./CREDENTIALS.md) - Know what's available
- Then: [memory/astria-project-state.md](./memory/astria-project-state.md) - Current status
- Daily: [RULES.md](./RULES.md) - How we operate

**Developer (Future)**
- Start: [README.md](./README.md) - Project overview
- Setup: [QUICK_START.md](./QUICK_START.md) - Local environment
- Code: [website/](./website/), [scraper/](./scraper/), [webhook/](./webhook/)
- Test: [TEST_SETUP.md](./TEST_SETUP.md) and [RUN_PIPELINE.md](./RUN_PIPELINE.md)
- Deploy: [website/DEPLOY.md](./website/DEPLOY.md) and [webhook/WEBHOOK_SETUP.md](./webhook/WEBHOOK_SETUP.md)

**Sales/Support (Future)**
- Start: [PERSONALITY.md](./PERSONALITY.md) - Our voice
- Product: [ROADMAP.md](./ROADMAP.md) - What we offer
- Pricing: [stripe/STRIPE_SETUP.md](./stripe/STRIPE_SETUP.md) - Plans & pricing
- Legal: [website/LEGAL_SETUP.md](./website/LEGAL_SETUP.md) - Compliance, T&C
- Onboarding: [PHASE1_ACCOUNT_CREATION.md](./PHASE1_ACCOUNT_CREATION.md) - How to get started

---

### By Topic

**Getting Started**
1. [README.md](./README.md)
2. [QUICK_START.md](./QUICK_START.md)
3. [PHASE1_ACCOUNT_CREATION.md](./PHASE1_ACCOUNT_CREATION.md)

**Website & Frontend**
1. [website/README.md](./website/README.md)
2. [website/MOBILE_DESIGN.md](./website/MOBILE_DESIGN.md)
3. [website/DEPLOY.md](./website/DEPLOY.md)

**Payments & Billing**
1. [stripe/STRIPE_SETUP.md](./stripe/STRIPE_SETUP.md)
2. [webhook/WEBHOOK_SETUP.md](./webhook/WEBHOOK_SETUP.md)
3. [webhook/TELEGRAM_QUICK_SETUP.md](./webhook/TELEGRAM_QUICK_SETUP.md)

**Database**
1. [database/init_schema.sql](./database/init_schema.sql)
2. [BUILDOUT.md](./BUILDOUT.md) - Schema decisions

**Lead Generation Pipeline**
1. [RUN_PIPELINE.md](./RUN_PIPELINE.md)
2. [scraper/scrape_leads.py](./scraper/scrape_leads.py)
3. [scoring/score_leads.py](./scoring/score_leads.py)
4. [analysis/analyze_websites.py](./analysis/analyze_websites.py)
5. [emails/write_sequences.py](./emails/write_sequences.py)
6. [emails/send_emails.py](./emails/send_emails.py)

**Email & Communication**
1. [webhook/TELEGRAM_QUICK_SETUP.md](./webhook/TELEGRAM_QUICK_SETUP.md)
2. [emails/send_emails.py](./emails/send_emails.py)
3. [reporting/send_weekly_report.py](./reporting/send_weekly_report.py)

**Operations & Culture**
1. [PERSONALITY.md](./PERSONALITY.md)
2. [RULES.md](./RULES.md)
3. [TOKEN_EFFICIENCY.md](./TOKEN_EFFICIENCY.md)
4. [CREDENTIALS.md](./CREDENTIALS.md)

---

## 📂 File Structure

```
/workspace
├── ROADMAP.md                          # Product roadmap
├── PERSONALITY.md                      # Brand voice & personality
├── CREDENTIALS.md                      # API keys, secrets, access
├── TOKEN_EFFICIENCY.md                 # Token usage rules
├── RULES.md                            # Operational guidelines
├── KB_INDEX.md                         # This file
│
├── README.md                           # Project overview
├── QUICK_START.md                      # Quick reference
├── BUILDOUT.md                         # Construction notes
├── WORK_COMPLETED.md                   # What's done
├── ASTRIA_SPRINT.md                    # Sprint notes
│
├── PHASE1_ACCOUNT_CREATION.md          # Setup guide
├── TEST_SETUP.md                       # Testing environment
├── RUN_PIPELINE.md                     # Pipeline execution
│
├── website/
│   ├── README.md
│   ├── DEPLOY.md
│   ├── MOBILE_DESIGN.md
│   ├── MOBILE_TEST.md
│   ├── LEGAL_SETUP.md
│   ├── index.html                      # Desktop landing
│   ├── index-mobile.html               # Mobile landing
│   ├── checkout.html                   # Desktop checkout
│   ├── checkout-mobile.html            # Mobile checkout
│   ├── dashboard.html                  # Desktop dashboard
│   ├── dashboard-mobile.html           # Mobile dashboard
│   ├── terms.html                      # Terms of Service
│   ├── privacy.html                    # Privacy Policy
│   ├── contact.html                    # Contact page
│   └── ...
│
├── stripe/
│   ├── STRIPE_SETUP.md
│   ├── products.json
│   └── setup_products.py
│
├── webhook/
│   ├── README.md
│   ├── WEBHOOK_SETUP.md
│   ├── TELEGRAM_QUICK_SETUP.md
│   ├── stripe_webhook.py
│   └── requirements.txt
│
├── database/
│   └── init_schema.sql
│
├── scraper/
│   └── scrape_leads.py
│
├── scoring/
│   └── score_leads.py
│
├── analysis/
│   └── analyze_websites.py
│
├── emails/
│   ├── write_sequences.py
│   └── send_emails.py
│
├── replies/
│   └── classify_replies.py
│
├── reporting/
│   └── send_weekly_report.py
│
├── memory/
│   ├── astria-project-state.md
│   └── YYYY-MM-DD.md (daily notes)
│
└── .env (local, never commit)
```

---

## 🔍 Search Guide

**Looking for...?**

| Question | Answer |
|----------|--------|
| How do I get started? | [QUICK_START.md](./QUICK_START.md) |
| What's the roadmap? | [ROADMAP.md](./ROADMAP.md) |
| Where are the APIs? | [CREDENTIALS.md](./CREDENTIALS.md) |
| How do I write a feature? | [PERSONALITY.md](./PERSONALITY.md) |
| How do I use tokens efficiently? | [TOKEN_EFFICIENCY.md](./TOKEN_EFFICIENCY.md) |
| What are the rules? | [RULES.md](./RULES.md) |
| How do I deploy? | [website/DEPLOY.md](./website/DEPLOY.md) or [webhook/WEBHOOK_SETUP.md](./webhook/WEBHOOK_SETUP.md) |
| How do I run the pipeline? | [RUN_PIPELINE.md](./RUN_PIPELINE.md) |
| What's the database schema? | [database/init_schema.sql](./database/init_schema.sql) |
| How do I set up Telegram? | [webhook/TELEGRAM_QUICK_SETUP.md](./webhook/TELEGRAM_QUICK_SETUP.md) |
| What's our brand voice? | [PERSONALITY.md](./PERSONALITY.md) |
| Current project status? | [memory/astria-project-state.md](./memory/astria-project-state.md) |
| What's been built? | [WORK_COMPLETED.md](./WORK_COMPLETED.md) |

---

## 🔄 Documentation Maintenance

### When Adding New Features
1. Create relevant .md file(s)
2. Add entry to this KB_INDEX
3. Link from related documentation
4. Update [ROADMAP.md](./ROADMAP.md) if it's a major feature

### When Updating Information
1. Change the relevant .md file
2. Update this index if structure changes
3. Note in [memory/astria-project-state.md](./memory/astria-project-state.md) if major change
4. Never delete old docs (archive instead)

### Archival Files
These are for reference/history:
- [BUILDOUT.md](./BUILDOUT.md)
- [WORK_COMPLETED.md](./WORK_COMPLETED.md)
- [ASTRIA_SPRINT.md](./ASTRIA_SPRINT.md)

---

**Last Updated:** February 3, 2026  
**Maintained By:** Astria AI Assistant  
**Next Review:** When KB exceeds 20 files or 100KB
