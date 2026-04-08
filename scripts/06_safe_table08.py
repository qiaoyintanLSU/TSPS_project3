"""
generate_safe_tables.py
=======================
Regenerates table 08 as a fully aggregated summary
(platform × frame × stance counts) with NO row-level text or usernames.

Run this once after 03_descriptive_stats.py to overwrite the unsafe version.

INPUT:  data/cleaned/B50_classified_comments.csv   (local only — not in repo)
OUTPUT: tables/08_top10pct_high_engagement.csv      (aggregated — safe to commit)
"""

import pathlib
import pandas as pd

BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
DATA_CLEAN = BASE_DIR / "data" / "cleaned"
TABLES_DIR = BASE_DIR / "tables"

df = pd.read_csv(DATA_CLEAN / "B50_classified_comments.csv", encoding="utf-8-sig")
df["likes"]   = pd.to_numeric(df["likes"],   errors="coerce")
df["replies"] = pd.to_numeric(df["replies"], errors="coerce")
df["total_engagement"] = df["likes"].fillna(0) + df["replies"].fillna(0)
df["engage_rank_pct"]  = df.groupby("platform")["total_engagement"].rank(pct=True)
df["top10pct"] = (df["engage_rank_pct"] >= 0.90).astype(int)

top10 = df[df["top10pct"] == 1].copy()

# Aggregated: counts by platform × frame × stance — NO text or usernames
agg = (
    top10
    .groupby(["platform", "frame", "stance"])
    .agg(
        n_comments        = ("row_id", "count"),
        median_likes      = ("likes",            "median"),
        median_replies    = ("replies",           "median"),
        median_total_eng  = ("total_engagement",  "median"),
        mean_total_eng    = ("total_engagement",  "mean"),
    )
    .round(2)
    .reset_index()
)

out = TABLES_DIR / "08_top10pct_high_engagement.csv"
agg.to_csv(out, index=False, encoding="utf-8-sig")
print(f"Safe aggregated table saved: {out}")
print(agg.to_string())
