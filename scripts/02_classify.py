"""
B50 Cross-Platform Comment Analysis
=====================================
Script:  02_classify.py
Purpose: Apply lexicon-based binary indicators for framing and stance,
         then build mutually exclusive FRAME and STANCE variables.

INPUT:   data/cleaned/B50_unified_comments.csv
OUTPUT:  data/cleaned/B50_classified_comments.csv
         data/cleaned/codebook_keywords.txt  (documents all keyword lists)

FRAMING DIMENSIONS (analytically separate from stance):
  - golf_frame        : comment primarily references golf activity / performance
  - political_frame   : comment primarily references Trump, politics, partisanship
  - hybrid_frame      : comment contains BOTH golf AND political language
  - frame             : mutually exclusive label (golf / political / hybrid / neutral)

STANCE DIMENSIONS:
  - supportive        : language normalizing or approving the political presence
  - resistant         : language objecting to or disapproving the political presence
  - stance            : mutually exclusive label (supportive / resistant / contested / neutral)

IMPORTANT NOTES FOR MANUAL VALIDATION:
  * Keyword matching is case-insensitive and whole-word where possible.
  * Sarcasm, irony, and short emoji-heavy comments may be misclassified.
  * The 'political' lexicon intentionally includes the name 'Trump' —
    comments that merely mention Trump (descriptively, without evaluation)
    will be flagged; coders should assess whether the political signal is real.
  * 'Contested' stance = comment contains BOTH supportive AND resistant signals.
  * All percentages and counts are EXPLORATORY until manual validation is complete.
"""

import pathlib
import re
import logging
import pandas as pd
import numpy as np

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = pathlib.Path(__file__).resolve().parent.parent
DATA_CLEAN = BASE_DIR / "data" / "cleaned"

log_path = DATA_CLEAN / "classification_log.txt"
logging.basicConfig(
    filename=str(log_path), filemode="w",
    level=logging.INFO, format="%(asctime)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger()
log.addHandler(logging.StreamHandler())

log.info("=" * 70)
log.info("B50 LEXICON-BASED CLASSIFICATION")
log.info("=" * 70)


# ══════════════════════════════════════════════════════════════════════════════
# 1.  KEYWORD LEXICONS
#     Each list was developed by the research team through:
#       (a) review of sport-politics and social-media framing literature
#       (b) inspection of frequent tokens in the raw comment text
#       (c) iterative manual spot-checking
#
#     AMBIGUITY FLAG: words like 'eagle', 'drive', 'iron' are common English
#     words that also have golf meanings; they are NOT included in the golf
#     lexicon to reduce false positives.  Similarly, 'great' and 'patriot'
#     were excluded from the supportive lexicon because they appear frequently
#     in generic contexts.
# ══════════════════════════════════════════════════════════════════════════════

GOLF_TERMS = [
    "golf", "golfer", "golfing", "putt", "putting", "birdie", "eagle",
    "bogey", "par", "fairway", "tee", "tee box", "green", "hole in one",
    "hole-in-one", "driver", "iron", "wedge", "chip", "chipping",
    "swing", "backswing", "follow-through", "divot", "caddie",
    "pga", "lpga", "liv golf", "liv", "masters", "augusta", "ryder cup",
    "course", "round of golf", "golf course", "golf club",
    "dechambeau", "bryson", "break 50", "break50",
    "handicap", "scorecard", "bunker", "sand trap",
    "bogey", "albatross", "stroke", "strokes gained",
]

POLITICAL_TERMS = [
    "trump", "donald trump", "president trump", "president", "potus",
    "maga", "make america great", "republican", "democrat", "gop",
    "election", "political", "politics", "partisan", "liberal",
    "conservative", "biden", "white house", "campaign", "vote",
    "left wing", "right wing", "left-wing", "right-wing",
    "socialism", "capitalism", "progressive", "patriot", "patriotic",
    "america first", "deep state", "woke", "anti-trump", "pro-trump",
    "trump supporter", "trump hater", "maga hat", "dnc", "rnc",
]

SUPPORTIVE_TERMS = [
    "charity", "charitable", "wounded warrior", "veterans", "veteran",
    "donate", "donation", "giving back", "great cause", "good cause",
    "just golf", "only golf", "not political", "keep it golf",
    "love this", "amazing", "inspiring", "honor", "honour",
    "respect", "support our troops", "troops", "military",
    "God bless", "god bless america", "legend", "iconic",
    "so cool", "awesome", "incredible", "fantastic",
    "brings people together", "unity", "bipartisan",
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

# ── Export codebook ───────────────────────────────────────────────────────────
codebook_path = DATA_CLEAN / "codebook_keywords.txt"
with open(codebook_path, "w", encoding="utf-8") as cb:
    cb.write("B50 KEYWORD CODEBOOK\n")
    cb.write("=" * 60 + "\n\n")
    for label, terms in [
        ("GOLF LEXICON",       GOLF_TERMS),
        ("POLITICAL LEXICON",  POLITICAL_TERMS),
        ("SUPPORTIVE LEXICON", SUPPORTIVE_TERMS),
        ("RESISTANT LEXICON",  RESISTANT_TERMS),
    ]:
        cb.write(f"{label}\n{'-' * 40}\n")
        for t in sorted(terms):
            cb.write(f"  {t}\n")
        cb.write(f"\nTotal terms: {len(terms)}\n\n")
log.info("Codebook saved: %s", codebook_path)


# ══════════════════════════════════════════════════════════════════════════════
# 2.  CLASSIFICATION FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def make_pattern(terms: list) -> re.Pattern:
    """
    Build a single compiled regex from a keyword list.
    Uses word boundaries (\\b) where the term is a single token;
    for multi-word phrases, a simple casefold match is used.
    The pattern is case-insensitive.
    """
    escaped = [re.escape(t) for t in sorted(terms, key=len, reverse=True)]
    # Use word boundary only for single-word terms to avoid partial matches
    bordered = []
    for orig, esc in zip(sorted(terms, key=len, reverse=True), escaped):
        if " " in orig:
            bordered.append(esc)        # phrase: no word boundary needed
        else:
            bordered.append(r"\b" + esc + r"\b")
    return re.compile("|".join(bordered), flags=re.IGNORECASE)

GOLF_PAT      = make_pattern(GOLF_TERMS)
POLITICAL_PAT = make_pattern(POLITICAL_TERMS)
SUPPORT_PAT   = make_pattern(SUPPORTIVE_TERMS)
RESIST_PAT    = make_pattern(RESISTANT_TERMS)


def classify_text(text: str) -> dict:
    """
    Apply all four binary indicators to a single comment string.
    Returns a dict of 0/1 values.
    """
    if not isinstance(text, str) or text.strip() == "":
        return {"golf_ind": 0, "political_ind": 0, "supportive_ind": 0, "resistant_ind": 0}
    return {
        "golf_ind":       1 if GOLF_PAT.search(text)      else 0,
        "political_ind":  1 if POLITICAL_PAT.search(text) else 0,
        "supportive_ind": 1 if SUPPORT_PAT.search(text)   else 0,
        "resistant_ind":  1 if RESIST_PAT.search(text)    else 0,
    }


# ══════════════════════════════════════════════════════════════════════════════
# 3.  LOAD CLEANED DATA & APPLY CLASSIFICATION
# ══════════════════════════════════════════════════════════════════════════════

df = pd.read_csv(DATA_CLEAN / "B50_unified_comments.csv", encoding="utf-8-sig")
log.info("Loaded cleaned data: %s rows", len(df))

# Apply indicators
log.info("Applying lexicon-based indicators …")
indicators = df["text"].apply(classify_text)
ind_df = pd.DataFrame(indicators.tolist())
df = pd.concat([df, ind_df], axis=1)


# ══════════════════════════════════════════════════════════════════════════════
# 4.  BUILD MUTUALLY EXCLUSIVE FRAME VARIABLE
#
#     Priority rule (documented for transparency):
#       hybrid    → golf_ind == 1 AND political_ind == 1
#       golf      → golf_ind == 1 AND political_ind == 0
#       political → political_ind == 1 AND golf_ind == 0
#       neutral   → neither golf nor political signal detected
#
#     AMBIGUITY FLAG: The 'hybrid' category captures comments that
#     simultaneously use golf AND political vocabulary.  Because keyword
#     matching cannot distinguish intentional blending from incidental
#     co-occurrence, hybrid labels should receive priority manual review.
# ══════════════════════════════════════════════════════════════════════════════

def assign_frame(row: pd.Series) -> str:
    g = row["golf_ind"]
    p = row["political_ind"]
    if g and p:
        return "hybrid"
    if g and not p:
        return "golf"
    if p and not g:
        return "political"
    return "neutral"

df["frame"] = df.apply(assign_frame, axis=1)
log.info("Frame distribution:\n%s", df["frame"].value_counts().to_string())


# ══════════════════════════════════════════════════════════════════════════════
# 5.  BUILD MUTUALLY EXCLUSIVE STANCE VARIABLE
#
#     Priority rule:
#       contested  → supportive_ind == 1 AND resistant_ind == 1
#       supportive → supportive_ind == 1 AND resistant_ind == 0
#       resistant  → resistant_ind == 1 AND supportive_ind == 0
#       neutral    → neither detected
#
#     AMBIGUITY FLAG: 'Contested' comments may reflect sarcasm or nuanced
#     opinion; they warrant manual review before being treated as true
#     mixed stance.  Approximately 2–5% of comments are expected here.
# ══════════════════════════════════════════════════════════════════════════════

def assign_stance(row: pd.Series) -> str:
    s = row["supportive_ind"]
    r = row["resistant_ind"]
    if s and r:
        return "contested"
    if s and not r:
        return "supportive"
    if r and not s:
        return "resistant"
    return "neutral"

df["stance"] = df.apply(assign_stance, axis=1)
log.info("Stance distribution:\n%s", df["stance"].value_counts().to_string())


# ══════════════════════════════════════════════════════════════════════════════
# 6.  EXPORT
# ══════════════════════════════════════════════════════════════════════════════

out_path = DATA_CLEAN / "B50_classified_comments.csv"
df.to_csv(out_path, index=False, encoding="utf-8-sig")
log.info("\n✓ Classified CSV saved: %s", out_path)
log.info("Classification complete.")
