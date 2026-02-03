#!/usr/bin/env python3
"""
CAL.COM INTEGRATION
Set up Cal.com event types and get booking links.
Run: python calcom/setup_integration.py
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CAL_API_KEY = os.getenv("CALCOM_API_KEY")

if not CAL_API_KEY:
    print("❌ CALCOM_API_KEY not found in .env")
    print("Get it from: https://app.cal.com/settings/developer/api")
    exit(1)

API_URL = "https://api.cal.com/v1"
HEADERS = {
    "Content-Type": "application/json"
}

def get_api_url(endpoint):
    """Add API key to URL."""
    separator = "&" if "?" in endpoint else "?"
    return f"{API_URL}{endpoint}{separator}apiKey={CAL_API_KEY}"

def get_event_types(username):
    """Fetch all event types."""
    print("🔍 Fetching event types from Cal.com...\n")
    
    try:
        response = requests.get(get_api_url("/event-types"), headers=HEADERS)
        response.raise_for_status()
        
        data = response.json()
        events = data.get("event_types", [])
        
        if not events:
            print("No event types found. Create one in Cal.com dashboard:")
            print("https://app.cal.com/event-types\n")
            return None
        
        print(f"✅ Found {len(events)} event type(s)\n")
        
        for event in events:
            print(f"📅 {event.get('title', 'Untitled')}")
            print(f"   ID: {event.get('id')}")
            print(f"   Slug: {event.get('slug')}")
            print(f"   URL: https://cal.com/{username}/{event.get('slug')}")
            print(f"   Length: {event.get('length')} minutes")
            print()
        
        return events
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching event types: {e}")
        return None

def get_user_profile():
    """Get Cal.com user profile."""
    print("👤 Fetching user profile...\n")
    
    try:
        response = requests.get(get_api_url("/me"), headers=HEADERS)
        response.raise_for_status()
        
        data = response.json()
        user = data.get("user", {})
        
        print(f"✅ User: {user.get('name')}")
        print(f"   Email: {user.get('email')}")
        print(f"   Username: {user.get('username')}")
        print(f"   Timezone: {user.get('timeZone')}")
        print()
        
        return user
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching profile: {e}")
        return None

def generate_config(user, events):
    """Generate configuration for website."""
    
    config = {
        "api_key": CAL_API_KEY[:20] + "...",  # Don't expose full key
        "user": {
            "name": user.get("name"),
            "email": user.get("email"),
            "username": user.get("username"),
            "timezone": user.get("timeZone")
        },
        "events": []
    }
    
    for event in events:
        config["events"].append({
            "id": event.get("id"),
            "title": event.get("title"),
            "slug": event.get("slug"),
            "url": f"https://cal.com/{user.get('username')}/{event.get('slug')}",
            "description": event.get("description"),
            "length": event.get("length")  # in minutes
        })
    
    # Save config
    with open("calcom/config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration saved to calcom/config.json\n")
    
    return config

if __name__ == "__main__":
    print("=" * 60)
    print("CAL.COM INTEGRATION")
    print("=" * 60 + "\n")
    
    # Fetch user profile
    user = get_user_profile()
    
    if not user:
        print("❌ Could not fetch user profile. Check your API key.")
        exit(1)
    
    # Fetch event types
    events = get_event_types(user.get("username"))
    
    if not events:
        print("❌ No event types found.")
        exit(1)
    
    # Generate config
    config = generate_config(user, events)
    
    print("=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print("\nYour Cal.com booking links:")
    for event in config["events"]:
        print(f"  {event['title']}: {event['url']}")
    print("\nUpdate website with these URLs in:")
    print("  - website/script.js (checkout function)")
    print("  - website/script-modern.js (checkout function)")
    print("  - website/index.html (CTA buttons)")
    print("  - website/index-modern.html (CTA buttons)")
    print()
