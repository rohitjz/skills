---
name: council
description: "Run a Karpathy-style LLM Council on any PM or technical decision. Spawns 3-5 parallel perspectives (Operator, Customer Advocate, Skeptic, Strategist, Builder), runs adversarial review, and synthesizes a recommendation with consensus, dissent, and risks. Use when facing a hard decision, needing multiple perspectives, wanting to stress-test a plan, or saying 'council' or 'what does the council think'."
user-invocable: true
argument-hint: '"[your question]" [--full] [--pm|--tech]'
allowed-tools: Agent, Read, Glob, Grep, Write, AskUserQuestion
---

# /council -- Decision Council

Run a multi-perspective deliberation council on any PM or technical decision. Inspired by Karpathy's LLM Council, adapted for Claude Code with persona-driven diversity.

## Step 0: Parse Input

Extract the question and flags from the user's input.

- If `--full` flag is present, set mode to FULL.
- If `--pm` flag is present, set domain hint to PM.
- If `--tech` flag is present, set domain hint to TECH.
- If no question is provided, use AskUserQuestion: "What decision does the council need to deliberate?"

**Auto-escalation to FULL mode:** If the question contains any of these words, automatically use FULL mode: strategy, reorg, cancel, pivot, bet, migrate, reorganize, acquisition, sunset, deprecate, kill, shut down.

Tell the user which mode was selected (Quick or Full) and why.

## Step 1: Gather Context

**Optional PM OS integration.** If the user has a PM OS setup, read these memory files in parallel for context injection. If any file does not exist, skip it silently and proceed with whatever context is available. The council works fine without PM OS; the memory files just make its output more tailored.

1. Read `PM_OS/.claude/memory/identity.md` (user's role and org)
2. Read `PM_OS/.claude/memory/work-context.md` (active projects, stakeholders, sprint)
3. Read `PM_OS/.claude/memory/goals.md` (product and career goals)
4. Read `PM_OS/.claude/memory/preferences.md` (output format, writing style)

**Stakeholder detection (optional).** If a `PM_OS/knowledge/people/` directory exists, scan the question for names that match people files there. If any stakeholder names are detected, read their people files. Extract their communication preferences, pushback patterns, "What They Care About", and "How to Get a Yes" sections. If the directory does not exist, skip this step.

**Without PM OS:** Just ask the user one sentence about their role and the stakes of the decision. That single sentence becomes the context block. Do not block the council on missing files.

Build a CONTEXT BLOCK that will be injected into every subagent prompt:

```
CONTEXT ABOUT THE DECISION-MAKER:
- Role: [from identity.md]
- Active projects: [from work-context.md]
- Current goals: [from goals.md]
- Stakeholders referenced: [from people files, if any, including their key traits]
```

## Step 2: Select Personas

**FULL mode (5 personas + moderator):** All five personas participate.
1. The Operator (systems, dependencies, second-order effects)
2. The Customer Advocate (user experience, adoption, empathy)
3. The Skeptic (objections, failure modes, assumptions)
4. The Strategist (positioning, opportunity cost, 18-month view)
5. The Builder (implementation reality, first sprint, technical risk)

**QUICK mode (3 personas):** Always include The Operator and The Skeptic. Select the third based on context:
- If `--pm` or question is about users, customers, adoption: add The Customer Advocate
- If `--tech` or question is about architecture, migration, tooling: add The Builder
- If question is about positioning, competitive, long-term: add The Strategist
- Default (ambiguous): add The Customer Advocate

## Step 3: Dispatch Stage 1 (Parallel Opinions)

For each selected persona, read its persona file from `~/.claude/skills/council/personas/` and spawn a subagent using the Agent tool. **All subagents must be dispatched in a single message for parallel execution.**

Each subagent prompt follows this structure:

```
[Contents of the persona .md file]

CONTEXT ABOUT THE DECISION-MAKER:
[Context block from Step 1]

THE QUESTION:
[User's question, verbatim]

INSTRUCTIONS:
- Lead with your position in one sentence (support / oppose / conditional).
- Give your single strongest argument (not three).
- Name the biggest risk you see from your perspective.
- Total response: 250-300 words maximum.
- Be direct and opinionated. Do not hedge with "it depends" unless you genuinely see a binary fork. If you hedge, name both sides of the fork.
- Do not summarize the question back. Start with your position.
```

Use `model: "sonnet"` for each subagent to keep costs low. The synthesis (Step 5) runs in the main Opus thread.

Collect all responses. Label them for the moderator as "Member 1" through "Member N" (mapping persona names to numbers internally).

## Step 4: Stage 2 -- Adversarial Review (FULL mode only)

Skip this step entirely in QUICK mode.

In FULL mode, read `~/.claude/skills/council/moderator.md` and spawn a single Moderator subagent (model: sonnet).

The Moderator prompt:

```
[Contents of moderator.md]

Here are the five council opinions:

MEMBER 1:
[Operator's response]

MEMBER 2:
[Customer Advocate's response]

MEMBER 3:
[Skeptic's response]

MEMBER 4:
[Strategist's response]

MEMBER 5:
[Builder's response]
```

Collect the Moderator's analysis.

## Step 5: Synthesis

In the main thread (not a subagent), synthesize the final council ruling. You have access to:
- The original question
- All persona opinions (with their real names, not member numbers)
- The Moderator's analysis (in FULL mode)
- The full PM OS context (people files, goals, project context)

Read the output template from `~/.claude/skills/council/templates/council-output.md`.

**Synthesis rules:**
- The Recommendation section MUST use O-I-R-C-W format (Observation, Implication, Response, Confidence, Watch).
- Weight opinions by reasoning quality, not confidence or verbosity. In FULL mode, reference the Moderator's force-ranking.
- The Key Dissent section must represent the strongest counterargument, even if the council mostly agrees.
- The "Condition that would flip this" field is mandatory. Name the specific evidence or change that would reverse the recommendation.
- If stakeholder people files were loaded, incorporate their pushback patterns and communication preferences into the Next Steps.
- Follow ALL writing style rules from preferences.md: no em-dashes, no AI vocabulary, direct and opinionated tone.

## Step 6: Save and Report

1. Display the full council ruling to the user.
2. Save the output to `./output/docs/DC-council-[topic-slug]-[YYYY-MM-DD].md` (create the directory if needed).
3. Tell the user where the file was saved.

## Writing Style Rules (Apply to ALL output)

- Never use em-dashes. Use commas, periods, semicolons, colons, or parentheses.
- No AI vocabulary: no "delve," "crucial," "landscape," "tapestry," "foster," "underscore," "showcase," "leverage."
- Be direct, specific, opinionated. Have a point of view.
- Use bullet points and structured tables. Narrative only where it serves clarity.
- Always include concrete next steps.
