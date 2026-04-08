# Project 3: Group Research Plan

**Course:** KIN 7518 Social Issues in Sport  
**Submission Format:** Markdown (.md)

---

## 1. Research Questions & Significance

Bryson DeChambeau's `Break 50` episode featuring Donald Trump is a strong case for studying how audiences react when a sport-media product becomes politically charged. On the surface, the content is golf and entertainment. But the presence of a former president, the patriotic symbolism in the comments, and the emphasis on the Wounded Warrior Project turn the episode into something larger than a simple golf video. It becomes a site where commenters negotiate whether they are watching golf content, political content, or a hybrid of both.

The dataset scale makes this case especially useful for a social-media-based research project. Across YouTube, Instagram, and X, the `B50` files contain 58,464 comments or replies tied to the same broader event. In our preliminary keyword-based exploration, political framing appeared in 21.8% of all comments, compared with 14.2% for golf-only framing, while another 14.8% combined both golf and political language. The platforms were not the same: X was heavily political (58.1% political), YouTube was more mixed (24.0% political; 17.6% hybrid), and Instagram contained many shorter or neutral reactions (76.4% neutral). These early patterns motivate three connected research questions:

**RQ1:** How do commenters frame Bryson DeChambeau's `Break 50` episode featuring Donald Trump across YouTube, Instagram, and X: as golf content, political content, or hybrid golf-politics content?

This question establishes the basic discourse landscape and tests whether the same sport-media event is framed differently across platforms.

**RQ2:** Which framing receives the strongest social validation within and across platforms, as indicated by likes and replies?

This question asks whether audiences reward golf-centered comments, politically centered comments, or comments that explicitly combine both frames.

**RQ3:** What language do commenters use to normalize or resist the presence of Trump and partisan politics within a golf-media setting, and how often is charity or patriotism used to justify that blending?

This question moves from counting frames to examining the rhetorical strategies commenters use when they approve of or object to the episode's political dimension.

### Why This Case Matters

This case matters because it captures the politicization of a space that might otherwise be treated as "just sports content." It speaks directly to themes reflected in the Project 3 readings, including celebrity politics (Street, 2018), partisan spillover into non-political spaces (Wang et al., 2024), and identity conflict among politically engaged sport fans (Larkin, 2025). Rather than measuring opinion through surveys, this project observes how people talk spontaneously in public comment spaces when politics enters a golf environment. That makes the case valuable for understanding how sport, media, celebrity, charity, and politics become entangled in everyday fan discourse.

---

## 2. Dataset Selection & Justification

**Dataset Choice:** [X] `B50`

**Justification:**  
The `B50` dataset is well suited to these research questions because it captures audience reactions to the same event across three major social platforms. This allows the group to compare how platform context shapes discourse without having to merge unrelated cases. The files contain comment text, engagement measures, and timestamps, which means the dataset supports both content analysis and descriptive comparison of social validation. Compared with the much larger `GENDER` dataset, `B50` is also more manageable for a week-by-week course project while still being large enough to produce meaningful patterns.

**Key files we plan to use:**

| File | Records | Key Variables |
|---|---:|---|
| `B50_YT_COMMENT.xlsx` | 45,623 | Comment text, likes, reply count, time, source |
| `B50_INS_COMMENT.xlsx` | 11,833 | Comment text, likes, reply count, time, post ID, post link |
| `B50_X_COMMENT.xlsx` | 1,008 | Comment text, likes, reply count, retweets, date, comment ID |

Together, these files provide 58,464 comments or replies. Their shared structure supports comment-level analysis by frame and platform, while their platform-specific metrics make it possible to compare relative engagement patterns.

---

## 3. Preliminary Variable Operationalization

| Construct | Operational Definition | Example Keywords | Data Source / Indicator |
|---|---|---|---|
| Golf framing | Comments whose language primarily references golf play, golf skill, equipment, course context, or golfer performance | `golf`, `swing`, `putt`, `driver`, `fairway`, `birdie`, `course`, `round`, `shot`, `PGA` | Keyword-based classification of comment text in all three `B50` files |
| Political framing | Comments whose language primarily references Trump, presidency, elections, partisan identity, or explicitly political evaluation | `Trump`, `president`, `POTUS`, `MAGA`, `election`, `Biden`, `Republican`, `Democrat` | Keyword-based classification of comment text |
| Hybrid golf-politics framing | Comments containing both golf and political language, explicitly blending the sport event and the political figure | `Trump` + `golf`, `president` + `round`, `MAGA` + `shot`, etc. | Joint keyword matches across golf and political dictionaries |
| Supportive normalization | Language that treats the episode as acceptable, admirable, or worthwhile by appealing to charity, patriotism, or the idea that it is "just golf" | `charity`, `Wounded Warrior`, `veteran`, `honor`, `donate`, `great cause`, `just golf`, `giving back` | Second-layer keyword coding of stance |
| Resistant / disapproving language | Language objecting to the political presence, criticizing the creator, or expressing withdrawal or disapproval | `unsubscribe`, `boycott`, `disappointed`, `terrible`, `keep politics out`, `wrong`, `disgusting` | Second-layer keyword coding of stance |
| Social validation | The degree to which the comment community responds to a comment | Likes and reply counts in each platform file |

**Lexicon development and validation:** We will use curated keyword lists for golf, politics, supportive normalization, and resistance, then refine them iteratively after manual review. At least two group members will independently inspect a random sample of approximately 100 to 150 comments to identify systematic misclassification, especially short comments, sarcasm, and comments where patriotism overlaps with partisanship.

---

## 4. Proposed Analyses

The three analyses below are designed as a connected sequence. Analysis 1 establishes how the event is framed across platforms. Analysis 2 examines which framings receive stronger community validation. Analysis 3 moves inside the comments to identify the rhetorical logic commenters use when they defend or resist politics in a golf context.

### Analysis 1: Cross-Platform Framing Distribution (RQ1)

| Step | Description |
|---|---|
| 1 | Classify every comment as golf, political, hybrid golf-politics, or neutral using keyword lexicons |
| 2 | Report frame counts and percentages overall and separately for YouTube, Instagram, and X |
| 3 | Compare each platform's framing profile to identify where politicization is strongest |
| 4 | If time permits, compare top-level comments and replies to see whether reply threads become more political than original comments |

**What this tells us:** Whether the same sport-media event is interpreted differently depending on platform context. In our preliminary exploration, political framing was the most common classifiable category overall (21.8%), but this was driven heavily by X, where 58.1% of comments were political. YouTube was more mixed, with 24.0% political and 17.6% hybrid comments, while Instagram had a large neutral share (76.4%), suggesting many short reactions that do not clearly signal a frame.

### Analysis 2: Social Validation by Frame (RQ2)

| Step | Description |
|---|---|
| 1 | For each platform, compute average likes, median likes, and average replies for each frame |
| 2 | Compare frame shares among higher-engagement comments to see which frames are over-represented |
| 3 | Normalize engagement within platform so that YouTube, Instagram, and X are not treated as directly equivalent environments |
| 4 | Extract top-engagement examples from each frame for interpretation |

**What this tells us:** Whether audiences reward pure golf framing, pure political framing, or blended golf-politics framing. Preliminary results suggest that hybrid comments are especially important: across the combined dataset, hybrid comments make up 14.8% of all comments but 23.8% of comments with 10 or more combined likes and replies. On YouTube in particular, hybrid comments received the strongest average validation in the exploratory pass (30.91 average likes and 0.81 average replies), exceeding golf-only and political-only comments.

### Analysis 3: Supportive Normalization vs Resistance (RQ3)

| Step | Description |
|---|---|
| 1 | Apply a second-layer stance classification: supportive, resistant, contested, or neutral |
| 2 | Count supportive and resistant comments overall and by frame |
| 3 | Rank the most frequent supportive and resistant keywords |
| 4 | Extract representative examples showing how charity, patriotism, and "keep politics out" language function rhetorically |

**What this tells us:** How commenters justify or reject the political blending. In the exploratory pass, explicit stance language was relatively rare, but supportive normalization slightly outnumbered resistance overall (1,026 supportive vs 802 resistant comments). Supportive language centered on terms such as `charity`, `Wounded Warrior`, `veteran`, `honor`, and `donate`, while resistant language centered on terms such as `wrong`, `terrible`, `unsubscribe`, `ridiculous`, and `disgusting`. This suggests that much of the approval work is done through charity and patriotic framing, whereas resistance is expressed more through moral objection and audience withdrawal.

### Optional Extension: Platform-Specific Comment Cultures

If time permits, a supplementary comparison of platform norms could be added. For example, X may function as the most overtly political discussion space, while YouTube may be the most important site for hybrid normalization and Instagram may function primarily as a low-text reaction space.

---

## 5. Limitations & Potential Issues

1. **Keyword classification is blunt.** It captures explicit language but misses irony, sarcasm, and context. A comment praising a "great cause" may still carry political criticism, and a comment about Trump may be descriptive rather than political in stance.

2. **The neutral category is still large.** In the exploratory pass, 49.1% of comments were neutral, meaning they lacked clear golf or political keywords. Many of these appear to be short reactions, emojis, or vague statements that are difficult to interpret systematically.

3. **Platform metrics are not identical.** Likes and replies do not mean exactly the same thing on YouTube, Instagram, and X. Direct raw comparison across platforms should therefore be treated cautiously and supplemented with within-platform normalization.

4. **One event, one political figure.** This is a focused case study of one highly visible media event involving Donald Trump. The patterns may not generalize to all sport-politics cases or to golf content more broadly.

5. **The X file is much smaller than the YouTube and Instagram files.** X appears especially political in the exploratory pass, but the smaller comment count means some engagement estimates on that platform may be unstable.

---

## 6. Ethical Considerations

**Privacy:**  
All data consist of publicly posted comments. We will not attempt to identify commenters, profile individual users, or reproduce user names in the report.

**Harm:**  
The topic involves political polarization and patriotic language. To avoid amplifying hostility, the project will present comment examples only as brief anonymized excerpts and will frame findings analytically rather than normatively.

**Bias:**  
The coding rules reflect researcher judgment about what counts as golf, politics, support, and resistance. We will address this through transparent keyword documentation, manual validation, and clear acknowledgment that classification is interpretive rather than purely objective.

---

## 7. Group Role Assignments

| Role | Group Member | Primary Responsibilities |
|---|---|---|
| Data & Classification Lead | Paul Son | File organization, keyword dictionary setup, first-pass coding workflow, exploratory count verification |
| Cross-Platform Analyst | Qiaoyin Tan | Platform comparison tables, descriptive statistics, RQ1 write-up |
| Theory & Interpretation Lead | Lauryn Porter | Connect findings to sport-politics, celebrity politics, and fan identity literature |
| Visualization & Reporting Lead | Jolyn Seow | Create charts, check percentages, align narrative with visuals, formatting review |
| Validation Support | Paul Son and Qiaoyin Tan | Manual review of coded comments, disagreement checks, final QA before submission |

---

## 8. Data Visualization Plan

**Primary Goal:**  
Show how a golf-media event becomes differently politicized across platforms, and whether blended golf-politics framing receives disproportionate community validation.

**Visualization Descriptions:**

1. **Frame Distribution by Platform (RQ1):** A stacked bar chart showing golf, political, hybrid, and neutral shares for YouTube, Instagram, and X.
2. **Overall Framing Landscape (RQ1):** A bar chart showing total counts and percentages across the full `B50` dataset.
3. **Social Validation by Frame (RQ2):** A grouped bar chart comparing average likes and replies by frame within each platform, plus a secondary chart showing each frame's share of high-engagement comments.
4. **Supportive vs Resistant Language (RQ3):** A paired horizontal bar chart comparing the most frequent supportive keywords with the most frequent resistant keywords.

**Design Rationale:**  
These visuals keep the project readable and course-appropriate while still telling a coherent story. The stacked platform chart highlights comparison, the engagement chart shows social reward patterns, and the paired keyword chart makes rhetorical contrast immediately visible.

**Verification Methods:**  
- [X] Spot-checked row totals against the source Excel files  
- [X] Verified preliminary frame counts sum to the total dataset size  
- [X] Reviewed column mappings for each platform separately  
- [ ] Final visualization files embedded or linked  

**Brief Interpretation (2-3 sentences):**  
The visualizations will show whether commenters treat the episode mainly as golf, politics, or a blended form of both, and whether that pattern changes by platform. They will also show whether charity-centered approval and anti-politics resistance operate as competing rhetorical strategies within the same comment ecosystem.

---

## 9. AI-Assisted Work Documentation & Verification

**Tools Used:**  
OpenAI Codex was used to inspect the dataset structure, draft keyword categories, run an exploratory PowerShell-based classification pass, and help draft the research plan.

**Verification Methods:**

**Code Explanation:**  
- [X] Exploratory classification logic reviewed for correct column mapping across all three files  
- [X] Keyword lists checked manually against sample comments  
- [ ] Final reproducible analysis script prepared for the full project workflow  

**Output Validation:**  
- [X] Verified record totals against the original Excel files  
- [X] Checked that frame counts sum correctly within each platform and overall  
- [X] Treated all current counts as exploratory rather than final published results  
- [X] Reviewed all AI-assisted writing for fit with course expectations and research goals  

**Iterative Refinement:**  
- Number of prompt iterations before usable output: 3-4  
- Key refinements made: narrowed from several possible datasets to `B50`, shifted from a single yes-or-no political question to a three-part narrative about framing, engagement, and rhetorical justification, and added platform comparison as the central design feature

**Learning Reflection:**  
Using AI for dataset familiarization and exploratory counting helped identify the most workable case and a coherent set of connected research questions. At the same time, the process reinforced that keyword coding is only a first step: human review is necessary to interpret sarcasm, platform norms, and the overlap between patriotism, charity, and politics.

---

## Submission Checklist

- [X] All sections completed  
- [X] Research questions are specific, justified, and connected as a narrative  
- [X] Dataset choice is clearly explained  
- [X] Constructs are operationalized  
- [X] Proposed analyses are linked to RQs  
- [X] Limitations and ethics are addressed  
- [X] Group roles are assigned  
- [X] Data visualization plan is included  
- [X] AI-assisted work is documented  
- [X] Preliminary dataset profiling completed  
- [ ] Final visualizations embedded or linked  
- [ ] All group members have reviewed and approved the final draft  

Street, J. (2018). *What is Donald Trump? Forms of "Celebrity" in Celebrity Politics.*

Larkin, B. (2025). *Identity Conflict Among Politically Engaged Sport Fans: Implications for Fan Loyalty.*

Wang, et al. (2024). *The Growing Partisan Politicization of Non-Political Online Spaces: A Mixed-Method Analysis of News App Reviews on Google Play.*
