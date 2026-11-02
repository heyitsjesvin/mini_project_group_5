"""Tests for Member 3: invalid values, outliers, validation."""
import unittest

from tests.helpers import needs, stage_df


@needs(1, 2, 3)
class TestMember3(unittest.TestCase):
    def setUp(self):
        from etl import member3_invalid_and_outliers as m3
        self.m3 = m3
        self.df = stage_df(2)

    def test_invalid_and_outlier_rows_removed(self):
        result = self.m3.remove_invalid_rows(self.df)
        remaining = set(result["id"])
        self.assertNotIn(2, remaining)   # price 1250 above the limit
        self.assertNotIn(5, remaining)   # outside Berlin
        self.assertNotIn(6, remaining)   # minimum_nights 1125
        self.assertEqual(remaining, {1, 4, 7, 8, 10, 11})

    def test_valid_rows_are_kept(self):
        result = self.m3.remove_invalid_rows(self.df)
        self.assertEqual(len(result), 6)

    def test_round_numeric(self):
        df = self.df.copy()
        df["price"] = 99.123456
        result = self.m3.round_numeric(df)
        self.assertTrue((result["price"] == 99.12).all())

    def test_validate_passes_on_clean_data(self):
        clean = self.m3.remove_invalid_rows(self.df)
        self.assertEqual(len(self.m3.validate(clean)), len(clean))

    def test_validate_fails_on_bad_data(self):
        with self.assertRaises(ValueError):
            self.m3.validate(self.df)      # still contains outliers

    def test_end_to_end(self):
        result = self.m3.remove_invalid_and_outliers(self.df)
        self.assertEqual(len(result), 6)
        self.assertTrue(result["price"].between(1, 1000).all())


if __name__ == "__main__":
    unittest.main()
