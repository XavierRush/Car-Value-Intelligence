from google import genai

client = genai.Client()  # picks up GEMINI_API_KEY from the environment


def generate_narrative(make, model, age, mileage, purchase_price, car_value):
    prompt = (
        f"A {age}-year-old {make} {model} with {mileage} miles was purchased "
        f"for ${purchase_price:,.2f}. Its estimated current value is "
        f"${car_value:,.2f}. In 2-3 plain-language sentences, explain why the "
        f"car depreciated to this value, referencing its age and mileage."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"GenAI API call failed: {e}")
        return None