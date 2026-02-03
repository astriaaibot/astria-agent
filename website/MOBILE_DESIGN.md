# Mobile-First Design Strategy

## Overview
Astria now has **dedicated mobile and desktop versions** for optimal UX on each device. This isn't responsive design—it's two purpose-built experiences.

## Files

### Mobile-First (Primary for Mobile Devices)
- **`index-mobile.html`** - Mobile landing page
- **`checkout-mobile.html`** - Mobile checkout flow
- **`detect-platform.js`** - Auto-detection and redirect logic

### Desktop (Optimized for Large Screens)
- **`index.html`** - Desktop landing page
- **`checkout.html`** - Desktop checkout

### Auto-Detection
Both `index.html` and `checkout.html` now include platform detection scripts in the `<head>`:
```html
<script>
    const isMobile = () => /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || window.innerWidth < 768;
    if (isMobile()) {
        window.location.replace('/index-mobile.html' + window.location.search);
    }
</script>
```

**How it works:**
1. User visits `/` (desktop version by default)
2. If detected as mobile: **auto-redirects** to `index-mobile.html`
3. If already on correct version: no redirect (no flicker)

## Mobile Design Features

### ✨ Touch-First
- **Large touch targets** (min 44px × 44px per Apple HIG)
- **Smooth scrolling** with `scroll-behavior: smooth`
- **Bottom navigation bar** (thumb-friendly)
- **Reduced cognitive load** - simpler layouts

### 📱 Mobile-Optimized Layout
- **Single-column grid** (no multi-column layouts)
- **Stacked buttons** (full-width, easy to tap)
- **Large fonts** (no squinting)
- **Generous spacing** (thumb-friendly gaps)
- **Safe area support** (notches, home indicators via `env(safe-area-inset-*)`)

### 🚀 Performance
- **Minimal CSS** (~8KB instead of 20KB)
- **No animations on scroll** (battery-friendly)
- **Touch-optimized interactions** (no hover states)
- **Optimized images** (smaller on mobile)

### 🎨 Visual Hierarchy
- **Bottom navigation** - Key actions always accessible
- **Hero section** - Strong CTA above fold
- **Feature cards** - Tap-responsive with visual feedback
- **Sticky header** - Navigation always visible

## Key Differences: Mobile vs Desktop

| Aspect | Mobile | Desktop |
|--------|--------|---------|
| **Navigation** | Bottom nav bar (fixed) | Top navbar (sticky) |
| **CTAs** | Stacked, full-width | Side-by-side, contained |
| **Features** | Single column | Multi-column grid |
| **Typography** | Larger base (16px) | Standard (14-16px) |
| **Spacing** | Generous (1.5rem gaps) | Tighter (1rem gaps) |
| **Interactions** | Tap/scroll | Click/hover |

## Checkout Flow

### Desktop (`checkout.html`)
- Side-by-side order summary + form
- Multiple input fields visible at once
- Horizontal button layouts

### Mobile (`checkout-mobile.html`)
- Order summary at top (sticky)
- Form below
- Full-width inputs
- Vertical button stack
- Minimal scrolling required

## Analytics & Testing

Platform info is stored in `window.platformInfo`:
```javascript
{
    isMobile: true,
    userAgent: "Mozilla/5.0...",
    timestamp: "2025-02-03T..."
}
```

Use this to track conversion rates by device.

## Deployment

### Vercel
Platform detection is **automatic** - just push all files:
```
/index.html              (desktop)
/index-mobile.html       (mobile)
/checkout.html           (desktop)
/checkout-mobile.html    (mobile)
/detect-platform.js      (utility)
```

No special config needed. Detection happens client-side.

### Testing
- **Desktop**: Visit in Chrome DevTools desktop mode
- **Mobile**: Visit in DevTools mobile emulation or real device
- **Cross-check**: Verify auto-redirect works both ways

## CSS Variables & Dark Mode

Both versions use the same color scheme:
```css
--primary: #6366f1     (Indigo)
--accent: #06b6d4      (Cyan)
--bg-dark: #0f172a     (Dark navy)
```

Support for `prefers-color-scheme` is built-in (dark mode by default).

## Accessibility

✅ **Mobile**
- Touch targets >44×44px
- Focus indicators visible
- Color contrast >4.5:1
- Semantic HTML

✅ **Desktop**
- Keyboard navigation
- Hover states
- ARIA labels
- Semantic HTML

## Future Enhancements

- [ ] Add iPad-specific design (medium viewport)
- [ ] Implement PWA for mobile install
- [ ] Add web app shortcuts (mobile launcher)
- [ ] Dark mode toggle (manual override)
- [ ] A/B test conversion rates by design

## Rollback

If mobile design needs tweaking:
1. Update `index-mobile.html` directly
2. Vercel auto-deploys on push
3. No impact to desktop version
4. Users see changes instantly

---

**TL;DR:** Mobile users get a purpose-built mobile experience. Desktop users get the full feature set. Auto-detection handles routing. No confusing responsive design—just two great experiences.
