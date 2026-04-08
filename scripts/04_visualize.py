"""
B50 Cross-Platform Comment Analysis
=====================================
Script:  04_visualize.py
Purpose: Produce the three required figures for the final report.

INPUT:   data/cleaned/B50_classified_comments.csv
         tables/ (CSV files from 03_descriptive_stats.py)

OUTPUT:
  figures/fig1_frame_by_platform.png   — stacked bar: frame distribution
  figures/fig2_engagement_by_frame.png — grouped bar: median total engagement
  figures/fig3_keyword_bar.png         — horizontal bar: top supportive/resistant keywords

DESIGN NOTES:
  * All figures use a consistent color palette and font (DejaVu Sans).
  * Figure 2 uses MEDIAN total engagement (within-platform) rather than mean
    because engagement distributions are heavily right-skewed.  Mean values
    are still reported in the tables.
  * Figure 3 uses keyword frequency counts from the classified dataset;
    only comments flagged as supportive (n_supportive) or resistant
    (n_resistant) are tallied.
"""

import pathlib
import re
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")   # non-interactive backend so it works headlessly
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
DATA_CLEAN = BASE_DIR / "data" / "cleaned"
TABLES_DIR = BASE_DIR / "tables"
FIGS_DIR   = BASE_DIR / "figures"
FIGS_DIR.mkdir(parents=True, exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_CLEAN / "B50_classified_comments.csv", encoding="utf-8-sig")
df["likes"]   = pd.to_numeric(df["likes"],   errors="coerce")
df["replies"] = pd.to_numeric(df["replies"], errors="coerce")
df["total_engagement"] = df["likes"].fillna(0) + df["replies"].fillna(0)

# ── Shared style ──────────────────────────────────────────────────────────────
FRAME_COLORS  = {
    "golf":      "#2196F3",   # blue
    "political": "#E53935",   # red
    "hybrid":    "#7B1FA2",   # purple
    "neutral":   "#B0BEC5",   # grey
}
STANCE_COLORS = {
    "supportive": "#43A047",  # green
    "resistant":  "#E53935",  # red
    "contested":  "#FB8C00",  # orange
    "neutral":    "#B0BEC5",  # grey
}
FRAME_ORDER  = ["golf", "political", "hybrid", "neutral"]
STANCE_ORDER = ["supportive", "resistant", "contested", "neutral"]
PLATFORMS    = ["YouTube", "Instagram", "X"]

plt.rcParams.update({
    "font.family":  "DejaVu Sans",
    "font.size":    11,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Stacked bar chart: frame distribution by platform (RQ1)
# ══════════════════════════════════════════════════════════════════════════════

print("Building Figure 1 …")
fig1, ax1 = plt.subplots(figsize=(9, 5))

# Build a platform × frame percentage table
frame_tab = (
    df.groupby(["platform", "frame"])
    .size()
    .unstack(fill_value=0)
    .reindex(index=PLATFORMS, columns=FRAME_ORDER, fill_value=0)
)
frame_pct = frame_tab.div(frame_tab.sum(axis=1), axis=0) * 100

# Plot stacked bars
left = np.zeros(len(PLATFORMS))
for frame in FRAME_ORDER:
    vals = frame_pct[frame].values
    bars = ax1.barh(PLATFORMS, vals, left=left,
                    color=FRAME_COLORS[frame], label=frame.capitalize(),
                    height=0.55, edgecolor="white", linewidth=0.5)
    # Annotate if slice ≥ 5%
    for i, (v, l) in enumerate(zip(vals, left)):
        if v >= 5:
            ax1.text(l + v / 2, i, f"{v:.1f}%",
                     ha="center", va="center", fontsize=9, color="white", fontweight="bold")
    left += vals

ax1.set_xlabel("Percentage of comments (%)", fontsize=11)
ax1.set_title("Figure 1. Frame Distribution by Platform\n"
              "(Lexicon-based classification; exploratory)", fontsize=12, fontweight="bold")
ax1.set_xlim(0, 100)
ax1.legend(loc="lower right", frameon=False, fontsize=10)
ax1.tick_params(axis="y", labelsize=11)

plt.tight_layout()
out1 = FIGS_DIR / "fig1_frame_by_platform.png"
fig1.savefig(out1, dpi=180, bbox_inches="tight")
plt.close(fig1)
print(f"  Saved: {out1}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Grouped bar chart: median total engagement by frame, per platform
#            Uses MEDIAN (not mean) due to skewed distributions.
# ══════════════════════════════════════════════════════════════════════════════

print("Building Figure 2 …")
eng_rows = []
for plat in PLATFORMS:
    pdf = df[df["platform"] == plat]
    for frame in FRAME_ORDER:
        fdf = pdf[pdf["frame"] == frame]
        eng_rows.append({
            "platform": plat,
            "frame":    frame,
            "median_eng": fdf["total_engagement"].median() if len(fdf) > 0 else 0,
            "n":          len(fdf),
        })
eng_df = pd.DataFrame(eng_rows)

fig2, axes = plt.subplots(1, 3, figsize=(13, 5), sharey=False)
for ax, plat in zip(axes, PLATFORMS):
    sub = eng_df[eng_df["platform"] == plat].set_index("frame").reindex(FRAME_ORDER)
    vals = sub["median_eng"].fillna(0).values
    bars = ax.bar(FRAME_ORDER, vals,
                  color=[FRAME_COLORS[f] for f in FRAME_ORDER],
                  width=0.55, edgecolor="white", linewidth=0.5)
    ax.set_title(plat, fontsize=12, fontweight="bold")
    ax.set_ylabel("Median total engagement\n(likes + replies)" if plat == "YouTube" else "",
                  fontsize=10)
    ax.set_xticklabels([f.capitalize() for f in FRAME_ORDER], rotation=20, ha="right", fontsize=9)
    ax.set_ylim(bottom=0)   # never go below 0 even if replies are missing
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ax.get_ylim()[1] * 0.01,
                f"{v:.1f}", ha="center", va="bottom", fontsize=9)
    # Note if engagement data is sparse for this platform
    if vals.max() == 0:
        ax.text(0.5, 0.5, "Engagement data\nnot available",
                transform=ax.transAxes, ha="center", va="center",
                fontsize=9, color="gray", style="italic")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig2.suptitle("Figure 2. Median Total Engagement by Frame, Within Each Platform\n"
              "(Median used due to right-skewed distributions; exploratory)",
              fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
out2 = FIGS_DIR / "fig2_engagement_by_frame.png"
fig2.savefig(out2, dpi=180, bbox_inches="tight")
plt.close(fig2)
print(f"  Saved: {out2}")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Horizontal bar chart: top supportive vs resistant keywords (RQ3)
#
# Approach: for each keyword in the supportive and resistant lexicons,
# count how many classified comments (supportive or resistant respectively)
# contain that keyword.  Show top N for each side.
# ══════════════════════════════════════════════════════════════════════════════

print("Building Figure 3 …")

# Import keyword lists from classify script (re-define inline to avoid import)
SUPPORTIVE_TERMS = [
    "charity", "charitable", "wounded warrior", "veterans", "veteran",
    "donate", "donation", "giving back", "great cause", "good cause",
    "just golf", "only golf", "not political", "keep it golf",
    "love this", "amazing", "inspiring", "honor", "honour",
    "respect", "support our troops", "troops", "military",
    "God bless", "legend", "iconic", "so cool", "awesome",
    "incredible", "fantastic", "brings people together", "unity", "bipartisan",
]
RESISTANT_TERMS = [
    "unsubscribe", "unsubscribed", "boycott", "disappointed",
    "terrible", "disgusting", "keep politics out", "stay out of politics",
    "shouldn't be political", "don't mix politics", "wrong",
    "lost a subscriber", "lost my subscription", "dislike",
    "trash", "sellout", "sell out", "pathetic", "embarrassing",
    "shame", "shameful", "ridiculous", "absurd", "horrible",
    "stop watching", "done watching", "unfollowed", "unfollowing",
    "not the place for politics", "just play golf",
]

# Only count within comments that were classified as that stance
sup_text  = df[df["stance"] == "supportive"]["text"].str.lower()
res_text  = df[df["stance"] == "resistant"]["text"].str.lower()

def count_kw(texts: pd.Series, term: str) -> int:
    return texts.str.contains(re.escape(term), case=False, na=False).sum()

TOP_N = 12
sup_counts = {t: count_kw(sup_text, t) for t in SUPPORTIVE_TERMS}
res_counts = {t: count_kw(res_text, t) for t in RESISTANT_TERMS}

sup_sorted = sorted(sup_counts.items(), key=lambda x: x[1], reverse=True)[:TOP_N]
res_sorted = sorted(res_counts.items(), key=lambda x: x[1], reverse=True)[:TOP_N]

# Build plot
fig3, (ax_sup, ax_res) = plt.subplots(1, 2, figsize=(13, 6))

# Supportive (left panel)
skw, sval = zip(*sup_sorted) if sup_sorted else ([], [])
ax_sup.barh(list(skw)[::-1], list(sval)[::-1], color="#43A047", height=0.6)
ax_sup.set_title("Supportive Keywords", fontsize=12, fontweight="bold", color="#43A047")
ax_sup.set_xlabel("Frequency in supportive comments", fontsize=10)
ax_sup.spines["top"].set_visible(False)
ax_sup.spines["right"].set_visible(False)

# Resistant (right panel)
rkw, rval = zip(*res_sorted) if res_sorted else ([], [])
ax_res.barh(list(rkw)[::-1], list(rval)[::-1], color="#E53935", height=0.6)
ax_res.set_title("Resistant Keywords", fontsize=12, fontweight="bold", color="#E53935")
ax_res.set_xlabel("Frequency in resistant comments", fontsize=10)
ax_res.spines["top"].set_visible(False)
ax_res.spines["right"].set_visible(False)

fig3.suptitle("Figure 3. Top Supportive vs Resistant Keywords (RQ3)\n"
              "(Counts within stance-classified comments only; exploratory)",
              fontsize=12, fontweight="bold")
plt.tight_layout()
out3 = FIGS_DIR / "fig3_keyword_bar.png"
fig3.savefig(out3, dpi=180, bbox_inches="tight")
plt.close(fig3)
print(f"  Saved: {out3}")

print("\nAll figures complete.")
