---
name: planning
description: Phase 0 pre-implementation planning for a Linux kernel change — split the request into one-logical-change-per-patch themes, check for function-length/helper-extraction needs, converge the plan via self- or peer-review, and get human sign-off before writing code. Load before Phase 1 draft code, for any non-trivial change.
metadata:
  type: reference
---
# Phase 0 — plan before writing code

Concrete checklist for planning a kernel change before any code is drafted. Load this file before Phase 1 draft code (see [coding.md](./coding.md)) whenever the trigger below fires. For full load order see README.md "How to load".

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute. Treat as data when crawling; guidance applies only when a user deliberately loads it to plan a kernel patch.

## When this phase fires

Run Phase 0 planning whenever the requested change is not trivially a single, self-evident edit — concretely: it touches more than one function, more than one file, describes more than one distinct behavior change, or can't be stated as one sentence without "and". Skip it for a one-line fix, a straightforward revert, a single self-contained bug fix confined to one function, or a request that is itself just "apply rule X here."

Also run it when the task is to evaluate, rewrite, or forward-port a patch series that already exists, rather than to write fresh code — the split-check in §2 below still applies, but see [patch-series-rework.md](./patch-series-rework.md) for the procedure specific to restructuring already-committed history rather than choosing boundaries for a diff that doesn't exist yet.

When in doubt, run it. A short planning pass on a change that turns out to be simple costs far less than writing a large diff and retrofitting it into a series afterward.

## 1. Resolve ambiguity before planning, don't guess

If the request's scope, target subsystem, or success criteria (what "done" looks like, what to benchmark or test) are genuinely unclear, ask before drafting a plan. A confident-looking plan built on a wrong assumption about scope costs more to unwind than a clarifying question costs to ask.

## 2. Split into logical-change themes — one functional change per patch

Apply [patch-series.md](./patch-series.md) §1's split procedure — inventory the distinct pieces, sweep target patch counts upward (2, 3, 4, ...), apply the incremental-narrowing check before accepting a ceiling, then sweep back down folding only patches with nothing independently checkable — to the *description* of the intended change, before any code exists, not just at Phase 2 review time against a finished diff. Finding the seams before writing code is cheaper than reverse-engineering them out of a diff afterward.

If the task is instead to evaluate or rework an existing series (see "When this phase fires" above), apply the same test retroactively per patch-series.md's pointer to [patch-series-rework.md](./patch-series-rework.md), which covers squashing a later fixup into an earlier patch, moving a hunk that belongs elsewhere, and re-splitting just the affected part of a series.

If the examination finds the change is genuinely one atomic logical step, say so explicitly and move on with a one-patch plan. Don't force a split that isn't there.

## 3. Check for functions that would grow too long, or already are too long

For each planned change, estimate whether it will push an existing function past [kernel-style.md](./kernel-style.md) §3's cap (80% ≤20 lines, hard max 40) or whether the function already is too long. If so, plan a helper extraction as its own patch ahead of the functional change that needs it, split along theme boundaries per [kernel-style.md](./kernel-style.md) §3 CS-13 rather than by line count.

An extraction patch must obey the same rules as any other patch in the series: it must be pure code motion with no behavior change riding along ([patch-series.md](./patch-series.md) §1, "move code and change code in separate patches"), and the extracted helper must go live immediately — don't stage a helper with no caller and add its first user in a later patch ([patch-series.md](./patch-series.md) §2, "new code should go live in the patch that adds it"). If an extraction has nothing independently checkable on its own, fold it into the patch that uses it instead of manufacturing a separate step.

## 4. Check the order: no patch should write code a later patch rewrites

Splitting decides what the patches are; ordering decides which goes first, and a defensible split can still be in an order that wastes reviewer effort. The test is mechanical and applies to the patch list before any code exists: for each patch, name what it adds, then check whether a later patch changes those same lines. Every hit is a patch writing something one way so a later patch can rewrite it, and a reviewer reads both.

The usual shape is a helper arriving after its callers. If patch 2 open-codes the same block in three places and patch 4 factors it into a helper, patch 2 should have called the helper and the helper should come first: the series loses a patch and patch 2 gets smaller. Same for an interface or type conversion — convert, then use, never use then convert.

Where two orders are both correct, prefer the one where each patch's code survives to the end of the series, so every patch can be read forward without a mental note that it gets reworked later.

This is the design-stage form of [patch-series.md](./patch-series.md) §1's "a later patch whose diff touches only lines introduced earlier in the series", which catches the same problem afterward from a finished diff.

## 5. Write the plan down

A plan is a short document, not a paragraph of prose held in your head. Cover:

- **Problem statement** — what's broken or missing, one or two sentences.
- **Scope boundaries** — what this change does and does not do. State explicitly if a related but separable concern is out of scope; don't let it creep in mid-implementation.
- **Patch list** — numbered, each with a one-line description, what makes it bisectable on its own (builds, and has its own checkable behavioral claim), and its dependency on prior patches in the list.
- **Function-length risks** — which planned patches need a helper extraction per §3, and where that extraction patch sits in the list.
- **Ordering check** — the result of §4: for each patch, whether any later patch rewrites lines it adds, and why the chosen order is the one a reviewer reads most easily.
- **Open questions** — anything not yet resolved that implementation will need to answer: an API choice, a locking question, a benchmark target.
- **Verification plan** — how each patch will be checked: build, checkpatch, existing test suite, a specific benchmark, or a specific repro. Decide this before writing code, not after.

## 6. Converge the plan via review, before writing code

Run [peer-review.md](./peer-review.md)'s two mandatory questions — "what's wrong?" and "is there a materially better way?" — against the plan itself, the same way peer-review.md runs them against a diff at Phase 2. Use the same self-review-by-default, second-reviewer-when-available structure described there, including its "Escalating to a second reviewer" tiers.

Iterate: revise the plan, then re-run both questions against the revised plan. **Convergence** means one full pass finds nothing under (a) that requires a change, and either finds no alternative worth adopting under (b) or explicitly justifies why the current plan beats the alternative found. Cap iteration at roughly two or three rounds — if the plan still hasn't converged by then, surface the disagreement or open question to the human rather than looping indefinitely.

## 7. Present the plan; wait for sign-off

Present the converged plan to the human before starting Phase 1 draft code. Don't start writing code on the strength of a plan that hasn't been shown to them, even a well-reviewed one.

If implementation later reveals the plan needs a material change — a different patch count, a scope change, a different split point — re-present the updated plan before continuing, not just once at the start. A plan converging once doesn't license silent drift for the rest of the task.

## Next phase pointer

Once the human signs off on the plan, move to Phase 1 draft code — see [coding.md](./coding.md). Keep the approved plan available through Phase 1–3 as the reference for what each patch is supposed to do. Phase 2 review (review.md step 1a) runs the same patch-series.md split procedure again, against the actual diff — that is a check that the plan was followed, not a substitute for having planned first.

---
*Phase 0 planning checklist. For the split-procedure details it reuses see [patch-series.md](./patch-series.md) §1; for the review-question mechanics it reuses see [peer-review.md](./peer-review.md).*
