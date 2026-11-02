# Task Card - Member 3: Invalid values, outliers and validation

| | |
|---|---|
| **Your file** | `etl/member3_invalid_and_outliers.py` |
| **Your branch** | `feature/member3-invalid-and-outliers` |
| **Start after** | Members 1 and 2 merged |
| **You provide** | `remove_invalid_and_outliers(df)` |

## What your code does
- T6 remove invalid and outlier rows (price outside 1-1000, minimum nights over 365, coordinates outside Berlin, ...)
- T7 round numeric columns
- Validation checks that raise an error if a rule is still broken

## You are finished when
1. `flake8 .` prints nothing
2. `pytest` ends with **20 passed, 16 skipped** (the skipped tests wait for later members)
3. `python check_member.py 3` ends with `CHECK OK after Member 3: 9,133 rows x 32 columns`
4. You took a screenshot of step 3
5. Your pull request is open, the CI check is green, and the lead merged it

## You will be asked to explain
Why the price limit is 1000 (99th percentile is about 660, maximum is 50,000) and what the validation step protects against.

## Steps
Follow `docs/GIT_WORKFLOW.md`, Part B. Copy only your own file into `etl/`.
