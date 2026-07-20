import os
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
        make=make,
        model=model,
        vehicle_type=vehicle_type,
        price=price,
        age=age,
        mileage=mileage,
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
        recent_queries=recent_queries,
    )


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