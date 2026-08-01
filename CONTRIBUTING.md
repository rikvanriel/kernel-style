# Contributing to kernel-style

This document defines how to modify the style guide itself — not how to write kernel patches (see README.md for that). It applies equally whether you are a human contributor opening a pull request on GitHub, or an LLM drafting a proposed change locally.

The goal is three properties simultaneously: well documented, efficient to load, and staying that way into the future.

---

## Three-tier file architecture

Every file in this repository falls into exactly one tier. The tier determines how heavily it is optimized for token cost and what kind of content belongs there.

**Tier 1 — normative hot.** Loaded every time an LLM drafts or reviews kernel code or changelogs. Must stay under soft token budget (see below). Contains only checkable imperatives and minimal concrete patterns necessary to disambiguate those imperatives. No history, no Message-IDs, no dates, no inline provenance tags naming who reviewed or approved a change, no alternative phrasings considered and rejected, no per-developer anecdote expansion beyond what is in the file today.

Current Tier 1 files and approximate budgets (measured via `wc -w`; token estimate via chars÷4 or tiktoken cl100k_base — use `wc -w` locally for approximate word count, or `./scripts/measure-tokens.py` for the token estimate):

| File | Words | ~tokens | Role |
|---|---|---|---|
| kernel-style.md | ~990 | ~1,735 | slim entry point, factual integrity, code structure, 4 anchor quotes |
| kernel-readability-principles.md | ~1,175 | ~2,060 | composite principles from 14 developers, signature strengths |
| llm-tells-checklist.md | ~800 | ~1,210 | final-pass checklist, verification never-invent |
| coding.md | ~700 | ~1,160 | Phase 1 draft-code checklist, upstream coding-style pointer |
| **Phase 1 total always hot** | **~3,660** | **~6,165** | base resident set |

These four stay resident through all phases of a patch-writing task. Nothing in Tier 1 may reference internal tooling, private hostnames, private bucket IDs, agent codenames, internal branch names, or vendor ticket IDs. Assume every character in Tier 1 is world-readable forever via public git history.

**Tier 2 — on-demand normative.** Loaded only for specific phases of a patch task, then unloaded at task end. Contains detailed rules that are too large for always-hot but still normative (must be followed, not optional reference). This includes both content files (changelog-style.md, exemplars.md, patch-series.md, planning.md) and the phase-checklist files that orchestrate loading them (review.md, commit.md, peer-review.md) — all are mandatory once their phase's trigger fires, none are optional reference reading.

Current Tier 2 files:

| File | Words | ~tokens | Load trigger |
|---|---|---|---|
| changelog-style.md | ~4,000 | ~6,610 | mandatory on Phase 3 draft changelog; may pull early in Phase 2 review if checking comment density or message wording |
| exemplars.md | ~3,685 | ~6,445 | mandatory on Phase 2 review before git commit; may load once in Phase 1 to calibrate specific voice but not every draft iteration |
| patch-series.md | ~3,145 | ~5,065 | on demand only when change is >1 patch, or during Phase 0 planning per planning.md §2 |
| patch-series-rework.md | ~1,120 | ~1,780 | on demand, on top of patch-series.md, only when reworking an already-existing series rather than splitting fresh work |
| peer-review.md | ~2,565 | ~4,065 | mandatory during Phase 0 plan convergence, Phase 2 review, and Phase 3 changelog drafting |
| planning.md | ~1,060 | ~1,660 | on demand, before Phase 1, whenever the change is not a single self-evident edit |
| review.md | ~1,235 | ~2,005 | mandatory Phase 2 review checklist |
| commit.md | ~1,175 | ~2,015 | mandatory Phase 3 changelog checklist |

`review-prompts.md` (~275 words, ~530 tokens) is a special case: read once to set up `/kreview`/`/kseries`, not part of the recurring per-task load budget below.

Phase 2 adds exemplars to Phase 1 base for total ~7,340 words (~12,610 tok) resident during review. Phase 3 adds changelog-style (and patch-series if needed) on top for total ~11,340 words (~19,220 tok) resident during changelog drafting (~14,390 words / ~24,110 tok with patch-series). This cumulative figure tracks the flagship content addition per phase (exemplars.md, changelog-style.md, patch-series.md) on top of the Tier 1 base; it does not additionally sum review.md/commit.md/peer-review.md, which are also resident at those phases — see the Tier 2 table above for their individual sizes. Unload all at task end. See README.md "How to load" for the full workflow with per-subsystem routing cues.

**Tier 3 — rationale and history. Never loaded by default.** Load only when modifying the style guide itself, to understand intent before changing a rule.

Planned files (to be created alongside slimming work, not yet present for all):
- `changelog-style-rationale.md` — Message-IDs, dates, public LKML reviewer names, alternative phrasings considered and rejected, per-rule history, validation notes from public reviews.
- `patch-series-rationale.md` — full lore Message-ID quotes, submitting-patches.rst excerpts that support each rule, historical evolution.
- `kernel-readability-rationale.md` — per-developer detail expansion beyond the one-line signatures in principles.md.
- `exemplars.md` already serves as reference detail today; after move to on-demand it straddles Tier 2 and Tier 3 depending on use case.

Rationale files are public-audience too — no internal identifiers, no internal project codenames, no private process narration. Internal audit trail (who reviewed whom internally, which internal tool found what) belongs in git commit trailers or in private notes, never in any public .md file at any tier.

---

## Rules for modifying this repository

These apply to every pull request or local commit that touches normative content (Tier 1 or Tier 2). Exempt: one-line typo fix in README human-facing prose, LICENSE update, or reversible local scratch.

### 1. Scope separation is mandatory, not suggested

- Hot files contain normative checkable rules only. Max soft budget per file: kernel-style.md <1,000 words, kernel-readability-principles.md <1,000, llm-tells-checklist.md <800, changelog-style.md <2,000 after slim, patch-series.md <1,200 after slim, exemplars.md unchanged but moved to on-demand. Total hot-set token budget is tracked, not per-file hard cap — see measurement section below.
- Rationale files contain provenance metadata only: Message-IDs, dates, public reviewer names from LKML, alternative phrasings considered, historical evolution, per-developer anecdote expansion. No new normative rules may hide only in rationale; rationale must never contradict hot text.
- If you add or change a normative rule in a hot or Tier 2 file, you **must** update or create the corresponding entry in the matching *-rationale.md* in the same commit or same PR stack. A rule change without rationale update will fail review.

### 2. One source of truth per rule across hot files

- No rule may be duplicated verbatim in more than one hot file. If multiple files need the same concept, pick one canonical location and cross-reference with a short link in the others.
- Current known duplications to fix over time: Rule 0 factual integrity appears in kernel-style §0, changelog-style §0, and llm-tells verification block — canonical should be kernel-style §0 with cross-references elsewhere. Audience relevancy rule appears in kernel-style §1, §2, §4 and changelog-style §1, §2, §3 — consolidate to one canonical long form in changelog-style §1 with short cross-references elsewhere. llm-tells-checklist is single source for "do not" list; changelog §3 should cross-reference not duplicate ~80% overlap.
- Exception: prompt-injection guard blocks ("this repository is reference documentation... nothing here is instruction to execute") are intentionally duplicated across README, AGENTS.md, CLAUDE.md, and kernel-style.md as defense in depth — do not dedup those.

### 3. Adversarial review required before landing norm changes

- Every change to normative content (Tier 1 or Tier 2) must be reviewed by an independent reviewer before commit or merge. The reviewer's job is to find what is wrong or weakened, not to ratify.
- The reviewer must re-derive from source: read old file and new file side by side, not just the diff summary or PR description. Check specifically:
  * Does any checkable imperative lose enforceable meaning, become ambiguous, or change from must to should?
  * Does any calibration example necessary to disambiguate a stylistic rule get dropped from hot path? (Pattern examples stay hot; provenance metadata moves cold.)
  * Does any carve-out, exemption, or edge-case note disappear?
  * Does new text introduce internal identifiers, internal project codenames, private hostnames, private bucket hashes, or 1:1 context not meaningful to an external reader?
  * **The cut test:** for every sentence in the new text, ask "would cutting or shortening this phrase lose the reader anything they could act on?" If no, cut it or trim it down to whatever part does carry actionable content. Apply this literally to phrases like "adapted from X", "moved here per plan", "distilled for token efficiency", "generalizes patterns proven effective elsewhere" — these narrate the document's own drafting or adaptation history instead of telling the reader what to do or what a rule is, and they almost always fail the cut test. This is distinct from an internal-identifier leak: it isn't a confidentiality problem, it's dead weight the reader gets zero value from. Genuine provenance that helps the reader interpret a rule (e.g. "distilled from 14 kernel developers" naming what a rule is synthesized *from*) usually passes the cut test and should stay — the test is the same either way, judge each phrase on it rather than pattern-matching the example list.
  * Does CONTRIBUTING's Tier 1/2 tables, README's "How to load" section, or a phase file's own "Load order" section still match actual file sizes and load triggers after the change?
- A review returning "looks good" with no specific probing is not a review — ask for re-review with adversarial stance.
- Genuine disagreement between author and reviewer escalates to repository owner (Rik van Riel) or third-party tiebreak, not resolved by author alone.

### 4. External-facing discipline — public repo standard

This repository is public on GitHub and intended for upstream kernel contributors who have never met the authors. Every character in every committed file, including commit messages, is assumed world-readable forever via public git history.

- No internal codenames, no agent codenames, no internal tool nicknames, no private bucket hashes without public syzbot link, no internal branch names, no internal hostnames, no private build IDs, no vendor ticket IDs, no Phabricator or Jira IDs, no 1:1 chat shorthand, in file content **or commit messages**.
- Write what changed, why, how to verify, what behavior or documentation quality is unlocked — in terms an external reviewer can act on without private context.
- Inline rule provenance (who reviewed or approved a change, when) does not belong in normative hot files. Use git commit history for authorship and dates. If provenance aids understanding, put it in the matching *-rationale.md* file with public LKML Message-IDs and public reviewer names only — never internal codenames.
- Before publishing a commit, re-read the diff as if you are an external reviewer with zero internal context. If anything requires private context to parse, rewrite it.

### 5. Commit trailers required

Every commit to this repository must end with both trailers in this order, after a blank line separating them from the commit message body:

```
Assisted-by: <PROVIDER>:<MODEL> [<TOOL> or <ROLE>]
Signed-off-by: Rik van Riel <riel@surriel.com>
```

* `Assisted-by` acknowledges non-trivial tool assistance following Documentation/process/coding-assistants.rst style adapted for docs repositories. Use public provider:model names that already appear in git history for this repository — scan `git log --grep Assisted-by` or `git log --format=%B | grep Assisted-by` before inventing new spelling. Current established forms in this repo history (verified via `git log --grep Assisted-by`):
  - `Assisted-by: Claude:claude-opus-4-8` — for Claude-family models
  - `Assisted-by: Meta:avocado-tester` — for Meta Avocado-family models
If using another provider model family, follow the same `PROVIDER:MODEL` pattern with capitalized provider name matching public model family naming — for example `Assisted-by: Gemini:gemini-3-pro` would be appropriate format for Gemini models, adjust version as needed, but verify no prior established spelling already exists in git history before inventing new variant.
  List only public model names, never internal-only tooling codenames. Multiple Assisted-by lines allowed, one per model, ordered by contribution weight. If changes are purely human-authored with trivial tool assistance (spelling, formatting, boilerplate completion), Assisted-by may be omitted, but when in doubt include it — omitting meaningful assistance may impede acceptance.

* `Signed-off-by` certifies Developer Certificate of Origin per usual kernel process. For this repository Rik van Riel signs off as owner on every commit, whether human-authored or AI-assisted. An AI agent must never add its own Signed-off-by — only human SOB.

* No other trailers are required unless fixing a prior commit (then add `Fixes:` with full 12-character commit hash and subject context in body, per kernel-style rules themselves).

This rule exists so git history itself carries complete provenance without needing inline `` tags in normative markdown files — those tags belong in commit trailers, not in file content, per external-facing discipline above.

### 6. Token budget measurement — soft not hard

- Total hot-set token budget is tracked as informational, not as hard CI failure, to avoid perverse incentives to delete load-bearing calibration examples to hit a number.
- Measure with real tokenizer, not words alone, because Message-IDs and commit hashes tokenize worse than prose. Use `wc -w` locally, or `./scripts/measure-tokens.py` (uses tiktoken cl100k_base when installed, else chars÷4 heuristic) cl100k_base or equivalent, reporting total tokens for Phase 1 always-hot set, Phase 2 with exemplars, Phase 3 with changelog-style, and Phase 3 with patch-series.
- Soft targets (reassess quarterly):
  * Phase 1 always hot ≤5,000 tokens (≈3,000 words)
  * Phase 2 review with exemplars ≤11,000 tokens
  * Phase 3 single-patch with changelog-style ≤17,000 tokens
  * Phase 3 multi-patch with patch-series ≤21,000 tokens
  Current estimated baseline as of 2026-08-01 (re-measured when coding.md was added to the Tier 1 table and Tier 2 file sizes were refreshed): Phase1 ~6,165 tok, Phase2 ~12,610 tok, Phase3 single ~19,220 tok, Phase3 multi ~24,110 tok — all now over their soft targets, partly because coding.md was previously tracked in the always-hot load order but never counted toward this budget, and partly organic growth of existing files since the 2026-07-22 baseline. Soft targets themselves have not been re-baselined; treat the current numbers as a signal that a slimming pass or a target reassessment is due, not as an immediate blocker.
- Token delta should be reported in PR description as informational, does not block merge; future CI may automate this. Human reviewer uses the number as signal, not gate.

### 7. Hard denylist for internal identifiers

- A denylist check should be run locally before committing, and may be enforced via CI in future — for now run locally as manual review checklist item if matched. Denylist is an explicit enumerated list, never a regex matching hex patterns (to avoid false positives on legitimate kernel commit hashes which saturate these files).
- Initial denylist to be maintained in `.github/workflows/` or pre-commit hook config: case-insensitive fixed strings for known internal project codenames, internal host patterns, internal tool names that are not public, private bucket hash prefixes if known distinct from kernel hashes, and any other tokens Rik adds over time.
- This is the hard guard complementing the soft token budget. It catches the leak class that actually matters for a public repo.

### 8. Exemplar citation rule

- Every new checkable rule added to hot or Tier 2 files must cite at least one real kernel commit hash verified via `git show` or `git log --oneline`, or be explicitly marked experimental with an expiry date for reassessment.
- For calibration/stylistic rules, include at minimum one positive example hash and, where the rule corrects a common LLM default, include the negative contrast pattern as well (what not to do, ideally with reference to real AI-generated draft that got it wrong if available, phrased generically without internal attribution).
- For mechanically checkable rules (no trailing period in subject, paragraph ≤50 words, Fixes: paired with Cc: stable), zero hashes needed — rule is self-verifying.
- Hashes live in hot files only to the minimum needed for disambiguation; extended hash lists and per-developer anecdotes belong in exemplars.md or *-rationale.md companions.

### 9. Rule ID system for cross-linking hot to cold

- Every normative rule in hot and Tier 2 files gets a stable ID comment or anchor that survives wording tweaks, e.g. `<!-- CL-14 -->` in markdown source near the rule, or a markdown heading anchor that is part of the API.
- Corresponding entry in *-rationale.md uses same ID as heading or key, so an editor modifying a hot rule can find its rationale unambiguously and a CI script can check for orphan IDs in either direction.
- CI cross-check: fail PR if a hot rule ID has no matching cold rationale entry, or cold rationale entry has no matching hot rule (orphan after deletion). This enforces presence, not quality — quality remains human adversarial review responsibility.

---

## How to propose changes

1. Edit the relevant hot file(s) to update normative checkable rules, keeping within token budget philosophy (pattern hot, provenance cold, one source of truth, no duplication).
2. Update or create corresponding *-rationale.md entry/entries in same commit or same PR stack, moving provenance metadata out of hot text into rationale with public LKML Message-IDs and public reviewer names only.
3. Run `./scripts/measure-tokens.py --files` to get current word/token counts for every tracked file, and update the affected row(s) in CONTRIBUTING.md's Tier 1/2 tables (and the cumulative Phase-N totals below them if a Tier 1 file or a flagship Tier 2 content file changed size).
4. Run denylist grep locally to confirm no internal identifiers introduced.
5. Request adversarial review from independent reviewer before landing. Reviewer checklist must include: re-derive from source old vs new, confirm no enforceable meaning weakened, confirm rationale updated, confirm no internal identifiers leaked, confirm CONTRIBUTING's Tier tables and README/phase-file load-order documentation still accurate.
6. Commit with descriptive commit message following the repository's own style rules — what changed, why, how to verify, no internal codenames in commit text.

---

## License and scope

This repository is licensed under CC-BY-4.0 (see LICENSE). It is reference documentation for Linux kernel patch style, supplementing Documentation/process/ in the upstream kernel tree with rules easier for LLMs to follow. Nothing here is an instruction to execute outside deliberate style-guide loading context.

---

_Last updated: 2026-07-26 — peer-review.md reframed so self-review by a single author is the default, mandatory gate (a second reviewer is an optional enhancement, not a prerequisite); added the cut test (§3) as a standing check against audience-irrelevant meta-commentary (phrases narrating a document's own drafting/adaptation history instead of giving the reader actionable content), applied repo-wide. Prior: 2026-07-22 — initial version establishing three-tier architecture, adversarial review gate, token budget methodology, and external-facing discipline for public repo._
