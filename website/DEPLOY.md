# Deploy Astria Website

## Quick Deploy (Choose One)

### 🚀 Option 1: Vercel (Recommended - 2 min)

Simplest, fastest. Perfect for astria.fun.

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy (from website folder)
cd website
vercel --prod

# Follow prompts:
# - Link to GitHub repo? (optional, pick "other")
# - Project name? astria
# - Deploy from current directory? Yes

# Get your URL, then add custom domain:
# Settings → Domains → Add astria.fun
```

**Result:** Live in seconds at `https://astria.fun`

---

### 🌐 Option 2: Netlify (2-3 min)

Also fast. Easy domain setup.

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy (from website folder)
cd website
netlify deploy --prod

# Pick custom domain: astria.fun
```

---

### 📦 Option 3: Self-Hosted on Your Server (5 min)

If you have your own server/VPS:

```bash
# Copy files to your web root
scp -r website/* user@astria.fun:/var/www/astria/

# Make sure nginx/apache is serving that directory
# Point astria.fun DNS to your server

# Test: curl https://astria.fun
```

---

### 🐙 Option 4: GitHub Pages (3 min)

Free, if you have GitHub repo:

```bash
# 1. Push website folder to GitHub
git add website/
git commit -m "Add Astria landing page"
git push origin main

# 2. In GitHub repo settings:
# - Settings → Pages
# - Source: Deploy from a branch
# - Branch: main, folder: /website

# 3. Add custom domain:
# - Settings → Pages → Custom domain
# - Enter: astria.fun
# - Update DNS CNAME to point to GitHub Pages

# Done! Live at https://astria.fun
```

---

## Post-Deploy Checklist

After deploying, verify:

- [ ] **Homepage loads:** https://astria.fun
- [ ] **Responsive:** Works on mobile + desktop
- [ ] **Links work:** Click "Book a Demo" → Cal.com
- [ ] **Email link works:** Click "astriaaibot@gmail.com"
- [ ] **Navigation smooth:** Scroll to sections works
- [ ] **SSL cert:** HTTPS shows locked padlock

---

## Update Website Later

Any changes? Redeploy:

```bash
# Edit files (index.html, style.css, script.js)

# Redeploy
cd website
vercel --prod  # or netlify deploy --prod
```

Changes live in 30 seconds.

---

## Domain Setup

If you own astria.fun but domain isn't pointed yet:

### Add DNS Records:

**For Vercel:**
```
Name: @
Type: CNAME
Value: astria-git-main.vercel.app
```

**For Netlify:**
```
Name: @
Type: CNAME
Value: astria.netlify.app
```

**For Self-Hosted:**
```
Name: @
Type: A
Value: [your-server-ip]
```

---

## Monitor Performance

**Vercel Dashboard:**
- Deployments, build logs, analytics
- https://vercel.com/dashboard

**Netlify Dashboard:**
- Builds, deploys, analytics
- https://app.netlify.com

---

## Troubleshooting

**Site not loading?**
- Clear browser cache (Cmd+Shift+R)
- Check DNS propagation: https://dnschecker.org

**Domain not working?**
- DNS can take 24-48 hours to propagate
- Check CNAME record is correct
- Verify in your registrar's DNS settings

**Styles not showing?**
- Check browser console for CSS errors (F12)
- Verify style.css and script.js deployed
- Clear cache

---

## Need Help?

- **Vercel support:** https://vercel.com/help
- **Netlify support:** https://support.netlify.com
- **Domain registrar:** Contact them for DNS help

---

**Pick one option above and deploy now.** Site will be live in 2-5 minutes.
