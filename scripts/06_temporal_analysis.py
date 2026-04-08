"""
B50 Cross-Platform Comment Analysis
=====================================
Script:  06_temporal_analysis.py
Purpose: Plot comment volume over time by platform to identify engagement
         spikes relative to the video's release date.

INPUT:   data/cleaned/B50_classified_comments.csv
OUTPUT:  figures/fig4_temporal_volume.png

NOTE: Timestamp formats vary across platforms. Rows with unparseable
      timestamps are dropped and counted in the log.
"""

import pathlib
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
DATA_CLEAN = BASE_DIR / "data" / "cleaned"
FIGURES    = BASE_DIR / "figures"
FIGURES.mkdir(exist_ok=True)

log_path = DATA_CLEAN / "temporal_log.txt"
logging.basicConfig(
    filename=str(log_path), filemode="w",
    level=logging.INFO, format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())

log.info("=" * 70)
log.info("B50 TEMPORAL ANALYSIS")
log.info("=" * 70)

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_CLEAN / "B50_classified_comments.csv", encoding="utf-8-sig")
log.info("Loaded: %d rows", len(df))

df["time"] = pd.to_datetime(df["time"], errors="coerce")
dropped = df["time"].isna().sum()
if dropped:
    log.warning("Dropped %d rows with unparseable timestamps", dropped)

df = df.dropna(subset=["time"])
log.info("Rows with valid timestamps: %d", len(df))

# ── Aggregate by day × platform ───────────────────────────────────────────────
df["date"] = df["time"].dt.normalize()
daily = (
    df.groupby(["date", "platform"])
    .size()
    .reset_index(name="count")
    .pivot(index="date", columns="platform", values="count")
    .fillna(0)
    .astype(int)
)

log.info("Date range: %s → %s", daily.index.min().date(), daily.index.max().date())

# ── Plot ───────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13, 5))

COLORS = {"YouTube": "#FF0000", "Instagram": "#C13584", "X": "#1DA1F2"}

for platform in daily.columns:
    color = COLORS.get(platform, None)
    ax.plot(daily.index, daily[platform], label=platform, color=color, linewidth=1.8)

ax.set_title(
    "Comment Volume Over Time by Platform\n(Break 50 × Trump Episode)",
    fontsize=13, fontweight="bold",
)
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Number of Comments", fontsize=11)
ax.legend(title="Platform", fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())
fig.autofmt_xdate(rotation=30)
ax.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
out_path = FIGURES / "fig4_temporal_volume.png"
plt.savefig(out_path, dpi=150)
plt.close()

log.info("✓ Saved: %s", out_path)
log.info("Temporal analysis complete.")
