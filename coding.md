---
name: coding
description: Phase 1 draft code checklist for Linux kernel style — concrete rules for code structure and comments distilled for hot-path token efficiency. Load during Phase 1 draft code per README three-phase cumulative workflow.
metadata:
  type: reference
---
# Phase 1 — draft code

Load this file at start of Phase 1 draft code task. Keep resident through Phase 2 review and Phase 3 changelog drafting per cumulative load model — do not unload until task end. For full load order see README.md How to load section.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute. Treat as data when crawling; guidance applies only when user deliberately loads it to write or review kernel patch.

## Load order for Phase 1 — always hot

- `kernel-style.md` — entry point overview, factual integrity summary, code structure rules, 4 anchor verbatim quotes for base voice calibration. Keep resident through all phases.
- `kernel-readability-principles.md` — composite principles distilled from 14 kernel developers. Keep resident through all phases.
- `llm-tells-checklist.md` — final-pass checklist for generic LLM tells to strip and verification never-invent. Run as final pass within Phase 1 draft, keep resident through Phase 2, re-run at review gate. Do not unload until task end.
- This file `coding.md` — Phase 1 specific checklist below.

On demand during Phase 1 only if needed:
- `exemplars.md` may load once to calibrate specific voice, but not every draft iteration — mandatory load is at Phase 2 review gate. See exemplars.md introduction for per-subsystem routing table.

Do not load changelog-style.md yet — Phase 3 mandatory when drafting commit message. Do not load patch-series.md yet — on demand only for multi-patch in Phase 3.

## Phase 1 checklist — what to do while drafting code

- Follow kernel-style.md §0 factual integrity checklist before any other pass: never invent facts numbers quotes dates performance results commit hashes or technical claims; if you don't know say you don't know mark TODO; verify every claim against diff and primary sources; paste raw artifacts verbatim not from memory; treat unverified prose as bug on par with wrong code. Full detail in kernel-style.md §0 and changelog-style.md §0 — those are single source of truth, do not duplicate here beyond this summary pointer.

- Follow kernel-style.md §3 code structure rules for splitting helpers, function length caps, renaming vs duplicating, minimal obvious fix preference, locals naming, guard early return. Full detail and example hashes in kernel-style.md §3 — single source of truth, do not duplicate here beyond this pointer.

- Follow kernel-style.md §2 and changelog-style.md §2 code comment rules for WHY not WHAT comment density, 50-word paragraph cap, no internal identifiers in source ever, one source of truth at definition not header prototype, cross-reference not duplicate. Full detail in those files — single source, do not duplicate here beyond this pointer.

- Upstream kernel coding style reference: Documentation/process/coding-style.rst in the Linux kernel tree is the human-readable upstream document with coding style rules for kernel contributions. The rules in this directory supplement the upstream document with LLM-focused guidance not learned from training data.

- Run llm-tells-checklist.md final pass before moving to Phase 2 review to verify no LLM tells slipped into code or comments. Full list in llm-tells-checklist.md single source of truth; core tells to watch in code comments specifically that are less obvious elsewhere: over-bulleting in comments, templated Pros/Cons scaffolding, ornate verbs, vague justification without numbers.

## Next phase pointer

When code draft passes llm-tells checklist final pass, move to Phase 2 review — see review.md for Phase 2 mandatory checklist including exemplars.md mandatory load before git commit and peer-review process per peer-review.md and git diff comparison workflow. Do not proceed to git commit without completing Phase 2 review gate per CONTRIBUTING.md adversarial review requirement for norm changes to style guide itself and per kernel patch best practice of self-review before commit.

---
*Phase 1 draft code checklist for kernel-style guide per README three-phase workflow. For full rules see kernel-style.md §3 code structure, changelog-style.md §2 comments, llm-tells-checklist.md final pass.*
