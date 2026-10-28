# Skills

My agent skills for Claude Code and GitHub Copilot, in one place: **17 skills in 4 categories.**
Each skill is a folder with a `SKILL.md` that the agent reads, plus any references, templates,
scripts or evals it needs.

Browse them at **[rohitjz.github.io/skills](https://rohitjz.github.io/skills/)**.

```
skills/
├── design/                  how things look
├── product-strategy/        what to build and how to position it
├── writing-and-presenting/  how to say it
└── finance/                 how to value it
```

## Catalog

### Design
| Skill | What it does |
|---|---|
| [analog-ui](skills/design/analog-ui) | Design that looks made by hand, not AI-templated: borrow a real medium (sketchbook, blueprint, museum, lab notebook, riso zine, receipt, field journal, departure board) and rebuild it in code. `/analog-ui sketchbook` jumps straight to one. [Gallery](https://rohitjz.github.io/skills/skills/design/analog-ui/gallery/) |
| [elevate-ui](skills/design/elevate-ui) | Turns flat, AI-looking pages into designed ones: bespoke SVG icons, depth, liquid-glass chrome, motion. |
| [glassify](skills/design/glassify) | Single-file sites with a validated liquid-glass treatment (SVG refraction and layered dome shadows). |

### Product strategy
| Skill | What it does |
|---|---|
| [distinctive-positioning](skills/product-strategy/distinctive-positioning) | Evidence-backed positioning: research the category, compare three territories, build a content system, test it. |
| [council](skills/product-strategy/council) | Runs an LLM council on a hard decision: five perspectives, adversarial review, one recommendation. |

### Writing and presenting
| Skill | What it does |
|---|---|
| [pm-writing](skills/writing-and-presenting/pm-writing) | A writing system for PMs, distilled from Zinsser, Ogilvy, Orwell and Finshots, with an LLM-judge eval. |
| [patrick-winston-presentation](skills/writing-and-presenting/patrick-winston-presentation) | Coaches a talk with Patrick Winston's MIT "How to Speak" framework. |

### Finance
Educational, not financial advice. Adapted from Anthropic's Claude for Financial Services under
Apache-2.0 (see [LICENSE](skills/finance/LICENSE) and [NOTICE](skills/finance/NOTICE)), and
rewired to free market data.

| Skill | What it does |
|---|---|
| [idea-generation](skills/finance/idea-generation) | Screens a quality large-cap universe for the best setups. |
| [sector-overview](skills/finance/sector-overview) | Industry primer: size, growth, structure, drivers, players, multiples. |
| [competitive-analysis](skills/finance/competitive-analysis) | Competitive map: positioning, moats, bull and bear cases. |
| [initiating-coverage](skills/finance/initiating-coverage) | A five-step workflow to initiate coverage on one name. |
| [3-statement-model](skills/finance/3-statement-model) | An integrated income statement, balance sheet and cash flow model. |
| [dcf-model](skills/finance/dcf-model) | A DCF with a CAPM WACC build and a terminal value cross-check. |
| [comps-analysis](skills/finance/comps-analysis) | A peer trading-multiples spread with outlier flags. |
| [lbo-model](skills/finance/lbo-model) | An LBO model: sources and uses, debt schedule, returns. |
| [earnings-analysis](skills/finance/earnings-analysis) | A post-earnings note: beat or miss, trend, guidance, thesis impact. |
| [thesis-tracker](skills/finance/thesis-tracker) | Defines a thesis, logs updates and scores it over time. |

## Install

Agent hosts look for skills one level deep (`<skills-dir>/<name>/SKILL.md`), so the installer
flattens the categories.

```bash
git clone https://github.com/rohitjz/skills && cd skills
./install.sh --list                      # see everything
./install.sh                             # all skills -> ~/.claude/skills
./install.sh --target copilot            # all skills -> ~/.copilot/skills
./install.sh --category design           # one category
./install.sh analog-ui council          # just these
./install.sh --link                      # symlink, so `git pull` updates them
```

To install one skill by hand, copy its folder, for example
`cp -R skills/design/analog-ui ~/.claude/skills/`.

## Tests

```bash
pip install matplotlib pillow openpyxl playwright && python -m playwright install chromium
python scripts/validate.py       # every skill's layout and frontmatter
python tests/test_tools.py       # installer, chart script (all modes), email export, inliner
python tests/run_samples.py      # every sample at 3 screen sizes + reduced motion
```

The sample run checks for horizontal overflow, broken images, missing alt text, unlabelled SVGs,
text under 10px, keyboard access to scrolling areas, infinite animation, receipts that don't add
up, and the departure board's interaction. CI runs all three on every push and keeps the
screenshots as an artifact.

## Adding a skill

1. Put it at `skills/<category>/<name>/SKILL.md`, with `name:` in the frontmatter matching the folder.
2. Run `python scripts/validate.py`. CI runs the same check on every push.
3. Add a row to the catalog above.

## Licenses

MIT ([LICENSE](LICENSE)), except `skills/finance/`, which is Apache-2.0.

Several skills also have standalone repos with demos and history:
[elevate-ui](https://github.com/rohitjz/elevate-ui) ·
[distinctive-positioning](https://github.com/rohitjz/distinctive-positioning) ·
[clear-writing-for-pms](https://github.com/rohitjz/clear-writing-for-pms) ·
[claude-for-pms](https://github.com/rohitjz/claude-for-pms) ·
[stock-advisor-pro](https://github.com/rohitjz/stock-advisor-pro) (the full Claude Code plugin, with commands and agents).
