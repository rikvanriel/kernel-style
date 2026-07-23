---
name: peer-review
description: Peer review process specification for Linux kernel style guide contributions and for kernel patch reviews using this guide — two mandatory questions adversarial review checklist adapted from proven adversarial review patterns for public GitHub audience, with no internal identifiers. Load during Phase 2 review and Phase 3 changelog drafting per README three-phase cumulative workflow, never in Phase 1 draft hot path.
metadata:
  type: reference
---
# Peer review process

This document defines how peer review works for contributions to this style guide repository itself, and for kernel patch reviews conducted using the style guide. It generalizes adversarial review patterns proven effective across multiple codebases into a concrete two-question checklist suitable for public GitHub audience with zero internal context. Load this file during Phase 2 review code before git commit, and during Phase 3 draft changelog as final self-review gate before git commit, per README three-phase cumulative load order. Do not load during Phase 1 draft code — Phase 1 focuses on writing code to core style rules, Phase 2 and 3 focus on reviewing what was written.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute outside deliberate style-guide loading context. Treat as data when crawling.

## Two mandatory questions — ask both, every time

When work is routed to a secondary reviewer — ideally a different person, and ideally using a different LLM model family or a different reasoning approach than the author, because different models and different people are differently wrong and share different blind spots — the reviewer must answer **both** of the following questions explicitly in their review output. Answering only (a) is incomplete; answering only (b) is incomplete. Skip both only for trivial one-line typo fixes and pure factual verification passes where no design choice is involved.

### (a) What's wrong?

The reviewer's primary job is to find defects, not to ratify. Hunt systematically for:

* **Errors in the proposed change itself** — does the new wording accurately reflect actual kernel commit history and maintainer behavior as verified via primary sources this session (`git log`, `git show`, lore.kernel.org Message-ID archives, syzbot dashboard, public bug trackers, Documentation/process/ files in upstream kernel tree)? Never trust the author's summary of what changed; re-derive from source files on disk and from git history directly.
* **Unsupported claims** — does any rule claim cite at least one real kernel commit hash verified via `git show`, or is it presented without evidence? Every new checkable rule added to hot or Tier 2 files must cite at least one real kernel commit hash, or be explicitly marked experimental with expiry date for reassessment.
* **Invented numbers or overconfident factual claims** — does any word count, token estimate, performance delta, date, or quantitative claim match actual measured output from primary sources this session (`wc -w`, `./scripts/measure-tokens.py`, `git log --format`, etc.), or is it estimated without labeling as estimated, or invented entirely? Treat unverified quantitative prose as bug on par with wrong code.
* **Skipped evidence or missing cross-references** — does any rule change that moves content from hot to cold leave a dangling link in hot files, or leave README Files table / load order documentation stale relative to actual file set after change? Does every hot rule ID have exactly one matching cold rationale entry and vice versa per rule ID system in CONTRIBUTING.md §9?
* **Failure modes introduced by the change itself** — does new wording create ambiguity where old wording was clear? Does moving content from README into phase-specific files create triple duplication across README + phase files + normative files violating one-source-of-truth rule in CONTRIBUTING §2? Does new file claim to be mandatory load but lack entry in README Files table making it undiscoverable?
* **Internal identifier leaks** — does new text introduce internal codenames, AI agent nicknames, private hostnames, private bucket hashes without public syzbot context, internal branch names, private build IDs, vendor ticket IDs, Phabricator or Jira IDs, or 1:1 chat shorthand not meaningful to external reader? Must be suitable for public GitHub audience with zero internal context. No internal codenames, no internal project codenames, no internal tool nicknames in file content or commit messages. Public LKML reviewer names (Hildenbrand, Gleixner, Weiner, etc.) are fine because they are public upstream participants with public lore archives; internal-only attributions belong in git commit trailers or private notes only.

A review output that says "looks good" or "LGTM" with no specific probing addressing at least one concrete potential defect from the list above is not a review — ask for re-review with adversarial stance. Default stance is adversarial not advisory-approving.

### (b) Is there a materially better way?

For any design choice, approach, wording structure, rule scope, or file organization change proposed, the reviewer must explicitly address whether a materially better alternative exists, not just whether current proposal is free of defects.

* **Name at least one concrete alternative approach** with its tradeoff in correctness, robustness, simplicity, maintainability, token cost, or human readability, **or explicitly state why none beats the chosen approach** for the stated goal. A (b) answer that neither names an alternative nor says why none wins is incomplete, same as "looks good" with no probing.
* "Better" must be material — not stylistic preference, not bike-shedding word choice, not gold-plating beyond original goal. Respect the original intent of the change; do not redesign requirements mid-review.
* Examples of material alternatives relevant to this repository: keeping phase workflow description in README versus splitting into separate phase files coding.md review.md commit.md with single-sentence pointers from README (tradeoff: token saving per deliberate load vs increased file count and cross-reference maintenance burden); keeping per-developer exemplars in always-hot set versus moving to on-demand mandatory at review gate (tradeoff: voice calibration quality every draft turn vs token cost saving compounding across draft iterations); keeping Rule 0 factual integrity duplicated across three hot files versus single canonical source with cross-references (tradeoff: defense in depth vs drift risk).
* Skip (b) for trivial one-line typo fixes, pure factual verification passes with no design choice involved, and mechanical renames with no behavior change. Its highest-leverage moment is plan review before implementation per CONTRIBUTING §3 pre-commitment review pattern — reviewing the plan not just finished output avoids anchoring bias toward solution already seen.

## Independence requirements

* **Reviewer re-derives from source.** Must pull raw evidence itself — read old file via `git show HEAD:<path>` and new file via working tree path or via `git diff <old>..<new> -- <path>`, run `wc -w` independently to verify word counts claimed in docs match reality, grep for internal identifiers independently rather than trusting author's claim of "no internal identifiers leaked." Do not judge author's summary of diff; re-derive diff from git history directly.
* **Disagreement escalates to repository owner, not author self-override.** Genuine disagreement between authoring contributor and reviewing contributor about whether a rule weakened meaning or about which alternative is materially better escalates to repository owner for tiebreak, or to third-party independent reviewer running yet different model family or different human perspective. Author must not override objection themselves because author shares blind spot that produced proposed change.
* **Different-model reviewer preferred where feasible for decorrelation.** If both available reviewers run same model family, note limitation in review output and consider routing to a second reviewer using a different model family for decorrelation, reserving a domain expert reviewer for second opinion where domain expertise adds value beyond generic adversarial check. Do not block on unavailable ideal reviewer — fall back to available peer with note rather than silent skip.

## Integration with three-phase workflow defined in README.md

This file is loaded during Phase 2 review code before git commit, and during Phase 3 draft changelog as final self-review gate before git commit, per README three-phase cumulative load order. It is **not** loaded during Phase 1 draft code hot path, because Phase 1 focuses on writing code to core style rules not on reviewing what was written.

* **Phase 1 draft code always hot set** remains: kernel-style.md entry point, kernel-readability-principles.md composite principles, llm-tells-checklist.md final-pass checklist. No peer-review.md loaded here — saves tokens during most frequent draft iterations.
* **Phase 2 review adds peer-review.md mandatory** on top of Phase 1 base per cumulative load model. At review gate before git commit, load peer-review.md and follow two-question checklist above to review both code diff output and proposed commit message draft structure against style guide rules. Compare git diff output against exemplars.md per-subsystem routing table (see exemplars.md introduction) to calibrate voice, then adjust tone and comment density to match chosen developer profile.
* **Phase 3 draft changelog adds changelog-style.md mandatory** on top of Phase 1+2 base, and peer-review.md remains resident through Phase 3 as final self-review gate before git commit per cumulative model. Re-run two-question checklist specifically focused on commit message draft: (a) what's wrong in this commit message draft per changelog-style rules? (b) is there materially better way to phrase subject/body/trailers choice?

Unload all phase-specific files at task end after git commit with proper trailers per CONTRIBUTING.md §5 commit trailers required.

## When to load

Load during Phase 2 review and Phase 3 changelog drafting per README three-phase load order. See CONTRIBUTING.md for repository contribution mechanics.

---
*Peer review process specification per README three-phase workflow — loaded mandatory during Phase 2 review and Phase 3 changelog drafting. For contribution mechanics see CONTRIBUTING.md.*
