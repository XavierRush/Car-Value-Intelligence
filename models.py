from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    queries = db.relationship("Query", backref="user", lazy="dynamic")

    def set_password(self, raw_password: str) -> None:
        # scrypt/pbkdf2 salted hash — never store or log the raw password
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)


class Query(db.Model):
    """One saved valuation, scoped to the user who ran it."""
    __tablename__ = "queries"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    make = db.Column(db.String(80))
    model = db.Column(db.String(80))
    vehicle_type = db.Column(db.String(40))
    price = db.Column(db.Integer)
    age = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    estimated_value = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
