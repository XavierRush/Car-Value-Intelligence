import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "cars.db"


def create_table():
    os.makedirs(DB_PATH.parent, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    try:
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

        columns = [row[1] for row in conn.execute("PRAGMA table_info(valuations)")]
        if "make" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN make TEXT")
        if "model" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN model TEXT")
        if "vehicle_type" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN vehicle_type TEXT")
        if "price" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN price REAL")
        if "age" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN age INTEGER")
        if "mileage" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN mileage INTEGER")
        if "estimated_value" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN estimated_value REAL")
        if "created_at" not in columns:
            conn.execute("ALTER TABLE valuations ADD COLUMN created_at TEXT")

        conn.commit()
    finally:
        conn.close()


def save_valuation(
    make=None,
    model=None,
    vehicle_type=None,
    price=None,
    age=None,
    mileage=None,
    estimated_value=None,
    created_at=None,
):
    if created_at is None:
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.execute(
            """
            INSERT INTO valuations (
                make, model, vehicle_type, price, age, mileage, estimated_value, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (make, model, vehicle_type, price, age, mileage, estimated_value, created_at),
        )
        conn.commit()
    finally:
        conn.close()


def get_recent_valuations(limit=5):
    conn = sqlite3.connect(str(DB_PATH))
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT make, model, vehicle_type, price, age, mileage, estimated_value, created_at
            FROM valuations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        conn.close()
<<<<<<< HEAD
<<<<<<< HEAD
    return [dict(row) for row in rows]
=======
    return [dict(row) for row in rows]
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
=======
    return [dict(row) for row in rows]
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
