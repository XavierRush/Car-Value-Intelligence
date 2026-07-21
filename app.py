import os
<<<<<<< HEAD
import re
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import db
import pricing

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "carvalue-dev-secret")

db.init_db()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


MAKES = [
    "Toyota",
    "Honda",
    "Ford",
    "Chevrolet",
    "BMW",
    "Mercedes-Benz",
    "Tesla",
    "Mazda",
    "Subaru",
    "Jeep",
]


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def _to_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@app.route("/")
def home():
    return render_template("home.html", active_page="home")


@app.route("/evaluate")
@login_required
def evaluate():
    return render_template(
        "evaluate.html",
        active_page="evaluate",
        makes=MAKES,
        result=None,
    )


@app.route("/calculate", methods=["POST"])
@login_required
def calculate():
    make = request.form.get("make", "").strip() or "Honda"
    model = request.form.get("model", "").strip() or "Civic"
    vehicle_type = request.form.get("vehicle_type", "sedan")
    condition = request.form.get("condition", "good")

    price = _to_float(request.form.get("price"), 30000)
    age = _to_int(request.form.get("age"), 5)
    mileage = _to_int(request.form.get("mileage"), 60000)

    valuation = pricing.build_full_valuation(
        make=make,
        model=model,
        vehicle_type=vehicle_type,
        condition=condition,
        price=price,
        age=age,
        mileage=mileage,
    )

    db.save_valuation(
=======
import threading
import webbrowser
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request
from genai_helper import generate_narrative
from utils.depreciation import estimate_value
from utils.ownership import estimate_costs
from utils.recommendations import get_ai_recommendation, get_recommendation
from utils.database import create_table, get_recent_valuations, save_valuation

app = Flask(__name__)
create_table()


@app.route("/", methods=["GET"])
def home():
    return render_template("landingpage.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    make = request.form["make"]
    model = request.form["model"]
    price = float(request.form["price"])
    age = int(request.form["age"])
    mileage = int(request.form["mileage"])
    vehicle_type = request.form["vehicle_type"]

    value = estimate_value(price, age, mileage, vehicle_type)
    costs = estimate_costs(12000)
    ai_recommendation = get_ai_recommendation(age, mileage, price, value)
    recommendation = get_recommendation(age, mileage, estimated_value=value, price=price)
    if ai_recommendation:
        recommendation = {
            "action": ai_recommendation.split("Action:", 1)[1].split("Reasoning:", 1)[0].strip(),
            "reasoning": ai_recommendation.split("Reasoning:", 1)[1].strip(),
        }
    narrative = generate_narrative(make, model, age, mileage, price, value)

    save_valuation(
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
        make=make,
        model=model,
        vehicle_type=vehicle_type,
        price=price,
        age=age,
        mileage=mileage,
<<<<<<< HEAD
        estimated_value=valuation["estimated_value"],
    )

    recent_queries = db.get_recent_valuations(limit=5)

    return render_template(
        "results.html",
        active_page="results",
        value=valuation["estimated_value"],
        vehicle={"make": make, "model": model, "age": age, "mileage": mileage},
        confidence=92,
        source_count=len(valuation["sources"]),
        price_variants=valuation["price_variants"],
        breakdown=valuation["breakdown"],
        recommendation=valuation["recommendation"],
        sources=valuation["sources"],
        market_trends=valuation["market_trends"],
        similar_listings=valuation["similar_listings"],
=======
        estimated_value=value,
    )
    recent_queries = get_recent_valuations(limit=5)

    return render_template(
        "results.html",
        value=value,
        costs=costs,
        recommendation=recommendation,
        narrative=narrative,
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
        recent_queries=recent_queries,
    )


<<<<<<< HEAD
@app.route("/results")
@login_required
def results():
    # No submitted vehicle to show a valuation for — send them to the form
    # instead of rendering stale/fake numbers.
    flash("Run an estimate first to see your results.", "error")
    return redirect(url_for("evaluate"))


@app.route("/history")
@login_required
def history():
    queries = db.get_recent_valuations(limit=20)
    return render_template(
        "history.html",
        active_page="history",
        queries=queries,
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password:
            flash("Please fill in every field.", "error")
        elif not EMAIL_RE.match(email):
            flash("That email address doesn't look right.", "error")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
        elif password != confirm_password:
            flash("Passwords don't match.", "error")
        elif db.get_user_by_email(email):
            flash("An account with that email already exists.", "error")
        else:
            db.create_user(name, email, generate_password_hash(password))
            user = db.get_user_by_email(email)
            session["user_id"] = user["id"]
            session["user"] = user["name"]
            flash("Account created — welcome to CarValue!", "success")
            return redirect(url_for("evaluate"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("home"))

    next_url = request.values.get("next") or url_for("home")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.get_user_by_email(email)

        # Same generic message whether the email or password was wrong —
        # don't leak which one, so accounts can't be enumerated.
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Incorrect email or password.", "error")
        else:
            session["user_id"] = user["id"]
            session["user"] = user["name"]
            flash("Signed in successfully.", "success")
            if not next_url.startswith("/") or next_url.startswith("//"):
                next_url = url_for("home")
            return redirect(next_url)

    return render_template("login.html", next_url=next_url)


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("user", None)
    flash("You've been logged out.", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
=======
@app.route("/history")
def history():
    queries = get_recent_valuations(limit=20)
    return render_template("history.html", queries=queries)

@app.route("/evaluate")
def evaluate():
    return render_template("index.html")


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    # Avoid opening two tabs when debug=True triggers the reloader
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1, open_browser).start()
    app.run(debug=True)
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
