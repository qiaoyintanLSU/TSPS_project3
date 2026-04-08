"""
B50 Cross-Platform Comment Analysis
=====================================
Script:  03_descriptive_stats.py
Purpose: Produce descriptive statistics for framing and stance,
         and compute within-platform engagement metrics.

INPUT:   data/cleaned/B50_classified_comments.csv
OUTPUT:
  tables/01_platform_counts.csv
  tables/02_frame_overall.csv
  tables/03_frame_by_platform.csv
  tables/04_stance_overall.csv
  tables/05_stance_by_platform.csv
  tables/06_engagement_by_frame.csv
  tables/07_engagement_by_stance.csv
  tables/08_top10pct_high_engagement.csv

ENGAGEMENT APPROACH:
  Because like counts are highly skewed across all three platforms
  (long tail of viral comments), we report BOTH mean and median.
  Within-platform percentile rank is used to identify high-engagement
  comments rather than a fixed raw threshold, which would be
  arbitrary and non-comparable across platforms.
"""

import pathlib
import logging
import pandas as pd
import numpy as np

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
DATA_CLEAN = BASE_DIR / "data" / "cleaned"
TABLES_DIR = BASE_DIR / "tables"
TABLES_DIR.mkdir(parents=True, exist_ok=True)

log_path = TABLES_DIR / "stats_log.txt"
logging.basicConfig(
    filename=str(log_path), filemode="w",
    level=logging.INFO, format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())

log.info("=" * 70)
log.info("B50 DESCRIPTIVE STATISTICS")
log.info("=" * 70)


# ── Load classified data ──────────────────────────────────────────────────────
df = pd.read_csv(DATA_CLEAN / "B50_classified_comments.csv", encoding="utf-8-sig")
log.info("Loaded: %d rows", len(df))

# Ensure numeric
df["likes"]   = pd.to_numeric(df["likes"],   errors="coerce")
df["replies"] = pd.to_numeric(df["replies"], errors="coerce")

# Total engagement = likes + replies (NaN treated as 0 for this sum)
df["total_engagement"] = df["likes"].fillna(0) + df["replies"].fillna(0)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: save a table and log it
# ══════════════════════════════════════════════════════════════════════════════
def save_table(table: pd.DataFrame, filename: str, label: str):
    path = TABLES_DIR / filename
    table.to_csv(path, index=True, encoding="utf-8-sig")
    log.info("\n[%s]\n%s", label, table.to_string())
    log.info("Saved: %s", path)


# ══════════════════════════════════════════════════════════════════════════════
# 1.  PLATFORM COMMENT COUNTS
# ══════════════════════════════════════════════════════════════════════════════
plat_counts = (
    df.groupby("platform")
    .size()
    .rename("n_comments")
    .to_frame()
)
plat_counts["pct"] = (plat_counts["n_comments"] / plat_counts["n_comments"].sum() * 100).round(1)
save_table(plat_counts, "01_platform_counts.csv", "Platform comment counts")


# ══════════════════════════════════════════════════════════════════════════════
# 2.  FRAME DISTRIBUTION — OVERALL
# ══════════════════════════════════════════════════════════════════════════════
FRAME_ORDER  = ["golf", "political", "hybrid", "neutral"]
STANCE_ORDER = ["supportive", "resistant", "contested", "neutral"]

frame_overall = (
    df["frame"]
    .value_counts()
    .reindex(FRAME_ORDER, fill_value=0)
    .rename("n")
    .to_frame()
)
frame_overall["pct"] = (frame_overall["n"] / frame_overall["n"].sum() * 100).round(1)
save_table(frame_overall, "02_frame_overall.csv", "Frame distribution (overall)")


# ══════════════════════════════════════════════════════════════════════════════
# 3.  FRAME DISTRIBUTION — BY PLATFORM
# ══════════════════════════════════════════════════════════════════════════════
frame_by_plat = (
    df.groupby(["platform", "frame"])
    .size()
    .rename("n")
    .unstack(fill_value=0)
    .reindex(columns=FRAME_ORDER, fill_value=0)
)
frame_by_plat_pct = frame_by_plat.div(frame_by_plat.sum(axis=1), axis=0).multiply(100).round(1)
frame_by_plat_pct.columns = [f"{c}_pct" for c in frame_by_plat_pct.columns]
frame_by_plat_combined = pd.concat([frame_by_plat, frame_by_plat_pct], axis=1)
save_table(frame_by_plat_combined, "03_frame_by_platform.csv", "Frame by platform")


# ══════════════════════════════════════════════════════════════════════════════
# 4.  STANCE DISTRIBUTION — OVERALL
# ══════════════════════════════════════════════════════════════════════════════
stance_overall = (
    df["stance"]
    .value_counts()
    .reindex(STANCE_ORDER, fill_value=0)
    .rename("n")
    .to_frame()
)
stance_overall["pct"] = (stance_overall["n"] / stance_overall["n"].sum() * 100).round(1)
save_table(stance_overall, "04_stance_overall.csv", "Stance distribution (overall)")


# ══════════════════════════════════════════════════════════════════════════════
# 5.  STANCE DISTRIBUTION — BY PLATFORM
# ══════════════════════════════════════════════════════════════════════════════
stance_by_plat = (
    df.groupby(["platform", "stance"])
    .size()
    .rename("n")
    .unstack(fill_value=0)
    .reindex(columns=STANCE_ORDER, fill_value=0)
)
stance_by_plat_pct = stance_by_plat.div(stance_by_plat.sum(axis=1), axis=0).multiply(100).round(1)
stance_by_plat_pct.columns = [f"{c}_pct" for c in stance_by_plat_pct.columns]
stance_by_plat_combined = pd.concat([stance_by_plat, stance_by_plat_pct], axis=1)
save_table(stance_by_plat_combined, "05_stance_by_platform.csv", "Stance by platform")


# ══════════════════════════════════════════════════════════════════════════════
# 6.  ENGAGEMENT METRICS
#
#     We compute engagement WITHIN each platform to avoid cross-platform
#     comparison of raw counts (YouTube comments tend to have more likes
#     than X or Instagram comments for structural reasons unrelated to content).
#
#     Within-platform percentile rank:
#       rank_pct = percent of comments in the same platform with
#                  total_engagement <= this comment's total_engagement.
#       Top 10% = rank_pct >= 0.90
# ══════════════════════════════════════════════════════════════════════════════

# Compute within-platform percentile rank
df["engage_rank_pct"] = df.groupby("platform")["total_engagement"].rank(pct=True)
df["top10pct"]        = (df["engage_rank_pct"] >= 0.90).astype(int)

log.info("\nTop-10%% high-engagement comments by platform:")
log.info(df.groupby("platform")["top10pct"].sum().to_string())


# ── 6a.  Engagement by Frame (within platform) ───────────────────────────────
def engagement_summary(subdf: pd.DataFrame, group_var: str) -> pd.DataFrame:
    """
    For a given grouping variable, compute mean likes, median likes,
    mean replies, median replies, mean total engagement, n top10pct.
    """
    rows = []
    for name, grp in subdf.groupby(group_var):
        rows.append({
            group_var:          name,
            "n":                len(grp),
            "mean_likes":       round(grp["likes"].mean(), 2),
            "median_likes":     round(grp["likes"].median(), 2),
            "mean_replies":     round(grp["replies"].mean(), 2),
            "median_replies":   round(grp["replies"].median(), 2),
            "mean_total_eng":   round(grp["total_engagement"].mean(), 2),
            "median_total_eng": round(grp["total_engagement"].median(), 2),
            "n_top10pct":       int(grp["top10pct"].sum()),
            "pct_top10pct":     round(grp["top10pct"].mean() * 100, 1),
        })
    return pd.DataFrame(rows).set_index(group_var)

# Per platform × frame
eng_frame_rows = []
for plat, plat_df in df.groupby("platform"):
    summary = engagement_summary(plat_df, "frame")
    summary.insert(0, "platform", plat)
    eng_frame_rows.append(summary.reset_index())
eng_by_frame = pd.concat(eng_frame_rows, ignore_index=True)
save_table(eng_by_frame.set_index(["platform", "frame"]),
           "06_engagement_by_frame.csv", "Engagement by frame (within platform)")

# Per platform × stance
eng_stance_rows = []
for plat, plat_df in df.groupby("platform"):
    summary = engagement_summary(plat_df, "stance")
    summary.insert(0, "platform", plat)
    eng_stance_rows.append(summary.reset_index())
eng_by_stance = pd.concat(eng_stance_rows, ignore_index=True)
save_table(eng_by_stance.set_index(["platform", "stance"]),
           "07_engagement_by_stance.csv", "Engagement by stance (within platform)")


# ── 6b.  Top-10% high-engagement comments ────────────────────────────────────
top10 = df[df["top10pct"] == 1].copy()
top10_export = top10[["platform", "frame", "stance", "likes", "replies",
                       "total_engagement", "engage_rank_pct"]].copy()
top10_export = top10_export.sort_values(["platform", "total_engagement"], ascending=[True, False])
save_table(top10_export, "08_top10pct_high_engagement.csv",
           "Top 10% high-engagement comments")


# ── 6c.  Save the full annotated file ────────────────────────────────────────
df.to_csv(DATA_CLEAN / "B50_classified_comments.csv", index=False, encoding="utf-8-sig")
log.info("\n✓ Annotated CSV (with engagement ranks) resaved.")
log.info("All descriptive statistics complete.")
