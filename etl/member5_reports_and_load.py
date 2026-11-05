"""Member 5 - REPORTS and LOAD.

generate_reports(df) returns {file_name: DataFrame}; load(df, reports) writes the files.
"""
import os

from etl import config

IS_STUB = False

REPORT_COLUMNS = ["id", "name", "district", "room_type", "accommodates", "price",
                  "review_scores_rating"]


def summary_statistics(df):
    cols = ["price", "price_per_person", "accommodates", "bedrooms", "amenities_count",
            "review_scores_rating", "number_of_reviews", "availability_365",
            "host_tenure_years"]
    return df[cols].describe().T.round(2).reset_index().rename(columns={"index": "column"})


def district_report(df):
    result = df.groupby("district").agg(
        listings=("id", "count"),
        avg_price=("price", "mean"),
        median_price=("price", "median"),
        avg_rating=("review_scores_rating", "mean"),
        avg_availability=("availability_365", "mean"),
        total_est_revenue=("est_revenue_365", "sum"),
    ).round(2)
    share = result["listings"] / result["listings"].sum() * 100
    result["share_of_listings_pct"] = share.round(1)
    return result.sort_values("avg_price", ascending=False).reset_index()


def room_type_report(df):
    result = df.groupby(["room_type", "price_category"]).agg(
        listings=("id", "count"), avg_price=("price", "mean")).round(2)
    return result.reset_index()


def top10_expensive(df):
    return df.sort_values(["price", "id"], ascending=[False, True]).head(10)[REPORT_COLUMNS]


def bottom10_cheapest(df):
    return df.sort_values(["price", "id"], ascending=[True, True]).head(10)[REPORT_COLUMNS]


def top10_rated(df):
    """Highest rated listings with at least 20 reviews (fair comparison)."""
    cols = ["id", "name", "district", "price", "number_of_reviews", "review_scores_rating"]
    good = df[df["number_of_reviews"] >= 20]
    ordered = good.sort_values(["review_scores_rating", "number_of_reviews", "id"],
                               ascending=[False, False, True])
    return ordered.head(10)[cols]


def superhost_report(df):
    result = df.groupby("host_is_superhost", dropna=False).agg(
        listings=("id", "count"), avg_price=("price", "mean"),
        avg_rating=("review_scores_rating", "mean"),
        avg_reviews=("number_of_reviews", "mean")).round(2)
    labels = {True: "Superhost", False: "Regular host"}
    result.index = result.index.map(labels).fillna("Unknown")
    return result.reset_index().rename(columns={"host_is_superhost": "host_category"})


def monthly_review_report(df):
    """Monthly report: listings whose most recent review was in each month (last 24 months)."""
    result = (df.dropna(subset=["last_review_month"])
                .groupby("last_review_month")
                .agg(listings=("id", "count"), avg_price=("price", "mean"))
                .round(2).reset_index())
    return result.tail(24)


def affordable_top_rated_homes(df):
    """Filtered report: entire homes, price <= 100, rating >= 4.8, 10+ reviews."""
    keep = ((df["room_type"] == "Entire Home/Apt") & (df["price"] <= 100)
            & (df["review_scores_rating"] >= 4.8) & (df["number_of_reviews"] >= 10))
    cols = ["id", "name", "district", "price", "accommodates",
            "review_scores_rating", "number_of_reviews"]
    return df[keep].sort_values(["review_scores_rating", "id"], ascending=[False, True])[cols]


def generate_reports(df):
    """Build all reports and return them as {file_name: DataFrame}."""
    print("\n[REPORTS] Generating reports (Member 5) ...")
    reports = {
        "cleaned_data.csv": df,
        "summary_statistics.csv": summary_statistics(df),
        "district_report.csv": district_report(df),
        "room_type_price_report.csv": room_type_report(df),
        "top10_expensive_listings.csv": top10_expensive(df),
        "bottom10_cheapest_listings.csv": bottom10_cheapest(df),
        "top10_rated_listings.csv": top10_rated(df),
        "superhost_report.csv": superhost_report(df),
        "monthly_last_review_report.csv": monthly_review_report(df),
        "affordable_top_rated_homes.csv": affordable_top_rated_homes(df),
    }
    for name, report in reports.items():
        print(f"  {name:<34} {report.shape[0]:>6} rows")
    return reports


def load(df, reports):
    """LOAD - save every report to reports/ and the final dataset to output/."""
    print("\n[LOAD] Saving files ...")
    os.makedirs(config.REPORTS_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    for file_name, report in reports.items():
        path = os.path.join(config.REPORTS_DIR, file_name)
        report.to_csv(path, index=False, encoding="utf-8")
        print(f"  saved {path}")
    df.to_csv(config.FINAL_FILE, index=False, encoding="utf-8")
    print(f"  saved {config.FINAL_FILE}")
