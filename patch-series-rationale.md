---
name: patch-series-rationale
description: Provenance and reasoning behind patch-series.md rules. Cold file; not loaded during the drafting workflow.
metadata:
  type: rationale
---
# patch-series rationale

Provenance for rules in [patch-series.md](./patch-series.md). Cold file: loaded when editing a rule,
not when following one.

## Series-level function growth

Added 2026-08 after forward-porting a 40-patch mm series onto a newer base.

`__rmqueue_smallest` went from 24 lines upstream to 546 at the end of the series, grown by seven
patches: +165, +42, +32, +24, +156, +33, +70. No single patch is obviously at fault, and each
addition is a coherent new allocation pass. Reviewing any one patch in isolation shows a function
that was already long before that patch touched it, so nobody is prompted to act, and the per-patch
40-line check never fires on the total.

Two other functions in the same series show the pattern: `rmqueue_bulk` 36 -> 265, and
`resize_zone_gigablocks` created at 222 across six patches.

Detection threshold. Flagging every function over the cap at series end gave 38 hits on this series,
including ones already long upstream that the series barely touched (`show_free_areas` +15 on 224).
Requiring that the series itself added more than a whole permitted function's worth cut that to 16,
all genuine. The signal is series contribution, not final size.

Why the rule says extract in the patch that adds the pass. Retrofitting was attempted on this series
and abandoned partway: restructuring the function in the patch that first grew it forced a full
re-derivation of every later patch that touched it, and produced two resolution errors within the
first four conflicts (a dropped `static __always_inline` on a hot-path function, and a regex
resolution that silently left stray code from the incoming side). Both were caught by the compiler,
which is luck rather than process. Extracting at the point of addition costs almost nothing.

Parser note. `scripts/series-function-growth.py` brace-matches function bodies and reads forward to
the first `;` or `{` to tell a declaration from a definition. An earlier version decided from the
first line alone, which mis-parses a prototype whose `;` sits on a continuation line: it then scans
for the next `}` and silently swallows the function after it. That version reported
`__rmqueue_smallest` as untouched by patches 15 through 26. Verified against hand measurement at
base, p15, p21, p27 and p39 before use.
