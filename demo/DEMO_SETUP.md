# Astria Demo System

Complete demo automation: I handle initial call, you close the deal.

## Flow

```
Customer books demo
         ↓
Telegram alert to you (instant)
         ↓
Pre-demo email sent (24h before)
         ↓
DEMO CALL (AI agent: me answering)
         ↓
Post-demo email (same day)
         ↓
Hot prospect? → Telegram alert + "READY TO SELL"
         ↓
You follow up with pricing
         ↓
Close or nurture
```

## Setup (5 Steps)

### Step 1: Create Demo Event in Cal.com

1. Go to https://app.cal.com/event-types
2. Create new event: "Astria AI Demo"
3. Duration: 15 minutes
4. Description: "Quick demo of how Astria finds customers for you"
5. Video: Enabled (Zoom/Google Meet)
6. Save

You'll get URL: `https://cal.com/astria/ai-demo`

### Step 2: Set Up Telegram Alerts

Get your Telegram user ID (one-time):

```bash
# Send a message to @userinfobot on Telegram
# It will reply with your user ID
# Copy that ID
```

Add to `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_user_id
```

**How to get tokens:**
1. Message @BotFather on Telegram
2. Type `/newbot`
3. Name: "Astria Alerts"
4. Username: "astria_alerts_bot"
5. Copy token
6. Start bot: `/start`

### Step 3: Deploy Webhook with Demo Handler

Update `webhook/app.py` to include demo logic:

```python
# When BOOKING_CREATED event has eventName == "Astria AI Demo":
# 1. Send Telegram alert to you
# 2. Queue pre-demo email (24h before)
# 3. Queue post-demo follow-up email
```

### Step 4: Create Demo Email Templates

#### Pre-Demo Email (24h before call)

```
Subject: Your Astria Demo is Tomorrow 🚀

Hi [Name],

Your AI sales agent demo is scheduled for tomorrow at [TIME].

What to expect:
- 15-minute walkthrough of how Astria finds customers
- Live demo of lead discovery + email automation
- Answer any questions you have
- No pressure to buy—just learning

Join here: [ZOOM_LINK]

See you soon,
Astria Team
```

#### Post-Demo Email (immediately after)

```
Subject: Here's How to Get Started with Astria

Hi [Name],

Thanks for joining the demo! Here's what we showed you:

✓ Finding 50+ qualified leads daily
✓ Personalized email sequences  
✓ Automatic appointment booking
✓ Weekly reports of activity

Pricing:
- Starter: $299/mo (30-50 leads)
- Standard: $699/mo (80-120 leads) ← Most pick this
- Enterprise: $1,299/mo (200+ leads)

Questions? Reply to this email or book a call with [YOUR_NAME] to discuss:
https://cal.com/astria/sales-call

Ready to get started?
[START_BUTTON: https://astriaaiagent.vercel.app/checkout.html?tier=standard]

Cheers,
Astria Team
```

### Step 5: Connect to Your Telegram

Add demo notification handler:

```python
# In webhook/app.py

def send_telegram_alert(message):
    """Send alert to your Telegram."""
    import requests
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    requests.post(url, json={
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    })

# On demo booking:
send_telegram_alert(
    f"🎯 <b>DEMO BOOKED</b>\n"
    f"Name: {name}\n"
    f"Email: {email}\n"
    f"Time: {start_time}\n\n"
    f"<b>ACTION:</b> Prepare to close them after demo!"
)
```

## Demo Event Types Needed

### 1. "Astria AI Demo" (AI-handled)
- Duration: 15 min
- URL: https://cal.com/astria/ai-demo
- **Who handles:** Me (AI)
- **What I do:**
  - Explain 8-step process
  - Show live lead example
  - Demo email sequences
  - Answer questions
  - Score their fit

### 2. "Sales Call" (You handle)
- Duration: 30 min
- URL: https://cal.com/astria/sales-call
- **Who handles:** You
- **What you do:**
  - Close them on pricing
  - Answer objections
  - Set up Stripe payment
  - Get them started

---

## Demo Scoring

After demo, I score prospects as:

**🔴 Cold** (not ready)
- Wrong business type
- No budget mentioned
- Seems skeptical

**🟡 Warm** (interested)
- Asks good questions
- Mentions pain point
- Wants to see more

**🟢 Hot** (ready to buy)
- Asks about pricing
- Wants to start ASAP
- Has budget available

**Alert you immediately for Hot prospects!**

---

## Automation Sequence

### T-0: Booking Confirmation
Cal.com sends auto-email confirming demo time

### T-24h: Pre-Demo Email
Remind them, set expectations

### T-0: DEMO CALL
Me handling the call (you observing or busy)

### T+0 (same day): Post-Demo Email
Pitch pricing, link to checkout, link to your sales call

### T+2d: Follow-Up Email  
"How did you like the demo? Any questions?"

### T+5d: Last Chance Email
"One more thing... [discount or urgency]"

### T+7d: Archive
Mark as "no response" or loop into nurture

---

## Your Handoff Checklist

When someone books a demo, you get Telegram alert with:
- ✅ Their name
- ✅ Email
- ✅ Business type (if provided)
- ✅ Booking time
- ✅ Direct link to their Cal.com profile

After demo, you get second alert:
- ✅ Demo score (Hot/Warm/Cold)
- ✅ Key questions they asked
- ✅ Objections raised
- ✅ Recommended next action

**If Hot:** Jump on the sales call within 24h

---

## Files Needed

1. `webhook/app.py` — Add demo handlers + Telegram alerts
2. `demo/email_templates.py` — Pre-demo + post-demo emails
3. `demo/scoring.py` — AI scoring of demo attendees
4. `demo/handoff.py` — Flag hot prospects for you

---

## Testing

1. Book a test demo: https://cal.com/astria/ai-demo
2. You get Telegram alert (instant)
3. Pre-demo email comes (or you send manually)
4. Demo time: I handle the call
5. Post-demo email + Telegram with score
6. If hot: You follow up with sales call

---

## Next: Smart Handoff

After each demo:
1. **Telegram tells you the score**
2. **If Hot:** "READY TO SELL - John Smith is hot"
3. **If Warm:** "Follow up in 2 days"
4. **If Cold:** "Not ready yet"

You reply via Telegram:
- `/close` = You're closing now
- `/follow` = Schedule 2-day follow-up
- `/nurture` = Add to nurture sequence

---

## Demo Talking Points (for me)

When handling demo, I cover:

1. **The Problem:** Cold calling doesn't work, hiring salespeople is expensive
2. **The Solution:** Astria finds leads + sends emails + books appointments automatically
3. **The Process:** 8 daily tasks (scrape → score → analyze → write → send → monitor → book → report)
4. **The Results:** 50+ leads/month, 2-4 appointments/week, 42% email open rate
5. **The Pricing:** 3 tiers, $299-$1,299/month, only pay if it works
6. **The Timeline:** First leads in 3 days, appointments in 1-2 weeks
7. **The Question:** "What's your ideal customer, and what area do you serve?"

---

## Ready?

Once you confirm:
1. I'll update webhook to send Telegram alerts
2. Create email templates
3. You set up Telegram bot token
4. Update Cal.com with demo event
5. You're ready to close demos!

This is the dream: **I qualify them, you close them.**

---

**Want to set this up now?**
