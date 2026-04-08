# Data Availability Statement

**Project:** Cross-platform audience reactions to the Break 50 × Trump episode  
**Course:** KIN 7518 — Social Issues in Sport  
**Repository:** `b50-comment-analysis`

---

## What This Document Explains

This file explains why raw social-media comment data are not included in this
repository and what materials are available in their place.

---

## Why Raw Data Are Not Published

Raw comment data collected from YouTube, Instagram, and X (formerly Twitter)
are **not published** in this repository for the following reasons:

### 1. Platform Terms of Service

Each platform's developer or scraping terms of service restricts redistribution
of user-generated content. Publishing raw comment text collected from these
platforms — even if the comments are publicly visible — may violate those terms.

| Platform | Relevant policy |
|---|---|
| YouTube | YouTube Terms of Service §5, YouTube API Services Terms of Service |
| Instagram / Meta | Meta Platform Terms, Instagram Community Guidelines |
| X (Twitter) | X Developer Agreement and Policy, Section 4 (Data redistribution) |

### 2. Research Ethics and Participant Privacy

Although the comments analysed in this project were posted publicly, the
commenters did not know their posts would be part of an academic study.
Publishing row-level data — even without names — could enable re-identification
of individuals through comment text, timing, or cross-platform linkage.

This project follows the **ethical principle of minimal data exposure**:
only the aggregated, anonymized outputs necessary to support reproducibility
are shared publicly.

### 3. Username and User-ID Protection

The raw files contain usernames and numeric user IDs that could be used to
identify or track individual commenters. These fields are **never published**
in any form.

---

## What IS Available in This Repository

The following materials are safe to share and are included in the repository:

| File / Folder | Description |
|---|---|
| `codebook/keywords.txt` | All four keyword lexicons (golf, political, supportive, resistant) with full term lists and counts |
| `tables/01_platform_counts.csv` | Total comment counts by platform |
| `tables/02_frame_overall.csv` | Frame distribution across full dataset |
| `tables/03_frame_by_platform.csv` | Frame distribution by platform |
| `tables/04_stance_overall.csv` | Stance distribution across full dataset |
| `tables/05_stance_by_platform.csv` | Stance distribution by platform |
| `tables/06_engagement_by_frame.csv` | Median and mean engagement by frame, within platform |
| `tables/07_engagement_by_stance.csv` | Median and mean engagement by stance, within platform |
| `tables/08_top10pct_high_engagement.csv` | Aggregated summary of top-10% engagement comments by frame/stance — **no comment text or usernames** |
| `figures/fig1_frame_by_platform.png` | Stacked bar: frame distribution by platform |
| `figures/fig2_engagement_by_frame.png` | Grouped bar: median engagement by frame |
| `figures/fig3_keyword_bar.png` | Horizontal bar: top supportive vs resistant keywords |
| `scripts/` | All five reproducible Python analysis scripts |
| `docs/methods_summary.md` | Auto-generated academic methods narrative |

---

## How to Obtain the Raw Data

The raw Excel files are available to course group members only.
Contact the Data & Classification Lead (Paul Son) or the course instructor.

Files required:

```
data/raw/B50_YT_COMMENT.xlsx    (45,623 comments — YouTube)
data/raw/B50_INS_COMMENT.xlsx   (11,833 comments — Instagram)
data/raw/B50_X_COMMENT.xlsx     (1,008 comments — X)
```

Place them in `data/raw/` before running `python run_all.py`.

---

## Data-Sharing Principles Applied

This project follows *minimal necessary data exposure* principles consistent
with the Association of Internet Researchers (AoIR) ethical guidelines for
research on publicly available social media data (Franzke et al., 2020).

> Franzke, A. S., Bechmann, A., Zimmer, M., Ess, C., & the Association of
> Internet Researchers. (2020). *Internet Research: Ethical Guidelines 3.0.*
> <https://aoir.org/reports/ethics3.pdf>

---

*Last updated: April 2026*
