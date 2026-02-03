# ASTRIA BUILDOUT PLAN
**Autonomous AI Sales Agent for Local Service Businesses**

---

## OVERVIEW

This plan breaks the Astria Agent Execution Guide into 7 phases. Each phase has clear deliverables, dependencies, and success criteria. Target timeline: **4 weeks for full build** (2 weeks for MVP).

**Start Date:** 2026-02-03  
**Full Launch Target:** 2026-03-03  
**MVP Target:** 2026-02-17

---

## PHASE 1: INFRASTRUCTURE & ACCOUNTS (Days 1–3)

### What Gets Done
Set up all third-party services, accounts, and API keys. Verify connectivity.

### Accounts to Create

| Service | Purpose | Cost | Setup Time | API Key Needed |
|---------|---------|------|-----------|---|
| **Supabase** | Database (leads, emails, opportunities) | Free tier | 15 min | Yes |
| **n8n** (self-hosted on Mac) | Automation engine | Free (Community) | 30 min | Yes |
| **Instantly.ai** | Email sending platform | $25/mo (base) | 20 min | Yes |
| **Cal.com** | Appointment scheduling | Free tier | 15 min | Yes |
| **Stripe** | Payment processor | Free to set up | 20 min | Yes |
| **Claude API** | AI scoring, writing, monitoring | Pay-as-you-go (~$50/mo estimated) | 10 min | Yes |
| **Google Maps Scraper** | Lead discovery | Free (open source) | 30 min | N/A |
| **Domain: astria.fun** | Main brand domain | Check status | — | — |
| **Sending Domain** | Email authentication (SPF/DKIM) | $0–10/mo | 45 min | — |

### Deliverables

- [ ] Supabase project created, databases initialized
- [ ] n8n instance running locally, accessible at `http://localhost:5678`
- [ ] 3 Instantly.ai sending accounts created (warmup initiated)
- [ ] Cal.com account set up with Discovery Call event type
- [ ] Stripe account ready for $500/mo + $250 setup fee billing
- [ ] Claude API key stored securely (1Password or .env)
- [ ] All API keys documented in a secure location
- [ ] Google Maps scraper installed and tested locally

### Cost Summary (Month 1)
- Supabase: $0 (free tier, <1GB)
- n8n: $0 (self-hosted)
- Instantly.ai: $25 (3 accounts)
- Cal.com: $0 (free tier)
- Stripe: $0 (no fees until transaction)
- Claude API: ~$50 (estimated, pay-as-you-go)
- Domain renewal: ~$10 (if needed)
- Sending domain: $0–10

**Total: ~$85–95/month**

### Success Criteria
- All 8 services are live and connectable
- API keys stored and accessible
- n8n dashboard loads
- Supabase shows empty tables
- Instantly accounts in "warming up" state

---

## PHASE 2: DATABASE SCHEMA & TABLES (Days 3–4)

### What Gets Done
Create Supabase tables to match the data flows in the execution guide.

### Tables to Create

#### 1. **clients**
```
id (PK)
business_name (text)
contact_name (text)
email (text)
phone (text)
category (text) — HVAC, plumbing, electrical, roofing, etc.
service_area_cities (array)
service_area_zips (array)
icp_filters (jsonb) — min reviews, must have website, etc.
stripe_customer_id (text)
stripe_subscription_id (text)
subscription_status (enum: active, canceled, past_due)
subscription_tier (text) — $500, $1000, $1500
monthly_lead_target (int)
onboarding_stage (enum: discovery, setup, testing, live)
launched_date (timestamp)
created_date (timestamp)
```

#### 2. **leads**
```
id (PK)
client_id (FK → clients)
business_name (text)
phone (text)
email (text)
website (text)
address (text)
city (text)
state (text)
zip (text)
google_rating (float)
review_count (int)
category (text)
place_id (text) — Google Maps unique ID
scraped_date (date)
status (enum: new, qualified, cold, analyzed, contacted, engaged, opportunity, appointment_booked, no_show, stale, opted_out, no_email, score_error)
score (int 1–10)
tier (enum: hot, warm, cold)
score_reasoning (text)
contacted_date (timestamp)
last_email_date (timestamp)
last_reply_date (timestamp)
created_date (timestamp)
```

#### 3. **lead_details**
```
id (PK)
lead_id (FK → leads)
services (text)
service_area (text)
usp (text) — unique selling point
team (text)
pain_points (text)
personalization_hook (text)
analyzed_date (timestamp)
```

#### 4. **email_sequences**
```
id (PK)
lead_id (FK → leads)
client_id (FK → clients)
subject (text)
body (text)
send_day (int) — 0, 3, or 7
status (enum: pending_review, approved, scheduled, sent, bounced, failed)
created_date (timestamp)
sent_date (timestamp)
sent_from_account (text) — which Instantly account
open_count (int)
click_count (int)
```

#### 5. **replies**
```
id (PK)
lead_id (FK → leads)
client_id (FK → clients)
email_id (FK → email_sequences)
reply_text (text)
received_date (timestamp)
classification (enum: interested, question, objection, not_interested, out_of_office)
confidence (float 0–1)
draft_response (text)
action (enum: send_booking_link, answer_and_follow_up, address_objection, stop_sequence, pause_and_retry)
escalate_to_human (boolean)
escalation_reason (text)
response_sent (boolean)
response_sent_date (timestamp)
```

#### 6. **opportunities**
```
id (PK)
lead_id (FK → leads)
client_id (FK → clients)
first_interested_date (timestamp)
booking_link_sent_date (timestamp)
appointment_booked (boolean)
appointment_date (timestamp)
appointment_time (time)
show_status (enum: scheduled, no_show, completed)
notes (text)
created_date (timestamp)
```

#### 7. **errors**
```
id (PK)
task_name (text) — SCRAPE, SCORE, WRITE, SEND, etc.
error_message (text)
error_details (jsonb)
input_data (jsonb)
timestamp (timestamp)
resolved (boolean)
resolution_notes (text)
```

#### 8. **activities_log**
```
id (PK)
client_id (FK → clients)
lead_id (FK → leads)
activity_type (enum: scraped, scored, analyzed, email_sent, reply_received, appointment_booked, report_sent)
details (jsonb)
timestamp (timestamp)
```

#### 9. **reports**
```
id (PK)
client_id (FK → clients)
week_start (date)
week_end (date)
leads_scraped (int)
leads_scored_hot (int)
leads_scored_warm (int)
emails_sent (int)
replies_received (int)
replies_interested (int)
replies_questions (int)
replies_objections (int)
replies_not_interested (int)
appointments_booked (int)
open_rate (float)
reply_rate (float)
report_text (text)
sent_date (timestamp)
```

### Deliverables
- [ ] All 9 tables created in Supabase
- [ ] All foreign keys established
- [ ] Indexes created on common queries (client_id, lead_id, status, created_date)
- [ ] Sample data inserted (optional, for testing)
- [ ] Backup procedure documented

### Success Criteria
- All tables visible in Supabase dashboard
- Foreign key constraints working
- Sample query (e.g., "get all leads for client X") returns expected results
- Schema diagram exported or documented

---

## PHASE 3: PYTHON SCRAPER & LEAD INGESTION (Days 5–7)

### What Gets Done
Build the lead scraping workflow. Daily at 6:00 AM, find new local service businesses from Google Maps.

### Components

#### 3.1 Google Maps Scraper Setup
```bash
# Install omkarcloud/google-maps-scraper
pip install google-maps-scraper

# Test with a simple query
python -m google_maps_scraper --query "HVAC repair Fort Lauderdale"
```

#### 3.2 Scraper Script (`scraper/scrape_leads.py`)
- Input: client_id, search queries from clients table
- Output: Raw lead data (name, phone, email, website, rating, reviews, place_id)
- Deduplication: Check place_id, phone, business_name + city combo
- Error handling: Retry 3x on fail, log to errors table
- Stores results in `leads` table with status "new"

#### 3.3 Search Query Rotation
- For each client, read their service_area_cities and service_area_zips
- Generate 5–8 unique search queries per day (rotate through variations)
- Example for HVAC client in Broward:
  - "HVAC repair Fort Lauderdale"
  - "air conditioning Pompano Beach"
  - "AC installation Coral Springs"
  - "HVAC contractor Broward County FL"
  - "heating and cooling Plantation FL"

#### 3.4 Rate Limiting & Warmup
- Respect Google Maps rate limits (no more than 2 requests/second)
- Space requests 3–5 seconds apart
- Rotate IP/user agent if possible
- Log success/failure per query

### Deliverables
- [ ] Scraper script written and tested locally
- [ ] Handles 50+ leads/day without errors
- [ ] Deduplication logic verified
- [ ] Error logging works
- [ ] Database inserts validated
- [ ] Search query rotation logic tested
- [ ] n8n workflow skeleton created (even if not fully connected)

### Cost & Dependencies
- **Time:** 2–3 days
- **Cost:** $0 (open source tool)
- **Requires:** Phase 1 (Supabase, Python env) & Phase 2 (database schema)

### Success Criteria
- Script runs daily, finds 30+ unique leads per client
- All leads inserted into `leads` table with status "new"
- Deduplication prevents duplicates
- Errors logged and don't stop the pipeline
- Ready to integrate into n8n workflow

---

## PHASE 4: LEAD SCORING & ANALYSIS (Days 8–10)

### What Gets Done
Daily at 6:30 AM, score every new lead 1–10 using Claude API. Then analyze websites of qualified leads (7:00 AM).

### Components

#### 4.1 Lead Scoring Workflow
- **Trigger:** All leads with status "new"
- **For each lead:** Send to Claude API with scoring prompt
- **Scoring criteria:** Review count, website presence, rating, maturity, category fit, online presence gaps
- **Output:** Score (1–10), Tier (Hot/Warm/Cold), reasoning
- **Update:** Move to "qualified" (if Hot/Warm) or "cold" (if Cold)

#### 4.2 Website Analysis Workflow
- **Trigger:** All leads with status "qualified" that have a website URL
- **For each lead:** 
  - Fetch homepage HTML via HTTP
  - Extract visible text (first 3000 chars)
  - Send to Claude API with analysis prompt
- **Output:** services, service_area, USP, team, pain_points, personalization_hook
- **Store:** In `lead_details` table
- **Update:** Move to "analyzed"

#### 4.3 Fallback for No-Website Leads
- If website fetch fails or no website URL exists:
  - Use fallback hook: "I noticed {business_name} doesn't have a website listed — that's a huge opportunity..."
  - Skip website analysis, move straight to "analyzed"

### Deliverables
- [ ] Claude scoring prompt finalized and tested
- [ ] Claude analysis prompt finalized and tested
- [ ] n8n workflow for Task 2 (SCORE) built and tested
- [ ] n8n workflow for Task 3 (ANALYZE) built and tested
- [ ] Error handling for invalid JSON responses working
- [ ] Website fetch timeout handling working (30s max per URL)
- [ ] Sample leads scored and analyzed manually verified
- [ ] Cost estimate validated (~$0.003/lead for scoring, ~$0.005/lead for analysis)

### Cost & Dependencies
- **Time:** 2–3 days
- **Cost:** ~$0.15/day for 50 leads (Claude API)
- **Requires:** Phase 1 (Claude API key), Phase 2 (database), Phase 3 (leads populated)

### Success Criteria
- Scores are realistic and match rubric
- Hooks are personalized and specific, not generic
- No invalid JSON errors after first attempt
- Website analysis captures real pain points
- Leads move through pipeline: new → qualified → analyzed
- Speed: 50 leads scored + analyzed in <15 minutes

---

## PHASE 5: EMAIL SEQUENCE GENERATION & SENDING (Days 11–14)

### What Gets Done
Daily at 7:30 AM, generate 3-email sequences for analyzed leads. At 9:00 AM, send today's emails through Instantly.

### Components

#### 5.1 Email Writing Workflow
- **Trigger:** All leads with status "analyzed"
- **For each lead:** Send to Claude API with email writing prompt
- **Inputs:** business name, category, location, rating, reviews, website, services, USP, pain points, personalization hook
- **Output:** 3-email JSON array (subject, body, send_day)
- **Quality checks:** Valid JSON, <100 words each, Email 1 references real business, no exclamation marks
- **Store:** In `email_sequences` table
- **Status:** "pending_review" (first 14 days of client) or "approved" (after)

#### 5.2 Email Sending Workflow
- **Trigger:** All emails with status "approved" and send_day matching today
- **Rules:**
  - Never exceed 25 emails/account/day (3 accounts = 75 max)
  - Rotate between accounts evenly
  - Space 3–7 minutes apart
  - Send only 9 AM–1 PM EST
- **For each email:**
  - Check if prospect already replied (if yes, skip)
  - Check if prospect unsubscribed (if yes, skip)
  - Push to Instantly.ai API
  - Update status to "sent"
  - Log send time, account used, campaign_id
- **Update lead:** status to "contacted"

#### 5.3 Immediately Pre-Send
- Check Instantly warmup dashboard
- Verify no bounce rate >2%
- If bounce rate >2% on any account, PAUSE that account immediately and alert operator

### Deliverables
- [ ] Claude email writing prompt finalized and tested
- [ ] Email quality check logic built
- [ ] n8n workflow for Task 4 (WRITE) built and tested
- [ ] n8n workflow for Task 5 (SEND) built and tested
- [ ] Instantly.ai API integration working
- [ ] Email spacing/throttling logic verified (3–7 min between sends)
- [ ] 3 Instantly accounts warmed up and verified
- [ ] Sending domain SPF/DKIM records configured correctly
- [ ] Test batch of 20 emails sent successfully (manual + inspection)
- [ ] Open/bounce rates monitored in Instantly dashboard

### Cost & Dependencies
- **Time:** 3–4 days
- **Cost:** ~$0.005/lead for email generation (Claude API) + Instantly ($25/mo for 3 accounts)
- **Requires:** Phase 1 (Claude, Instantly, n8n), Phase 2 (database), Phase 4 (leads analyzed)

### Success Criteria
- Emails are personalized, under 100 words, no generic jargon
- Subject lines are lowercase and conversational
- No emails sent to unsubscribed/duplicate contacts
- Bounce rate <2% on all sending accounts
- Open rate >30% (target >40%)
- Email sequences are spacing correctly (0, 3, 7 days)
- All sends logged to database
- Sending accounts staying healthy (no suspensions)

---

## PHASE 6: REPLY MONITORING & OPPORTUNITY CREATION (Days 15–18)

### What Gets Done
Continuously (9 AM–6 PM), monitor for email replies. Classify each reply and take action: interested → send booking link, question → answer, objection → address, not interested → stop.

### Components

#### 6.1 Reply Ingestion
- **Source:** Instantly webhook → n8n
- **Data received:** reply text, original email, lead email, campaign ID, timestamp
- **Store:** In `replies` table

#### 6.2 Reply Classification Workflow
- **Trigger:** New reply webhook
- **For each reply:** Send to Claude API with classification prompt
- **Output:** category (interested/question/objection/not_interested/out_of_office), confidence, draft_response, action, escalate_to_human
- **Store:** In `replies` table

#### 6.3 Action Handler
Based on classification:

| Classification | Action | Details |
|---|---|---|
| INTERESTED | send_booking_link | Send draft response + Cal.com link, stop sequence, create opportunity |
| QUESTION | answer_and_follow_up | Send draft response, pause sequence 3 days |
| OBJECTION | address_objection | Send draft response, pause 2 days, then send breakup email |
| NOT_INTERESTED | stop_sequence | Send removal confirmation, add to suppression list immediately |
| OUT_OF_OFFICE | pause_and_retry | No response, pause for 7 days (or return date + 2 days) |

#### 6.4 Response Timing
- INTERESTED: Respond <15 min
- QUESTION: Respond <30 min
- OBJECTION: Respond <1 hour
- NOT_INTERESTED: Respond <1 hour

#### 6.5 Escalation Rules
Escalate to human if:
- Confidence <0.7
- Reply is hostile/threatening
- Reply mentions lawyer, legal, sue, attorney, cease & desist
- Reply asks detailed technical questions
- You can't tell what they want

#### 6.6 Opportunity Creation
When reply = INTERESTED:
- Create record in `opportunities` table
- Update lead status to "opportunity"
- Send Cal.com discovery call link
- Notify operator: "New interested reply from {business_name} in {city}"

### Deliverables
- [ ] Instantly webhook integration set up in n8n
- [ ] Reply classification prompt finalized and tested
- [ ] n8n workflow for Task 6 (MONITOR) built and tested
- [ ] Action handler logic built for all 5 classifications
- [ ] Response timing enforced
- [ ] Escalation logic tested with edge cases
- [ ] Cal.com integration working (booking links embed correctly)
- [ ] Suppression list sync working (not_interested adds to Instantly)
- [ ] Operator notifications working (Telegram/email alerts)
- [ ] Sample replies classified manually and verified

### Cost & Dependencies
- **Time:** 3–4 days
- **Cost:** ~$0.002/reply (Claude API)
- **Requires:** Phase 1 (Claude, Instantly, n8n), Phase 2 (database), Phase 5 (emails being sent)

### Success Criteria
- All reply classifications accurate (manually spot-check 20+ examples)
- Responses sent within target timeframes
- No interested prospects missed
- Cal.com bookings appear on calendar correctly
- Unsubscribe requests honored immediately
- Escalations flagged and operator alerted
- No false positives (e.g., mistaking "maybe later" for not interested)

---

## PHASE 7: APPOINTMENT BOOKING & WEEKLY REPORTING (Days 19–21)

### What Gets Done
When prospects book via Cal.com, update opportunities and notify operator. Every Sunday 8 PM, send clients their weekly report.

### Components

#### 7.1 Appointment Booking Workflow
- **Trigger:** Cal.com webhook (appointment scheduled)
- **Data received:** prospect email, appointment date/time, event type
- **Update opportunities table:**
  - appointment_booked = true
  - appointment_date, appointment_time
  - show_status = "scheduled"
- **Update lead status:** "appointment_booked"
- **Notify operator:** "APPOINTMENT BOOKED: {business_name} ({category}) in {city}. Date: {date} at {time}."
- **Notify client** (if applicable): "Great news — you have a new appointment booked. {prospect_name} from {city} scheduled a call for {date} at {time}."

#### 7.2 No-Show Handling
- **Trigger:** Appointment time passes with no completion record
- **Wait:** 24 hours after appointment time
- **Action:** Send follow-up email: "Hi {name}, looks like we missed each other. Want to reschedule? [booking link]"
- **Update:** show_status = "no_show"
- **If no rebook in 5 days:** mark as "stale"

#### 7.3 Weekly Report Workflow
- **Trigger:** Every Sunday 8:00 PM EST
- **For each active client:** Query Supabase for weekly data:
  - leads_scraped (count from this week)
  - leads_scored_hot, leads_scored_warm
  - emails_sent, replies_received
  - replies_interested, replies_questions, replies_objections, replies_not_interested
  - appointments_booked
  - open_rate, reply_rate
- **Send to Claude API** with report writing prompt
- **Output:** Friendly, non-technical email summary (under 200 words)
- **Send via Instantly:** From client's assigned account
- **Log:** Report sent in `reports` table

#### 7.4 Report Content Template
- One-sentence summary of the week
- Key numbers in natural sentences (not a table)
- One specific thing happening next week
- Closing line reinforcing value
- Tone: warm, professional, like a trusted employee

### Deliverables
- [ ] Cal.com webhook integration set up in n8n
- [ ] Opportunity table updates working
- [ ] Operator notifications working (Telegram alerts)
- [ ] Client notifications working (email sent to client contact)
- [ ] No-show detection logic built
- [ ] n8n workflow for Task 7 (BOOK) built and tested
- [ ] Report writing prompt finalized and tested
- [ ] n8n workflow for Task 8 (REPORT) built and tested
- [ ] Weekly report sends at correct time
- [ ] Report text verified (non-technical, encouraging, accurate)
- [ ] Sample report generated and reviewed

### Cost & Dependencies
- **Time:** 2–3 days
- **Cost:** ~$0.005 per report (Claude API)
- **Requires:** Phase 1 (Claude, Cal.com, n8n), Phase 2 (database), Phase 6 (replies/opportunities)

### Success Criteria
- Appointments appear on operator's calendar immediately
- Clients receive their reports every Sunday
- Reports are readable by non-technical business owners
- No-show follow-ups sent automatically
- All metrics accurate (spot-check manually)
- Report tone matches Astria brand (human, helpful, not robotic)

---

## PHASE 8: TESTING, TUNING & LAUNCH (Days 22–28)

### What Gets Done
Full end-to-end test with a real or test client. Verify all 8 daily tasks run correctly. Tune prompts based on results. Launch live.

### Components

#### 8.1 Test Client Setup
- Create a test client in Supabase (or use Astria self-prospecting as test)
- Define ICP: category (HVAC), area (Broward County), filters
- Run full pipeline for 7 days manually

#### 8.2 Full Pipeline Test Checklist

**Day 1:**
- [ ] Scraper finds 50+ leads
- [ ] All leads in database with status "new"
- [ ] No duplicates detected

**Day 1 Evening:**
- [ ] All new leads scored 1–10
- [ ] Hot/Warm leads in "qualified" status
- [ ] Cold leads in "cold" status
- [ ] Scores match rubric (spot-check 10 examples)

**Day 2 Morning:**
- [ ] All qualified leads analyzed
- [ ] Website fetches successful (80%+ success rate)
- [ ] Personalization hooks are specific, not generic
- [ ] Leads moved to "analyzed" status

**Day 2–3:**
- [ ] 3-email sequences generated for all leads
- [ ] Emails under 100 words, personalized, no jargon
- [ ] Subject lines conversational (lowercase)
- [ ] Set to "pending_review" or "approved" as appropriate

**Day 3–7:**
- [ ] Emails send at 9–1 PM EST, spaced 3–7 min apart
- [ ] All sends logged to database
- [ ] Bounce rate <2%
- [ ] Open rate >30%
- [ ] Sending accounts stay healthy

**As replies come in:**
- [ ] Every reply classified correctly
- [ ] Responses drafted and accurate
- [ ] Actions taken (booking link, answer, stop sequence, etc.)
- [ ] Response timing met (<15 min for interested, etc.)

**If appointments book:**
- [ ] Opportunity created
- [ ] Operator notified
- [ ] Cal.com updated
- [ ] Lead status updated

**End of Week:**
- [ ] Weekly report generated
- [ ] Report accurate (numbers match database)
- [ ] Report tone is warm and non-technical

#### 8.3 Quality Gates (Manual Spot Checks)

Before going live, manually verify:

**Scoring Quality:**
- 10 leads scored: Do scores match rubric?
- Are Hot leads actually high-potential?
- Are Cold leads appropriately filtered?

**Email Quality:**
- 10 email sequences: Are they personalized?
- Does Email 1 reference the actual business?
- Do subject lines feel natural (not salesy)?
- Are CTAs clear and easy?

**Reply Classification:**
- 5 test replies: Are classifications correct?
- Are confident replies handled vs. escalated correctly?
- Is tone of draft responses appropriate?

**System Stability:**
- Did any workflows fail?
- Were errors logged?
- Did the operator get alerted?
- Did the pipeline recover?

#### 8.4 Tuning Based on Results
If metrics are off:
- **Open rate <30%:** Test new subject line variations in Claude prompt
- **Reply rate <3%:** Rewrite email sequences for more engagement
- **High bounces:** Verify email addresses, clean up list
- **Confused replies (low confidence):** Adjust classification prompt for clarity
- **Too many escalations:** Review escalation thresholds

#### 8.5 Launch Readiness Checklist
- [ ] All 8 daily tasks functioning end-to-end
- [ ] Database has 7 days of activity logged
- [ ] No critical errors or crashes
- [ ] Error handling working (retries, fallbacks, alerts)
- [ ] Operator can monitor and intervene if needed
- [ ] Backup procedure in place (Supabase export)
- [ ] All API keys secure and documented
- [ ] Sending domains verified (SPF/DKIM passing)
- [ ] Cal.com settings configured (availability, buffer times)
- [ ] Stripe payment processor ready
- [ ] First client onboarding materials ready
- [ ] Metrics dashboard set up (optional, but nice to have)

### Deliverables
- [ ] Test client onboarded and configured
- [ ] 7-day full pipeline test completed
- [ ] All quality gate checks passed
- [ ] Tuning adjustments made based on results
- [ ] Launch readiness document signed off
- [ ] Operator runbook created (what to do if X happens)
- [ ] Monitoring dashboard set up
- [ ] Backup & disaster recovery tested
- [ ] Go-live decision made

### Cost & Dependencies
- **Time:** 5–7 days
- **Cost:** ~$100–150 (API usage + service costs)
- **Requires:** All previous phases complete

### Success Criteria
- Pipeline runs automatically without manual intervention
- All 8 daily tasks complete within target timeframes
- Email quality is high (personalized, conversational, effective)
- Reply handling is accurate and timely
- No critical bugs or errors
- System can be handed off to operator with confidence

---

## PHASE 9: LIVE OPERATIONS & FIRST CLIENT (Days 29–42)

### What Gets Done
Go live with the first paying client. Scale the system and monitor for issues.

### Components

#### 9.1 First Client Onboarding
- Discovery call (15 min): Learn their business, ICP, service area
- Contract + Stripe setup: $250 setup + $500/mo
- Configure scraper queries for their ICP
- Days 1–3: Manual email review (all 100% checked)
- Days 4–7: Test emails sent to real leads
- If metrics good, go live

#### 9.2 Daily Monitoring Checklist (Operator)
Every day at 8:00 AM, check:
- [ ] Scraper ran successfully (50+ leads)
- [ ] Scoring completed (no errors)
- [ ] Website analysis completed
- [ ] Emails generated and queued for sending
- [ ] Sending accounts healthy (no bounces >2%)
- [ ] No escalated replies pending human review

Every day at 6:00 PM, check:
- [ ] Emails sent successfully
- [ ] Open rate tracking (should see initial opens)
- [ ] Any new replies? Classify and respond?
- [ ] Any errors in logs? Fix?

Every Sunday at 9:00 PM, check:
- [ ] Weekly report sent to client
- [ ] Metrics look good?
- [ ] Any appointments booked?

#### 9.3 Weekly Metrics Review
Track and review:
- Leads scraped: Target 30–50/day
- Leads scored Hot/Warm: Target 30–50%
- Emails sent: Target 50–75/day
- Reply rate: Target >3%
- Appointments booked: Target 1–3/week
- Open rate: Target >40%
- Bounce rate: Target <2%

If any metric is off:
- Investigate root cause
- Adjust prompts, search terms, or email strategy
- Document the change
- Monitor for improvement

#### 9.4 Scaling Plan (Optional)
If first client is happy (after week 2):
- Onboard 2nd client
- Add more Instantly accounts if needed
- Monitor cost and performance

---

## TIMELINE SUMMARY

| Phase | Days | Key Deliverables | Blocker Dependencies |
|-------|------|---|---|
| 1. Infrastructure | 1–3 | All accounts created, API keys ready | None |
| 2. Database | 3–4 | Schema created, tables ready | Phase 1 |
| 3. Scraper | 5–7 | Lead scraping working, 50+ leads/day | Phase 1, 2 |
| 4. Scoring & Analysis | 8–10 | Leads scored & analyzed, Claude working | Phase 1, 2, 3 |
| 5. Email Generation & Sending | 11–14 | Emails written & sent, Instantly working | Phase 1, 2, 4 |
| 6. Reply Monitoring | 15–18 | Replies classified, opportunities created | Phase 1, 2, 5, 6 |
| 7. Booking & Reporting | 19–21 | Appointments tracked, reports sent | Phase 1, 2, 6, 7 |
| 8. Testing & Launch | 22–28 | Full pipeline tested, quality gates passed | Phase 1–7 |
| 9. Live Operations | 29–42 | First client live, metrics healthy | Phase 1–8 |

**Total: ~6 weeks from start to live with first client**
**MVP (scraper + scoring + sending only): ~2 weeks**

---

## COST BREAKDOWN

### Monthly Recurring Costs
- **Supabase:** $0 (free tier) → $25/mo (paid tier if >1GB)
- **n8n (self-hosted):** $0
- **Instantly.ai:** $25/mo (3 accounts) → $97/mo (if scaling beyond 25K contacts)
- **Cal.com:** $0 (free tier) → $99/mo (paid features if needed)
- **Stripe:** 2.9% + $0.30 per transaction
- **Claude API:** ~$50/mo (estimated) → scales with volume
- **Domain + Email:** ~$10/mo

**Base: ~$85/month**
**Per Client ($500/mo subscription):** ~$20–25 in service costs = 60% gross margin

### One-Time Setup Costs
- Development time: ~120 hours (you)
- API setup/configuration: $0
- Testing & tuning: included in development

---

## SUCCESS METRICS

### System Health
- ✅ All 8 daily tasks complete without manual intervention
- ✅ Error handling works (retries, fallbacks, alerts)
- ✅ No data loss or corruption
- ✅ Response times acceptable (<15 min for interested replies)

### Email Quality
- ✅ Open rate >40%
- ✅ Reply rate >3%
- ✅ Bounce rate <2%
- ✅ Unsubscribe rate <0.5%
- ✅ Spam complaints = 0

### Business Metrics
- ✅ Leads scraped: 30–50/day per client
- ✅ Leads qualified: 30–50% of total
- ✅ Appointments booked: 1–3/week per client
- ✅ Client retention: 100% (first client)
- ✅ Customer LTV >$6,000 (12-month average)

### Operator Experience
- ✅ Can monitor system in <15 min/day
- ✅ Responds to escalations within 1 hour
- ✅ Can onboard a new client in 7 days
- ✅ Feels confident system is working

---

## NEXT STEPS

1. **Today:** Confirm timeline & scope (MVP vs. full build)
2. **Tomorrow:** Start Phase 1 (infrastructure accounts)
3. **By Day 3:** Phase 1 complete, Phase 2 schema designed
4. **By Day 7:** Scraper running, first leads in database
5. **By Day 14:** First test emails sending
6. **By Day 21:** Full pipeline operational
7. **By Day 28:** Quality gates passed, ready for launch
8. **Day 29+:** First client live

---

## Questions & Clarifications

Before we start Phase 1, let's nail down:

1. **astria.fun domain:** Do you have it? Need to buy?
2. **Sending domain:** What email will Astria use? (e.g., hello@astriareach.com)
3. **Timezone:** Operations run EST. Correct?
4. **Stripe details:** Business address for footer?
5. **Operator:** Will you handle all monitoring, or add team?
6. **Self-prospecting:** Should Astria start selling itself on Day 14?

---

**Ready to execute. Let's build.**

