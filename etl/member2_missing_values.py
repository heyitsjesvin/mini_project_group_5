"""Member 2 - missing values.

Transformation: T5 handle missing values.
"""
import pandas as pd

IS_STUB = False

FILL_BY_ROOM_TYPE = ["bedrooms", "beds", "bathrooms"]


def drop_rows_without_price(df):
    """T5a - a listing without a price cannot be analysed, so it is removed."""
    before = len(df)
    df = df.dropna(subset=["price"]).copy()
    print(f"  T5a rows dropped (no price)      : {before - len(df)}")
    return df


def fill_room_numbers(df):
    """T5b - fill bedrooms / beds / bathrooms with the median of the same room type."""
    df = df.copy()
    for col in FILL_BY_ROOM_TYPE:
        df[col] = df[col].fillna(df.groupby("room_type")[col].transform("median"))
        df[col] = df[col].fillna(df[col].median())
    print("  T5b bedrooms/beds/bathrooms      : filled with room-type median")
    return df


def fill_review_counts(df):
    """T5c - listings with no reviews get reviews_per_month = 0.
    review_scores_rating stays empty on purpose: 'not rated yet' is not a score of 0."""
    df = df.copy()
    df["reviews_per_month"] = df["reviews_per_month"].fillna(0)
    print("  T5c reviews_per_month            : missing -> 0")
    return df


def missing_value_summary(df):
    """Return a table of columns that still contain missing values."""
    counts = df.isna().sum()
    counts = counts[counts > 0].sort_values(ascending=False)
    return pd.DataFrame({"column": counts.index, "missing": counts.values})


def handle_missing_values(df):
    """Run T5 in order."""
    print("\n[TRANSFORM 2/4] Missing values (Member 2) ...")
    df = drop_rows_without_price(df)
    df = fill_room_numbers(df)
    df = fill_review_counts(df)
    return df
