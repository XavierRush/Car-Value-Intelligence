from google import genai
import os 
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_narrative(make, model, age, mileage, purchase_price, car_value,
    vehicle_type=None, market_price=None,
    days_on_market=None, price_trend=None,
    recommendation=None, annual_costs=None):

    depreciation_amount = purchase_price - car_value
    depreciation_pct = (depreciation_amount / purchase_price) * 100
    expected_mileage = age * 12000
    excess_mileage = mileage - expected_mileage

    if excess_mileage > 0:
        mileage_context = f"{mileage:,} miles - {excess_mileage:,} miles above average for its age"
    else:
        mileage_context = f"{mileage:,} miles - {abs(excess_mileage):,} miles below average for its age"

    market_section = f"\n- Market Price: ${market_price:,.2f}" if market_price else ""
    rec_section = f"\n- Recommendation: {recommendation}" if recommendation else ""

    try:
        
        cost_section = (
            f"\n- Estimated Annual Ownership Cost: ${annual_costs['total_annual']:,.2f}"
            if annual_costs else ""
        )

        prompt = f"""
You are a car valuation expert helping a SELLER understand their car's value.
Speak like a knowledgeable friend — direct, honest, plain English. No filler phrases.

Car Details:
- Vehicle: {age}-year-old {make} {model}{f' ({vehicle_type})' if vehicle_type else ''}
- Mileage: {mileage_context}
- Original Purchase Price: ${purchase_price:,.2f}
- Estimated Current Value: ${car_value:,.2f}
- Total Depreciation: ${depreciation_amount:,.2f} ({depreciation_pct:.1f}%){market_section}{cost_section}{rec_section}

Write 3-4 sentences that:
1. Explain WHY this car is worth ${car_value:,.2f} right now
2. Call out the biggest factor helping OR hurting its value (age, mileage, type, market trend)
3. Give one clear, actionable insight for the seller — should they list now, wait, or adjust price?

Be specific to this car. Do not be generic.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"GenAI API call failed: {e}")
        return "Unable to generate explanation at this time."