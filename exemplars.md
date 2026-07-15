---
name: exemplars
description: "Per-developer kernel style profiles for 14 respected kernel developers, each derived from their real commits with cited hashes. Reference detail behind kernel-readability-principles.md; load a specific section when you want to emulate a particular developer's strength."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1b03c34b-c035-4437-8752-9061cdcb78a1
---
Per-developer profiles derived from real commits in ~/linux (cited hashes). Synthesis: [kernel-readability-principles](./kernel-readability-principles.md). Primary voice: [kernel-style](./kernel-style.md).
---
# David Hildenbrand kernel style
Subsystem: mm-heavy (rmap, folios, memory hotplug, pfnmap), also s390/KVM, virtio-mem. ~1186 commits 2014-2025.
## Changelog
- Open with the problem/current state in present tense, THEN the fix (e.g. 41cddf83d8b0 "If migration succeeded, we called...").
- For trivial removals, one flat sentence: "It's unused, so let's remove it." (e.g. cba4dbeb7bfc).
- Pivot to the action with a hortative "Let's ..." (~50% of bodies) (e.g. 756d25be457f).
- Tack secondary cleanups under "While at it, ..." rather than hiding them (e.g. 756d25be457f).
- Justify with concrete consequences: enumerate exactly which /proc, cgroup, meminfo fields change and by how much (e.g. 749492229e3b).
- Numbered/bulleted lists for enumerating user classes/implications; prose for reasoning (e.g. 756d25be457f).
- Hedge residual risk honestly with "Note that ..." and "How relevant this is in practice remains to be seen." (e.g. 749492229e3b).
- Paste the full splat verbatim when fixing a bug, then explain below (e.g. 41cddf83d8b0).
- Always cite how the bug was found: "Found by code inspection." / Reported-by + Closes: (e.g. 4a5e85f4eb8f).
- Series cover "Patch series ...", per-patch "This patch (of N):", footnotes "[1]" (e.g. a0ac9b3598fa).
- Tone: precise, conversational, occasionally wry bracketed asides and ":)".
## Comments
- Heavy, high-quality kerneldoc on new helpers: summary, every @param, failure modes, "See <fn>() for details." (e.g. e1e1a3ae7f9f).
- Inline comments explain WHY/contract, never restate (e.g. 003fde4492c8).
- Document imprecision explicitly so callers trust the result (e.g. 003fde4492c8).
## Code structure
- Extract a well-named helper as a prep patch before the behavior change (e.g. 07b0303540e1).
- Names encode the semantic guarantee (folio_maybe_mapped_shared) (e.g. 003fde4492c8).
- Mechanical conversions split one-change-per-commit (e.g. 003fde/e1e1a3 series).
Steal this: justify every claim with the exact observable fallout — name the precise /proc, cgroup, meminfo fields that move and which direction, paste the splat, say how the bug was found.
---
# Thomas Gleixner kernel style
## Changelog — open with the concrete symptom, end with the cure.
- Open by naming WHO reported it and WHAT breaks, plain past tense (e.g. 76031d9536a0, c1ab449df871).
- Structure as a story: symptom → mechanism → root cause → fix, each its own paragraph (e.g. da791a667536, 8b68e978718f).
- Signal the fix with imperative verb-first, almost always "Cure this by...", "Fix it up.", "Cleanup the mess." (e.g. 31acbfd84448, 76031d9536a0).
- Prefer prose; numbered list ONLY for genuinely distinct issues: "There are two issues: 1)... 2)..." mirrored in the fix (e.g. 8b68e978718f).
- Quantify with real numbers from the failure (e.g. 76031d9536a0).
- For races, draw a two-column CPU0/CPU1 ASCII ladder (e.g. da791a667536).
- Always cite the offending commit with Fixes: and the short reason inline (e.g. e716efde7526).
- Pure refactors: state intent + "No functional change intended." (e.g. b66d28142dc4).
- Dry, precise, self-deprecating about own bugs ("Undo tglxs brainfart") (e.g. b9d9d6911bd5).
## Comments — why, never what; at the decision point.
- Explain the reasoning and invariant, not mechanics (e.g. 76031d9536a0).
- Block immediately above the surprising branch, @param-referencing prose (e.g. 8b68e978718f).
- Update the comment when logic changes (e.g. 76031d9536a0).
## Code structure
- Replace goto error ladders with direct early `return -ERR;` (e.g. b66d28142dc4).
- When every caller passes `current`, drop the param, fetch inside (e.g. 8b68e978718f).
- WARN_ON_ONCE + graceful recovery for "can't happen" states (e.g. 8b68e978718f).
- Naming verb_object, unabbreviated.
Steal this: write the changelog as a causal narrative — name the reporter, walk symptom→mechanism→root-cause with real numbers or an ASCII race ladder, then "Cure this by...".
---
# Johannes Weiner kernel style
- Open by stating the mechanism/problem, not the fix; describe how the code behaves today first (e.g. c2f6ea38fc1b, e3aa7df331bc).
- Flowing prose paragraphs, bullets only for parallel cases (e.g. e3aa7df331bc).
- Long fixes as a narrative arc: symptom → root-cause investigation → why it regressed now → fix; literally asks "why is this failing now?" (e.g. f53af4285d77, 63fd327016fd).
- Justify with real measured data pasted inline — perf counters, bpftrace tallies, before/after tables (e.g. 17edeb5d3f76, e3aa7df331bc).
- Name the exact culprit commit in prose + matching Fixes: (e.g. 90abee6d7895).
- State the action as a final imperative paragraph naming the function/rename (e.g. c2f6ea38fc1b).
- Pre-empt the skeptic honestly: call out remaining weaknesses ("the keen reader will notice the baseline rate is much smaller") (e.g. e3aa7df331bc, f53af4285d77).
- One-line cleanup: 1-2 sentences on why it's now safe, not what the diff shows (e.g. c7c3dec1c9db).
- Series: lead with "Patch series" summary + aggregate numbers, then "This patch (of N):" (e.g. 17edeb5d3f76).
- Fold review changes as bracketed [hannes@...: ...] crediting the suggester (e.g. 90abee6d7895).
- Comments explain why, esp. locking/racing invariants, full sentences (e.g. 51b8c1fe250d); update header comment in the same diff (e.g. c2f6ea38fc1b).
- Decompose: each decision its own named helper, replace goto labels with early-return helpers + a got_one: tail (e.g. c2f6ea38fc1b).
Steal this: lead with how the code behaves today, prove the problem and fix with pasted real measurements, and disarm the skeptic by naming the fix's own remaining weaknesses.
---
# Breno Leitao kernel style
Changelogs read like incident write-ups: symptom, root cause, fix.
- Open with the concrete symptom/one-line bug, no preamble (e.g. 6552fca6143f, 06717a7b6c86).
- Prose over bullets; numbered lists for sequences to trace in order (refcount race, deadlock chains) (e.g. a4da447a2efb).
- Paste real evidence verbatim — KASAN splat, stack, `time` output — then explain (e.g. 94da84410298, 62adf8c290f2).
- Quantify the win ("13.195s" → "1.789s", "10x") (e.g. 62adf8c290f2).
- Fix as its own short imperative paragraph ("Fix this by moving...") (e.g. 94da84410298).
- Justify why this approach over alternatives, first person, honest doubt ("I _think_...") (e.g. c0739ee5037a).
- Pre-empt the reviewer: call out a TOCTOU/race yourself, argue it's harmless (e.g. c0739ee5037a).
- Refactors labeled plainly + "No functional change." + why now (e.g. 4b52cdfcce21).
- Always Fixes: + reproducer link; Cc: stable with reasoning (e.g. 94da84410298).
- Comments sparse, why-only, where a reader would misread the invariant (e.g. a4da447a2efb).
- Extract cohesive helpers (push_udp/push_ipv4/push_ipv6), one protocol layer each; tiny no-functional-change steps before the behavioral patch (e.g. cacfb1f4e9f6).
Steal this: forensic narrative — paste the splat/numbers, walk the failure step by step, name the alternatives you rejected.
---
# Usama Arif kernel style
(Large sample ~200 commits across mm/THP/hugetlb/zswap/filemap.)
- Open with the problem/mechanism in present tense, not "This patch" (e.g. a3be0819bde7, e474218a75ac).
- Fixes lead with the exact failure mode + trigger, then a one-line imperative fix (e.g. 5a3acef3ccb8).
- Prose; bullets only for parallel cases (e.g. a3be0819bde7).
- Trace the full causal chain before the fix so the reader sees why (e.g. a3be0819bde7).
- Justify with concrete evidence: shell repro, profiling, numeric thresholds (e.g. e474218a75ac).
- Name the design lineage ("inspired from deferred_split_shrinker") (e.g. af667102c81e).
- State scope limits up front (e.g. 226e99d18455).
- Comments sparse, strictly why; rewrite a comment the change invalidates in the same diff (e.g. a3be0819bde7).
- Extract duplicated inline logic into one static-inline helper, convert every call site in the same commit (e.g. 05b7dcf221c9); thread error returns through whole chains (e.g. c5106d76977b).
- Names read as English: probationary_split_queue, force_thp_readahead.
Steal this: before writing the fix sentence, write the causal chain that makes the fix obviously correct — trigger, each broken assumption, consequence, in order.
---
# David Woodhouse kernel style
Narrative debugging changelogs as detective stories.
- Open by stating the buggy behavior plainly, present tense, no preamble (e.g. cae49ede00ec).
- Tell the failure as a causal chain — what calls what until it breaks (e.g. 7725834e5965).
- Give forensic detail: name the offending commit, the year, the BIOS/hardware, even a ticket URL (e.g. 2bba66d6ae0f, 3a03456dc34f).
- State why the fix is correct and bound its blast radius ("relatively harmless; led to a leak but no other ill-effects") (e.g. 6491d4d02893).
- Prose; lists only for enumerating cases.
- Justify tradeoffs from the consumer's side (e.g. ecf6dc026b8e).
- Dry, wry voice aimed at humans, including WARN strings ("Your BIOS is broken;" + vendor/version) (e.g. 39035f9c0969).
- Fixes: with subject + Cc: stable when warranted.
- Comments: why and contract; upgrade a one-liner into a block once the subtlety grows (e.g. f18a02b45805).
- Move work past the cheap early-exit guard (run the bail-out before allocation) (e.g. 7725834e5965); add defensive checks against hostile/broken inputs at entry (e.g. 39035f9c0969).
Steal this: write the changelog as the bug's biography — trace the exact call sequence that breaks, name the commit/year/hardware that caused it, say in plain prose why the fix is correct and what it deliberately doesn't do.
---
# Joerg Roedel kernel style
(iommu/amd, vt-d, x86/sev, KVM/SVM; ~1614 commits.)
- Open with one declarative present-tense sentence stating the action (e.g. ed96f228ba97).
- Subject `subsystem/area: Imperative summary`, capitalized verb, no period (e.g. 94441c3bd992).
- Always answer why: state the bug's consequence/goal before the fix, often cause→effect (e.g. 9d2c7203ffdb, fef81c862628).
- Short plain-prose paragraphs over bullets (e.g. be1a5408868a).
- Compile fixes: paste the exact compiler error, then root cause, then the fix (e.g. be280ea763f7).
- Quote referenced commits inline as `hash ("subject")` (e.g. a33bf8d8ce7e).
- Calm, factual, blame-free even for security leaks (e.g. fef81c862628).
- Fixes: rigorously; credit Suggested-by/Reported-by.
- Comments: moderate, purposeful — every non-obvious function states when it runs and what invariant it protects; explain execution context (NMI/IST/noinstr) (e.g. be1a5408868a).
- One commit, one change; extract `__name()` helper in its own patch (e.g. 237b6f332913); front-load validation then goto out_free_* unwinding.
Steal this: state the consequence before the fix — what breaks and why it matters, then the one-line remedy.
---
# Dan Williams kernel style
Each changelog is a self-contained case file.
- Open with the concrete trigger: paste the command/config/reproducer, indented (e.g. 41fce90f2633).
- Paste the real failure: full splat with call trace, then annotate inline with numbered markers 1) 2) 3) the prose refers to (e.g. 101c268bd2f3).
- State the fix as a reasoned decision: "The fix here is to recognize that..." (e.g. 101c268bd2f3).
- Justify why the naive approach fails before giving yours (e.g. ae86cbfef381).
- Prose; `Details:` header to separate summary from deep mechanism walk (e.g. 53989fad1286).
- Spell out collateral choices + safety argument (downgrade to warning, why crashing is acceptable) (e.g. 101c268bd2f3).
- Subject `subsys/component: imperative`, lowercase (e.g. 6f5c4eca48ff).
- Disciplined trailers: Fixes: with full subject, Cc: stable, Link: keyed [1].
- Name a stop-gap as a stop-gap so future readers know it's intentional debt (e.g. ae86cbfef381).
- Comments sparse, why-not-what; replace now-wrong comments in the same hunk; full kerneldoc on exported helpers (e.g. 2aeaf663b85e, 101c268bd2f3).
- lockdep_assert_held + caller-side guard() over re-acquiring in a leaf; small named predicates/resets for state lifecycle (e.g. 6f5c4eca48ff, 53989fad1286).
Steal this: changelog as standalone forensic report — reproducer + raw splat annotated 1)2)3) + fix as a reasoned decision — so a future reader diagnoses and trusts the fix without the thread or diff.
---
# Peter Zijlstra kernel style
- Open with the concrete symptom/offending behavior in one plain sentence (e.g. a551844e345b, 2a77e4be12cb).
- Root cause as a causal chain: who did what, what state results, why it breaks (e.g. 45178ac0cea8).
- Quote the prior commit you're correcting inline before your fix (e.g. 1f676247f36a).
- Justify with mechanism not authority (explain why the ordering/barrier suffices) (e.g. c7f2e3cd6c1f).
- Blunt, opinionated framing about the code ("People seem to delight in writing wrong and broken mwait idle routines; collapse the lot.") (e.g. 16824255394f).
- Reason adversarially: name the dangerous converse case and argue it cannot happen (e.g. fbeb558b0dd0).
- Short declarative sentences, one idea per blank-line-separated paragraph.
- Fixes: + precise Reported-by/Debugged-by; carries patches with [Name: ...] in-body notes.
- Comments: the why/invariant, never the obvious what (e.g. a551844e345b).
- ASCII tables for concurrency: two CPU columns, ordered ops, labeled barriers, explicit "X pairs with Y"; tag each barrier with its partner inline (e.g. c7f2e3cd6c1f, 1f676247f36a).
- Factor recurring idioms into tiny static inlines (try_get_desc/put_desc); single labeled exit when cleanup added; thread state through signatures, not globals (e.g. 1f676247f36a, 894d1b3db41c).
Steal this: the two-column ASCII concurrency table with explicitly paired, partner-tagged barriers — makes an unreviewable memory-ordering claim auditable at a glance.
---
# Ingo Molnar kernel style
## Changelog
- Open with action/state in present tense; for cleanups state the no-op contract up front: "No change in functionality:" then a bulleted list (e.g. 2b4d5b2582de).
- Cleanups: enumerate every change as parallel lowercase dash-prefixed bullets, one concern per line (e.g. 127f6bf16188).
- Behavioral changes: flowing short paragraphs justifying WHY before HOW (e.g. 09348d75a6ce).
- Embed a small literal before/after hunk or sample output when illustrative (e.g. 09348d75a6ce).
- Reverts: name the reverted SHA1 + subject, why, point to the better fix by SHA1 (e.g. c1ad41f1f727).
- Defer follow-on work with a parenthetical "(Addressed in a separate patch.)" (e.g. 5a505085f043).
- Calm, factual, lightly opinionated; dry asides without losing rigor.
## Comments
- Treat comments as prose to copy-edit: fix typos/grammar/punctuation (e.g. 40eb0cb4939e).
- Explain WHY and tradeoffs ("IRET-to-self is nice because... The only downsides are...").
- Hoist a whole-function caveat to the function header instead of one branch.
## Code structure
- Vertically align related definitions into columns (e.g. 2b4d5b2582de).
- Simplify expressions ((&p->se)->cfs_rq → p->se.cfs_rq); split fat headers; never mix a whitespace sweep with a logic change.
Steal this: land the functional change and a separate "No change in functionality:" cleanup that realigns and copy-edits the surrounding code/comments.
---
# Mel Gorman kernel style
Subject: lowercase `subsystem[, subsystem]:` then a precise imperative naming the mechanism, not the symptom (e.g. e1a556374abc).
## Changelog
- Open by stating current behavior and why it's wrong/costly before proposing anything (e.g. 8d58802fc9de).
- Flowing prose, one idea per paragraph (problem → mechanism → consequence) (e.g. bbbecb35a41c).
- "This patch ..." present tense, mechanism step by step (e.g. 479f854a207c).
- Justify with measured data: raw benchmark tables, before/after columns, (%) deltas, significant ones marked *...* (e.g. d097a6f63522).
- Report multiple dimensions — wall time, User/System/Elapsed, then counters (NUMA faults, pages migrated) (e.g. 09a913a7a947).
- Candid about regressions and limits in the same breath ("main weakness is...", "I cannot reproduce this myself") (e.g. 8d58802fc9de).
- Bug fixes: reconstruct the race as numbered/ASCII state, quote the reporter, Fixes:/Cc: stable (e.g. 3d36424b3b58).
- Series: "Patch series" blurb then "This patch (of N):" (e.g. bbbecb35a41c); inline the shell reproducer (e.g. a8bbf72ab9b3).
- Comments sparse, why-not-what (ordering rationale) (e.g. d34c5fa06fad); block comments for subtle invariants.
- Decompose a giant hot function into named fast/slow static-inline helpers, rare path `unlikely`, note the text-size tradeoff (e.g. 11e33f6a55ed); predicate/action helper names.
Steal this: make the changelog prove itself — current-behavior-then-why-wrong, then a real before/after benchmark table with %-deltas and the CPU/counter breakdown that explains the cause; name your own regressions first.
---
# Vlastimil Babka kernel style
- Open with the present-tense status quo or the bug before any fix (e.g. 284f17ac13fe, 700d2e9a36b9).
- Bug fixes: name+quote the reporter, reproduce as a numbered cause-and-effect chain ("1... 2... 6. goto 2. indefinite stall.") (e.g. 803de9000f33).
- Separate diagnosis from remedy with an explicit pivot — "To fix this, introduce..." / "Therefore, simplify..." (e.g. 803de9000f33).
- Justify trade-offs with the alternative you rejected and why ("A robust solution would be to refactor... However to fix with minimized risk and easier backports, this patch only...") (e.g. fc0c8f9089c2).
- Enumerate consequences as a bulleted list — reasons or "resulting user visible changes", one effect per bullet (e.g. 700d2e9a36b9).
- Flag incidental tidy-ups: "While at it, flip (and document)..." (e.g. 284f17ac13fe).
- State "Otherwise this is not a functional change" / "no measurable gains" when true (e.g. 90f055df1121).
- Back claims with numbers: bloat-o-meter tables, "14% speedup for munlocking a 56GB area" (e.g. 284f17ac13fe); walk a worked example with before/after ranges (e.g. 5886fc82b6e3); embed the minimal reproducer C program (e.g. fc0c8f9089c2).
- Even one-line removals get a "what is now dead and why it's safe" log (e.g. c9929f0e344a).
- Comments: why + warn, not what; full kerneldoc with Context:/Return: spelling out the danger and safer alternative (e.g. 284f17ac13fe, cfb837e84331).
- Decompose by use case not flags (split into a clean path + a _bulk variant); rename for accuracy and say why; drop params/dead locals once derivable; land big reworks as a dozen+ small bisectable steps.
Steal this: present-tense status quo → numbered failure chain → explicit "To fix this / Therefore" pivot; always name what you didn't do and why.
---
# Michal Hocko kernel style
- Open with the problem before the fix — a concrete user-visible symptom or bug report, often citing the introducing commit by hash+subject (e.g. 9a5b183941b5). Reverts: "This reverts commit <hash>." then concede what was good before why it must go (e.g. 55ab834a86a9).
- Flowing prose, almost never bullets: symptom/context → mechanism → "This patch takes a different approach..." / "Fix the issue by..." (e.g. 09f49dca570a).
- Argue alternatives explicitly: name the obvious fix, explain why he rejected it ("That is unfortunately adding a branch into allocator hot path") (e.g. 09f49dca570a).
- Walk the failure naming actors ("Consider a process (call it A)...") + a real reproducer (cgroup/shell sequence) (e.g. 79dfdaccd1d5).
- Honesty markers: flags his own past misses ("I have completely missed..."), admits incomplete understanding ("still not fully understood but let's...") (e.g. e9c3cda4d86e, a75ffa26122b).
- Dense reference apparatus: numbered [1][2][3] lkml links tied to claims, Fixes:, attribution.
- First person, collegial ("I have tested with 16 CPUs", "I would recommend backporting"); "Let's" for cleanup intent; cites org-level pressure ("We (SUSE) have had several bug reports").
- Even trivial patches get a real one-line justification.
- Comments why-not-what at the decision point; explain semantic constraints/dangers ("Higher order nofail allocations are really expensive and potentially dangerous"); terse, lowercase-casual, readable over polished.
- Minimal surgical diffs; intent-named locals (bool nofail, gfp_t alloc_gfp); named predicates over open-coded bit tests (!gfpflags_allow_blocking(gfp)); rename for symmetry.
Steal this: make the changelog argue the change — open with the symptom, name the obvious fix you rejected and why, reason about consequences over asserting correctness, be honest about what you got wrong or still don't understand.
---
# Shakeel Butt kernel style
- Open with current behavior in present tense ("At the moment, the kernel..."), then problem, then fix; never "This patch" (e.g. f735eebe55f8).
- State the fix as a short imperative, often "Let's": "Let's fix it.", "Let's remove them." (e.g. 462966dc7d70).
- Flowing prose; bullets only for design choices or distinct trigger scenarios (e.g. f735eebe55f8).
- Justify with production reality: name the environment and symptom ("In META's fleet, we observed...") (e.g. e82916895e88).
- Back perf claims with a reproducible benchmark: exact commands + results table with percentages (e.g. f735eebe55f8, 2fba5961c64c).
- Explain root cause mechanically before fixing — trace the exact refcount/pointer (e.g. cefc7ef3c87d).
- Fixes: with summary; reference regression and reverting commits inline by hash+subject.
- Pose and answer the reader's likely objection in the changelog (e.g. cefc7ef3c87d); quote a maintainer verbatim under a labeled block when their reasoning matters (e.g. c8e6002bd611).
- Record fixups transparently as bracketed [shakeel.butt@...: ...] with Link.
- Comments sparse, strictly why (a race, cacheline constraint, arch limit); encode invariants + BUILD_BUG_ON pairs; rewrite stale kerneldoc on behavior change (e.g. f735eebe55f8, 2fba5961c64c).
- Refactor toward fewer args/inlined helpers; `__` prefix signals "not re-entrant/irq-safe"; replace a global lock with a per-object lock when the global wasn't protecting shared data; many small single-purpose commits under a titled series.
- Plainspoken, self-deprecating ("a simple (and dumb)" approach that beat the clever one by 1-3%).
Steal this: lead every changelog with the measured production symptom and a reproducible benchmark table, so reviewers feel the pain and trust the win before reading a single line of diff.
