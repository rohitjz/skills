#!/usr/bin/env bash
# Install skills from this repo into your agent's skills folder.
# Agent hosts look for <skills-dir>/<name>/SKILL.md one level deep, so the
# category folders are flattened on install.
#
#   ./install.sh                      # all skills -> ~/.claude/skills
#   ./install.sh --target copilot     # all skills -> ~/.copilot/skills
#   ./install.sh --category design    # one category
#   ./install.sh sketchbook-ui council # specific skills
#   ./install.sh --link               # symlink instead of copy (stays in sync with git pull)
#   ./install.sh --list               # show what's available
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/skills"; MODE=copy; CATEGORY=""; LIST=0; NAMES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --target) case "$2" in claude) DEST="$HOME/.claude/skills";; copilot) DEST="$HOME/.copilot/skills";; *) DEST="$2";; esac; shift 2;;
    --category) CATEGORY="$2"; shift 2;;
    --link) MODE=link; shift;;
    --list) LIST=1; shift;;
    -h|--help) sed -n '2,12p' "$0"; exit 0;;
    *) NAMES+=("$1"); shift;;
  esac
done
found=0
for skill in "$ROOT"/skills/*/*/SKILL.md; do
  dir="$(dirname "$skill")"; name="$(basename "$dir")"; cat="$(basename "$(dirname "$dir")")"
  [ -n "$CATEGORY" ] && [ "$cat" != "$CATEGORY" ] && continue
  if [ ${#NAMES[@]} -gt 0 ]; then
    match=0; for n in "${NAMES[@]}"; do [ "$n" = "$name" ] && match=1; done
    [ $match -eq 0 ] && continue
  fi
  found=$((found+1))
  if [ $LIST -eq 1 ]; then printf '%-24s %s\n' "$cat" "$name"; continue; fi
  mkdir -p "$DEST"; rm -rf "${DEST:?}/$name"
  if [ $MODE = link ]; then ln -s "$dir" "$DEST/$name"; else cp -R "$dir" "$DEST/$name"; fi
  echo "installed $cat/$name -> $DEST/$name"
done
[ $found -eq 0 ] && { echo "no matching skills" >&2; exit 1; }
exit 0
