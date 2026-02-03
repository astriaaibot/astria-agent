#!/usr/bin/env python3
"""
ASTRIA WEBSITE ANALYZER
Fetches websites and extracts personalization hooks.
Run: python analysis/analyze_websites.py --client-id <id>
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from typing import Dict, Any

try:
    import anthropic
    from supabase import create_client, Client
    from dotenv import load_dotenv
except ImportError as e:
    print(f"⚠️  Missing dependency: {e}")
    print("Install with: pip install anthropic supabase python-dotenv requests")
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

ANALYSIS_PROMPT = """You are analyzing a local business website to find personalization details for a sales email.

BUSINESS: {business_name}
CATEGORY: {category}
WEBSITE TEXT:
{extracted_text}

Extract the following. If you can't find something, say "not found":

1. SERVICES: What specific services do they offer? List them.
2. SERVICE_AREA: What geographic area do they serve?
3. UNIQUE_SELLING_POINT: What makes them different? (family-owned, years in business, guarantees, certifications)
4. TEAM: Any names of owners or team members mentioned?
5. PAIN_POINTS: What problems might they have based on their website?
   - Is the website outdated or modern?
   - Is there online booking?
   - Are there testimonials?
   - Is there a blog or content?
   - Are social media links present?
6. PERSONALIZATION_HOOK: Write ONE specific observation about their business that could be used to open a cold email. Make it genuine and specific, not generic.

Return ONLY valid JSON:
{{
  "services": "string",
  "service_area": "string",
  "usp": "string",
  "team": "string",
  "pain_points": "string",
  "personalization_hook": "string"
}}"""


def fetch_website(url: str, timeout: int = 30) -> str:
    """Fetch website content and extract text."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Extract text (simple approach — remove HTML tags)
        from html.parser import HTMLParser
        
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
            
            def handle_data(self, data):
                text = data.strip()
                if text and len(text) > 2:
                    self.text.append(text)
        
        extractor = TextExtractor()
        extractor.feed(response.text)
        extracted = ' '.join(extractor.text)[:3000]  # First 3000 chars
        
        return extracted
    
    except requests.Timeout:
        logger.warning(f"  ⏱️  Timeout fetching {url}")
        return ""
    except requests.RequestException as e:
        logger.warning(f"  ⚠️  Could not fetch {url}: {e}")
        return ""


def analyze_lead(lead: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze a single lead's website."""
    lead_id = lead["id"]
    business_name = lead.get("business_name", "Unknown")
    website = lead.get("website")
    
    if not website:
        # Fallback hook if no website
        city = lead.get("city", "your area")
        return {
            "services": "not found",
            "service_area": city,
            "usp": "not found",
            "team": "not found",
            "pain_points": "No website listed on Google Maps",
            "personalization_hook": f"I noticed {business_name} doesn't have a website listed on Google — that's actually a huge opportunity because most of your competitors are getting found online."
        }
    
    try:
        # Fetch website
        text = fetch_website(website)
        if not text:
            # Fallback if fetch failed
            return {
                "services": "not found",
                "service_area": lead.get("city", "unknown"),
                "usp": "not found",
                "team": "not found",
                "pain_points": "Website not accessible",
                "personalization_hook": f"I came across {business_name} while researching {lead.get('category', 'service')} companies in {lead.get('city')} and noticed you have {lead.get('review_count', 0)} reviews at {lead.get('google_rating', 0)} stars."
            }
        
        # Analyze with Claude
        prompt = ANALYSIS_PROMPT.format(
            business_name=business_name,
            category=lead.get("category", "Service"),
            extracted_text=text
        )
        
        message = claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text.strip()
        analysis = json.loads(response_text)
        
        return analysis
    
    except json.JSONDecodeError:
        logger.error(f"  ❌ Invalid JSON for {business_name}")
        return None
    
    except Exception as e:
        logger.error(f"  ❌ Error analyzing {business_name}: {e}")
        return None


def analyze_websites(client_id: str) -> dict:
    """Analyze all qualified leads with websites."""
    logger.info(f"🔍 Analyzing websites for client {client_id}")
    
    results = {"analyzed": 0, "skipped": 0, "errors": 0}
    
    # Fetch qualified leads
    try:
        response = supabase.table("leads").select("*").match(
            {"client_id": client_id, "status": "qualified"}
        ).execute()
        leads = response.data
    except Exception as e:
        logger.error(f"❌ Could not fetch leads: {e}")
        return results
    
    logger.info(f"Found {len(leads)} qualified leads")
    
    for lead in leads:
        if not lead.get("website"):
            # Fallback hook for no-website leads
            analysis = analyze_lead(lead)
            results["skipped"] += 1
        else:
            analysis = analyze_lead(lead)
        
        if not analysis:
            results["errors"] += 1
            continue
        
        try:
            # Create or update lead_details
            detail = {
                "lead_id": lead["id"],
                "services": analysis.get("services"),
                "service_area": analysis.get("service_area"),
                "usp": analysis.get("usp"),
                "team": analysis.get("team"),
                "pain_points": analysis.get("pain_points"),
                "personalization_hook": analysis.get("personalization_hook")
            }
            
            # Check if exists
            existing = supabase.table("lead_details").select("id").eq("lead_id", lead["id"]).execute()
            
            if existing.data:
                supabase.table("lead_details").update(detail).eq("lead_id", lead["id"]).execute()
            else:
                supabase.table("lead_details").insert(detail).execute()
            
            # Update lead status
            supabase.table("leads").update({"status": "analyzed"}).eq("id", lead["id"]).execute()
            
            results["analyzed"] += 1
            logger.debug(f"  ✅ Analyzed {lead['business_name']}")
        
        except Exception as e:
            logger.error(f"  ❌ Database error for {lead['business_name']}: {e}")
            results["errors"] += 1
    
    logger.info(f"✅ Analysis complete: {results['analyzed']} analyzed, {results['skipped']} skipped, {results['errors']} errors")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Analyze websites for leads")
    parser.add_argument("--client-id", required=True, help="Client ID")
    args = parser.parse_args()
    
    result = analyze_websites(args.client_id)
    print(json.dumps(result, indent=2))
