# Merge eval: analog-ui vs sketchbook-ui + medium-first-design

**Question:** after merging `sketchbook-ui` and `medium-first-design` into `analog-ui`, is quality
the same or better?
**Answer:** better, but only after fixes the eval exposed. The first merged draft lost 2 of 3 briefs.
The shipped version won all 6 blind judgements and scored higher on every criterion.

Run on 28 Oct 2026. The briefs use fictional products (Tidewater, Northpay, Ledgerly).

## 1. Coverage: did anything get lost?

| Check | Result |
|---|---|
| Guidance items in the two old skills (lines, rules, table rows) | 162 |
| Carried over word for word | 143 |
| Carried over with small wording changes (≥90% of words) | 15 |
| Flagged as missing | 4, all deliberate rewrites: a table header, a lessons heading, the old examples list, and "blinking forever" (reworded) |
| Files (CSS, templates, scripts, samples) | 30. 26 identical, 4 changed only in paths and links, 0 lost |

A first pass found that three medium names ("flight recorder log", "air-traffic flight strips",
"announce something energetic") had been dropped from the medium table. They were restored before
the A/B test.

## 2. Routing: does the agent still pick the right skill?

Four routers (two model tiers × old/new skill lists) ran 30 prompts each against 8 real competing
skills: 12 asking for a specific medium, 5 open "make it not generic", 13 that should go elsewhere.

| | Old (2 skills) | New (analog-ui) |
|---|---|---|
| Medium prompts routed to the design skill | 12/12 | 12/12 |
| Medium named in the call, so it routes straight there | 4/24 (the old skills had no argument) | 24/24 |
| Open "make it distinctive" prompts | 6/6 on the light model, 5/6 on the strong model | 6/6 after the description fix |
| Prompts that belong elsewhere (glass, Excalidraw, CSS bug…) | 0 false grabs | 0 false grabs |

The first router round showed one miss: the strong model sent "investor update that doesn't look
like a template" to `frontend-design`. The description was widened to cover "update" and "report",
and the second round caught it.

## 3. Context cost: how much does the agent read?

| Job | Old | New |
|---|---|---|
| Always in context (skill descriptions) | 1,413 B (two skills) | 855 B (−39%) |
| Non-sketchbook medium (method + guidance) | 16,008 B | 14,225 B on average (method + one MEDIUM.md, −11%) |
| Sketchbook job | 6,960 B | 20,182 B |

The sketchbook job now reads more, because it gets the full method as well as the kit. That
buys the eval's biggest gains (the one-bold-move and phone rules). Every other medium reads less,
because the agent loads one medium file instead of the whole library.

## 4. Blind A/B: does the output look as good?

Each brief was built twice, once per skill, by separate agents that could only see their own skill.
Two judges (different model families) scored screenshots at 1280px and 390px without knowing which
was which. Seven criteria, 1–5.

**Round 1 (first merged draft):**

| Brief | Medium | Winner (both judges) |
|---|---|---|
| Stars milestone | sketchbook | **new** |
| Incident report | lab notebook | old |
| Roadmap | blueprint | old |

Mean 4.05 new vs 4.43 old: **a regression**. Both losses traced to the merged skill's examples,
which builders copied. The lab-notebook example used two bold moves, and the blueprint example
scrolled sideways on phones.

**Fixes before round 2:**
- Both examples were corrected.
- The method now comes before any example ("write your own mapping table first").
- Wide content is redrawn as a stack on phones, never scrolled sideways.
- New rules: one bold move, which must be visible on a phone; no invented convention data
  (page numbers, stamps); a precise chart label format; a render recipe that waits for fonts.

**Round 2 (shipped version), the two lost briefs re-run with fresh builders on both sides:**

| Brief | Judge 1 | Judge 2 |
|---|---|---|
| Incident report | **new** | **new** |
| Roadmap | **new** | **new** |

**Final, shipped skill vs the old pair** (milestone from round 1, the others from round 2;
6 judgements):

| Criterion | Old | New |
|---|---|---|
| Medium feels real | 3.83 | **4.50** |
| Fits the content | 4.50 | **4.67** |
| One bold move | 3.00 | **4.00** |
| Readable in 3 seconds | 4.17 | **4.67** |
| Craft | 3.67 | **4.17** |
| Phone | 3.33 | **4.50** |
| Facts exact | 4.00 | **4.83** |
| **Mean** | **3.79** | **4.48** |
| Preferred | 0 / 6 | **6 / 6** |

## Caveats
- Small sample: 3 briefs, 2 judges, one build per side. LLM builds vary run to run; treat this as
  "no regression, likely better", not a precise effect size.
- Round 2 tested a skill revised after round 1. The old side was re-run fresh at the same time, so
  each side got a second attempt, but the fixes were informed by round 1.
- The judges saw screenshots, not live pages, so interaction and accessibility are covered by the
  separate automated suite (`tests/run_samples.py`), which both versions' samples pass.
