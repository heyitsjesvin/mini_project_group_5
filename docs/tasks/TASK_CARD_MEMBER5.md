# Task Card - Member 5: Reports and load

| | |
|---|---|
| **Your file** | `etl/member5_reports_and_load.py` |
| **Your branch** | `feature/member5-reports-and-load` |
| **Start after** | Members 1, 2, 3 and 4 merged |
| **You provide** | `generate_reports(df)` and `load(df, reports)` |

## What your code does
- 10 reports: cleaned data, summary statistics, district, room type x price category, top 10 expensive, bottom 10 cheapest, top 10 rated, superhost comparison, monthly report, filtered report
- load(): save every report to reports/ and the final dataset to output/

## You are finished when
1. `flake8 .` prints nothing
2. `pytest` ends with **36 passed, 0 skipped** (the skipped tests wait for later members)
3. `python check_member.py 5` ends with `PIPELINE FINISHED ... 14,187 x 79 -> clean 9,133 x 42`
4. You took a screenshot of step 3
5. Your pull request is open, the CI check is green, and the lead merged it

## You will be asked to explain
What each report shows, why top-rated listings need at least 20 reviews, and how `groupby` + `agg` work.

## Steps
Follow `docs/GIT_WORKFLOW.md`, Part B. Copy only your own file into `etl/`.

Note: `check_member.py 5` creates files in `reports/` and `output/`. `git status` will show them as untracked. Do not add them; the lead uploads them at the end.
