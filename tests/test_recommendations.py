import unittest

from utils.recommendations import get_recommendation


class RecommendationTests(unittest.TestCase):
    def test_returns_sell_action_and_reasoning_for_older_vehicle(self):
        result = get_recommendation(age=12, mileage=180000, estimated_value=5000, price=12000)

        self.assertEqual(result["action"], "Sell the car at this value.")
        self.assertIn("depreciation", result["reasoning"].lower())


if __name__ == "__main__":
<<<<<<< HEAD
    unittest.main()
=======
    unittest.main()
>>>>>>> 6b61039cf293e630bba18734b0d0032baf1eab01
