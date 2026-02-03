# Astria Webhook Server

Complete webhook integration for Cal.com bookings → Supabase automation.

## What It Does

When someone books a call via Cal.com:
1. Cal.com sends webhook to your server
2. Server receives booking details
3. Checks if lead exists in Supabase
4. Creates opportunity record
5. Updates lead status to "appointment_booked"
6. Logs activity

## Setup (5 Steps)

### Step 1: Install Dependencies

```bash
pip install -r webhook/requirements.txt
```

### Step 2: Configure .env

Add these to your `.env` file:

```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sbp_3bd29e93ddd96d89dd0f8a7af1c257c132406ad7
CALCOM_API_KEY=cal_live_a335953057662d932bd4b38521999779
WEBHOOK_URL=https://your-webhook-server.com/webhooks/calcom
CALCOM_WEBHOOK_SECRET=optional_secret_for_security
```

### Step 3: Deploy Webhook Server

#### Option A: Vercel (Easiest)

```bash
cd webhook
vercel --prod
```

Vercel will give you a URL like: `https://your-webhook.vercel.app`

#### Option B: Render

1. Go to https://render.com
2. Create new Web Service
3. Connect GitHub repo
4. Set Root Directory: `webhook`
5. Build command: `pip install -r requirements.txt`
6. Start command: `gunicorn app:app`
7. Add environment variables from .env
8. Deploy

#### Option C: Railway

```bash
railway link
railway up
```

#### Option D: Your Own Server

```bash
cd webhook
pip install -r requirements.txt
python app.py
# Or use gunicorn for production:
gunicorn app:app --bind 0.0.0.0:5000
```

### Step 4: Register Webhook with Cal.com

After deploying, update your webhook URL and run:

```bash
export WEBHOOK_URL=https://your-webhook.vercel.app/webhooks/calcom
export CALCOM_API_KEY=cal_live_a335953057662d932bd4b38521999779
python calcom/register_webhook.py
```

This will:
- List existing webhooks
- Create new webhook for BOOKING_CREATED, BOOKING_RESCHEDULED, BOOKING_CANCELLED
- Save config to `calcom/webhook.json`

### Step 5: Test It

1. Visit https://cal.com/astria/15min
2. Book a test appointment
3. Check your webhook server logs (should see booking details)
4. Check Supabase `opportunities` table (should have new record)

## Webhook Events

### BOOKING_CREATED
When someone books a call:
- Creates lead record (if new)
- Creates opportunity record
- Updates lead status to "appointment_booked"

### BOOKING_RESCHEDULED
When someone changes their appointment time:
- Updates opportunity date/time
- Maintains status as "scheduled"

### BOOKING_CANCELLED
When someone cancels their appointment:
- Updates opportunity status to "cancelled"
- Keeps record for reference

## API Endpoints

### GET `/health`
Health check for monitoring.

```bash
curl https://your-webhook.vercel.app/health
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2026-02-03T12:51:00.000Z"
}
```

### POST `/webhooks/calcom`
Receives Cal.com webhook events.

Payload example:
```json
{
  "triggerEvent": "BOOKING_CREATED",
  "payload": {
    "id": 12345,
    "eventName": "15 min meeting",
    "startTime": "2026-02-04T14:00:00Z",
    "endTime": "2026-02-04T14:15:00Z",
    "attendees": [
      {
        "name": "John Smith",
        "email": "john@example.com"
      }
    ],
    "organizer": {
      "name": "Astria",
      "email": "astriaaibot@gmail.com"
    }
  }
}
```

## Database Updates

When a booking is created, the webhook:

1. **Creates/updates lead record** in `leads` table
   - business_name
   - email
   - status: "appointment_booked"

2. **Creates opportunity record** in `opportunities` table
   - lead_id (linked to lead)
   - client_id (if known)
   - appointment_booked: true
   - appointment_date & appointment_time
   - show_status: "scheduled"

3. **Logs activity** in `activities_log` table
   - activity_type: "appointment_booked"
   - details: booking info
   - timestamp

## Monitoring

### Check Logs

**Vercel:**
```
vercel logs webhook
```

**Render:**
Check dashboard → Logs tab

**Railway:**
```bash
railway logs
```

**Local:**
```
tail -f webhook.log
```

### Common Issues

**"No payload"**
- Cal.com webhook didn't send data
- Check Cal.com webhook configuration

**"Invalid signature"**
- Webhook secret mismatch
- Update CALCOM_WEBHOOK_SECRET in .env

**"Supabase not connected"**
- Missing SUPABASE_SERVICE_ROLE_KEY
- Check .env variables

**"Lead not found"**
- Booking is from someone outside Astria campaigns
- Creates new lead in Supabase automatically

## Webhook Secret (Optional)

For security, Cal.com can sign webhook requests:

1. Add `CALCOM_WEBHOOK_SECRET=your_secret` to .env
2. Re-register webhook with `register_webhook.py`
3. Server will verify signature

## Testing Locally

If you want to test before deploying:

```bash
# Terminal 1: Start webhook server
python webhook/app.py

# Terminal 2: Send test request
curl -X POST http://localhost:5000/webhooks/calcom \
  -H "Content-Type: application/json" \
  -d '{
    "triggerEvent": "BOOKING_CREATED",
    "payload": {
      "id": 999,
      "eventName": "Test",
      "startTime": "2026-02-04T14:00:00Z",
      "endTime": "2026-02-04T14:15:00Z",
      "attendees": [{"name": "Test", "email": "test@example.com"}],
      "organizer": {"name": "Astria", "email": "astriaaibot@gmail.com"}
    }
  }'
```

## Production Checklist

- [ ] Webhook server deployed (Vercel/Render/Railway/own server)
- [ ] WEBHOOK_URL environment variable set
- [ ] Cal.com webhook registered with `register_webhook.py`
- [ ] Test booking created and logged in Supabase
- [ ] Monitoring alerts set up (optional)
- [ ] Webhook secret configured (optional but recommended)
- [ ] Database backups enabled (Supabase)

## Troubleshooting

**Webhooks not firing:**
1. Check Cal.com dashboard → Webhooks
2. Verify webhook is "active"
3. Check logs for delivery errors
4. Test with manual booking

**Data not appearing in Supabase:**
1. Check webhook server logs
2. Verify SUPABASE_SERVICE_ROLE_KEY
3. Check Supabase table permissions
4. Manually insert test record to verify connection

**"Unauthorized" errors:**
1. Verify SUPABASE_SERVICE_ROLE_KEY is correct (starts with `sbp_`)
2. Verify CALCOM_API_KEY is correct (starts with `cal_live_`)
3. Check Supabase API key permissions

## Files

- `app.py` — Main Flask webhook server
- `requirements.txt` — Python dependencies
- `vercel.json` — Vercel deployment config
- `WEBHOOK_SETUP.md` — This file

## Next Steps

1. ✅ Deploy webhook server
2. ✅ Register webhook with Cal.com
3. ✅ Test with booking
4. → Set up reply monitoring (future)
5. → Add email notifications (future)

---

**Webhook is live when you see "BOOKING_CREATED" events in your logs!** 🔗
