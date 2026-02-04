---
name: farcaster
description: Post, reply, and engage on Farcaster. Create agent accounts, post casts, build interactive Frames, manage channels. Use when building autonomous agents for Farcaster, posting updates, capturing leads via Frames, or creating Farcaster-native experiences.
---

# Farcaster Skill

Post, engage, and build interactive experiences on Farcaster. Enables AI agents to post updates, reply to mentions, build Frames (interactive mini-apps), and manage Farcaster presence.

---

## When to Use This Skill

✅ **Use this skill when:**

- Building an AI agent with a Farcaster account
- Posting casts (updates) to Farcaster timeline
- Replying to mentions and engaging with community
- Creating interactive Frames or mini-apps
- Capturing leads via Farcaster engagement
- Broadcasting announcements to channels
- Automating social media presence on Farcaster

❌ **Don't use this skill for:**

- General social media (use platform-specific skills)
- Blockchain transactions (use base/onchain skills)
- Direct messages (rare use case, separate API)

---

## Quick Start

### 1. Create Farcaster Account for Agent

Use **clawcaster** (recommended):

```
1. Get clawcaster skill: https://clawcaster.com/skill.md
2. Generate custody wallet (Ed25519 keypair)
3. Call clawcaster to register FID (no gas cost)
4. Set profile: username, display name, bio, avatar
5. Create Neynar account (neynar.com)
6. Get API key + set signer UUID
7. Store in environment:
   FARCASTER_NEYNAR_API_KEY=...
   FARCASTER_SIGNER_UUID=...
   FARCASTER_FID=...
```

### 2. Post a Cast

```python
import requests
import os

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
        body["channel_id"] = channel  # "dev", "ai", "base", etc.
    
    if image_url:
        body["embeds"] = [{"url": image_url}]
    
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# Post to /dev channel
post_cast(
    text="Building something cool on Farcaster 🚀",
    channel="dev"
)
```

### 3. Reply to a Cast

```python
def reply_to_cast(text, parent_cast_hash, image_url=None):
    """Reply to another user's cast (thread/mention reply)"""
    url = "https://api.neynar.com/v2/farcaster/cast"
    
    body = {
        "signer_uuid": os.getenv("FARCASTER_SIGNER_UUID"),
        "text": text,
        "parent": parent_cast_hash,  # Hash of cast you're replying to
    }
    
    if image_url:
        body["embeds"] = [{"url": image_url}]
    
    response = requests.post(
        url,
        json=body,
        headers={"api_key": os.getenv("FARCASTER_NEYNAR_API_KEY")}
    )
    return response.json()

# Example: Reply to a mention
reply_to_cast(
    text="Great question! Here's how...",
    parent_cast_hash="0xabc123..."
)
```

### 4. Fetch Notifications/Mentions

```python
def get_mentions():
    """Fetch recent mentions of your account"""
    url = f"https://api.neynar.com/v2/farcaster/notifications"
    
    params = {
        "fid": os.getenv("FARCASTER_FID"),
        "filter_type": "mention",
    }
    
    response = requests.get(
        url,
        params=params,
        headers={"api_key": os.getenv("FARCASTER_NEYNAR_API_KEY")}
    )
    return response.json()

# Usage
mentions = get_mentions()
for mention in mentions.get("notifications", []):
    print(f"@{mention['user']['username']}: {mention['cast']['text']}")
```

---

## Common Patterns

### Pattern: Post with Image

```python
post_cast(
    text="Check this out 👇",
    image_url="https://example.com/image.png",
    channel="dev"
)
```

**Note:** Images must be publicly accessible URLs. Supported formats: PNG, JPG, GIF, WebP.

### Pattern: Create Thread (Multiple Casts)

```python
# First cast
response1 = post_cast(text="Thread incoming 🧵")
cast_hash = response1["cast"]["hash"]

# Second cast (reply to first)
response2 = reply_to_cast(
    text="Here's part 2 of the thread",
    parent_cast_hash=cast_hash
)

# Third cast (reply to second, continues thread)
response3 = reply_to_cast(
    text="And part 3 to wrap up",
    parent_cast_hash=response2["cast"]["hash"]
)
```

### Pattern: Post to Specific Channel

Channels are like subreddits. Common ones:

- `/dev` - Software, tools, builders
- `/ai` - AI and agents
- `/base` - Onchain/Base/Crypto
- `/degen` - Risk/speculation
- `/memes` - Memes and culture
- `/frames` - Frames/mini-apps

```python
# Post to channels
post_cast(text="New AI agent launched 🤖", channel="ai")
post_cast(text="Building on Base", channel="base")
post_cast(text="Dev tools update", channel="dev")
```

### Pattern: Mention a User

```python
# To mention, use @username in text
# Neynar handles FID encoding automatically

post_cast(text="Hey @dwr, thoughts on this?")

# Or in reply
reply_to_cast(
    text="Thanks for sharing @alice",
    parent_cast_hash="0x..."
)
```

### Pattern: Like or Recast

```python
def react_to_cast(cast_hash, reaction_type="like"):
    """Like or recast a cast"""
    url = "https://api.neynar.com/v2/farcaster/reaction"
    
    body = {
        "signer_uuid": os.getenv("FARCASTER_SIGNER_UUID"),
        "reaction_type": reaction_type,  # "like" or "recast"
        "target": cast_hash,
    }
    
    response = requests.post(
        url,
        json=body,
        headers={"api_key": os.getenv("FARCASTER_NEYNAR_API_KEY")}
    )
    return response.json()

# Like a cast
react_to_cast("0xabc123...", reaction_type="like")

# Recast (amplify)
react_to_cast("0xabc123...", reaction_type="recast")
```

---

## Building Frames (Interactive Mini-Apps)

A Frame is an interactive webpage embedded in Farcaster. Users see buttons, can fill forms, and interact within their client.

### Frame Meta Tags (HTML Head)

```html
<head>
  <!-- Required -->
  <meta property="fc:frame" content="vNext" />
  <meta property="fc:frame:image" content="https://yourapp.com/frame-image.png" />
  
  <!-- Button 1 (required) -->
  <meta property="fc:frame:button:1" content="Click me" />
  <meta property="fc:frame:post_url" content="https://yourapp.com/api/frame" />
  
  <!-- Button 2, 3, 4 (optional) -->
  <meta property="fc:frame:button:2" content="Option 2" />
  <meta property="fc:frame:button:3" content="Option 3" />
  <meta property="fc:frame:button:4" content="Option 4" />
  
  <!-- Input field (optional) -->
  <meta property="fc:frame:input:text" content="Enter your name..." />
</head>
```

### Frame Flow (Backend)

When a user clicks a button, your `post_url` receives:

```json
{
  "untrustedData": {
    "fid": 12345,
    "url": "https://yourframe.com",
    "messageHash": "0x...",
    "timestamp": 1234567890,
    "network": "mainnet",
    "buttonIndex": 1,
    "inputText": "user input if exists",
    "interactor": {
      "fid": 12345,
      "username": "alice",
      "displayName": "Alice"
    }
  },
  "trustedData": {
    "messageBytes": "0x..."
  }
}
```

**Server-side:**

```python
from flask import Flask, request, jsonify

@app.route("/api/frame", methods=["POST"])
def frame_handler():
    data = request.json
    
    # Verify signature (production)
    # ...
    
    fid = data["untrustedData"]["fid"]
    button_index = data["untrustedData"]["buttonIndex"]
    input_text = data["untrustedData"].get("inputText")
    
    # Handle interaction
    if button_index == 1:
        # Do something
        next_image = "https://yourapp.com/frame-2.png"
        next_buttons = [
            {"label": "Next", "action": "post"},
        ]
    
    # Return next frame state
    return jsonify({
        "version": "vNext",
        "image": next_image,
        "buttons": [
            {"label": btn["label"], "action": btn["action"]}
            for btn in next_buttons
        ],
    })
```

### Example: Lead Capture Frame

```python
@app.route("/frame/lead-capture", methods=["GET"])
def lead_frame_get():
    """Initial frame display"""
    html = """
    <html>
      <head>
        <meta property="fc:frame" content="vNext" />
        <meta property="fc:frame:image" content="https://astria.fun/lead-frame.png" />
        <meta property="fc:frame:input:text" content="Your email..." />
        <meta property="fc:frame:button:1" content="Capture Lead" />
        <meta property="fc:frame:post_url" content="https://astria.fun/api/frame/lead" />
      </head>
    </html>
    """
    return html

@app.route("/api/frame/lead", methods=["POST"])
def lead_capture():
    """Handle lead capture"""
    data = request.json
    
    fid = data["untrustedData"]["fid"]
    username = data["untrustedData"]["interactor"]["username"]
    email = data["untrustedData"].get("inputText")
    
    # Store in Supabase
    supabase.table("farcaster_leads").insert({
        "fid": fid,
        "username": username,
        "email": email,
        "source": "lead_frame",
        "timestamp": datetime.now(),
    }).execute()
    
    # Return confirmation frame
    return jsonify({
        "version": "vNext",
        "image": "https://astria.fun/confirmation.png",
        "buttons": [{
            "label": "View Results",
            "action": "link",
            "target": "https://astria.fun/results"
        }]
    })
```

---

## Automation: Daily Posts

Schedule daily posts using APScheduler or cron:

```python
from apscheduler.schedulers.background import BackgroundScheduler

def daily_post():
    """Post summary once per day"""
    summary = generate_daily_summary()
    post_cast(text=summary, channel="dev")

scheduler = BackgroundScheduler()
scheduler.add_job(
    daily_post,
    "cron",
    hour=9,
    minute=0,  # 9 AM daily
    timezone="America/New_York"
)
scheduler.start()
```

---

## Rate Limits & Costs

**Neynar Free Tier:**
- 300 requests/min
- Sufficient for: Daily posts + replies to mentions + polls

**Neynar Paid:**
- Higher limits if you grow

**Farcaster Fees:**
- Registration: ~$1 (one-time, via clawcaster or self-funded)
- Posts: Free
- Gas: Minimal for hub writes (usually free via Neynar)

---

## Gotchas & Common Mistakes

1. **320 byte limit** - Casts are bytes, not characters. Emojis use multiple bytes. Test length.
2. **Embeds for links** - URLs in text don't auto-preview. Must be in `embeds` array.
3. **Signer UUID vs FID** - Signer UUID = your posting identity. FID = account ID. Different.
4. **Mentions need username in text** - Format: `@username`. Neynar handles FID encoding.
5. **Channel IDs are lowercase** - Use `channel_id: "dev"`, not `"DEV"`
6. **Replies need parent hash** - To reply, always include `"parent": "0x..."`
7. **Rate limit: 300/min** - Plan casts accordingly (batch during low-traffic times)
8. **Hub sync delay** - Direct hub writes can lag. Use Neynar API (faster).

---

## Integration Examples

### Astria (Sales Agent)

Post daily lead summaries, reply to prospects, capture leads via Frames.

See: **FARCASTER_ASTRIA.md** for complete integration guide.

### Gilfoyle (Developer Agent)

Post updates on systems, respond to alerts, create debugging Frames.

### News Bot

Fetch news from RSS, post to /dev channel, monitor engagement.

---

## Resources

**Official Docs:**
- Neynar API: https://docs.neynar.com
- Farcaster Protocol: https://docs.farcaster.xyz
- OnchainKit (Frames SDK): https://onchainkit.xyz

**Guides:**
- Frame Development: https://miniapps.farcaster.xyz/llms-full.txt
- Neynar Reference: https://docs.neynar.com/llms-full.txt
- Ecosystem News: https://gmfarcaster.com

**Account Setup:**
- Clawcaster (account creation): https://clawcaster.com/skill.md
- Neynar (API): https://neynar.com

---

## Environment Variables Required

```bash
# Essential
FARCASTER_NEYNAR_API_KEY=...  # From neynar.com
FARCASTER_SIGNER_UUID=...      # From clawcaster setup
FARCASTER_FID=...              # Your agent's Farcaster ID

# Optional
FARCASTER_POSTING_CHANNEL=dev  # Default channel for posts
FARCASTER_MAX_BYTE_LENGTH=300  # Cast length limit
```

---

## Testing

### Test Post Without Publishing

```python
def preview_cast(text):
    """Count bytes and validate before posting"""
    byte_length = len(text.encode('utf-8'))
    if byte_length > 320:
        print(f"⚠️ Cast too long: {byte_length} bytes (max 320)")
        return False
    print(f"✅ Cast OK: {byte_length} bytes")
    return True

# Test
preview_cast("Hello Farcaster 🚀")
```

### Test Frame Locally

```bash
# Test frame HTML
curl -s https://yourapp.com/frame/demo | grep "fc:frame"

# Should output meta tags
```

---

## Next Steps

1. **Setup:** Get clawcaster skill, create Farcaster account
2. **Post:** Write 3-5 test casts
3. **Engage:** Reply to mentions manually
4. **Automate:** Set up daily posts
5. **Frame:** Build lead capture or demo booking Frame
6. **Measure:** Track engagement, conversions, ROI

---

**Maintained by:** Astria Team  
**Last Updated:** Feb 3, 2026  
**Status:** Production-ready
