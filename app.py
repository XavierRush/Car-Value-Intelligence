from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    car_value = None

    if request.method == "POST":
        make = request.form["make"]
        model = request.form["model"]

        purchase_price = float(request.form["price"])
        age = int(request.form["age"])
        mileage = int(request.form["mileage"])

        value = purchase_price

        for i in range(age):
            value = value * 0.90
        value = value - (mileage * 0.05)

        if value < 0:
            value = 0
        car_value = round(value, 2)

    return render_template("index.html", car_value=car_value)

if __name__ == "__main__":
    app.run(debug=True)