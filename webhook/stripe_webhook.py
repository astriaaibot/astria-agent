#!/usr/bin/env python3
"""
Stripe Webhook Handler for Astria
Listens to checkout.session.completed events and:
1. Creates client record in Supabase
2. Sends Telegram notification
3. Triggers initial pipeline setup
"""

import os
import json
import stripe
import requests
from flask import Flask, request
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

# Initialize Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Initialize Supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Telegram config
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_notification(message: str) -> bool:
    """Send notification to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️  Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Telegram notification failed: {e}")
        return False

def create_client_from_checkout(session_id: str, session_data: dict) -> dict:
    """Create client record from Stripe checkout session"""
    try:
        # Fetch full session with line items
        session = stripe.checkout.Session.retrieve(
            session_id,
            expand=["line_items", "customer"]
        )
        
        # Extract product info
        line_items = session.line_items.data
        product_id = line_items[0].price.product if line_items else None
        
        # Get product to determine plan tier
        plan_tier = "starter"
        if product_id:
            product = stripe.Product.retrieve(product_id)
            plan_name = product.name.lower()
            if "enterprise" in plan_name:
                plan_tier = "enterprise"
            elif "standard" in plan_name:
                plan_tier = "standard"
        
        # Extract customer info
        customer_email = session.customer_details.email if session.customer_details else None
        customer_name = session.customer_details.name if session.customer_details else "Unknown"
        
        # Create client record
        client_data = {
            "business_name": customer_name,
            "email": customer_email,
            "plan": plan_tier,
            "stripe_customer_id": session.customer,
            "stripe_session_id": session_id,
            "status": "active",
            "onboarded": False,
            "created_at": "now()"
        }
        
        response = supabase.table("clients").insert(client_data).execute()
        created_client = response.data[0] if response.data else None
        
        return {
            "success": True,
            "client_id": created_client.get("id") if created_client else None,
            "email": customer_email,
            "name": customer_name,
            "plan": plan_tier,
            "message": f"✅ New {plan_tier.title()} client: {customer_name} ({customer_email})"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Failed to create client: {str(e)}"
        }

@app.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """Handle Stripe webhook events"""
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(f"❌ Invalid payload: {e}")
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        print(f"❌ Invalid signature: {e}")
        return "Invalid signature", 400
    
    # Handle checkout.session.completed
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session["id"]
        
        print(f"\n🔔 Checkout completed: {session_id}")
        
        # Create client record
        result = create_client_from_checkout(session_id, session)
        print(result["message"])
        
        # Send Telegram notification
        if result["success"]:
            telegram_msg = (
                f"<b>🎉 New Astria Client!</b>\n\n"
                f"<b>Name:</b> {result['name']}\n"
                f"<b>Email:</b> {result['email']}\n"
                f"<b>Plan:</b> {result['plan'].title()}\n"
                f"<b>Client ID:</b> {result['client_id']}\n\n"
                f"✨ Ready to onboard!"
            )
            send_telegram_notification(telegram_msg)
            
            # Log to activities_log
            try:
                supabase.table("activities_log").insert({
                    "client_id": result["client_id"],
                    "activity_type": "client_created",
                    "description": f"New {result['plan']} client onboarded via Stripe",
                    "metadata": {"stripe_session_id": session_id}
                }).execute()
            except Exception as e:
                print(f"⚠️  Failed to log activity: {e}")
        else:
            send_telegram_notification(f"❌ Webhook error: {result['message']}")
        
        return "OK", 200
    
    # Acknowledge other event types
    print(f"⚠️  Unhandled event type: {event['type']}")
    return "OK", 200

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "astria-stripe-webhook"}, 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"\n🚀 Stripe webhook server running on port {port}")
    print(f"📍 Webhook endpoint: http://localhost:{port}/webhook/stripe")
    app.run(host="0.0.0.0", port=port, debug=False)
