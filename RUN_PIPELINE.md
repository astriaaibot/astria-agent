# RUN PIPELINE — Quick Reference

Once you have API keys, here's how to run the full Astria pipeline.

## Setup (One-Time)

```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Add your API keys to .env
# SUPABASE_URL=https://xxxxx.supabase.co
# SUPABASE_ANON_KEY=...
# CLAUDE_API_KEY=sk-ant-...
# INSTANTLY_API_KEY=...
# STRIPE_PUBLISHABLE_KEY=...
# STRIPE_SECRET_KEY=...

# 3. Install Python dependencies
pip install anthropic supabase python-dotenv requests

# 4. Test your credentials
python -c "from scraper.scrape_leads import supabase; print('✅ Connected' if supabase else '❌ Failed')"
```

---

## Run Daily Pipeline (8 Tasks in Order)

### 6:00 AM — Task 1: SCRAPE

```bash
# Find 50+ new leads from Google Maps
python scraper/scrape_leads.py --client-id <CLIENT_ID>

# Output:
# {
#   "success": 45,
#   "duplicates": 8,
#   "errors": 0
# }
```

### 6:30 AM — Task 2: SCORE

```bash
# Rate each new lead 1-10
python scoring/score_leads.py --client-id <CLIENT_ID>

# Output:
# {
#   "scored": 45,
#   "hot": 12,
#   "warm": 18,
#   "cold": 15,
#   "errors": 0
# }
```

### 7:00 AM — Task 3: ANALYZE

```bash
# Get personalization hooks from websites
python analysis/analyze_websites.py --client-id <CLIENT_ID>

# Output:
# {
#   "analyzed": 27,
#   "skipped": 3,
#   "errors": 0
# }
```

### 7:30 AM — Task 4: WRITE

```bash
# Generate 3-email sequences
python emails/write_sequences.py --client-id <CLIENT_ID>

# Output:
# {
#   "written": 27,
#   "errors": 0,
#   "skipped": 0
# }
```

### 9:00 AM — Task 5: SEND

```bash
# Send today's emails via Instantly
python emails/send_emails.py --client-id <CLIENT_ID>

# Output:
# {
#   "sent": 25,
#   "failed": 0,
#   "skipped": 2,
#   "details": []
# }
```

### 9:00 AM - 6:00 PM — Task 6: MONITOR

```bash
# When a reply comes in (via webhook):
python replies/classify_replies.py --reply-id <REPLY_ID>

# Output:
# {
#   "success": true,
#   "classification": "interested",
#   "action": "send_booking_link",
#   "business": "ABC Plumbing"
# }
```

### Real-Time — Task 7: BOOK

```bash
# Handled automatically by Cal.com webhook
# When prospect books: Creates opportunity record
# Updates lead status to "appointment_booked"
```

### Sundays 8:00 PM — Task 8: REPORT

```bash
# Generate weekly report for client
python reporting/send_weekly_report.py --client-id <CLIENT_ID>

# Output:
# {
#   "success": true,
#   "metrics": {
#     "leads_scraped": 315,
#     "emails_sent": 280,
#     "replies_received": 12,
#     "appointments_booked": 3,
#     "open_rate": "42%",
#     "reply_rate": "4%"
#   },
#   "report_preview": "This week was strong..."
# }
```

---

## Using n8n (Automate Daily)

Once pipelines work manually, automate them:

```bash
# 1. Start n8n
n8n start

# 2. Go to http://localhost:5678

# 3. Create workflows:
#    - Task 1 (SCRAPE) at 6:00 AM
#    - Task 2 (SCORE) at 6:30 AM
#    - Task 3 (ANALYZE) at 7:00 AM
#    - Task 4 (WRITE) at 7:30 AM
#    - Task 5 (SEND) at 9:00 AM
#    - Task 6 (MONITOR) on webhook trigger
#    - Task 8 (REPORT) at Sundays 20:00

# 4. Use HTTP Request nodes to call Python scripts
#    or use native n8n integrations
```

---

## Test Everything First (Recommended)

Before going live, test with test data:

```bash
# 1. Create test client
# In Supabase: INSERT INTO clients VALUES (...)

# 2. Run each task manually
python scraper/scrape_leads.py --client-id test-client
python scoring/score_leads.py --client-id test-client
# ... etc

# 3. Verify database updates
# Check Supabase tables for data flow

# 4. Check outputs match expectations
# Scores 1-10? Emails < 100 words? Personalized?

# 5. If all good, switch to real client
```

---

## Monitoring & Troubleshooting

### Check daily logs:
```bash
# View errors in database
# SELECT * FROM errors ORDER BY timestamp DESC LIMIT 10

# View activity summary
# SELECT COUNT(*), activity_type FROM activities_log 
# WHERE DATE(timestamp) = TODAY() 
# GROUP BY activity_type
```

### Common issues:

| Issue | Fix |
|-------|-----|
| "Missing API key" | Check .env file, make sure all keys are set |
| "No leads found" | Verify search queries are correct for client |
| "Claude API timeout" | Retry — may be rate-limited. Check quota. |
| "Email send failed" | Verify Instantly.ai account is warm + active |
| "Invalid JSON" | Likely Claude output error — check prompt, retry once |
| "Database connection error" | Verify Supabase key is correct + has permission |

---

## Scaling (Multiple Clients)

To run for multiple clients:

```bash
# Loop through all active clients
for CLIENT_ID in $(get_active_clients); do
  echo "Running pipeline for $CLIENT_ID"
  
  python scraper/scrape_leads.py --client-id $CLIENT_ID
  sleep 30
  python scoring/score_leads.py --client-id $CLIENT_ID
  sleep 30
  # ... etc
done
```

Or use n8n to manage multiple workflows.

---

## Performance Tips

1. **Batch similar tasks:** Score all leads at once, not one-by-one
2. **Rate limit:** Respect API limits (Claude: ~3.5 RPM, Instantly: varies)
3. **Cache results:** Store website text locally so you don't re-fetch
4. **Async replies:** Process reply classification in background (don't block email sending)
5. **Database indexes:** Index on client_id, lead_id, status for fast queries

---

## Questions?

- Check logs: `tail -f logs.txt`
- Check database: Supabase dashboard
- Debug scripts: Add `--debug` flag (if implemented)
- Check API status: Claude, Instantly.ai, Supabase dashboards

---

**Everything is ready. Just add keys and run.**
