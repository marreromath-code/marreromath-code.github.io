# SAT Command Center → Base44 Build Guide

Everything you need to rebuild the SAT app inside **Base44** as a real, account-based,
Stripe-subscription product. I can't log into Base44 for you, but this kit is paste-ready:
schemas, data, logic, and the exact prompts to drive Base44's AI builder.

> ## ⭐ SCOPE: MATH ONLY
> This product is **SAT Math** — no Reading & Writing. The bank, practice, and simulator
> are 100% math across four domains (Algebra, Advanced Math, Problem-Solving & Data,
> Geometry & Trig). The simulator runs **two adaptive Math modules** and estimates a
> **200–800 Math score**. Ignore any Reading & Writing references in the older prompts below.

## What's in this folder
| File | Use it for |
|------|-----------|
| `BUILD-GUIDE.md` | This guide — do the steps in order |
| `entities.json` | Database schemas to paste into Base44's Data panel |
| `questions.json` | Your 44-question bank — import into the `Question` entity |
| `scoring.js` | Drop-in adaptive practice + simulator + scoring logic (no Base44-specific code) |

> The static `sat.html` at the repo root stays as your **free funnel page**. This Base44
> app becomes the **paid product** its "Unlock Premium" button points to.

---

## Why Base44 (what changes vs. the static app)
| | Static `sat.html` | Base44 build |
|---|---|---|
| Accounts | none (per-device) | real logins, progress synced across devices |
| Paywall | client-side (readable) | **server-enforced** via Stripe + user `plan` field |
| Question bank | hardcoded in HTML | a database entity you edit without redeploying |
| Stats/history | `localStorage` | per-user records (`Attempt`, `TestSession`) |

---

## Step 0 — Create the app
In Base44, start a new app and paste this as the opening prompt:

> **Build prompt (paste into Base44):**
> Create a **Digital SAT Math** prep web app called **"SAT Math Command Center."** Signed-in
> students practice SAT **math** questions across four domains (Algebra, Advanced Math,
> Problem-Solving & Data, Geometry & Trig), take a module-adaptive Math simulator, review
> mistakes, and track progress toward a target Math score (200–800). There is **no Reading &
> Writing section.** It has a free tier (limited daily practice) and a paid **Premium**
> subscription (Stripe) that unlocks the full simulator, mistake review, and unlimited
> practice. Use a refined navy (#1a2744) + gold (#d4af1f) theme on a warm cream (#f9f7f2)
> background, serif display headings (Fraunces) and Inter for UI. I will provide the database
> schemas and question data next.

---

## Step 1 — Create the entities (Data panel)
Open **Data → create entity** and paste each schema from `entities.json`:
`Question`, `Attempt`, `TestSession`, `Bookmark`.
Base44 auto-adds `id`, `created_date`, `updated_date`, `created_by` — don't re-add them.

Then add the **custom fields** from `entities.json → _UserEntity.custom_fields` to the
built-in **User** entity: `test_date`, `goal_score`, `streak_days`, `last_active_date`,
`plan` (free/premium), `subscription_status`, `stripe_customer_id`, `daily_quota_date`,
`daily_quota_used`.

## Step 2 — Seed the question bank
Import `questions.json` into the **Question** entity (Base44 supports JSON/CSV import; or
ask the builder: *"Import these records into the Question entity"* and paste the file).
You'll have 44 items (31 Math, 13 R&W). **Grow this to a few hundred before launch** — see
"Scaling the bank" below.

## Step 3 — Add the logic
Create a shared util (e.g. `lib/scoring.js`) and paste **`scoring.js`**. Your screens call:
- `buildPracticeSet(questions, opts)` — practice sets (handles section/domain/difficulty/adaptive/quota)
- `isCorrect(question, response)` / `gridMatch(...)` — grading (MC + grid-in)
- `buildModule`, `routeToHard`, `sectionScore`, `buildScoreReport` — the simulator
- `overallStats`, `masteryByDomain`, `estimatedScore`, `updateStreak`, `quotaLeft` — dashboard/progress

---

## Step 4 — Build the screens
Give Base44 these one screen at a time (it builds incrementally best). Each is a copy-paste prompt.

### 4a. Dashboard (home)
> Build the **Dashboard** home screen for signed-in users. Show: a **test-day countdown**
> (days until the user's `test_date`, editable date picker that saves to the User), a **score
> goal** card comparing `estimatedScore(attempts)` to the user's `goal_score` (slider 400–1600),
> four stat tiles (questions answered, overall accuracy, day streak, full tests taken), and a
> **Domain Mastery** list with a progress bar per domain from `masteryByDomain(attempts)`. Add
> four quick-start buttons linking to Practice, Simulator, Review, Reference. Load the user's
> `Attempt` and `TestSession` records to compute these.

### 4b. Practice
> Build the **Practice** screen. A setup card lets the user pick Section (Math / Reading &
> Writing / Mixed), Domain (chips, depends on section — Math: Algebra, Advanced Math,
> Problem-Solving & Data, Geometry & Trig; R&W: Information & Ideas, Craft & Structure,
> Expression of Ideas, English Conventions), Difficulty (Adaptive / Easy / Medium / Hard), and
> Length (5/10/20). On start, call `buildPracticeSet(questions, opts)`. Show one question at a
> time: optional passage, stem, multiple-choice (A–D) **or** a grid-in text input. A **Check
> Answer** button grades with `isCorrect`, reveals the correct choice (green) / wrong choice
> (red), and shows the explanation. A bookmark (star) toggles a `Bookmark` record. Each answer
> writes an **Attempt** record (`mode: "practice"`, `session_id`, `time_seconds`, `domain`,
> `difficulty`, `is_correct`, `given_answer`). **Free users:** enforce `quotaLeft(user, today)`
> — when it hits 0, show the paywall. After the set, show a summary (correct/total, time) with
> "Review Mistakes" and "Practice Again."

### 4c. Full-Test Simulator  *(Premium-gated)*
> Build the **Simulator** screen, locked behind `user.plan === 'premium'` (else show the
> paywall). It runs a 4-stage module-adaptive test using `scoring.js`:
> 1) R&W Module 1 (`buildModule(questions,'rw',false)`), timed ~10 min;
> 2) R&W Module 2 — `routeToHard(correct,total)` decides standard vs. higher (`buildModule('rw', hard)`);
> 3) Math Module 1 (`buildModule('math',false)`), timed ~11 min;
> 4) Math Module 2 — routed by Math M1 accuracy.
> Show a module banner with title + countdown; one question per view; auto-advance when time
> expires (unanswered = incorrect). Write an **Attempt** per question (`mode: "test"`). At the
> end call `buildScoreReport(rw, math)` and save a **TestSession**; show the 400–1600 report
> with section scores and which route (standard/higher) each section took. Add a "new personal
> best" badge by comparing to the user's prior max `TestSession.total_score`.

### 4d. Review  *(Premium-gated)*
> Build the **Review** screen (Premium only). List the user's **missed** questions (their most
> recent `Attempt` per `question_id` where `is_correct=false`) plus all **bookmarked**
> questions. For each, show the stem, passage, correct answer, and explanation, with a "remove
> from review" action (deletes the Bookmark / ignores the missed item going forward).

### 4e. Progress
> Build the **Progress** screen: a domain-accuracy list from `masteryByDomain(attempts)` and a
> **Session History** table from `TestSession` + grouped practice `Attempt` sessions (date,
> type, detail, result). Include a "Reset my data" action that deletes the user's Attempt/
> TestSession/Bookmark records but keeps their account and subscription.

### 4f. Reference
> Build a static **Reference** screen: the SAT geometry/formula reference sheet (circle area
> πr², circumference 2πr, triangle ½bh, Pythagorean a²+b²=c², box ℓwh, cylinder πr²h, 30-60-90
> and 45-45-90 ratios), must-know formulas (slope, slope-intercept, quadratic formula,
> exponential growth/decay, percent change, d=rt), top strategies, and a numbered list of the
> 12 Digital SAT math question types. Link to the YouTube video
> https://www.youtube.com/watch?v=11Oi9gd3BdU.

---

## Step 5 — The Stripe paywall (the whole point of moving to Base44)
1. In Base44, open **Integrations → Payments/Stripe** and connect your Stripe account.
2. Create a **recurring price** (e.g. *SAT Premium — $9/mo* and/or *$59/yr*).
3. Add a **Subscribe** button on the paywall that starts Stripe Checkout for that price,
   passing the signed-in user so Stripe knows who paid.
4. Add a **webhook / automation**: on `checkout.session.completed` and
   `customer.subscription.updated/deleted`, update the User:
   - active → `plan: "premium"`, `subscription_status: "active"`, store `stripe_customer_id`
   - canceled/past_due → `plan: "free"`, mirror the status.
5. **Gate** every premium screen/server action on `user.plan === 'premium'` (server-side, not
   just hidden in the UI). Free users get Dashboard, Reference, and `FREE_DAILY_QUOTA`
   questions/day.

> **Paywall prompt (paste into Base44):**
> Add a **Premium paywall**. Gate the Simulator and Review screens, and practice beyond the
> daily free quota, behind `user.plan === 'premium'`. Non-premium users see a card explaining
> Premium (unlimited practice, full adaptive simulator, mistake review, progress sync) with a
> **Subscribe** button that opens Stripe Checkout for my "SAT Premium" recurring price. When
> the Stripe webhook confirms an active subscription, set the user's `plan` to "premium"; when
> it cancels or lapses, set it back to "free". Enforce the gate in backend actions, not just the UI.

### Hook it up to your existing site
In the static `sat.html`, point the upgrade buttons at your Base44 app URL. Open the
`LS = {…}` config block near the top of the `<script>` and set `checkoutUrl` to your Base44
app/checkout link. The free static app becomes the top of the funnel; Base44 is the paid app.

---

## Scaling the question bank (do this before charging)
- 44 items is enough to demo, not to sell. Aim for **300–500+**, weighted toward Math.
- Keep the **exact schema** in `questions.json`. To bulk-author, ask Base44's AI (or me):
  *"Generate 30 original, SAT-style Algebra questions as records matching the Question schema,
  difficulties mixed, each with choices, answer_index, and a worked explanation."* Then import.
- All items must be **original** — College Board's released questions are copyrighted. Keep the
  trademark disclaimer ("SAT is a trademark of the College Board, which does not endorse this product").

## Suggested build order
1. Entities + import questions → 2. paste `scoring.js` → 3. Dashboard → 4. Practice (free path
working end-to-end) → 5. Stripe paywall + `plan` gating → 6. Simulator → 7. Review → 8. Progress
→ 9. Reference → 10. polish + expand the bank.

---

*Questions are original, SAT-style items. "SAT" is a trademark of the College Board, which does not endorse this product.*
