"""Member 4 - feature engineering, categories and ranking.

Transformations: T8-T14 (price features, host features, amenities count,
review features, availability level, price rank and sorting).
"""
import json

import numpy as np
import pandas as pd

from etl import config

IS_STUB = False


def add_price_features(df):
    """T8 price_per_person and T9 price_category."""
    df = df.copy()
    df["price_per_person"] = (df["price"] / df["accommodates"]).round(2)
    df["price_category"] = pd.cut(
        df["price"], bins=[0, 60, 120, 250, np.inf],
        labels=["Budget", "Standard", "Premium", "Luxury"]).astype("string")
    print("  T8  price_per_person created")
    print("  T9  price_category created")
    return df


def add_host_features(df):
    """T10 host_tenure_years and host_type."""
    df = df.copy()
    ref = pd.Timestamp(config.REFERENCE_DATE)
    df["host_tenure_years"] = ((ref - df["host_since"]).dt.days / 365.25).round(1)
    df["host_type"] = np.where(
        df["host_listings_count"] > 1, "Multi-listing host", "Single-listing host")
    print("  T10 host_tenure_years + host_type created")
    return df


def add_amenities_count(df):
    """T11 count the amenities (stored as JSON text) and drop the long text column."""
    df = df.copy()

    def count(value):
        try:
            return len(json.loads(value))
        except (TypeError, ValueError):
            return 0

    df["amenities_count"] = df["amenities"].apply(count)
    df = df.drop(columns=["amenities"])
    print("  T11 amenities_count created (amenities text dropped)")
    return df


def add_review_features(df):
    """T12 has_reviews, rating_category, last_review_year and last_review_month."""
    df = df.copy()
    df["has_reviews"] = df["number_of_reviews"] > 0
    df["rating_category"] = pd.cut(
        df["review_scores_rating"], bins=[0, 3.99, 4.49, 4.79, 5.0],
        labels=["Poor", "Good", "Very Good", "Excellent"]).astype("string")
    df["rating_category"] = df["rating_category"].fillna("Not rated")
    df["last_review_year"] = df["last_review"].dt.year
    df["last_review_month"] = df["last_review"].dt.to_period("M").astype("string")
    print("  T12 has_reviews, rating_category, last_review_year/month created")
    return df


def add_availability_level(df):
    """T13 availability_level: Low / Medium / High."""
    df = df.copy()
    df["availability_level"] = pd.cut(
        df["availability_365"], bins=[-1, 60, 180, 365],
        labels=["Low", "Medium", "High"]).astype("string")
    print("  T13 availability_level created")
    return df


def rank_and_sort(df):
    """T14 rank price inside each district (1 = most expensive) and sort."""
    df = df.copy()
    df["price_rank_in_district"] = df.groupby("district")["price"].rank(
        method="min", ascending=False).astype(int)
    df = df.sort_values(["district", "price_rank_in_district", "id"]).reset_index(drop=True)
    print("  T14 price_rank_in_district created + data sorted")
    return df


def add_features(df):
    """Run T8-T14 in order."""
    print("\n[TRANSFORM 4/4] Feature engineering (Member 4) ...")
    df = add_price_features(df)
    df = add_host_features(df)
    df = add_amenities_count(df)
    df = add_review_features(df)
    df = add_availability_level(df)
    df = rank_and_sort(df)
    return df
