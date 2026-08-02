#!/usr/bin/env python3
"""
lint-changelog.py — machine-checkable subset of kernel-style rules.

Checks a commit message file or patch changelog file for:
- R0 factual integrity markers (TODO vs invented numbers — heuristic)
- CL-10 subject format: subsys: lowercase imperative, no trailing period
- CL-11 Fixes: must be paired with Cc: stable@
- CL-12 paragraph caps: 90% ≤50w, max 70, never beyond
- CL-13 banned LLM tells: "This patch", "Note that", marketing adjectives, em-dash sprinkling, recap
- CL-14 internal identifiers: bucket hashes, agent nicknames, private branches
- CL-15 verbatim artifact rule: bugfix mentioning KASAN/WARNING/oops must include indented literal block

Usage:
  ./scripts/lint-changelog.py <changelog-file>
  ./scripts/lint-changelog.py --stdin < patch.txt
  git log -1 --pretty=%B | ./scripts/lint-changelog.py --stdin

Exit 0 = pass, 1 = violations found, 2 = error.
Designed to run in commit.md Phase 3 final verification alongside checkpatch.pl.
"""

import argparse
import re
import sys
from pathlib import Path

BANNED_PHRASES = [
    (r"\bThis patch\b", "Opens with 'This patch' — rewrite to open with problem in present tense [CL-13, llm-tells]"),
    (r"\bNote that\b", "Hedging filler 'Note that' — state fact directly [CL-13]"),
    (r"\bImportantly\b", "Hedging filler 'Importantly' — cut [CL-13]"),
    (r"\bIt's worth noting\b", "Hedging filler — cut [CL-13]"),
    (r"\bIn summary\b", "Recap paragraph 'In summary' — cut, end on effect [CL-13]"),
    (r"\brobust\b|\bpowerful\b|\bseamless\b|\bcomprehensive\b|\belegant\b", "Marketing adjective — quantify effect, don't praise [CL-13]"),
    (r"\bnot X and not Y\b|\bdoesn'?t not\b|\bnot uncommon\b", "Double negative — rewrite as positive [CL-13]"),
]

# em-dash sprinkling: more than 2 em-dashes in changelog is flag
EM_DASH_RE = re.compile(r"—")

INTERNAL_PATTERNS = [
    (r"\bmyclaw\b|\bmetaclaw\b|\badelie\b|\bmacaroni\b|\bemperor\b|\bchinstrap\b|\brookhopper\b", "Internal agent/penguin nickname in changelog [CL-14, audience]"),
    (r"bucket [a-f0-9]{8,}|syzkaller.*bucket", "Private syzkaller bucket hash without public syzbot link [CL-14]"),
    (r"internal-fixes|private.*branch", "Internal branch name [CL-14]"),
    (r"\bJIRA-[0-9]+\b|\bT[0-9]{6,}\b.*phabricator", "Vendor ticket ID [CL-14] — use generic phrasing"),
]

# Prefix is usually lowercase, but established subsystems capitalise: PM:, ACPI:,
# KVM:, PCI:, RDMA/, Bluetooth:. Allow uppercase in the prefix, not in the summary.
SUBJECT_RE = re.compile(r"^(?P<prefix>[A-Za-z0-9_,/+-]+): (?P<summary>[^\n]+)$")
# x86/tip exception: capitalized first word allowed
X86_CAP_RE = re.compile(r"^x86/")

def count_words(s: str) -> int:
    return len(s.split())

def parse_commit(text: str):
    lines = text.splitlines()
    # subject is first non-empty line
    subject = ""
    body_start = 0
    for i, l in enumerate(lines):
        if l.strip():
            subject = l.strip()
            body_start = i+1
            break
    body = "\n".join(lines[body_start:]).strip()
    # split trailers: lines at end matching Trailer: value
    trailer_re = re.compile(r"^(Fixes:|Cc:|Reported-by:|Suggested-by:|Tested-by:|Link:|Assisted-by:|Signed-off-by:)\s")
    trailers = []
    body_lines = body.splitlines()
    # trailers are contiguous from end
    non_trailer_end = len(body_lines)
    for i in range(len(body_lines)-1, -1, -1):
        if not body_lines[i].strip():
            continue
        if trailer_re.match(body_lines[i]):
            non_trailer_end = i
            # continue collecting upwards
            continue
        # once we hit non-trailer after trailers started, stop
        if non_trailer_end != len(body_lines):
            # we already collected some trailers, stop when non-trailer
            # Actually need to find start of trailer block
            break
    # more robust: find last blank-separated trailer block
    trailer_block = []
    for l in reversed(body_lines):
        if not l.strip():
            if trailer_block:
                break
            continue
        if trailer_re.match(l):
            trailer_block.append(l)
        else:
            if trailer_block:
                break
    trailers = list(reversed(trailer_block))
    # body paragraphs: split on blank lines, ignoring trailer block
    if trailers:
        # remove trailer block from end
        body_text_for_paras = "\n".join(body_lines[:len(body_lines)-len(trailer_block)]).strip()
    else:
        body_text_for_paras = "\n".join(body_lines).strip()
    paras = [p.strip() for p in re.split(r"\n\s*\n", body_text_for_paras) if p.strip() and not p.strip().startswith("---")]
    return subject, paras, trailers, body

def check_subject(subject: str):
    violations = []
    if not subject:
        violations.append("Empty subject [CL-10]")
        return violations
    if subject.endswith("."):
        violations.append(f"Subject ends with period: '{subject}' [CL-10]")
    m = SUBJECT_RE.match(subject)
    if not m:
        # allow if x86/ with capital? check
        if not X86_CAP_RE.match(subject):
            violations.append(f"Subject does not match 'subsystem: imperative summary' lowercase: '{subject}' [CL-10]")
        return violations
    summary = m.group("summary")
    if summary and summary[0].isupper() and not X86_CAP_RE.match(subject):
        violations.append(f"Subject summary should be lowercase after colon: '{subject}' [CL-10] (x86/tip exception: capital allowed)")
    # check prevailing prefix would need git history; skip here
    return violations

def check_trailer_pairing(trailers):
    violations = []
    has_fixes = any(t.startswith("Fixes:") for t in trailers)
    has_cc_stable = any("stable@vger.kernel.org" in t for t in trailers)
    if has_fixes and not has_cc_stable:
        violations.append("Has Fixes: but no Cc: stable@vger.kernel.org — pair them [CL-11, changelog-style §1]")
    return violations

def check_paragraph_caps(paras):
    violations = []
    word_counts = [count_words(p) for p in paras if p]
    if not word_counts:
        return violations
    over_50 = sum(1 for c in word_counts if c > 50)
    over_70 = sum(1 for c in word_counts if c > 70)
    # 90% ≤50
    if len(word_counts) >= 2:
        pct_over_50 = over_50 / len(word_counts)
        if pct_over_50 > 0.10:
            violations.append(f"Paragraph cap: {over_50}/{len(word_counts)} paragraphs >50w ({pct_over_50*100:.0f}%) — need ≤10% [CL-12]. Counts: {word_counts}")
    if over_70:
        violations.append(f"Paragraph cap: {over_70} paragraph(s) >70w — never beyond 70 [CL-12]. Counts: {word_counts}")
    # also flag any single para >70 individually
    for i, (p, c) in enumerate(zip(paras, word_counts)):
        if c > 70:
            preview = p[:80].replace("\n"," ")
            violations.append(f"Para {i+1} {c}w >70: '{preview}...' [CL-12]")
    return violations

def check_banned_phrases(body: str):
    violations = []
    for pat, msg in BANNED_PHRASES:
        if re.search(pat, body, re.IGNORECASE if "This patch" not in pat else 0):
            violations.append(msg + f" — matched /{pat}/")
    # em-dash sprinkling: >2 em-dashes
    em_count = len(EM_DASH_RE.findall(body))
    if em_count > 2:
        violations.append(f"Em-dash sprinkling: {em_count} em-dashes — prefer periods/parentheses [CL-13]")
    return violations

def check_internal_identifiers(body: str):
    violations = []
    for pat, msg in INTERNAL_PATTERNS:
        if re.search(pat, body, re.IGNORECASE):
            violations.append(msg + f" — /{pat}/")
    return violations

def check_verbatim_artifact(body: str, subject: str, full_text: str):
    violations = []
    # if mentions KASAN/WARNING/oops/Call Trace but no indented literal block (4-space or tab)
    triggers = ["KASAN", "WARNING:", "BUG:", "Call Trace", "INFO: task hung", "softlockup", "RCU stall", "Kfence", "lockdep"]
    mentions = any(t.lower() in full_text.lower() for t in triggers)
    # indented block: line starting with 4 spaces or tab, and containing relevant
    # 2-space indent is as common as 4 for pasted splats in kernel changelogs
    has_indented = bool(re.search(r"\n(?: {2,}|\t).*(?:KASAN|WARNING|Call Trace|dump_stack|RIP:)", full_text))
    if mentions and not has_indented:
        # heuristic: only flag if bugfix-ish (has Fixes:)
        if "Fixes:" in full_text or "fix" in subject.lower():
            violations.append("Bugfix mentions kernel message (KASAN/WARNING/oops) but no indented verbatim splat block found [CL-15, changelog-style §1 artifact rule]")
    return violations

# R0-9: sentences that explain code or assert a system fact are claims.
# The lint cannot judge truth; it enumerates the sentences you must cite a
# source for. Signal = names code AND states it absolutely, because a
# confident simplification is what hides an unchecked path.
NAMES_CODE = [
    re.compile(r"\b[a-z_][a-z0-9_]*\(\)"),          # foo()
    re.compile(r"->[a-z_]+|\bstruct [a-z_]+"),        # ->field, struct x
    re.compile(r"\b[A-Z][A-Z0-9_]{3,}\b"),            # CONFIG_X, DMA32, PG_Reserved-ish
]
ABSOLUTE_RE = re.compile(
    r"\b(simply|just|merely|always|never|all|only|any|every|necessarily)\b", re.I)

def split_sentences(body: str):
    # drop trailers and indented literal blocks (splats are covered by CL-15)
    kept = [l for l in body.split("\n")
            if not re.match(r"^\s*(Signed-off-by|Cc|Fixes|Assisted-by|Acked-by|"
                            r"Reviewed-by|Tested-by|Link|Reported-by|Suggested-by):", l)
            and not re.match(r"^(?: {2,}|\t)", l)]
    flat = " ".join(kept)
    # protect abbreviations so they do not fake a sentence break
    for abbr in ("e.g.", "i.e.", "etc.", "cf.", "vs.", "Dr.", "approx."):
        flat = flat.replace(abbr, abbr.replace(".", "\x00"))
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p.replace("\x00", ".").strip() for p in parts if len(p.strip()) > 25]

def collect_citation_needed(body: str):
    out = []
    for s in split_sentences(body):
        if any(p.search(s) for p in NAMES_CODE) and ABSOLUTE_RE.search(s):
            out.append(s)
    return out

def lint(text: str):
    subject, paras, trailers, body = parse_commit(text)
    all_violations = []
    all_violations.extend(check_subject(subject))
    all_violations.extend(check_trailer_pairing(trailers))
    all_violations.extend(check_paragraph_caps(paras))
    all_violations.extend(check_banned_phrases(body))
    all_violations.extend(check_internal_identifiers(body))
    all_violations.extend(check_verbatim_artifact(body, subject, text))
    return subject, paras, trailers, all_violations

def main():
    parser = argparse.ArgumentParser(description="lint kernel changelog")
    parser.add_argument("file", nargs="?", help="changelog file")
    parser.add_argument("--stdin", action="store_true", help="read from stdin")
    parser.add_argument("--cite", action="store_true",
                        help="R0-9: list sentences explaining code that need a source named")
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        text = Path(args.file).read_text(errors="replace")
    else:
        parser.print_help()
        sys.exit(2)

    subject, paras, trailers, violations = lint(text)

    print(f"Subject: {subject}")
    print(f"Paragraphs: {len(paras)} Trailer lines: {len(trailers)}")
    if paras:
        print(f"Word counts: {[count_words(p) for p in paras]}")
    print()

    if args.cite:
        _, _, _, body = parse_commit(text)
        needing = collect_citation_needed(body)
        print("R0-9 — name the source for each sentence below "
              "(file:function for behaviour, boot log or /proc for a system fact).")
        print("An absolute in a sentence about code usually marks a path that was not checked.")
        if not needing:
            print("  (none flagged — this does not mean the prose is verified)")
        for i, s in enumerate(needing, 1):
            print(f"  {i}. {s}")
        print()

    if not violations:
        print("PASS — no rule-ID violations detected (heuristic, not complete)")
        sys.exit(0)
    else:
        print(f"FAIL — {len(violations)} potential violation(s):")
        for v in violations:
            print(f"  - {v}")
        sys.exit(1)

if __name__ == "__main__":
    main()
