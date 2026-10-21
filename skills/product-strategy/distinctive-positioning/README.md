# Distinctive positioning

Find a position your audience cares about and your competitors cannot claim
unchanged.

An agent skill for products, businesses, creators, and early ideas. It researches
category conventions, compares three strategic directions, and turns the strongest
credible direction into a content system and a test.

## What you get

- An evidence-backed category map, with assumptions kept separate.
- Three positioning territories: category misfit, category reframe, and belief
  challenger, or better alternatives supported by the research.
- A seven-criterion decision matrix with trade-offs and credibility checks.
- A positioning statement, signature point of view, content identity, and
  repeatable creative rule.
- Ten content concepts with hooks, narratives, formats, intended responses,
  and metrics.
- A controlled validation experiment tied to your goal.

The skill can conclude that no defensible position exists yet. It does not invent
product strengths, customer research, or a winning score to finish the brief.

## Install

For Copilot and compatible agents that discover personal skills:

```bash
mkdir -p "$HOME/.copilot/skills" &&
git clone https://github.com/rohitjz/distinctive-positioning.git \
  "$HOME/.copilot/skills/distinctive-positioning"
```

To expose the same installation to Claude Code on macOS or Linux:

```bash
mkdir -p "$HOME/.claude/skills" &&
ln -s "$HOME/.copilot/skills/distinctive-positioning" \
  "$HOME/.claude/skills/distinctive-positioning"
```

These commands do not replace an existing installation. Do not use a force
overwrite to resolve a collision. If already installed, inspect local changes
before updating.

Start a new agent session or reload skill discovery after installation.
Automatic selection and slash-command visibility depend on the host.
The skill uses standard `name` and `description` frontmatter and does not disable
either automatic selection or explicit invocation.

## Use

Request it by name, or use `/distinctive-positioning` where the host supports
skill slash commands:

```text
Use distinctive-positioning for this idea.

Idea: A bookkeeping service for independent designers.
Audience: Solo designers who avoid their accounts until tax season.
Goal: Acquire paying clients.
Platform or market: LinkedIn and the service website.
Constraints: One founder, limited content budget, no paid ads.

Research the category before recommending a position. Do not invent customer
insights or performance claims.
```

Supply competitor links, interviews, reviews, or product proof when available.
Missing nonessential inputs become labeled assumptions.

For a focused follow-up, ask for a particular stage, such as "revisit the category
reframe using these interviews" or "turn territory B into a message test."
Approved copy and designs stay intact unless you request a change.

## How it works

The workflow has six phases: diagnose the opportunity, map category conventions,
develop territories, evaluate them, build the execution system, and design a test.

The [skill instructions](./SKILL.md) contain the full procedure.
The [output template](./references/output-template.md) defines the nine-section
deliverable, including the ten-concept table.

Research improves the result, but browsing is not required to run the workflow.
Without research access, the agent must disclose the gap and treat unsupported
conclusions as hypotheses. Browsing tools, permissions, and model access come from
the host. There are no package dependencies, embedded credentials, or required
companion skills.

## Review the result

Run the [evaluation cases](./evals/cases.md) in your agent to check the workflow,
including missing research, unsupported promises, and the no-winner path.
They are a manual rubric, not a claimed performance benchmark.

Reject an output if it fabricates sources, treats views as revenue, changes an
approved identity without permission, or gives three slogans instead of three
different strategic choices.

## Origin and license

Created by [Rohit Jaiswal](https://github.com/rohitjz), adapted from a supplied
six-phase positioning brief, "Find the Most Distinctive Positioning for Any Idea."

The adaptation adds discovery metadata, explicit evidence handling, scoring
anchors, a no-winner path, and a reusable output template.

[MIT license](./LICENSE).
