#!/usr/bin/env bash
# install-skill.sh — install kernel-style repo skills into agent homes.
# No auto-install — requires --install and a confirmation prompt.
# Usage:
#   ./scripts/install-skill.sh --list
#   ./scripts/install-skill.sh --install kernel-style            # live pointer (default)
#   ./scripts/install-skill.sh --install all --mode snapshot    # self-contained copy
#   ./scripts/install-skill.sh --check                           # report drifted installs
#   ./scripts/install-skill.sh --update                          # refresh snapshot copies
#
# Modes:
#   live     — tiny generated SKILL.md pointing at this checkout. Always
#              latest automatically. Needs the checkout present at load time.
#   snapshot — full copy of the repo (git archive) under the skill dir plus
#              the canonical SKILL.md on top. Works without the checkout;
#              refresh with --update.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_DIR="$REPO/skills"
MODE="live"

agent_targets() {
  for base in "$HOME/.claude/skills" "$HOME/.hermes/skills" "$HOME/.agents/skills" "$HOME/.config/opencode/skills"; do
    if [ -d "$(dirname "$base")" ] || [ -d "$base" ]; then
      printf '%s\n' "$base"
    fi
  done
}

list_skills() {
  echo "## Detected agent homes"
  agent_targets | sed 's/^/ - /'
  echo ""
  echo "## Available skills (from $SKILLS_DIR)"
  for d in "$SKILLS_DIR"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    desc=$(grep -m1 '^description:' "$d/SKILL.md" | sed 's/^description: *//' | head -c 140)
    echo " - $(basename "$d") — $desc"
  done
}

repo_head() { git -C "$REPO" rev-parse HEAD 2>/dev/null || echo "uncommitted"; }

write_live_shim() {  # $1 = dest SKILL.md
  local dest="$1"
  # The skills/ dir may not exist yet (e.g. a fresh ~/.agents or opencode
  # home) — create it rather than failing on the redirect below.
  mkdir -p "$(dirname "$dest")"
  # The description below mirrors the canonical SKILL.md trigger wording
  # ("Use when ..." trigger-first), so the installed skill routes on the
  # same load conditions as the repo copy. Keep in sync on wording changes.
  local desc
  desc=$(grep -m1 '^description:' "$SKILLS_DIR/kernel-style/SKILL.md" | sed 's/^description: *//')
  cat > "$dest" <<EOF
---
name: kernel-style
description: $desc Live pointer, always latest.
version: 1.0.0
author: kernel-style contributors
license: CC-BY-4.0
---

# Kernel Style — live pointer

Canonical skill (always latest): $REPO/skills/kernel-style/SKILL.md — read it and follow it.

Rule files and loader live at the checkout root: $REPO
Get exact load commands per phase from: \`cd $REPO && ./scripts/phases.py --phase N [--bug-class race|perf|syzkaller]\`
EOF
  echo "Installed live pointer $dest -> $REPO"
}

install_snapshot() {  # $1 = dest dir
  local dest="$1"
  mkdir -p "$dest"
  if git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
    git -C "$REPO" archive HEAD | tar -x -C "$dest"
  else
    tar --exclude=.git -cf - -C "$REPO" . | tar -x -C "$dest"
  fi
  cp "$dest/skills/kernel-style/SKILL.md" "$dest/SKILL.md"
  repo_head > "$dest/.upstream-version"
  echo "Installed snapshot $dest (@ $(cat "$dest/.upstream-version" | head -c 12))"
}

resolve_list() {
  if [ "$1" = "all" ]; then
    for d in "$SKILLS_DIR"/*/; do [ -f "$d/SKILL.md" ] && basename "$d"; done
  else
    tr ',' '\n' <<< "$1"
  fi
}

do_install() {  # $1 = csv|all
  local s t targets=()
  while read -r t; do targets+=("$t"); done < <(agent_targets)
  if [ ${#targets[@]} -eq 0 ]; then
    echo "No agent homes found. Known locations (created on confirm):"
    for base in "$HOME/.claude/skills" "$HOME/.hermes/skills" "$HOME/.agents/skills" "$HOME/.config/opencode/skills"; do
      echo " - $base"
    done
    read -p "Create them and continue? (y/N) " -r
    [[ $REPLY =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
    for base in "$HOME/.claude/skills" "$HOME/.hermes/skills" "$HOME/.agents/skills" "$HOME/.config/opencode/skills"; do
      mkdir -p "$base" && targets+=("$base")
    done
  fi
  echo "## Skills: $(resolve_list "$1" | tr '\n' ' ')"
  echo "## Mode: $MODE"
  echo "## Targets: ${targets[*]}"
  read -p "Proceed? (y/N) " -r
  [[ $REPLY =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
  while read -r s; do
    [ -f "$SKILLS_DIR/$s/SKILL.md" ] || { echo "SKIP $s — not found"; continue; }
    for t in "${targets[@]}"; do
      if [ -f "$t/$s/SKILL.md" ] && ! grep -q "live pointer" "$t/$s/SKILL.md" 2>/dev/null; then
        # Never silently overwrite a foreign skill that owns the trigger name.
        if ! cmp -s "$t/$s/SKILL.md" "$SKILLS_DIR/$s/SKILL.md"; then
          echo "SKIP $t/$s — foreign SKILL.md owns that name; rename it first"
          continue
        fi
      fi
      if [ "$MODE" = "snapshot" ]; then
        install_snapshot "$t/$s"
      else
        write_live_shim "$t/$s/SKILL.md"
      fi
    done
  done < <(resolve_list "$1")
}

do_check() {
  local rc=0 s t
  for d in "$SKILLS_DIR"/*/; do
    [ -f "$d/SKILL.md" ] || continue
    s="$(basename "$d")"
    while read -r t; do
      if [ ! -f "$t/$s/SKILL.md" ]; then
        echo " - $s @ $t: MISSING"; rc=1
      elif grep -q "live pointer" "$t/$s/SKILL.md" 2>/dev/null; then
        echo " - $s @ $t: live -> $REPO (@ $(repo_head | head -c 12))"
      elif [ -f "$t/$s/.upstream-version" ]; then
        if [ "$(cat "$t/$s/.upstream-version")" = "$(repo_head)" ]; then
          echo " - $s @ $t: snapshot current"
        else
          echo " - $s @ $t: snapshot STALE (run --update)"; rc=1
        fi
      else
        echo " - $s @ $t: FOREIGN (not installed by this script)"; rc=1
      fi
    done < <(agent_targets)
  done
  return $rc
}

do_update() {
  local s t
  while read -r s; do
    while read -r t; do
      if [ -f "$t/$s/.upstream-version" ]; then
        rm -rf "$t/$s"
        install_snapshot "$t/$s"
      elif [ -f "$t/$s/SKILL.md" ]; then
        echo " - $s @ $t: live pointer, nothing to do"
      fi
    done < <(agent_targets)
  done < <(resolve_list "all")
}

for a in "${@:2}"; do
  case "$a" in --mode) ;; live|snapshot) MODE="$a" ;; esac
done
# accept '--mode X' in either order
prev=""
for a in "$@"; do
  [ "$prev" = "--mode" ] && MODE="$a"
  prev="$a"
done

case "${1:-}" in
  --list|--ls) list_skills ;;
  --install) do_install "${2:-}" ;;
  --check) do_check ;;
  --update) do_update ;;
  *) echo "Usage: $0 --list | --install <name|all> [--mode live|snapshot] | --check | --update"; list_skills ;;
esac
