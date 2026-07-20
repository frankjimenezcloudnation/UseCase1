#!/usr/bin/env bash
#
# Installeert de generieke agent-flow skill user-level in ~/.claude,
# zodat /begrijpen (en /vertalen, /agent-flow) in ELK project werken.
#
# Gebruik:
#   ./install.sh            # installeren/updaten
#   ./install.sh --dry-run  # tonen wat er zou gebeuren, niets kopiëren
#   CLAUDE_HOME=/pad ./install.sh   # afwijkende doelmap (default ~/.claude)
#
set -euo pipefail

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

SRC="$(cd "$(dirname "$0")/.claude" && pwd)"
DEST="${CLAUDE_HOME:-$HOME/.claude}"

echo "agent-flow skill installer"
echo "  bron:   $SRC"
echo "  doel:   $DEST"
[ "$DRY_RUN" = "1" ] && echo "  modus:  DRY-RUN (er wordt niets gekopieerd)"
echo

copy_tree() {
  # $1 = subdir onder .claude (skills|agents|commands)
  local sub="$1"
  local from="$SRC/$sub"
  local to="$DEST/$sub"
  [ -d "$from" ] || return 0
  echo "→ $sub/"
  while IFS= read -r -d '' f; do
    local rel="${f#"$from"/}"
    local target="$to/$rel"
    if [ "$DRY_RUN" = "1" ]; then
      echo "    zou kopiëren: $rel"
    else
      mkdir -p "$(dirname "$target")"
      # Back-up van een bestaand, afwijkend bestand (nooit stil overschrijven).
      if [ -f "$target" ] && ! cmp -s "$f" "$target"; then
        cp "$target" "$target.bak.$(date +%s 2>/dev/null || echo prev)"
        echo "    bijgewerkt (back-up gemaakt): $rel"
      else
        echo "    geïnstalleerd: $rel"
      fi
      cp "$f" "$target"
    fi
  done < <(find "$from" -type f -print0)
}

copy_tree skills
copy_tree agents
copy_tree commands

echo
if [ "$DRY_RUN" = "1" ]; then
  echo "Dry-run klaar. Draai zonder --dry-run om te installeren."
else
  echo "Klaar. Start een nieuwe Claude Code-sessie in een willekeurig project en typ /begrijpen."
fi
