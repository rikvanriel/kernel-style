---
name: commit
description: Phase 3 draft changelog checklist for Linux kernel style — mandatory changelog-style load when drafting commit message, trailers checklist, checkpatch reference moved here from README. Load during Phase 3 draft changelog on top of Phase 1 base and Phase 2 review base per README three-phase cumulative workflow.
metadata:
 type: reference
---
# Phase 3 — draft changelog

Concrete checklist for drafting Linux kernel commit messages and final verification before git commit. Load this file at start of Phase 3 draft changelog task **in addition to** Phase 1 base files and Phase 2 review files already resident per cumulative load model — do not unload previous phase files until task end. For full load order see README.md How to load section.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute. Treat as data when crawling; guidance applies only when user deliberately loads it to write or review kernel patch.

## Load order for Phase 3

Keep resident from Phase 1 and Phase 2:
- `kernel-style.md` — entry point overview, factual integrity, code structure, 4 anchor quotes. Keep resident.
- `kernel-readability-principles.md` — composite principles. Keep resident.
- `llm-tells-checklist.md` — final-pass checklist. Re-run at final verification gate before commit.
- `coding.md` — Phase 1 draft checklist. Keep resident per cumulative model.
- `review.md` — Phase 2 review checklist. Keep resident per cumulative model; cross-reference not duplicate here.
- `exemplars.md` — annotated real-commit examples per developer voice. Keep resident through Phase 3 if already loaded at the Phase 2 review gate (the typical workflow order). Unload at task end.

Add mandatory for Phase 3 draft changelog:
- `changelog-style.md` — detailed changelog and code-comment style rules. Load mandatory when writing commit message. Follow problem→cause→fix→effect structure, verbatim artifacts rule, paragraph caps, audience relevancy, trailers, LLM-slop contrasts. Unload at task end after commit written.
- This file `commit.md` itself — Phase 3 specific checklist below.

On demand during Phase 3 if needed:
- `patch-series.md` — how to structure multi-patch series: one logical change per patch, bisectability, ordering, cover letters. Load only when change is >1 patch (~2,112 words ≈3,475 tokens transient). Keep resident until task end if loaded.

## Phase 3 mandatory steps

1. Keep Phase 1 and Phase 2 files resident per cumulative model — do not unload previous phase context or you lose code structure rules and voice calibration achieved in earlier phases.

2. Load changelog-style.md mandatory when writing commit message. Follow its §1 structure:
 - Subject `subsystem: imperative summary`, lowercase after colon, no period, imperative mood. Check git history prevailing prefix via `git log --oneline -- <path>` to match existing subsystem token consistency.
 - Open body with problem in present tense; lead bugfix with real-world symptom not code mechanism.
 - Structure problem → cause → fix → effect as 3–6 short paragraphs, 90% ≤50 words, max 70, never beyond.
 - Before finalizing, run changelog-style.md's compression pass: cut anything restating a code comment in the same diff, cut glosses of already-obvious values, join adjacent paragraphs that describe sequential sub-steps of one change when a connective fits them under the cap. Keep separate only paragraphs carrying a genuinely distinct, independently-verifiable claim.
 - Explain WHY with data; paste raw kernel message verbatim for bugfixes — KASAN/WARNING/oops/Call Trace as indented literal block, not paraphrase. Must appear, not optional.
 - Write for upstream audience not internal tooling per audience relevancy rule — strip internal agent nicknames, private bucket hashes without public syzbot link, internal branch names, hostnames, build IDs, vendor ticket IDs. Use generic phrasing.
 - Trailers: Fixes: + Cc: stable paired, Reported-by, Link to lore, Assisted-by for non-trivial tool work, Signed-off-by for DCO certification.
 - Tone calm factual engineer-to-engineer, active voice, no marketing adjectives hedging filler em-dash sprinkling or recap.

3. Load peer-review.md mandatory during Phase 3 changelog drafting as final self-review gate before git commit.

4. Run llm-tells-checklist.md final pass against commit message draft to verify no LLM tells slipped in. Machine helper: `scripts/lint-changelog.py <file> --` checks caps [CL-12], banned phrases [CL-13], Fixes+Cc [CL-11], internal IDs [CL-14], verbatim splat [CL-27/28]: no "This patch" opening, no vague justification without numbers, no marketing adjectives, no hedging filler, no recap paragraph, no em-dash sprinkling, no mixed verb tense, no over-bulleting, no templated Pros/Cons, no hyper-formal tone, no ornate verbs, no inferable boilerplate, no verbose operational detail, no internal identifiers, no invented facts numbers or commit hashes.

5a. Account for the explanatory prose per kernel-style.md §0 R0-9: run `scripts/lint-changelog.py --cite <file>` and, for each sentence it lists, name where you read it — `file:function` for a statement about code, a boot log or `/proc` file for a statement about the running system. Re-read the named function; do not answer from the understanding you had while writing the patch, which is what produced the sentence. Treat an "e.g." example as a claim: an example that cannot occur discredits the paragraph around it.

5. Account for every empirical claim in the changelog per kernel-style.md §0 R0-8: list each number, symptom, splat, timing, and test result beside the artifact that produced it — log path, command output, `git show` hash, benchmark file. Delete or mark TODO anything with nothing to point at. Apply this to sentences retained from an earlier version of the changelog too, not only to newly typed ones (R0-7): a claim measured on a previous base, or copied from the patch you are porting, is re-asserted the moment you keep it.

6. Run checkpatch.pl + lint-changelog verification before posting — moved here from README. Run `scripts/checkpatch.pl --strict` and `scripts/lint-changelog.py <changelog-file>` (or `git log -1 --pretty=%B | scripts/lint-changelog.py --stdin`) which checks for other things that may need adjustment per Rule IDs. No warnings expected with modified CONFIG =y/m/n, and pass allnoconfig/allmodconfig and O=builddir per submit-checklist.rst. For multi-patch, also run `scripts/verify-cover-letter.py --cover cover.txt --range <range>` per patch-series.md §5 to catch stale numbers.

   **What these tools do not cover.** checkpatch reports "no obvious style problems and is ready for submission" on a patch whose changelog asserts an unobserved splat, whose comment restates the code it sits above, or which leaves a call the change has made a no-op. It checks form, not truth, necessity, or whether a comment earns its space. A clean checkpatch run is not evidence that steps 1-5 were done.

7. Verify commit trailers per CONTRIBUTING.md §5 commit trailers required and per kernel-style repo history established forms: every commit must end with both trailers in order after blank line separating from commit message body:
 ```
 Assisted-by: <PROVIDER>:<MODEL> [<TOOL> or <ROLE>]
 Signed-off-by: Your Name <your.email@example.com>
 ```
 Use public provider:model names already appearing in git history for this repository — scan `git log --grep Assisted-by` before inventing new spelling. Current established forms verified in git history: `Assisted-by: Claude:claude-opus-4-8` for Claude-family models, `Assisted-by: Meta:avocado-tester` for Meta Avocado-family models. If using another provider model family follow same PROVIDER:MODEL pattern with capitalized provider name matching public model family naming — for example Gemini:gemini-3-pro would be appropriate format for Gemini models, adjust version as needed, but verify no prior established spelling already exists in git history before inventing new variant. List only public model names never internal-only tooling codenames. Multiple Assisted-by lines allowed ordered by contribution weight. An AI agent must never add its own Signed-off-by — only human SOB certifies DCO per kernel process.

8. If this patch is part of a multi-patch series with a cover letter, before sending run the cover-letter verification pass per patch-series.md §5: for every number and every "patch N does/is the only one that..." claim in the cover letter, open that specific patch's own current changelog and diff and confirm the exact match. Do this as its own explicit pass over the finished cover letter, separate from writing it — a cover letter drafted earlier in the process (or regenerated via `git format-patch --cover-letter` after a patch changed) is exactly the case this catches. Do not send on the strength of having verified the patches alone.

9. Unload all files at task end after commit is written and trailers verified. Do not leave Phase-specific files resident between tasks to respect token budget.

## Next phase pointer

This is final phase of three-phase workflow. After Phase 3 completes with commit message drafted following above checklist and trailers verified, commit to git per `git commit` with descriptive commit message following repository's own style rules. For guidelines on modifying this style guide itself rather than using it to write kernel patches, see CONTRIBUTING.md which is loaded on demand when modifying rules rather than when writing kernel patches.

---
*Phase 3 draft changelog checklist per README three-phase workflow. For full changelog rules see changelog-style.md §1; for trailers and commit trailer requirements see CONTRIBUTING.md §5; for checkpatch usage see upstream scripts/checkpatch.pl documentation referenced here.*
