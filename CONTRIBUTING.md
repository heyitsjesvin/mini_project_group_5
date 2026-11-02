# Contributing

This is a five-person team project. These rules keep everyone's work from colliding.

## Golden rules
1. **Never push directly to `main`.** Work on your own branch and open a pull request.
2. **Edit only your own file(s)** in `etl/`. If you think another file needs a change, tell the lead.
3. **Merge order is 1 -> 2 -> 3 -> 4 -> 5.** Each stage uses the output of the previous one.
4. **One purpose per commit**, with a clear message.

## Branch names
| Member | Branch |
|---|---|
| 1 | `feature/member1-extract-and-structure` |
| 2 | `feature/member2-missing-values` |
| 3 | `feature/member3-invalid-and-outliers` |
| 4 | `feature/member4-features` |
| 5 | `feature/member5-reports-and-load` |
| Lead, final reports | `docs/final-reports` |

## Commit messages
Start with a type: `feat:` new code, `fix:` bug fix, `docs:` documentation, `test:` tests, `chore:` setup.
Example: `feat: add missing value handling (T5)`

## Before every pull request
```
flake8 .
pytest
python check_member.py N      # N = your member number
```
All three must pass. Then open the pull request and fill in the template.

## Code style
- Python 3.11 or newer, PEP 8, lines up to 100 characters (checked by flake8).
- Every function has a short docstring that says what it does and why.
- Print one short line per transformation so the console output documents the run.
