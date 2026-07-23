---
name: commit
description: Phase 3 draft changelog checklist for Linux kernel style — mandatory changelog-style load when drafting commit message, trailers checklist, checkpatch reference moved here from README, distilled for token efficiency. Load during Phase 3 draft changelog on top of Phase 1 base and Phase 2 review base per README three-phase cumulative workflow.
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
- `exemplars.md` — annotated real-commit examples per developer voice. Keep resident through Phase 3 if loaded at Phase 2 review gate as mandatory per plan, which is typical workflow order. Unload at task end.

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
 - Explain WHY with data; paste raw kernel message verbatim for bugfixes — KASAN/WARNING/oops/Call Trace as indented literal block, not paraphrase. Must appear, not optional.
 - Write for upstream audience not internal tooling per audience relevancy rule — strip internal agent nicknames, private bucket hashes without public syzbot link, internal branch names, hostnames, build IDs, vendor ticket IDs. Use generic phrasing.
 - Trailers: Fixes: + Cc: stable paired, Reported-by, Link to lore, Assisted-by for non-trivial tool work, Signed-off-by for DCO certification.
 - Tone calm factual engineer-to-engineer, active voice, no marketing adjectives hedging filler em-dash sprinkling or recap.

3. Load peer-review.md mandatory during Phase 3 changelog drafting as final self-review gate before git commit.

4. Run llm-tells-checklist.md final pass against commit message draft to verify no LLM tells slipped in: no "This patch" opening, no vague justification without numbers, no marketing adjectives, no hedging filler, no recap paragraph, no em-dash sprinkling, no mixed verb tense, no over-bulleting, no templated Pros/Cons, no hyper-formal tone, no ornate verbs, no inferable boilerplate, no verbose operational detail, no internal identifiers, no invented facts numbers or commit hashes.

5. Run checkpatch.pl script verification before posting patches — moved here from README.md per plan to keep README focused on index role while preserving checkpatch reference in Phase 3 final verification path where it is actually executed. Run `scripts/checkpatch.pl` script, which will check for other things that may need to be adjusted. No warnings expected with modified CONFIG options =y =m =n, and pass allnoconfig / allmodconfig and O=builddir per submit-checklist.rst.

6. Verify commit trailers per CONTRIBUTING.md §5 commit trailers required and per kernel-style repo history established forms: every commit must end with both trailers in order after blank line separating from commit message body:
 ```
 Assisted-by: <PROVIDER>:<MODEL> [<TOOL> or <ROLE>]
 Signed-off-by: Your Name <your.email@example.com>
 ```
 Use public provider:model names already appearing in git history for this repository — scan `git log --grep Assisted-by` before inventing new spelling. Current established forms verified in git history: `Assisted-by: Claude:claude-opus-4-8` for Claude-family models, `Assisted-by: Meta:avocado-tester` for Meta Avocado-family models. If using another provider model family follow same PROVIDER:MODEL pattern with capitalized provider name matching public model family naming — for example Gemini:gemini-3-pro would be appropriate format for Gemini models, adjust version as needed, but verify no prior established spelling already exists in git history before inventing new variant. List only public model names never internal-only tooling codenames. Multiple Assisted-by lines allowed ordered by contribution weight. An AI agent must never add its own Signed-off-by — only human SOB certifies DCO per kernel process.

7. Unload all files at task end after commit is written and trailers verified. Do not leave Phase-specific files resident between tasks to respect token budget.

## Next phase pointer

This is final phase of three-phase workflow. After Phase 3 completes with commit message drafted following above checklist and trailers verified, commit to git per `git commit` with descriptive commit message following repository's own style rules. For guidelines on modifying this style guide itself rather than using it to write kernel patches, see CONTRIBUTING.md which is loaded on demand when modifying rules rather than when writing kernel patches.

---
*Phase 3 draft changelog checklist per README three-phase workflow. For full changelog rules see changelog-style.md §1; for trailers and commit trailer requirements see CONTRIBUTING.md §5; for checkpatch usage see upstream scripts/checkpatch.pl documentation referenced here.*
