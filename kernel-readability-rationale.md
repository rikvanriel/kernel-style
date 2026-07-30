---
name: kernel-readability-rationale
description: "Tier 3 rationale companion to kernel-readability-principles.md. Provenance metadata (Message-IDs, dates, public reviewer names, historical evolution) for principles in the hot file. Load only when modifying a principle, to understand its origin before changing it."
metadata:
  type: reference
---
# Rationale for kernel-readability-principles.md

Not loaded during normal patch drafting or review. See [CONTRIBUTING.md](./CONTRIBUTING.md) for the three-tier architecture this file belongs to.

## Principle 18 — unused parameter as a design smell

Source: David Hildenbrand, reviewing `follow_pte_batch()` in a standalone
`mm/gup` patch derived from an access_remote_vm RFC series (lore
Message-ID `db3d2c65-31f2-4430-bef4-4dae76135eed@kernel.org`, 2026-07-29).
The function took a `struct page *page` parameter it never read. Quote:
"Why is this passed when it's not even used? Maybe it should be used?"
The fix used the unused parameter to drive a precise
`PageAnonExclusive()`-based batch check instead of a blanket
single-page fallback.

Marked experimental (2026-07-29): single review instance, no corpus of
real merged commits checked yet. Reassess 2026-10-29 — either find/confirm
independent instances among the 14 developers' real commits and promote to
a normal cited rule, or fold into existing principle 17 if it turns out to
be the same underlying rule, or drop if it doesn't generalize.

## Principle 19 — compute broad, then narrow the safety check

Same review as principle 18. The original code:
```c
if (!pte_write(pte) && (flags & (FOLL_WRITE | FOLL_PIN)))
	return 1;
```
ran unconditionally for every folio type, but the restriction is only
required for anonymous folios. Hildenbrand's suggested restructuring
computed `folio_pte_batch_flags()` first, then applied the anon-only
`gup_must_unshare()`-safety check afterward, so file-backed folios (which
never needed the restriction) keep the full batch.

Marked experimental (2026-07-29), same status and reassessment date as
principle 18.

## Principle 20 — grep for an existing helper before writing new logic

Same review as principle 18. Hildenbrand pointed at the existing
`page_anon_exclusive_batch()` helper in `mm/mprotect.c` as prior art for
the batch-safety check being written from scratch, noting the existing
helper is "rather ugly" but usable, or suggesting a small local
open-coded loop over `PageAnonExclusive()` instead.

Marked experimental (2026-07-29), same status and reassessment date as
principle 18.
