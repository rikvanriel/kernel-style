---
name: kernel-readability-principles
description: "Composite kernel changelog/comment/code readability principles synthesized from 14 respected kernel developers. A companion to kernel-style.md for writing or reviewing kernel code/comments/changelogs; kernel-style is the primary voice, this is the broader \"what good looks like\" calibration."
metadata:
  type: reference
---
# Kernel readability principles (composite)
Synthesized from the commit styles of 14 widely-respected kernel developers (Hildenbrand, Gleixner, Weiner, Leitao, Arif, Woodhouse, Roedel, D. Williams, Zijlstra, Molnar, Gorman, Babka, Hocko, Butt). Per-developer detail with hashes: [exemplars](./exemplars.md). Primary voice for our patches stays [kernel-style](./kernel-style.md); where these 14 agree, treat it as a strong rule.
## Changelog
1. **Open with the problem / current behavior in present tense.** Never "This patch", never the fix first. State what the code does today and why that's wrong, then fix it. (near-universal: Weiner `c2f6ea38fc1b`, Hildenbrand `41cddf83d8b0`, Gorman `8d58802fc9de`, Babka `284f17ac13fe`, Shakeel `f735eebe55f8`, Usama `a3be0819bde7`)
2. **Tell it as a causal narrative: symptom → mechanism → root cause → fix → effect.** Make the reader understand the bug before they see one line of diff. (Gleixner `da791a667536`, Weiner `f53af4285d77`, Usama "teach the bug", Dan "case file", Woodhouse "the bug's biography")
3. **Justify with real, pasted evidence, not adjectives.** The actual oops/splat with call trace, the reproducer command, the before/after benchmark table with deltas — indented as a literal block, then annotated. (Dan annotated splat `101c268bd2f3`, Mel `09a913a7a947`, Shakeel netperf tables, Breno KASAN+`time` `62adf8c290f2`, Hildenbrand names exact /proc & memcg fields that move)
4. **Name the fix in an imperative pivot sentence:** "Cure this by… / Fix it by… / To fix this, … / Let's …". (Gleixner "Cure this by", Babka "To fix this/Therefore", Hildenbrand/Hocko/Shakeel "Let's")
5. **Argue the design: name the obvious/naive alternative and why you rejected it.** (Hocko `09f49dca570a`, Babka `fc0c8f9089c2`, Dan `ae86cbfef381`, Breno `c0739ee5037a`)
6. **Bound the scope honestly.** Say what the patch does NOT do, and name its remaining weaknesses or small regressions before a reviewer does ("the keen reader will notice…", "No functional change intended."). (Weiner `e3aa7df331bc`, Mel, Babka, Usama, Gleixner)
7. **Prose paragraphs by default; bullets only for genuinely parallel enumerations.** (universal)
8. **Cite provenance rigorously:** `Fixes:` with subject, name the offending commit inline, credit Reported-by/Suggested-by by name, `Link:` to lore keyed `[1]`. (universal)
9. **Tone: calm, factual, engineer-to-engineer.** First person ("we"/"I") is natural; dry wit only when it carries information. (Gleixner self-deprecating, Woodhouse wry, Hocko honest, Shakeel "the dumb one was better")
## Comments
10. **Comment the WHY** — invariant, locking, ordering, hardware quirk — never restate the code. Sparse, placed exactly at the surprising branch. (universal: Gleixner, Weiner `51b8c1fe250d`, Mel `d34c5fa06fad`)
11. **Update a stale comment in the same diff that changes behavior.** Comments are code, not decoration. (Weiner `c2f6ea38fc1b`, Dan, Usama, Shakeel)
12. **Reserve full kerneldoc `/**` for genuinely exported APIs;** internal statics get a plain `/*` why-block or nothing. (Hildenbrand, Roedel, Dan — contrast: our SPB code over-kerneldoc'd ~53 statics)
13. **For concurrency, draw a two-column CPU0/CPU1 ASCII ladder, and tag each barrier with the partner it pairs with** (`smp_wmb(); /* B, matches C */`). (Gleixner `da791a667536`, Zijlstra `c7f2e3cd6c1f` — the signature device)
## Code
14. **Decompose into small, intent-named helpers** (predicates `should_x()`, actions `verb_noun()`); flatten goto-ladders into early returns. (universal: Weiner `try_to_steal_block`, Gleixner, Mel `should_alloc_retry`, Hildenbrand)
15. **Rename for accuracy as part of the change, and say why in the log.** (Babka `adj_next`→`adj_start` `1e76454f9361`, Weiner, Hocko)
16. **One logical change per commit;** land big reworks as a sequence of small, individually-bisectable steps; keep mechanical cleanup ("No change in functionality:") separate from logic. (Ingo `2b4d5b2582de`, Babka, Breno)
17. **Minimal surgical diffs:** drop dead params/locals the moment a refactor makes them derivable; no drive-by changes. (Babka `e1f42a577f63`, Breno, Hocko)
## Anti-LLM-tells (none of the 14 do these) — see [llm-tells-checklist](./llm-tells-checklist.md)
- Opening with "This patch …" and skipping the problem; leading with the fix.
- Vague justification ("improves performance") instead of a number, workload, or pasted artifact.
- Marketing adjectives (robust/powerful/seamless/comprehensive/elegant).
- Comments that restate the code; kerneldoc essays on trivial statics.
- Over-bulleting; recap/"In summary" paragraphs; em-dash sprinkling.
- Hiding limitations; templated Pros/Cons scaffolding.
## Signature strength to steal from each
- **Hildenbrand** — justify with the exact observable fallout (which /proc, cgroup, meminfo fields move, in which direction); paste the splat; say how the bug was found.
- **Gleixner** — causal narrative naming the reporter, real numbers or an ASCII race ladder, then "Cure this by…".
- **Weiner** — lead with today's behavior, prove it with pasted measurements, disarm the skeptic by naming the fix's own weaknesses.
- **Leitao** — forensic write-up: paste the splat/numbers, walk the failure step by step, name the alternatives you rejected.
- **Arif** — write the causal chain that makes the fix obviously correct before the fix sentence.
- **Woodhouse** — the bug's biography: exact call sequence, the commit/year/hardware that caused it, and what the fix deliberately doesn't do.
- **Roedel** — state the consequence before the fix; one-line "why it matters" then the one-line remedy.
- **D. Williams** — standalone forensic report: reproducer + raw splat annotated `1) 2) 3)` + fix stated as a reasoned decision ("recognize that…").
- **Zijlstra** — two-column ASCII concurrency table with explicitly paired, partner-tagged barriers.
- **Molnar** — split the logic change from a separate "No change in functionality:" cleanup that realigns and copy-edits.
- **Gorman** — prove it: current-behavior-then-why-wrong, then a real before/after benchmark table with %-deltas and the counter breakdown that explains the cause.
- **Babka** — present-tense status quo → numbered failure chain → explicit "To fix this / Therefore" pivot; always name what you didn't do and why.
- **Hocko** — make the changelog argue: name the obvious fix you rejected and why; reason about consequences; be honest about what you got wrong.
- **Butt** — lead with the measured production symptom and a reproducible benchmark table so reviewers feel the pain before the diff.
