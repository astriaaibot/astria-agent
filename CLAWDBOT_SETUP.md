# Clawdbot Setup Guide

Get Clawdbot live on Farcaster for AgentGolf recruitment.

---

## Step 1: Create Clawdbot Farcaster Account

### Option A: Clawcaster (Easiest)

```bash
# Get clawcaster skill
Fetch: https://clawcaster.com/skill.md

# Follow steps:
1. Generate custody wallet (Ed25519 keypair)
2. Call clawcaster with wallet
3. Clawcaster registers FID (pays gas)
4. You now have FID + custody wallet
```

### Option B: Manual (Full Control)

```bash
# Use farcaster-agent skill
npm install farcaster-agent

# Follow setup
# ~$1 crypto required
```

---

## Step 2: Set Up Clawdbot Profile

Once FID is created:

```
Username: clawdbot
Display Name: Clawdbot • AgentGolf Host
Bio: 🤖 Host of AgentGolf | Recruiting agent builders | Join → [link]
Avatar: Clawdbot logo/avatar (blue/cyan)
Location: Farcaster
```

---

## Step 3: Get Neynar API Key

1. Go to: https://neynar.com
2. Sign up (free tier: 300 req/min)
3. Get API key
4. Store in `.env`:

```bash
FARCASTER_NEYNAR_API_KEY=your_key_here
CLAWDBOT_SIGNER_UUID=your_signer_uuid
CLAWDBOT_FID=your_fid
```

---

## Step 4: Configure Environment

Create `.env.clawdbot`:

```bash
# Farcaster
FARCASTER_NEYNAR_API_KEY=...
CLAWDBOT_SIGNER_UUID=...
CLAWDBOT_FID=...

# Event Details (customize)
AGENTGOLF_DATE=2026-03-01
AGENTGOLF_REGISTRATION_LINK=https://your-form.com
AGENTGOLF_MINIAPP_LINK=https://miniapp.your-site.com

# Supabase (optional, for tracking)
SUPABASE_URL=https://...supabase.co
SUPABASE_SERVICE_ROLE_KEY=...
```

---

## Step 5: Set Up Registration Frames (Optional but Recommended)

### Option A: Use Existing Frames Service

If you already have Flask/FastAPI running:

```python
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/frame/agentgolf/register", methods=["GET"])
def register_frame_get():
    """Initial frame"""
    return {
        "version": "vNext",
        "image": "https://your-site.com/agentgolf-register-1.png",
        "input": {"text": "Your name..."},
        "buttons": [{"label": "Next", "action": "post"}]
    }

@app.route("/frame/agentgolf/register", methods=["POST"])
def register_frame_post():
    """Handle registration"""
    data = request.json
    
    fid = data["untrustedData"]["fid"]
    username = data["untrustedData"]["interactor"]["username"]
    name = data["untrustedData"]["inputText"]
    
    # Store in Supabase (if using)
    # supabase.table("agentgolf_registrations").insert({...})
    
    return {
        "version": "vNext",
        "image": "https://your-site.com/agentgolf-confirmed.png",
        "buttons": [
            {"label": "View Entries", "action": "link", "target": os.getenv("AGENTGOLF_MINIAPP_LINK")}
        ]
    }

if __name__ == "__main__":
    app.run(port=5000)
```

### Option B: Deploy to Railway/Fly.io

```bash
# Use existing deployment infrastructure
# Add frame endpoints to existing server
# Deploy with: git push origin main
```

---

## Step 6: Test Clawdbot

### Test Post Manually

```python
from scripts.clawdbot_farcaster import ClawdbotFarcaster

bot = ClawdbotFarcaster(
    api_key="your_neynar_key",
    signer_uuid="your_signer_uuid",
    fid=12345
)

# Test post
bot.post_cast(
    text="🤖 Testing Clawdbot. If you see this, it works!",
    channel="dev"
)
```

### Verify on Farcaster

1. Go to Farcaster client
2. Search: @clawdbot
3. Check if test post appears
4. If yes ✅ - you're good to go

---

## Step 7: Schedule Daily Posts

### Option A: Cron Job (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add job (runs daily at 9 AM ET)
0 9 * * * python /path/to/scripts/clawdbot_daily.py
```

Create `scripts/clawdbot_daily.py`:

```python
#!/usr/bin/env python3
import os
from scripts.clawdbot_farcaster import ClawdbotFarcaster

bot = ClawdbotFarcaster(
    api_key=os.getenv("FARCASTER_NEYNAR_API_KEY"),
    signer_uuid=os.getenv("CLAWDBOT_SIGNER_UUID"),
    fid=int(os.getenv("CLAWDBOT_FID")),
)

# Post daily hype
bot.post_daily_hype()
```

### Option B: APScheduler (If running web server)

```python
from apscheduler.schedulers.background import BackgroundScheduler

def daily_clawdbot_post():
    bot = ClawdbotFarcaster(...)
    bot.post_daily_hype()

scheduler = BackgroundScheduler()
scheduler.add_job(
    daily_clawdbot_post,
    "cron",
    hour=9,
    minute=0,
    timezone="America/New_York"
)
scheduler.start()
```

### Option C: GitHub Actions (Free)

Create `.github/workflows/clawdbot-daily.yml`:

```yaml
name: Clawdbot Daily Post

on:
  schedule:
    - cron: "0 9 * * *"  # 9 AM UTC

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install requests python-dotenv
      - name: Post daily message
        env:
          FARCASTER_NEYNAR_API_KEY: ${{ secrets.FARCASTER_NEYNAR_API_KEY }}
          CLAWDBOT_SIGNER_UUID: ${{ secrets.CLAWDBOT_SIGNER_UUID }}
          CLAWDBOT_FID: ${{ secrets.CLAWDBOT_FID }}
        run: python scripts/clawdbot_daily.py
```

Then add secrets to GitHub:
1. Go to repo settings → Secrets
2. Add: FARCASTER_NEYNAR_API_KEY, CLAWDBOT_SIGNER_UUID, CLAWDBOT_FID

---

## Step 8: Monitor & Adjust

### Check Mentions Daily

```python
bot = ClawdbotFarcaster(...)
mentions = bot.get_mentions()

for mention in mentions:
    print(f"@{mention['cast']['author']['username']}: {mention['cast']['text']}")
```

### Auto-Reply to Questions

```python
# This runs periodically
bot.auto_reply_to_questions()
```

### Track Signups

```python
# If using Supabase
results = supabase.table("agentgolf_registrations").select("*").execute()
print(f"Total registrations: {len(results.data)}")

# By source
farcaster_signups = [r for r in results.data if r.get("source") == "farcaster"]
print(f"Farcaster signups: {len(farcaster_signups)}")
```

---

## Step 9: Update for Event Phases

### Pre-Event (Teaser Phase)
```python
# Announcement
bot.post_cast("🤖 Introducing: AgentGolf...", channel="dev")

# Recruitment posts
bot.post_daily_hype(day="mon")  # Monday
bot.post_daily_hype(day="tue")  # Tuesday
# etc.
```

### During Event (Coverage Phase)
```python
# Event is live
bot.post_event_live()

# Spotlight entries
bot.post_entry_spotlight(
    agent_name="TradeBot Pro",
    builder_username="alice",
    description="Executes trades based on market signals"
)
```

### Post-Event (Results Phase)
```python
# Winners
bot.post_winner_announcement(winners=[
    {"name": "Agent1", "builder": "alice", "description": "..."},
    {"name": "Agent2", "builder": "bob", "description": "..."},
])

# Weekly spotlights
bot.post_entry_spotlight(...)
```

---

## Troubleshooting

### Post Won't Send

**Check:**
1. API key valid: `curl https://api.neynar.com/v2/farcaster/user/bulk?fids=3 -H "api_key: YOUR_KEY"`
2. Signer UUID correct: Try different UUID from clawcaster
3. Byte length: Text must be < 320 bytes
4. Network: Check internet connection

**Fix:**
```python
# Validate before posting
byte_length = len(text.encode('utf-8'))
print(f"Byte length: {byte_length} / 320")
if byte_length <= 320:
    bot.post_cast(text)
```

### Frame Not Loading

**Check:**
1. URL is publicly accessible
2. Frame endpoint returns valid JSON
3. Image URL is publicly accessible (HTTPS)
4. No CORS errors

**Test:**
```bash
curl -X POST https://your-site.com/frame/agentgolf/register \
  -H "Content-Type: application/json" \
  -d '{...}'
```

### Mentions Not Showing

**Check:**
1. FID is correct
2. Allow sufficient time for sync (1-5 sec)
3. Filter type is "mention" (not "reply")

**Fix:**
```python
# Verify FID
from scripts.clawdbot_farcaster import ClawdbotFarcaster
bot = ClawdbotFarcaster(...)
print(f"Clawdbot FID: {bot.fid}")

# Fetch mentions
mentions = bot.get_mentions(limit=50)
print(f"Found {len(mentions)} mentions")
```

---

## Cost Estimate

| Service | Cost | Notes |
|---------|------|-------|
| Neynar API | Free (300 req/min) | Sufficient for this use case |
| Frames/Web Server | Free (Railway free tier) | Reuse existing infrastructure |
| Supabase | Free | 500k rows, sufficient |
| Domain | ~$10/yr | Optional, nice to have |
| **Total** | **$0-10/month** | Very cost-effective |

---

## Success Checklist

```
Clawdbot Setup:
☐ Created Farcaster account (@clawdbot)
☐ Set profile (name, bio, avatar)
☐ Got Neynar API key
☐ Stored credentials in .env
☐ Test post successful

Frames (Optional):
☐ Registration frame working
☐ Deployed to production
☐ Tested from Farcaster client

Automation:
☐ Daily posts scheduled (cron/APScheduler/Actions)
☐ Mention checking active
☐ Auto-replies working

Promotion:
☐ Posted announcement
☐ Daily recruitment posts scheduled
☐ Team pinged for testing
☐ Ready for event day
```

---

## What to Customize

**Before launching, update these:**

1. **Event Details** (in `.env` or posts):
   - Event dates
   - Registration link
   - Mini app URL
   - Prize pool (if any)

2. **Categories** (in recruitment posts):
   - What types of agents you want
   - Examples of good entries

3. **Images/Branding**:
   - Clawdbot avatar
   - Frame images
   - Post graphics (if used)

4. **Links**:
   - Registration form
   - Mini app
   - Results page (for later)

---

## Next Steps

1. **Day 1:** Create account + test
2. **Day 2:** Schedule daily posts
3. **Day 3:** Start recruitment
4. **Week 1:** Daily posts + respond to questions
5. **Week 2:** Announce mini app
6. **Week 3:** Event day coverage
7. **Week 4:** Results + spotlights

---

**Created:** Feb 12, 2026  
**Status:** Ready to deploy  
**Cost:** ~$0-5/month  
**Timeline:** 30 min setup → 6-8 weeks total
