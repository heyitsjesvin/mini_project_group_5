"""Member 1 - EXTRACT and structural cleaning.

Transformations: T1 remove duplicates, T2 select and rename columns,
T3 convert data types, T4 standardize text.
"""
import os
import shutil

import pandas as pd

from etl import config

IS_STUB = False


def extract():
    """Read the Berlin listings CSV, show its size, save a raw copy, return the data."""
    print("\n[EXTRACT] Reading source file ...")
    if not os.path.exists(config.SOURCE_FILE):
        raise FileNotFoundError(
            "Source file not found: " + config.SOURCE_FILE + "\n"
            "Place listings_berlin.csv (Inside Airbnb, Berlin) in the raw_data folder."
        )
    df = pd.read_csv(config.SOURCE_FILE, low_memory=False)
    print(f"[EXTRACT] Number of records : {df.shape[0]:,}")
    print(f"[EXTRACT] Number of columns : {df.shape[1]}")

    os.makedirs(config.RAW_DIR, exist_ok=True)
    shutil.copy(config.SOURCE_FILE, config.RAW_COPY_FILE)
    print(f"[EXTRACT] Raw copy saved    : {config.RAW_COPY_FILE}")
    return df


def remove_duplicates(df):
    """T1 - keep each listing id only once."""
    before = len(df)
    df = df.drop_duplicates(subset="id", keep="first")
    print(f"  T1 duplicates removed            : {before - len(df)}")
    return df


def select_and_rename_columns(df):
    """T2 - keep the 32 useful columns (of 79) and give them clear names."""
    df = df[config.COLUMNS_TO_KEEP].rename(columns=config.RENAME_MAP)
    print(f"  T2 columns kept / renamed        : {df.shape[1]}")
    return df


def convert_data_types(df):
    """T3 - '$1,105.00' -> float, '95%' -> float, 't'/'f' -> boolean, text -> datetime."""
    df = df.copy()
    df["price"] = pd.to_numeric(
        df["price"].astype("string").str.replace(r"[$,]", "", regex=True), errors="coerce")

    for col in ["host_response_rate", "host_acceptance_rate"]:
        df[col] = pd.to_numeric(
            df[col].astype("string").str.replace("%", "", regex=False), errors="coerce")

    for col in ["host_is_superhost", "host_identity_verified", "instant_bookable"]:
        df[col] = df[col].map({"t": True, "f": False}).astype("boolean")

    for col in ["host_since", "first_review", "last_review"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    print("  T3 data types converted          : price, rates, booleans, dates")
    return df


def standardize_text(df):
    """T4 - trim spaces, unify capitalisation, fill missing names."""
    df = df.copy()
    text_cols = ["name", "host_name", "district", "neighbourhood", "property_type", "room_type"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    df["district"] = df["district"].str.title()
    df["room_type"] = df["room_type"].str.title()
    df["name"] = df["name"].fillna("Unknown")
    df["host_name"] = df["host_name"].fillna("Unknown")
    print("  T4 text standardized             : 6 text columns")
    return df


def structural_cleaning(df):
    """Run T1-T4 in order."""
    print("\n[TRANSFORM 1/4] Structural cleaning (Member 1) ...")
    df = remove_duplicates(df)
    df = select_and_rename_columns(df)
    df = convert_data_types(df)
    df = standardize_text(df)
    return df
