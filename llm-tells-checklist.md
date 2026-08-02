---
name: llm-tells-checklist
description: "Final-pass checklist to strip LLM tells from kernel code, comments, and changelogs before finishing. A pass to make after drafting; it's the negative half of kernel-style.md / kernel-readability-principles.md."
metadata:
  type: reference
---
# LLM-tells final pass
A final pass for any kernel changelog/comment/code, made before it is considered done. Each line means "delete or rewrite if present". Derived from what 14 respected kernel devs do and don't do ([kernel-readability-principles](./kernel-readability-principles.md)) and the kernel-style voice ([kernel-style](./kernel-style.md)).

**Scope.** These apply to text your patch adds or changes. Pre-existing prose sitting next to your diff is out of scope — rewriting it is a drive-by cleanup (patch-series.md §1) that inflates a small fix and collides with later patches touching the same lines. Fix it in its own patch.

This checklist is a blunt, self-administered pass over the same category of tell; `/kslop` (from [review-prompts](./review-prompts.md)) runs an automated version with a much higher confidence bar — cluster requirement, compared against neighbouring code, hard cap of 3 findings, phrased as questions rather than flat deletions. Use both: this checklist to fix things yourself before posting, `/kslop` as a second, noise-gated pass.
## Verification — never invent facts
Canonical: kernel-style.md §0 (R0-1..R0-6) — this section is cross-ref checklist only per CONTRIBUTING §2.
This pass comes first, before the style fixes.
- [ ] <!-- R0-1 --> Every number/quote/date/perf result/hash/claim sourced this session (file, git log/show, cmd output, benchmark, crash dump, public tracker, lore) — not memory. See R0-1 canonical.
- [ ] <!-- R0-2 --> If you don't know, TODO — not plausible fill. See R0-2.
- [ ] Performance before/after tables match actual benchmark output pasted verbatim; no rounded/invented deltas.
- [ ] Commit hashes exist in `git log` (`git show <hash>`); `Fixes:` points to real commit.
- [ ] Links to lore.kernel.org/syzbot/public tracker resolve — no private-only URLs.
- [ ] Changelog scope matches diff stat — no claims about untouched files.
- [ ] <!-- R0-4 --> If cover letter present, every number/mechanism claim checked against specific patch's own current changelog/diff — not earlier draft or pre-split version. Re-verify after any patch change. See R0-4.
- [ ] <!-- R0-6 --> Treat unverified prose as bug on par with wrong code. Gate: `scripts/lint-changelog.py`, `/kreview`, `checkpatch.pl`.
## Changelog
- [ ] Opens with "This patch …" or the fix — rewrite to open with the problem / current behavior in present tense.
- [ ] Bugfix that doesn't lead with the real-world symptom (who hits it, what breaks) — add it; for a race, add an ASCII `CPU 1 / CPU 2` ladder.
- [ ] Vague justification ("improves performance", "more efficient") — replace with a number, a named workload, a pasted splat/repro, or concrete reasoning. Don't invent numbers; if none, say so.
- [ ] Marketing adjectives: robust, powerful, seamless, comprehensive, elegant, gracefully — cut.
- [ ] Hedging filler: "Note that", "Importantly", "It's worth noting", "Keep in mind" — cut, state the fact directly.
- [ ] Double negative ("not X, not Y", "doesn't not do Z") — rewrite as the positive condition it actually describes. Applies to comments too.
- [ ] Recap/"In summary" paragraph at the end — cut; end on the effect or a trailer.
- [ ] Bulleted lists where prose fits — convert to paragraphs; keep bullets only for genuinely parallel items or pasted data.
- [ ] Em-dash sprinkling — prefer periods/parentheses.
- [ ] No `Fixes:`/`Link:`/`Reported-by:` where warranted — add.
- [ ] Doesn't say what the change does NOT do / its limits — add if non-trivial.
- [ ] A paragraph restates a code comment added or touched in the same diff, or two adjacent paragraphs describe sequential sub-steps of one change that a connective (since/so/then/--) could join under the paragraph cap — compress; run changelog-style.md's compression pass.
## Comments
- [ ] Comment restates the code ("/* increment counter */") — delete.
- [ ] Kerneldoc `/**` with `@param` on a static internal helper — downgrade to a plain `/*` why-block or delete; reserve `/**` for exported APIs.
- [ ] Multi-paragraph essay / numbered "plan" comment — compress to a 2-8 line why.
- [ ] A comment now contradicted by the code change — rewrite it in the same diff.
- [ ] Genuinely subtle logic (locking, ordering, lifetime, invariant) with NO why-comment — add one.
## Code
- [ ] Function over ~40 lines — see the 40-line rule; extract intent-named helpers.
- [ ] Bare `{ }` scoping blocks — declare at function top.
- [ ] goto-ladder where early returns read better — flatten.
- [ ] Drive-by changes mixed with the logic change — split into a separate commit.
- [ ] Pre-existing code the change has made redundant — a call the new code turns into a no-op, a branch nothing can reach now — remove it, and don't let a comment explain the dead step as if it were required. Check the failure paths, not just the happy one: a call that is unreachable when every preceding step succeeds may be the only thing that runs when one bails out early. Sibling of the "comment now contradicted by the code change" item above.
