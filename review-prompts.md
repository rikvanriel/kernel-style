---
name: review-prompts
description: What /kreview (referenced in kernel-style.md and changelog-style.md) actually is and how to set it up — an external AI-assisted review slash command from the review-prompts repository, not a built-in.
metadata:
  type: reference
---
# The `/kreview` command comes from an external repository

`/kreview` (referenced in kernel-style.md §0 and changelog-style.md §0) is not a
built-in command. It comes from the external
[review-prompts](https://github.com/masoncl/review-prompts) repository — AI-assisted
code review prompts for Linux kernel, systemd, and iproute development.

## Setup (one-time, per agent/machine)
1. Clone it: `git clone https://github.com/masoncl/review-prompts`
2. From the clone's root, install the kernel prompts for your agent:
   ```
   ./setup.sh <agent> kernel
   ```
   `<agent>` is one of `claude`, `codex`, `opencode`, `gemini`. This installs the
   kernel skill (auto-loads when you're working in a kernel tree) and the slash
   commands (`/kreview`, `/kseries`, `/kdebug`, `/kverify`) into your agent's
   command directory (e.g. `~/.claude/commands/` for Claude).
3. **Don't move the clone after installing** — the installed skill and commands
   reference its path directly.

## Usage
- **Run `/kreview` against the specific commit/diff you're reviewing before
  drafting the changelog.** This is what "Run `/kreview`... then write" in
  kernel-style.md §0 / changelog-style.md §0 means: fold its findings in as part
  of the factual-integrity pass, not as a separate optional step.
- `/kseries` reviews an entire patch series (a git range) commit-by-commit — see
  [patch-series.md](./patch-series.md) for multi-patch structure.
- `/kdebug` (crash/warning triage) and `/kverify` (false-positive checking) are
  useful on demand but not part of the standard review gate.

## Optional: semcode
review-prompts works best paired with
[semcode](https://github.com/facebookexperimental/semcode) for fast semantic
code navigation over the kernel tree (indexed definitions/call graphs) — not
required to use `/kreview`, but reduces time spent grepping.
