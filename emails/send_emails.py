#!/usr/bin/env python3
"""
ASTRIA EMAIL SENDER
Sends emails via Instantly.ai
Run: python emails/send_emails.py --client-id <id>
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any

try:
    from supabase import create_client, Client
    from dotenv import load_dotenv
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Install with: pip install supabase python-dotenv requests")
    sys.exit(1)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
INSTANTLY_API_KEY = os.getenv("INSTANTLY_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, INSTANTLY_API_KEY]):
    logger.error("❌ Missing required .env variables")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

INSTANTLY_API_URL = "https://api.instantly.ai/api/v1"
SENDING_ACCOUNTS = [
    os.getenv("SENDING_EMAIL_1", "account1@astriareach.com"),
    os.getenv("SENDING_EMAIL_2", "account2@astriareach.com"),
    os.getenv("SENDING_EMAIL_3", "account3@astriareach.com"),
]

# Track sends per account
send_count = {account: 0 for account in SENDING_ACCOUNTS}
current_account_index = 0

BUSINESS_ADDRESS = "Pelican Pointe LLC\nFort Lauderdale, FL 33301"


def get_next_account() -> str:
    """Rotate through sending accounts."""
    global current_account_index
    account = SENDING_ACCOUNTS[current_account_index % len(SENDING_ACCOUNTS)]
    current_account_index += 1
    return account


def send_via_instantly(
    email: str,
    subject: str,
    body: str,
    first_name: str,
    company: str,
    from_account: str,
    campaign_id: str = None
) -> Dict[str, Any]:
    """Send email via Instantly.ai"""
    
    # Add unsubscribe link and footer
    full_body = f"""{body}

---
Unsubscribe: https://instantly.ai/unsubscribe
{BUSINESS_ADDRESS}"""
    
    payload = {
        "api_key": INSTANTLY_API_KEY,
        "email": email,
        "first_name": first_name,
        "subject": subject,
        "body": full_body,
        "from": from_account,
        "company": company,
    }
    
    if campaign_id:
        payload["campaign_id"] = campaign_id
    
    try:
        response = requests.post(
            f"{INSTANTLY_API_URL}/campaign/email/add",
            json=payload,
            timeout=10
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("status") == "success":
            return {"success": True, "message_id": result.get("id")}
        else:
            return {"success": False, "error": result.get("error", "Unknown error")}
    
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_scheduled_emails(client_id: str) -> dict:
    """Send all emails scheduled for today."""
    logger.info(f"📧 Sending emails for client {client_id}")
    
    results = {
        "sent": 0,
        "failed": 0,
        "skipped": 0,
        "details": []
    }
    
    # Get today's day of week
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Fetch emails to send
    try:
        response = supabase.table("email_sequences").select("*").match(
            {"client_id": client_id, "status": "approved"}
        ).execute()
        emails = response.data
    except Exception as e:
        logger.error(f"❌ Could not fetch emails: {e}")
        return results
    
    logger.info(f"Found {len(emails)} approved emails")
    
    for email_record in emails:
        lead_id = email_record["lead_id"]
        send_day = email_record["send_day"]
        
        # Check if this email is scheduled for today
        # (Simplified: you'd calculate actual send date based on contact date)
        # For now, just send all approved emails
        
        # Fetch lead to get email + name
        try:
            lead_response = supabase.table("leads").select("*").eq("id", lead_id).single().execute()
            lead = lead_response.data
        except:
            logger.warning(f"  ⚠️  Could not fetch lead {lead_id}")
            results["skipped"] += 1
            continue
        
        lead_email = lead.get("email")
        business_name = lead.get("business_name", "Friend")
        
        if not lead_email:
            logger.warning(f"  ⚠️  No email for {business_name}, skipping")
            # Update status to no_email
            try:
                supabase.table("leads").update({"status": "no_email"}).eq("id", lead_id).execute()
            except:
                pass
            results["skipped"] += 1
            continue
        
        # Check if prospect already replied
        try:
            reply_check = supabase.table("replies").select("*").match(
                {"lead_id": lead_id}
            ).execute()
            if reply_check.data:
                logger.debug(f"  ✓ {business_name} already replied, skipping further emails")
                results["skipped"] += 1
                continue
        except:
            pass
        
        # Check if already contacted
        if lead.get("status") == "contacted" and email_record["send_day"] == 0:
            results["skipped"] += 1
            continue
        
        # Send email
        account = get_next_account()
        send_result = send_via_instantly(
            email=lead_email,
            subject=email_record["subject"],
            body=email_record["body"],
            first_name=business_name.split()[0],
            company=business_name,
            from_account=account,
            campaign_id=None
        )
        
        if send_result["success"]:
            # Update email record
            try:
                supabase.table("email_sequences").update({
                    "status": "sent",
                    "sent_date": datetime.now().isoformat(),
                    "sent_from_account": account
                }).eq("id", email_record["id"]).execute()
                
                # Update lead status if first email
                if email_record["send_day"] == 0:
                    supabase.table("leads").update({"status": "contacted"}).eq("id", lead_id).execute()
                
                results["sent"] += 1
                logger.debug(f"  ✅ Sent to {business_name} from {account}")
            except Exception as e:
                logger.error(f"  ❌ Database error for {business_name}: {e}")
                results["failed"] += 1
        
        else:
            logger.error(f"  ❌ Failed to send to {business_name}: {send_result['error']}")
            results["failed"] += 1
            results["details"].append({
                "lead": business_name,
                "error": send_result["error"]
            })
        
        # Rate limiting (3-7 seconds between sends)
        time.sleep(5)
    
    logger.info(f"✅ Sending complete: {results['sent']} sent, {results['failed']} failed, {results['skipped']} skipped")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Send emails")
    parser.add_argument("--client-id", required=True, help="Client ID")
    args = parser.parse_args()
    
    result = send_scheduled_emails(args.client_id)
    print(json.dumps(result, indent=2))
