# Analog UI

Design that looks made by hand, not generated. Analog UI borrows a real physical medium whose
job matches your content, lists what is physically in it, and rebuilds each object in code with
a reason to be there.

**[See all eight mediums →](https://rohitjz.github.io/skills/skills/design/analog-ui/gallery/)**

```
/analog-ui                 pick the right medium for this content
/analog-ui sketchbook      go straight to one
```

| Medium | Call | Job | Sample |
|---|---|---|---|
| Designer's sketchbook | `/analog-ui sketchbook` | Milestone | [Let's Encrypt, 10 years](mediums/sketchbook/examples/lets-encrypt-10-years/index.html) · [kit](mediums/sketchbook/examples/kit/index.html) |
| Architect's blueprint | `/analog-ui blueprint` | Roadmap | [blueprint-roadmap](mediums/blueprint/examples/blueprint-roadmap/index.html) |
| Museum exhibit | `/analog-ui museum` | Quarterly review | [museum-qbr](mediums/museum/examples/museum-qbr/index.html) |
| Lab notebook | `/analog-ui lab-notebook` | Incident report | [lab-notebook-incident](mediums/lab-notebook/examples/lab-notebook-incident/index.html) |
| Risograph zine | `/analog-ui riso-zine` | Launch | [riso-launch](mediums/riso-zine/examples/riso-launch/index.html) |
| Receipt and price tags | `/analog-ui receipt` | Pricing | [receipt-pricing](mediums/receipt/examples/receipt-pricing/index.html) |
| Field journal | `/analog-ui field-journal` | Feedback digest | [field-journal-feedback](mediums/field-journal/examples/field-journal-feedback/index.html) |
| Departure board | `/analog-ui departure-board` | Release status | [departure-board-status](mediums/departure-board/examples/departure-board-status/index.html) |

The sketchbook is fully built: a CSS and SVG kit, page and newsletter templates, and an
xkcd-style chart script. Every medium can ship as one self-contained file
(`scripts/inline_assets.py`) or as email-safe images (`scripts/export_email.py`).

Name another medium (`/analog-ui polaroid`) and the skill runs the full method to invent it.

The Let's Encrypt page is an unofficial redesign of a public post. All other samples use a
fictional product, Northwind Notes, with illustrative data.

Formerly two skills, `sketchbook-ui` and `medium-first-design`, merged here. The merge was checked
for coverage, routing, context cost and a blind A/B on built pages: see [EVAL.md](EVAL.md).
