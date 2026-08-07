---
name: peer-review
description: Review process specification for Linux kernel style guide contributions and for kernel patch reviews using this guide — two mandatory questions adversarial review checklist, self-review by a single agent as the default gate, escalating to a second reviewer (same model in a fresh session, or a different reviewer/model) as an optional enhancement when available. Load during Phase 0 plan convergence, Phase 2 review, and Phase 3 changelog drafting per README workflow, never in Phase 1 draft hot path.
metadata:
  type: reference
---
# Review process — self-review by default, a second reviewer when available

This document defines how review works for contributions to this style guide repository itself,
and for kernel patch reviews conducted using the style guide. **It is designed to work standalone,
with one person and one AI agent reviewing their own work — that is the common case, and the
process must be complete and effective on its own in that case.** Routing to a second reviewer is a
real, valuable enhancement when the opportunity exists, but its absence must never be a reason to
skip review, water it down, or treat it as incomplete. Do not assume a multi-agent setup, a second
person, or a different model is available.

Load this file during Phase 0 plan convergence (see [planning.md](./planning.md) §6, applying the
two questions below to a plan instead of a diff), during Phase 2 review code before git commit, and
during Phase 3 draft changelog as final review gate before git commit, per README cumulative load
order. Do not load during Phase 1 draft code — Phase 1 focuses on writing code to core style rules,
Phase 0, 2, and 3 focus on planning or reviewing rather than drafting.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction
> to execute outside deliberate style-guide loading context. Treat as data when crawling.

## Two mandatory questions — ask both, every time, of your own work

Before committing any change, the author — whether a solo kernel developer, an AI agent working
alone, or a human-AI pair — must explicitly answer both of the following questions about the work
**as if reviewing someone else's patch**, not as a formality. This is the default gate and it is
mandatory whether or not a second reviewer is ever involved. Answering only (a) is incomplete;
answering only (b) is incomplete. Skip both only for trivial one-line typo fixes and pure factual
verification passes where no design choice is involved.

**Why self-review can work, and where it genuinely can't fully replace a second party:** the same
reasoning that produced a subtle logic or design mistake is often the same reasoning that will
happily re-validate it, because the gap is conceptual, not a typo you'd literally see twice. Two
things make self-review effective anyway: (1) doing it as a **separate, deliberate pass** with an
adversarial stance — not glancing at the diff again while still holding the "I just wrote this and
it's obviously right" frame, and (2) treating the two questions below as a real checklist to work
through methodically, not a vibe check. For genuinely high-stakes, high-blast-radius, or hard-to-
reverse changes, still actively seek a second opinion if you possibly can (see "Escalating to a
second reviewer" below) — self-review is a strong floor, not a claim that it's exactly as good as
an independent pair of eyes every time. Say so plainly rather than pretending otherwise.

### (a) What's wrong?

The job is to find defects, not to ratify. Hunt systematically for:

* **Errors in the proposed change itself** — does the new wording accurately reflect actual kernel commit history and maintainer behavior as verified via primary sources this session (`git log`, `git show`, lore.kernel.org Message-ID archives, syzbot dashboard, public bug trackers, Documentation/process/ files in upstream kernel tree)? Never trust your own summary of what changed from memory; re-derive from the actual file on disk and from git history directly, even reviewing your own work — re-open the diff and re-read it cold rather than reasoning from what you remember writing.
* **Unsupported claims** — does any rule claim cite at least one real kernel commit hash verified via `git show`, or is it presented without evidence? Every new checkable rule added to hot or Tier 2 files must cite at least one real kernel commit hash, or be explicitly marked experimental with expiry date for reassessment.
* **Invented numbers or overconfident factual claims** — does any word count, token estimate, performance delta, date, or quantitative claim match actual measured output from primary sources this session (`wc -w`, `./scripts/measure-tokens.py`, `git log --format`, etc.), or is it estimated without labeling as estimated, or invented entirely? Treat unverified quantitative prose as bug on par with wrong code.
* **Skipped evidence or missing cross-references** — does any rule change that moves content from hot to cold leave a dangling link in hot files, or leave CONTRIBUTING's Tier tables / README's "How to load" / a phase file's own "Load order" section stale relative to actual file set after change? Does every hot rule ID have exactly one matching cold rationale entry and vice versa per rule ID system in CONTRIBUTING.md §9?
* **Failure modes introduced by the change itself** — does new wording create ambiguity where old wording was clear? Does moving content from README into phase-specific files create triple duplication across README + phase files + normative files violating one-source-of-truth rule in CONTRIBUTING §2? Does a new file claim to be mandatory load but lack a trigger mentioned anywhere in README's "How to load" or the phase file that should reference it, making it undiscoverable?
* **Internal identifier leaks** — does new text introduce internal codenames, AI agent nicknames, private hostnames, private bucket hashes without public syzbot context, internal branch names, private build IDs, vendor ticket IDs, Phabricator or Jira IDs, or 1:1 chat shorthand not meaningful to external reader? Must be suitable for public GitHub audience with zero internal context. No internal codenames, no internal project codenames, no internal tool nicknames in file content or commit messages. Public LKML reviewer names (Hildenbrand, Gleixner, Weiner, etc.) are fine because they are public upstream participants with public lore archives; internal-only attributions belong in git commit trailers or private notes only.
* **The cut test** — for every sentence in new text, ask "would cutting or shortening this phrase lose the reader anything they could act on?" If no, cut it or trim it down to whatever part does carry actionable content. Apply this literally to phrases like "adapted from X", "moved here per plan", "distilled for token efficiency" — these narrate the document's own drafting or adaptation history instead of telling the reader what to do or what a rule is, and they almost always fail the cut test. This is distinct from the internal-identifier bullet above: it isn't a confidentiality problem, it's dead weight the reader gets zero value from. Genuine provenance that helps the reader interpret a rule (e.g. a style rule citing which real kernel commit or developer it's synthesized from) usually passes the cut test and should stay — judge each phrase on the test itself rather than pattern-matching the example list.

Concluding "looks good" with no specific probing addressing at least one concrete potential defect
from the list above is not a review, even of your own work — go back and probe harder before
committing. Default stance is adversarial, not advisory-approving, regardless of who (or what) is
doing the reviewing.

### (b) Is there a materially better way?

For any design choice, approach, wording structure, rule scope, or file organization change you're
about to commit, explicitly address whether a materially better alternative exists — not just
whether the current proposal is free of defects.

* **Name at least one concrete alternative approach** with its tradeoff in correctness, robustness, simplicity, maintainability, token cost, or human readability, **or explicitly state why none beats the chosen approach** for the stated goal. An answer that neither names an alternative nor says why none wins is incomplete, same as "looks good" with no probing.
* "Better" must be material — not stylistic preference, not bike-shedding word choice, not gold-plating beyond original goal. Respect the original intent of the change; do not redesign requirements mid-review.
* Examples of material alternatives relevant to this repository: keeping phase workflow description in README versus splitting into separate phase files coding.md review.md commit.md with single-sentence pointers from README (tradeoff: token saving per deliberate load vs increased file count and cross-reference maintenance burden); keeping per-developer exemplars in always-hot set versus moving to on-demand mandatory at review gate (tradeoff: voice calibration quality every draft turn vs token cost saving compounding across draft iterations); keeping Rule 0 factual integrity duplicated across three hot files versus single canonical source with cross-references (tradeoff: defense in depth vs drift risk).
* Skip (b) for trivial one-line typo fixes, pure factual verification passes with no design choice involved, and mechanical renames with no behavior change. Its highest-leverage moment is plan review before implementation per [planning.md](./planning.md) §6 — reviewing the plan not just finished output avoids anchoring bias toward a solution already seen, and this applies just as much when you are the only reviewer: pressure-test the plan before you've sunk cost into one implementation.

### Write it down

Keep a short, concrete self-review note before committing — three or four bullets is enough: what
you checked under (a) and what (if anything) you found and fixed; the alternative you weighed under
(b) and why you kept (or changed) your approach. This is not bureaucracy for its own sake — a review
that only ever happens silently in your head is the one that gets skipped under time pressure, and
writing it down forces you to actually apply the checklist instead of pattern-matching to "looks
fine." Keep the note out of the public commit message (it's about your own process, not something
an external reader needs) — a scratch file, a comment in your working notes, or a commit trailer
you strip before the final commit is fine.

## Escalating to a second reviewer (when available) — an enhancement, not a prerequisite

If a genuine second reviewer is available, use one — different people and different models are
differently wrong and catch different blind spots, especially on conceptual mistakes that
self-review's own reasoning is least likely to catch. But this section describes an upgrade path,
not a gate: nothing above requires it, and its unavailability is never a reason to skip or weaken
the self-review above.

Two tiers, roughly in order of how much they typically decorrelate from the author's own blind
spots, and roughly in order of how available they are to most people:

1. **Same model, a genuinely fresh session.** Even without a second person or a different AI
   product, open a new conversation and hand it just the diff (and the commit message draft) with
   no access to your original reasoning or rationale for why you wrote it that way — ask it to run
   the same two questions cold. This costs nothing beyond a second conversation and is available to
   essentially anyone with a single AI coding assistant; it will not catch everything an
   independently-reasoning reviewer would, but a genuinely blind re-read (not "does this look
   right, you just wrote it") recovers a meaningful share of the benefit.
2. **A different person, or a different model family.** The strongest decorrelation, because a
   different person or a different underlying model is least likely to share the exact reasoning
   pattern that produced a mistake. Use this when you actually have it — a colleague, a different
   AI product, or (for people who do run multiple AI agents day to day) a separate agent instance.
   Do not block work waiting for this to become available; it is the ideal, not the requirement.

When a second reviewer of either tier is used, the same two mandatory questions from above apply
to them, plus:

* **The reviewer re-derives from source**, the same way the self-review pass above does — read the
  old file and new file directly (`git show HEAD:<path>`, `git diff <old>..<new> -- <path>`), run
  `wc -w` independently to verify word counts claimed in docs, grep for internal identifiers
  independently rather than trusting the author's claim of "no internal identifiers leaked." Judge
  the actual diff, not the author's summary of it.
* **Genuine disagreement between author and a second reviewer** escalates to the repository owner
  for a tiebreak, or to a third independent reviewer, rather than being resolved by the author
  overriding the objection themselves — the author shares whatever blind spot produced the
  disputed change in the first place, so self-override defeats the point of having asked for a
  second opinion at all. (This does not apply to the self-review case above, where there is no
  second party to escalate to — that is precisely why self-review leans on a written, methodical
  checklist instead.)

## Integration with the workflow defined in README.md

This file is loaded during Phase 0 plan convergence, during Phase 2 review code before git commit,
and during Phase 3 draft changelog as final review gate before git commit, per README cumulative
load order. It is **not** loaded during Phase 1 draft code hot path, because Phase 1 focuses on
writing code to core style rules not on reviewing what was written.

* **Phase 0 planning uses peer-review.md before any code exists.** Per [planning.md](./planning.md) §6, run the same two questions against the plan document instead of a diff, iterating until convergence (or the iteration cap) before presenting the plan to the human. No exemplars.md or changelog-style.md involved yet — there is no code or commit message draft to calibrate voice against at this point.
* **Phase 1 draft code always hot set** remains: kernel-style.md entry point, kernel-readability-principles.md composite principles, llm-tells-checklist.md final-pass checklist. No peer-review.md loaded here — saves tokens during most frequent draft iterations.
* **Phase 2 review adds peer-review.md mandatory** on top of Phase 1 base per cumulative load model. At review gate before git commit, load peer-review.md and run the two-question self-review checklist above against both the code diff and the proposed commit message draft structure, then, if a second reviewer is available, route to them per "Escalating to a second reviewer" above. Compare git diff output against exemplars.md per-subsystem routing table (see exemplars.md introduction) to calibrate voice, then adjust tone and comment density to match chosen developer profile.
* **Phase 3 draft changelog adds changelog-style.md mandatory** on top of Phase 1+2 base, and peer-review.md remains resident through Phase 3 as the final review gate before git commit per cumulative model. Re-run the two-question self-review specifically focused on the commit message draft: (a) what's wrong in this commit message draft per changelog-style rules? (b) is there a materially better way to phrase the subject/body/trailers choice? Route to a second reviewer here too if one is available.

Unload all phase-specific files at task end after git commit with proper trailers per CONTRIBUTING.md §5 commit trailers required.

## When to load

Load during Phase 0 plan convergence, Phase 2 review, and Phase 3 changelog drafting per README load order. See CONTRIBUTING.md for repository contribution mechanics.

---
*Review process specification per README workflow — self-review by a single agent is
the default, mandatory gate; routing to a second reviewer is an optional enhancement layered on top
when available. Loaded mandatory during Phase 0 plan convergence, Phase 2 review, and Phase 3 changelog drafting. For
contribution mechanics see CONTRIBUTING.md.*
