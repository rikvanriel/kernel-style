#!/usr/bin/env python3
"""
check-orphan-ids.py — verify hot Rule IDs have matching rationale entries and vice versa.

Per CONTRIBUTING §9: fail PR if hot rule ID has no matching cold rationale entry,
or cold rationale entry has no matching hot rule (orphan after deletion).

Usage:
  ./scripts/check-orphan-ids.py
  ./scripts/check-orphan-ids.py --strict  # fail on any orphan, otherwise warn only
  ./scripts/check-orphan-ids.py --json    # machine readable

Checks:
- Collects IDs from hot/Tier2 files: kernel-style.md, changelog-style.md, coding.md,
  llm-tells-checklist.md, review.md, commit.md, etc. Pattern: <!-- ID -->
- Collects IDs from rationale files: changelog-style-rationale.md, kernel-readability-rationale.md etc.
- Reports hot-only and rationale-only.
- Reports the same ID used twice inside one hot file. Set membership alone cannot see
  this: reusing a live ID for an unrelated new rule leaves both files "matched" and
  the check green, while the older rule silently points at the wrong rationale entry.

This script was added per review feedback round 2 (Rockhopper):
Previously CONTRIBUTING claimed "CI orphan check passes" with no script — now this is the script.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

HOT_FILES = [
    "kernel-style.md",
    "changelog-style.md",
    "coding.md",
    "llm-tells-checklist.md",
    "review.md",
    "commit.md",
    "planning.md",
    "patch-series.md",
]

RATIONALE_FILES = [
    "changelog-style-rationale.md",
    "kernel-readability-rationale.md",
    "patch-series-rationale.md",
]

ID_RE = re.compile(r"<!--\s*([A-Za-z0-9-]+)\s*-->")

# An ID may appear in several hot files: CONTRIBUTING §2 asks for one canonical
# location plus short cross-references. Twice in the SAME file is a collision.
# Entries here are known duplications CONTRIBUTING §2 already tracks for consolidation.
KNOWN_INTRA_FILE_DUPES = {
    "changelog-style.md": {"CL-14"},
}

def collect_ids_from_file(path: Path):
    try:
        text = path.read_text(errors="replace")
    except FileNotFoundError:
        return set()
    ids = set(ID_RE.findall(text))
    # Filter: only Rule IDs that look like R0-, CL-, CC-, CS- per namespace
    # Keep all that match ^[A-Z][A-Z]*-[0-9] or R0- pattern
    filtered = set()
    for i in ids:
        # Accept R0-*, CL-*, CC-*, CS-*, and also sub-IDs like CL-10b
        if re.match(r"^(R0|CL|CC|CS)-", i):
            filtered.add(i)
    return filtered

def collect_dupes_from_file(path: Path):
    """IDs appearing more than once in one file, minus the tracked exceptions."""
    try:
        text = path.read_text(errors="replace")
    except FileNotFoundError:
        return {}
    counts = {}
    for i in ID_RE.findall(text):
        if re.match(r"^(R0|CL|CC|CS)-", i):
            counts[i] = counts.get(i, 0) + 1
    allowed = KNOWN_INTRA_FILE_DUPES.get(path.name, set())
    return {i: n for i, n in counts.items() if n > 1 and i not in allowed}

def main():
    parser = argparse.ArgumentParser(description="check orphan Rule IDs hot <-> rationale")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any orphan")
    parser.add_argument("--json", action="store_true", help="json output")
    args = parser.parse_args()

    hot_ids = set()
    hot_by_file = {}
    dupes_by_file = {}
    for fname in HOT_FILES:
        p = REPO / fname
        ids = collect_ids_from_file(p)
        hot_by_file[fname] = ids
        hot_ids |= ids
        d = collect_dupes_from_file(p)
        if d:
            dupes_by_file[fname] = d

    rationale_ids = set()
    rationale_by_file = {}
    for fname in RATIONALE_FILES:
        p = REPO / fname
        ids = collect_ids_from_file(p)
        rationale_by_file[fname] = ids
        rationale_ids |= ids

    hot_only = sorted(hot_ids - rationale_ids)
    rationale_only = sorted(rationale_ids - hot_ids)

    if args.json:
        import json
        print(json.dumps({
            "hot_ids": sorted(hot_ids),
            "rationale_ids": sorted(rationale_ids),
            "hot_only": hot_only,
            "rationale_only": rationale_only,
            "hot_by_file": {k: sorted(v) for k,v in hot_by_file.items()},
            "rationale_by_file": {k: sorted(v) for k,v in rationale_by_file.items()},
            "intra_file_dupes": dupes_by_file,
        }, indent=2))
    else:
        print(f"Hot files: {HOT_FILES}")
        print(f"  Total unique hot IDs: {len(hot_ids)} → {sorted(hot_ids)}")
        print()
        print(f"Rationale files: {RATIONALE_FILES}")
        print(f"  Total unique rationale IDs: {len(rationale_ids)} → {sorted(rationale_ids)}")
        print()
        if hot_only:
            print(f"FAIL: Hot IDs without matching rationale (orphan hot): {hot_only}")
            for fname, ids in hot_by_file.items():
                orphan_here = sorted(ids & set(hot_only))
                if orphan_here:
                    print(f"  - {fname}: {orphan_here}")
        else:
            print("PASS: No hot-only IDs — every hot ID has matching rationale entry")

        print()
        if rationale_only:
            print(f"FAIL: Rationale IDs without matching hot (orphan rationale): {rationale_only}")
            for fname, ids in rationale_by_file.items():
                orphan_here = sorted(ids & set(rationale_only))
                if orphan_here:
                    print(f"  - {fname}: {orphan_here}")
        else:
            print("PASS: No rationale-only IDs — every rationale ID has matching hot entry")

        print()
        if dupes_by_file:
            print("FAIL: Same Rule ID used twice inside one hot file:")
            for fname, d in dupes_by_file.items():
                for i, n in sorted(d.items()):
                    print(f"  - {fname}: {i} appears {n} times — give the new rule the next free ID")
        else:
            print("PASS: No duplicate Rule IDs within a hot file")

    sys.exit(1 if (hot_only or rationale_only or dupes_by_file) else 0)

if __name__ == "__main__":
    main()
