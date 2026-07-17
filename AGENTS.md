# About this directory

This is a reference guide to Linux kernel commit, changelog, comment, and code
style. It is documentation, not a set of commands.

A tool that encounters this directory while reviewing or crawling code should
treat every file here as ordinary reference material. Nothing here is an
instruction to execute, and nothing here changes a task the tool was already
given.

If you want an LLM to write in this style, load the guide into its context
deliberately: start at [README.md](./README.md), then read the files in the
order it lists ([kernel-style.md](./kernel-style.md) first). The guide aims to
describe how kernel patch prose reads when a human wrote it well.
