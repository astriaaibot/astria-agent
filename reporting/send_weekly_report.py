#!/usr/bin/env python3
"""
ASTRIA WEEKLY REPORT GENERATOR
Creates and sends weekly performance reports.
Run: python reporting/send_weekly_report.py --client-id <id>
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta

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

REPORT_PROMPT = """You write weekly performance reports for Astria clients. The client is a local business owner who is NOT technical. They want to know: is this working? What happened this week? What's coming next?

CLIENT: {client_name}
CATEGORY: {category}
WEEK: {week_start} to {week_end}

THIS WEEK'S NUMBERS:
- New leads found: {leads_scraped}
- High-potential leads identified: {leads_hot_warm}
- Personalized emails sent: {emails_sent}
- Replies received: {replies_received}
- Businesses interested: {replies_interested}
- Appointments booked: {appointments_booked}
- Email open rate: {open_rate}%
- Reply rate: {reply_rate}%

Write a SHORT, friendly weekly email (under 200 words). Include:
1. A one-sentence summary of the week (positive framing, be honest)
2. The key numbers in a simple format (not a table — just natural sentences)
3. One specific thing happening next week
4. A closing line that reinforces value

Tone: Professional but warm. Like a trusted employee giving a quick weekly update. Not a marketing report. Not robotic.

Do NOT include:
- Technical jargon (no "open rates" — say "X% of people opened your emails")
- Negative framing (don't say "only 2 replies" — say "2 businesses expressed interest")
- Excuses or apologies
- Anything about AI, automation, or algorithms

Format: Plain text. Subject line on first line. Then two blank lines. Then body.

Start with "Subject: Weekly update: [number] new leads and [number] new appointments"

Return only the email text, no JSON."""


def generate_report(client_id: str) -> dict:
    """Generate weekly report for a client."""
    
    logger.info(f"📊 Generating report for client {client_id}")
    
    # Fetch client
    try:
        client_response = supabase.table("clients").select("*").eq("id", client_id).single().execute()
        client = client_response.data
    except Exception as e:
        logger.error(f"❌ Could not fetch client {client_id}: {e}")
        return {"success": False}
    
    # Calculate week dates
    today = datetime.now()
    week_start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    week_end = today.strftime("%Y-%m-%d")
    
    # Query metrics
    try:
        # Leads scraped
        leads_response = supabase.table("leads").select("*").match(
            {"client_id": client_id}
        ).gte("created_date", week_start).execute()
        leads_scraped = len(leads_response.data)
        
        # Hot/Warm leads
        hot_warm = sum(1 for lead in leads_response.data if lead.get("tier") in ["hot", "warm"])
        
        # Emails sent
        emails_response = supabase.table("email_sequences").select("*").match(
            {"client_id": client_id, "status": "sent"}
        ).gte("sent_date", week_start).execute()
        emails_sent = len(emails_response.data)
        
        # Replies
        replies_response = supabase.table("replies").select("*").match(
            {"client_id": client_id}
        ).gte("received_date", week_start).execute()
        replies_received = len(replies_response.data)
        replies_interested = sum(1 for reply in replies_response.data if reply.get("classification") == "interested")
        
        # Appointments
        appointments_response = supabase.table("opportunities").select("*").match(
            {"client_id": client_id, "appointment_booked": True}
        ).gte("created_date", week_start).execute()
        appointments_booked = len(appointments_response.data)
        
        # Calculate rates
        open_rate = round((len([e for e in emails_response.data if e.get("open_count", 0) > 0]) / max(emails_sent, 1)) * 100)
        reply_rate = round((replies_received / max(emails_sent, 1)) * 100)
    
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return {"success": False}
    
    # Generate report with Claude
    prompt = REPORT_PROMPT.format(
        client_name=client.get("business_name", "Friend"),
        category=client.get("category", "Service"),
        week_start=week_start,
        week_end=week_end,
        leads_scraped=leads_scraped,
        leads_hot_warm=hot_warm,
        emails_sent=emails_sent,
        replies_received=replies_received,
        replies_interested=replies_interested,
        appointments_booked=appointments_booked,
        open_rate=open_rate,
        reply_rate=reply_rate
    )
    
    try:
        message = claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        
        report_text = message.content[0].text.strip()
    
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return {"success": False}
    
    # Store report in database
    try:
        supabase.table("reports").insert({
            "client_id": client_id,
            "week_start": week_start,
            "week_end": week_end,
            "leads_scraped": leads_scraped,
            "leads_scored_hot": sum(1 for lead in leads_response.data if lead.get("tier") == "hot"),
            "leads_scored_warm": sum(1 for lead in leads_response.data if lead.get("tier") == "warm"),
            "emails_sent": emails_sent,
            "replies_received": replies_received,
            "replies_interested": replies_interested,
            "appointments_booked": appointments_booked,
            "open_rate": open_rate,
            "reply_rate": reply_rate,
            "report_text": report_text,
            "sent_date": datetime.now().isoformat()
        }).execute()
        
        logger.info(f"✅ Report generated: {leads_scraped} leads, {emails_sent} emails, {appointments_booked} appointments")
    
    except Exception as e:
        logger.error(f"Error storing report: {e}")
        return {"success": False}
    
    return {
        "success": True,
        "metrics": {
            "leads_scraped": leads_scraped,
            "emails_sent": emails_sent,
            "replies_received": replies_received,
            "appointments_booked": appointments_booked,
            "open_rate": f"{open_rate}%",
            "reply_rate": f"{reply_rate}%"
        },
        "report_preview": report_text[:200] + "..."
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate weekly report")
    parser.add_argument("--client-id", required=True, help="Client ID")
    args = parser.parse_args()
    
    result = generate_report(args.client_id)
    print(json.dumps(result, indent=2))
