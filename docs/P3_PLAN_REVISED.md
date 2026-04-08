# Project 3: Group Research Plan — Revised

**Course:** KIN 7518 Social Issues in Sport  
**Submission Format:** Markdown (.md)  
**Dataset:** B50 (YouTube · Instagram · X)

> **Revision note:** This version strengthens methodological precision, distinguishes framing from stance, formalizes the validation plan, and adds a GitHub reproducibility section. Substantive topic, dataset choice, and three research questions are unchanged.

---

## 1. Research Questions & Significance

Bryson DeChambeau's *Break 50* episode featuring Donald Trump constitutes a productive site for studying audience discourse at the intersection of sport, celebrity, and political identity. Although the video presents itself as golf entertainment, the presence of a former president, the invocation of the Wounded Warrior Project, and the patriotic register of audience commentary transform the episode into a space where commenters publicly negotiate the meaning and legitimacy of political figures in sport-media contexts. This project examines that negotiation across three major social platforms, using structured content analysis of naturally occurring comment text.

The dataset scale and multi-platform design strengthen the case's suitability for a course research project. Across YouTube, Instagram, and X, the B50 files contain 58,464 comments or replies tied to the same event. Preliminary dictionary-assisted classification suggests meaningful platform variation: X appears to concentrate the most overtly political commentary, YouTube shows a greater share of hybrid golf-politics framing, and Instagram contains a substantially larger proportion of brief or neutral reactions. These patterns are treated as exploratory indicators that motivate the following three research questions.

**RQ1:** How do commenters frame Bryson DeChambeau's *Break 50* episode featuring Donald Trump across YouTube, Instagram, and X — as golf content, political content, or a hybrid of both?

**RQ2:** Which framing receives the strongest social validation within and across platforms, as indicated by platform-normalized engagement (likes and replies)?

**RQ3:** What rhetorical strategies do commenters employ to normalize or resist the presence of Trump and partisan politics in a golf-media setting, and how frequently is charity or patriotic language deployed to justify that blending?

### Why This Case Matters

This case connects directly to course themes of celebrity politics (Street, 2018), partisan spillover into non-political media spaces (Wang et al., 2024), and identity conflict among politically engaged sport fans (Larkin, 2025). Unlike survey-based opinion research, this project observes spontaneous public discourse in response to a specific media event, enabling naturalistic analysis of how sport, celebrity, charity, and political identity become discursively entangled.

---

## 2. Dataset Selection & Justification

**Dataset choice:** B50

| File | Records | Key Variables |
|---|---:|---|
| `B50_YT_COMMENT.xlsx` | 45,623 | text, user, likes, replies, time, source (video ID) |
| `B50_INS_COMMENT.xlsx` | 11,833 | text, user, likes, replies, time, comment ID, post ID |
| `B50_X_COMMENT.xlsx` | 1,008 | text (contents), username, likes, reply counts, date, comment ID |

The B50 dataset captures reaction to a single, well-defined media event across three structurally distinct platforms, enabling controlled cross-platform comparison. The three files share sufficient overlap in available fields (text, engagement, user, time) to support both comment-level content analysis and descriptive engagement comparison. The dataset is large enough to detect distributional patterns while remaining computationally manageable within a semester-long course project.

---

## 3. Variable Operationalization

### 3.1 Construct Definitions

Framing and stance are treated as analytically separate dimensions following the conceptual distinction from framing theory (Entman, 1993) and stance analysis (Biber & Finegan, 1988):

- **Framing** concerns *what the comment is about* — specifically, whether the comment orients to the episode as golf content, as political content, or as an explicit combination of both.
- **Stance** concerns *what position the comment takes* — specifically, whether the commenter approves of, objects to, or remains neutral toward the political or blended character of the episode.

### 3.2 Operationalization Table

| Construct | Operational Definition | Classification Method |
|---|---|---|
| **Golf framing** | Comment primarily references golf activity, golfer performance, golf equipment, course context, or golf competition | Lexicon-based indicator: presence of golf-domain keyword(s) |
| **Political framing** | Comment primarily references Trump, the presidency, partisan identity, elections, or explicitly political evaluation | Lexicon-based indicator: presence of political-domain keyword(s) |
| **Hybrid framing** | Comment contains both golf and political language, explicitly blending the sport event and the political figure | Joint indicator: both golf and political lexicons triggered |
| **Neutral framing** | Comment contains neither golf nor political language; typically short reactions, emojis, or generic expressions | Default when no framing indicator is triggered |
| **Supportive normalization** | Language approving of or normalizing the episode's political dimension by appealing to charity, patriotism, or the framing of golf as apolitical | Second-layer lexicon indicator on stance dimension |
| **Resistant/disapproving** | Language objecting to political presence in a golf setting, expressing viewer withdrawal, or evaluating the episode negatively on political grounds | Second-layer lexicon indicator on stance dimension |
| **Social validation** | Degree to which a comment receives community endorsement | Within-platform percentile rank of total engagement (likes + replies) |

### 3.3 Frame Variable (Mutually Exclusive)

The final `frame` variable collapses indicators into four mutually exclusive categories using this priority rule:

- `hybrid` → golf AND political indicators both triggered
- `golf` → golf triggered, political not triggered
- `political` → political triggered, golf not triggered
- `neutral` → neither triggered

### 3.4 Stance Variable (Mutually Exclusive)

The final `stance` variable uses this priority rule:

- `contested` → supportive AND resistant both triggered (warrants manual review)
- `supportive` → supportive triggered, resistant not
- `resistant` → resistant triggered, supportive not
- `neutral` → neither triggered

### 3.5 Lexicon Development

Four curated keyword lexicons were developed through: (a) review of sport-politics and social-media framing literature, (b) frequency inspection of raw comment tokens, and (c) iterative manual refinement. All keyword lists are archived in `data/cleaned/codebook_keywords.txt`. Limitations: the lexicons do not capture irony, sarcasm, or context-dependent meaning; single-mention of "Trump" is treated as a political signal regardless of evaluative intent.

---

## 4. Data Cleaning

Prior to classification, all three Excel files were standardized into a single comment-level dataset using script `01_load_clean.py`. Key cleaning steps:

1. **Column harmonization** — Platform-specific column names were mapped to a unified schema (`platform`, `text`, `user`, `likes`, `replies`, `time`, `comment_id`, `post_id`). All mapping decisions and ambiguities are documented in the cleaning log.
2. **Numeric coercion** — `likes` and `replies` were coerced to numeric using `pd.to_numeric(errors='coerce')`; non-numeric placeholders were converted to `NaN` and logged.
3. **Missing text removal** — Rows with absent, empty, or whitespace-only comment text were removed.
4. **Deduplication** — Rows sharing identical values across *platform*, *text*, *user*, and *time* were treated as export artifacts and removed; cross-platform identical comments were retained.
5. **Whitespace trimming** — Leading and trailing whitespace was stripped from all string fields.
6. All cleaning decisions are logged to `data/cleaned/cleaning_log.txt`.

---

## 5. Proposed Analyses

### Analysis 1 — Cross-Platform Framing Distribution (RQ1)

1. Apply dictionary-assisted classification to all comments using the four keyword lexicons.
2. Compute frame counts and percentages overall and separately by platform.
3. Compare platform-level framing profiles to identify where politicization is most concentrated.
4. If time permits, compare top-level comments and reply threads to detect escalation patterns.

*What this addresses:* Whether the same sport-media event is framed differently depending on platform context, and whether YouTube, Instagram, and X constitute distinct discursive environments for the same content.

### Analysis 2 — Social Validation by Frame (RQ2)

1. Compute within-platform engagement metrics (mean likes, median likes, mean replies, median replies, total engagement = likes + replies).
2. Assign each comment a within-platform percentile rank of total engagement.
3. Identify high-engagement comments (≥ 90th percentile within platform) and examine their frame distribution.
4. Compare median total engagement across frame categories within each platform.
5. Extract and review qualitative examples from high-engagement comments in each frame.

*Engagement note:* Because engagement distributions are highly right-skewed, analyses emphasize median values and percentile-based thresholds rather than means or fixed raw cutoffs, which would be non-comparable across platforms.

### Analysis 3 — Supportive Normalization vs Resistance (RQ3)

1. Apply second-layer stance classification to all comments (supportive / resistant / contested / neutral).
2. Count and compare stance categories overall and by platform.
3. Tabulate the most frequent keywords within supportive and resistant stances.
4. Extract representative excerpts illustrating how charity, patriotism, and "keep politics out" language function rhetorically.

*What this addresses:* How commenters justify or reject the blending of politics and golf, and whether charity/patriotic framing is the dominant rhetorical resource for normalization.

---

## 6. Validation Plan

Lexicon-based classification constitutes preliminary, exploratory coding only. Manual validation will proceed as follows:

1. **Stratified sampling** — A random sample of approximately 100–150 comments will be drawn proportionally from each platform and from each frame category.
2. **Independent coding** — Two group members will code frame and stance for each sampled comment independently, using the codebook in `data/cleaned/codebook_keywords.txt`.
3. **Reliability assessment** — Inter-rater reliability will be computed using Cohen's kappa. A kappa ≥ 0.70 is the minimum threshold for acceptable agreement before proceeding to final reporting.
4. **Discrepancy resolution** — Disagreements will be discussed and resolved through consensus; patterns of disagreement will be used to refine lexicons.
5. **Priority review targets** — `hybrid`, `contested`, and high-engagement top-10% comments will be prioritized in the validation sample.

---

## 7. Limitations & Potential Issues

1. **Dictionary-assisted classification is sensitive to vocabulary coverage.** It captures explicit keyword signals but systematically misses irony, sarcasm, and context-dependent meaning. Manual validation is required to estimate the false-positive and false-negative rates.

2. **The neutral category is substantial.** A large share of comments — particularly on Instagram — may not contain clear golf or political signals, either because they are short reactions (emojis, brief affirmations) or because they use domain-relevant language that is not yet captured by the lexicons.

3. **Platform metrics are structurally non-equivalent.** Likes and replies do not carry the same social meaning across YouTube, Instagram, and X. Within-platform normalization addresses this, but direct cross-platform engagement comparisons remain interpretively limited.

4. **Single-event, single-political-figure design.** Findings are specific to a highly visible, politically exceptional media event. Patterns may not generalize to other sport-politics cases or to golf content more broadly.

5. **X sample is substantially smaller.** At 1,008 comments, the X file is roughly 45 times smaller than the YouTube file. Percentile-based engagement estimates for X may be less stable, and platform-level comparisons should be interpreted with appropriate caution.

6. **"Trump" as keyword.** Including `trump` in the political lexicon captures mentions that are purely descriptive (e.g., "I didn't know Trump played golf") as well as evaluative ones. This is flagged explicitly in the classification log and is a priority target for manual review.

---

## 8. Ethical Considerations

**Privacy:** All data consist of publicly posted comments. User names are retained in the cleaned dataset for deduplication purposes only and are not reported in any public output.

**Anonymized reporting:** Comment text is presented in the written report only as brief, anonymized or paraphrased excerpts. No full comment text is published or attributed to specific users.

**No raw data published:** Raw and comment-level cleaned data are excluded from the GitHub repository in compliance with platform terms of service and course ethics guidelines.

**Analytical framing:** Findings are presented descriptively and analytically. The project does not endorse or critique any political figure or position.

**Bias and transparency:** Keyword lists reflect researcher judgment about what constitutes golf, political, supportive, and resistant language. This is inherently interpretive; we address it through transparent codebook documentation, manual validation, and clear acknowledgment of classification limitations.

---

## 9. Group Role Assignments

| Role | Member | Primary Responsibilities |
|---|---|---|
| Data & Classification Lead | Paul Son | File organization, lexicon development, `01_load_clean.py`, `02_classify.py`, cleaning log review |
| Cross-Platform Analyst | Qiaoyin Tan | Descriptive statistics, platform comparison tables, `03_descriptive_stats.py`, RQ1 write-up |
| Theory & Interpretation Lead | Lauryn Porter | Connect findings to sport-politics and celebrity politics literature; draft discussion sections |
| Visualization & Reporting Lead | Jolyn Seow | `04_visualize.py`, figure review, formatting, final narrative alignment with visuals |
| Validation Support | Paul Son & Qiaoyin Tan | Manual coding of validation sample, kappa computation, lexicon refinement |

---

## 10. Data Visualization Plan

1. **Frame Distribution by Platform (RQ1):** Stacked horizontal bar chart showing golf, political, hybrid, and neutral percentage shares for each platform.
2. **Engagement by Frame, Within Platform (RQ2):** Three-panel grouped bar chart showing median total engagement by frame for YouTube, Instagram, and X separately.
3. **Supportive vs Resistant Keywords (RQ3):** Dual horizontal bar chart comparing the most frequent keywords within supportive and resistant stances.

All figures include exploratory caveats in titles and are generated automatically by `04_visualize.py` from the classified dataset.

---

## 11. GitHub Reproducibility

All code, cleaned data, keyword codebooks, summary tables, figures, and documentation are organized in a structured GitHub repository. The workflow is fully reproducible by running `python run_all.py` from the project root. Raw data files are excluded from the repository; a data manifest in `docs/` describes file sources, collection dates, and record counts.

**Repository contents:**

| Folder/File | Contents |
|---|---|
| `data/raw/` | Raw Excel files (excluded from GitHub; `.gitkeep` placeholder) |
| `data/cleaned/` | Unified CSV, classified CSV, keyword codebook, cleaning/classification logs |
| `scripts/` | Five numbered analysis scripts |
| `tables/` | Eight summary CSV tables |
| `figures/` | Three publication-ready PNG figures |
| `docs/` | Methods summary (auto-generated), project documentation |
| `run_all.py` | Single-command pipeline runner |
| `requirements.txt` | Python package dependencies |
| `.gitignore` | Excludes raw data, cache, and OS artifacts |
| `README.md` | Project overview, reproduction instructions, ethics note |
| `LICENSE` | MIT License (code only) |

---

## 12. AI-Assisted Work Documentation

**Tools used:** Google Antigravity (Gemini-based agentic coding assistant) was used to inspect dataset column structures, draft and debug all Python scripts, produce the README and project file structure, and assist with drafting this research plan revision.

**Verification:** All code was reviewed for correct column mapping, accurate keyword logic, and faithful reporting of analytical decisions. All outputs are treated as exploratory until manual validation is complete.

**Iterative process:** Approximately 3–4 prompt iterations were used to refine the research questions from a general interest in "audience reaction" to the current three-part narrative linking framing, engagement, and rhetorical stance.

---

## Submission Checklist

- [x] All sections completed
- [x] Research questions are specific, justified, and narratively connected
- [x] Framing and stance are defined and kept analytically separate
- [x] Dataset choice is clearly explained
- [x] Constructs are operationalized with explicit coding rules
- [x] Data cleaning steps are documented
- [x] Manual validation plan with kappa threshold is specified
- [x] Proposed analyses are linked to RQs
- [x] Engagement analysis emphasizes within-platform normalization
- [x] Limitations and ethics are addressed
- [x] Group roles are assigned
- [x] Visualization plan is included with design rationale
- [x] GitHub reproducibility section is included
- [x] AI-assisted work is documented
- [ ] Manual validation sample coded and kappa computed
- [ ] Final visualizations reviewed and approved by full team

---

## Changes Made in This Revision

| Change | Rationale |
|---|---|
| Added explicit **framing vs stance** definitions (§3.1) | Previous plan conflated what a comment is *about* with what *position* it takes; this distinction is foundational in content analysis |
| Replaced "keyword classification" with **lexicon-based coding** and **dictionary-assisted classification** | More precise terminology aligned with established computational content analysis methods |
| Added formal **data cleaning section** (§4) with six explicit steps | Improves methodological transparency and reproducibility |
| Added formal **validation plan** (§6) with stratified sampling, independent coding, and Cohen's kappa threshold | Previous plan mentioned spot-checking; this formalizes it as a methodological step |
| Replaced mean-based engagement description with **within-platform percentile rank** and **median-first** framing | Engagement distributions are known to be right-skewed; percentile approach avoids arbitrary raw thresholds |
| Framed all preliminary findings with **"exploratory"** and **"preliminary"** language | Previous plan stated percentages as if they were final results; they are pre-validation estimates |
| Added **GitHub reproducibility section** (§11) with table of all repository contents | Addresses course emphasis on reproducible, documented research |
| All analytical decisions now **explicitly flagged** in code comments and logs | Supports peer review and instructor verification of methodology |

---

## References

Biber, D., & Finegan, E. (1988). Adverbial stance types in English. *Discourse Processes*, 11(1), 1–34.

Entman, R. M. (1993). Framing: Toward clarification of a fractured paradigm. *Journal of Communication*, 43(4), 51–58.

