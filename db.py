"""
Thin SQLite helper around cars.db.

The `valuations` table already exists in cars.db with this schema:

    CREATE TABLE valuations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT,
        model TEXT,
        vehicle_type TEXT,
        price REAL,
        age INTEGER,
        mileage INTEGER,
        estimated_value REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )

init_db() will create it if it's ever missing (e.g. a fresh cars.db),
so the app never crashes on a clean checkout.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "cars.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS valuations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT,
            model TEXT,
            vehicle_type TEXT,
            price REAL,
            age INTEGER,
            mileage INTEGER,
            estimated_value REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def create_user(name, email, password_hash):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_valuation(make, model, vehicle_type, price, age, mileage, estimated_value):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO valuations (make, model, vehicle_type, price, age, mileage, estimated_value)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (make, model, vehicle_type, price, age, mileage, estimated_value),
    )
    conn.commit()
    conn.close()


def get_recent_valuations(limit=5):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM valuations ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()

    queries = []
    for row in rows:
        item = dict(row)
        # created_at is stored as "YYYY-MM-DD HH:MM:SS" — templates just
        # want the date.
        if item.get("created_at"):
            item["created_at"] = str(item["created_at"]).split(" ")[0]
        queries.append(item)
    return queries