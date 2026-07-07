def estimate_costs(miles_per_year, vehicle_type=None, age=None):
    fuel_cost = miles_per_year * 0.12
    maintenance_cost = miles_per_year * 0.05

    insurance_base = {
        "sedan": 1200,
        "suv": 1400,
        "truck": 1300,
        "luxury": 2000,
    }
    insurance_cost = insurance_base.get(vehicle_type, 1500)

    # Older cars typically cost a bit less to insure
    if age is not None and age > 5:
        insurance_cost *= 0.85

    registration_cost = 150

    total_annual = fuel_cost + maintenance_cost + insurance_cost + registration_cost

    return {
        "fuel": round(fuel_cost, 2),
        "maintenance": round(maintenance_cost, 2),
        "insurance": round(insurance_cost, 2),
        "registration": registration_cost,
        "total_annual": round(total_annual, 2),
        "cost_per_month": round(total_annual / 12, 2),
    }