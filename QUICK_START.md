# QUICK START — Right Now

## WHAT'S HAPPENING

1. **n8n installing** (in background) — will finish in ~3 min
2. **Account guide ready** — see `PHASE1_ACCOUNT_CREATION.md`
3. **You need to:** Create 6 accounts (Supabase, Claude, Instantly, Cal.com, Stripe, Sending Domain)

---

## YOUR NEXT STEPS (Do This Now)

### STEP 1: Go get the 6 accounts (90 min)

Open `PHASE1_ACCOUNT_CREATION.md` and follow each section:

1. **Supabase** (15 min) — https://supabase.com
2. **Claude API** (10 min) — https://console.anthropic.com
3. **Instantly.ai** (20 min) — https://instantly.ai
4. **Cal.com** (15 min) — https://cal.com
5. **Stripe** (20 min) — https://stripe.com
6. **Sending Domain** (45 min with DNS wait) — Namecheap.com or your registrar

**Save all API keys to 1Password labeled "Astria - All API Keys"**

---

### STEP 2: Wait for n8n to finish

I've started `npm install -g n8n` in the background. It's building now (~3 min).

Once done, you'll be able to:
```bash
n8n start
```

And access: http://localhost:5678

---

### STEP 3: When you're done with accounts

Reply with the keys:
- Supabase URL + 2 API keys
- Claude API key
- Instantly API key (+ 3 email accounts)
- Cal.com booking link
- Stripe keys (publishable + secret)

I'll store them securely and move you to **Phase 2: Database Schema**.

---

## WHERE TO FIND THINGS

| File | Purpose |
|------|---------|
| `ASTRIA_SPRINT.md` | 14-day checklist (your main guide) |
| `BUILDOUT.md` | Detailed plan with costs, timeline, success criteria |
| `PHASE1_ACCOUNT_CREATION.md` | Step-by-step account creation (open now) |
| `QUICK_START.md` | This file |

---

## GO.

Open `PHASE1_ACCOUNT_CREATION.md` and start with Supabase. I'll check on n8n installation and ping you when it's ready.

**Target: Accounts done by tonight. Phase 2 tomorrow.**
