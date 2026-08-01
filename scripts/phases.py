#!/usr/bin/env python3
"""
phases.py — loader for kernel-style 4-phase workflow with token accounting.

Prints exact files to cat for a given phase and token counts, so an LLM
doesn't have to remember cumulative residency rules.

Real per-profile extraction: --bug-class or --extract loads only one
developer section from exemplars.md instead of the full 3,685w file,
saving ~3k words / ~5.5k tok. This makes exemplars-routing.md's claim real.

Usage:
  ./scripts/phases.py --phase 1              # draft code
  ./scripts/phases.py --phase 2              # review before commit
  ./scripts/phases.py --phase 2 --bug-class race
  ./scripts/phases.py --phase 2 --bug-class race --extract-only
  ./scripts/phases.py --phase 2 --extract "Thomas Gleixner"
  ./scripts/phases.py --phase 3              # changelog
  ./scripts/phases.py --phase 3 --multi      # multi-patch series
  ./scripts/phases.py --all                  # all phases with totals
  ./scripts/phases.py --list-profiles        # list available exemplars profiles

Token counting: tiktoken cl100k_base if installed, else chars//4 heuristic.
"""

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Bug class -> developer profile mapping (canonical: exemplars-routing.md)
BUG_CLASS_MAP = {
    "syzkaller": "Dan Williams",
    "uaf": "Dan Williams",
    "kasan": "Dan Williams",
    "oops": "Dan Williams",
    "race": "Thomas Gleixner",
    "concurrency": "Thomas Gleixner",
    "locking-race": "Thomas Gleixner",
    "barrier": "Peter Zijlstra",
    "memory-ordering": "Peter Zijlstra",
    "perf": "Mel Gorman",
    "performance": "Mel Gorman",
    "benchmark": "Mel Gorman",
    "locking": "David Hildenbrand",
    "refcount": "David Hildenbrand",
    "lifetime": "David Hildenbrand",
    "tradeoff": "Michal Hocko",
    "design": "Michal Hocko",
    "cleanup": "Ingo Molnar",
    "surgical": "Ingo Molnar",
    "forensic": "Breno Leitao",
    "production": "Shakeel Butt",
}

PHASES = {
    0: {
        "name": "Phase 0 — plan before writing code (on-demand)",
        "trigger": "change touches >1 func/file, >1 behavior, or can't be 1 sentence without 'and'. Skip for 1-line fix.",
        "files": ["planning.md"],
        "optional": ["patch-series.md", "patch-series-rework.md"],
        "note": "Load on demand before Phase 1 for non-trivial changes. Get human sign-off before code."
    },
    1: {
        "name": "Phase 1 — draft code (always hot)",
        "trigger": "Always hot when drafting kernel code",
        "files": ["kernel-style.md", "kernel-readability-principles.md", "llm-tells-checklist.md", "coding.md"],
        "optional": ["exemplars-routing.md"],
        "note": "Keep resident through Phase 2+3 per cumulative model — do not unload until task end.",
        "target_tokens": 5000,
    },
    2: {
        "name": "Phase 2 — review before git commit",
        "trigger": "After draft passes llm-tells final pass, before git commit",
        "files": ["kernel-style.md", "kernel-readability-principles.md", "llm-tells-checklist.md", "coding.md",
                  "exemplars-routing.md", "review.md", "peer-review.md"],
        "optional": ["exemplars.md", "changelog-style.md", "patch-series.md"],
        "note": "Load exemplars-routing.md to pick profile, then load only that section from exemplars.md via --bug-class or --extract. Saves ~5k tok vs full file. Run peer-review.md two questions as self-review, then llm-tells re-pass.",
        "target_tokens": 11000,
    },
    3: {
        "name": "Phase 3 — draft changelog",
        "trigger": "After Phase 2 review passes",
        "files": ["kernel-style.md", "kernel-readability-principles.md", "llm-tells-checklist.md", "coding.md",
                  "review.md", "exemplars-routing.md", "peer-review.md",
                  "changelog-style.md", "commit.md"],
        "optional": ["patch-series.md", "exemplars.md"],
        "note": "Mandatory: changelog-style.md. Run lint-changelog.py + checkpatch.pl + peer-review two questions focused on commit message. Verify cover letter vs patches if multi.",
        "target_tokens": 17000,
        "multi_target_tokens": 21000,
    },
}

def count_tokens(text: str) -> int:
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4

def file_info(p: Path):
    try:
        txt = p.read_text(errors="replace")
        w = len(txt.split())
        t = count_tokens(txt)
        return w, t, txt
    except FileNotFoundError:
        return None, None, None

def parse_exemplars_profiles():
    """Parse exemplars.md into dict name -> section text."""
    f = REPO / "exemplars.md"
    if not f.exists():
        return {}
    content = f.read_text(errors="replace")
    # Split on headings that start with "# <Name> kernel style" or "# <Name> style" or "# <Name>" alone
    # Pattern: ^# (.+?) kernel style$ or ^# (.+?) style$
    # We want to capture each top-level "# " section after the intro
    sections = {}
    # Find all top-level headings
    heading_re = re.compile(r"^# (.+?)(?: kernel style| style)?\s*$", re.MULTILINE)
    matches = list(heading_re.finditer(content))
    # Filter out the very first intro heading "How to choose..."
    for idx, m in enumerate(matches):
        name = m.group(1).strip()
        # Skip the routing intro heading
        if "How to choose" in name:
            continue
        start = m.start()
        end = matches[idx+1].start() if idx+1 < len(matches) else len(content)
        section_text = content[start:end].strip()
        # Use full name as key, e.g., "David Hildenbrand"
        # Heading may be "David Hildenbrand kernel style" -> captured as "David Hildenbrand"
        # But also some are "Thomas Gleixner kernel style" etc
        # Keep mapping
        sections[name] = section_text
        # Also add short first-name mapping for convenience? Keep full.
    return sections

def extract_profile_text(profile_name: str):
    profiles = parse_exemplars_profiles()
    # Exact match first
    if profile_name in profiles:
        return profile_name, profiles[profile_name]
    # Case-insensitive substring match
    lower = profile_name.lower()
    for full_name, text in profiles.items():
        if lower in full_name.lower() or full_name.lower() in lower:
            return full_name, text
    # No match
    return None, None

def list_profiles():
    profiles = parse_exemplars_profiles()
    for name in sorted(profiles.keys()):
        w = len(profiles[name].split())
        t = count_tokens(profiles[name])
        print(f"{name:30s} {w:4d}w ~{t:4d}tok")

def print_phase(n: int, multi=False, bug_class=None, extract=None, extract_only=False):
    ph = PHASES[n]
    print(f"# {ph['name']}")
    print(f"Trigger: {ph['trigger']}")
    print(f"Note: {ph['note']}")
    print()
    total_w = 0
    total_t = 0
    for fname in ph["files"]:
        f = REPO / fname
        w, t, _ = file_info(f)
        if w is None:
            print(f"  MISSING: {fname}")
            continue
        total_w += w
        total_t += t
        print(f"  HOT      {fname:35s} {w:5d}w ~{t:5d}tok")
    for fname in ph.get("optional", []):
        if extract_only and fname == "exemplars.md":
            # Don't count full file when extract-only
            continue
        f = REPO / fname
        w, t, _ = file_info(f)
        if w is None:
            continue
        marker = ""
        if fname == "exemplars.md" and n in (2,3) and (bug_class or extract):
            marker = " <- full file ON-DEMAND, but see --extract below for token saving"
        print(f"  ON-DEMAND {fname:35s} {w:5d}w ~{t:5d}tok{marker}")
    print()
    print(f"  Phase {n} HOT total: {total_w}w ~{total_t}tok", end="")
    if "target_tokens" in ph:
        tgt = ph["multi_target_tokens"] if multi and n==3 else ph.get("target_tokens")
        if tgt:
            over = total_t - tgt
            status = f" OVER by {over}" if over>0 else f" under by {-over}"
            print(f" (target {tgt}{status})")
        else:
            print()
    else:
        print()

    # Bug class -> profile extraction
    chosen_profile = None
    if bug_class:
        chosen_profile = BUG_CLASS_MAP.get(bug_class.lower())
        if not chosen_profile:
            # try substring match on bug class keys
            for k, v in BUG_CLASS_MAP.items():
                if k in bug_class.lower():
                    chosen_profile = v
                    break
        if chosen_profile:
            print(f"  Bug class '{bug_class}' → profile '{chosen_profile}' (from exemplars-routing.md canonical)")
        else:
            print(f"  Bug class '{bug_class}' → no mapping found, use --extract <Developer Name> or see --list-profiles")
            chosen_profile = None
    if extract:
        chosen_profile = extract

    if chosen_profile:
        full_name, section = extract_profile_text(chosen_profile)
        if section:
            w = len(section.split())
            t = count_tokens(section)
            full_w = file_info(REPO / "exemplars.md")[0] or 0
            saved_w = full_w - w
            saved_t = (file_info(REPO / "exemplars.md")[1] or 0) - t
            print(f"  Extracted profile '{full_name}': {w}w ~{t}tok (full exemplars.md {full_w}w, saves {saved_w}w ~{saved_t}tok)")
            if extract_only:
                # Print just the section for direct use
                print(f"\n--- BEGIN EXEMPLARS PROFILE: {full_name} ---\n")
                print(section)
                print(f"\n--- END PROFILE: {full_name} ---\n")
                return
            else:
                print(f"  To load only this profile: ./scripts/phases.py --phase {n} --extract \"{full_name}\" --extract-only")
                print(f"  Or cat with: python3 -c \"from pathlib import Path; import re; txt=Path('exemplars.md').read_text(); ...\"")
        else:
            print(f"  Profile '{chosen_profile}' not found. Available:")
            list_profiles()
    print()
    # cat commands
    print(f"  Load command (hot): cat {' '.join(ph['files'])}")
    print()

def main():
    parser = argparse.ArgumentParser(description="kernel-style phase loader with real exemplars extraction")
    parser.add_argument("--phase", type=int, choices=[0,1,2,3], help="phase number")
    parser.add_argument("--multi", action="store_true", help="Phase 3 multi-patch")
    parser.add_argument("--bug-class", help="for Phase 2: syzkaller|race|perf|locking|tradeoff|cleanup (maps to developer)")
    parser.add_argument("--extract", help="extract specific developer profile, e.g. 'Thomas Gleixner'")
    parser.add_argument("--extract-only", action="store_true", help="when used with --extract or --bug-class, print only that profile section, not phase totals")
    parser.add_argument("--all", action="store_true", help="show all phases")
    parser.add_argument("--list-profiles", action="store_true", help="list all available exemplars profiles with word counts")
    args = parser.parse_args()

    if args.list_profiles:
        list_profiles()
        return

    if args.all:
        for i in [0,1,2,3]:
            print_phase(i, multi=(i==3 and args.multi), bug_class=args.bug_class, extract=args.extract, extract_only=args.extract_only)
        if not args.extract_only:
            print("# To actually load for an LLM task, cat the HOT files listed above in order.")
            print("# For token saving, use --bug-class or --extract to load one profile only.")
        return

    if args.phase is None:
        parser.print_help()
        print("\nExamples:")
        print("  ./scripts/phases.py --phase 1")
        print("  ./scripts/phases.py --phase 2 --bug-class race")
        print("  ./scripts/phases.py --phase 2 --bug-class race --extract-only")
        print("  ./scripts/phases.py --phase 2 --extract \"David Hildenbrand\" --extract-only > /tmp/profile.md")
        print("  ./scripts/phases.py --list-profiles")
        sys.exit(2)

    print_phase(args.phase, multi=args.multi, bug_class=args.bug_class, extract=args.extract, extract_only=args.extract_only)

if __name__ == "__main__":
    main()
