def estimate_costs(miles_per_year):
    fuel_cost = miles_per_year * 0.12
    maintenance_cost = miles_per_year * 0.05
    insurance_cost = 1500
    total = fuel_cost + maintenance_cost + insurance_cost
    return {
        "fuel": round(fuel_cost, 2),
        "maintenance": round(maintenance_cost, 2),
        "insurance": insurance_cost,
        "total": round(total, 2)
    }
