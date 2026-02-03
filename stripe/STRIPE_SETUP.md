# Stripe Integration Setup

Complete guide to set up Stripe for Astria pricing, payments, and subscriptions.

---

## Step 1: Create Products & Prices in Stripe

### Automated Setup (Recommended)

```bash
# Make sure .env has your Stripe Secret Key
pip install stripe

# Run setup script
python stripe/setup_products.py

# Output will save to stripe/products.json
```

### Manual Setup (Alternative)

Go to https://dashboard.stripe.com/acct_1SwmTpEe7Idz4FdT/test/products

1. **Create Product: "Astria Starter"**
   - Name: Astria Starter
   - Description: 30-50 leads per month, 1-2 appointments per week
   - Type: Service
   - Pricing:
     - Monthly: $299/month (recurring)
     - Setup: $99 (one-time)

2. **Create Product: "Astria Standard"**
   - Name: Astria Standard
   - Description: 80-120 leads per month, 2-4 appointments per week
   - Type: Service
   - Pricing:
     - Monthly: $699/month (recurring)
     - Setup: $199 (one-time)

3. **Create Product: "Astria Enterprise"**
   - Name: Astria Enterprise
   - Description: 200+ leads per month, 4-8 appointments per week
   - Type: Service
   - Pricing:
     - Monthly: $1,299/month (recurring)
     - Setup: $299 (one-time)

---

## Step 2: Get Product IDs

After creating products, save the IDs from Stripe:

```json
{
  "starter": "price_xxxxx (monthly)",
  "starter_setup": "price_xxxxx (setup)",
  "standard": "price_xxxxx (monthly)",
  "standard_setup": "price_xxxxx (setup)",
  "enterprise": "price_xxxxx (monthly)",
  "enterprise_setup": "price_xxxxx (setup)"
}
```

Save to `stripe/products.json` (the script does this automatically)

---

## Step 3: Wire Website to Stripe Checkout

Update `website/script.js`:

```javascript
function checkout(tier) {
    const stripe = Stripe('YOUR_PUBLISHABLE_KEY');
    
    // Map tier to price ID
    const priceIds = {
        starter: ['price_starter_monthly', 'price_starter_setup'],
        standard: ['price_standard_monthly', 'price_standard_setup'],
        enterprise: ['price_enterprise_monthly', 'price_enterprise_setup']
    };
    
    // Redirect to Stripe checkout
    stripe.redirectToCheckout({
        lineItems: priceIds[tier].map(priceId => ({
            price: priceId,
            quantity: 1
        })),
        mode: 'subscription',
        successUrl: 'https://astria.fun/success',
        cancelUrl: 'https://astria.fun/pricing'
    });
}
```

---

## Step 4: Create Webhook Endpoint

When a customer subscribes, Stripe sends a webhook. Handle it:

```python
# In your backend (e.g., Flask, FastAPI)
@app.post("/webhooks/stripe")
def stripe_webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, STRIPE_WEBHOOK_SECRET
    )
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_id = session['customer']
        subscription_id = session['subscription']
        
        # Store in Supabase
        supabase.table('clients').update({
            'stripe_customer_id': customer_id,
            'stripe_subscription_id': subscription_id,
            'subscription_status': 'active'
        }).match({'email': session['customer_email']}).execute()
    
    return {'success': True}
```

---

## Step 5: Test in Test Mode

Stripe has test cards for testing:

- **Success:** `4242 4242 4242 4242`
- **Decline:** `4000 0000 0000 0002`
- **Requires auth:** `4000 0025 0000 3155`

Expiry: any future date  
CVC: any 3 digits

---

## Step 6: Enable Webhooks

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. URL: `https://your-backend.com/webhooks/stripe`
4. Events to listen to:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`

5. Click "Add endpoint"
6. Copy webhook secret → save to `.env` as `STRIPE_WEBHOOK_SECRET`

---

## Step 7: Deploy to Production

When ready to go live:

1. Switch from Test keys to Live keys in Stripe
2. Update `.env`:
   ```
   STRIPE_PUBLISHABLE_KEY=pk_live_...
   STRIPE_SECRET_KEY=sk_live_...
   ```

3. Update website with live publishable key
4. Test with real card (you'll be charged $0.50 for verification, refunded immediately)

---

## Step 8: Monitor Subscriptions

Track in Supabase:

```sql
SELECT 
    business_name,
    subscription_tier,
    subscription_status,
    stripe_subscription_id,
    created_date
FROM clients
WHERE subscription_status = 'active'
ORDER BY created_date DESC;
```

---

## Testing Checklist

- [ ] Created 3 products in Stripe
- [ ] Prices set correctly ($299, $699, $1,299 monthly)
- [ ] Setup fees configured ($99, $199, $299)
- [ ] Product IDs saved in `stripe/products.json`
- [ ] Test mode webhook created + secret saved
- [ ] Tested checkout with test card
- [ ] Supabase webhook handler written + deployed
- [ ] Test subscription appears in Supabase
- [ ] Webhook confirmation email received

---

## Live Checklist (Before Going Live)

- [ ] Live API keys in `.env` (not test keys!)
- [ ] Live webhook endpoint created
- [ ] HTTPS enabled on your domain
- [ ] Stripe SSL certificate verified
- [ ] Test with real card (small amount)
- [ ] Monitor first real subscription
- [ ] Customer email confirmation working

---

## Resources

- Stripe Dashboard: https://dashboard.stripe.com
- Stripe Docs: https://stripe.com/docs
- Webhook Signing: https://stripe.com/docs/webhooks/signatures

---

## Support

- Stripe Support: https://support.stripe.com
- In case of payment issues, check Stripe logs
- Monitor webhooks: Dashboard → Webhooks → View logs

---

**Ready? Start with Step 1.**
