from flask import Flask, render_template, request

from utils.depreciation import estimate_value
from utils.ownership import estimate_costs
from utils.recommendations import get_recommendation
from utils.database import create_table, save_valuation

app = Flask(__name__)

create_table()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        price = float(request.form["price"])
        age = int(request.form["age"])
        mileage = int(request.form["mileage"])
        vehicle_type = request.form["vehicle_type"]

        value = estimate_value(
            price,
            age,
            mileage,
            vehicle_type
        )

        costs = estimate_costs(12000)

        recommendation = get_recommendation(
            age,
            mileage
        )

        save_valuation(vehicle_type, price, age, mileage, value)

        return render_template(
            "results.html",
            value=value,
            costs=costs,
            recommendation=recommendation
        )
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)