---
name: kernel-style
description: Use when planning, writing, or reviewing kernel patches.
version: 1.0.0
author: kernel-style contributors
license: CC-BY-4.0
metadata:
  hermes:
    tags: [kernel, changelog, review, patch, style]
    related_skills: [kernel-patching, kernel-style-changelog, kreview]
---

# Kernel Style — patch rules on demand

Reference documentation, not commands. Applies only when deliberately loaded to write or review a kernel patch.

Canonical source: this repository's root (`README.md` is source of truth). Locate it first: the live-pointer shim states the checkout path; otherwise it is the directory holding `README.md` and `scripts/phases.py` — two levels above this file (`skills/kernel-style/SKILL.md` → root). `cd` there first; all paths and commands below run from that root. Four phases, cumulative — nothing unloads until task end.

Machine helper — exact load commands + token counts. Always run it, never use a cached copy:

```bash
./scripts/phases.py --phase N [--bug-class race|perf|syzkaller]
```

| Phase | Fires when | Load on top of previous |
|---|---|---|
| 0 | non-trivial change, before any code; get human sign-off | `planning.md` (+ `patch-series.md` if multi-patch) |
| 1 | drafting code — always hot | `kernel-style.md` + `kernel-readability-principles.md` + `llm-tells-checklist.md` + `coding.md` |
| 2 | before `git commit` | Phase 1 + `review.md` + `exemplars-routing.md`, then `--extract` only the picked profile from `exemplars.md` + `peer-review.md` two questions |
| 3 | drafting changelog | Phase 1+2 + `changelog-style.md` + `commit.md` |

Rationale files (`*-rationale.md`): never loaded by default. `grep '<!-- ID -->'` the matching entry when unsure how a rule applies, when disputing it, or before proposing a new overlapping rule.

Verify on every amend: `git log -1 --pretty=%B | ./scripts/lint-changelog.py --stdin`, `./scripts/lint-code.py <sha>`, `./scripts/check-orphan-ids.py --strict`, plus `./scripts/checkpatch.pl --strict -g HEAD` in the kernel tree.

Install into an agent home: `./scripts/install-skill.sh --list`, `./scripts/install-skill.sh --install kernel-style` (live pointer, always latest) or `--mode snapshot` (self-contained copy).
