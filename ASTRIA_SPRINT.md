# ASTRIA SPRINT — Fast Build (14 Days to Launch)

## PHASE 1: INFRASTRUCTURE (Days 1-2)

- [ ] Create Supabase project
- [ ] Generate Supabase API key + password
- [ ] Install n8n locally: `npm install -g n8n` then `n8n start`
- [ ] Create Instantly.ai account + 3 email accounts (warmup)
- [ ] Get Instantly API key
- [ ] Create Cal.com account + Discovery Call event (15 min)
- [ ] Create Claude API account + get API key
- [ ] Create Stripe account
- [ ] Verify/buy sending domain (astriareach.com or similar)
- [ ] Configure SPF/DKIM on sending domain
- [ ] Store all API keys in 1Password or .env
- [ ] Test: Supabase dashboard loads, n8n loads at localhost:5678, API calls work

---

## PHASE 2: DATABASE (Days 2-3)

- [ ] Create 9 tables in Supabase:
  - `clients` (business_name, email, category, service_area, subscription_status, created_date)
  - `leads` (business_name, phone, email, website, rating, review_count, status, score, tier, created_date)
  - `lead_details` (lead_id, services, usp, pain_points, personalization_hook)
  - `email_sequences` (lead_id, subject, body, send_day, status, sent_date)
  - `replies` (lead_id, reply_text, classification, confidence, action, received_date)
  - `opportunities` (lead_id, appointment_booked, appointment_date, appointment_time)
  - `errors` (task_name, error_message, timestamp)
  - `activities_log` (client_id, activity_type, details, timestamp)
  - `reports` (client_id, week_start, leads_scraped, emails_sent, replies_received, appointments_booked)
- [ ] Create indexes on: client_id, lead_id, status, created_date
- [ ] Create foreign keys
- [ ] Insert test client record

---

## PHASE 3: SCRAPER (Days 3-4)

- [ ] Install google-maps-scraper: `pip install google-maps-scraper`
- [ ] Write `scraper/scrape_leads.py`:
  - Input: client_id, search queries
  - Output: leads inserted into `leads` table (status: "new")
  - Dedup: check place_id, phone, business_name+city
  - Error handling: retry 3x, log to `errors` table
- [ ] Test scraper locally: 50+ leads from sample query
- [ ] Create n8n workflow: triggers daily 6:00 AM, runs scraper, logs results

---

## PHASE 4: SCORING (Days 4-5)

- [ ] Write Claude scoring prompt (8 criteria, output JSON: score 1-10, tier, reasoning)
- [ ] Write `scoring/score_leads.py`:
  - Input: all leads with status "new"
  - For each: call Claude API, parse JSON response
  - Move Hot/Warm to "qualified", Cold to "cold"
  - Log errors to `errors` table
- [ ] Test with 20 real leads (manual verification)
- [ ] Create n8n workflow: triggers 6:30 AM, runs scoring, updates leads table

---

## PHASE 5: WEBSITE ANALYSIS (Days 5-6)

- [ ] Write Claude analysis prompt (extract: services, usp, pain_points, personalization_hook, output JSON)
- [ ] Write `analysis/analyze_websites.py`:
  - Input: all leads with status "qualified" + website URL
  - Fetch homepage HTML (30s timeout)
  - Extract text (first 3000 chars)
  - Send to Claude, parse response
  - Store in `lead_details` table
  - Fallback hook if no website or fetch fails
- [ ] Test with 10 real websites (manual verification)
- [ ] Create n8n workflow: triggers 7:00 AM, runs analysis, updates leads to "analyzed"

---

## PHASE 6: EMAIL WRITING (Days 6-7)

- [ ] Write Claude email writing prompt:
  - 3 emails (subject, body, send_day: 0, 3, 7)
  - Rules: <100 words each, personalized, conversational, no jargon
  - Output: JSON array
- [ ] Write `emails/write_sequences.py`:
  - Input: all leads with status "analyzed"
  - Call Claude for each lead
  - Quality checks: valid JSON, <100 words, Email 1 refs business, no !
  - Store in `email_sequences` table (status: "approved")
- [ ] Test with 10 real leads (manual read-through)
- [ ] Create n8n workflow: triggers 7:30 AM, runs email writing

---

## PHASE 7: EMAIL SENDING (Days 7-8)

- [ ] Integrate Instantly.ai API in n8n
- [ ] Write `sending/send_emails.py`:
  - Input: all emails with status "approved" + send_day matching today
  - Skip if prospect already replied
  - Skip if prospect unsubscribed
  - Push to Instantly API (max 25/account/day, rotate between 3)
  - Space 3-7 min apart (9 AM - 1 PM EST only)
  - Update status to "sent", log send time + account
  - Update lead status to "contacted"
- [ ] Test: send 10 emails manually, verify in Instantly dashboard
- [ ] Check Instantly warmup status (all 3 accounts green)
- [ ] Check bounce rate (<2%)
- [ ] Create n8n workflow: triggers 9:00 AM, runs sending

---

## PHASE 8: REPLY MONITORING (Days 8-10)

- [ ] Set up Instantly webhook in n8n (reply webhook → n8n endpoint)
- [ ] Write Claude classification prompt:
  - Input: reply text + original email + prospect info
  - Output: JSON (category: interested/question/objection/not_interested/out_of_office, confidence, draft_response, action, escalate_to_human)
- [ ] Write `replies/classify_replies.py`:
  - Receive webhook payload
  - Call Claude for classification
  - Store in `replies` table
  - Take action based on classification:
    - INTERESTED: send booking link, create opportunity, stop sequence, notify operator
    - QUESTION: draft response, pause 3 days
    - OBJECTION: draft response, pause 2 days
    - NOT_INTERESTED: remove confirmation, add to suppression list, stop sequence
    - OUT_OF_OFFICE: pause 7 days, no response
  - Escalate if confidence <0.7 or suspicious words (lawyer, legal, sue)
- [ ] Test with 5 sample replies (manual verification)
- [ ] Create n8n workflow: webhook trigger → classification → action

---

## PHASE 9: BOOKING & REPORTING (Days 10-12)

- [ ] Set up Cal.com webhook in n8n (booking confirmed → n8n endpoint)
- [ ] Write `booking/handle_booking.py`:
  - Receive webhook (prospect booked)
  - Update `opportunities` table (appointment_booked = true, date, time)
  - Update lead status to "appointment_booked"
  - Notify operator: Telegram message with appointment details
  - Optionally notify client
- [ ] Write weekly report prompt (Claude):
  - Input: client_id, week_start, week_end
  - Query Supabase: leads_scraped, emails_sent, replies_received, appointments_booked, open_rate, reply_rate
  - Output: Plain-English email summary (under 200 words, warm tone, non-technical)
- [ ] Write `reporting/send_weekly_report.py`:
  - Trigger every Sunday 8 PM
  - For each active client: query data, call Claude, send via Instantly
  - Log in `reports` table
- [ ] Test report generation (manual read-through)
- [ ] Create n8n workflows: booking webhook + weekly report scheduler

---

## PHASE 10: END-TO-END TEST (Days 12-14)

- [ ] Create test client in Supabase (or use Astria self-prospecting)
- [ ] Run full pipeline for 7 days:
  - [ ] Day 1: Scraper finds 50+ leads ✅
  - [ ] Day 1 Eve: All leads scored ✅
  - [ ] Day 2: All qualified leads analyzed ✅
  - [ ] Day 2-3: Emails generated for all ✅
  - [ ] Day 3-7: Emails sending, open rate tracking ✅
  - [ ] Replies classified correctly ✅
  - [ ] Booking link works ✅
  - [ ] Sunday: Weekly report sent ✅
- [ ] Spot-check quality (10 scores, 10 emails, 5 replies)
- [ ] Fix any bugs
- [ ] Verify all metrics match expected ranges

---

## PHASE 11: LAUNCH (Day 14+)

- [ ] Prepare first client onboarding call
- [ ] Set up client in Supabase
- [ ] Run scraper for their ICP
- [ ] Generate first batch of emails
- [ ] Manual review of first 20 emails (quality gate)
- [ ] Send first test batch (10 emails)
- [ ] Monitor for replies, adjustments
- [ ] If metrics good (open >30%, reply >2%), unlock auto-mode
- [ ] Go live

---

## DAILY CHECKLIST (Operator, Once Live)

- [ ] 8:00 AM: Scraper ran? (50+ leads) ✅
- [ ] 8:00 AM: Scoring done? (errors logged?) ✅
- [ ] 8:00 AM: Website analysis done? ✅
- [ ] 9:00 AM: Emails sent? (bounce rate <2%) ✅
- [ ] 6:00 PM: Any escalated replies? (classify + respond) ✅
- [ ] 6:00 PM: Any appointments booked? (log, notify) ✅
- [ ] Sunday 9:00 PM: Weekly report sent? ✅

---

## DEPENDENCIES & BLOCKERS

| Phase | Requires |
|-------|----------|
| 1 | None |
| 2 | Phase 1 |
| 3 | Phase 1, 2 |
| 4 | Phase 1, 2, 3 |
| 5 | Phase 1, 2, 4 |
| 6 | Phase 1, 2, 5 |
| 7 | Phase 1, 2, 6 |
| 8 | Phase 1, 2, 5, 7 |
| 9 | Phase 1, 2, 8 |
| 10 | Phase 1-9 |
| 11 | Phase 10 ✅ |

---

## FAST-TRACK TIPS

1. **Don't overthink emails.** Claude is good—trust the output. Spot-check 10%, adjust prompt once.
2. **Test API integrations early.** Make sure Instantly, Cal.com, Claude all work before building workflows.
3. **Skip fancy UI.** n8n workflows run headless. You don't need a dashboard. Just logs.
4. **Batch test data.** Generate 100 test leads at once, run full pipeline, spot-check. Fast feedback loop.
5. **Use defaults.** n8n has webhook templates. Cal.com has standard settings. Don't customize unless it breaks.
6. **Log everything.** Every error, every sent email, every reply. Saves debugging time later.
7. **Manual first.** Run Phase 3-9 manually once before automating in n8n. Easier to debug.

---

## READY?

Go through this checklist top-to-bottom. Each item is a single, discrete task. When you finish a phase, mark it done and move to the next.

**Day 1 starts with Phase 1. Go.**
