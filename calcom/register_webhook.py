#!/usr/bin/env python3
"""
REGISTER CAL.COM WEBHOOK
Create webhook subscription for booking events.
Run: python calcom/register_webhook.py
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CALCOM_API_KEY = os.getenv("CALCOM_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not CALCOM_API_KEY:
    print("❌ CALCOM_API_KEY not found in .env")
    exit(1)

if not WEBHOOK_URL:
    print("❌ WEBHOOK_URL not found in .env")
    print("Set WEBHOOK_URL to your deployed webhook server URL")
    print("Example: WEBHOOK_URL=https://your-webhook-server.com/webhooks/calcom")
    exit(1)

API_URL = "https://api.cal.com/v1"

def get_api_url(endpoint):
    """Add API key to URL."""
    separator = "&" if "?" in endpoint else "?"
    return f"{API_URL}{endpoint}{separator}apiKey={CALCOM_API_KEY}"

def list_webhooks():
    """List existing webhooks."""
    print("\n📋 Listing existing webhooks...\n")
    
    try:
        response = requests.get(get_api_url("/webhooks"), headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        data = response.json()
        webhooks = data.get("webhooks", [])
        
        if not webhooks:
            print("No webhooks found.\n")
            return []
        
        print(f"✅ Found {len(webhooks)} webhook(s):\n")
        
        for webhook in webhooks:
            print(f"  ID: {webhook.get('id')}")
            print(f"  URL: {webhook.get('subscriberUrl')}")
            print(f"  Events: {webhook.get('eventTriggers')}")
            print(f"  Active: {webhook.get('active')}")
            print()
        
        return webhooks
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listing webhooks: {e}\n")
        return []

def create_webhook():
    """Create new webhook subscription."""
    
    print(f"\n📝 Creating webhook...\n")
    print(f"  URL: {WEBHOOK_URL}")
    print(f"  Events: BOOKING_CREATED, BOOKING_RESCHEDULED, BOOKING_CANCELLED\n")
    
    payload = {
        "subscriberUrl": WEBHOOK_URL,
        "eventTriggers": [
            "BOOKING_CREATED",
            "BOOKING_RESCHEDULED", 
            "BOOKING_CANCELLED"
        ],
        "active": True
    }
    
    try:
        response = requests.post(
            get_api_url("/webhooks"),
            headers={"Content-Type": "application/json"},
            json=payload
        )
        response.raise_for_status()
        
        webhook = response.json()
        
        webhook_id = webhook.get("webhook", {}).get("id") or webhook.get("id")
        
        print(f"✅ Webhook created successfully!\n")
        print(f"  ID: {webhook_id}")
        print(f"  URL: {WEBHOOK_URL}")
        print(f"  Events: BOOKING_CREATED, BOOKING_RESCHEDULED, BOOKING_CANCELLED")
        print(f"  Active: True\n")
        
        # Save webhook config
        with open("calcom/webhook.json", "w") as f:
            json.dump({
                "id": webhook_id,
                "url": WEBHOOK_URL,
                "events": ["BOOKING_CREATED", "BOOKING_RESCHEDULED", "BOOKING_CANCELLED"],
                "created_at": str(__import__("datetime").datetime.now())
            }, f, indent=2)
        
        print("✅ Webhook config saved to calcom/webhook.json\n")
        
        return webhook
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating webhook: {e}\n")
        return None

if __name__ == "__main__":
    print("=" * 60)
    print("CAL.COM WEBHOOK REGISTRATION")
    print("=" * 60)
    
    # List existing
    existing = list_webhooks()
    
    # Check if already registered
    for webhook in existing:
        if webhook.get("subscriberUrl") == WEBHOOK_URL:
            print(f"✅ Webhook already registered for {WEBHOOK_URL}\n")
            exit(0)
    
    # Create new
    webhook = create_webhook()
    
    if webhook:
        print("=" * 60)
        print("NEXT STEPS")
        print("=" * 60)
        print("\n1. Deploy your webhook server:")
        print("   - Vercel: vercel deploy webhook/")
        print("   - Render: render deploy")
        print("   - Railway: railway up")
        print("\n2. Update WEBHOOK_URL in .env with your deployed URL")
        print("\n3. Re-run this script to register the new webhook")
        print("\n4. Test by creating a booking at https://cal.com/astria/15min")
        print("   You should see the webhook fire in your server logs\n")
    else:
        print("❌ Failed to create webhook. Check your API key and try again.\n")
