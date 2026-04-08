"""
B50 Cross-Platform Comment Analysis
=====================================
Project: Cross-platform audience reactions to Bryson DeChambeau's Break 50
         episode featuring Donald Trump — YouTube, Instagram, and X.
Course:  KIN 7518 Social Issues in Sport

Script:  01_load_clean.py
Purpose: Load all three raw Excel files, standardize column names,
         clean the data, and export a unified comment-level CSV.

Authors: TSPS Group (KIN 7518)
Date:    2026

HOW TO RUN:
    python scripts/01_load_clean.py

OUTPUT:
    data/cleaned/B50_unified_comments.csv
    data/cleaned/cleaning_log.txt
"""

# ── Standard library ──────────────────────────────────────────────────────────
import os
import re
import pathlib
import logging
from datetime import datetime

# ── Third-party ───────────────────────────────────────────────────────────────
import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# 0.  CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

# Adjust this path if you move the repository
BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
DATA_RAW   = BASE_DIR / "data" / "raw"
DATA_CLEAN = BASE_DIR / "data" / "cleaned"
DATA_CLEAN.mkdir(parents=True, exist_ok=True)

# Set up a cleaning log so every decision is documented
log_path = DATA_CLEAN / "cleaning_log.txt"
logging.basicConfig(
    filename=str(log_path),
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())   # also print to console

log.info("=" * 70)
log.info("B50 DATA LOADING AND CLEANING — %s", datetime.now().strftime("%Y-%m-%d"))
log.info("=" * 70)


# ══════════════════════════════════════════════════════════════════════════════
# 1.  LOAD RAW FILES
#     Each file has different column names; we map them to a unified schema.
#
#     Unified schema fields:
#       platform    – 'YouTube', 'Instagram', or 'X'
#       text        – comment body (string)
#       user        – screen name / username
#       likes       – number of likes (numeric, may be missing)
#       replies     – number of replies / reply count (numeric, may be missing)
#       time        – timestamp string (kept as-is for now)
#       comment_id  – platform-specific comment identifier
#       post_id     – platform-specific post / video identifier
# ══════════════════════════════════════════════════════════════════════════════

def load_youtube(path: pathlib.Path) -> pd.DataFrame:
    """
    Load B50_YT_COMMENT.xlsx.
    Observed columns: text, user, comment_re, likes, time, source
    'comment_re' is the reply count column.
    'source' appears to be a post-level identifier (video URL or ID).
    """
    log.info("Loading YouTube file: %s", path.name)
    df = pd.read_excel(path, engine="openpyxl")
    log.info("  Raw shape: %s", df.shape)

    # Rename to unified schema
    df = df.rename(columns={
        "comment_re": "replies",
        "source":     "post_id",
    })

    # Fields missing in this file — fill with NA so the unified frame is consistent
    df["comment_id"] = np.nan       # YT file does not expose comment IDs
    df["platform"]   = "YouTube"

    unified_cols = ["platform", "text", "user", "likes", "replies",
                    "time", "comment_id", "post_id"]
    return df[unified_cols].copy()


def load_instagram(path: pathlib.Path) -> pd.DataFrame:
    """
    Load B50_INS_COMMENT.xlsx.
    Observed columns: postlink, postid, text, userid, user,
                      commentid, comment_re, likes, time
    """
    log.info("Loading Instagram file: %s", path.name)
    df = pd.read_excel(path, engine="openpyxl")
    log.info("  Raw shape: %s", df.shape)

    df = df.rename(columns={
        "commentid":  "comment_id",
        "postid":     "post_id",
        "comment_re": "replies",
    })

    # 'userid' is numeric; 'user' is the display name — we keep 'user'
    # 'postlink' is redundant with 'post_id'; drop it to keep schema clean
    df["platform"] = "Instagram"

    unified_cols = ["platform", "text", "user", "likes", "replies",
                    "time", "comment_id", "post_id"]
    return df[unified_cols].copy()


def load_x(path: pathlib.Path) -> pd.DataFrame:
    """
    Load B50_X_COMMENT.xlsx.
    This file has 30 columns; we select the relevant ones.
    Key columns:
      contents      → text
      username      → user
      likes         → likes
      reply counts  → replies
      date          → time
      contentsid    → comment_id
      Blog ID       → post_id  (AMBIGUITY FLAG: 'Blog ID' may be tweet/thread ID)
    """
    log.info("Loading X file: %s", path.name)
    df = pd.read_excel(path, engine="openpyxl")
    log.info("  Raw shape: %s", df.shape)

    # AMBIGUITY FLAG: X file contains 'retweets count' and 'reference count'
    # We use 'reply counts' as the replies field; retweets are not included
    # in the engagement metric to stay comparable across platforms.
    log.info("  AMBIGUITY: X 'Blog ID' used as post_id; verify this maps to"
             " the original tweet thread, not the individual reply ID.")

    df = df.rename(columns={
        "contents":      "text",
        "username":      "user",
        "reply counts":  "replies",
        "date":          "time",
        "contentsid":    "comment_id",
        "Blog ID":       "post_id",
    })

    df["platform"] = "X"

    unified_cols = ["platform", "text", "user", "likes", "replies",
                    "time", "comment_id", "post_id"]
    return df[unified_cols].copy()


# ── Load all three ────────────────────────────────────────────────────────────
yt_df  = load_youtube(DATA_RAW / "B50_YT_COMMENT.xlsx")
ins_df = load_instagram(DATA_RAW / "B50_INS_COMMENT.xlsx")
x_df   = load_x(DATA_RAW / "B50_X_COMMENT.xlsx")

df = pd.concat([yt_df, ins_df, x_df], ignore_index=True)
log.info("\nCombined shape (before cleaning): %s", df.shape)


# ══════════════════════════════════════════════════════════════════════════════
# 2.  CLEAN THE DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── 2a. Convert likes and replies to numeric ──────────────────────────────────
log.info("\n--- Numeric conversion: likes and replies ---")

def to_numeric_safe(series: pd.Series, col_name: str) -> pd.Series:
    """
    Coerce a column to numeric.  Non-numeric values (placeholders, strings)
    are converted to NaN and logged.
    """
    original_non_null = series.notna().sum()
    numeric = pd.to_numeric(series, errors="coerce")
    failed  = original_non_null - numeric.notna().sum()
    if failed > 0:
        bad_vals = series[series.notna() & numeric.isna()].unique()[:10]
        log.info("  [%s] %d non-numeric values coerced to NaN. Examples: %s",
                 col_name, failed, bad_vals)
    return numeric

df["likes"]   = to_numeric_safe(df["likes"],   "likes")
df["replies"] = to_numeric_safe(df["replies"], "replies")

log.info("  likes   NaN count: %d / %d", df["likes"].isna().sum(),   len(df))
log.info("  replies NaN count: %d / %d", df["replies"].isna().sum(), len(df))


# ── 2b. Remove rows with missing text ────────────────────────────────────────
log.info("\n--- Removing rows with missing or whitespace-only text ---")
n_before = len(df)
df["text"] = df["text"].astype(str).str.strip()
df = df[df["text"].notna() & (df["text"] != "") & (df["text"].str.lower() != "nan")]
n_after = len(df)
log.info("  Removed %d rows with empty/missing text. Remaining: %d", n_before - n_after, n_after)


# ── 2c. Trim whitespace in string columns ────────────────────────────────────
for col in ["user", "text"]:
    df[col] = df[col].astype(str).str.strip()


# ── 2d. Handle duplicates ────────────────────────────────────────────────────
log.info("\n--- Duplicate detection ---")
# Definition: an exact duplicate has the same platform, text, user, AND time.
# We KEEP cross-platform duplicates (same words, different platforms) and
# comments from the same user that are genuinely repeated across posts.
# We remove only rows that are byte-for-byte identical across ALL key fields,
# which likely indicates a data export artifact rather than real repeated posting.

dup_mask = df.duplicated(subset=["platform", "text", "user", "time"], keep="first")
n_dups = dup_mask.sum()
log.info("  Exact duplicate records (same platform+text+user+time): %d", n_dups)
log.info("  DECISION: removing confirmed exact duplicates (likely export artifacts).")
df = df[~dup_mask].reset_index(drop=True)
log.info("  Shape after deduplication: %s", df.shape)


# ── 2e. Add a row index for traceability ─────────────────────────────────────
df.insert(0, "row_id", range(1, len(df) + 1))


# ── 2f. Summary stats post-cleaning ──────────────────────────────────────────
log.info("\n--- Post-cleaning platform counts ---")
for plat, grp in df.groupby("platform"):
    log.info("  %s: %d comments", plat, len(grp))
log.info("  TOTAL: %d comments", len(df))


# ── 2g. Export cleaned file ───────────────────────────────────────────────────
out_path = DATA_CLEAN / "B50_unified_comments.csv"
df.to_csv(out_path, index=False, encoding="utf-8-sig")
log.info("\n✓ Cleaned CSV saved: %s", out_path)
log.info("Cleaning complete.")
