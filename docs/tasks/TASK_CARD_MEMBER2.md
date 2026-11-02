# Task Card - Member 2: Missing values

| | |
|---|---|
| **Your file** | `etl/member2_missing_values.py` |
| **Your branch** | `feature/member2-missing-values` |
| **Start after** | Member 1 merged |
| **You provide** | `handle_missing_values(df)` |

## What your code does
- T5 handle missing values: drop rows with no price, fill bedrooms/beds/bathrooms with the room-type median, set reviews_per_month to 0 for unreviewed listings, keep review scores empty

## You are finished when
1. `flake8 .` prints nothing
2. `pytest` ends with **14 passed, 22 skipped** (the skipped tests wait for later members)
3. `python check_member.py 2` ends with `CHECK OK after Member 2: 9,183 rows x 32 columns`
4. You took a screenshot of step 3
5. Your pull request is open, the CI check is green, and the lead merged it

## You will be asked to explain
Why 5,004 rows without a price are dropped instead of filled, why the median (not the mean) is used, and why ratings are left empty.

## Steps
Follow `docs/GIT_WORKFLOW.md`, Part B. Copy only your own file into `etl/`.
