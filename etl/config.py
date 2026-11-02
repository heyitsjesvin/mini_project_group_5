"""Shared settings used by every module (maintained by the team lead)."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw_data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SOURCE_FILE = os.path.join(RAW_DIR, "listings_berlin.csv")
RAW_COPY_FILE = os.path.join(RAW_DIR, "listings_berlin_raw_copy.csv")
FINAL_FILE = os.path.join(OUTPUT_DIR, "berlin_airbnb_analysis_ready.csv")

# Scrape date of the dataset (used for host tenure)
REFERENCE_DATE = "2025-06-21"

# The 32 columns we keep from the original 79
COLUMNS_TO_KEEP = [
    "id", "name", "host_id", "host_name", "host_since",
    "host_response_rate", "host_acceptance_rate",
    "host_is_superhost", "host_identity_verified",
    "neighbourhood_group_cleansed", "neighbourhood_cleansed",
    "latitude", "longitude", "property_type", "room_type",
    "accommodates", "bathrooms", "bedrooms", "beds", "amenities",
    "price", "minimum_nights", "availability_365",
    "number_of_reviews", "first_review", "last_review",
    "review_scores_rating", "reviews_per_month", "instant_bookable",
    "calculated_host_listings_count",
    "estimated_occupancy_l365d", "estimated_revenue_l365d",
]

RENAME_MAP = {
    "neighbourhood_group_cleansed": "district",
    "neighbourhood_cleansed": "neighbourhood",
    "calculated_host_listings_count": "host_listings_count",
    "estimated_occupancy_l365d": "est_occupancy_days_365",
    "estimated_revenue_l365d": "est_revenue_365",
}

# Validation limits (Member 3)
MIN_PRICE = 1
MAX_PRICE = 1000            # above the 99th percentile; larger values are outliers
MAX_MIN_NIGHTS = 365
BERLIN_LAT = (52.3, 52.7)
BERLIN_LON = (13.0, 13.8)
