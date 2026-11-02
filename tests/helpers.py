"""Shared test helpers: a small fake dataset and skip logic for unfinished members."""
import unittest

import pandas as pd

from etl import config
from etl.common import is_stub, run_stages


def needs(*members):
    """Skip a test class while any of the given members is still a placeholder."""
    waiting = [n for n in members if is_stub(n)]
    return unittest.skipIf(bool(waiting), f"waiting for member(s) {waiting}")


def _base_row(row_id):
    return {
        "id": row_id, "name": "Cozy Flat", "host_id": 100 + row_id, "host_name": "Anna",
        "host_since": "2015-03-01", "host_response_rate": "95%", "host_acceptance_rate": "90%",
        "host_is_superhost": "t", "host_identity_verified": "t",
        "neighbourhood_group_cleansed": "Mitte", "neighbourhood_cleansed": "Brunnenstr. Sued",
        "latitude": 52.53, "longitude": 13.40, "property_type": "Entire rental unit",
        "room_type": "Entire home/apt", "accommodates": 2, "bathrooms": 1.0, "bedrooms": 1.0,
        "beds": 1.0, "amenities": '["Wifi", "Kitchen", "Heating"]', "price": "$100.00",
        "minimum_nights": 2, "availability_365": 200, "number_of_reviews": 10,
        "first_review": "2018-01-10", "last_review": "2025-03-02",
        "review_scores_rating": 4.8, "reviews_per_month": 0.5, "instant_bookable": "f",
        "calculated_host_listings_count": 1, "estimated_occupancy_l365d": 90,
        "estimated_revenue_l365d": 9000, "listing_url": "https://example.com/rooms/1",
    }


def raw_sample():
    """11 rows in the ORIGINAL Inside Airbnb format, with deliberate problems:

    id 1 ok | id 2 price $1,250.00 (outlier) | id 3 no price | id 4 missing room numbers
    id 5 outside Berlin | id 6 minimum_nights 1125 | id 7 no reviews | id 8 messy text
    id 1 again (duplicate) | id 10 bad amenities text | id 11 low rating
    """
    rows = [_base_row(i) for i in (1, 2, 3, 4, 5, 6, 7, 8, 1, 10, 11)]
    rows[1]["price"] = "$1,250.00"
    rows[2]["price"] = None
    rows[3].update({"bedrooms": None, "beds": None, "bathrooms": None,
                    "room_type": "Private room", "price": "$50.00", "accommodates": 1})
    rows[4]["latitude"] = 48.0
    rows[5]["minimum_nights"] = 1125
    rows[6].update({"number_of_reviews": 0, "first_review": None, "last_review": None,
                    "review_scores_rating": None, "reviews_per_month": None,
                    "price": "$30.00", "host_is_superhost": None, "availability_365": 10})
    rows[7].update({"name": "  Sunny   Room ", "price": "$75.50",
                    "neighbourhood_group_cleansed": "  friedrichshain-kreuzberg "})
    rows[9].update({"amenities": "not json", "price": "$200.00", "host_since": "2010-06-15",
                    "review_scores_rating": 4.95, "number_of_reviews": 50,
                    "calculated_host_listings_count": 3, "host_is_superhost": "f"})
    rows[10].update({"accommodates": 4, "price": "$160.00", "review_scores_rating": 3.5,
                     "number_of_reviews": 25, "availability_365": 300})
    return pd.DataFrame(rows)


def stage_df(upto):
    """The sample data after transform stages 1..upto."""
    return run_stages(raw_sample(), upto)


def real_data_available():
    import os
    return os.path.exists(config.SOURCE_FILE)
