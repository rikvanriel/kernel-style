---
name: llm-tells-checklist
description: "Final-pass checklist to strip LLM tells from kernel code, comments, and changelogs before finishing. Run it after drafting; it's the negative half of kernel-style.md / kernel-readability-principles.md."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b03c34b-c035-4437-8752-9061cdcb78a1
---
# LLM-tells final pass
Run this over any kernel changelog/comment/code you wrote, before declaring it done. Each line is a "delete or rewrite if present". Derived from what 14 respected kernel devs do and don't do ([kernel-readability-principles](./kernel-readability-principles.md)) and the kernel-style voice ([kernel-style](./kernel-style.md)).
## Verification — never invent facts
Run this FIRST, before style fixes. [added 2026-07-09].
- [ ] Every number, quote, date, performance result, commit hash, or technical claim in the changelog/comment/code has been read from a primary source this session (file, command output, git log, benchmark artifact, brain record) — not from memory, pattern completion, or plausible invention.
- [ ] If you don't know a value, you said so explicitly or marked TODO — you did not fill in a plausible number.
- [ ] Performance before/after tables match actual benchmark output pasted verbatim; no rounded or invented deltas.
- [ ] Commit hashes cited exist in `git log` (check with `git show <hash>` or `git log --oneline --grep`); `Fixes:` tag points to real commit.
- [ ] Links to lore, Phabricator diffs, tasks, SEVs resolve and point to the right artifact.
- [ ] Changelog scope matches actual diff stat — no claims about files not touched, no omitted major changes.
- [ ] When drafting for upstream consumption especially, treat unverified prose as a bug on par with wrong code.
## Changelog
- [ ] Opens with "This patch …" or the fix — rewrite to open with the problem / current behavior in present tense.
- [ ] Bugfix that doesn't lead with the real-world symptom (who hits it, what breaks) — add it; for a race, add an ASCII `CPU 1 / CPU 2` ladder.
- [ ] Vague justification ("improves performance", "more efficient") — replace with a number, a named workload, a pasted splat/repro, or concrete reasoning. Don't invent numbers; if none, say so.
- [ ] Marketing adjectives: robust, powerful, seamless, comprehensive, elegant, gracefully — cut.
- [ ] Hedging filler: "Note that", "Importantly", "It's worth noting", "Keep in mind" — cut, state the fact directly.
- [ ] Recap/"In summary" paragraph at the end — cut; end on the effect or a trailer.
- [ ] Bulleted lists where prose fits — convert to paragraphs; keep bullets only for genuinely parallel items or pasted data.
- [ ] Em-dash sprinkling — prefer periods/parentheses.
- [ ] No `Fixes:`/`Link:`/`Reported-by:` where warranted — add.
- [ ] Doesn't say what the change does NOT do / its limits — add if non-trivial.
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
