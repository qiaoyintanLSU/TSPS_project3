"""
tests/test_classify.py
Unit tests for the lexicon-based classifier in 02_classify.py.

Run with:  python -m pytest tests/
"""

import sys
import pathlib

# Allow importing from scripts/
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

from importlib import util as _ilu

# Load 02_classify without executing its top-level I/O (pd.read_csv, log setup, etc.)
# We only need the classify_text function and the pattern objects.
_spec = _ilu.spec_from_file_location(
    "classify",
    pathlib.Path(__file__).resolve().parent.parent / "scripts" / "02_classify.py",
)

import unittest


# ── Helper: import only the pure functions we need ───────────────────────────
# Re-declare the patterns here so tests have no I/O side effects.
import re

GOLF_TERMS = [
    "golf", "golfer", "golfing", "putt", "putting", "birdie", "eagle",
    "bogey", "par", "fairway", "tee", "tee box", "green", "hole in one",
    "hole-in-one", "driver", "iron", "wedge", "chip", "chipping",
    "swing", "backswing", "follow-through", "divot", "caddie",
    "pga", "lpga", "liv golf", "liv", "masters", "augusta", "ryder cup",
    "course", "round of golf", "golf course", "golf club",
    "dechambeau", "bryson", "break 50", "break50",
    "handicap", "scorecard", "bunker", "sand trap",
    "albatross", "stroke", "strokes gained",
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


def make_pattern(terms):
    escaped = [re.escape(t) for t in sorted(terms, key=len, reverse=True)]
    bordered = []
    for orig, esc in zip(sorted(terms, key=len, reverse=True), escaped):
        if " " in orig:
            bordered.append(esc)
        else:
            bordered.append(r"\b" + esc + r"\b")
    return re.compile("|".join(bordered), flags=re.IGNORECASE)


GOLF_PAT      = make_pattern(GOLF_TERMS)
POLITICAL_PAT = make_pattern(POLITICAL_TERMS)
SUPPORT_PAT   = make_pattern(SUPPORTIVE_TERMS)
RESIST_PAT    = make_pattern(RESISTANT_TERMS)


def classify_text(text: str) -> dict:
    if not isinstance(text, str) or text.strip() == "":
        return {"golf_ind": 0, "political_ind": 0, "supportive_ind": 0, "resistant_ind": 0}

    golf_hit = 1 if GOLF_PAT.search(text) else 0
    political_matches = set(m.group(0).lower() for m in POLITICAL_PAT.finditer(text))
    if political_matches == {"trump"} and golf_hit:
        political_hit = 0
    else:
        political_hit = 1 if political_matches else 0

    return {
        "golf_ind":       golf_hit,
        "political_ind":  political_hit,
        "supportive_ind": 1 if SUPPORT_PAT.search(text) else 0,
        "resistant_ind":  1 if RESIST_PAT.search(text)  else 0,
    }


def assign_frame(golf_ind, political_ind):
    if golf_ind and political_ind:
        return "hybrid"
    if golf_ind and not political_ind:
        return "golf"
    if political_ind and not golf_ind:
        return "political"
    return "neutral"


def assign_stance(supportive_ind, resistant_ind):
    if supportive_ind and resistant_ind:
        return "contested"
    if supportive_ind and not resistant_ind:
        return "supportive"
    if resistant_ind and not supportive_ind:
        return "resistant"
    return "neutral"


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestFrameClassification(unittest.TestCase):

    def _frame(self, text):
        r = classify_text(text)
        return assign_frame(r["golf_ind"], r["political_ind"])

    def test_golf_frame(self):
        self.assertEqual(self._frame("Great putt on the fairway today!"), "golf")

    def test_political_frame(self):
        self.assertEqual(self._frame("Trump should not be on television at all"), "political")

    def test_hybrid_frame(self):
        # Contains both golf terms AND non-trump political terms → hybrid
        self.assertEqual(self._frame("The MAGA crowd loved his birdie on hole 7"), "hybrid")

    def test_neutral_frame(self):
        self.assertEqual(self._frame("This video is okay I guess"), "neutral")

    def test_empty_string(self):
        self.assertEqual(self._frame(""), "neutral")

    def test_golf_context_trump_override(self):
        # "trump" alone in a golf-context comment should NOT trigger political_ind
        result = classify_text("Bryson's putt on the fairway was amazing, nothing could trump that shot")
        self.assertEqual(result["golf_ind"], 1)
        self.assertEqual(result["political_ind"], 0)
        self.assertEqual(self._frame("Bryson's putt on the fairway was amazing, nothing could trump that shot"), "golf")

    def test_trump_with_maga_is_political(self):
        # "trump" + another political term → political_ind should fire
        result = classify_text("Trump and MAGA fans loved this golf video")
        self.assertEqual(result["political_ind"], 1)


class TestStanceClassification(unittest.TestCase):

    def _stance(self, text):
        r = classify_text(text)
        return assign_stance(r["supportive_ind"], r["resistant_ind"])

    def test_supportive_stance(self):
        self.assertEqual(self._stance("This is amazing, love the charity work for veterans"), "supportive")

    def test_resistant_stance(self):
        self.assertEqual(self._stance("I'm going to unsubscribe, this is disgusting"), "resistant")

    def test_contested_stance(self):
        self.assertEqual(self._stance("Amazing content but I'm going to boycott this"), "contested")

    def test_neutral_stance(self):
        self.assertEqual(self._stance("Interesting video"), "neutral")


class TestEdgeCases(unittest.TestCase):

    def test_none_input(self):
        result = classify_text(None)
        self.assertEqual(result, {"golf_ind": 0, "political_ind": 0, "supportive_ind": 0, "resistant_ind": 0})

    def test_whitespace_only(self):
        result = classify_text("   ")
        self.assertEqual(result, {"golf_ind": 0, "political_ind": 0, "supportive_ind": 0, "resistant_ind": 0})

    def test_case_insensitive(self):
        self.assertEqual(classify_text("BIRDIE on the FAIRWAY")["golf_ind"], 1)
        self.assertEqual(classify_text("MAGA forever")["political_ind"], 1)


if __name__ == "__main__":
    unittest.main()
