"""EDA for the cleaned Berlin Airbnb data.

Run from the project folder (next to pipeline.py):
    py eda.py
Reads output/berlin_airbnb_analysis_ready.csv, saves plots to eda_plots/.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

DATA = os.path.join("output", "berlin_airbnb_analysis_ready.csv")
OUT = "eda_plots"
ROOM_ORDER = ["Entire Home/Apt", "Private Room", "Shared Room", "Hotel Room"]
CAT_ORDER = ["Budget", "Standard", "Premium", "Luxury"]


def save(name):
    os.makedirs(OUT, exist_ok=True)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, name), dpi=120)
    plt.close()
    print("  saved", name)


def load_data(path=DATA):
    if not os.path.exists(path):
        sys.exit("File not found: " + path + "\nRun py pipeline.py first.")
    df = pd.read_csv(path, low_memory=False)
    df["host_is_superhost"] = df["host_is_superhost"].map(
        {True: "Superhost", False: "Regular host", "True": "Superhost",
         "False": "Regular host"})
    return df


def data_overview(df):
    print("Shape:", df.shape)
    miss = df.isna().sum()
    miss = miss[miss > 0].sort_values(ascending=False)
    print("Columns with missing values:\n", miss.to_string())
    os.makedirs(OUT, exist_ok=True)
    df.describe().T.round(2).to_csv(os.path.join(OUT, "summary_statistics.csv"))
    miss.rename("missing").to_csv(os.path.join(OUT, "missing_values.csv"))
    plt.figure(figsize=(8, 4))
    miss.sort_values().plot.barh(color="#c0504d")
    plt.title("Missing values per column (cleaned data)")
    plt.xlabel("Number of listings")
    save("00_missing_values.png")


def price_distribution(df):
    cap = df["price"].quantile(0.99)
    plt.figure(figsize=(8, 4.5))
    plt.hist(df["price"].clip(upper=cap), bins=50, color="#4f81bd")
    plt.axvline(df["price"].median(), color="red", ls="--",
                label="median %.0f" % df["price"].median())
    plt.axvline(df["price"].mean(), color="orange", ls="--",
                label="mean %.0f" % df["price"].mean())
    plt.legend()
    plt.title("Price per night (values above the 99th percentile grouped at %.0f)" % cap)
    plt.xlabel("Price (EUR)")
    plt.ylabel("Listings")
    save("01_price_distribution.png")


def price_by_room_type(df):
    rooms = [r for r in ROOM_ORDER if r in set(df["room_type"])]
    data = [df.loc[df["room_type"] == r, "price"].clip(upper=500) for r in rooms]
    plt.figure(figsize=(8, 4.5))
    plt.boxplot(data, tick_labels=rooms, showfliers=False)
    plt.title("Price by room type (outliers hidden)")
    plt.ylabel("Price (EUR)")
    save("02_price_by_room_type.png")


def listings_per_district(df):
    plt.figure(figsize=(8, 6))
    df["district"].value_counts().sort_values().plot.barh(color="#4f81bd")
    plt.title("Listings per district")
    plt.xlabel("Listings")
    save("03_listings_per_district.png")


def price_by_district(df):
    plt.figure(figsize=(8, 6))
    df.groupby("district")["price"].median().sort_values().plot.barh(color="#9bbb59")
    plt.title("Median price per district")
    plt.xlabel("Median price (EUR)")
    save("04_median_price_by_district.png")


def room_type_share(df):
    counts = df["room_type"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=90)
    plt.title("Room type share")
    save("05_room_type_share.png")


def price_category_counts(df):
    counts = df["price_category"].value_counts().reindex(CAT_ORDER)
    plt.figure(figsize=(7, 4.5))
    ax = counts.plot.bar(color="#8064a2", rot=0)
    ax.bar_label(ax.containers[0])
    plt.title("Listings per price category")
    plt.ylabel("Listings")
    save("06_price_category_counts.png")


def rating_distribution(df):
    r = df["review_scores_rating"].dropna()
    plt.figure(figsize=(8, 4.5))
    plt.hist(r, bins=30, color="#f79646")
    plt.axvline(r.median(), color="red", ls="--", label="median %.2f" % r.median())
    plt.legend()
    plt.title("Rating distribution (%d rated listings)" % len(r))
    plt.xlabel("review_scores_rating")
    plt.ylabel("Listings")
    save("07_rating_distribution.png")


def price_vs_accommodates(df):
    d = df[df["accommodates"] <= 8]
    keys = sorted(d["accommodates"].unique())
    data = [d.loc[d["accommodates"] == k, "price"] for k in keys]
    plt.figure(figsize=(8, 4.5))
    plt.boxplot(data, tick_labels=keys, showfliers=False)
    plt.title("Price by number of guests (up to 8, outliers hidden)")
    plt.xlabel("accommodates")
    plt.ylabel("Price (EUR)")
    save("08_price_vs_accommodates.png")


def correlation_heatmap(df):
    cols = ["price", "accommodates", "bedrooms", "bathrooms", "beds",
            "amenities_count", "minimum_nights", "availability_365",
            "number_of_reviews", "review_scores_rating", "reviews_per_month",
            "host_listings_count", "host_tenure_years", "price_per_person"]
    corr = df[cols].corr()
    plt.figure(figsize=(9, 7.5))
    plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar()
    plt.xticks(range(len(cols)), cols, rotation=90)
    plt.yticks(range(len(cols)), cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            plt.text(j, i, "%.1f" % corr.iloc[i, j], ha="center", va="center", fontsize=6)
    plt.title("Correlation heatmap")
    save("09_correlation_heatmap.png")
    return corr["price"].drop("price").sort_values()


def superhost_comparison(df):
    d = df.dropna(subset=["host_is_superhost"])
    g = d.groupby("host_is_superhost").agg(
        median_price=("price", "median"), avg_rating=("review_scores_rating", "mean"))
    fig, ax = plt.subplots(1, 2, figsize=(8, 4))
    g["median_price"].plot.bar(ax=ax[0], rot=0, color=["#c0504d", "#4f81bd"])
    ax[0].set_title("Median price (EUR)")
    g["avg_rating"].plot.bar(ax=ax[1], rot=0, color=["#c0504d", "#4f81bd"])
    ax[1].set_title("Average rating")
    ax[1].set_ylim(4, 5)
    for a in ax:
        a.set_xlabel("")
    save("10_superhost_comparison.png")


def host_type(df):
    plt.figure(figsize=(6, 4.5))
    ax = df["host_type"].value_counts().plot.bar(rot=0, color="#4bacc6")
    ax.bar_label(ax.containers[0])
    plt.title("Single vs multi-listing hosts")
    plt.ylabel("Listings")
    save("11_host_type.png")


def availability(df):
    plt.figure(figsize=(8, 4.5))
    plt.hist(df["availability_365"], bins=36, color="#9bbb59")
    plt.title("Availability (days open for booking in the next year)")
    plt.xlabel("availability_365")
    plt.ylabel("Listings")
    save("12_availability.png")


def reviews_over_time(df):
    s = df["last_review_month"].dropna().value_counts().sort_index().tail(36)
    plt.figure(figsize=(10, 4.5))
    plt.plot(s.index, s.values, marker="o", ms=3)
    plt.xticks(rotation=90, fontsize=7)
    plt.title("Listings by month of last review (last 36 months)")
    plt.ylabel("Listings")
    save("13_reviews_over_time.png")


def amenities_vs_price(df):
    d = df[df["price"] <= 500]
    m, b = np.polyfit(d["amenities_count"], d["price"], 1)
    x = np.linspace(d["amenities_count"].min(), d["amenities_count"].max(), 50)
    plt.figure(figsize=(8, 4.5))
    plt.scatter(d["amenities_count"], d["price"], s=4, alpha=0.25)
    plt.plot(x, m * x + b, color="red", label="trend")
    plt.legend()
    plt.title("Amenities vs price (price up to 500)")
    plt.xlabel("amenities_count")
    plt.ylabel("Price (EUR)")
    save("14_amenities_vs_price.png")


def price_map(df):
    d = df[df["price"] <= 300]
    plt.figure(figsize=(8, 6))
    sc = plt.scatter(d["longitude"], d["latitude"], c=d["price"], s=4, cmap="viridis")
    plt.colorbar(sc, label="Price (EUR)")
    plt.title("Price map of Berlin (price up to 300)")
    plt.xlabel("longitude")
    plt.ylabel("latitude")
    save("15_price_map.png")


def run_eda():
    df = load_data()
    print("Loaded", df.shape)
    data_overview(df)
    for fn in (price_distribution, price_by_room_type, listings_per_district,
               price_by_district, room_type_share, price_category_counts,
               rating_distribution, price_vs_accommodates, correlation_heatmap,
               superhost_comparison, host_type, availability, reviews_over_time,
               amenities_vs_price, price_map):
        fn(df)
    print("EDA finished. Plots are in", OUT)


if __name__ == "__main__":
    run_eda()
