# Fidelity eval: Story launch zine vs the board mock

Two blind judges per round. Each one viewed the mock (`src/source/board-mock.png`) next to screenshots of the build at 1152, 1440 and 390px, the zoom view, a second spread and every page image. They scored 8 criteria from 1 to 10 and listed the top differences. Every round used fresh judges, so no judge was anchored on an earlier score.

| Criterion | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| Page art | 6, 6 | 7, 7 | 6, 7 |
| Page typography and layout | 6, 6 | 7, 6 | 5, 6 |
| Board layout and placement | 6, 5 | 6, 5 | 7, 7 |
| Board chrome typography | 5, 6 | 7, 6 | 7, 7 |
| Colour and paper | 5, 6 | 7, 7 | 6, 8 |
| Interaction affordances | 8, 8 | 8, 8 | 8, 8 |
| Mobile | 7, 7 | 6, 7 | 6, 7 |
| **Overall** | **6, 6** | **6.5, 6** | **6, 7** |

The judges usually agree within 1 point. Differences of a point between rounds are noise.

## What changed between rounds
- **Round 1 to 2:**
  - Linework on the separated art was made solid with a levels curve. Grain had turned the soft, upscaled lines into static.
  - Light tints now print as soft grain.
  - Pages got aged edges and stains.
  - The book got stacked page edges, a gutter and a contact shadow.
  - The arrows moved off the art.
  - Art was added to pages 2, 5 and 7.
- **Round 2 to 3:**
  - The title sits on one line at the mock's size.
  - The tags are narrower.
  - The thumbnail labels are short ("2. Intro", "6. CTA") and the active state is quieter.
  - Page 5 got a hero phone illustration and short claims.
  - The page 4 tiles use the mock's cool tint.
- **After round 3:** fixed the clipped "Hard call" and "Lesson" notes on page 2 and the "Match your audience" overflow on page 3. Page 5 got a foot band.

## Known gaps
- The inside art is drawn in code or separated from the low-resolution mock. Both round 3 judges called it cleaner than the mock's hand-drawn art. Higher-resolution two-ink illustrations would close that gap; drop them in `src/source/` and point `CROPS` at them.
- At 1152 x 768 the notes band starts about 65px lower than in the mock, because no text is set below 12px. At 1440 x 960 the whole board fits on one screen.
