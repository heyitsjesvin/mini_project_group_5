# Git Workflow - step by step, from the basics

Replace `<LEAD-USERNAME>` with the GitHub username of the team lead (Member 1) everywhere below.
Repository: `https://github.com/<LEAD-USERNAME>/Berlin_Airbnb_ETL`

## The basic ideas
- **GitHub**: a website that stores the project online so all five of you can work on it.
- **Repository (repo)**: the project folder on GitHub.
- **Branch**: your own copy of the project where you work without disturbing others. The main branch is `main`.
- **Commit**: a save point with a message.
- **Push**: upload your commits to GitHub.
- **Pull request (PR)**: "please review my branch and add it to `main`".
- **Merge**: your reviewed work becomes part of `main`.

Everyone works on **their own branch** and **their own file**. That is how five people avoid overwriting each other.

## Tools every member needs
1. **Git**: git-scm.com, install with default options.
2. **Python 3.11 or newer**: python.org (Windows: tick "Add Python to PATH").
3. A **GitHub account**.

Check in a terminal (Windows: "Git Bash"): `git --version` and `python --version`.

---

# Part A - Lead (Member 1): set up the repository

### A1. Unzip the main package
You get `Berlin_Airbnb_ETL/` (this is what you upload) and `member_code/` (**do not upload**; it holds everyone's finished code).

### A2. Create the empty repository on GitHub
1. Log in at github.com, click **+** (top right) -> **New repository**.
2. Name: `Berlin_Airbnb_ETL`.
3. Leave README, .gitignore and licence **unticked**. Click **Create repository**.

### A3. Invite the team
Repo -> **Settings -> Collaborators -> Add people**. Add each member's username. Each person must **accept the invitation email**, otherwise they cannot push.

### A4. Upload the starter project
Open a terminal **inside the `Berlin_Airbnb_ETL` folder** (Windows: right-click -> **Git Bash Here**) and run one line at a time:
```
git init -b main
git config user.name  "Your Name"
git config user.email "your-github-email@example.com"
git add .
git commit -m "chore: initial project scaffold"
git remote add origin https://github.com/<LEAD-USERNAME>/Berlin_Airbnb_ETL.git
git push -u origin main
```
A browser window may ask you to sign in to GitHub. Passwords do not work in the terminal; use the browser sign-in.

The upload includes the 29 MB dataset, so the first push can take a minute.

Refresh the repo page: you should see all files. Open the **Actions** tab: the first CI run should turn green (it passes with every test skipped, because every member file is still a placeholder).

### A5. Protect `main` (recommended)
**Settings -> Branches -> Add rule**, pattern `main`, tick **Require a pull request before merging**. On a private repo with a free plan this may be unavailable; then simply agree never to push to `main`.

### A6. Create one issue per member
**Issues -> New issue -> Member task**. Assign each member their task card (`docs/tasks/`).

### A7. Send the members their packages
Send **only their own zip** (`Member2_package.zip` to Member 2, ...), plus the repo link and this message:

> Accept the GitHub invitation, install Git and Python, unzip your package and follow Part B of GIT_WORKFLOW.md. Don't start until I tell you it is your turn.

Members start **in order 1 -> 2 -> 3 -> 4 -> 5**, because each stage needs the previous one.

---

# Part B - Every member (in order)

Replace `N` with your member number and use your own branch name from `CONTRIBUTING.md`.

### B1. Download the project
```
git clone https://github.com/<LEAD-USERNAME>/Berlin_Airbnb_ETL.git
cd Berlin_Airbnb_ETL
git config user.name  "Your Name"
git config user.email "your-github-email@example.com"
```
(The lead already has the folder and can skip this.)

### B2. Update before you start (Members 2-5)
```
git checkout main
git pull origin main
```

### B3. Install the libraries (first time only)
```
pip install -r requirements-dev.txt
```

### B4. Create your branch
| Member | Command |
|---|---|
| 1 | `git checkout -b feature/member1-extract-and-structure` |
| 2 | `git checkout -b feature/member2-missing-values` |
| 3 | `git checkout -b feature/member3-invalid-and-outliers` |
| 4 | `git checkout -b feature/member4-features` |
| 5 | `git checkout -b feature/member5-reports-and-load` |

### B5. Copy your code into the project
Unzip your package. Your file is in `memberN/etl/`. Copy **only that file** into the project's `etl/` folder and choose **Replace** (drag and drop, or from Git Bash: `cp ../path/to/memberN/etl/<file>.py etl/`).
Open the file and read it. You will be asked to explain it.

### B6. Check your work
```
flake8 .
pytest
python check_member.py N
```
- `flake8 .` prints nothing.
- `pytest` ends with the numbers on your task card (for example Member 1: `7 passed, 29 skipped`).
- `python check_member.py N` ends with `CHECK OK ...` (Member 5: `PIPELINE FINISHED ...`). **Take a screenshot.**

### B7. Save and upload your branch
```
git add etl
git status
git commit -m "feat: <what your module does>"
git push -u origin <your-branch-name>
```
`git status` must list **only your own file** as changed. If it lists other changed files, stop and ask the lead.
(Member 5 only: running `check_member.py 5` creates new files in `reports/` and `output/`. They appear as "untracked" in `git status`. That is normal - do **not** add them; the lead uploads them in Part D.)

### B8. Open the pull request
1. On GitHub click the yellow **Compare & pull request** banner.
2. Fill in the template and paste your screenshot.
3. Pick a reviewer on the right and click **Create pull request**.

---

# Part C - Lead: review and merge, in order

For Member 1, 2, 3, 4, 5:
1. **Pull requests** tab -> open the request -> **Files changed**: only their own file should appear.
2. Wait for the green tick from CI.
3. **Merge pull request -> Confirm merge**.
4. Tell the next member: "Merged. Run `git pull origin main` and start."

The number of passing tests in CI grows after each merge: 7, 14, 20, 27, then 36 (0 skipped).

---

# Part D - Final run and reports (lead)
After all five are merged:
```
git checkout main
git pull origin main
python pipeline.py
```
It ends with `PIPELINE FINISHED ... 14,187 x 79 -> clean 9,133 x 42`. Put the team's screenshots in `screenshots/`, then:
```
git checkout -b docs/final-reports
git add reports output screenshots
git commit -m "docs: add generated reports, final dataset and screenshots"
git push -u origin docs/final-reports
```
Open a pull request and merge it.

Last tasks: fill the **Team** table in `README.md`, replace `<LEAD-USERNAME>` in the README badge, and edit "Why did you choose it?" in `docs/DATASET_DESCRIPTION.md` in your own words. To get automatic review requests, edit `.github/CODEOWNERS` (replace the usernames and remove the leading `#`).

---

# Common problems
| Problem | Fix |
|---|---|
| `git` is not recognized | Install Git, close and reopen the terminal |
| Authentication failed | Sign in through the browser window; passwords don't work |
| Permission denied / 403 | The member has not accepted the invitation email |
| `remote origin already exists` | `git remote set-url origin https://github.com/<LEAD-USERNAME>/Berlin_Airbnb_ETL.git` |
| `NOT READY: ... still placeholders` | Earlier members are not merged yet: `git pull origin main` |
| `flake8` or `pytest` not found | `pip install -r requirements-dev.txt` |
| `git status` shows extra files | Stop; do not commit. Ask the lead |
| Merge conflict | You edited a file that is not yours. Ask the lead before doing anything |
| Not sure where you are | `git status` |
