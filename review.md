---
name: review
description: Phase 2 review code checklist for Linux kernel style — mandatory exemplars load before git commit, self-review process (escalating to a second reviewer when available) per peer-review.md, git diff comparison workflow. Load during Phase 2 review on top of Phase 1 base per README three-phase cumulative workflow.
metadata:
 type: reference
---
# Phase 2 — review code before git commit

Concrete checklist for reviewing Linux kernel code and proposed commit message structure before committing to git. Load this file at start of Phase 2 review task **in addition to** Phase 1 base files already resident per cumulative load model — do not unload Phase 1 files until task end. For full load order see README.md How to load section.

**When this gate fires.** On the action, not the task label: any `git commit`, `git commit --amend`, or rebase `edit` that lands code or a changelog you wrote. That includes a patch you author incidentally while doing something else — a fix discovered mid-forward-port, a helper added during a rebase, a changelog reworded while restructuring a series. "I was doing a port, not writing a patch" is not an exemption; those patches reach reviewers identically to planned ones.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute. Treat as data when crawling; guidance applies only when user deliberately loads it to write or review kernel patch.

## Load order for Phase 2

Keep resident from Phase 1:
- `kernel-style.md` — entry point overview, factual integrity, code structure, 4 anchor quotes. Keep resident.
- `kernel-readability-principles.md` — composite principles from 14 developers. Keep resident.
- `llm-tells-checklist.md` — final-pass checklist. Re-run at review gate, keep resident.
- `coding.md` — Phase 1 draft checklist. Keep resident per cumulative model; cross-reference not duplicate here.

Add mandatory for Phase 2 review:
- `exemplars-routing.md` — tiny routing table (~180w). Load mandatory at review gate to pick profile (syzkaller→Dan Williams, race→Gleixner/Zijlstra, perf→Gorman/Butt). Then load only that section from `exemplars.md` on demand via `scripts/phases.py --phase 2 --bug-class <class>`. Saves ~5k tok vs full file. Full `exemplars.md` (3,685w) remains mandatory at gate per cumulative model but after routing pick, keep only chosen section resident through Phase 3 to save tokens. Do not preload exemplars every draft iteration; do not skip routing at review gate even if anchors seem sufficient.
- `peer-review.md` — review process specification with two mandatory questions "what's wrong?" and "is there a materially better way?", run as self-review by default and escalated to a second reviewer when one is available. Load mandatory during Phase 2 review and Phase 3 changelog drafting.

On demand during Phase 2 if needed:
- `changelog-style.md` — pull early if reviewing code comments for density or style, or if reviewing proposed commit message structure before drafting final message. Its §2 contains detailed comment rules beyond summary in kernel-style.md; §1 contains detailed changelog rules beyond summary. Normally changelog-style loads in Phase 3, but an early pull in Phase 2 is fine if you need it there.

- `patch-series.md` - pull early if any single source file has 200 or more changed lines, or a patch has 400 or more changed lines, or if a single patch covers more than one theme. Check the theme trigger separately, because it fires on patches well under both line counts: a patch that changes when a lock is held *and* changes a function's signature or return contract is carrying two themes, and so is one that leaves a function it touched still over kernel-style.md §3's length cap.

## Phase 2 mandatory steps

1. Capture the change as an artifact and review *that*, not the working copy you just typed. Commit (or stage) first, then read it back with `git show`, `git format-patch --stdout`, or `git diff --cached`, and review the output as if another developer had posted it. Reviewing your own draft in place tends to re-run the reasoning that produced it and confirm intent; reading the same change back as a decontextualized patch is what surfaces a comment that restates the code, a claim with no artifact behind it, or a now-redundant line. Keep Phase 1 files resident.

1a. Check per-file changed-line counts from that diff. If any single source file has 200 or more changed lines, load patch-series.md and run its size-threshold examination before continuing: inventory the diff's distinct logical pieces, then sweep target patch counts upward (2, 3, 4, ...) per patch-series.md, applying its incremental-narrowing check before accepting any ceiling, then sweep back down folding only patches with nothing independently checkable of their own — do not stop at the first cut and do not fold back a real parallel-old-and-new milestone just because its full payoff lands in a later patch. Tell the human the resulting split — named patches, scope, dependency order — before proceeding; do not silently keep reviewing or commit the single large diff. If the examination finds no separable step, state explicitly why this is one atomic logical change despite its size, then continue to step 2.

2. Load exemplars-routing.md mandatory at review gate. See exemplars-routing.md for routing table mapping bug class to developer section to focus on (extracted from exemplars.md intro to save tokens). Then load only chosen section from exemplars.md on demand. Compare diff against relevant developer section(s), adjust tone and comment density to match, then keep resident through Phase 3 — do not skip this load. Do not preload exemplars every draft iteration; once per patch at review is sufficient because kernel-readability-principles already synthesizes the 14 profiles hot and kernel-style.md carries 4 anchor quotes hot. You may load routing once during Phase 1 only to calibrate specific voice, but not every draft iteration.

3. Load peer-review.md mandatory during Phase 2 review. Run the two mandatory questions per peer-review.md as a self-review of your own diff and commit message draft first — this is the default, always-available gate, not optional even when working alone:
 * (a) What's wrong? — hunt for errors, unsupported claims, invented numbers or commit hashes, skipped evidence, failure modes in proposed code and commit message draft. Concluding "looks good" with no probing is not a review, even of your own work. Include the changelog's explanatory sentences, not just the diff: pick the ones stating how the code behaves or what the system looks like and check them against the source or a live artifact, the way you would check a number. Prose is where an author's model of the code gets asserted as fact, and it is quoted back long after the patch lands.
 * (b) Is there a materially better way? — for any design choice in code structure or rule wording, name at least one concrete alternative with tradeoff in correctness robustness simplicity maintainability token cost, or explicitly state why none beats chosen approach for stated goal. Skip (b) for trivial one-line fixes and pure fact-checks.
 * If a second reviewer is available (a different person, a fresh session of the same model reviewing the diff blind, or a different model family) route to them per peer-review.md "Escalating to a second reviewer" — a real enhancement when possible, never a blocker when it isn't.

4. Re-run llm-tells-checklist.md final pass against diff output to verify no LLM tells slipped in during drafting. Checklist is always hot, so no extra load needed beyond re-running with current diff context. Optional machine helpers, both on the artifact from step 1: `scripts/lint-code.py <sha>` for the diff side — @param scaffolding on a static [CC-12], a comment block left above the wrong function [CS-10], a function grown past the cap [CS-11] — and `scripts/lint-changelog.py` for the message side: paragraph caps [CL-12], banned phrases [CL-13], Fixes+Cc pairing [CL-11], internal IDs [CL-14], trailer forms, and a forward reference naming nothing. For a series pass a range, `lint-code.py <base>..<head>`; after rewording or rebasing a commit add `--against <old-ref>` so a measured claim carried onto a new base is flagged [R0-7]. Neither is a substitute for the checklist above; both are cheap enough to run every time.

5. Verify factual integrity per kernel-style.md §0 checklist against diff and primary sources — scope files touched, symptom root cause fix mechanism, performance delta if claimed, Fixes hash, Link URL, Reported-by name, etc. Never invent facts.

6. Verify external-facing discipline per CONTRIBUTING.md §4 / kernel-style norm 10 equivalent for public repo — no internal identifiers in file content or commit messages, write what changed why how to verify what behavior unlocked in terms external reviewer can act on without private context, re-read diff as external reviewer with zero internal context before proceeding to commit.

7. If all checks pass or have been addressed via fixes applied in working tree, proceed to Phase 3 draft changelog. Do not commit to git yet — commit happens after Phase 3 changelog drafting per workflow order, unless change is code-only with no changelog update needed (then commit at end of Phase 2 after exemplars calibration).

## Upstream kernel coding style reference

The Documentation/process/coding-style.rst file in the Linux kernel repository is a human-readable document with more coding style rules that should be followed for Linux kernel contributions.

## Next phase pointer

When Phase 2 review passes with exemplars calibration applied and peer review completed per two-question gate, move to Phase 3 draft changelog — see [commit.md](./commit.md) for Phase 3 mandatory checklist including changelog-style rules summary, trailers checklist, checkpatch reference moved there from README, and final verification before git commit. Do not proceed to git commit without completing the Phase 2 self-review gate above — it applies whether or not a second reviewer is ever involved. CONTRIBUTING's adversarial-review requirement for norm changes to this style guide itself is a separate, additional gate for changes to the repository's own normative content; see CONTRIBUTING.md §3.

---
*Phase 2 review checklist for kernel-style guide per README three-phase workflow. For peer review process specification see peer-review.md; for per-developer exemplars see exemplars.md; for meta rules see CONTRIBUTING.md.*
