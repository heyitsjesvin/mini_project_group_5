# Task Card - Member 4: Feature engineering

| | |
|---|---|
| **Your file** | `etl/member4_features.py` |
| **Your branch** | `feature/member4-features` |
| **Start after** | Members 1, 2 and 3 merged |
| **You provide** | `add_features(df)` |

## What your code does
- T8 price_per_person
- T9 price_category
- T10 host_tenure_years and host_type
- T11 amenities_count (parse JSON text)
- T12 has_reviews, rating_category, last_review_year/month
- T13 availability_level
- T14 price_rank_in_district and sorting

## You are finished when
1. `flake8 .` prints nothing
2. `pytest` ends with **27 passed, 9 skipped** (the skipped tests wait for later members)
3. `python check_member.py 4` ends with `CHECK OK after Member 4: 9,133 rows x 42 columns`
4. You took a screenshot of step 3
5. Your pull request is open, the CI check is green, and the lead merged it

## You will be asked to explain
How `pd.cut` creates categories, how the amenities JSON is parsed, and what a rank within a district means.

## Steps
Follow `docs/GIT_WORKFLOW.md`, Part B. Copy only your own file into `etl/`.
