#!/usr/bin/env python3
"""
ASTRIA LEAD SCRAPER
Finds local service businesses from Google Maps.
Run: python scraper/scrape_leads.py --client-id <id>
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import List, Dict, Any

# You'll install these later
# pip install google-maps-scraper supabase python-dotenv

try:
    from google_maps_scraper import scrape_places
    from supabase import create_client, Client
    from dotenv import load_dotenv
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Install with: pip install google-maps-scraper supabase python-dotenv")
    sys.exit(1)

# Load .env
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.error("❌ Missing SUPABASE_URL or SUPABASE_ANON_KEY in .env")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def scrape_leads(client_id: str, queries: List[str]) -> Dict[str, Any]:
    """
    Scrape Google Maps for leads matching given queries.
    
    Args:
        client_id: Unique client ID from database
        queries: List of search queries (e.g., "HVAC repair Fort Lauderdale")
    
    Returns:
        {"success": int, "duplicates": int, "errors": int, "details": [...]}
    """
    logger.info(f"🔍 Starting scrape for client {client_id}")
    
    results = {
        "success": 0,
        "duplicates": 0,
        "errors": 0,
        "leads": []
    }
    
    # Get existing leads for deduplication
    existing_place_ids = set()
    existing_phones = set()
    existing_combos = set()
    
    try:
        response = supabase.table("leads").select("place_id, phone, business_name, city").match({"client_id": client_id}).execute()
        for lead in response.data:
            if lead.get("place_id"):
                existing_place_ids.add(lead["place_id"])
            if lead.get("phone"):
                existing_phones.add(lead["phone"])
            if lead.get("business_name") and lead.get("city"):
                existing_combos.add(f"{lead['business_name']}_{lead['city']}")
    except Exception as e:
        logger.warning(f"⚠️  Could not fetch existing leads: {e}")
    
    # Scrape each query
    for query in queries:
        logger.info(f"  Scraping: {query}")
        try:
            places = scrape_places(query, reviews_limit=100, max_places=50)
            
            for place in places:
                # Extract fields
                name = place.get("title", "").strip()
                phone = place.get("phone", "").strip()
                website = place.get("website", "").strip()
                address = place.get("address", "").strip()
                rating = float(place.get("rating", 0)) if place.get("rating") else None
                review_count = int(place.get("review_count", 0)) if place.get("review_count") else 0
                place_id = place.get("place_id", "").strip()
                
                # Parse address
                city = state = zip_code = ""
                if address:
                    parts = address.split(",")
                    if len(parts) >= 2:
                        city = parts[-2].strip()
                    if len(parts) >= 3:
                        state = parts[-1].strip().split()[0]
                
                # Deduplication checks
                if place_id and place_id in existing_place_ids:
                    results["duplicates"] += 1
                    continue
                
                if phone and phone in existing_phones:
                    results["duplicates"] += 1
                    continue
                
                combo_key = f"{name}_{city}"
                if combo_key in existing_combos:
                    results["duplicates"] += 1
                    continue
                
                # Valid lead — prepare for insert
                lead_data = {
                    "client_id": client_id,
                    "business_name": name,
                    "phone": phone or None,
                    "email": None,  # Google Maps scraper doesn't get email
                    "website": website or None,
                    "address": address,
                    "city": city,
                    "state": state,
                    "zip": zip_code,
                    "google_rating": rating,
                    "review_count": review_count,
                    "category": None,  # Will be set by client ICP
                    "place_id": place_id,
                    "scraped_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "new"
                }
                
                results["leads"].append(lead_data)
                results["success"] += 1
        
        except Exception as e:
            logger.error(f"  ❌ Error scraping '{query}': {e}")
            results["errors"] += 1
            # Log error to database
            try:
                supabase.table("errors").insert({
                    "task_name": "SCRAPE",
                    "error_message": str(e),
                    "error_details": {"query": query},
                    "timestamp": datetime.now().isoformat()
                }).execute()
            except:
                pass
        
        # Rate limiting
        time.sleep(3)
    
    # Batch insert leads
    if results["leads"]:
        try:
            supabase.table("leads").insert(results["leads"]).execute()
            logger.info(f"✅ Inserted {len(results['leads'])} new leads")
        except Exception as e:
            logger.error(f"❌ Batch insert failed: {e}")
            results["errors"] += len(results["leads"])
            results["success"] = 0
    
    logger.info(f"📊 Scrape complete: {results['success']} new, {results['duplicates']} dupes, {results['errors']} errors")
    
    return results


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scrape leads from Google Maps")
    parser.add_argument("--client-id", required=True, help="Client ID")
    parser.add_argument("--queries", type=str, help="Comma-separated search queries (or will fetch from DB)")
    
    args = parser.parse_args()
    
    # Get client queries from database (if not provided)
    if args.queries:
        queries = [q.strip() for q in args.queries.split(",")]
    else:
        try:
            client = supabase.table("clients").select("*").eq("id", args.client_id).single().execute()
            queries = client.data.get("search_queries", [])
            if not queries:
                logger.error(f"❌ No search queries defined for client {args.client_id}")
                sys.exit(1)
        except Exception as e:
            logger.error(f"❌ Could not fetch client {args.client_id}: {e}")
            sys.exit(1)
    
    # Run scraper
    result = scrape_leads(args.client_id, queries)
    
    # Print summary
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
