#!/usr/bin/env python3
"""
ASTRIA LEAD SCORING
Scores leads 1-10 using Claude API.
Run: python scoring/score_leads.py --client-id <id>
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

# Initialize
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, CLAUDE_API_KEY]):
    logger.error("❌ Missing required .env variables")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
claude = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

SCORING_PROMPT = """You are a lead qualification expert for Astria, a B2B service that helps local businesses get more customers through AI-powered outreach.

Score this business 1–10 on likelihood to purchase a lead generation service at $500–$1,500/month.

BUSINESS DATA:
Name: {business_name}
Category: {category}
Rating: {google_rating} stars
Reviews: {review_count}
Website: {website}
Address: {address}

SCORING CRITERIA (weight each roughly equally):

1. REVIEW COUNT
   - 0–5 reviews = high need, score boost +2
   - 6–20 reviews = moderate need, score boost +1
   - 21–50 reviews = some need, neutral
   - 50+ reviews = lower need, score penalty -1

2. WEBSITE
   - No website listed = very high need, score boost +2
   - Has website = neutral (website quality checked separately)

3. GOOGLE RATING
   - Below 3.5 = may be struggling, score boost +1
   - 3.5–4.2 = normal range, neutral
   - 4.3–5.0 = doing well but can always grow, neutral

4. BUSINESS MATURITY
   - If review dates span 3+ years = established, has budget, score boost +1
   - If very new (under 1 year of reviews) = may not have budget, score penalty -1

5. CATEGORY FIT
   - Core service business (HVAC, plumbing, electrical, roofing) = strong fit, score boost +1
   - Adjacent (landscaping, pest control, cleaning) = decent fit, neutral
   - Poor fit (retail, restaurant, franchise) = bad fit, score penalty -2

6. ONLINE PRESENCE GAPS
   - No website + few reviews + low rating = maximum need, score boost +2
   - Strong website + many reviews + high rating = minimal need, score penalty -1

Return ONLY valid JSON, no other text:
{{"score": number, "tier": "Hot" or "Warm" or "Cold", "reasoning": "one sentence explaining why"}}"""


def score_leads(client_id: str) -> dict:
    """Score all leads with status 'new' for a client."""
    logger.info(f"📊 Scoring leads for client {client_id}")
    
    results = {"scored": 0, "hot": 0, "warm": 0, "cold": 0, "errors": 0}
    
    # Fetch new leads
    try:
        response = supabase.table("leads").select("*").match(
            {"client_id": client_id, "status": "new"}
        ).execute()
        leads = response.data
    except Exception as e:
        logger.error(f"❌ Could not fetch leads: {e}")
        return results
    
    logger.info(f"Found {len(leads)} new leads to score")
    
    for lead in leads:
        try:
            # Build prompt
            prompt = SCORING_PROMPT.format(
                business_name=lead.get("business_name", "Unknown"),
                category=lead.get("category", "Service"),
                google_rating=lead.get("google_rating", 0),
                review_count=lead.get("review_count", 0),
                website=lead.get("website", "None"),
                address=lead.get("address", "")
            )
            
            # Call Claude
            message = claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # Parse JSON
            score_data = json.loads(response_text)
            
            # Update lead
            new_status = "qualified" if score_data["tier"] in ["Hot", "Warm"] else "cold"
            
            update = {
                "status": new_status,
                "score": score_data["score"],
                "tier": score_data["tier"].lower(),
                "score_reasoning": score_data["reasoning"]
            }
            
            supabase.table("leads").update(update).eq("id", lead["id"]).execute()
            
            results["scored"] += 1
            if score_data["tier"] == "Hot":
                results["hot"] += 1
            elif score_data["tier"] == "Warm":
                results["warm"] += 1
            else:
                results["cold"] += 1
            
            logger.debug(f"  ✅ {lead['business_name']}: {score_data['score']} ({score_data['tier']})")
        
        except json.JSONDecodeError:
            logger.error(f"  ❌ Invalid JSON response for {lead['business_name']}")
            results["errors"] += 1
            # Log error
            try:
                supabase.table("errors").insert({
                    "task_name": "SCORE",
                    "error_message": "Invalid JSON from Claude",
                    "error_details": {"lead_id": lead["id"]},
                    "timestamp": datetime.now().isoformat()
                }).execute()
            except:
                pass
        
        except Exception as e:
            logger.error(f"  ❌ Error scoring {lead['business_name']}: {e}")
            results["errors"] += 1
    
    logger.info(f"✅ Scoring complete: {results['scored']} scored ({results['hot']} Hot, {results['warm']} Warm, {results['cold']} Cold), {results['errors']} errors")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Score leads with Claude")
    parser.add_argument("--client-id", required=True, help="Client ID")
    args = parser.parse_args()
    
    result = score_leads(args.client_id)
    print(json.dumps(result, indent=2))
