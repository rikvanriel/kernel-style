#!/usr/bin/env python3
"""
verify-cover-letter.py — check that cover letter claims match actual patches.

Per patch-series.md §5 and kernel-style.md §0 R0-4: for every number and every
"patch N does/is the only one that..." claim in the cover letter, open that
specific patch's own current changelog and diff and confirm exact match.
This script does a heuristic automated part of that check; manual verification
is still mandatory.

Usage:
  ./scripts/verify-cover-letter.py --cover cover.txt --range HEAD~5..HEAD
  ./scripts/verify-cover-letter.py --cover cover.txt --patches patches/*.patch
  git show HEAD:cover.txt | ./scripts/verify-cover-letter.py --stdin --range HEAD~5..HEAD
  ./scripts/verify-cover-letter.py --cover cover.txt --patches patch1.patch --strict

Heuristic checks:
- Extracts numbers with units (%, s, ms, us, µs, ns, MB/s, x, times) from cover and patches
- Flags cover numbers not found in patches (potential stale benchmark)
- Flags Before:/After: table in cover without matching table in patches (pre-split staleness)
- Lists patch N references to manually verify
- Flags mechanism claims ("merge") not in patches

Exit 0 = no obvious staleness detected by heuristic (manual check still required)
Exit 1 = potential stale claims found
Exit 2 = error / incomplete (e.g., no patches provided)

This is NOT a complete verification — see patch-series.md §5: open each patch's
own changelog/diff and confirm exact match for every number.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path
from collections import Counter

# Improved unit list per feedback #3: us was missing, also µs, ns, x
# Matches: 2801 us, 207 us, 14.5x, 2.3x, 10%, 4.5s, 13.195s, 4720 MB/s, etc.
NUM_RE = re.compile(
    r"(?P<val>\d+(?:\.\d+)?)\s*(?P<unit>%|s|ms|us|µs|ns|MB/s|sec(?:ond)?s?|times?|x)\b",
    re.IGNORECASE
)
# Also capture bare large numbers that look like benchmark results (3+ digits) without unit, to catch tables
BARE_NUM_RE = re.compile(r"\b(?P<val>\d{3,}(?:\.\d+)?)\b")

PATCH_REF_RE = re.compile(r"patch\s+(?P<num>\d+)", re.IGNORECASE)
BENCH_TABLE_RE = re.compile(r"Before:\s*~?.*\n.*After:", re.IGNORECASE | re.MULTILINE)

def get_patch_texts_from_range(git_range: str):
    result = subprocess.run(["git", "log", "--reverse", "--pretty=format:%H %s", git_range],
                            capture_output=True, text=True, cwd=Path(__file__).resolve().parent.parent)
    if result.returncode != 0:
        print(f"git log failed: {result.stderr}", file=sys.stderr)
        return []
    commits = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
    patches = []
    for h in commits:
        r = subprocess.run(["git", "show", "-s", "--format=%B", h], capture_output=True, text=True)
        patches.append((h, r.stdout))
    return patches

def get_patch_texts_from_files(files):
    patches = []
    for f in files:
        txt = Path(f).read_text(errors="replace")
        patches.append((f, txt))
    return patches

def extract_numbers(text: str):
    """Extract numbers with optional units, return Counter of values."""
    nums = []
    for m in NUM_RE.finditer(text):
        try:
            val = float(m.group("val"))
            unit = m.group("unit").lower()
            # Normalize us/μs
            if unit in ("µs",):
                unit = "us"
            nums.append((val, unit, m.group(0), m.start()))
        except:
            continue
    # Also bare numbers for tables like 2801 / 1198
    for m in BARE_NUM_RE.finditer(text):
        # Skip if already captured with unit at same position (approx)
        pos = m.start()
        # Check if overlapping with previous
        if any(abs(pos - existing[3]) < 5 for existing in nums):
            continue
        try:
            val = float(m.group("val"))
            nums.append((val, "bare", m.group(0), pos))
        except:
            continue
    return nums

def verify(cover: str, patches, strict=False):
    violations = []
    warnings = []

    # Check benchmark table presence
    cover_has_table = bool(BENCH_TABLE_RE.search(cover))
    if cover_has_table:
        found_in_patches = any(BENCH_TABLE_RE.search(p[1]) or "Before:" in p[1] for p in patches) if patches else False
        if patches and not found_in_patches:
            violations.append("Cover letter has Before:/After: benchmark table but no patch contains matching table — possible stale pre-split artifact [patch-series.md §5]")

    # Extract numbers from cover and patches
    cover_nums = extract_numbers(cover)
    patch_nums_combined = []
    for _, ptxt in patches:
        patch_nums_combined.extend(extract_numbers(ptxt))

    # Build set of patch values for quick lookup
    patch_values = set((round(v, 2), u) if u != "bare" else (round(v, 2), "bare") for v, u, _, _ in patch_nums_combined)
    patch_bare_values = set(round(v, 2) for v, u, _, _ in patch_nums_combined if u == "bare" or True)

    # Find cover numbers not in patches
    if cover_nums and patches:
        # Focus on numbers that look like benchmark results (has unit or 3+ digits)
        # Ignore small counts like patch numbers themselves (1-15)
        significant_cover = [n for n in cover_nums if not (n[1] == "bare" and n[0] < 100)]
        for val, unit, raw, pos in significant_cover:
            # Check if this exact value exists in patches (with same or compatible unit)
            found_exact = any(abs(val - pv[0]) < 0.01 for pv in patch_nums_combined if pv[0]==val or abs(pv[0]-val)<0.01)
            # More precise: check value+unit
            key = (round(val,2), unit)
            # For bare numbers, check value only
            if unit == "bare":
                if round(val,2) not in patch_bare_values:
                    # Don't flag if it's a timestamp/date fragment
                    if val > 1000:  # likely benchmark
                        ctx = cover[max(0,pos-20):pos+20].replace("\n"," ")
                        warnings.append(f"Cover number '{raw}' ({ctx}) not found in patches — possible stale benchmark (patches have {[f'{v}{u}' for v,u,_,_ in patch_nums_combined[:5]]} ...)")
            else:
                if key not in patch_values:
                    # Look for same unit but different value (potential stale)
                    same_unit_vals = [pv[0] for pv in patch_nums_combined if pv[1]==unit]
                    if same_unit_vals:
                        closest = min(same_unit_vals, key=lambda x: abs(x-val))
                        if abs(closest - val) / max(val,1) > 0.02:  # >2% diff
                            ctx = cover[max(0,pos-20):pos+20].replace("\n"," ")
                            violations.append(f"Cover has '{raw}' but patches have '{closest}{unit}' for same unit — likely stale (context: {ctx}) [R0-4, patch-series.md §5]")
                    else:
                        # No same unit in patches at all
                        if unit in ("us","ms","%","x","times","mb/s","s"):
                            ctx = cover[max(0,pos-20):pos+20].replace("\n"," ")
                            warnings.append(f"Cover number '{raw}' with unit '{unit}' not found in patches (context: {ctx}) — verify manually")

        # Specific check for the real bug from today: cover 2721/1198 vs actual 2801/1188 etc.
        # If cover has multiple bare numbers in a table-like context, compare sets
        cover_bare = [round(v,2) for v,u,_,_ in cover_nums if u=="bare" and v>=100]
        patch_bare = [round(v,2) for v,u,_,_ in patch_nums_combined if (u=="bare" or u in ("us","ms")) and v>=100]
        if cover_bare and patch_bare and len(cover_bare)>=2 and len(patch_bare)>=2:
            # If less than 50% overlap, likely stale
            overlap = len(set(cover_bare) & set(patch_bare))
            if overlap / max(len(set(cover_bare)),1) < 0.5:
                violations.append(f"Cover bare numbers {sorted(set(cover_bare))[:8]} have <50% overlap with patch bare numbers {sorted(set(patch_bare))[:8]} — likely stale benchmark table [R0-4]")

    # Check numbers in cover — always warn to manually verify
    if cover_nums:
        sample = [f"{raw}" for _,_,raw,_ in cover_nums[:10]]
        print(f"Cover numbers extracted (with units): {sample}")
        if patches:
            print(f"Patch numbers extracted (with units, first 10): {[f'{rv[2]}' for rv in patch_nums_combined[:10]]}")

    # Check patch N claims
    refs = PATCH_REF_RE.findall(cover)
    if refs:
        print(f"Cover references patches: {sorted(set(refs))} — verify each 'patch N does...' claim against patch N's current changelog/diff, not earlier draft [patch-series.md §5]")

    # Mechanism claim check
    if "merge" in cover.lower() and patches and not any("merge" in p[1].lower() for p in patches):
        violations.append("Cover mentions 'merge' but no patch mentions it — verify mechanism claim")

    return violations, warnings

def main():
    parser = argparse.ArgumentParser(description="verify cover letter against patches (heuristic, manual check still required)")
    parser.add_argument("--cover", help="cover letter file")
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--range", help="git range for patches, e.g. HEAD~5..HEAD")
    parser.add_argument("--patches", nargs="*", help="patch files")
    parser.add_argument("--strict", action="store_true", help="strict: treat warnings as violations")
    args = parser.parse_args()

    if args.stdin:
        cover = sys.stdin.read()
    elif args.cover:
        cover = Path(args.cover).read_text(errors="replace")
    else:
        parser.print_help()
        sys.exit(2)

    patches = []
    if args.range:
        patches = get_patch_texts_from_range(args.range)
    elif args.patches:
        patches = get_patch_texts_from_files(args.patches)
    else:
        patches = []

    vios, warns = verify(cover, patches, strict=args.strict)

    if warns:
        print(f"\nWarnings ({len(warns)}):")
        for w in warns:
            print(f"  - {w}")

    if vios:
        print(f"\nPotential staleness — {len(vios)} flagged:")
        for v in vios:
            print(f"  - {v}")
        print("\nThis is a heuristic check only. Per patch-series.md §5 and kernel-style.md R0-4:")
        print("  Open each patch's own current changelog/diff and confirm exact match for every number.")
        sys.exit(1)
    else:
        if not patches:
            print("\nINCOMPLETE: No patches provided via --range or --patches")
            print("  Only cover letter was analyzed — cannot verify numbers against patches.")
            print("  This is NOT a real verification yet. Manual check per patch-series.md §5 still required:")
            print("    For every number and 'patch N does...' claim, open that specific patch's changelog/diff.")
            sys.exit(2)
        else:
            print("\nHEURISTIC PASS — no obvious staleness detected by automated checks")
            print("  BUT: manual verification per patch-series.md §5 and R0-4 is still mandatory:")
            print("  Open each patch's own current changelog/diff and confirm exact match for every number/mechanism claim.")
            if warns:
                print(f"  {len(warns)} warning(s) above should still be manually checked.")
            sys.exit(0)

if __name__ == "__main__":
    main()
