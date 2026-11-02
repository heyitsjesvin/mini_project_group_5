"""Tests for Member 5: reports and load."""
import os
import tempfile
import unittest
from unittest import mock

from etl import config
from tests.helpers import needs, stage_df


@needs(1, 2, 3, 4, 5)
class TestMember5(unittest.TestCase):
    def setUp(self):
        from etl import member5_reports_and_load as m5
        self.m5 = m5
        self.df = stage_df(4)

    def test_at_least_three_reports(self):
        reports = self.m5.generate_reports(self.df)
        self.assertGreaterEqual(len(reports), 3)
        self.assertIn("cleaned_data.csv", reports)

    def test_summary_statistics(self):
        stats = self.m5.summary_statistics(self.df)
        self.assertIn("price", list(stats["column"]))
        self.assertIn("mean", stats.columns)

    def test_district_report(self):
        report = self.m5.district_report(self.df)
        self.assertEqual(report["listings"].sum(), len(self.df))
        self.assertAlmostEqual(report["share_of_listings_pct"].sum(), 100, delta=0.5)

    def test_top_and_bottom_10(self):
        top = self.m5.top10_expensive(self.df)
        bottom = self.m5.bottom10_cheapest(self.df)
        self.assertEqual(top.iloc[0]["price"], self.df["price"].max())
        self.assertEqual(bottom.iloc[0]["price"], self.df["price"].min())
        self.assertLessEqual(len(top), 10)

    def test_top_rated_requires_20_reviews(self):
        result = self.m5.top10_rated(self.df)
        self.assertTrue((result["number_of_reviews"] >= 20).all())
        self.assertEqual(result.iloc[0]["id"], 10)

    def test_superhost_and_monthly_and_filtered(self):
        self.assertGreaterEqual(len(self.m5.superhost_report(self.df)), 2)
        self.assertGreaterEqual(len(self.m5.monthly_review_report(self.df)), 1)
        filtered = self.m5.affordable_top_rated_homes(self.df)
        self.assertTrue((filtered["price"] <= 100).all())
        self.assertTrue((filtered["review_scores_rating"] >= 4.8).all())

    def test_load_writes_files(self):
        reports = self.m5.generate_reports(self.df)
        with tempfile.TemporaryDirectory() as tmp:
            reports_dir = os.path.join(tmp, "reports")
            output_dir = os.path.join(tmp, "output")
            final_file = os.path.join(output_dir, "final.csv")
            with mock.patch.object(config, "REPORTS_DIR", reports_dir), \
                    mock.patch.object(config, "OUTPUT_DIR", output_dir), \
                    mock.patch.object(config, "FINAL_FILE", final_file):
                self.m5.load(self.df, reports)
            for name in reports:
                self.assertTrue(os.path.exists(os.path.join(reports_dir, name)), name)
            self.assertTrue(os.path.exists(final_file))


@needs(1, 2, 3, 4, 5)
class TestWholePipeline(unittest.TestCase):
    def test_pipeline_functions_exist(self):
        import pipeline
        for name in ["extract", "transform", "load", "run_etl_pipeline"]:
            self.assertTrue(callable(getattr(pipeline, name)), name)

    def test_transform_on_sample(self):
        import pipeline
        from tests.helpers import raw_sample
        result = pipeline.transform(raw_sample())
        self.assertEqual(len(result), 6)
        self.assertTrue(result["id"].is_unique)


if __name__ == "__main__":
    unittest.main()
