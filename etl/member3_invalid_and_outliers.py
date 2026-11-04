"""Member 3 - invalid values, outliers and validation checks.

Transformations: T6 remove invalid/outlier rows, T7 round numbers, plus validation checks.
"""
from etl import config

IS_STUB = False


def remove_invalid_rows(df):
    """T6 - remove impossible values and extreme outliers."""
    before = len(df)
    mask = (
        df["price"].between(config.MIN_PRICE, config.MAX_PRICE)
        & (df["accommodates"] >= 1)
        & df["minimum_nights"].between(1, config.MAX_MIN_NIGHTS)
        & df["availability_365"].between(0, 365)
        & df["latitude"].between(*config.BERLIN_LAT)
        & df["longitude"].between(*config.BERLIN_LON)
    )
    df = df[mask].copy()
    print(f"  T6 invalid / outlier rows removed: {before - len(df)}")
    return df


def round_numeric(df):
    """T7 - consistent decimal places."""
    df = df.copy()
    df["price"] = df["price"].round(2)
    df["reviews_per_month"] = df["reviews_per_month"].round(2)
    for col in ["bathrooms", "bedrooms", "beds"]:
        df[col] = df[col].round(1)
    print("  T7 numeric columns rounded")
    return df


def validate(df):
    """Validation check - raise ValueError if any rule is still broken."""
    problems = []
    if df["id"].duplicated().any():
        problems.append("duplicate ids")
    if df["price"].isna().any():
        problems.append("missing prices")
    if not df["price"].between(config.MIN_PRICE, config.MAX_PRICE).all():
        problems.append("price outside allowed range")
    if not df["latitude"].between(*config.BERLIN_LAT).all():
        problems.append("latitude outside Berlin")
    if problems:
        raise ValueError("Validation failed: " + ", ".join(problems))
    print("  Validation checks passed")
    return df


def remove_invalid_and_outliers(df):
    """Run T6, T7 and the validation checks in order."""
    print("\n[TRANSFORM 3/4] Invalid values and outliers (Member 3) ...")
    df = remove_invalid_rows(df)
    df = round_numeric(df)
    df = validate(df)
    return df
