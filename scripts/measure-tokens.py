#!/usr/bin/env python3
"""
measure-tokens.py — approximate token count for kernel-style hot set.

Uses wc -w for words and chars//4 heuristic for tokens, matching the methodology
documented in CONTRIBUTING.md §6 until tiktoken is available in CI image.
If tiktoken is installed, uses cl100k_base encoding for exact counts.

Usage:
  python3 scripts/measure-tokens.py [--json]
Outputs human-readable table by default, JSON with --json for CI parsing.
"""
import pathlib, sys, json, os

try:
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    def tok(s): return len(enc.encode(s))
    method = "tiktoken cl100k_base"
except Exception:
    def tok(s): return len(s)//4
    method = "chars//4 heuristic"

base = pathlib.Path(__file__).resolve().parent.parent
filesets = {
    "phase1_always_hot": ["kernel-style.md","kernel-readability-principles.md","llm-tells-checklist.md"],
    "phase2_review_add": ["exemplars.md"],
    "phase3_changelog_add": ["changelog-style.md"],
    "patch_series_on_demand": ["patch-series.md"],
}

def measure_list(flist):
    total_w=0; total_c=0; total_t=0
    for fn in flist:
        p=base/fn
        if not p.exists(): continue
        txt=p.read_text(errors='ignore')
        total_w += len(txt.split())
        total_c += len(txt)
        total_t += tok(txt)
    return total_w, total_c, total_t

phase1 = measure_list(filesets["phase1_always_hot"])
phase2_add = measure_list(filesets["phase2_review_add"])
phase3_add = measure_list(filesets["changelog-style.md"] if False else filesets["phase3_changelog_add"])
# compute cumulative
p1_w,p1_c,p1_t = phase1
p2_w,p2_c,p2_t = measure_list(filesets["phase1_always_hot"]+filesets["phase2_review_add"])
p3_w,p3_c,p3_t = measure_list(filesets["phase1_always_hot"]+filesets["phase2_review_add"]+filesets["phase3_changelog_add"])
p3m_w,p3m_c,p3m_t = measure_list(filesets["phase1_always_hot"]+filesets["phase2_review_add"]+filesets["phase3_changelog_add"]+filesets["patch_series_on_demand"])

out = {
 "method": method,
 "phase1_always_hot": {"words":p1_w,"tokens":p1_t},
 "phase2_review": {"words":p2_w,"tokens":p2_t},
 "phase3_changelog_single": {"words":p3_w,"tokens":p3_t},
 "phase3_multi": {"words":p3m_w,"tokens":p3m_t},
}
if "--json" in sys.argv:
    print(json.dumps(out,indent=2))
else:
    print(f"method: {method}")
    for k in ["phase1_always_hot","phase2_review","phase3_changelog_single","phase3_multi"]:
        v=out[k]; print(f"{k:30} {v['words']:5} words  ~{v['tokens']} tok")
