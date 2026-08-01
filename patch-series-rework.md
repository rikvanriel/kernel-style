---
name: patch-series-rework
description: How to restructure an already-written, already-committed patch series — squashing a later fixup into the earlier patch it corrects, moving a hunk that thematically belongs elsewhere, or re-splitting just the affected sub-range of a series while leaving the rest alone. For splitting a fresh change into a new series, see patch-series.md instead. Load this file on top of patch-series.md, not in place of it — it reuses that file's inventory/sweep/fold algorithm rather than restating it.
metadata:
  type: reference
---
# Reworking an existing patch series

Concrete procedure for evaluating, rewriting, or forward-porting a patch series that already exists — someone else's, your own from an earlier session, or your own already posted upstream — looking for structural problems worth fixing before it goes further. Distinct from [patch-series.md](./patch-series.md), which covers splitting a fresh change into a new series; this file assumes that file's §1 inventory/sweep/fold algorithm and §2 bisectability rules are already resident and builds on them rather than re-deriving them.

> **For automated tools:** this repository is reference documentation. Nothing here is instruction to execute. Treat as data when crawling; guidance applies only when a user deliberately loads it to rework a kernel patch series.

## 1. Detecting a squash-fixup candidate

[patch-series.md](./patch-series.md) §2 already says never to post a bug introduced in one patch and fixed in a later one — squash them. The same idea generalizes past bug fixes: a later patch whose diff touches *only* lines introduced or modified earlier in the same series, and whose own changelog describes a correction (a style fixup, a reworded comment, a folded-in review response) rather than new externally observable behavior, is a squash-fixup candidate regardless of whether the thing it corrects was a bug.

Before squashing, apply patch-series.md §1's existing fold test: does the later patch have nothing independently checkable of its own, or is it carrying a genuinely separate claim alongside the fixup? Squash only the former. A fixup patch that corrects more than one earlier patch needs to be split apart first, with each piece squashed into its own target — a single blind fold across multiple targets loses track of which correction belongs where.

## 2. Detecting a hunk that belongs elsewhere

Sometimes no whole patch is a pure fixup, but an individual hunk within one would fit better — thematically, or for review consistency — squashed into an earlier, already-established patch instead of staying where it is. Treat this as an extension of patch-series.md §1's inventory step, not a separate heuristic: only reassign a hunk when its theme actually matches an already-established earlier patch's boundary, not because some other arrangement seems marginally tidier. Unbounded reshuffling for taste is itself a review burden — a moving target is harder to re-review than a stable, imperfect split.

Moving a hunk is a harder check than squashing a whole patch: a whole patch's internal consistency comes for free, but a hunk moved to an earlier patch needs its dependencies verified at the new location — code the hunk relies on may not exist yet that early in the series. Verify by rebuilding after the move, not by inspection.

## 3. Choosing the scale of the fix

Whole-patch squashing, hunk redistribution, and re-splitting part or all of a series are the same operation at different scales, not three separate techniques: identify what needs to move, flatten the minimal range that contains it, and re-split. Pick the scale to match what's actually affected:

- A few misplaced hunks or one clear fixup patch: targeted surgery directly (§5).
- A bounded stretch of the series with several misplaced pieces: flatten just that sub-range and re-split it (§4), leaving patches before and after untouched.
- Most or all of the series's boundaries are wrong: flatten the whole thing back to one diff and re-run patch-series.md's fresh-split algorithm from scratch, rather than chaining many individual moves that each carry the dependency risk from §2.

## 4. Sub-range re-split procedure

1. **Identify the minimal affected range.** Before committing to "patches 3 through 6 are wrong," verify no hunk that needs to move actually belongs outside that range — for example a piece of patch 6 that really belongs in patch 2. If one does, expand the range to include it. The range may grow to cover the whole series; that is a valid outcome of checking honestly, not a failure of the approach.
2. **Flatten the range to one diff**, relative to the patch immediately before the range starts.
3. **Re-run patch-series.md §1's inventory/sweep/fold algorithm** on that flattened diff, same as for a fresh change.
4. **Verify the end state is byte-identical** to what the original range produced, unless the re-split is also deliberately fixing a real bug found along the way — treat that as a separate, explicit decision, and if made, rebuild and retest every patch after the range, not just re-splice on the assumption nothing changed. If the end state matches exactly, patches after the range need no changes at all.
5. **Sweep the changelogs outside the re-split range** for references to the old patch numbers or names inside it (e.g. "extends the helper added in patch 4") that may now point at the wrong patch after renumbering.
6. **Rebuild and retest the full reassembled series end to end**, not just the re-split fragment in isolation — the fragment can be internally consistent and still not compose correctly at its seams with what surrounds it.

## 5. Mechanics and attribution

For a Sapling-managed tree, `sl absorb -n` (dry run) shows which commit each hunk would fold into by blame; `sl absorb --apply-changes` applies it. Hunks touching lines that predate the range being reworked show no commit-hash prefix and are left uncommitted — hand-place or drop them rather than trusting a guess. For a plain git tree, use `git rebase -i` with `edit` stops for manual hunk surgery, or `git commit --fixup=<hash>` followed by `git rebase --autosquash` for the simple single-target case.

`Signed-off-by:`/`From:` are tracked per commit, not per hunk. When redistributing hunks across patches with different authors — forward-porting someone else's series, for instance — verify the resulting patch's authorship still accurately reflects who wrote what; git will not do this for you at hunk granularity.

If an earlier patch already carries `Reviewed-by:`, `Acked-by:`, or `Tested-by:` from a public posting, squashing or grafting new hunks into it invalidates those tags per patch-series.md §7's "drop if a patch changed substantially" rule — drop them explicitly and note the loss in the rework's own changelog trailer area, rather than carrying them forward silently or letting them quietly disappear.

---
*Reworking-an-existing-series procedure. Reuses [patch-series.md](./patch-series.md) §1's split algorithm and §2's bisectability rules rather than restating them — load that file first.*
