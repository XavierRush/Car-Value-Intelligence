import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from genai_helper import generate_narrative
from utils.depreciation import estimate_value
from utils.ownership import estimate_costs
from utils.recommendations import get_recommendation
from utils.database import create_table, save_valuation

app = Flask(__name__)
create_table()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        make         = request.form["make"]
        model        = request.form["model"]
        price        = float(request.form["price"])
        age          = int(request.form["age"])
        mileage      = int(request.form["mileage"])
        vehicle_type = request.form["vehicle_type"]

        value          = estimate_value(price, age, mileage, vehicle_type)
        costs          = estimate_costs(12000, vehicle_type, age)
        recommendation = get_recommendation(age, mileage, vehicle_type)

        # Inject original price so results page can show value-retained %
        costs["original_price"] = price

        narrative = generate_narrative(
            make=make,
            model=model,
            age=age,
            mileage=mileage,
            purchase_price=price,
            car_value=value,
            vehicle_type=vehicle_type,
            recommendation=recommendation["recommendation"],
            annual_costs=costs,
        )

        save_valuation(vehicle_type, price, age, mileage, value)
        
        print("VALUE:", value)
        print("COSTS:", costs)
        print("REC:", recommendation)
        print("NARRATIVE:", narrative)

        return render_template(
            "results.html",
            make=make,
            model=model,
            value=value,
            costs=costs,
            recommendation=recommendation,
            narrative=narrative,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)