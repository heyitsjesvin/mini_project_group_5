# Berlin Airbnb Listings - ETL Pipeline

[![CI](https://github.com/<LEAD-USERNAME>/Berlin_Airbnb_ETL/actions/workflows/ci.yml/badge.svg)](https://github.com/<LEAD-USERNAME>/Berlin_Airbnb_ETL/actions)

## Objective
Build an ETL pipeline that turns the raw Inside Airbnb Berlin listings file
(14,187 rows x 79 columns) into an analysis-ready dataset and a set of reports for future
Data Science projects.

## Data source
Inside Airbnb, Berlin `listings.csv` (scraped 20-21 June 2025). Structured CSV, public.
Full answers (why chosen, contents, format, update frequency): [docs/DATASET_DESCRIPTION.md](docs/DATASET_DESCRIPTION.md).

## ETL workflow
```
Data Source -> Extract -> Validate/Clean -> Transform -> Generate Reports -> Load
```
Diagram and ownership: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Project structure
```
Berlin_Airbnb_ETL/
├── raw_data/        original CSV (+ raw copy created by extract())
├── reports/         10 report CSV files
├── screenshots/     screenshots of the run
├── output/          final analysis-ready dataset
├── etl/             one module per team member
├── tests/           one test file per member
├── docs/            architecture, dataset description, git workflow, task cards
├── pipeline.py      extract(), transform(), load(), run_etl_pipeline()
├── check_member.py  self-check for each member
├── README.md
└── requirements.txt
```

## How to run
```
pip install -r requirements.txt
python pipeline.py
```
Run the tests: `pip install -r requirements-dev.txt`, then `flake8 .` and `pytest`.

## List of transformations
| # | Transformation | Why it was necessary | Owner |
|---|---|---|---|
| T1 | Remove duplicate listing ids | Each listing must be counted once | Member 1 |
| T2 | Keep 32 of 79 columns, rename | Drop URLs and long text; clearer names | Member 1 |
| T3 | Convert data types ($ price, % rates, t/f, dates) | Text cannot be used for calculations | Member 1 |
| T4 | Standardize text | Spaces/capitalisation would split groups | Member 1 |
| T5 | Handle missing values | 35% of rows have no price -> dropped; room numbers filled by room-type median; reviews_per_month 0 | Member 2 |
| T6 | Remove invalid / outlier rows | Prices up to EUR 50,000, minimum nights over a year, points outside Berlin | Member 3 |
| T7 | Round numbers | Consistent precision | Member 3 |
| -  | Validation checks | Stop the pipeline if a rule is still broken | Member 3 |
| T8 | `price_per_person` | Fair price comparison between small and large listings | Member 4 |
| T9 | `price_category` | Budget / Standard / Premium / Luxury groups | Member 4 |
| T10 | `host_tenure_years`, `host_type` | Host experience and single vs multi-listing | Member 4 |
| T11 | `amenities_count` | Turn JSON text into a usable number | Member 4 |
| T12 | `has_reviews`, `rating_category`, review month/year | Group ratings, split dates | Member 4 |
| T13 | `availability_level` | Low / Medium / High booking availability | Member 4 |
| T14 | `price_rank_in_district` + sorting | Ranking and ordered output | Member 4 |

Result: 14,187 x 79 -> 9,133 x 42.

## Reports generated (`reports/`)
`cleaned_data`, `summary_statistics`, `district_report`, `room_type_price_report`,
`top10_expensive_listings`, `bottom10_cheapest_listings`, `top10_rated_listings`,
`superhost_report`, `monthly_last_review_report`, `affordable_top_rated_homes`.
The final dataset is saved as `output/berlin_airbnb_analysis_ready.csv`.

## Team
| Member | Name | GitHub | Part |
|---|---|---|---|
| 1 (lead) |  |  | Extract + structural cleaning |
| 2 |  |  | Missing values |
| 3 |  |  | Invalid values, outliers, validation |
| 4 |  |  | Feature engineering |
| 5 |  |  | Reports and load |

How we collaborate: [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md).

## Challenges faced
- 35% of listings had no price.
- Price stored as text; extreme outliers (up to EUR 50,000).
- Amenities stored as JSON text inside a CSV cell.
- Five people working on one pipeline without overwriting each other.

## Learning outcomes
ETL design, pandas cleaning and feature engineering, modular Python, unit testing,
continuous integration, Git branching and pull requests.

## Future improvements
Download directly from the Inside Airbnb URL, use the calendar and reviews files, load into a
SQL database, add logging, build a dashboard.

## Licence
Code: MIT (see [LICENSE](LICENSE)). Check the dataset's own licence before redistributing the data.
