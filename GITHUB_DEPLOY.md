# Push to GitHub

Everything is committed and ready to push. Follow these steps to create a new GitHub repo and deploy.

---

## Option 1: Using GitHub CLI (Fastest)

```bash
# 1. Ensure you're logged in to GitHub CLI
gh auth status

# 2. Create new repo (public or private)
gh repo create astria-agent \
  --public \
  --source=. \
  --remote=origin \
  --push

# Done! Your repo is live at github.com/yammerboss/astria-agent
```

---

## Option 2: Manual (Via GitHub Web)

```bash
# 1. Go to https://github.com/new
# 2. Create repo: "astria-agent" (public)
# 3. Do NOT initialize with README (we have one)
# 4. Copy the repo URL

# 5. In terminal:
cd /Users/yammerboss/.openclaw/workspace

# 6. Add remote
git remote add origin https://github.com/yammerboss/astria-agent.git

# 7. Push
git branch -M main
git push -u origin main

# Done!
```

---

## What Gets Pushed

✅ **Code:**
- Landing page (`website/index.html`, `.css`, `.js`)
- Client dashboard (`website/dashboard.html`, `.css`, `.js`)
- All 8 Python scripts (scraper, scoring, analysis, emails, replies, reporting)
- Database schema (`database/init_schema.sql`)

✅ **Documentation:**
- `README.md` — Project overview
- `ASTRIA_SPRINT.md` — 14-day checklist
- `BUILDOUT.md` — Full plan + costs
- `TEST_SETUP.md` — Testing guide
- `RUN_PIPELINE.md` — How to run
- `website/DEPLOY.md` — Website deployment

✅ **.gitignore** — Excludes `.env`, `node_modules`, `__pycache__`, etc.

❌ **NOT pushed:**
- `.env` (secrets never committed)
- `node_modules/`
- Python cache files
- System files

---

## After Push: GitHub Actions (Optional)

You can add CI/CD workflows to auto-test scripts, but for now, just push the code.

---

## Deploy Website from GitHub

Once pushed, deploy the landing page + dashboard to Vercel:

```bash
# 1. Install Vercel CLI (if not done)
npm install -g vercel

# 2. Deploy from GitHub repo
cd website
vercel --prod

# 3. When Vercel asks for project name:
#    → Choose "astria" or "astria-web"

# 4. Connect to GitHub (optional but recommended)
#    → Vercel will auto-deploy on every push to main

# 5. Add custom domain: astria.fun
#    → In Vercel dashboard: Settings → Domains
#    → Add astria.fun, follow DNS setup

# Live in <2 minutes!
```

---

## Verify on GitHub

After push, check:
1. https://github.com/yammerboss/astria-agent
2. Should see all files + folders
3. README displays nicely
4. Commit message shows "🚀 Astria v1..."

---

## Next Steps After GitHub

1. **Star the repo** (bookmark for later)
2. **Share with team** (if you have one)
3. **Deploy website** (Vercel, see above)
4. **Get API keys** (Supabase, Claude, Stripe)
5. **Run `TEST_SETUP.md`** (verify everything works)
6. **Go live with first client**

---

## Commit Often

As you make changes:

```bash
git add .
git commit -m "Update [what changed]"
git push
```

This keeps GitHub in sync with your local changes.

---

**Ready to push? Go!**

```bash
gh repo create astria-agent --public --source=. --remote=origin --push
```

Or follow Option 2 above.

Let me know once it's live! 🚀
