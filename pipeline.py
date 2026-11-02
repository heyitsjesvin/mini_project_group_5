"""Main ETL pipeline: Extract -> Transform -> Reports -> Load.

Run with:  python pipeline.py
"""
import time

from etl import member1_extract_and_structure as member1
from etl import member2_missing_values as member2
from etl import member3_invalid_and_outliers as member3
from etl import member4_features as member4
from etl import member5_reports_and_load as member5


def extract():
    """Step 5 - read the raw data and save a copy in raw_data/."""
    return member1.extract()


def transform(df):
    """Step 6 - cleaning, missing values, validation and feature engineering."""
    rows_in = len(df)
    df = member1.structural_cleaning(df)
    df = member2.handle_missing_values(df)
    df = member3.remove_invalid_and_outliers(df)
    df = member4.add_features(df)
    print(f"\n[TRANSFORM] {rows_in:,} raw rows -> {len(df):,} rows, {df.shape[1]} columns")
    return df


def generate_reports(df):
    """Step 7 - build the reports."""
    return member5.generate_reports(df)


def load(df, reports):
    """Step 8 - store the reports and the final dataset."""
    member5.load(df, reports)


def run_etl_pipeline():
    """Step 9 - Extract -> Transform -> Reports -> Load."""
    start = time.time()
    print("=" * 60)
    print(" BERLIN AIRBNB ETL PIPELINE")
    print("=" * 60)
    raw_df = extract()
    clean_df = transform(raw_df)
    reports = generate_reports(clean_df)
    load(clean_df, reports)
    print(f"\nPIPELINE FINISHED in {time.time() - start:.1f}s: "
          f"{raw_df.shape[0]:,} x {raw_df.shape[1]} -> clean {clean_df.shape[0]:,} x "
          f"{clean_df.shape[1]}")
    return clean_df


if __name__ == "__main__":
    run_etl_pipeline()
