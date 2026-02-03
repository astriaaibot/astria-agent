# INITIAL TEST SETUP

Complete instructions to prepare for first-run testing of the Astria pipeline.

---

## Step 1: Secure API Keys in 1Password

**Status:** Waiting on you to provide:
- Supabase: Project URL, Anon Key, Service Role Key
- Claude API: API Key
- Stripe: Publishable Key, Secret Key

Once you reply with these keys, I'll:
1. Create "Astria" vault in 1Password
2. Store each key securely
3. Generate secure `.env` file

---

## Step 2: Create Database Schema

**Once keys are secured:**

```bash
# 1. Copy init_schema.sql to Supabase
cd database
cat init_schema.sql

# 2. Go to Supabase dashboard:
#    - Your project → SQL Editor
#    - Paste init_schema.sql
#    - Click "Run"

# 3. Verify tables created:
#    - In Supabase: Table Editor
#    - Should see 9 tables:
#      - clients
#      - leads
#      - lead_details
#      - email_sequences
#      - replies
#      - opportunities
#      - errors
#      - activities_log
#      - reports
```

**What it does:**
- Creates all 9 tables
- Sets up indexes for performance
- Creates foreign keys
- Inserts test client: "Test HVAC Company"

---

## Step 3: Update `.env` File

```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Fill in your keys:
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGc...
CLAUDE_API_KEY=sk-ant-...
INSTANTLY_API_KEY=your_api_key
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
SENDING_DOMAIN=astriareach.com
SENDING_EMAIL_1=account1@astriareach.com
SENDING_EMAIL_2=account2@astriareach.com
SENDING_EMAIL_3=account3@astriareach.com

# 3. Save and verify
source .env
echo $SUPABASE_URL  # Should print your URL
```

**Security:**
- Never commit `.env` to git
- Keep `.env.example` (without real keys) in repo
- Store real keys in 1Password + `.env`

---

## Step 4: Install Dependencies

```bash
# Install Python packages
pip install anthropic supabase python-dotenv requests

# Verify installations
python -c "import anthropic, supabase; print('✅ Dependencies OK')"
```

---

## Step 5: Test Connection to Services

```bash
# Test Supabase
python -c "
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')
supabase = create_client(url, key)
result = supabase.table('clients').select('*').execute()
print(f'✅ Supabase connected: {len(result.data)} clients')
"

# Test Claude API
python -c "
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
msg = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=50,
    messages=[{'role': 'user', 'content': 'Say hello'}]
)
print(f'✅ Claude API connected: {msg.content[0].text[:50]}...')
"
```

---

## Step 6: Run Single Pipeline Tasks (Manual Test)

Test each task individually to verify it works:

### Task 1: Scrape Leads

```bash
# Get test client ID from Supabase (should be in database after init_schema.sql)
# For now, use: test-client-id (you'll replace with real UUID)

python scraper/scrape_leads.py --client-id test-client-id

# Expected output:
# {
#   "success": 30,
#   "duplicates": 5,
#   "errors": 0
# }

# Verify in Supabase: Table "leads" should have ~30 rows
```

### Task 2: Score Leads

```bash
python scoring/score_leads.py --client-id test-client-id

# Expected output:
# {
#   "scored": 30,
#   "hot": 8,
#   "warm": 12,
#   "cold": 10,
#   "errors": 0
# }

# Verify: Leads should have score + tier fields populated
```

### Task 3: Analyze Websites

```bash
python analysis/analyze_websites.py --client-id test-client-id

# Expected output:
# {
#   "analyzed": 15,
#   "skipped": 3,
#   "errors": 0
# }

# Verify: lead_details table should have personalization_hook, services, etc.
```

### Task 4: Write Email Sequences

```bash
python emails/write_sequences.py --client-id test-client-id

# Expected output:
# {
#   "written": 15,
#   "errors": 0,
#   "skipped": 0
# }

# Verify: email_sequences table should have 3 rows per lead (45 total)
```

### Task 5: Send Emails

```bash
# Requires Instantly.ai account + API key configured
python emails/send_emails.py --client-id test-client-id

# Expected output:
# {
#   "sent": 20,
#   "failed": 0,
#   "skipped": 0
# }

# Verify: email_sequences.status should be "sent"
```

### Task 6: Monitor Replies

```bash
# This is triggered by webhook from Instantly
# For testing, you can manually create a reply and classify it:

# In Supabase, insert a test reply:
# INSERT INTO replies (lead_id, client_id, email_id, reply_text, received_date)
# VALUES (lead_uuid, client_uuid, email_uuid, 'Tell me more', NOW())

python replies/classify_replies.py --reply-id reply-uuid

# Expected output:
# {
#   "success": true,
#   "classification": "interested",
#   "action": "send_booking_link",
#   "business": "ABC Plumbing"
# }
```

### Task 8: Generate Report

```bash
python reporting/send_weekly_report.py --client-id test-client-id

# Expected output:
# {
#   "success": true,
#   "metrics": {
#     "leads_scraped": 30,
#     "emails_sent": 45,
#     "replies_received": 2,
#     "appointments_booked": 0,
#     "open_rate": "35%",
#     "reply_rate": "4%"
#   },
#   "report_preview": "This week was solid..."
# }
```

---

## Step 7: Full End-to-End Test

Once each task works individually, run the full pipeline:

```bash
# Run all tasks in order (simulating daily workflow)
echo "🔍 Task 1: Scraping..."
python scraper/scrape_leads.py --client-id test-client-id
sleep 2

echo "✍️ Task 2: Scoring..."
python scoring/score_leads.py --client-id test-client-id
sleep 2

echo "🔗 Task 3: Analyzing..."
python analysis/analyze_websites.py --client-id test-client-id
sleep 2

echo "📝 Task 4: Writing..."
python emails/write_sequences.py --client-id test-client-id
sleep 2

echo "📧 Task 5: Sending..."
python emails/send_emails.py --client-id test-client-id
sleep 2

echo "✅ Pipeline complete!"
```

---

## Step 8: Verify Database State

```bash
# Check leads table
SELECT COUNT(*) as total_leads, 
       COUNT(CASE WHEN status='new' THEN 1 END) as new_leads,
       COUNT(CASE WHEN tier='hot' THEN 1 END) as hot_leads
FROM leads
WHERE client_id = 'test-client-id';

# Check emails table
SELECT COUNT(*) as total_emails,
       COUNT(CASE WHEN status='sent' THEN 1 END) as sent,
       COUNT(CASE WHEN status='pending_review' THEN 1 END) as pending
FROM email_sequences
WHERE client_id = 'test-client-id';

# Check replies table
SELECT COUNT(*) as total_replies,
       classification,
       COUNT(*) 
FROM replies
WHERE client_id = 'test-client-id'
GROUP BY classification;
```

---

## Step 9: Test Client Dashboard

Once database has test data:

```bash
# Open dashboard.html in browser
open website/dashboard.html

# Or serve locally:
cd website
python3 -m http.server 8000
# Visit http://localhost:8000/dashboard.html
```

Dashboard will display:
- KPI cards (leads, emails, replies, appointments)
- Pipeline status
- Activity feed
- Weekly summary
- Lead list
- Email metrics
- Appointments
- Reports

---

## Troubleshooting

### "Missing API key" error
```bash
# Check .env file exists and has all keys
cat .env | grep -E "SUPABASE|CLAUDE|STRIPE|INSTANTLY"

# Reload env variables
source .env
```

### "No leads found"
```bash
# Verify scraper is finding businesses
# Check Google Maps is accessible
# Try different search queries

python scraper/scrape_leads.py --client-id test-client-id --debug
```

### "Claude API timeout"
```bash
# Check API quota
# Try again in a few seconds
# Check network connection
```

### "Invalid JSON from Claude"
```bash
# Claude's response format was wrong
# Script will retry once automatically
# Check prompt in script matches expected format
```

### Database connection error
```bash
# Verify Supabase URL is correct
echo $SUPABASE_URL

# Verify API key has permission to read tables
# Try in Supabase dashboard manually
```

---

## Success Criteria

✅ Test passes when:
- All 9 tables created in Supabase
- Test client exists: "Test HVAC Company"
- All 8 Python scripts run without errors
- Database populates with test data
- Dashboard loads with mock metrics
- No API errors in logs

Once all tests pass → Ready for first real client!

---

## Next: Real Client Onboarding

After testing succeeds:

1. **Create new client record** in Supabase
2. **Discovery call** (15 min with prospect)
3. **Define ICP** (business type, service area)
4. **Run pipeline** with their real ICP
5. **Monitor first week** of activity
6. **Adjust based on metrics** (open rate, reply rate, etc.)

---

**Ready to test? Reply with your 3 API key sets.**
