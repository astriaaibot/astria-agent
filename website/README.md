# Astria Website

Complete website for Astria - Autonomous AI Sales Agent.

## Files

### Core Pages
- `index.html` — Original landing page
- `index-modern.html` — Modern redesigned landing page (recommended)
- `dashboard.html` — Client portal (real-time metrics)
- `checkout.html` — Stripe payment checkout

### Styling
- `style.css` — Original landing page styles
- `style-modern.css` — Modern landing page styles
- `dashboard.css` — Client dashboard styles

### Scripts
- `script.js` — Original landing page interactions
- `script-modern.js` — Modern landing page interactions
- `dashboard.js` — Dashboard interactions

### Configuration
- `favicon.svg` — Astria lightning bolt favicon
- `manifest.json` — PWA manifest (app info, icons)
- `robots.txt` — Search engine crawling rules
- `sitemap.xml` — URL structure for search engines
- `_redirects` — Vercel routing rules
- `.htaccess` — Apache server configuration (optional)

### Documentation
- `README.md` — This file
- `DEPLOY.md` — Deployment guide

## Quick Links

- **Main Site:** https://astria.fun (redirects to index-modern.html)
- **Modern Site:** https://astria.fun/index-modern.html
- **Dashboard:** https://astria.fun/dashboard.html
- **Checkout:** https://astria.fun/checkout.html

## Features

### Landing Page (Modern)
- ⚡ Stunning hero section with gradient backgrounds
- 📊 8-step automated process visualization
- 💰 3-tier pricing (Starter, Standard, Enterprise)
- 📈 Metrics & social proof
- ❓ FAQ section
- 🎯 Clear CTAs throughout

### Client Dashboard
- 📊 Real-time KPIs (leads, emails, replies, appointments)
- 🔍 Lead management
- 📧 Email performance metrics
- 📅 Appointment calendar
- 📈 Weekly reports
- ⚙️ Settings & configuration

### Checkout Page
- 🔐 Secure Stripe integration
- 💳 Real payment processing
- 🎯 Tier selection
- 📝 Order summary

## Deployment

### Vercel (Recommended)
```bash
vercel --prod
```

### GitHub Pages
```bash
git add .
git commit -m "Update website"
git push origin main
```

### Self-Hosted
Copy all files to your web server public directory.

## Icons & Branding

- **Favicon:** Lightning bolt (⚡) in gradient (Indigo → Cyan)
- **Colors:** 
  - Primary: `#6366f1` (Indigo)
  - Accent: `#06b6d4` (Cyan)
- **Fonts:** 
  - Headlines: Space Grotesk (bold, modern)
  - Body: Inter (clean, readable)

## SEO & Optimization

- ✅ Favicon for browser tab
- ✅ Manifest.json for PWA
- ✅ Robots.txt for search engines
- ✅ Sitemap.xml for indexing
- ✅ Meta tags (OG, description)
- ✅ Responsive design (mobile-first)
- ✅ GZIP compression support

## Performance

- ⚡ Fast load times
- 📱 Mobile optimized
- 🎨 Smooth animations
- 🔒 Secure (HTTPS)

## Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## File Structure

```
website/
├── index.html              # Original landing page
├── index-modern.html       # Modern landing page (recommended)
├── dashboard.html          # Client portal
├── checkout.html           # Payment checkout
│
├── style.css               # Original styles
├── style-modern.css        # Modern styles
├── dashboard.css           # Dashboard styles
│
├── script.js               # Original interactions
├── script-modern.js        # Modern interactions
├── dashboard.js            # Dashboard interactions
│
├── favicon.svg             # Browser icon
├── manifest.json           # PWA config
├── robots.txt              # SEO crawler rules
├── sitemap.xml             # URL structure
├── _redirects              # Vercel routing
├── .htaccess               # Apache config
│
├── README.md               # This file
└── DEPLOY.md               # Deployment guide
```

## Testing Checklist

- [ ] Homepage loads (landing page)
- [ ] Modern design loads (`/index-modern.html`)
- [ ] Dashboard loads (`/dashboard.html`)
- [ ] Checkout page loads (`/checkout.html`)
- [ ] All links work
- [ ] Favicon appears in browser tab
- [ ] Mobile responsive (test on phone)
- [ ] Stripe test card works (4242 4242 4242 4242)
- [ ] Animations smooth
- [ ] Page loads in <3 seconds

## Maintenance

### Weekly
- Check analytics
- Monitor checkout flow
- Test links

### Monthly
- Update copy if needed
- Review metrics
- Check for broken links

### Quarterly
- Update sitemap.xml
- Refresh CSS/JS if bugs found
- Security audit

## Support

- Landing Page: `https://astria.fun`
- Dashboard: `https://astria.fun/dashboard.html`
- Checkout: `https://astria.fun/checkout.html`
- Contact: hello@astria.fun

---

**Last Updated:** 2026-02-03  
**Status:** ✅ Ready for Production
