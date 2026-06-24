def get_recommendation(age, mileage):
    if age > 10 or mileage > 150000:
        return "Consider selling soon."
    if age < 5 and mileage < 60000:
        return "Holding may be a good option."
    return "Monitor depreciation trends."
