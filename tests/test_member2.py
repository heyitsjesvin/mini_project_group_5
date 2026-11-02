"""Tests for Member 2: missing values."""
import unittest

from tests.helpers import needs, stage_df


@needs(1, 2)
class TestMember2(unittest.TestCase):
    def setUp(self):
        from etl import member2_missing_values as m2
        self.m2 = m2
        self.df = stage_df(1)

    def test_rows_without_price_are_dropped(self):
        result = self.m2.drop_rows_without_price(self.df)
        self.assertEqual(len(result), 9)
        self.assertFalse(result["price"].isna().any())

    def test_room_numbers_are_filled(self):
        result = self.m2.fill_room_numbers(self.df)
        for col in ["bedrooms", "beds", "bathrooms"]:
            self.assertFalse(result[col].isna().any(), col)

    def test_filled_value_is_room_type_median(self):
        result = self.m2.fill_room_numbers(self.df)
        row = result[result["id"] == 4].iloc[0]
        self.assertEqual(row["bedrooms"], 1.0)

    def test_reviews_per_month_filled_with_zero(self):
        result = self.m2.fill_review_counts(self.df)
        self.assertEqual(result.loc[result["id"] == 7, "reviews_per_month"].iloc[0], 0)

    def test_rating_is_not_invented(self):
        result = self.m2.handle_missing_values(self.df)
        row = result[result["id"] == 7].iloc[0]
        self.assertTrue(row["review_scores_rating"] != row["review_scores_rating"])

    def test_missing_value_summary(self):
        summary = self.m2.missing_value_summary(self.df)
        self.assertEqual(list(summary.columns), ["column", "missing"])
        self.assertIn("price", list(summary["column"]))

    def test_handle_missing_values_end_to_end(self):
        result = self.m2.handle_missing_values(self.df)
        self.assertEqual(len(result), 9)
        self.assertFalse(result[["price", "bedrooms", "beds", "bathrooms"]].isna().any().any())


if __name__ == "__main__":
    unittest.main()
