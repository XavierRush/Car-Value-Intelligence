import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from utils import database as db


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.original_db_path = db.DB_PATH
        db.DB_PATH = Path(self.temp_db.name)
        db.create_table()

    def tearDown(self):
        db.DB_PATH = self.original_db_path
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_save_valuation_and_retrieve_recent_queries(self):
        db.save_valuation(
            make="Toyota",
            model="Camry",
            vehicle_type="Sedan",
            price=20000,
            age=3,
            mileage=30000,
            estimated_value=18000,
        )

        rows = db.get_recent_valuations(limit=5)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["make"], "Toyota")
        self.assertEqual(rows[0]["model"], "Camry")
        self.assertEqual(rows[0]["estimated_value"], 18000.0)

    def test_create_table_adds_missing_columns_to_existing_schema(self):
        conn = sqlite3.connect(self.temp_db.name)
        conn.execute("CREATE TABLE valuations(id INTEGER PRIMARY KEY, vehicle_type TEXT, price REAL)")
        conn.commit()
        conn.close()

        db.create_table()

        conn = sqlite3.connect(self.temp_db.name)
        columns = [row[1] for row in conn.execute("PRAGMA table_info(valuations)")]
        conn.close()

        self.assertIn("make", columns)
        self.assertIn("model", columns)
        self.assertIn("age", columns)
        self.assertIn("mileage", columns)
        self.assertIn("estimated_value", columns)


if __name__ == "__main__":
<<<<<<< HEAD
    unittest.main()
=======
    unittest.main()
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
