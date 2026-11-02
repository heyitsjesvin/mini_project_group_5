"""Tests for Member 1: extract and structural cleaning."""
import os
import unittest

import pandas as pd

from etl import config
from tests.helpers import needs, raw_sample, real_data_available


@needs(1)
class TestMember1(unittest.TestCase):
    def setUp(self):
        from etl import member1_extract_and_structure as m1
        self.m1 = m1
        self.raw = raw_sample()

    def test_remove_duplicates_keeps_one_row_per_id(self):
        result = self.m1.remove_duplicates(self.raw)
        self.assertEqual(len(result), 10)
        self.assertTrue(result["id"].is_unique)

    def test_select_and_rename_columns(self):
        result = self.m1.select_and_rename_columns(self.raw)
        self.assertEqual(result.shape[1], 32)
        self.assertIn("district", result.columns)
        self.assertIn("est_revenue_365", result.columns)
        self.assertNotIn("listing_url", result.columns)

    def test_price_becomes_number(self):
        renamed = self.m1.select_and_rename_columns(self.raw)
        result = self.m1.convert_data_types(renamed)
        self.assertTrue(pd.api.types.is_float_dtype(result["price"]))
        self.assertEqual(result.loc[1, "price"], 1250.0)
        self.assertTrue(pd.isna(result.loc[2, "price"]))

    def test_percentages_and_booleans_and_dates(self):
        renamed = self.m1.select_and_rename_columns(self.raw)
        result = self.m1.convert_data_types(renamed)
        self.assertEqual(result.loc[0, "host_response_rate"], 95.0)
        self.assertTrue(bool(result.loc[0, "host_is_superhost"]))
        self.assertFalse(bool(result.loc[0, "instant_bookable"]))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(result["host_since"]))

    def test_standardize_text(self):
        step = self.m1.select_and_rename_columns(self.raw)
        step = self.m1.convert_data_types(step)
        result = self.m1.standardize_text(step)
        self.assertEqual(result.loc[7, "name"], "Sunny Room")
        self.assertEqual(result.loc[7, "district"], "Friedrichshain-Kreuzberg")
        self.assertEqual(result.loc[0, "room_type"], "Entire Home/Apt")

    def test_structural_cleaning_end_to_end(self):
        result = self.m1.structural_cleaning(self.raw)
        self.assertEqual(len(result), 10)
        self.assertEqual(result.shape[1], 32)

    @unittest.skipUnless(real_data_available(), "real data file not present")
    def test_extract_reads_file_and_saves_raw_copy(self):
        if os.path.exists(config.RAW_COPY_FILE):
            os.remove(config.RAW_COPY_FILE)
        df = self.m1.extract()
        self.assertEqual(df.shape[1], 79)
        self.assertGreater(len(df), 10000)
        self.assertTrue(os.path.exists(config.RAW_COPY_FILE))


if __name__ == "__main__":
    unittest.main()
