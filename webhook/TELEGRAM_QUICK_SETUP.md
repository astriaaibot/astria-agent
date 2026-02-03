# Telegram Bot Setup - Quick Reference

## Get Bot Token (2 min)

1. **Telegram**: Search for **@BotFather** → Start chat
2. **Send**: `/newbot`
3. **Answer prompts**:
   - Bot name: `Astria Bot` (or any name)
   - Bot username: `astria_notifications_bot` (must be unique, ends in `_bot`)
4. **Copy token** → Add to `.env` as `TELEGRAM_BOT_TOKEN`

**Example token:**
```
123456789:ABCDefGHIjklmnoPQRstuvwxyzABCDefg
```

## Get Chat ID (1 min)

1. **Telegram**: Find your bot in search → Start chat → Send `/start`
2. **Browser**: Go to:
   ```
   https://api.telegram.org/bot<PASTE_YOUR_TOKEN>/getUpdates
   ```
3. **Look for**: `"chat":{"id":<THIS_IS_YOUR_ID>}`
4. **Copy ID** → Add to `.env` as `TELEGRAM_CHAT_ID`

**Example:**
```
{
  "ok": true,
  "result": [
    {
      "message": {...},
      "chat": {
        "id": 987654321    ← YOUR CHAT ID
      }
    }
  ]
}
```

## Test It Works

```bash
# Test bot responds
curl "https://api.telegram.org/bot<TOKEN>/getMe"

# Test sending message
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": <CHAT_ID>, "text": "Testing"}'
```

## .env Example

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHIjklmnoPQRstuvwxyzABCDefg
TELEGRAM_CHAT_ID=987654321
```

## Done! ✅

That's it. The webhook will now send Telegram messages when:
- New customer signs up
- Pipeline events happen
- Errors occur

---

**Reminder**: Keep these values in `.env` (never commit to Git).
