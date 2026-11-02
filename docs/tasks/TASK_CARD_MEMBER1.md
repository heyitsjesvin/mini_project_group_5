# Task Card - Member 1: Extract and structural cleaning

| | |
|---|---|
| **Your file** | `etl/member1_extract_and_structure.py` |
| **Your branch** | `feature/member1-extract-and-structure` |
| **Start after** | none (you go first) |
| **You provide** | `extract()` and `structural_cleaning(df)` |

## What your code does
- T1 remove duplicate listing ids
- T2 keep 32 of 79 columns and rename them
- T3 convert data types ($ price, % rates, t/f booleans, dates)
- T4 standardize text (spaces, capitalisation, missing names)

## You are finished when
1. `flake8 .` prints nothing
2. `pytest` ends with **7 passed, 29 skipped** (the skipped tests wait for later members)
3. `python check_member.py 1` ends with `CHECK OK after Member 1: 14,187 rows x 32 columns`
4. You took a screenshot of step 3
5. Your pull request is open, the CI check is green, and the lead merged it

## You will be asked to explain
Why we use `drop_duplicates(subset='id')`, how `'$1,105.00'` becomes `1105.0`, and why `t`/`f` become booleans.

## Steps
Follow `docs/GIT_WORKFLOW.md`, Part B. Copy only your own file into `etl/`.
