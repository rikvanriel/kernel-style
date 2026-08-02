# changelog-style rationale — per-rule history and provenance

This file is Tier 3 rationale for rules whose canonical text lives in `kernel-style.md` §0 and `changelog-style.md` §1-§3. Each rule has stable ID matching hot files per CONTRIBUTING §9, so CI can check for orphan IDs.

Rationale is public-audience: Message-IDs, public reviewer names, commit hashes, alternative phrasings considered/rejected. No internal identifiers.

## R0 — Factual integrity (canonical: kernel-style.md §0)

- <!-- R0-1 --> Never invent — derived from maintainer edits of AI drafts in 2026-07 where numbers and hashes were hallucinated. Real examples: fabricated benchmark deltas in get_user_page_vma draft, invented Fixes: hashes not in `git log`. Enforcement: `git show <hash>`, paste verbatim.

- <!-- R0-2 --> If you don't know, TODO — pattern from Breno Leitao style: honest doubt "I _think_..." preferred over plausible fill. Trust breach vs recoverable gap.

- <!-- R0-3 --> Verify every claim against diff — standard kernel practice, but LLMs skip. Derived from changelog-style.md verification gate. See also `scripts/lint-changelog.py` checks scope.

- <!-- R0-4 --> Cover letter is claim against every patch — from real bug 2026-08-01 where gup cover letter had 2721/1198/2.3x vs patch actual 2801/1188/2.4x (stale after rebase). Found by hand, missed by old `verify-cover-letter.py` which only checked Before:/After: shape presence, not number diffing. Fixed to diff values per unit. See also patch-series.md §5.

- <!-- R0-5 --> Paste raw artifact verbatim — Dan Williams `101c268bd2f3` annotated splat with 1)2)3) markers; Mel Gorman `09a913a7a947` benchmark table; Breno Leitao `62adf8c290f2` time before/after. Rule: paste literal block then explain.

- <!-- R0-6 --> Treat unverified prose as bug — enforced via `/kreview` gate, checkpatch.pl, lint-changelog.py.

- <!-- R0-7 --> Carried-forward text is re-asserted — from forward-porting a long mm series onto a newer base in 2026-08. Two independent failures, both inherited rather than invented: a changelog kept "zero WARN/BUG" stress figures and a "~14 hours bare-metal" claim measured on the *old* base, and a bugfix changelog described a `list_del` corruption splat that the author had never reproduced, both restated verbatim under the porting author's name. The 14-hour run had in fact missed a preempt-count underflow later found in that same code, so the retained claim was not merely stale but misleading. R0-1 ("never invent") did not fire because nothing was invented — the gap was that re-asserting someone else's unverified claim is indistinguishable, to a reader, from making it yourself. Enforcement: treat every retained sentence in a rewritten changelog as newly written for R0-8 purposes.

- <!-- R0-9 --> An explanation is a claim — added after R0-1/R0-5/R0-7/R0-8 all failed to catch two wrong sentences in one small mm changelog in 2026-08. First: "that zone id is *simply* the last zone processed in memmap_init()'s iteration", true of one of the two call sites and false of the other, which passes the zone whose memory follows the hole; the sentence also framed long-documented deliberate behaviour as an oversight. Second: "e.g. a hole between DMA32 and Normal", describing a gap between zones, which cannot exist — zones tile PFN space contiguously (checkable in `/proc/zoneinfo`: each zone's start_pfn equals the previous zone's start_pfn plus its spanned pages). Neither is a number, hash, splat or benchmark, so every existing factual-integrity rule was shaped for the wrong target. Both were confident prose *about* code, written from the author's model of it rather than read off it. Detection signal: names code AND states it absolutely. Measured 30 of 293 sentences (10%) over a 40-patch series, roughly one per changelog, and flags both failures above. Caveat for future editors: that heuristic was tuned knowing the two failures it had to catch, so the rate is optimistic until validated on an unrelated series. The lint cannot judge truth; its value is forcing enumeration, which is the step that was skipped — the same reason R0-8's claims table worked.

- <!-- R0-8 --> Name the artifact per claim — companion mechanical step for R0-1/R0-3/R0-7. Same 2026-08 series: `checkpatch.pl` reported "no obvious style problems and is ready for submission" on a patch whose changelog asserted an unobserved splat, so the existing tool gate gave false assurance. Listing each empirical claim beside the artifact that produced it (log path, command output, `git show` hash) is checkable by a reviewer and by the author, where "did I verify this?" recalled from memory is not.

- <!-- R0-3-CH --> Changelog-specific verification of scope/files/symptom/cause/fix/perf/Fixes/Link/Reported-by — subset of R0-3 focused on changelog.

- <!-- R0-5-CH --> Artifact verbatim checks: git show exists, lore/syzbot link resolves.

- <!-- R0-6-CH --> Pre-write gate tools: /kreview setup (review-prompts.md), checkpatch.pl, git log, benchmark, lint-changelog.py.

## CL-10 — Subject line

- <!-- CL-10 --> `subsystem: lowercase imperative` — from submitting-patches.rst. Examples `1aa43598c03b` "mm: remove unnecessary calls...", `434247637c66` "bpf: use kvzmalloc...". x86/tip exception `209954cbc7d0` capitalizes first word — match subsystem's existing style, not fixed rule. Mechanically checkable: no trailing period.

- <!-- CL-10b --> Check git history prevailing prefix — `kernel/trace/fprobe.c` uses `tracing/fprobe:` not `trace/fprobe:` (historical precedent). Run `git log --oneline -- <path>`.

- <!-- CL-10c --> Comma-joined multi-subsystem prefixes `mm,vmscan:` — common habit e.g. `8ebe0a5eaaeb`, `da27f796a832`, no space after commas.

## CL-11 — Fixes + Cc: stable pairing

- <!-- CL-11 --> If Fixes: footer, add Cc: stable@vger.kernel.org — Fixes: marks bug worth backporting. Checkable: Fixes present but no Cc stable is red flag. Enforced by `scripts/lint-changelog.py`.

## CL-12 — Paragraph caps

- <!-- CL-12 --> 90% ≤50w, max 70 never beyond — checkable backstop for "one idea per paragraph" from kernel-readability-principles. Applies to changelogs and code comments. Enforced by lint-changelog.py. Cutting >70 signals to split or compress, not pad to 70. Merging two related clauses under cap beats splitting for "one idea per paragraph" cost.

## CL-14 — Audience / internal identifiers

- <!-- CL-14 --> No internal identifiers — agent/bot nicknames, private syzkaller bucket hashes without public syzbot link, internal branch names, private hostnames, build IDs, vendor ticket IDs, Phabricator/Jira IDs. Upstream reviewers lack context; reads as noise. Use generic "syzkaller triggers", "KASAN reports", "tested on v6.15-rc1". Provenance in trailers (Reported-by, Link, Assisted-by) not prose. Extends to code comments: no dashboards in `/* */`. Public LKML reviewer names (Hildenbrand, Gleixner, etc.) are fine — public participants with lore archives. Internal-only attributions belong in trailers or private notes only. See also CONTRIBUTING §4 external-facing discipline, flock-norms #10. Example cut: "analyzed by internal-agent-1" → "syzkaller triggers..".

- <!-- CL-14-CH --> Audience rule changelog-specific — same as CL-14 but emphasizes changelog body must make sense to external reviewer with zero internal context.

- <!-- CC-14 --> Same rule for code comments — even less context allowed in source than changelog.

## CL-20..28 — Changelog body structure

- <!-- CL-20 --> Open with problem in present tense — universal from 14 developers. Never "This patch". Example `e9868505987a`. Validated against llm-tells checklist.

- <!-- CL-21 --> Keep verb tense consistent — present throughout. Mixing tenses makes reviewer unsure whether current behavior or history. Validation 2026-07-01 David Hildenbrand review.

- <!-- CL-22 --> Lead bugfix with real-world symptom — who triggers, what breaks, then internals. Example `2820b0f09be9` opens with jemalloc/tcalloc → SIGBUS, not "zap_page_range_single fails to take i_mmap_rwsem".

- <!-- CL-23 --> For race, draw CPU 1 / CPU 2 ASCII ladder — common device, e.g. `2820b0f09be9`. Partner-tagged barriers for Zijlstra.

- <!-- CL-24 --> Match changelog length to change size — simple improvement ~3 paragraphs (efa7df3e3bb5), race earns more.

- <!-- CL-25 --> Structure problem→cause→fix→effect, 3-6 paragraphs 2-4 sentences each — typical shape `5cbcb62dddf5`.

- <!-- CL-26 --> Explain WHY with data — before/after tables, percentages. Examples `e1e4cfd01a6e` 1560→4720 MB/s, `209954cbc7d0` 4.5s→4.2s, `da27f796a832` 6 min→1 sec.

- <!-- CL-27 --> Paste raw artifact verbatim — KASAN splat, benchmark table indented as literal block. Composite: Dan Williams `101c268bd2f3` annotated splat.

- <!-- CL-28 --> If bug produces kernel message, MUST include verbatim — KASAN/UBSAN/WARNING/oops/Call Trace indented literal block, not paraphrase. Trim noise but keep signature, Call Trace, Allocated-by/Freed-by for UAF. Never fabricate matching splat if you captured different signature (R0).

- Also see CL-10..CL-14 above for trailers, caps, audience.

## CC-10..14 / CS-10..11 — Code

- <!-- CC-10 --> Comment WHY not WHAT — hardware, locking, ordering, lifetime. Universal.

- <!-- CC-11 --> Density low purposeful 1-2 lines typical max 2-8 block, same 50w cap per CL-12.

- <!-- CS-10 --> Split out named helper when predicate multi-branch/reused — e.g. should_flush_tlb(). Decompose.

- <!-- CS-11 --> Cap function length 80% ≤20 lines hard max 40 — signal to extract helper.

## CL-13 — Contrast / LLM tells (summary pointer)

- <!-- CL-13 --> Full list in llm-tells-checklist.md, summary in changelog-style.md §3. Core bans: redundant comments, hedging filler "Note that", marketing adjectives robust/powerful/seamless, over-bulleting, em-dash, recap, mixed tense, vague justification, double negatives, templated Pros/Cons, ornate verbs, inferable boilerplate "No functional change" on obvious rename, internal identifiers. Enforced by lint-changelog.py heuristic + /kslop automated (higher confidence bar, cluster requirement, hard cap 3 findings).

## Verification workflow

- Phase 3 final gate: `scripts/checkpatch.pl --strict`, `scripts/lint-changelog.py <file>` or `git log -1 --pretty=%B | lint-changelog.py --stdin`, `scripts/verify-cover-letter.py --cover cover.txt --patches patch*.patch` for multi (with real number diffing, not just shape presence — fixed per feedback #3). Then peer-review.md two questions as self-review, then commit with trailers per CONTRIBUTING §5.

## Cross-links

- Hot: kernel-style.md §0 R0-1..R0-6 canonical, §1 CL-10, §2 CC-10, §3 CS-10, §4 CL-13 summary
- This file: per-ID rationale above
- CI: should fail if hot ID no matching rationale entry or vice versa (CONTRIBUTING §9)
