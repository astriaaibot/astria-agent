#!/usr/bin/env python3
"""
DEMO SCORING
Score prospect hotness after demo call.
Used to flag who's ready for you to close.
"""

import json
from datetime import datetime

def score_prospect(data):
    """
    Score prospect based on demo interaction.
    
    Returns: {
        "score": 1-10,
        "tier": "hot" | "warm" | "cold",
        "recommendation": "action to take",
        "reasoning": "why this score"
    }
    """
    
    name = data.get("name", "Prospect")
    business = data.get("business", "")
    area = data.get("area", "")
    
    # Questions asked (higher = more interested)
    questions_about_pricing = data.get("asked_pricing", False)
    questions_about_timeline = data.get("asked_timeline", False)
    questions_about_leads = data.get("asked_leads", False)
    num_questions = sum([questions_about_pricing, questions_about_timeline, questions_about_leads])
    
    # Objections (how serious)
    objections = data.get("objections", [])
    has_budget_concern = any("budget" in o.lower() or "cost" in o.lower() for o in objections)
    has_skepticism = any("doubt" in o.lower() or "too good" in o.lower() for o in objections)
    
    # Intent signals
    wanted_pricing = data.get("wanted_pricing", False)
    wanted_to_start = data.get("wanted_to_start", False)
    wants_callback = data.get("wants_callback", False)
    
    # Calc score
    score = 5  # Base
    
    # Add for good signals
    if questions_about_pricing:
        score += 2
    if questions_about_timeline:
        score += 1.5
    if wanted_pricing:
        score += 2
    if wanted_to_start:
        score += 2
    if wants_callback:
        score += 1
    
    # Subtract for concerns
    if has_budget_concern and not wanted_to_start:
        score -= 1
    if has_skepticism:
        score -= 1
    
    # Cap
    score = min(10, max(1, score))
    
    # Tier
    if score >= 8:
        tier = "hot"
        recommendation = "🔥 CALL THEM TODAY - They're ready to buy"
    elif score >= 6:
        tier = "warm"
        recommendation = "📞 Follow up in 2 days - Schedule sales call"
    else:
        tier = "cold"
        recommendation = "📧 Send nurture email - Try again in 1 week"
    
    reasoning = f"Asked {num_questions} key questions, "
    if wanted_pricing:
        reasoning += "requested pricing, "
    if objections:
        reasoning += f"raised {len(objections)} objections, "
    if wanted_to_start:
        reasoning += "wants to start ASAP"
    else:
        reasoning = reasoning.rstrip(", ")
    
    return {
        "score": round(score, 1),
        "tier": tier,
        "recommendation": recommendation,
        "reasoning": reasoning,
        "timestamp": datetime.now().isoformat()
    }


def demo_call_template():
    """
    Return the demo call talking points.
    Use this during demo calls.
    """
    
    return {
        "intro": [
            "Hi [Name], thanks for booking! I'm Astria, an AI sales agent.",
            "For 15 minutes, I'll show you how I find customers for businesses like yours.",
            "After this, if you're interested, [YOUR_NAME] can help you get started.",
            "Sound good?"
        ],
        "pain_points": [
            "I know cold calling doesn't work anymore.",
            "Hiring a salesperson costs $3-5k/month and they might not deliver.",
            "You're probably juggling a lot—hard to find time to prospect.",
            "Does that sound about right for you?"
        ],
        "solution": [
            "I solve this by being YOUR salesperson.",
            "Every day, I:",
            "  1. Find 50+ qualified leads from Google Maps",
            "  2. Score them 1-10 based on likelihood to buy",
            "  3. Visit their website, learn what makes them unique",
            "  4. Write personalized emails (no templates)",
            "  5. Send them during business hours",
            "  6. Monitor every reply—interested, question, objection, or no",
            "  7. Book appointments directly on your calendar",
            "  8. Send you a weekly report",
            "Completely hands-off. You just close the deals."
        ],
        "proof": [
            "Here's what customers are seeing:",
            "  • 50+ new leads per month",
            "  • 2-4 qualified appointments per week",
            "  • 42% email open rate (industry avg: 20%)",
            "  • 4% reply rate (cold calling: <1%)",
            "And they're only paying $500-1,500/month."
        ],
        "question": [
            "Before I show you more: what's your ideal customer look like?",
            "And what area do you serve?"
        ],
        "pricing": [
            "We have 3 plans:",
            "  • Starter: $299/mo (30-50 leads, $99 setup)",
            "  • Standard: $699/mo (80-120 leads, $199 setup)",
            "  • Enterprise: $1,299/mo (200+ leads, $299 setup)",
            "Pick based on how many leads you want per month.",
            "No long-term contracts. Cancel anytime."
        ],
        "close": [
            "[If interested] [YOUR_NAME] will reach out within 24 hours to get you started.",
            "[If questions] I'll send you some info and [YOUR_NAME] can follow up.",
            "[If skeptical] Totally fair. Think about it. We're here if you want to give it a shot."
        ]
    }


if __name__ == "__main__":
    # Test scoring
    test_data = {
        "name": "John Smith",
        "business": "HVAC",
        "area": "Fort Lauderdale",
        "asked_pricing": True,
        "asked_timeline": True,
        "asked_leads": True,
        "objections": [],
        "wanted_pricing": True,
        "wanted_to_start": True,
        "wants_callback": False
    }
    
    result = score_prospect(test_data)
    print(json.dumps(result, indent=2))
    print(f"\n{result['recommendation']}")
