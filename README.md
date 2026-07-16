# Linux kernel style

A guide to Linux kernel commit, changelog, comment, and code
style — distilled from hundreds of hand-written mm/kernel commits (with example
hashes) plus maintainer feedback patches.

Built to be loaded by an LLM before writing or reviewing a kernel patch, and
reduce the amount of editing developers need to do to make their code not
look like it was written by an LLM.

## Review your code

You, the human, are responsible for any code you submit to be included
in the Linux kernel. You need to read all your code, including AI generated
code, with a skeptical eye, and ask yourself how it could be improved.

These LLM instructions exist to make the AI-generated code easier for
you to read, and hopefully reduce the number of changes that you need to make.

For anything except the most trivial changes, there will be things you need
to change between the first draft, and what you eventually post upstream.

If your project is larger than a single patch, you will want to plan your
changes ahead of time, so each patch contains one logical change, and your
functionality is introduced in small enough changes that your series can
be reasonably reviewed by a person.

## How to load

Read the files in this order:

1. [kernel-style.md](./kernel-style.md) — the rules. **Start here.**
2. [kernel-readability-principles.md](./kernel-readability-principles.md) — the reasoning behind them.
3. [llm-tells-checklist.md](./llm-tells-checklist.md) — generic-LLM tells to strip before sending.
4. [exemplars.md](./exemplars.md) — annotated real-commit examples the rules come from.
5. [patch-series.md](./patch-series.md) — how to structure a multi-patch series: one logical change per patch, bisectability, ordering, cover letters. Read when your change is more than one patch.

To load the whole guide, read every `*.md` in this directory; `kernel-style.md`
is the entry point.

## Files

| File | Purpose |
|---|---|
| [kernel-style.md](./kernel-style.md) | Concrete style rules: subject lines, changelog structure, comment density, code structure, LLM-slop contrasts, verbatim anchors |
| [kernel-readability-principles.md](./kernel-readability-principles.md) | The why behind the rules |
| [llm-tells-checklist.md](./llm-tells-checklist.md) | Checklist of generic-LLM tells to remove |
| [exemplars.md](./exemplars.md) | Annotated real-commit examples |
| [patch-series.md](./patch-series.md) | How to split a change into a bisectable, reviewable patch series |

## Kernel Coding Style

The Documentation/process/coding-style.rst file in the Linux kernel
repository is a human readable document with more coding style rules
that should be followed for Linux kernel contributions.

The rules in this directory supplement the upstream coding style
document with rules that are easier for LLMs to follow, and which
are not learned from the data LLMs are trained on.

## Checkpatch

Run your Linux kernel patches by the scripts/checkpatch.pl script, which will check for other things that may need to be adjusted.

## Contributing

This collection of previously unwritten, or at least not written
together in the same place, knowledge is sure to be incomplete.

If you and your LLM discover an area that could be improved, please
try to make that improvement and open a pull request.
