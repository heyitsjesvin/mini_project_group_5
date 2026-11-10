# EDA findings (Berlin Airbnb, 9,133 cleaned listings)

Numbers come from `output/berlin_airbnb_analysis_ready.csv`. Rewrite in your own words before submitting.

| Plot | Finding |
|---|---|
| 00 Missing values | Only 11 columns still have gaps. The biggest are the review columns (2,045 listings, 22%, have no review yet), host_response_rate (1,121) and host_acceptance_rate (962). They were left empty on purpose: "not rated" is not a score of 0. |
| 01 Price distribution | Prices are right-skewed (skewness 2.85). The median is EUR 108 and the mean EUR 134.5; the top 1% of listings cost more than EUR 509, up to the EUR 1,000 cap. |
| 02 Price by room type | Entire homes (median EUR 125) cost almost double private rooms (EUR 66). Shared rooms are cheapest (EUR 38); the 83 hotel rooms are dearest (EUR 189). |
| 03 Listings per district | Mitte (2,026), Friedrichshain-Kreuzberg (1,910) and Pankow (1,381) hold more than half of all listings. Marzahn-Hellersdorf has only 105. |
| 04 Median price by district | Mitte is the most expensive (EUR 134), Reinickendorf the cheapest (EUR 69). The central districts cost more than the outer ones. |
| 05 Room type share | Entire homes are 73.6% of listings, private rooms 24.4%. Shared and hotel rooms together are about 2%. |
| 06 Price categories | Standard (3,610) and Premium (3,066) are the largest groups; Luxury is the smallest (871). |
| 07 Rating distribution | Ratings are concentrated near the top: median 4.85, and 87.7% of rated listings score 4.5 or more. Ratings therefore separate listings poorly. |
| 08 Price vs guests | Median price rises steadily with capacity, from EUR 56 for 1 guest to EUR 235 for 8 guests. |
| 09 Correlation heatmap | Price correlates most with accommodates (0.53), bedrooms (0.47), beds (0.39) and bathrooms (0.29). Amenities count is weaker (0.24). Ratings and review counts have almost no link to price (about 0). Minimum nights is mildly negative (-0.20). |
| 10 Superhost comparison | Superhosts (2,854) charge a little more (median EUR 112 vs 105) and score clearly higher (average 4.87 vs 4.67). |
| 11 Host type | 54.7% of listings belong to multi-listing hosts, so the market is not just individual hosts. |
| 12 Availability | Median availability is 227 days a year; 28.6% of listings are open 300+ days and only 1.1% are fully blocked. |
| 13 Reviews over time | Most last reviews are recent: 5,407 listings were last reviewed in 2025, with a sharp rise in May and June 2025. This reflects when the data was scraped, so do not read it as a booking trend. |
| 14 Amenities vs price | A weak positive trend (correlation 0.27 for prices up to EUR 500). More amenities go with a somewhat higher price, but it is far from a strong predictor. |
| 15 Price map | Listings are densest in the centre. Price differences are hard to see because the points overlap; the pattern is clearer in the district chart (04). |

## Caveats
- Prices were capped at EUR 1,000 in the ETL, and about 5,000 listings without a price were dropped, so these figures describe listings that show a price.
- Correlation is not causation: bigger places cost more, and that is the main driver of price here.
