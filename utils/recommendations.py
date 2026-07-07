def get_recommendation(age, mileage, vehicle_type=None):
    if age > 10 or mileage > 150000:
        return {
            "recommendation": "Consider selling soon",
            "urgency": "high",
            "reason": "High age or mileage means depreciation will keep accelerating. Value only drops further from here.",
        }
    elif age < 5 and mileage < 60000:
        return {
            "recommendation": "Holding may be a good option",
            "urgency": "low",
            "reason": "Low age and mileage mean the car is still retaining value well. No rush to sell.",
        }
    else:
        return {
            "recommendation": "Monitor depreciation trends",
            "urgency": "medium",
            "reason": "This car is in a middle range for age and mileage. Keep an eye on the market before deciding.",
        }