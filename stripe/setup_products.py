#!/usr/bin/env python3
"""
ASTRIA STRIPE SETUP
Create 3 pricing tiers in Stripe.
Run: python stripe/setup_products.py
"""

import os
import json
from dotenv import load_dotenv

try:
    import stripe
except ImportError:
    print("⚠️  Install stripe: pip install stripe")
    exit(1)

load_dotenv()

STRIPE_API_KEY = os.getenv("STRIPE_SECRET_KEY")

if not STRIPE_API_KEY:
    print("❌ STRIPE_SECRET_KEY not found in .env")
    exit(1)

stripe.api_key = STRIPE_API_KEY

# Define pricing tiers
PRODUCTS = [
    {
        "name": "Astria Starter",
        "description": "30-50 leads per month, 1-2 appointments per week",
        "price_monthly": 29900,  # $299 in cents
        "price_setup": 9900,     # $99 setup fee
        "tier": "starter",
        "features": [
            "30-50 qualified leads/month",
            "Personalized email sequences",
            "Real-time reply monitoring",
            "Appointment booking",
            "Weekly reports"
        ]
    },
    {
        "name": "Astria Standard",
        "description": "80-120 leads per month, 2-4 appointments per week",
        "price_monthly": 69900,  # $699 in cents
        "price_setup": 19900,    # $199 setup fee
        "tier": "standard",
        "features": [
            "80-120 qualified leads/month",
            "Personalized email sequences",
            "Real-time reply monitoring",
            "Appointment booking",
            "Weekly reports",
            "Priority support"
        ]
    },
    {
        "name": "Astria Enterprise",
        "description": "200+ leads per month, 4-8 appointments per week",
        "price_monthly": 129900,  # $1,299 in cents
        "price_setup": 29900,     # $299 setup fee
        "tier": "enterprise",
        "features": [
            "200+ qualified leads/month",
            "Personalized email sequences",
            "Real-time reply monitoring",
            "Appointment booking",
            "Weekly reports",
            "Dedicated account manager",
            "Custom workflows"
        ]
    }
]

def create_products():
    """Create Stripe products and prices."""
    
    print("🔧 Setting up Astria pricing in Stripe...\n")
    
    products_created = []
    
    for product_info in PRODUCTS:
        try:
            # Create product
            product = stripe.Product.create(
                name=product_info["name"],
                description=product_info["description"],
                type="service",
                metadata={
                    "tier": product_info["tier"],
                    "features": json.dumps(product_info["features"])
                }
            )
            
            print(f"✅ Created product: {product_info['name']}")
            print(f"   Product ID: {product.id}\n")
            
            # Create monthly price
            monthly_price = stripe.Price.create(
                product=product.id,
                unit_amount=product_info["price_monthly"],
                currency="usd",
                recurring={
                    "interval": "month",
                    "interval_count": 1
                },
                metadata={"billing_type": "monthly"}
            )
            
            print(f"   Monthly Price ID: {monthly_price.id}")
            print(f"   Price: ${product_info['price_monthly'] / 100}/month\n")
            
            # Create setup fee (one-time)
            if product_info["price_setup"] > 0:
                setup_price = stripe.Price.create(
                    product=product.id,
                    unit_amount=product_info["price_setup"],
                    currency="usd",
                    metadata={"billing_type": "setup"}
                )
                
                print(f"   Setup Fee Price ID: {setup_price.id}")
                print(f"   Price: ${product_info['price_setup'] / 100} (one-time)\n")
            
            products_created.append({
                "tier": product_info["tier"],
                "product_id": product.id,
                "monthly_price_id": monthly_price.id,
                "setup_price_id": setup_price.id if product_info["price_setup"] > 0 else None,
                "monthly_amount": product_info["price_monthly"],
                "setup_amount": product_info["price_setup"]
            })
            
        except Exception as e:
            print(f"❌ Error creating {product_info['name']}: {e}\n")
    
    return products_created

def save_config(products):
    """Save product IDs for website integration."""
    
    config = {
        "stripe_products": products,
        "publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY"),
        "created_at": str(__import__("datetime").datetime.now())
    }
    
    with open("stripe/products.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("\n✅ Configuration saved to stripe/products.json\n")
    
    return config

if __name__ == "__main__":
    print("=" * 60)
    print("ASTRIA STRIPE SETUP")
    print("=" * 60 + "\n")
    
    products = create_products()
    
    if products:
        config = save_config(products)
        
        print("=" * 60)
        print("SETUP COMPLETE")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Copy Product IDs to website dashboard")
        print("2. Update pricing page with Stripe checkout buttons")
        print("3. Test with test mode before going live")
        print("\nProduct IDs:")
        for p in products:
            print(f"  {p['tier'].upper()}: {p['product_id']}")
        print()
    else:
        print("❌ No products created. Check your Stripe API key.")
