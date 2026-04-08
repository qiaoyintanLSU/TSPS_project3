# Cross-Platform Audience Reactions to the Break 50 × Trump Episode

**Course:** KIN 7518 — Social Issues in Sport  
**Team:** TSPS Group (Paul Son · Qiaoyin Tan · Lauryn Porter · Jolyn Seow)  
**Platforms analysed:** YouTube · Instagram · X (formerly Twitter)  
**Status:** Exploratory analysis — awaiting manual inter-rater validation

> **Data notice:** Raw social-media comment data are not included in this
> repository. See [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md) for the
> full data-sharing statement.

---

## Project Overview

This repository contains all code, keyword codebook, aggregated summary
tables, figures, and documentation for a course research project examining
how audiences across three platforms reacted to Bryson DeChambeau's
*Break 50* golf video featuring former U.S. President Donald Trump (2024).

The project addresses three research questions:

| # | Research Question |
|---|---|
| **RQ1** | How do commenters frame the episode — as golf content, political content, or a hybrid of both — across YouTube, Instagram, and X? |
| **RQ2** | Which framing receives the strongest within-platform social validation (likes and replies)? |
| **RQ3** | What rhetorical strategies do commenters use to normalize or resist the presence of Trump and politics in a golf-media context? |

---

## Repository Structure

```
project-root/
│
├── codebook/
│   └── keywords.txt              # All four keyword lexicons (golf, political,
│                                 #   supportive, resistant) — safe to share
│
├── docs/
│   ├── methods_summary.md        # Auto-generated academic methods narrative
│   ├── P3_PLAN_REVISED.md        # Full revised research plan
│   └── P3_PLAN_TSPS.md           # Original research plan (v1)
│
├── figures/
│   ├── fig1_frame_by_platform.png
│   ├── fig2_engagement_by_frame.png
│   └── fig3_keyword_bar.png
│
├── scripts/
│   ├── 01_load_clean.py          # Load + standardize + clean → unified CSV
│   ├── 02_classify.py            # Lexicon coding → frame + stance variables
│   ├── 03_descriptive_stats.py   # 8 summary tables + engagement percentiles
│   ├── 04_visualize.py           # 3 figures (PNG)
│   └── 05_methods_summary.py     # Auto-generates docs/methods_summary.md
│
├── tables/
│   ├── 01_platform_counts.csv
│   ├── 02_frame_overall.csv
│   ├── 03_frame_by_platform.csv
│   ├── 04_stance_overall.csv
│   ├── 05_stance_by_platform.csv
│   ├── 06_engagement_by_frame.csv
│   ├── 07_engagement_by_stance.csv
│   └── 08_top10pct_high_engagement.csv  # Aggregated counts only — no row data
│
├── data/
│   └── raw/
│       └── .gitkeep              # Placeholder only — raw Excel files excluded
│
├── run_all.py                    # Master pipeline: runs all 5 scripts in order
├── requirements.txt              # Python dependencies
├── .gitignore
├── DATA_AVAILABILITY.md          # Data-sharing statement
├── CONTRIBUTING.md               # Contributor guide for group members
├── LICENSE                       # MIT (code only)
└── README.md
```

---

## How to Reproduce the Analysis

### 1. Prerequisites

- Python 3.10 or later  
- `pip`

### 2. Clone the repository

```bash
git clone https://github.com/<your-org>/b50-comment-analysis.git
cd b50-comment-analysis
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Obtain the raw data

Raw Excel files are not included in this repository.
Contact the course instructor or the Data & Classification Lead (Paul Son)
to receive the three source files:

```
data/raw/B50_YT_COMMENT.xlsx
data/raw/B50_INS_COMMENT.xlsx
data/raw/B50_X_COMMENT.xlsx
```

Place them in `data/raw/` before running any scripts.

### 5. Run the full pipeline

```bash
python run_all.py
```

Or run each step individually:

```bash
python scripts/01_load_clean.py
python scripts/02_classify.py
python scripts/03_descriptive_stats.py
python scripts/04_visualize.py
python scripts/05_methods_summary.py
```

### 6. Outputs

| Output | Location | Published in repo? |
|---|---|---|
| Keyword codebook | `codebook/keywords.txt` | ✅ Yes |
| Aggregated summary tables | `tables/*.csv` | ✅ Yes |
| Figures | `figures/*.png` | ✅ Yes |
| Methods summary | `docs/methods_summary.md` | ✅ Yes |
| Unified comment-level CSV | `data/cleaned/B50_unified_comments.csv` | ❌ No |
| Classified comment-level CSV | `data/cleaned/B50_classified_comments.csv` | ❌ No |
| Raw Excel files | `data/raw/*.xlsx` | ❌ No |

---

## Manual Validation — Where Human Review Is Needed

Lexicon-based classification is a first-pass tool.
Three checkpoints require manual review before results are finalised:

1. **After `02_classify.py`** — Draw a stratified random sample of ~150
   comments (50 per platform) and independently code frame and stance.
   Compute Cohen's kappa; target ≥ 0.70 before proceeding.

2. **Priority review targets** — `hybrid` frame comments and `contested`
   stance comments carry the highest classification ambiguity.
   Comments that mention "Trump" descriptively (not evaluatively) may be
   incorrectly labelled as `political`.

3. **After `04_visualize.py`** — Inspect all three figures for correctness
   of labels, percentages, and colour coding.

---

## Ethical Handling of Public Comments

- **No individual profiling.** Usernames are used only for deduplication
  and are never reported.
- **No row-level data published.** Comment-level CSVs are excluded from
  the repository.
- **Anonymized excerpts only.** Any comment text quoted in reports is
  presented as a brief, paraphrased or anonymized excerpt.
- **Analytical framing.** All findings are presented descriptively.
  The project does not endorse or critique any political position.

See [`DATA_AVAILABILITY.md`](DATA_AVAILABILITY.md) for the full statement.

---

## Citation

> TSPS Group. (2026). *Cross-platform audience reactions to the Break 50 × Trump episode: A lexicon-based framing and stance analysis.* Course project, KIN 7518 Social Issues in Sport.

---

## License

Analysis code: [MIT License](LICENSE).  
Cleaned data and outputs: not licensed for redistribution.  
Raw comment data: subject to each platform's terms of service.
