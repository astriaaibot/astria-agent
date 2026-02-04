# Astria + Farcaster Integration

Deploy Astria as an autonomous sales agent on Farcaster. Post updates, reply to leads, and book demos on the decentralized social network.

---

## Overview

**What:** Astria launches a Farcaster account (@astria or similar) to:
- Post daily lead summaries
- Reply to potential customers
- Engage in relevant channels (/dev, /base, /ai)
- Share case studies and results
- Book demos via interactive frames

**Why Farcaster:**
- Builder-focused community (SaaS, crypto, dev tools)
- Direct relationship with users (no algorithm gatekeeping)
- Native monetization (Frames, mini-apps)
- Lower spam than Twitter
- Privacy-forward users = privacy-forward sales

**Timeline:** 1-2 weeks to launch + integrate

---

## Phase 1: Account Setup (Day 1)

### 1a. Create Farcaster Account

**Method A: Clawcaster (Easiest)**

Use clawcaster to create Astria's account without managing gas costs.

```bash
# Get clawcaster skill
Fetch: https://clawcaster.com/skill.md

# Steps:
1. Generate custody wallet (Ed25519 keypair, you control keys)
2. Call clawcaster with wallet address
3. Clawcaster registers FID on Optimism (pays gas)
4. Astria now has FID + custody wallet
```

**Method B: farcaster-agent (Full Control)**

For more control, use farcaster-agent:

```bash
npm install farcaster-agent
# Follow skill setup
# ~$1 crypto required for registration
```

**Recommended:** Use clawcaster (simpler, no gas cost)

### 1b. Set Farcaster Profile

Once FID is created:

**Username:** `astria` or `astriaai`  
**Display Name:** `Astria • AI Sales Agent`  
**Bio:** `Autonomous sales agent for local service businesses. Lead scoring, outreach, booking.`  
**Avatar:** Astria logo (indigo + cyan)  
**Location:** "The Internet" or "Everywhere"

### 1c. Get Neynar API Key

Create free Neynar account:
- Go to: neynar.com
- Sign up (free tier: 300 req/min)
- Get API key
- Store in `.env`:

```
FARCASTER_NEYNAR_API_KEY=...
FARCASTER_SIGNER_UUID=...
FARCASTER_FID=...
```

---

## Phase 2: Post & Engage (Week 1-2)

### 2a. Daily Cast Strategy

**Monday-Friday Schedule:**

| Day | Content | Channel |
|-----|---------|---------|
| Mon | Weekly lead summary | /dev, /ai |
| Tue | Case study or result | /base (local SaaS) |
| Wed | Feature update or tip | /dev |
| Thu | Customer success story | general |
| Fri | Week recap + booking link | /dev, /ai |

**Example Casts:**

**Monday - Lead Summary:**
```
🔍 This week's Astria: 248 qualified leads found
📊 Top industries: Plumbing (42), Electrician (38), HVAC (35)
📝 Case study coming Friday

Book a demo: [link]
```

**Wednesday - Feature Update:**
```
✨ NEW: Real-time reply classification
Astria now auto-categorizes inbound responses as:
✅ Interested
⏸️ Maybe later
❌ Not interested

Helps you focus on hot leads. Running it live with 3 clients.
```

**Friday - Case Study:**
```
📈 Client Win: HVAC contractor

Weeks 1-3: Generated 156 leads
Weeks 4-6: 12 qualified appointments
Result: $34k in new contracts

Here's what worked... 🧵

[Thread about strategy]
```

### 2b. Engagement Rules

**When to reply:**

✅ **Do reply:**
- Direct mentions asking about Astria
- Questions about lead generation
- Builders asking about automating sales
- Relevant conversation in channels
- Feature requests or feedback

❌ **Don't reply:**
- Spam/obvious bots
- Unrelated debates
- Off-topic threads

**Reply template:**

```
Hey [name],

Thanks for the question. [Helpful answer specific to their situation]

If you're thinking about this for your business, happy to walk through how Astria could help. Book a time: [link]
```

### 2c. Channel Strategy

**Primary channels:**

- **/dev** - Software, tools, builders
  - Audience: Technical founders
  - Post: Tools, automation, architecture updates

- **/ai** - AI & agents
  - Audience: AI enthusiasts
  - Post: AI-specific features, benchmarks, experiments

- **/base** - Base/Onchain
  - Audience: Crypto-adjacent builders
  - Post: Customer wins (especially crypto/web3 service businesses)

- **General (no channel)**
  - Audience: Broader Farcaster
  - Post: Major announcements, case studies

---

## Phase 3: Interactive Frames (Week 2-3)

### 3a. Demo Request Frame

Create interactive Frame for booking demos on Farcaster.

**What it does:**
1. User sees cast: "Try Astria for free"
2. Clicks "Book Demo" button
3. Frame appears with form:
   - Company name
   - Email
   - Industry (dropdown)
   - Message
4. Submits → Creates Supabase record → Sends Telegram alert

**Frame URL:** `https://astria.fun/frame/demo-request`

**Implementation:**

```html
<!-- Frame meta tags -->
<meta property="fc:frame" content="vNext" />
<meta property="fc:frame:image" content="https://astria.fun/demo-frame.png" />
<meta property="fc:frame:button:1" content="Book Demo" />
<meta property="fc:frame:post_url" content="https://astria.fun/api/frame/demo" />

<!-- On button click, backend receives:
     - User's FID
     - User's username
     - Frame interaction data
     
     Then show form fields for company, email, industry
-->
```

### 3b. Lead Generation Frame

Cast: "See what leads Astria finds for your area"

Frame shows:
- Local service type picker (plumbing, electrical, HVAC, etc.)
- Zipcode input
- "Find Leads" button
- Display sample leads matching criteria

Captures: User's FID, service type, location → Qualified lead

### 3c. Results Showcase Frame

Cast: "Check out real client results"

Frame shows:
- Dropdown: Select case study
- Display: Lead count, appointments, revenue
- Button: "I want these results too"

Clicks → Book demo

---

## Phase 4: Analytics & Optimization (Ongoing)

### 4a. Metrics to Track

```sql
-- In Supabase
SELECT 
  source_channel,
  COUNT(*) as casts,
  SUM(likes) as total_engagement,
  SUM(recasts) as amplification,
  COUNT(DISTINCT referred_user) as referrals,
  COUNT(DISTINCT booked_demo) as demos_booked
FROM farcaster_engagement
GROUP BY source_channel
ORDER BY demos_booked DESC;
```

**Key metrics:**
- Casts per week
- Engagement rate (likes + recasts)
- Click-through to demo frame
- Demos booked via Farcaster
- Conversion to customers

### 4b. Optimization Loop

**Weekly:**
- Check which casts got most engagement
- Which channels drove most demos
- What content types work best

**Monthly:**
- Analyze conversion: impressions → demos → customers
- A/B test post times
- Refine channel strategy
- Update bio/profile based on learnings

---

## Setup Checklist

```
Phase 1: Account (Day 1)
☐ Get clawcaster skill
☐ Generate custody wallet
☐ Register FID via clawcaster
☐ Set profile (username, bio, avatar)
☐ Create Neynar account
☐ Get Neynar API key
☐ Store credentials in .env

Phase 2: Posts (Week 1)
☐ Plan content calendar (5 post types above)
☐ Write first week's posts
☐ Schedule using Neynar API
☐ Reply to mentions manually (first week)
☐ Track engagement metrics

Phase 3: Frames (Week 2)
☐ Design demo frame
☐ Build frame endpoint
☐ Deploy to production
☐ Test from Farcaster
☐ Post frame cast
☐ Iterate based on usage

Phase 4: Automation (Week 3)
☐ Set up daily cast schedule (Python/cron)
☐ Auto-post weekly summary
☐ Auto-reply to certain mention types (optional)
☐ Build analytics dashboard
☐ Weekly optimization review
```

---

## Integration with Astria Pipeline

### Current Pipeline
```
Google Maps scrape
    ↓
Score leads (Claude)
    ↓
Analyze websites
    ↓
Write email sequences
    ↓
Send via Instantly.ai
    ↓
Classify replies
    ↓
Respond to hot leads
    ↓
Book appointment via Cal.com
```

### New: Farcaster Layer

```
Farcaster engagement happens in parallel:

Post on Farcaster (daily)
    ↓
Capture mentions / frame clicks
    ↓
Qualify inbound leads
    ↓
Store in Supabase (farcaster_leads table)
    ↓
Run through scoring (same as email leads)
    ↓
Send personalized message (or book direct from frame)
    ↓
Track conversion → customer
```

---

## Code Examples

### Post a Cast (Python)

```python
import requests

def post_cast(text, channel=None, image_url=None):
    url = "https://api.neynar.com/v2/farcaster/cast"
    
    headers = {
        "api_key": os.getenv("FARCASTER_NEYNAR_API_KEY"),
    }
    
    body = {
        "signer_uuid": os.getenv("FARCASTER_SIGNER_UUID"),
        "text": text,
    }
    
    if channel:
        body["channel_id"] = channel  # "dev", "ai", "base"
    
    if image_url:
        body["embeds"] = [{"url": image_url}]
    
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# Example: Post daily summary
post_cast(
    text=f"🔍 Astria This Week: {lead_count} leads found\n📊 Top: {top_industry}\n📝 Demo: [link]",
    channel="dev",
)
```

### Capture Frame Interaction (Flask)

```python
from flask import Flask, request

@app.route("/api/frame/demo", methods=["POST"])
def frame_demo():
    data = request.json
    
    fid = data.get("interactor", {}).get("fid")
    username = data.get("interactor", {}).get("username")
    
    # Store in Supabase
    supabase.table("farcaster_leads").insert({
        "fid": fid,
        "username": username,
        "source": "demo_frame",
        "timestamp": datetime.now(),
    }).execute()
    
    # Return new frame (form or confirmation)
    return {
        "type": "frame",
        "image": "https://astria.fun/form-frame.png",
        "buttons": [...],
    }
```

### Reply to Mentions (Scheduled)

```python
def check_mentions():
    # Get mentions using Neynar
    mentions = neynar_client.fetch_notifications(
        fid=ASTRIA_FID,
        filter_type="mention",
    )
    
    for mention in mentions:
        if should_reply(mention):
            response_text = generate_reply(mention.text)
            post_cast(
                text=response_text,
                parent=mention.hash,  # Reply to their cast
            )
        
        mark_as_processed(mention.id)

# Schedule via cron
schedule.every().day.at("09:00").do(check_mentions)
```

---

## Farcaster Gotchas

1. **320 byte limit** - Casts are bytes, not chars. Emojis = multiple bytes.
2. **Signer ≠ wallet** - Farcaster signer is Ed25519, not your ETH wallet
3. **Rate limits** - Neynar free: 300 req/min
4. **Mentions need FIDs** - Use @username in text, Neynar handles FID encoding
5. **Hub sync delay** - Direct writes can lag. Use Neynar API (faster)
6. **Embeds for previews** - URLs in text don't preview; must be in embeds array
7. **Channels are optional** - Posting without channel is fine (general feed)

---

## Resources

| Resource | Link | Use |
|----------|------|-----|
| Neynar Docs | https://docs.neynar.com | API reference |
| Farcaster Protocol | https://docs.farcaster.xyz | Protocol details |
| OnchainKit | https://onchainkit.xyz | Frame/Mini App SDK |
| Mini Apps llms.txt | https://miniapps.farcaster.xyz/llms-full.txt | Frame development |
| GM Farcaster | https://gmfarcaster.com | Stay current on ecosystem |

---

## FAQ

**Q: Should Astria have its own Farcaster account?**  
A: Yes. Easier to build following, trust, and community around a branded account than a personal one.

**Q: Will people trust an AI agent?**  
A: Yes, especially in /dev and /ai. Be transparent: "Built by Astria, an AI sales agent." Transparency > hiding.

**Q: What if Astria gets hate/criticism on Farcaster?**  
A: Respond thoughtfully. Farcaster users value honesty. If criticism is fair, acknowledge. If trolls, ignore.

**Q: Can Astria reply to every mention?**  
A: No. Selective reply (qualified leads only) = better engagement. Automatic spam kills credibility.

**Q: How do Frames integrate with booking?**  
A: Frame → Supabase lead record → Astria scores lead → If hot: auto-send Cal.com link or direct booking button.

---

## What's Next

1. **Week 1:** Account setup + first 5 casts
2. **Week 2:** Build demo booking frame
3. **Week 3:** Automate daily posts + reply system
4. **Ongoing:** Analyze, optimize, scale

---

**Created:** Feb 3, 2026  
**Status:** Ready to launch  
**Integration:** Parallel to existing email pipeline  
**Effort:** ~1-2 weeks to full launch
