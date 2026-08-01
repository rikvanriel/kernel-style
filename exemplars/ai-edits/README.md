# AI edit before/after — real maintainer edits of AI drafts

Mix of externally-verifiable examples (with lore Message-ID / public commit hash) and internal illustrative drafts. Labeled explicitly per CONTRIBUTING §8 — real vs internal.

## Example 1 — verbose why-comment trimmed (Lorenzo review, PG_has_hwpoisoned fix, 2026-07-01)

**Before (AI draft):**
```c
/*
 * We need to check if the page has the hwpoisoned flag set. Note that
 * this is important because if the page is marked as hwpoisoned it
 * means it is already known to be bad and we should not try to use it.
 * Importantly, this is a robust safety check that ensures comprehensive
 * handling of memory errors.
 */
if (TestClearPageHasHwpoisoned(page))
```

**After (upstream):**
```c
/* Avoid using page already known to be bad. */
if (TestClearPageHasHwpoisoned(page))
```

**Why cut:** one-line invariant sufficient, no hedging filler [CL-13], no marketing adjectives, 50-word cap [CL-12], restates code removed.

## Example 2 — "reads oddly" justification cut (get_user_page_vma rename, 2026) — INTERNAL DRAFT, NOT POSTED UPSTREAM, ILLUSTRATIVE ONLY

**Before (AI draft, internal session 2026-07, never posted upstream — illustrative only):**
```
The 'remote' in the name describes the mm, not what the helper does, and
reads oddly next to get_user_pages_remote(). Name it for its action.
```

**After (internal edit, illustrative):**
```
# cut entirely — reason once is enough, don't sell the change
```

**Rule:** changelog-style.md compression pass — "State the reason once; don't sell the change or re-argue it" [CL-26]. Justification already in rename itself, second sentence is meta-commentary failing cut test per peer-review.md. **Provenance:** internal drafting session, no lore Message-ID, not merged — do not cite as external evidence; kept here only to show cut-test pattern.

## Example 3 — "instead of" comparison that shouldn't be in comment (get_user_pages loop, 2026) — INTERNAL DRAFT, NOT POSTED UPSTREAM, ILLUSTRATIVE ONLY

**Before (internal session 2026-07, never posted upstream — illustrative only):**
```c
/* Walk every PTE from @address to @end in one call, instead of
 * restarting the walk at each folio boundary.
 */
```

**After (internal edit, illustrative):**
```c
/* Walk every PTE from @address to @end. */
```

**Rule:** changelog is before/after doc, comment is standalone [CC-10]. Don't frame current behavior as "instead of" alternative not visible in code. **Provenance:** internal drafting session, no external reviewer, not merged — illustrative only.

## Example 4 — redundant cleanup hunk riding in semantic patch (Andy Shevchenko review)

**Before:** patch includes unrelated whitespace/formatting + logic change.

**After:** split per patch-series.md §1 — "when a hunk is unrelated to patch's stated purpose, split it out" — Andy Shevchenko Message-ID ak99ouEr7n807Ss3@ashevche-desk.local

**Rule:** One logical change per patch [patch-series.md §1].

---
**Labeling convention per CONTRIBUTING §8:**
- `EXTERNAL` = has lore Message-ID or public commit hash verifiable via `git show` / lore.kernel.org
- `INTERNAL DRAFT` = session-local, never posted, no external reviewer, illustrative only — must not be cited as evidence of upstream style, kept only to show cut-test / compression pattern

Add more EXTERNAL examples with `git log --grep Assisted-by` + lore link.
