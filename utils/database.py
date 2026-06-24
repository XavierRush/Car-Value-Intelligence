import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "cars.db"

def create_table():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS valuations(
            id INTEGER PRIMARY KEY,
            vehicle_type TEXT,
            price REAL,
            age INTEGER,
            mileage INTEGER,
            estimated_value REAL
        )
    """)
    conn.commit()
    conn.close()


def save_valuation(vehicle_type, price, age, mileage, estimated_value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO valuations (vehicle_type, price, age, mileage, estimated_value) VALUES (?, ?, ?, ?, ?)",
        (vehicle_type, price, age, mileage, estimated_value)
    )
    conn.commit()
    conn.close()
