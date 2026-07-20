import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None


def generate_narrative(make, model, age, mileage, purchase_price, car_value):
    prompt = (
        f"A {age}-year-old {make} {model} with {mileage} miles was purchased "
        f"for ${purchase_price:,.2f}. Its estimated current value is "
        f"${car_value:,.2f}. In 2-3 plain-language sentences, explain why the "
        f"car depreciated to this value, referencing its age and mileage."
    )

    if client is None:
        print("GEMINI_API_KEY is not set. Please add it to your .env file.")
        return None

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"GenAI API call failed: {e}")
        return None


def generate_recommendation(age, mileage, purchase_price, car_value):
    prompt = (
        f"You are helping a car owner decide whether to sell or hold a vehicle. "
        f"The car is {age} years old, has {mileage} miles, was purchased for ${purchase_price:,.2f}, "
        f"and is now estimated at ${car_value:,.2f}. "
        f"Respond in exactly two short sentences. The first sentence should start with 'Action:' and give a clear recommendation such as 'Sell the car at this value.' or 'Hold on to the car for now.' "
        f"The second sentence should start with 'Reasoning:' and explain why in plain language."
    )

    if client is None:
        return None

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"GenAI recommendation call failed: {e}")
        return None