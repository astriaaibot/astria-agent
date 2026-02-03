#!/usr/bin/env python3
"""
ASTRIA EMAIL WRITER
Generates 3-email sequences using Claude.
Run: python emails/write_sequences.py --client-id <id>
"""

import os
import sys
import json
import logging
from datetime import datetime

try:
    import anthropic
    from supabase import create_client, Client
    from dotenv import load_dotenv
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Install with: pip install anthropic supabase python-dotenv")
    sys.exit(1)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, CLAUDE_API_KEY]):
    logger.error("❌ Missing required .env variables")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
claude = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

EMAIL_WRITING_PROMPT = """You write cold outreach emails for Astria, an AI-powered service that finds and books new customers for local businesses. The business owner you are writing to is busy, skeptical of marketing pitches, and gets spam daily. Your email must feel like it was written by a real human who actually looked at their business.

TARGET BUSINESS:
Name: {business_name}
Category: {category}
Location: {city}, {state}
Rating: {google_rating} stars, {review_count} reviews
Website: {website}
Services: {services}
Unique selling point: {usp}
Pain points: {pain_points}
Personalization hook: {personalization_hook}

CLIENT OFFERING:
Astria finds and books qualified appointments for local service businesses. AI-powered. Exclusive leads (not shared). Appointments appear on their calendar. They only pay for results. Starting at $500/month.

RULES — follow every single one:
1. Each email MUST be under 100 words. Shorter is better. 60–80 words ideal.
2. Reference something SPECIFIC about their actual business in Email 1. Use the personalization hook.
3. Sound like a real person. No marketing jargon. No "revolutionary" or "cutting-edge" or "game-changing."
4. Never use exclamation marks in subject lines.
5. Never start with "I hope this finds you well" or "My name is" or "I'm reaching out because."
6. One CTA per email. Make it easy — a reply, not a long form.
7. Subject lines: lowercase, short, conversational. Like a text from a colleague.
8. No emoji in subject lines or body.
9. Write from first person as "Alex from Astria" — a person, not a company.

WRITE 3 EMAILS:

Email 1 — PERSONALIZED INTRO (send Day 0):
Open with the personalization hook. Briefly explain what Astria does. Ask if they'd be open to seeing how it works. CTA: "Would you be open to a quick 15-min walkthrough?"

Email 2 — DIFFERENT ANGLE (send Day 3):
Don't repeat Email 1. Come at it from a different angle:
- Mention a specific pain point you identified
- Or reference what competitors in their area are doing
- Or share a concrete result ("We helped a [similar business type] in [area] book 12 new appointments in their first month")
CTA: "Want me to show you how it works for {category} specifically?"

Email 3 — BREAKUP (send Day 7):
Short. 3–4 sentences max. Acknowledge they're busy. Say you won't follow up again after this. Leave the door open.
CTA: "If the timing is ever better, just reply to this email."

Return ONLY a valid JSON array, no other text:
[
  {{"subject": "string", "body": "string", "send_day": 0}},
  {{"subject": "string", "body": "string", "send_day": 3}},
  {{"subject": "string", "body": "string", "send_day": 7}}
]"""


def write_email_sequence(lead: Dict[str, Any], details: Dict[str, Any]) -> list:
    """Generate 3-email sequence for a lead."""
    business_name = lead.get("business_name", "Unknown")
    
    prompt = EMAIL_WRITING_PROMPT.format(
        business_name=business_name,
        category=lead.get("category", "Service"),
        city=lead.get("city", "your city"),
        state=lead.get("state", ""),
        google_rating=lead.get("google_rating", 0),
        review_count=lead.get("review_count", 0),
        website=lead.get("website", "None"),
        services=details.get("services", "not found"),
        usp=details.get("usp", "not found"),
        pain_points=details.get("pain_points", "not found"),
        personalization_hook=details.get("personalization_hook", "")
    )
    
    try:
        message = claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        emails = json.loads(response_text)
        
        # Validate
        if not isinstance(emails, list) or len(emails) != 3:
            logger.error(f"  ❌ Invalid response structure for {business_name}")
            return None
        
        for email in emails:
            if len(email.get("body", "")) > 120:
                logger.warning(f"  ⚠️  Email too long for {business_name}, regenerating...")
                # Could trigger regenerate here
            if "!" in email.get("subject", ""):
                email["subject"] = email["subject"].replace("!", "")
        
        return emails
    
    except json.JSONDecodeError:
        logger.error(f"  ❌ Invalid JSON for {business_name}")
        return None
    
    except Exception as e:
        logger.error(f"  ❌ Error writing emails for {business_name}: {e}")
        return None


def write_sequences(client_id: str, day_14_only: bool = True) -> dict:
    """Write email sequences for all analyzed leads."""
    logger.info(f"✍️  Writing email sequences for client {client_id}")
    
    results = {"written": 0, "errors": 0, "skipped": 0}
    
    # Fetch analyzed leads
    try:
        response = supabase.table("leads").select("*").match(
            {"client_id": client_id, "status": "analyzed"}
        ).execute()
        leads = response.data
    except Exception as e:
        logger.error(f"❌ Could not fetch leads: {e}")
        return results
    
    logger.info(f"Found {len(leads)} analyzed leads")
    
    for lead in leads:
        # Fetch lead details
        try:
            details_response = supabase.table("lead_details").select("*").eq("lead_id", lead["id"]).single().execute()
            details = details_response.data
        except:
            logger.warning(f"  ⚠️  No details for {lead['business_name']}, using defaults")
            details = {
                "services": "not found",
                "usp": "not found",
                "pain_points": "not found",
                "personalization_hook": f"I came across {lead['business_name']} and noticed..."
            }
        
        # Write sequences
        emails = write_email_sequence(lead, details)
        
        if not emails:
            results["errors"] += 1
            continue
        
        # Store emails
        try:
            for email in emails:
                email_data = {
                    "lead_id": lead["id"],
                    "client_id": client_id,
                    "subject": email["subject"],
                    "body": email["body"],
                    "send_day": email["send_day"],
                    "status": "pending_review" if day_14_only else "approved",
                    "created_date": datetime.now().isoformat()
                }
                supabase.table("email_sequences").insert(email_data).execute()
            
            # Update lead status
            supabase.table("leads").update({"status": "pending_send"}).eq("id", lead["id"]).execute()
            
            results["written"] += 1
            logger.debug(f"  ✅ Wrote 3 emails for {lead['business_name']}")
        
        except Exception as e:
            logger.error(f"  ❌ Database error for {lead['business_name']}: {e}")
            results["errors"] += 1
    
    logger.info(f"✅ Writing complete: {results['written']} sequences, {results['errors']} errors, {results['skipped']} skipped")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Write email sequences")
    parser.add_argument("--client-id", required=True, help="Client ID")
    parser.add_argument("--no-review", action="store_true", help="Skip pending_review (go straight to approved)")
    args = parser.parse_args()
    
    result = write_sequences(args.client_id, day_14_only=not args.no_review)
    print(json.dumps(result, indent=2))
