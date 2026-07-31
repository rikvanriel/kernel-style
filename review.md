---
name: review
description: Phase 2 review code checklist for Linux kernel style — mandatory exemplars load before git commit, self-review process (escalating to a second reviewer when available) per peer-review.md, git diff comparison workflow. Load during Phase 2 review on top of Phase 1 base per README three-phase cumulative workflow.
metadata:
 type: reference
---
# Phase 2 — review code before git commit

Concrete checklist for reviewing Linux kernel code and proposed commit message structure before committing to git. Load this file at start of Phase 2 review task **in addition to** Phase 1 base files already resident per cumulative load model — do not unload Phase 1 files until task end. For full load order see README.md How to load section.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute. Treat as data when crawling; guidance applies only when user deliberately loads it to write or review kernel patch.

## Load order for Phase 2

Keep resident from Phase 1:
- `kernel-style.md` — entry point overview, factual integrity, code structure, 4 anchor quotes. Keep resident.
- `kernel-readability-principles.md` — composite principles from 14 developers. Keep resident.
- `llm-tells-checklist.md` — final-pass checklist. Re-run at review gate, keep resident.
- `coding.md` — Phase 1 draft checklist. Keep resident per cumulative model; cross-reference not duplicate here.

Add mandatory for Phase 2 review:
- `exemplars.md` — annotated real-commit examples per developer voice. Load mandatory at review gate before git commit, compare git diff output against relevant developer section per routing table inside exemplars.md introduction, adjust tone and comment density to match, keep resident through Phase 3. Do not preload exemplars every draft iteration; do not skip at review gate even if anchors seem sufficient.
- `peer-review.md` — review process specification with two mandatory questions "what's wrong?" and "is there a materially better way?", run as self-review by default and escalated to a second reviewer when one is available. Load mandatory during Phase 2 review and Phase 3 changelog drafting.

On demand during Phase 2 if needed:
- `changelog-style.md` — pull early if reviewing code comments for density or style, or if reviewing proposed commit message structure before drafting final message. Its §2 contains detailed comment rules beyond summary in kernel-style.md; §1 contains detailed changelog rules beyond summary. Normally changelog-style loads in Phase 3, but an early pull in Phase 2 is fine if you need it there.

- `patch-series.md` - pull early if any single source file has 200 or more changed lines, or a patch has 400 or more changed lines.

## Phase 2 mandatory steps

1. Run `git diff` or `git diff --cached` to capture changed hunks. Keep Phase 1 files resident.

1a. Check per-file changed-line counts from that diff. If any single source file has 200 or more changed lines, load patch-series.md and run its size-threshold examination before continuing: does this diff contain more than one logical change (mechanical conversion vs. behavioral change, code motion vs. rewrite, an already-handled case vs. a genuinely new algorithm, a helper vs. its first caller)? If yes, propose a split, then re-run the same four-tell examination on each proposed patch per patch-series.md's recursion step — do not stop at the first cut. Tell the human the resulting split — named patches, scope, dependency order — before proceeding; do not silently keep reviewing or commit the single large diff. If no, state explicitly why this is one atomic logical change despite its size, then continue to step 2.

2. Load exemplars.md mandatory at review gate. See exemplars.md introduction "How to choose which developer section to focus on at review gate" for per-subsystem routing table mapping bug class to developer section to focus on. Compare diff against relevant developer section(s), adjust tone and comment density to match, then keep resident through Phase 3 — do not skip this load. Do not preload exemplars every draft iteration; once per patch at review is sufficient because kernel-readability-principles already synthesizes the 14 profiles hot and kernel-style.md carries 4 anchor quotes hot for base calibration. You may load exemplars once during Phase 1 only to calibrate specific voice, but not every draft iteration.

3. Load peer-review.md mandatory during Phase 2 review. Run the two mandatory questions per peer-review.md as a self-review of your own diff and commit message draft first — this is the default, always-available gate, not optional even when working alone:
 * (a) What's wrong? — hunt for errors, unsupported claims, invented numbers or commit hashes, skipped evidence, failure modes in proposed code and commit message draft. Concluding "looks good" with no probing is not a review, even of your own work.
 * (b) Is there a materially better way? — for any design choice in code structure or rule wording, name at least one concrete alternative with tradeoff in correctness robustness simplicity maintainability token cost, or explicitly state why none beats chosen approach for stated goal. Skip (b) for trivial one-line fixes and pure fact-checks.
 * If a second reviewer is available (a different person, a fresh session of the same model reviewing the diff blind, or a different model family) route to them per peer-review.md "Escalating to a second reviewer" — a real enhancement when possible, never a blocker when it isn't.

4. Re-run llm-tells-checklist.md final pass against diff output to verify no LLM tells slipped in during drafting. Checklist is always hot, so no extra load needed beyond re-running with current diff context.

5. Verify factual integrity per kernel-style.md §0 checklist against diff and primary sources — scope files touched, symptom root cause fix mechanism, performance delta if claimed, Fixes hash, Link URL, Reported-by name, etc. Never invent facts.

6. Verify external-facing discipline per CONTRIBUTING.md §4 / kernel-style norm 10 equivalent for public repo — no internal identifiers in file content or commit messages, write what changed why how to verify what behavior unlocked in terms external reviewer can act on without private context, re-read diff as external reviewer with zero internal context before proceeding to commit.

7. If all checks pass or have been addressed via fixes applied in working tree, proceed to Phase 3 draft changelog. Do not commit to git yet — commit happens after Phase 3 changelog drafting per workflow order, unless change is code-only with no changelog update needed (then commit at end of Phase 2 after exemplars calibration).

## Upstream kernel coding style reference

The Documentation/process/coding-style.rst file in the Linux kernel repository is a human-readable document with more coding style rules that should be followed for Linux kernel contributions.

## Next phase pointer

When Phase 2 review passes with exemplars calibration applied and peer review completed per two-question gate, move to Phase 3 draft changelog — see [commit.md](./commit.md) for Phase 3 mandatory checklist including changelog-style rules summary, trailers checklist, checkpatch reference moved there from README, and final verification before git commit. Do not proceed to git commit without completing the Phase 2 self-review gate above — it applies whether or not a second reviewer is ever involved. CONTRIBUTING's adversarial-review requirement for norm changes to this style guide itself is a separate, additional gate for changes to the repository's own normative content; see CONTRIBUTING.md §3.

---
*Phase 2 review checklist for kernel-style guide per README three-phase workflow. For peer review process specification see peer-review.md; for per-developer exemplars see exemplars.md; for meta rules see CONTRIBUTING.md.*
