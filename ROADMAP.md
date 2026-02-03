# Astria Product Roadmap - 2026

## Vision
Astria is an autonomous AI sales agent for local service businesses. Complete automation of lead generation, scoring, personalization, outreach, reply handling, and appointment booking.

---

## Phase 1: MVP (Current - COMPLETE ✅)
**Timeline:** 14 days  
**Status:** 95% Complete, Ready for Testing

### Launched
- ✅ **Website** - Premium desktop + mobile (animations, modern design)
- ✅ **Landing Page** - Book Demo, Free Trial CTA, responsive
- ✅ **Legal** - Terms, Privacy, Contact pages (GDPR/CCPA compliant)
- ✅ **Checkout Flow** - Stripe integrated, 3 pricing tiers
- ✅ **Dashboard** - Post-signup onboarding screens
- ✅ **8 Python Scripts** - Complete lead generation → reporting pipeline
- ✅ **Supabase Schema** - 9 tables, ready for initialization
- ✅ **Cal.com Integration** - Verified API, booking configured
- ✅ **Stripe Setup** - 3 products, webhooks, pricing configured
- ✅ **GitHub** - Repo live, auto-deployed to Vercel
- ✅ **Footer Year** - Dynamic (auto-updates 2026)
- ✅ **Email** - astriaaibot@gmail.com configured everywhere

### Immediate Next (This Week)
- [ ] **Backend Deployment** (30 min) - Deploy webhook server to Fly.io/Railway
- [ ] **Supabase Initialize** (15 min) - Run schema SQL with user-provided keys
- [ ] **Telegram Setup** (10 min) - Create bot, configure webhook notifications
- [ ] **Instantly.ai Config** (1 hour) - 3 email accounts + warmup setup
- [ ] **astriareach.com SPF/DKIM** (30 min) - Email deliverability config
- [ ] **End-to-End Test** (1 day) - Full pipeline: leads → scoring → emails → replies

---

## Phase 2: Production Ready (Week 2-3)
**Timeline:** 7-10 days  
**Goal:** First paying customer live

### Requirements
- ✅ All integrations working (Supabase, Stripe, Cal.com, Instantly.ai, Telegram)
- ✅ Pipeline tested end-to-end
- ✅ Website fully functional (checkout → dashboard → campaign launch)
- ✅ Lead quality validated (50+ leads/day, 40%+ open rate target)
- ✅ Reply handling working (AI responds to objections)
- ✅ Booking integration active (prospects → Cal.com → calendar)

### Deliverables
- [ ] **Client Onboarding Flow** - ICP questionnaire → configuration → launch
- [ ] **Customer Dashboard v1** - Real-time metrics (leads, opens, replies, calls)
- [ ] **Weekly Report Automation** - Friday reports to customer email
- [ ] **Support Email** - astriaaibot@gmail.com monitored and responsive
- [ ] **Monitoring & Alerts** - Track pipeline health, error notifications

### Success Metrics
- 50+ leads generated per plan tier per week ✓
- 40%+ email open rate ✓
- 3.2%+ reply rate ✓
- 8-12 booked calls per customer per month ✓
- 98%+ email deliverability ✓

---

## Phase 3: Scale & Growth (Week 4+)
**Timeline:** Ongoing  
**Goal:** 20+ customers, predictable revenue

### Customer Growth
- [ ] **Product-Market Fit** - Validate pricing, messaging, ICP
- [ ] **Case Studies** - 3-5 customers with >10 closed deals
- [ ] **Referral Program** - Incentivize word-of-mouth
- [ ] **Sales Playbook** - Documented sales process, objection handling
- [ ] **Customer Success** - Dedicated support, onboarding SOP

### Product Improvements
- [ ] **Advanced Personalization** - Website copy analysis, industry-specific templates
- [ ] **Multi-Channel Outreach** - LinkedIn, Twitter, SMS in addition to email
- [ ] **CRM Integration** - HubSpot, Salesforce, Pipedrive sync
- [ ] **Analytics Dashboard** - Advanced filters, custom reporting, forecasting
- [ ] **A/B Testing** - Subject lines, email templates, timing optimization

### Operations
- [ ] **Billing Automation** - Recurring charges, invoicing, dunning
- [ ] **Customer Portal** - Self-service ICP updates, campaign management
- [ ] **API** - REST API for integrations (CRM, webhooks, etc.)
- [ ] **Mobile App** - Native iOS/Android for on-the-go monitoring

---

## Phase 4: Enterprise (Month 3+)
**Timeline:** Ongoing  
**Goal:** $50k+ MRR, enterprise customers

### Enterprise Features
- [ ] **White Label** - Custom domain, branding
- [ ] **Team Management** - Multiple users per account, role-based access
- [ ] **Advanced Compliance** - HIPAA, SOC2, enterprise agreements
- [ ] **Dedicated Infrastructure** - Private deployments for large customers
- [ ] **Premium Support** - 24/7, dedicated success manager

### Market Expansion
- [ ] **Vertical Templates** - Plumbing, HVAC, Electrical, Cleaning, Landscaping
- [ ] **Geographic Expansion** - Canada, UK, Australia
- [ ] **Partnerships** - Integrations with software platforms, agencies

---

## Pricing Timeline

### Current (MVP)
- **Starter:** $299/month (50 leads/week, 1 sequence, 1 calendar)
- **Standard:** $699/month (200 leads/week, 3 sequences, 3 calendars) ← Most popular
- **Enterprise:** $1,299/month (500 leads/week, unlimited)
- **Setup Fee:** $199 (one-time onboarding)

### Phase 2 Adjustments (Pending)
- Monitor conversion rates, churn, payback period
- Adjust pricing based on customer feedback
- Introduce annual billing discount (10% off)

### Phase 3+ (Future)
- Usage-based pricing (pay per lead)
- Industry-specific pricing
- Enterprise custom pricing

---

## Revenue Targets

### Year 1
| Milestone | Customer Count | MRR | Target Month |
|-----------|----------------|-----|--------------|
| First customer | 1 | $699 | Feb 2026 |
| Break-even (5 customers) | 5 | $3,495 | Mar 2026 |
| Proof of concept (10 customers) | 10 | $6,990 | Apr 2026 |
| Scale validation (20 customers) | 20 | $13,980 | Jun 2026 |
| Real business (50 customers) | 50 | $34,950 | Sep 2026 |
| Sustainable (100 customers) | 100 | $69,900 | Dec 2026 |

### Gross Margin
- **Current:** 70-86% (infrastructure + AI costs minimal)
- **Target:** 75%+ (scale benefits)

### Unit Economics
- **LTV (2-year):** $16,776 (avg customer pays $699/mo × 24mo)
- **CAC:** TBD (depends on acquisition channel)
- **Payback Period:** <3 months (favorable)

---

## Technical Roadmap

### MVP (Done ✅)
- Python scripts (lead gen, scoring, email, replies, reporting)
- Supabase database (9 tables)
- Stripe payment processing
- Cal.com calendar integration
- Vercel website hosting
- GitHub CI/CD pipeline
- Webhook handler (local)

### Phase 2 (In Progress)
- Backend deployment (Fly.io/Railway/Heroku)
- Supabase initialization (production keys)
- Telegram webhook notifications
- Instantly.ai email integration
- Email deliverability (SPF/DKIM)
- End-to-end testing framework

### Phase 3
- REST API (public endpoints)
- Advanced analytics dashboard
- CRM integrations (HubSpot, Salesforce)
- ML personalization (Claude prompt optimization)
- Multi-channel outreach (LinkedIn, Twitter, SMS)
- Rate limiting & security hardening

### Phase 4
- Microservices architecture
- Horizontal scaling (lead processing)
- Multi-region deployment
- Private API deployments
- White-label hosting

---

## Risk Mitigation

### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Email deliverability issues | Medium | High | Early testing with Instantly.ai, SPF/DKIM setup |
| Lead quality poor | Medium | High | Refine ICP, A/B test scoring, validate with pilot |
| Stripe webhook failures | Low | Medium | Monitoring, retry logic, admin dashboard |
| Supabase scaling limits | Low | Medium | Plan scaling from day 1, benchmark growth |

### Market Risks
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Competitors enter market | Medium | High | Faster go-to-market, build moat with integrations |
| Customers churn | Medium | High | Focus on retention, dedicated support, product improvements |
| Pricing too high | Medium | Medium | Validate with early customers, offer annual discount |
| Sales cycle longer than expected | Medium | Medium | Start with warm leads (referrals), case studies |

---

## Key Dates & Milestones

**2026**
- **Feb 3 (Today)** - MVP complete, website live
- **Feb 7** - Backend deployed, first customer signing up
- **Feb 14** - Production testing complete, first $699 payment
- **Feb 21** - 3 customers, $2,097 MRR
- **Mar 7** - Break-even (5 customers), launch case studies
- **Apr 4** - 10 customers, proof of concept validated
- **Jun 1** - 20 customers, $13,980 MRR
- **Sep 1** - 50 customers, $34,950 MRR
- **Dec 1** - 100 customers, $69,900 MRR

---

## Success Definition

**MVP Success:** 5 customers, $3,495 MRR, 70%+ satisfaction  
**Year 1 Success:** 100 customers, $69,900 MRR, <30% churn  
**Year 2 Success:** 500+ customers, $350k+ MRR, expansion into new verticals

---

## Notes
- This roadmap is flexible and will evolve based on customer feedback
- Priority is customer satisfaction and retention over aggressive growth
- Each phase should be validated before proceeding to next
- Monthly reviews of metrics, customer feedback, and market changes
