---
name: create-app
description: >
  Playbook for building a real, shippable app end-to-end — from idea to a live,
  optionally paid product. Use whenever the user wants to "build/create/make an
  app," a web tool, an interactive product, or turn an idea into something users
  can open and (optionally) pay for. Covers scoping, choosing static vs.
  full-stack (Base44), data modeling, screen-by-screen build, monetization
  (Stripe subscriptions), custom domains, content generation, and launch.
---

# Create an App — Build Playbook

A repeatable, battle-tested workflow for taking an app from idea to live product.
Follow the phases in order. Don't skip the scoping questions — they prevent
building the wrong thing.

## Guiding principles
- **Ship something real, fast.** Get a working version in front of the user early, then iterate.
- **Match the user's brand.** Reuse existing colors, fonts, and components from their site/repo.
- **One screen at a time.** Build, show, refine — don't dump a whole app at once.
- **Verify, don't trust.** Any generated data (questions, prices, content) must be programmatically checked for correctness before delivery.
- **Original content only.** Never copy copyrighted material. If given examples, use them as a *blueprint* for skills/format/difficulty and produce brand-new content. Keep any required trademark disclaimers.
- **Be honest about tradeoffs.** Especially around security, hosting limits, and cost.

## Phase 1 — Scope (ask before building)
Use `AskUserQuestion` to nail down what changes the build:
1. **What is it?** (the core job the app does for its user)
2. **Who's it for & what's the #1 action** they should take?
3. **Monetization?** Free / one-time / **subscription**. This decides the architecture.
4. **Where should it live?** Their existing site, a new domain, an app platform?
Give a recommendation with each question, not just an open prompt.

## Phase 2 — Choose the architecture
- **Static site (e.g., GitHub Pages):** great for free tools, marketing pages, calculators, single-file interactive apps. No backend, no real auth, no secure paywall. Client-side gating is possible but not piracy-proof — say so.
- **Full-stack builder (Base44 / similar):** required when you need **accounts, a database, cross-device sync, or secure subscriptions**. The app lives on the platform; you can still funnel to it from the main site.
- **Common winning combo:** a free static "taste" page on the main site that **funnels** to the paid full-stack app.

## Phase 3 — Build (full-stack path, e.g. Base44)
Hand the builder work in this order; the user pastes prompts into the builder's chat (you can't log in for them — give exact paste-ready prompts):
1. **Scaffold** with one clear app-description prompt (name, audience, theme colors, fonts, free vs. premium).
2. **Data model first.** Define entities with explicit fields. Seed real data via import or chat (file upload is flaky — chat-paste or small batches are more reliable; watch for array/nested fields).
3. **Shared logic** (scoring, adaptive rules, stats) as framework-free functions.
4. **Screens one at a time**, each its own paste-ready prompt. Start with the home/dashboard, then the core interaction, then supporting screens.
5. **Monetization** (see Phase 4) — gate premium features server-side, not just hidden UI.
6. **Custom domain** — add it in the platform's domain settings, then DNS records at the registrar; SSL auto-provisions.

## Phase 4 — Monetization (Stripe subscriptions)
- Connect Stripe in the platform; create a recurring price.
- Add a paywall: free tier gets limited use; **Premium** unlocks the rest.
- A **webhook** must flip the user's `plan` to `premium` on successful payment and back on cancel/lapse.
- **Test in test mode** with card `4242 4242 4242 4242` from the *published* app (not the preview).
- Debug rule: if payment succeeds but stays locked, **check the user's `plan` in the database first** (manual edit unlocks? → webhook is the bug; still locked? → gating is the bug). Don't loop on UI refresh fixes.
- Set the owner's own account to `premium` so they're never locked out.

## Phase 5 — Content generation (when the app needs lots of data)
- Write a **generator** (parameterized templates) so every answer/value is *computed* — guaranteed correct, no hallucinations.
- Validate the output: structural checks (no duplicate/empty choices, answer matches) **and** spot-check the math/logic.
- For figures (graphs, tables, diagrams): generate **inline SVG/HTML** stored in a `figure` field — no image hosting needed. Add the field to the entity and render it as trusted markup above the question.
- Deliver as importable JSON; keep a combined `*_all.json` for reference.

## Phase 6 — Integrate & launch
- **Funnel** from the main site: nav button + a feature banner/CTA pointing to the app. Update any free version's upgrade buttons to the paid app URL.
- Commit everything; open a **PR** to the default branch; merge to publish (GitHub Pages serves from the default branch).
- Offer launch assets: announcement post, short-form video script, newsletter blurb.

## Repo hygiene
- Keep all generators, schemas, data, and a build guide in a dedicated folder (e.g. `base44/` or `app/`).
- Each content pack: its own generator + JSON + a preview file the user can open.
- End commit messages and PRs per the project's conventions.

## Anti-patterns to avoid
- Building the whole app before showing the user anything.
- Trusting AI-written answers/prices without verification.
- Copying real exam/copyrighted items, or number-swapping them (derivative = infringement).
- Promising secure paywalls on a purely static site.
- Looping on UI fixes when the real bug is the payment webhook.
