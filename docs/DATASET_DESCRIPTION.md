# Dataset Description (Step 2)

| Question | Answer |
|---|---|
| **What is your data source?** | Inside Airbnb - Berlin `listings.csv` (public, independent project that publishes scraped Airbnb listing data for cities). Our file was scraped on 20-21 June 2025. |
| **Why did you choose it?** | *(Team: edit this in your own words.)* It is real, large and messy: prices stored as text (`$1,105.00`), percentages as text, 35% of listings without a price, extreme outliers, and amenities stored as JSON text. That gives plenty of meaningful cleaning and transformation work, and the cleaned data is useful for later price, review and neighbourhood analysis. |
| **What information does it contain?** | 14,187 listings x 79 columns: host details (since when, response rate, superhost), location (district, neighbourhood, latitude/longitude), property (room type, accommodates, bedrooms, beds, bathrooms, amenities), price and booking rules (minimum nights, availability), and reviews (count, rating scores, reviews per month, estimated occupancy and revenue). |
| **Structured, semi-structured or unstructured?** | Mostly **structured** (rows and columns). Some fields are **semi-structured** (`amenities` and `host_verifications` hold JSON-like lists inside a text cell), and `description` / `host_about` are free text (unstructured). |
| **What format is the data?** | CSV (comma separated, UTF-8). File size about 29 MB. |
| **How frequently is the data updated?** | Inside Airbnb publishes new scrapes for each city every few months, so the file is a snapshot. Check insideairbnb.com for the current release schedule. |

**Licence note:** the MIT licence of this repository covers the code only. Check the data licence on
insideairbnb.com before redistributing the dataset outside your course.
