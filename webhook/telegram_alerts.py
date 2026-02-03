#!/usr/bin/env python3
"""
TELEGRAM ALERTS
Send instant notifications when demos are booked.
"""

import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_alert(message: str, html=True) -> bool:
    """
    Send Telegram alert to user.
    
    Args:
        message: Text to send
        html: Use HTML formatting (bold, links, etc.)
    
    Returns:
        True if sent successfully, False otherwise
    """
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("⚠️  Telegram not configured. Skipping alert.")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML" if html else "Markdown"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"✅ Telegram alert sent")
        return True
    
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to send Telegram alert: {e}")
        return False


def demo_booked(name: str, email: str, time: str):
    """Alert when demo is booked."""
    
    message = f"""🎯 <b>DEMO BOOKED!</b>

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>Time:</b> {time}

<b>ACTION:</b> Prepare to close them!
Answer: What's their business type?
"""
    
    return send_alert(message)


def demo_scored_hot(name: str, email: str, score: float, reason: str):
    """Alert when prospect is hot after demo."""
    
    message = f"""🔥 <b>HOT PROSPECT - READY TO CLOSE!</b>

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>Score:</b> {score}/10

<b>Why hot:</b> {reason}

<b>NEXT STEP:</b> Call or email them TODAY!
Say: "Ready to get started?"
"""
    
    return send_alert(message)


def demo_scored_warm(name: str, email: str, score: float, reason: str):
    """Alert when prospect is warm after demo."""
    
    message = f"""⚡ <b>WARM PROSPECT - FOLLOW UP IN 2 DAYS</b>

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>Score:</b> {score}/10

<b>Why warm:</b> {reason}

<b>ACTION:</b> Schedule sales call in 2 days
"""
    
    return send_alert(message)


def demo_scored_cold(name: str, email: str, score: float, reason: str):
    """Alert when prospect is cold after demo."""
    
    message = f"""❄️ <b>COLD PROSPECT - NURTURE SEQUENCE</b>

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>Score:</b> {score}/10

<b>Why cold:</b> {reason}

<b>ACTION:</b> Auto-nurture email sent
Follow up in 1 week
"""
    
    return send_alert(message)


def appointment_booked(name: str, email: str, date: str, time: str):
    """Alert when appointment is booked."""
    
    message = f"""📅 <b>APPOINTMENT BOOKED!</b>

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>When:</b> {date} at {time}

<b>Prepare:</b> 
- Review their business
- Have pricing ready
- Plan close strategy
"""
    
    return send_alert(message)


def test_connection():
    """Test Telegram connection."""
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Telegram not configured")
        print("\nTo set up:")
        print("1. Message @BotFather on Telegram")
        print("2. Type /newbot")
        print("3. Follow steps to create bot")
        print("4. Copy token to TELEGRAM_BOT_TOKEN in .env")
        print("\n5. Message @userinfobot on Telegram")
        print("6. Copy your user ID to TELEGRAM_CHAT_ID in .env")
        return False
    
    message = "✅ Astria webhook connected! I'll send alerts here."
    result = send_alert(message)
    
    if result:
        print("✅ Telegram connection working!")
    else:
        print("❌ Telegram connection failed")
    
    return result


if __name__ == "__main__":
    test_connection()
