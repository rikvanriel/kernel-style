---
name: exemplars-routing
description: Tiny hot routing table extracted from exemplars.md — maps bug class to developer profile to focus on at Phase 2 review gate. Load instead of full exemplars.md to pick profile, then load only that profile on demand.
metadata:
  type: reference
---
# Exemplars routing — which developer profile to focus on

Load this file (not full `exemplars.md`) during Phase 2 review to pick one profile. Then load only that section from `exemplars.md` on demand (or via `scripts/phases.py --phase 2 --bug-class <class>`).

## Routing table

* **syzkaller crash / UAF with KASAN / WARNING / oops with Call Trace** → **Dan Williams** (annotated splat with numbered markers 1) 2) 3)). Also: **Breno Leitao** forensic KASAN walk-through, **David Woodhouse** bug biography with exact call sequence.

* **concurrency / locking / memory ordering race / deadlock / RCU stall** → **Thomas Gleixner** (two-column CPU0/CPU1 ASCII race ladder) or **Peter Zijlstra** (partner-tagged barrier table). Gleixner for race ladder, Zijlstra for barrier pairing — do not conflate.

* **performance numbers / benchmark tables / throughput / latency** → **Mel Gorman** (before/after tables with %-deltas + counter breakdown) or **Shakeel Butt** (production fleet measurement with repro command + table).

* **locking / refcount / lifetime / invariant subtlety in comments** → **David Hildenbrand** (exact observable fallout: which /proc/cgroup/meminfo fields move) + **Joerg Roedel** (consequence-before-fix).

* **arguing design tradeoffs / pre-empting reviewer objections** → **Michal Hocko** (obvious fix rejected + why + honest misses), **Vlastimil Babka** (numbered failure chain + To-fix-Therefore pivot + scope limits), **Johannes Weiner** (disarming skeptic by naming fix's own weaknesses).

* **minimal surgical fix / mechanical cleanup separation** → **Ingo Molnar** (No-change-in-functionality separate cleanup that realigns and copy-edits).

* **Otherwise** → subsystem-closest developer per per-developer subsystem lists in `exemplars.md`, or skim one-line signatures in `kernel-readability-principles.md` § Signature strength.

Token cost: this file ~180 words. Full `exemplars.md` is ~3,685 words — load only after routing.
