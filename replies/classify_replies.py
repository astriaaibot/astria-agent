#!/usr/bin/env python3
"""
ASTRIA REPLY CLASSIFIER
Classifies incoming email replies and takes action.
Run: python replies/classify_replies.py --reply-id <id>
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

CLASSIFICATION_PROMPT = """You are the reply handler for Astria, an AI sales agent. A prospect has replied to a cold outreach email. Classify this reply and decide what to do.

ORIGINAL EMAIL SENT:
Subject: {original_subject}
Body: {original_body}

PROSPECT REPLY:
{reply_text}

PROSPECT INFO:
Business: {business_name}
Category: {category}
Location: {city}

Classify this reply into exactly ONE category:

INTERESTED — They want to learn more, see a demo, or talk. They might say: "Tell me more," "How does this work," "What's the cost," "Sure, let's chat," "Send me info."

QUESTION — They have a specific question but haven't said yes or no. They might ask about pricing, how it works, case studies, or your company.

OBJECTION — They push back but haven't said a hard no. They might say: "We already have a marketing company," "We're too busy right now," "We tried something like this before," "Sounds too good to be true."

NOT_INTERESTED — Clear rejection. They say: "Not interested," "Remove me," "Stop emailing," "No thanks," "Don't contact me again."

OUT_OF_OFFICE — Auto-reply indicating they're away. Contains phrases like "out of office," "on vacation," "limited access to email," "will return on [date]."

For your draft response:
- If INTERESTED: Express enthusiasm briefly, send the Cal.com booking link, keep it under 50 words
- If QUESTION: Answer their specific question honestly and concisely, then suggest a quick call to discuss further
- If OBJECTION: Acknowledge their concern respectfully, address it briefly with ONE sentence, ask ONE follow-up question
- If NOT_INTERESTED: Thank them for their time, confirm they're removed, wish them well. Under 30 words.
- If OUT_OF_OFFICE: Do not draft a response. Just log it.

Return ONLY valid JSON:
{{
  "category": "interested" | "question" | "objection" | "not_interested" | "out_of_office",
  "confidence": 0.0 to 1.0,
  "draft_response": "your drafted reply text or null",
  "action": "send_booking_link" | "answer_and_follow_up" | "address_objection" | "stop_sequence" | "pause_and_retry",
  "escalate_to_human": true or false,
  "reasoning": "one sentence explaining your classification"
}}"""


def classify_reply(
    reply_text: str,
    original_subject: str,
    original_body: str,
    business_name: str,
    category: str,
    city: str
) -> Dict[str, Any]:
    """Classify a single reply."""
    
    prompt = CLASSIFICATION_PROMPT.format(
        original_subject=original_subject,
        original_body=original_body,
        reply_text=reply_text,
        business_name=business_name,
        category=category,
        city=city
    )
    
    try:
        message = claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        classification = json.loads(response_text)
        
        return classification
    
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON response for {business_name}")
        return None
    
    except Exception as e:
        logger.error(f"Error classifying reply from {business_name}: {e}")
        return None


def process_reply(reply_id: str) -> dict:
    """Process a single reply from database."""
    
    # Fetch reply
    try:
        reply_response = supabase.table("replies").select("*").eq("id", reply_id).single().execute()
        reply = reply_response.data
    except Exception as e:
        logger.error(f"❌ Could not fetch reply {reply_id}: {e}")
        return {"success": False}
    
    lead_id = reply["lead_id"]
    client_id = reply["client_id"]
    reply_text = reply["reply_text"]
    
    # Fetch lead
    try:
        lead_response = supabase.table("leads").select("*").eq("id", lead_id).single().execute()
        lead = lead_response.data
    except:
        logger.error(f"❌ Could not fetch lead {lead_id}")
        return {"success": False}
    
    # Fetch original email
    try:
        email_response = supabase.table("email_sequences").select("*").eq("id", reply["email_id"]).single().execute()
        email = email_response.data
    except:
        email = {"subject": "Unknown", "body": ""}
    
    # Classify
    classification = classify_reply(
        reply_text=reply_text,
        original_subject=email.get("subject", ""),
        original_body=email.get("body", ""),
        business_name=lead.get("business_name", ""),
        category=lead.get("category", ""),
        city=lead.get("city", "")
    )
    
    if not classification:
        logger.error(f"❌ Classification failed for {lead['business_name']}")
        return {"success": False}
    
    # Check escalation triggers
    escalate = classification.get("escalate_to_human", False)
    if not escalate:
        if classification.get("confidence", 1.0) < 0.7:
            escalate = True
        elif any(word in reply_text.lower() for word in ["lawyer", "legal", "sue", "attorney", "cease"]):
            escalate = True
    
    # Update reply record
    try:
        supabase.table("replies").update({
            "classification": classification["category"],
            "confidence": classification["confidence"],
            "draft_response": classification.get("draft_response"),
            "action": classification["action"],
            "escalate_to_human": escalate
        }).eq("id", reply_id).execute()
    except Exception as e:
        logger.error(f"Error updating reply: {e}")
        return {"success": False}
    
    # Take action based on classification
    action = classification["action"]
    
    if action == "send_booking_link":
        # Create opportunity
        try:
            supabase.table("opportunities").insert({
                "lead_id": lead_id,
                "client_id": client_id,
                "first_interested_date": datetime.now().isoformat(),
                "booking_link_sent_date": datetime.now().isoformat()
            }).execute()
            
            supabase.table("leads").update({"status": "opportunity"}).eq("id", lead_id).execute()
            
            logger.info(f"✅ Opportunity created for {lead['business_name']}")
        except Exception as e:
            logger.error(f"Error creating opportunity: {e}")
    
    elif action == "stop_sequence":
        # Update lead status
        try:
            supabase.table("leads").update({"status": "opted_out"}).eq("id", lead_id).execute()
            logger.info(f"✓ {lead['business_name']} opted out")
        except:
            pass
    
    elif action in ["answer_and_follow_up", "address_objection"]:
        try:
            supabase.table("leads").update({"status": "engaged"}).eq("id", lead_id).execute()
            logger.info(f"✓ {lead['business_name']} engaged")
        except:
            pass
    
    return {
        "success": True,
        "classification": classification["category"],
        "action": action,
        "escalate": escalate,
        "business": lead["business_name"]
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Classify replies")
    parser.add_argument("--reply-id", required=True, help="Reply ID")
    args = parser.parse_args()
    
    result = process_reply(args.reply_id)
    print(json.dumps(result, indent=2))
