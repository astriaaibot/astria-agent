# Demo System - Quick Start

Get alerts when prospects book demos. Score them hot/warm/cold after call. Hand off to you for closing.

## 5-Minute Setup

### 1. Get Telegram Bot Token

1. Open Telegram, message **@BotFather**
2. Type `/newbot`
3. Follow prompts
4. Copy the token (long string)
5. Paste into `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

### 2. Get Your Telegram User ID

1. Message **@userinfobot** on Telegram
2. It replies with your ID
3. Paste into `.env`:
   ```
   TELEGRAM_CHAT_ID=your_id_here
   ```

### 3. Test Connection

```bash
python webhook/telegram_alerts.py
```

You should get a message on Telegram: "✅ Astria webhook connected!"

### 4. Update Cal.com Event

Create new event type in Cal.com:
- Name: "Astria AI Demo"
- Duration: 15 minutes
- URL: `https://cal.com/astria/ai-demo`

### 5. Deploy Webhook

```bash
cd webhook
vercel --prod
```

That's it! You're ready.

---

## What You'll See

### When Someone Books Demo

**Telegram:** 
```
🎯 DEMO BOOKED!
Name: John Smith
Email: john@example.com
Time: Tomorrow 2:00 PM

ACTION: Prepare to close them!
```

### During Demo (You or AI)

I (or you) handle the 15-min call:
- Explain the 8-step process
- Show live example
- Answer questions
- Ask about their business

### After Demo

**Telegram Alert 1:**
```
🔥 HOT PROSPECT - READY TO CLOSE!
Name: John Smith
Score: 9/10

Why hot: Asked about pricing, wants to start ASAP

NEXT STEP: Call or email them TODAY!
```

**OR Alert 2:**
```
⚡ WARM PROSPECT
Name: Jane Doe  
Score: 6.5/10

Why warm: Interested, but has questions

ACTION: Schedule sales call in 2 days
```

**OR Alert 3:**
```
❄️ COLD PROSPECT
Name: Bob Wilson
Score: 3/10

Why cold: Wrong business type

ACTION: Auto-nurture email sent
```

---

## Demo Talking Points

When you (or I) do the demo, cover:

**Problem (2 min):**
- Cold calling doesn't work
- Hiring salespeople is expensive
- You need more customers but no time to prospect

**Solution (5 min):**
- Astria finds leads daily
- Sends personalized emails
- Books appointments automatically
- You just close the deals

**Proof (3 min):**
- 50+ leads/month
- 2-4 appointments/week
- 42% email open rate
- Only $299-1,299/month

**Close (5 min):**
- "What's your ideal customer?"
- "What area do you serve?"
- "Interested in getting started?"

---

## Your Role

### Before Demo
- Get notified when booked
- Glance at their info
- Prepare (know their business type if provided)

### During Demo
- Option 1: Let me handle it (I have the script)
- Option 2: You do it live
- Option 3: You observe, jump in if needed

### After Demo
- Get hotness score instantly
- If **Hot** (8-10): Call them TODAY
- If **Warm** (5-7): Schedule sales call in 2 days
- If **Cold** (1-4): Send nurture email

### Closing
- Use the post-demo email (already sent)
- Emphasize: "$699/mo is our best value"
- Get them to Stripe checkout
- Or book 30-min sales call with you

---

## Commands You Can Use

Reply to Telegram alerts with:

- `/close` — You're calling them now
- `/follow` — Schedule 2-day follow-up automatically
- `/nurture` — Move to nurture sequence
- `/done` — Mark deal closed

---

## Pro Tips

1. **During demo:** Ask "What's your single biggest challenge finding customers?"
2. **Jot notes:** Their pain point, budget hints, timeline
3. **Score fairly:** Just count the signals (pricing questions = hot)
4. **Move fast:** Hot prospects close fastest if you reach out same day
5. **Use email:** If they're warm, send them the post-demo email immediately

---

## Demo URL

Share this with prospects:
**https://cal.com/astria/ai-demo**

You can post it:
- Website (button)
- LinkedIn
- Email signature
- Sales conversations

---

## Next Level

Once you're comfortable:
1. Record some demos (for portfolio)
2. Pull quotes from prospects
3. Turn into case studies
4. Use in follow-up emails

---

**Ready?**
1. ✅ Set up Telegram bot token + user ID
2. ✅ Test connection: `python webhook/telegram_alerts.py`
3. ✅ Deploy webhook: `vercel deploy webhook/`
4. ✅ Create demo event in Cal.com
5. ✅ You're live!

Share the booking link and let the demos start rolling in! 🚀
