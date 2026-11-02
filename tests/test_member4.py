"""Tests for Member 4: feature engineering."""
import unittest

from tests.helpers import needs, stage_df


@needs(1, 2, 3, 4)
class TestMember4(unittest.TestCase):
    def setUp(self):
        from etl import member4_features as m4
        self.m4 = m4
        self.df = stage_df(3)

    def row(self, df, row_id):
        return df[df["id"] == row_id].iloc[0]

    def test_price_per_person_and_category(self):
        result = self.m4.add_price_features(self.df)
        self.assertEqual(self.row(result, 11)["price_per_person"], 40.0)    # 160 / 4
        self.assertEqual(self.row(result, 7)["price_category"], "Budget")   # 30
        self.assertEqual(self.row(result, 1)["price_category"], "Standard")  # 100
        self.assertEqual(self.row(result, 10)["price_category"], "Premium")  # 200

    def test_host_features(self):
        result = self.m4.add_host_features(self.df)
        self.assertEqual(self.row(result, 1)["host_type"], "Single-listing host")
        self.assertEqual(self.row(result, 10)["host_type"], "Multi-listing host")
        self.assertEqual(self.row(result, 10)["host_tenure_years"], 15.0)

    def test_amenities_count(self):
        result = self.m4.add_amenities_count(self.df)
        self.assertNotIn("amenities", result.columns)
        self.assertEqual(self.row(result, 1)["amenities_count"], 3)
        self.assertEqual(self.row(result, 10)["amenities_count"], 0)   # invalid text

    def test_review_features(self):
        result = self.m4.add_review_features(self.df)
        self.assertFalse(bool(self.row(result, 7)["has_reviews"]))
        self.assertEqual(self.row(result, 7)["rating_category"], "Not rated")
        self.assertEqual(self.row(result, 10)["rating_category"], "Excellent")
        self.assertEqual(self.row(result, 11)["rating_category"], "Poor")
        self.assertEqual(self.row(result, 1)["last_review_month"], "2025-03")

    def test_availability_level(self):
        result = self.m4.add_availability_level(self.df)
        self.assertEqual(self.row(result, 7)["availability_level"], "Low")      # 10 days
        self.assertEqual(self.row(result, 1)["availability_level"], "High")     # 200 days

    def test_rank_and_sort(self):
        result = self.m4.rank_and_sort(self.df)
        mitte = result[result["district"] == "Mitte"]
        self.assertEqual(mitte.iloc[0]["id"], 10)                    # most expensive in Mitte
        self.assertEqual(mitte.iloc[0]["price_rank_in_district"], 1)
        self.assertEqual(list(result["district"]), sorted(result["district"]))

    def test_add_features_adds_new_columns(self):
        result = self.m4.add_features(self.df)
        new = {"price_per_person", "price_category", "host_tenure_years", "host_type",
               "amenities_count", "has_reviews", "rating_category", "availability_level",
               "price_rank_in_district"}
        self.assertTrue(new.issubset(result.columns))
        self.assertEqual(len(result), len(self.df))


if __name__ == "__main__":
    unittest.main()
