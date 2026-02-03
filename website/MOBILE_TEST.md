# Mobile Design Testing Guide

## Quick Test (2 minutes)

### On Your iPhone
1. Visit: **https://astriaaiagent.vercel.app/**
2. Should see mobile version (bottom nav, stacked buttons, single column)
3. Scroll down - features, pricing, FAQ all mobile-optimized
4. Tap "Start Trial" or plan button → should go to mobile checkout
5. Check spacing, fonts - should feel modern and not cramped

### On Desktop/Laptop
1. Visit: **https://astriaaiagent.vercel.app/**
2. Should see original desktop version (top nav, side-by-side CTAs)
3. Compare - cleaner layout for bigger screen
4. Checkout should be side-by-side form + summary

## Test Platform Detection

### Force Mobile View (Chrome DevTools)
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M or Cmd+Shift+M)
3. Select iPhone or Android
4. Refresh page
5. Should redirect to `index-mobile.html` automatically

### Force Desktop View
1. Same DevTools
2. Toggle to desktop / laptop size
3. Refresh page
4. Should show original `index.html`

## Specific Things to Check

### Mobile (`index-mobile.html`)
- [ ] Header with logo + menu toggle
- [ ] Hero with "50+ Leads Every Day" and 2 buttons (stacked)
- [ ] Stats banner (50+ leads, 3.2% reply rate)
- [ ] Features as single-column cards
- [ ] "How It Works" with numbered steps (1-6)
- [ ] Results metrics (4 cards)
- [ ] Pricing cards (Starter/Standard/Enterprise, Standard highlighted)
- [ ] FAQ with expand/collapse
- [ ] **Bottom navigation bar** (3 buttons: Features, How It Works, Pricing)
- [ ] No horizontal scrolling
- [ ] All text readable without pinch-zoom
- [ ] Button spacing appropriate for thumb taps

### Mobile Checkout (`checkout-mobile.html`)
- [ ] Back button (←) in header
- [ ] Order summary at top (plan name, price, setup fee, total)
- [ ] Email & business name fields
- [ ] Address fields (street, city, state, zip)
- [ ] Stripe card field
- [ ] "Pay Now" button (full-width)
- [ ] Security note at bottom
- [ ] No horizontal scrolling
- [ ] All fields full-width and easy to tap

### Desktop (Unchanged)
- [ ] Both `index.html` and `checkout.html` should still work as before
- [ ] No regression in styling
- [ ] Side-by-side layouts intact

## Common Issues & Fixes

### "Page redirects too many times"
- **Cause**: Browser cached both versions in same tab
- **Fix**: Open in new private/incognito window

### Looks stretched on tablet
- **Expected**: Not optimized for iPad (medium viewport)
- **Note**: This is fine for MVP; iPad design can be added later

### Mobile version feels slow
- **Check**: Browser DevTools Network tab (any large images?)
- **Normal**: Mobile version is smaller than desktop

### "Start Trial" button doesn't work
- **Check**: Are you missing query parameter `?price=...`?
- **This is fine** - button fills in price automatically

## Metrics to Monitor

Once live, track these in Google Analytics (or similar):

### Mobile Metrics
- **Page load time** - Target: <3s
- **Click-through rate on CTAs** - Target: >2%
- **Checkout completion rate** - Target: >25%
- **Mobile traffic %** - Should increase with better design

### Desktop Metrics
- **No regression** in conversion rates
- **Page load time** - Should be unchanged
- **Desktop traffic %** - Should stay stable

## A/B Testing (Optional)

If you want to test which design converts better:

1. Use Vercel Analytics or Google Analytics
2. Track conversion rates separately for mobile vs desktop
3. Compare:
   - Landing page CTR
   - Checkout completion rate
   - Plan selection (which plan converts best on mobile)

## Going Live

✅ Changes are **live now** on Vercel
✅ Auto-deploy from GitHub (no manual step)
✅ Instant updates when you push changes

## Rollback (If Needed)

If something breaks:
```bash
git revert HEAD  # Undo last commit
git push         # Vercel auto-deploys the previous version
```

## Next: Collect Feedback

After testing:
1. Share mobile link with early customers
2. Ask: "Does this feel mobile-friendly?"
3. Collect feedback on:
   - Navigation (is bottom nav intuitive?)
   - Form (is checkout easy?)
   - Reading (are fonts too small?)
4. Make adjustments based on feedback

---

**TL;DR**: Visit the site on your phone and on desktop. Mobile should feel modern and purpose-built. Desktop should feel unchanged. If they don't, something's wrong—let me know!
