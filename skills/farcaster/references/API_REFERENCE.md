# Farcaster + Neynar API Reference

Quick reference for common Neynar API endpoints and Farcaster concepts.

---

## Neynar Endpoints

### POST /cast - Create a Cast

**Endpoint:** `POST https://api.neynar.com/v2/farcaster/cast`

**Headers:**
```
api_key: YOUR_NEYNAR_API_KEY
```

**Body:**
```json
{
  "signer_uuid": "YOUR_SIGNER_UUID",
  "text": "Your cast text (max 320 bytes)",
  "channel_id": "dev",              // optional
  "embeds": [                       // optional
    { "url": "https://example.com" }
  ],
  "parent": "0xabc123...",          // optional, for replies
  "reply_settings": "everyone"      // optional
}
```

**Response:**
```json
{
  "success": true,
  "cast": {
    "hash": "0xabc123...",
    "author": { "fid": 12345, "username": "alice" },
    "text": "Your cast text",
    "timestamp": 1234567890
  }
}
```

---

### GET /feed - Get Feed

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/feed/home`

**Query Params:**
```
fid=12345              // Your FID
limit=25               // Items per page (max 100)
cursor=abc123          // For pagination
```

**Response:**
```json
{
  "casts": [
    {
      "hash": "0x...",
      "author": { "username": "alice", "fid": 123 },
      "text": "Cast text",
      "engagement": {
        "likes_count": 42,
        "recasts_count": 10,
        "replies_count": 5
      }
    }
  ]
}
```

---

### GET /feed/channel - Get Channel Feed

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/feed/channel`

**Query Params:**
```
channel_id=dev         // Channel to fetch
limit=25               // Items
cursor=abc123          // Pagination
```

---

### GET /notifications - Get Mentions/Notifications

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/notifications`

**Query Params:**
```
fid=YOUR_FID           // Your Farcaster ID
filter_type=mention    // "mention", "like", "recast", "reply"
limit=25
cursor=abc123
```

**Response:**
```json
{
  "notifications": [
    {
      "type": "mention",
      "cast": {
        "hash": "0x...",
        "text": "@yourbot hello!",
        "author": { "username": "alice", "fid": 123 }
      }
    }
  ]
}
```

---

### GET /user/by_username - Look Up User

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/user/by_username`

**Query Params:**
```
username=alice         // Username to look up
```

**Response:**
```json
{
  "user": {
    "fid": 123,
    "username": "alice",
    "display_name": "Alice",
    "pfp": "https://...",
    "bio": "User bio",
    "follower_count": 1000,
    "following_count": 500
  }
}
```

---

### GET /user/bulk - Get Multiple Users

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/user/bulk`

**Query Params:**
```
fids=123,456,789       // Comma-separated FIDs
```

---

### POST /reaction - Like or Recast

**Endpoint:** `POST https://api.neynar.com/v2/farcaster/reaction`

**Body:**
```json
{
  "signer_uuid": "YOUR_SIGNER_UUID",
  "reaction_type": "like",      // "like" or "recast"
  "target": "0xabc123..."       // Cast hash to react to
}
```

---

### GET /search/casts - Search Casts

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/search/casts`

**Query Params:**
```
q=astria               // Search term
limit=25
```

---

### GET /search/users - Search Users

**Endpoint:** `GET https://api.neynar.com/v2/farcaster/search/users`

**Query Params:**
```
q=alice                // Search term
limit=25
```

---

## Key Data Structures

### User

```json
{
  "fid": 123,
  "username": "alice",
  "display_name": "Alice",
  "profile": {
    "bio": "Builder",
    "location": "San Francisco",
    "website": "https://example.com"
  },
  "pfp_url": "https://...",
  "follower_count": 1000,
  "following_count": 500,
  "verified_accounts": ["eth"],
  "active_status": "active"
}
```

### Cast

```json
{
  "hash": "0xabc123...",
  "author": { "fid": 123, "username": "alice" },
  "text": "Cast text",
  "embeds": [
    { "url": "https://example.com", "metadata": {...} }
  ],
  "timestamp": 1234567890,
  "engagement": {
    "likes_count": 42,
    "recasts_count": 10,
    "replies_count": 5
  },
  "thread": {
    "parent_hash": "0xparent...",
    "root_parent_hash": "0xroot..."
  }
}
```

### Reaction

```json
{
  "type": "like",              // "like" or "recast"
  "hash": "0xabc123...",
  "user": { "fid": 123 },
  "timestamp": 1234567890
}
```

---

## Common Channels

| Channel | ID | Audience | Best For |
|---------|----|-----------| ----------|
| Dev | `dev` | Software builders, tools | Technical updates, releases |
| AI | `ai` | AI enthusiasts, agents | AI features, benchmarks |
| Base | `base` | Onchain builders, crypto | Web3 projects, token launches |
| Degen | `degen` | Risk-takers, traders | Speculation, trading signals |
| Memes | `memes` | Meme culture | Humor, viral content |
| Frames | `frames` | Frame builders | Mini-app launches, demos |

---

## Error Responses

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Invalid API key"
}
```
**Fix:** Check `FARCASTER_NEYNAR_API_KEY`

### 429 Rate Limited
```json
{
  "success": false,
  "error": "Rate limit exceeded"
}
```
**Fix:** Wait 60 seconds, retry. Max 300 req/min.

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid signer_uuid"
}
```
**Fix:** Check signer UUID format and validity.

---

## Byte Length Reference

Since Farcaster casts are limited to 320 bytes (not characters):

```
"hello"           = 5 bytes
"hello 🚀"        = 9 bytes (emoji = 4 bytes)
"hello world 🔥"  = 14 bytes

📊 Lead data
Lead count: 248   = 19 bytes

So this fits:
"📊 This week: 248 leads found
🏆 Biggest wins: Plumbing, HVAC
Book demo → [link]"
= ~80 bytes (plenty of room for 320 limit)
```

**Tool:** Test byte length before posting

```python
text = "Your cast text"
byte_length = len(text.encode('utf-8'))
print(f"Byte length: {byte_length} / 320")
```

---

## Signer Setup

Your signer is an Ed25519 keypair that authorizes posts:

**NOT the same as:**
- Ethereum wallet (different curve)
- Private key (Ed25519 vs ECDSA)
- Mnemonic seed

**Managed by:**
- clawcaster (handles for you)
- farcaster-agent (setup guided)

**Stored in:**
- `.env`: `FARCASTER_SIGNER_UUID` (reference)
- Farcaster hub: Actual key (don't expose)

---

## Frame Button Actions

```json
{
  "label": "Click me",
  "action": "post"              // Default, sends to post_url
}
```

```json
{
  "label": "Visit site",
  "action": "link",
  "target": "https://example.com"
}
```

```json
{
  "label": "Transaction",
  "action": "tx",
  "target": "https://yourapp.com/tx"
}
```

---

## Testing Checklist

- [ ] API key valid (test with `/user` endpoint)
- [ ] Signer UUID correct (test with dummy cast)
- [ ] FID correct (check Farcaster profile)
- [ ] Byte length checked (cast < 320 bytes)
- [ ] Channel ID correct (if using channel)
- [ ] Parent hash valid (if replying)
- [ ] Embeds publicly accessible (if using images)

---

## Rate Limits

**Free tier:** 300 requests/min

**Estimate your usage:**

- Post: 1 request
- Fetch mentions: 1 request
- Check feed: 1 request
- React (like): 1 request

**Example:** Daily automation

```
Daily post          = 1 req
Check mentions (2x) = 2 req
Auto-reply (5 max)  = 5 req
Monitor engagement  = 5 req
Total per day       = 13 req

Per month: ~400 req (plenty under 300/min limit)
```

---

## Troubleshooting

**Cast doesn't appear:**
- Check byte length (< 320)
- Wait 5-10 seconds (sync delay)
- Verify signer_uuid is valid
- Check API response for errors

**Mentions not showing:**
- Ensure filter_type is "mention" (not "reply")
- Check FID is correct
- Wait for hub sync (1-5 sec)

**Frame not loading:**
- Check HTML meta tags
- Verify post_url is publicly accessible
- Test endpoint with curl
- Check for CORS issues

**Rate limited:**
- Wait 1 minute
- Implement exponential backoff
- Batch requests if possible

---

## Production Checklist

- [ ] API key stored in `.env` (not hardcoded)
- [ ] Signer UUID stored in `.env`
- [ ] Error handling for rate limits
- [ ] Retry logic with exponential backoff
- [ ] Logging for all API calls
- [ ] Frame signature verification (if applicable)
- [ ] HTTPS for Frame post_url
- [ ] Testing on testnet before production

---

**Last Updated:** Feb 3, 2026  
**Accuracy:** Current as of Neynar v2 API
