---
name: add-questions
description: >
  Workflow for generating large batches of original, answer-verified practice
  questions for a learning app (SAT, test prep, quizzes, flashcards, assessments).
  Use whenever the user wants to "add questions," "create more questions," "expand
  the question bank," build a quiz/test item bank, or turn sample questions into
  more of the same. Produces importable JSON with computed (guaranteed-correct)
  answers and, when needed, inline SVG/HTML figures (graphs, tables, diagrams).
---

# Add Questions — Generation Playbook

Generate test-realistic, **original**, answer-verified questions at scale and hand
them over ready to import. Optimized for learning apps with a `Question`-style
entity.

## Non-negotiables
- **Original only.** Never copy real exam or copyrighted questions, and never
  number-swap/reword them (a near-twin is a derivative work = infringement).
- **Blueprint, not copy.** When the user uploads sample questions, extract only the
  *skill, format, and difficulty* (those aren't copyrightable) and write brand-new
  items with new contexts and numbers.
- **Computed answers.** Every answer must be *calculated* by the generator, not
  hand-typed or model-guessed — this guarantees correctness.
- **Keep the disclaimer.** If the domain has a trademark (e.g. "SAT"), keep the
  "trademark of … which does not endorse this product" note in the app.

## Step 1 — Build a coverage map
From the user's samples (or the public skill spec), list the skills to cover, each
with its format (multiple-choice vs. numeric/grid-in) and difficulty. Show the user
the plan and the rough mix (e.g. "40% Algebra, 30% Advanced Math, …") before
generating, so they can adjust.

## Step 2 — Write a parameterized generator
Create a small Node script (one per pack) that:
- Has helpers: `mc()` (builds a multiple-choice item, shuffles options, records the
  correct index) and `grid()` (numeric/free-response). Both output the app's schema.
- Uses **templates with randomized parameters** so each item is varied; the correct
  answer and the distractors are all derived from those parameters.
- Builds distractors from **realistic error patterns** (forgot a step, sign error,
  swapped operation) — and from a **filtered candidate pool** so they're always
  distinct from the answer and each other (avoid ugly "(1)" backfills).
- De-dupes by stem so random collisions are dropped.
- Uses unique `question_id` prefixes per pack so packs never collide on import.

## Step 3 — Figures (graphs, tables, diagrams)
When a skill needs a picture, generate it as **inline SVG or HTML** stored in a
`figure` field on the item — no image hosting required:
- **Graphs/parabolas:** draw a coordinate grid + the curve; mark key points (gold dots).
- **Tables (two-way / data):** emit a styled `<table>`.
- **Geometry diagrams:** draw triangles/circles with labeled sides, angle arcs, and
  tick marks for equal sides; add "Note: figure not drawn to scale."
The app must render `figure` as **trusted HTML/SVG** above the stem (add the field
to the entity first).

## Step 4 — Validate before delivery (always)
Run a checker over the generated JSON:
- For MC: `choices[answer_index] === answer_text`, exactly 4 **unique** choices, no
  empty/backfilled (" (1)") options.
- For grid: non-empty answer.
- Figures present where the stem references one.
- **Spot-check the math/logic** by re-deriving a few answers independently.
Fix the generator (not the JSON) until it reports zero issues.

## Step 5 — Deliver
- Write each pack to its own `*.json`; keep a combined `*_all.json` for reference.
- Generate a small **preview** (an HTML file or sample SVGs) the user can open to
  see figures render.
- Send the importable file(s) to the user, state the new bank total, and remind them
  to **import each pack** into the app (and that figure packs need the `figure`
  field) — generating ≠ importing.
- Commit the generator + JSON + preview.

## Quality bar
- Distractors are plausible, not random.
- Difficulty spread roughly mirrors the real assessment.
- Wording is clean (no `+ 0x`, unsimplified fractions like `6/8`, or `(x + 0)`).
- Each pack is self-contained and re-runnable.

## Reusable validation snippet
```js
const Q = require('./PACK.json'); let errs = 0;
for (const q of Q) {
  if (q.type === 'mc') {
    if (q.choices[q.answer_index] !== q.answer_text) { console.log('MISMATCH', q.question_id); errs++; }
    if (new Set(q.choices).size !== 4) { console.log('BADCH', q.question_id, q.choices); errs++; }
    if (q.choices.some(c => / \(\d+\)$/.test(c))) { console.log('UGLY', q.question_id); errs++; }
  } else if (!q.answer_text && q.answer_text !== 0) { errs++; }
}
console.log(errs === 0 ? `✓ All ${Q.length} valid` : `${errs} issues`);
```
