# Evaluation

Does the skill actually improve writing, or does it just feel like it does? Here is a small, reproducible eval that tries to answer honestly.

## Headline

Four real PM writing tasks, each drafted twice: once **without** the skill (a plausible default draft) and once **with** it. An independent model scored every draft against a fixed rubric, 30 points per draft. The objective metrics (word count, AI-tell count) are computed in code, not judged.

Aggregate rubric score: **44/120 without, 115/120 with.** AI tells across the four messages fell from 33 to 0.

| Sample | Without | With | Δ | Words | AI-tells |
|---|---|---|---|---|---|
| Leadership update (metric drop) | 8/30 | 30/30 | +22 | 94 → 54 | 13 → 0 |
| Team note (process change) | 13/30 | 30/30 | +17 | 78 → 59 | 8 → 0 |
| Explainer (tech debt) | 16/30 | 26/30 | +10 | 67 → 82 | 0 → 0 |
| Customer launch email | 7/30 | 29/30 | +22 | 69 → 57 | 12 → 0 |
| **Aggregate** | **44/120** | **115/120** | **+71** | | |

Judge: GPT-4o via Azure OpenAI, temperature 0, run on 2026-06-14. Full per-dimension scores are in [`evals/results.json`](evals/results.json).

## How it's scored

Two tracks, so the result doesn't rest on one model's opinion.

**1. Objective metrics (code, in [`evals/run_evals.py`](evals/run_evals.py)).** No judgment, fully verifiable:
- Word count.
- AI-tell count: em-dashes, AI-vocabulary words (leverage, crucial, seamless, and so on), hedges (somewhat, potentially), and filler ("I wanted to reach out", "thrilled to announce").

**2. LLM-as-judge rubric.** An independent model scores each draft 0 to 5 on six dimensions (30 max): lead strength, concision, concreteness, clarity of the ask, voice (absence of AI tells), and reader fit. The judge sees only the audience and the draft. Temperature 0. The exact prompt lives in `run_evals.py`.

## An honest reading

- The "with" drafts win every sample, which is expected: the same author wrote both and knew the rubric. Read this as a demonstration of what the skill changes, not a controlled trial. The value is in the deltas and the samples below, which you can judge yourself.
- Concision is not the whole story. The explainer's "with" draft is *longer* (67 to 82 words) because it trades words for an analogy, and the judge still scored it higher on clarity and reader fit. The skill optimizes for the reader, not for word count.
- The AI-tell counts move on their own, independent of any model. That is the most tamper-proof signal here: 33 tells across four "without" drafts, 0 across the "with" drafts.

## The samples

### 1. Leadership update, metric drop (8 → 30)

Audience: leadership team (VP and skip-level).

**Without (8/30):**
> Hi team, I wanted to quickly reach out to flag that it's important to note our onboarding completion rate has been trending downward somewhat over the past quarter. There are a number of factors that could potentially be contributing to this, and I think it's crucial that we delve into the data to better understand the underlying dynamics. I believe there may be some opportunities here for us to leverage to improve the situation going forward. Happy to discuss further and align on next steps whenever works. Let me know your thoughts!

**With (30/30):**
> Onboarding completion fell 9% last quarter, from 71% to 62%. The drop is concentrated in mobile signups, where a new identity-check step is timing out. I want to ship a fix before Q3 planning locks on the 30th. That needs one engineer for a week. Can I pull Priya from the activation squad?

### 2. Team note, process change (13 → 30)

Audience: your product and engineering team.

**Without (13/30):**
> Hi all, As part of our ongoing commitment to excellence and continuous improvement, I am pleased to announce that we will be implementing a new weekly design review process. This initiative will serve as a crucial forum to foster collaboration, ensure alignment, and showcase the great work being done across the team. Attendance is expected. I am confident this will be a transformative step in our journey toward operational excellence. Please find a recurring invite on your calendars.

**With (30/30):**
> We keep catching design gaps late, usually in code review, where they are expensive to fix. So let's catch them earlier. Starting Thursday, we will spend 30 minutes every week looking at in-progress designs together. Bring something rough; that is the whole point. It is on your calendars. If a week is quiet, we will cancel it.

### 3. Explainer, technical debt (16 → 26)

Audience: non-technical business stakeholders.

**Without (16/30):**
> We have made the strategic decision to prioritize the remediation of accumulated technical debt in the current development cycle. While this will result in the deprioritization of certain customer-facing feature deliverables, it represents a necessary investment in the long-term scalability and maintainability of our platform architecture. Technical debt, if left unaddressed, can lead to increased systemic risk and a degradation of engineering velocity over time.

**With (26/30):**
> Picture renovating a house where every new room you add tangles the wiring a little more. Add enough rooms, and the lights start flickering in all of them. That is where our codebase is. We can ship the next feature now, but each one is getting slower and riskier to build on a foundation we keep patching. So we are spending two weeks rewiring before we add the next room. You will see fewer features this sprint, and faster, steadier ones after.

### 4. Customer launch email (7 → 29)

Audience: customers (general users of a SaaS product).

**Without (7/30):**
> We are thrilled and excited to announce the launch of our latest groundbreaking feature: Saved Views! This innovative new capability leverages cutting-edge functionality to empower users to optimize and streamline their workflows. With Saved Views, you can now seamlessly customize and curate your experience like never before. We are confident this will revolutionize the way you work. Log in today to explore all the exciting possibilities that await!

**With (29/30):**
> You can now save a view. Set up the filters and columns you reach for every morning, give it a name, and it is one click away next time. No more rebuilding the same report at 9am. Open any list, arrange it how you like, and hit Save view. Your saved views live in the left sidebar.

## Reproduce it

```bash
# Azure OpenAI
export AZURE_OPENAI_ENDPOINT="https://<resource>.openai.azure.com/"
export AZURE_OPENAI_KEY="<key>"
python3 evals/run_evals.py

# or any OpenAI-compatible API
export OPENAI_API_KEY="<key>"
python3 evals/run_evals.py
```

Standard library only, nothing to install. Scores write to `evals/results.json`. Want a tougher test? Add your own messages to `evals/samples.json` and rerun.
