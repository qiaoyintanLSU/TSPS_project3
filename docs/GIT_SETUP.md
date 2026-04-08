# Git Setup Guide

**Project:** Cross-platform audience reactions to the Break 50 × Trump episode  
**Course:** KIN 7518 — Social Issues in Sport

This guide walks through initialising the repository, connecting to GitHub,
and sharing it with your group members.

---

## Step 1 — Verify your local setup

```bash
# Check that git is installed
git --version

# Set your identity (do this once on each machine)
git config --global user.name  "Your Name"
git config --global user.email "your@email.com"
```

---

## Step 2 — Initialise the repository locally

Navigate to the project folder in your terminal, then:

```bash
cd "C:\Users\qtan1\Desktop\Project_3"

git init
git branch -M main
```

---

## Step 3 — Check what will be staged (dry run — do this before every commit)

```bash
# See which files git sees as untracked or changed
git status

# Double-check that no raw data or row-level CSVs appear in the list.
# You should NOT see:
#   data/raw/*.xlsx
#   data/cleaned/B50_unified_comments.csv
#   data/cleaned/B50_classified_comments.csv
# If you do, stop and check your .gitignore before proceeding.
```

---

## Step 4 — Add safe files to staging

```bash
# Add everything that is not excluded by .gitignore
git add .

# Verify the staged list looks correct
git status
```

The following should be staged:

```
.gitignore
README.md
DATA_AVAILABILITY.md
CONTRIBUTING.md
LICENSE
requirements.txt
run_all.py
codebook/keywords.txt
docs/methods_summary.md
docs/P3_PLAN_REVISED.md
docs/P3_PLAN_TSPS.md
scripts/01_load_clean.py
scripts/02_classify.py
scripts/03_descriptive_stats.py
scripts/04_visualize.py
scripts/05_methods_summary.py
scripts/06_safe_table08.py
tables/01_platform_counts.csv
tables/02_frame_overall.csv
tables/03_frame_by_platform.csv
tables/04_stance_overall.csv
tables/05_stance_by_platform.csv
tables/06_engagement_by_frame.csv
tables/07_engagement_by_stance.csv
tables/08_top10pct_high_engagement.csv
figures/fig1_frame_by_platform.png
figures/fig2_engagement_by_frame.png
figures/fig3_keyword_bar.png
data/raw/.gitkeep
```

---

## Step 5 — Initial commit

```bash
git commit -m "init: initial project commit — scripts, codebook, tables, figures, docs"
```

---

## Step 6 — Create a GitHub repository

1. Go to <https://github.com> and log in.
2. Click **New** (top-left green button).
3. Name the repository, e.g. `b50-comment-analysis`.
4. Set visibility to **Private** (recommended for a course project).
5. **Do not** initialise with a README or .gitignore — you already have those.
6. Click **Create repository**.

---

## Step 7 — Connect your local repo to GitHub

GitHub will show you a URL after creating the repo. Use it here:

```bash
git remote add origin https://github.com/<your-username>/b50-comment-analysis.git
git push -u origin main
```

---

## Step 8 — Invite group members as collaborators

1. On GitHub, go to your repository → **Settings** → **Collaborators and teams**.
2. Click **Add people** and enter each group member's GitHub username or email.
3. Set their role to **Write** (they can push) or **Read** (browse only).

Recommended access levels:

| Member | GitHub role |
|---|---|
| Paul Son | Write |
| Qiaoyin Tan | Write |
| Lauryn Porter | Write |
| Jolyn Seow | Write |

---

## Step 9 — Daily workflow for group members

```bash
# Always pull before you start working
git pull origin main

# Make your changes, then stage only safe files
git add scripts/02_classify.py
git add codebook/keywords.txt
git add tables/

# Write a descriptive commit message
git commit -m "fix: extend resistant lexicon with 'boycott'; regenerate tables"

# Push
git push origin main
```

---

## Step 10 — Useful commands

```bash
# See the commit history
git log --oneline -10

# See what changed in a specific file
git diff scripts/02_classify.py

# Undo staged changes (before committing)
git restore --staged <file>

# Discard local edits (careful — this is permanent)
git restore <file>

# See all remote branches
git branch -r
```

---

## Troubleshooting

**"Permission denied" when pushing:**  
Check that you were added as a collaborator and that you are authenticated.
Use `git remote -v` to verify the remote URL.

**Accidentally staged a data file:**  
```bash
git restore --staged data/cleaned/B50_unified_comments.csv
```
Then update your `.gitignore` so it cannot happen again.

**Merge conflict:**  
Pull the latest changes, resolve conflicts in the affected file,
stage the resolved file, and commit with a `merge:` prefix message.
