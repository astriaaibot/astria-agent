# Token Efficiency Rules

How to work with the Astria AI assistant while respecting token limits and maintaining high quality output.

---

## Golden Rules

### 1. **Brevity is Efficiency**
- Say what matters. Cut filler.
- Short sentences > long paragraphs
- Action > explanation
- "Done. Live." > "I'm pleased to inform you that the system is now operational and ready for use."

### 2. **Context is in Files, Not Messages**
- Point to documentation instead of explaining
- Example: "See TOKEN_EFFICIENCY.md#response-structure" instead of restating it in chat
- User can read, saves tokens, faster for everyone

### 3. **Ask Before Summarizing**
- Don't assume the user wants a full summary
- Ask: "Need a summary of Phase 2?" (user decides)
- Assume they can read docs unless they ask for help

### 4. **Self-Check Before Responding**
- Is this information in existing documentation? → Link instead
- Is this message > 100 tokens? → Can I shorten it?
- Are we repeating ourselves? → Point to previous conversation

### 5. **Batch Work, Not Chit-Chat**
- One message with 3 action items > 3 messages with 1 item each
- Combine related updates
- One decision point per message (avoid back-and-forth)

---

## Token Budget by Task

### Ideal Token Ranges

| Task | Ideal | Max | Notes |
|------|-------|-----|-------|
| Status update | 50-100 | 150 | Link to docs if detailed |
| Bug fix | 200-400 | 600 | Include code snippet |
| New feature | 400-800 | 1200 | Design doc in files, link here |
| Roadmap/planning | 300-600 | 1000 | Point to ROADMAP.md |
| Emergency | 100-200 | 300 | Quick fix, explain later in docs |
| Documentation | 2000+ | ∞ | These are fine (not message overhead) |

### Total Session Budget
- **Daily:** 50k tokens (shared for all messages back & forth)
- **Per message:** 500 tokens (hard limit, auto-truncate above)
- **Per task:** Varies (see above)

---

## Response Structures

### Status Updates (50-100 tokens)
```
✅ [What's done]
⏳ [What's waiting]
❌ [Blockers]
🎯 [Next step]
```

### Technical Explanations (200-300 tokens)
```
[1-2 sentence summary]
[Code snippet or example if relevant]
[1 sentence on why]
[Link to full docs]
```

### Action Items (100-150 tokens)
```
IMMEDIATE (this hour/day):
• [Item 1]
• [Item 2]

NEXT (this week):
• [Item 3]
• [Item 4]
```

### Problem Solving (300-500 tokens)
```
PROBLEM: [What's broken]
CAUSE: [Why it broke]
FIX: [What to do]
VERIFY: [How to test]
[Link to relevant docs if complex]
```

---

## What NOT to Do

### ❌ Unnecessary Verbosity
```
I appreciate your interest in understanding the current state of the Astria platform, 
and I would like to provide you with a comprehensive overview of the various components 
and their current operational status. As you may know, the Astria project encompasses...
```

**Better:**
```
Current status: Website live, Stripe ready, waiting on Supabase keys.
```

### ❌ Repeating Documentation
```
User: "How do I set up Stripe?"
Assistant: [Restates all of STRIPE_SETUP.md]
```

**Better:**
```
See STRIPE_SETUP.md. Summary: create products → get API keys → add to .env
```

### ❌ Over-Explaining Simple Things
```
The GitHub platform, which is a distributed version control system widely used 
in software development, has been utilized in this project as a central repository...
```

**Better:**
```
GitHub repo live: github.com/astriaaibot/astria-agent
```

### ❌ Creating Messages That Should Be Docs
If response > 500 tokens and you're explaining complex concepts → write it to a file instead.

---

## Efficient Workflows

### Scenario 1: Quick Status Check
**User:** "What's the status?"

**Efficient:**
```
✅ Website live (desktop + mobile, modern)
✅ Stripe configured (3 products, webhooks ready)
⏳ Backend deployment (waiting on Fly.io setup)
⏳ Supabase init (waiting on user keys)
❌ Telegram (bot creation needed)

Next: Deploy backend, init Supabase.
See ROADMAP.md for timeline.
```

**Not efficient (way too long):**
```
The current status of the Astria project encompasses multiple components, each at 
different stages of completion. The website, which consists of both desktop and mobile 
versions, is now live and available at [URL]. Both versions incorporate modern design 
principles and are responsive to user interactions...
```

### Scenario 2: Debugging Issue
**User:** "Webhook not firing. What's wrong?"

**Efficient:**
```
PROBLEM: Stripe webhook not triggering
LIKELY CAUSE: Endpoint not registered in Stripe Dashboard
FIX:
1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: [your-url]/webhook/stripe
3. Copy signing secret → add to .env as STRIPE_WEBHOOK_SECRET
4. Restart webhook server

TEST: Use Stripe Dashboard test event
See webhook/WEBHOOK_SETUP.md for full guide
```

### Scenario 3: Feature Request
**User:** "Can we add X feature?"

**Efficient:**
```
ASSESSMENT:
- Impact: Medium (helps Y use case)
- Effort: High (requires Z changes)
- Priority: Low (not on roadmap for Q1)

RECOMMENDATION: Add to Phase 3 (scale phase). Document in ROADMAP.md.

See ROADMAP.md phase breakdown for context.
```

---

## Memory & Context Management

### What I Should Remember (and where)
- **Session context:** Last message in this conversation
- **Project state:** memory/astria-project-state.md (updated weekly)
- **Decisions:** BUILDOUT.md, ROADMAP.md
- **Daily notes:** memory/YYYY-MM-DD.md (created daily if needed)

### What I Should NOT Remember
- Chatty exchanges that don't matter
- Decisions that are documented
- Conversations that could be files

### Efficiency Rule
- If it's important, write it to a file
- If it's in a file, reference the file (don't repeat)
- If it's neither, we probably don't need it

---

## Writing Efficient Documentation

### Docs ARE Worth Tokens (Do Them Right)

**Structure for Efficiency:**
1. **Title + TL;DR** (first sentence tells the story)
2. **Quick Reference** (table/checklist for scanning)
3. **Detailed Explanation** (for context)
4. **Examples/Code** (show, don't tell)
5. **Links** (to related docs)

**Example: Good Doc Structure**
```markdown
# Feature X

**What it does:** [1 sentence]

**When to use it:** [1 sentence]

**Quick Setup:**
• Step 1
• Step 2
• Step 3

[Detailed explanation if needed]

[Code example]

See also: [Related docs]
```

---

## Token Usage Monitoring

### How to Check Your Token Usage
```
After each response, I'll note estimated tokens:
"~250 tokens / 50k daily budget"
```

### Warning Signs (Too Many Tokens)
- Responses consistently > 500 tokens
- Same info explained multiple times
- Repeating documentation in messages
- Long back-and-forth that should be a decision

### How to Reduce
1. Write more documentation
2. Use links instead of explanations
3. Use tables instead of paragraphs
4. Ask clarifying questions (focus effort)
5. Suggest user read docs for detailed info

---

## Best Practices Checklist

Before sending a message, ask:

- [ ] **Is this already documented?** → Link instead
- [ ] **Can this be shorter?** → Cut filler
- [ ] **Should this be a file?** → Write it down
- [ ] **Is there code?** → Include snippet, link to full file
- [ ] **Will user understand without context?** → Provide context
- [ ] **Could this be a table/list?** → Format it
- [ ] **Am I repeating myself?** → Reference previous message
- [ ] **Is this > 500 tokens?** → Should it be a doc?

---

## Special Cases

### Emergency (On Fire)
- **Tokens:** Don't worry, fix it fast
- **Later:** Document what happened and why
- **Example:** "Production down. Restarting now. See [file] for details once fixed."

### Complex Explanation Needed
- **Don't:** Try to fit it in a message (use 2000 tokens)
- **Do:** Write it to a file, link it, give 50-token summary
- **Example:** "Complex topic. Created FEATURE_X.md for full explanation. Key points: [summary]"

### User Asks for Detailed Write-Up
- **Great!** Worth the tokens. Write comprehensive docs.
- **Structure:** Use markdown, headings, examples
- **After:** Summarize for chat, link to file

---

## Evolving This Rules

As we learn what works:
- Document new patterns
- Remove what doesn't work
- Share learnings with team (future)
- Update this file quarterly

---

## TL;DR

**Work efficiently:**
1. Document important things
2. Link instead of repeat
3. Be brief
4. Ask before explaining

**Token budget:**
- ~500 tokens per message
- ~50k per day
- Docs don't count against message budget

**Golden rule:**
> If it's in a file, reference it. If it's not in a file and matters, write it.

---

**Last Updated:** February 3, 2026  
**Status:** Active  
**Next Review:** February 17, 2026
