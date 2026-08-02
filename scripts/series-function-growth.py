#!/usr/bin/env python3
"""
series-function-growth.py — attribute function length growth to a patch series.

The 40-line cap (kernel-style.md §3, CS-11) is a snapshot check on one patch.
A series can push a function far past it without any single patch looking
wrong, because each patch only adds "one more case" to something already long.
This measures what the series as a whole did, and names the patches that did it.

Usage:
  ./scripts/series-function-growth.py <base-ref> <last-ref> [--cap N]

Report a function when the series added more than one whole permitted
function's worth (> cap) to it, and it ends over the cap. Growth attribution
matters: a function already long upstream that the series barely touches is
not the series' problem, and flagging it only trains people to ignore output.

Exit 0 always; this reports, it does not gate.
"""
import argparse
import re
import subprocess
import sys

DEF = re.compile(r"^(static\s+)?[A-Za-z_][A-Za-z0-9_ *]*[ *]([a-z_][a-z0-9_]*)\s*\(")


def git(repo, *args):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          cwd=repo).stdout


def function_lengths(src):
    """Map function name -> line count, counting only real definitions.

    A prototype's ';' can sit on a continuation line, so deciding
    declaration-vs-definition from the first line alone mis-parses and
    silently swallows whatever follows it -- which hides exactly the
    long functions this script exists to find. Read forward to whichever
    comes first, the ';' or the opening '{', then brace-match the body.
    """
    out, lines, i = {}, src.splitlines(), 0
    while i < len(lines):
        m = DEF.match(lines[i])
        if not m:
            i += 1
            continue
        j, isdef = i, False
        while j < len(lines):
            stripped = lines[j].rstrip()
            if stripped.endswith(";"):
                break
            if stripped.endswith("{"):
                isdef = True
                break
            j += 1
            if j - i > 12:
                break
        if not isdef:
            i = j + 1
            continue
        depth, k, n = 0, j, 0
        while k < len(lines):
            depth += lines[k].count("{") - lines[k].count("}")
            n += 1
            if depth == 0:
                break
            k += 1
        name = m.group(2)
        out[name] = max(out.get(name, 0), n + (j - i))
        i = k + 1
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base")
    ap.add_argument("last")
    ap.add_argument("--cap", type=int, default=40)
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    repo, cap = args.repo, args.cap

    shas = git(repo, "log", "--format=%H", "--reverse",
               f"{args.base}..{args.last}").split()
    files = [f for f in git(repo, "diff", "--name-only",
                            f"{args.base}..{args.last}").split()
             if f.endswith(".c")]

    flagged = []
    for f in files:
        before = function_lengths(git(repo, "show", f"{args.base}:{f}"))
        after = function_lengths(git(repo, "show", f"{args.last}:{f}"))
        for fn, end in after.items():
            start = before.get(fn, 0)
            if end > cap and end - start > cap:
                flagged.append((end - start, end, start, fn, f))
    flagged.sort(reverse=True)

    if not flagged:
        print(f"No function grown by more than {cap} lines by this series.")
        return 0

    print(f"Functions this series grew by more than {cap} lines, now over {cap}.")
    print("Extract your addition as a named helper in the patch that adds it;")
    print("doing it later means re-deriving every patch that touched it since.\n")
    for grew, end, start, fn, f in flagged:
        origin = "new in series" if start == 0 else f"{start} at base"
        print(f"  {fn}  ({f})")
        print(f"      {origin} -> {end} lines  ({grew:+})")
        prev, attrib = start, []
        for i, s in enumerate(shas, 1):
            cur = function_lengths(git(repo, "show", f"{s}:{f}")).get(fn, prev)
            if cur != prev:
                attrib.append(f"p{i} {cur - prev:+}")
            prev = cur
        if attrib:
            print(f"      grown by: {', '.join(attrib)}")
    print(f"\n{len(flagged)} function(s) flagged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
