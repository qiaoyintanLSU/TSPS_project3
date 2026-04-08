"""
B50 Cross-Platform Comment Analysis
=====================================
Script:  05_methods_summary.py
Purpose: Generate a polished academic methods summary as a Markdown file.
         All numerical values are pulled from the actual output tables
         so the summary is reproducible and not hard-coded.

INPUT:   tables/ (CSV files from 03_descriptive_stats.py)
OUTPUT:  docs/methods_summary.md
"""

import pathlib
import pandas as pd
from datetime import date

BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
TABLES_DIR = BASE_DIR / "tables"
DOCS_DIR   = BASE_DIR / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# ── Load tables ───────────────────────────────────────────────────────────────
plat    = pd.read_csv(TABLES_DIR / "01_platform_counts.csv",    index_col=0, encoding="utf-8-sig")
f_ovr   = pd.read_csv(TABLES_DIR / "02_frame_overall.csv",      index_col=0, encoding="utf-8-sig")
f_plat  = pd.read_csv(TABLES_DIR / "03_frame_by_platform.csv",  index_col=0, encoding="utf-8-sig")
s_ovr   = pd.read_csv(TABLES_DIR / "04_stance_overall.csv",     index_col=0, encoding="utf-8-sig")

total_n = int(plat["n_comments"].sum())

# Pull key numbers safely
def get_n(df, idx, col="n"):
    try:
        return int(df.loc[idx, col])
    except Exception:
        return "N/A"

def get_pct(df, idx, col="pct"):
    try:
        return float(df.loc[idx, col])
    except Exception:
        return "N/A"

# ── Build methods text ────────────────────────────────────────────────────────
md = f"""# Methods Summary

*Generated automatically by `05_methods_summary.py` on {date.today()}.*
*All figures are exploratory and subject to manual validation.*

---

## Data Collection and Source Materials

This study analyzed audience comments collected from three social media
platforms — YouTube, Instagram, and X (formerly Twitter) — in response to
Bryson DeChambeau's *Break 50* episode featuring Donald Trump.
Comments were collected from publicly accessible posts and were supplied
as three platform-specific Microsoft Excel files
(`B50_YT_COMMENT.xlsx`, `B50_INS_COMMENT.xlsx`, `B50_X_COMMENT.xlsx`).

---

## Data Cleaning and Standardization

Prior to analysis, the three datasets were standardized into a single
comment-level dataset using a reproducible Python workflow (script
`01_load_clean.py`). Column names varied across platforms and were
harmonized to a unified schema comprising the following fields:
*platform*, *text*, *user*, *likes*, *replies*, *time*, *comment_id*,
and *post_id*. Where platform-specific columns lacked a direct equivalent
in the unified schema, the discrepancy was documented in the cleaning log.

Numeric fields (*likes*, *replies*) were coerced using pandas
`pd.to_numeric(errors='coerce')`, converting non-numeric placeholders
to `NaN` and logging all affected values for review. Rows in which the
comment text was absent, empty, or consisted solely of whitespace were
removed. Exact duplicate records — defined as rows sharing identical
values across *platform*, *text*, *user*, and *time* simultaneously —
were removed on the assumption that they represent data export artifacts
rather than genuine repeated posts; cross-platform identical comments were
retained because the same text may represent a user posting across
platforms. After cleaning, the unified dataset comprised
**{total_n:,} comments**:
{plat.to_string()}.

---

## Lexicon-Based Framing and Stance Classification

Following established dictionary-assisted content analysis procedures
(e.g., Young & Soroka, 2012), comment-level framing and stance were coded
using four curated keyword lexicons: a golf lexicon, a political lexicon,
a supportive-normalization lexicon, and a resistant/disapproving lexicon.
Each lexicon was developed through a combination of literature review,
frequency inspection of the raw comment corpus, and iterative manual
refinement. Full keyword lists are archived in
`data/cleaned/codebook_keywords.txt`.

Classification was implemented in script `02_classify.py` using
case-insensitive regular expression matching with word-boundary anchoring
for single-token terms and substring matching for multi-token phrases.
Four binary indicator variables were computed for each comment:
*golf\\_ind*, *political\\_ind*, *supportive\\_ind*, and *resistant\\_ind*.

**Frame variable.** A mutually exclusive *frame* variable was constructed
from the binary indicators using the following priority rule: comments
triggering both golf and political indicators were coded as *hybrid*;
comments triggering only golf were coded as *golf*; comments triggering
only political were coded as *political*; and comments triggering neither
were coded as *neutral*. In the present exploratory corpus, the frame
distribution was as follows:
golf = {get_n(f_ovr, 'golf'):,} ({get_pct(f_ovr, 'golf'):.1f}%),
political = {get_n(f_ovr, 'political'):,} ({get_pct(f_ovr, 'political'):.1f}%),
hybrid = {get_n(f_ovr, 'hybrid'):,} ({get_pct(f_ovr, 'hybrid'):.1f}%),
neutral = {get_n(f_ovr, 'neutral'):,} ({get_pct(f_ovr, 'neutral'):.1f}%).

**Stance variable.** Framing and stance were treated as analytically
separate dimensions, consistent with the conceptual distinction between
*what a comment is about* (frame) and *what position it takes* (stance).
A mutually exclusive *stance* variable was constructed by similar logic:
comments triggering both supportive and resistant indicators were coded as
*contested*; otherwise, the single triggered indicator determined the label;
comments triggering neither were coded as *neutral*. preliminary stance
distribution: supportive = {get_n(s_ovr, 'supportive'):,}
({get_pct(s_ovr, 'supportive'):.1f}%),
resistant = {get_n(s_ovr, 'resistant'):,} ({get_pct(s_ovr, 'resistant'):.1f}%),
contested = {get_n(s_ovr, 'contested'):,} ({get_pct(s_ovr, 'contested'):.1f}%),
neutral = {get_n(s_ovr, 'neutral'):,} ({get_pct(s_ovr, 'neutral'):.1f}%).

---

## Engagement Analysis

Because engagement distributions on social media are characteristically
right-skewed — with a small number of comments accumulating the large
majority of likes and replies — reliance on means alone would produce
misleading central-tendency estimates. Accordingly, engagement was
summarized using both mean and median values. A composite variable,
*total\\_engagement*, was computed as the sum of likes and replies for
each comment. To enable meaningful cross-platform comparison, each
comment was assigned a within-platform percentile rank of total engagement.
Comments at or above the 90th percentile within their respective platform
were designated high-engagement comments. This threshold-free,
rank-based approach avoids the arbitrariness of fixed raw cutoffs that
would not be comparable across platforms with structurally different
engagement scales.

---

## Validation Plan

The lexicon-based classification constitutes a first-pass, exploratory
coding and should be interpreted with appropriate caution. Keyword
matching cannot capture sarcasm, irony, or context-dependent meaning.
The research team will conduct manual validation using a stratified random
sample of approximately 100–150 comments drawn proportionally from each
platform and from each frame category. Two group members will code this
sample independently, and inter-rater reliability will be assessed using
Cohen's kappa. Discrepancies will be adjudicated through discussion and
used to refine the lexicons prior to final reporting. All ambiguous
classification decisions are documented in the cleaning and classification
logs.

---

## Reproducibility

All analysis code, cleaned data, keyword codebooks, summary tables,
figures, and log files are archived in a structured GitHub repository.
The workflow is fully reproducible by running four scripts in sequence
(`01_load_clean.py` → `02_classify.py` → `03_descriptive_stats.py` →
`04_visualize.py`). Raw data files are excluded from the public repository
in compliance with platform terms of service; the repository includes
instead a data manifest describing file sources, collection dates, and
record counts. See `README.md` for complete reproduction instructions.

---

*References cited in this summary:*

Young, L., & Soroka, S. (2012). Affective news: The automated coding of
sentiment in political texts. *Political Communication*, 29(2), 205–231.
"""

out = DOCS_DIR / "methods_summary.md"
out.write_text(md, encoding="utf-8")
print(f"Methods summary saved: {out}")
