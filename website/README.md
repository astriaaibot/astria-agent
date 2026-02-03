# Astria Website

Modern, responsive landing page for the Astria autonomous AI sales agent.

## Files

- `index.html` — Main landing page (HTML structure)
- `style.css` — Styling (responsive, modern design)
- `script.js` — Interactions (smooth scrolling, animations)

## Features

✅ **Hero section** with clear value prop  
✅ **Problem/Solution comparison**  
✅ **How It Works** (6-step process)  
✅ **Features grid** (8 core features)  
✅ **Pricing cards** (3 tiers)  
✅ **FAQ section**  
✅ **CTA to book demo**  
✅ **Fully responsive** (mobile, tablet, desktop)  
✅ **Smooth animations** and scroll effects  
✅ **Modern design** with clean typography

## Deployment Options

### Option 1: Vercel (Fastest)
```bash
npm install -g vercel
vercel
# Follow prompts, select this folder
```

### Option 2: Netlify
```bash
npm install -g netlify-cli
netlify deploy --prod --dir .
```

### Option 3: GitHub Pages
1. Push to GitHub
2. Enable Pages in repo settings
3. Set deploy branch to `main`

### Option 4: Self-hosted (your server)
```bash
# Copy files to your web server
scp -r ./* user@astria.fun:/var/www/html/
```

## Customization

### Update Domain
- Find `https://cal.com/astria/discovery-call` and replace with your Cal.com link
- Find `hello@astria.fun` and replace with your contact email

### Update Colors
Edit `:root` variables in `style.css`:
```css
--primary: #0066ff;        /* Main blue */
--primary-dark: #0052cc;   /* Hover blue */
--secondary: #ff6b35;      /* Orange accent */
```

### Update Copy
Edit text directly in `index.html`:
- Hero title and subtitle
- Feature descriptions
- Pricing details
- FAQ answers

## Analytics (Optional)

Add Google Analytics:
```html
<!-- Add before </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

## SEO Optimization

Update in `index.html` `<head>`:
```html
<meta name="description" content="...">
<meta name="keywords" content="...">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">
```

## Testing

Open `index.html` in a browser:
```bash
open index.html
```

Or use a local server:
```bash
python3 -m http.server 8000
# Visit http://localhost:8000
```

## Performance

- Lightweight (no external dependencies)
- Fast load time (<1s)
- Mobile-optimized
- SEO-friendly
- Accessibility-conscious

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: All modern

## License

© 2026 Astria. All rights reserved.
