# Farcaster Integration Status

## Overview

Astria is now ready to launch on Farcaster with a complete integration strategy, skill library, and production-ready code.

---

## What's Been Built

### 1. Farcaster Skill (Production-Ready)

**Location:** `skills/farcaster/SKILL.md` (13KB)

**Includes:**
- Complete API reference
- Post, reply, engage patterns
- Frame building guide
- Automation examples
- Error handling & troubleshooting
- Rate limits & costs

**Status:** ✅ Ready to use (can be shared with other projects)

### 2. Astria-Specific Integration Guide

**Location:** `FARCASTER_ASTRIA.md` (12KB)

**Includes:**
- Phase 1: Account setup (clawcaster)
- Phase 2: Content strategy (5 post types, channel selection)
- Phase 3: Interactive Frames (demo booking, lead gen, results)
- Phase 4: Analytics & optimization
- Integration with existing email pipeline
- Complete checklist

**Status:** ✅ Ready to execute

### 3. API Reference Documentation

**Location:** `skills/farcaster/references/API_REFERENCE.md` (8KB)

**Includes:**
- Neynar API endpoints (all methods)
- Request/response examples
- Key data structures
- Byte length calculator
- Error responses
- Rate limit info
- Testing checklist

**Status:** ✅ Complete reference

### 4. Production Python Client

**Location:** `skills/farcaster/scripts/farcaster_client.py` (12KB)

**Includes:**
- FarcasterClient class
- Methods: post_cast, reply, thread, get_mentions, get_feed
- Reactions: like, recast
- Search: search_casts, search_users, get_user
- Utilities: preview_cast
- Logging & error handling

**Status:** ✅ Ready to import and use

---

## Telegram Bot Setup

### Astria Bot (@Astriapeoplebot)

```
Token: 8394189992:AAF59O_hq9T1Fi_sTcfRUpks8X72t_nsrHc
Chat ID: 8516106442
Purpose: Notifications (new customers, errors, reports)
Status: ✅ Configured
```

### Gilfoyle Bot (@gifoylebot)

```
Token: 8106741522:AAEGy-UH1XrZ9wU-x1XTQrzgdGFKxlPJ8lU
Persona: Dark engineer (cynical, brilliant, competent)
Purpose: TBD (user decides functionality)
Status: ✅ Created, awaiting direction
```

---

## Next Steps to Launch

### Week 1: Account & Setup

**Day 1:**
- [ ] Get clawcaster skill
- [ ] Generate custody wallet
- [ ] Register Farcaster account (@astria or similar)
- [ ] Get FID + signer UUID

**Day 2:**
- [ ] Create Neynar account (neynar.com)
- [ ] Get API key (free tier: 300 req/min)
- [ ] Set Farcaster profile (username, bio, avatar)
- [ ] Store credentials in `.env.farcaster`

### Week 2: Content & Engagement

**Day 3-4:**
- [ ] Write 5 days of posts (using content templates)
- [ ] Schedule posts using farcaster_client.py
- [ ] Engage with /dev, /ai, /base channels
- [ ] Reply to mentions manually

**Day 5-7:**
- [ ] Analyze engagement metrics
- [ ] Refine post strategy based on performance
- [ ] Build audience (follows)
- [ ] Identify hot prospects

### Week 3: Frames & Automation

**Day 8-10:**
- [ ] Design demo booking Frame
- [ ] Build Frame endpoint (Flask/FastAPI)
- [ ] Deploy to production
- [ ] Test from Farcaster client

**Day 11-14:**
- [ ] Build lead generation Frame
- [ ] Build results showcase Frame
- [ ] Set up automated daily posts (cron)
- [ ] Set up mention tracking + auto-reply

---

## Integration with Existing Pipeline

### Current Astria Pipeline
```
Google Maps Scrape
    ↓
Score Leads (Claude)
    ↓
Analyze Websites
    ↓
Write Email Sequences
    ↓
Send via Instantly.ai
    ↓
Classify Replies
    ↓
Respond to Hot Leads
    ↓
Book Appointment (Cal.com)
```

### New: Farcaster Layer (Parallel)
```
Post on Farcaster (Daily)
    ↓
Capture Mentions / Frame Clicks
    ↓
Qualify Inbound Leads
    ↓
Store in Supabase (farcaster_leads table)
    ↓
Run through Scoring (same Claude AI)
    ↓
Send Personalized Message OR Book Direct
    ↓
Track Conversion → Customer
```

**Key Benefits:**
- 2nd channel for lead generation
- Builder-focused audience (high-quality leads)
- Direct engagement (no algorithm)
- Async sales (while email pipeline runs)
- Brand building on decentralized network

---

## Metrics to Track

### Engagement Metrics
- Casts per week
- Average likes per cast
- Recasts per cast (amplification)
- Replies per cast
- Engagement rate (total interactions / followers)

### Lead Metrics
- Mentions per week
- Frame clicks (demo + lead gen)
- Leads captured via Farcaster
- Qualified leads (scoring > 6)
- Demos booked

### Business Metrics
- Cost per Farcaster lead
- Farcaster lead to customer conversion
- Customer LTV (Farcaster-sourced)
- Revenue per dollar spent

---

## Content Strategy

### 5 Post Types (Rotate)

**Type 1: Lead Summary (Monday)**
```
🔍 Astria This Week: 248 qualified leads
📊 Top: Plumbing (42), Electrician (38), HVAC (35)
🎯 Interesting pattern: Local services in tech hubs getting more inbound
📝 Case study coming Friday
```

**Type 2: Case Study / Result (Tuesday-Thursday)**
```
📈 Client Win: Electrician in Austin

Weeks 1-3: Generated 156 leads
Weeks 4-6: 12 qualified appointments
Result: $34k in new contracts

Here's what worked...
```

**Type 3: Feature / Insight (Wednesday)**
```
✨ NEW: Real-time reply classification

Astria now auto-categorizes inbound responses:
✅ Interested
⏸️ Maybe later
❌ Not interested

Helps focus on hot leads. Live with 3 clients.
```

**Type 4: Ask / Engagement (Any day)**
```
Question for builders:

How do you currently find new customers for your service?
- Referrals
- Google
- Social media
- Outbound
- Other (reply)

Curious about local service biz 👇
```

**Type 5: Booking / CTA (Friday)**
```
Want to see Astria in action?

Generate 50+ qualified leads for your service business in 7 days.

See a live demo: [Book Demo button]

[Link to Frames]
```

---

## Channels to Target

| Channel | Why | Posting Frequency |
|---------|-----|---|
| /dev | Builders, founders, tech tools | 2x/week |
| /ai | AI agents, automation | 2x/week |
| /base | Crypto-adjacent, onchain | 1x/week |
| general | Broader announcements | 1x/week |
| /frames | Frame launches | As needed |

---

## Success Criteria

### Month 1
- [ ] 100+ followers
- [ ] 5-10 Farcaster-sourced leads
- [ ] 1-2 demos booked via Farcaster
- [ ] High engagement rate (>5%)

### Month 2
- [ ] 300+ followers
- [ ] 20-30 Farcaster-sourced leads
- [ ] 5-10 demos booked
- [ ] 1-2 customers acquired (Farcaster channel)

### Month 3
- [ ] 500+ followers
- [ ] 50+ leads/month from Farcaster
- [ ] 10-15 demos/month
- [ ] 3-5 customers acquired
- [ ] Farcaster = 10-15% of new revenue

---

## Risks & Mitigation

| Risk | Likelihood | Mitigation |
|------|-----------|-----------|
| Low engagement | Medium | Strong content strategy, consistent posting |
| Spam/criticism | Low | Selective replies, transparent about AI |
| Rate limiting | Low | Monitor API usage, batch requests |
| Account shadowban | Low | Follow guidelines, don't spam, quality posts |
| Frame bugs | Medium | Test thoroughly, monitor errors |

---

## Resource Links

**Official:**
- Neynar Docs: https://docs.neynar.com
- Farcaster Docs: https://docs.farcaster.xyz
- OnchainKit: https://onchainkit.xyz
- Mini Apps: https://miniapps.farcaster.xyz

**Setup:**
- Clawcaster: https://clawcaster.com
- Neynar: https://neynar.com
- FarcasterForAgents: https://github.com/ZeniLabs/FarcasterForAgents

**Community:**
- GM Farcaster: https://gmfarcaster.com
- Farcaster Protocol: https://github.com/farcasterxyz/protocol

---

## Files Created

```
workspace/
├── FARCASTER_ASTRIA.md (12KB) - Integration guide
├── FARCASTER_STATUS.md (this file)
├── .env.farcaster (template)
└── skills/farcaster/
    ├── SKILL.md (13KB) - Production skill
    ├── references/
    │   └── API_REFERENCE.md (8KB)
    └── scripts/
        └── farcaster_client.py (12KB)
```

---

## Summary

✅ **Farcaster skill is production-ready**  
✅ **Astria integration guide complete**  
✅ **Python client library built**  
✅ **Telegram bots configured**  
✅ **Clear path to launch (1-2 weeks)**  

🚀 **Ready to start building Astria's presence on Farcaster**

---

**Created:** Feb 3, 2026  
**Status:** ✅ Implementation ready  
**Confidence:** High  
**Next:** User decides when to start (after or alongside email pipeline)
