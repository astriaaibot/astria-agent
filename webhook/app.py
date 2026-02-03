#!/usr/bin/env python3
"""
ASTRIA WEBHOOK SERVER
Listens for Cal.com bookings and updates Supabase.
Run: python webhook/app.py
Deploy: Vercel, Render, Railway, or your own server
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from supabase import create_client, Client

load_dotenv()

# Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("⚠️  Supabase keys not found. Webhooks will not save to database.")
    supabase = None
else:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Webhook secret (optional, for security)
WEBHOOK_SECRET = os.getenv("CALCOM_WEBHOOK_SECRET", "")

---

## ROUTES

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()}), 200


@app.route("/webhooks/calcom", methods=["POST"])
def calcom_webhook():
    """
    Cal.com webhook handler.
    Receives booking events and saves to Supabase.
    """
    
    logger.info(f"📨 Webhook received: {request.method}")
    
    try:
        # Get payload
        data = request.get_json()
        
        if not data:
            logger.error("No JSON payload")
            return jsonify({"error": "No payload"}), 400
        
        # Verify webhook secret (optional)
        if WEBHOOK_SECRET:
            signature = request.headers.get("X-Cal-Signature", "")
            if signature != WEBHOOK_SECRET:
                logger.error("Invalid webhook signature")
                return jsonify({"error": "Invalid signature"}), 401
        
        # Log event
        event_type = data.get("triggerEvent")
        logger.info(f"Event: {event_type}")
        
        # Handle booking.created event
        if event_type == "BOOKING_CREATED":
            return handle_booking_created(data)
        
        # Handle booking.rescheduled event
        elif event_type == "BOOKING_RESCHEDULED":
            return handle_booking_rescheduled(data)
        
        # Handle booking.cancelled event
        elif event_type == "BOOKING_CANCELLED":
            return handle_booking_cancelled(data)
        
        else:
            logger.info(f"Ignored event type: {event_type}")
            return jsonify({"status": "ignored"}), 200
    
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500


def handle_booking_created(data):
    """Handle BOOKING_CREATED event."""
    
    logger.info("🔔 Booking created")
    
    booking = data.get("payload", {})
    
    if not supabase:
        logger.warning("⚠️  Supabase not connected, skipping database update")
        return jsonify({"status": "received"}), 200
    
    try:
        # Extract booking details
        booking_id = booking.get("id")
        attendee_email = booking.get("attendees", [{}])[0].get("email")
        attendee_name = booking.get("attendees", [{}])[0].get("name")
        event_name = booking.get("eventName")
        start_time = booking.get("startTime")
        end_time = booking.get("endTime")
        timezone = booking.get("timezone")
        organizer = booking.get("organizer", {})
        
        logger.info(f"  Booking ID: {booking_id}")
        logger.info(f"  Attendee: {attendee_name} ({attendee_email})")
        logger.info(f"  Event: {event_name}")
        logger.info(f"  Time: {start_time} → {end_time}")
        
        # Check if lead already exists by email
        existing_lead = supabase.table("leads").select("id, client_id").eq("email", attendee_email).execute()
        
        if existing_lead.data:
            # Lead exists, update opportunity
            lead_id = existing_lead.data[0]["id"]
            client_id = existing_lead.data[0]["client_id"]
            
            logger.info(f"  Found existing lead: {lead_id}")
            
            # Create opportunity record
            opportunity = supabase.table("opportunities").insert({
                "lead_id": lead_id,
                "client_id": client_id,
                "first_interested_date": datetime.now().isoformat(),
                "booking_link_sent_date": datetime.now().isoformat(),
                "appointment_booked": True,
                "appointment_date": start_time.split("T")[0],  # Extract date
                "appointment_time": start_time.split("T")[1],  # Extract time
                "show_status": "scheduled",
                "notes": f"Booked via Cal.com: {event_name}"
            }).execute()
            
            # Update lead status
            supabase.table("leads").update({
                "status": "appointment_booked",
                "last_reply_date": datetime.now().isoformat()
            }).eq("id", lead_id).execute()
            
            logger.info(f"  ✅ Opportunity created for lead {lead_id}")
        
        else:
            # New lead (not from Astria campaign)
            logger.info(f"  New lead from Cal.com: {attendee_name}")
            
            # Create lead record
            lead = supabase.table("leads").insert({
                "client_id": None,  # Will be set manually
                "business_name": attendee_name,
                "email": attendee_email,
                "status": "appointment_booked",
                "created_date": datetime.now().isoformat()
            }).execute()
            
            if lead.data:
                lead_id = lead.data[0]["id"]
                logger.info(f"  ✅ Created new lead: {lead_id}")
        
        # Log activity
        supabase.table("activities_log").insert({
            "activity_type": "appointment_booked",
            "details": {
                "booking_id": booking_id,
                "attendee": attendee_name,
                "event": event_name,
                "time": start_time
            },
            "timestamp": datetime.now().isoformat()
        }).execute()
        
        logger.info("✅ Webhook processed successfully")
        return jsonify({"status": "processed", "booking_id": booking_id}), 200
    
    except Exception as e:
        logger.error(f"❌ Error processing booking: {e}")
        return jsonify({"error": str(e)}), 500


def handle_booking_rescheduled(data):
    """Handle BOOKING_RESCHEDULED event."""
    
    logger.info("📅 Booking rescheduled")
    
    booking = data.get("payload", {})
    booking_id = booking.get("id")
    start_time = booking.get("startTime")
    
    if not supabase:
        return jsonify({"status": "received"}), 200
    
    try:
        # Update opportunity
        supabase.table("opportunities").update({
            "appointment_date": start_time.split("T")[0],
            "appointment_time": start_time.split("T")[1],
            "show_status": "scheduled"
        }).eq("notes", f"Booked via Cal.com").execute()
        
        logger.info(f"✅ Rescheduled: {booking_id} → {start_time}")
        return jsonify({"status": "processed"}), 200
    
    except Exception as e:
        logger.error(f"❌ Error rescheduling: {e}")
        return jsonify({"error": str(e)}), 500


def handle_booking_cancelled(data):
    """Handle BOOKING_CANCELLED event."""
    
    logger.info("❌ Booking cancelled")
    
    booking = data.get("payload", {})
    booking_id = booking.get("id")
    
    if not supabase:
        return jsonify({"status": "received"}), 200
    
    try:
        # Update opportunity
        supabase.table("opportunities").update({
            "show_status": "cancelled"
        }).eq("notes", f"Booked via Cal.com").execute()
        
        logger.info(f"✅ Cancelled: {booking_id}")
        return jsonify({"status": "processed"}), 200
    
    except Exception as e:
        logger.error(f"❌ Error cancelling: {e}")
        return jsonify({"error": str(e)}), 500


# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 error: {e}")
    return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"🚀 Astria webhook server starting on port {port}")
    app.run(debug=True, port=port, host="0.0.0.0")
