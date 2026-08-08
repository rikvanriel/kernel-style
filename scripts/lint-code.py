#!/usr/bin/env python3
"""
lint-code.py — machine-checkable subset of the code-side rules.

The diff-side companion to lint-changelog.py. Checks a commit or a range for:
- CC-12 kerneldoc scaffolding on an internal static (@param references under
  either marker)
- CS-10 helper placement: a comment block left describing a different function
  than the one it now sits above
- CS-11 function length: a function this commit touched that is still over the
  cap afterwards
- CL-30 safety paragraph: an advisory note when a commit changes locking with no
  "should be safe" in its message (the message-only half lives in
  lint-changelog.py, one home per rule)
- R0-7 carried-forward claims: with --against, a sentence containing a measured
  quantity that survived a reword onto a new base

Deliberately not implemented, with reasons, so nobody adds them by reflex:
- CS-12 guard()/__free() preference. goto+unlock is idiomatic in most of the
  tree and guard() does not fit conditional or re-taken locks, so the check
  fires far more often than it is right.
- CL-32 per-patch benchmark tables. "Several patches touch one function and
  only the last has a table" is equally true of a correct prep-then-optimise
  pair, so it belongs in a series-level advisory, not a per-patch gate.

Overlap with checkpatch.pl is avoided: commit-hash citation (GIT_COMMIT_ID,
BAD_FIXES_TAG) and Assisted-by shape are already enforced there.

Usage:
  ./scripts/lint-code.py <sha>
  ./scripts/lint-code.py <base>..<head>
  ./scripts/lint-code.py --repo /path/to/linux <base>..<head>
  ./scripts/lint-code.py --against <old-ref> <base>..<head>   # adds R0-7

Exit 0 = pass, 1 = findings, 2 = error.
"""

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

CAP = 40

LOCK_TOUCHED = re.compile(
    r"\b(spin_lock|spin_unlock|mutex_lock|mutex_unlock|read_lock|write_lock|"
    r"down_read|down_write|up_read|up_write|rcu_read_lock|rcu_read_unlock|"
    r"pte_unmap_unlock|pte_offset_map_lock|raw_spin_lock|local_irq_save)\b")

# a quantity a reviewer could go and re-measure, as opposed to any digit
MEASURED = re.compile(
    r"\b\d[\d,.]*\s*(us|ms|ns|s|%|x|MB/s|GB/s|KB|MB|GB|iops|cycles)\b", re.I)

DOC_NAME = re.compile(r"^\s*\*\s*([a-z_][a-z0-9_]*)\(?\)?\s+-\s")
PARAM_REF = re.compile(r"^\s*\*.*@[a-z_][a-z0-9_]*")
FUNC_DEF = re.compile(r"^(static\s+)?[A-Za-z_][A-Za-z0-9_ *]*[ *]([a-z_][a-z0-9_]*)\s*\(")


def load_function_lengths():
    """Reuse series-function-growth.py's parser rather than writing a second one.

    Its docstring documents the multi-line-declaration trap that a naive regex
    falls into; a second implementation would fall into it again.
    """
    path = Path(__file__).with_name("series-function-growth.py")
    spec = importlib.util.spec_from_file_location("sfg", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.function_lengths


def git(repo, *args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          cwd=repo).stdout


def added_lines(repo, sha, path):
    """Added lines of one file, as (line_text,) in diff order."""
    out = git(repo, "show", "--format=", "--unified=0", sha, "--", path)
    return [l[1:] for l in out.split("\n")
            if l.startswith("+") and not l.startswith("+++")]


def added_blocks(repo, sha, path):
    """Contiguous runs of added lines, with more context than --unified=0."""
    out = git(repo, "show", "--format=", "--unified=6", sha, "--", path)
    blocks, cur = [], []
    for l in out.split("\n"):
        if l.startswith("@@"):
            if cur:
                blocks.append(cur)
            cur = []
        elif l and not l.startswith(("+++", "---", "diff ", "index ")):
            cur.append(l)
    if cur:
        blocks.append(cur)
    return blocks


def check_scaffolding(repo, sha, path):
    """CC-12: @param references in a comment block above a static function."""
    findings = []
    for block in added_blocks(repo, sha, path):
        comment, in_comment = [], False
        for raw in block:
            text = raw[1:] if raw and raw[0] in "+- " else raw
            added = raw.startswith("+")
            if text.strip().startswith("/*"):
                comment, in_comment = [(text, added)], True
                continue
            if in_comment:
                comment.append((text, added))
                if "*/" in text:
                    in_comment = False
                continue
            if comment and FUNC_DEF.match(text) and "static" in text:
                if any(PARAM_REF.match(t) and a for t, a in comment):
                    name = FUNC_DEF.match(text).group(2)
                    findings.append(
                        f"{path}: comment above static {name}() carries @param "
                        f"scaffolding — a plain why-block restates less [CC-12]")
            comment = []
    return findings


def check_helper_placement(repo, sha, path):
    """CS-10: comment block naming a function other than the one below it."""
    findings = []
    for block in added_blocks(repo, sha, path):
        documented, in_comment, first_content = None, False, True
        for raw in block:
            text = raw[1:] if raw and raw[0] in "+- " else raw
            if text.strip().startswith(("/*", "/**")):
                documented, in_comment, first_content = None, True, True
                continue
            if in_comment:
                # only the block's first content line can be a kerneldoc
                # "name - summary"; a mid-block sentence that happens to open
                # with a function name is prose, not a subject
                if documented is None and first_content:
                    m = DOC_NAME.match(text)
                    documented = m.group(1) if m else ""
                    first_content = False
                if "*/" in text:
                    in_comment = False
                continue
            m = FUNC_DEF.match(text)
            if m:
                if documented and documented != m.group(2):
                    findings.append(
                        f"{path}: comment documents {documented}() but sits above "
                        f"{m.group(2)}() — helper inserted into the gap [CS-10]")
                documented = None
    return findings


def check_function_length(repo, sha, path, flen):
    """CS-11: a function this commit touched that is still over the cap."""
    findings = []
    after = flen(git(repo, "show", f"{sha}:{path}"))
    before = flen(git(repo, "show", f"{sha}~1:{path}"))
    touched = set()
    for l in git(repo, "show", "--format=", "--unified=0", sha, "--", path).split("\n"):
        if l.startswith("@@"):
            m = re.search(r"@@.*@@\s*.*?\b([a-z_][a-z0-9_]*)\s*\(", l)
            if m:
                touched.add(m.group(1))
    notes = []
    for name in sorted(touched):
        end = after.get(name)
        if not end or end <= CAP:
            continue
        start = before.get(name, 0)
        if end > start:
            findings.append(
                f"{path}: {name}() grew {start}->{end} lines, cap is {CAP} — "
                f"extract the addition here, not later [CS-11; split by theme, CS-13]")
        else:
            notes.append(
                f"{path}: {name}() was already {end} lines and this commit touched "
                f"it — splitting pre-existing debt is still in scope [CS-11]")
    return findings, notes


def note_safety_paragraph(repo, sha, message):
    """CL-30 advisory: locking primitives in the diff, no hedged paragraph.

    A note rather than a finding: moved or re-indented lock calls trip this as
    readily as a real change of lock scope, and only a reader can tell which.
    """
    if "should be safe" in message.lower():
        return []
    diff = git(repo, "show", "--format=", sha)
    if any(LOCK_TOUCHED.search(l) for l in diff.split("\n") if l.startswith("+")):
        return ["diff touches locking — if lock scope changed, add a \"should be "
                "safe because...\" paragraph naming what prevents reuse [CL-30]"]
    return []


def check_carried_claims(repo, sha, old_ref):
    """R0-7: a measured quantity that survived a reword onto a new base."""
    new = git(repo, "log", "-1", "--format=%B", sha)
    old = git(repo, "log", "-1", "--format=%B", old_ref)
    if not old:
        return []
    old_lines = set(l.strip() for l in old.split("\n") if l.strip())
    findings = []
    for line in new.split("\n"):
        s = line.strip()
        if s and s in old_lines and MEASURED.search(s):
            findings.append(
                f"retained from {old_ref[:12]}: \"{s[:60]}\" — re-measure on this "
                f"base or drop it [R0-7]")
    return findings


def review(repo, sha, old_ref, flen):
    subject = git(repo, "log", "-1", "--format=%s", sha).strip()
    message = git(repo, "log", "-1", "--format=%B", sha)
    files = [f for f in git(repo, "show", "--format=", "--name-only", sha).split("\n")
             if f.endswith((".c", ".h"))]
    findings, notes = [], []
    for path in files:
        findings += check_scaffolding(repo, sha, path)
        findings += check_helper_placement(repo, sha, path)
        f, n = check_function_length(repo, sha, path, flen)
        findings += f
        notes += n
    notes += note_safety_paragraph(repo, sha, message)
    if old_ref:
        findings += check_carried_claims(repo, sha, old_ref)
    return subject, findings, notes


def main():
    ap = argparse.ArgumentParser(description="lint kernel code changes")
    ap.add_argument("rev", help="a sha, or base..head")
    ap.add_argument("--repo", default=".", help="repository (default: cwd)")
    ap.add_argument("--against", help="R0-7: previous version of the same commit")
    args = ap.parse_args()

    flen = load_function_lengths()
    if ".." in args.rev:
        shas = git(args.repo, "rev-list", "--reverse", args.rev).split()
    else:
        shas = [args.rev]
    if not shas:
        print("no commits in range", file=sys.stderr)
        return 2

    total = 0
    for sha in shas:
        subject, findings, notes = review(args.repo, sha, args.against, flen)
        print(f"{sha[:12]} {subject}")
        for f in findings:
            print(f"    {f}")
        for n in notes:
            print(f"    note: {n}")
        total += len(findings)
    print()
    if total:
        print(f"{total} finding(s) — heuristic, not complete")
        return 1
    print("PASS — no findings (heuristic, not complete)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
