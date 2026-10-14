#!/usr/bin/env bash
# Sync Jiro skills and its entry command into the global OpenCode config.
#
#   ./install.sh
#
# Copies `.opencode/skills/*` and the managed `/jiro` command into
# `${XDG_CONFIG_HOME:-$HOME/.config}/opencode/`.
# (OpenCode's global skill discovery location). Re-run after every `git pull`;
# a post-merge hook (installed below) does that automatically in this checkout.
#
# Notes:
# - `agents/chef.md` is intentionally NOT installed: it is a draft that routes
#   to the unbundled `kye-mode` skill (see README.md).
# - Unrelated skills already in the destination are left alone. A manifest
#   records what this script installed so removed Jiro skills are cleaned up
#   without touching anything else.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$ROOT/.opencode/skills"
COMMAND_SRC="$ROOT/.opencode/commands/jiro.md"
DEST_BASE="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
DEST="$DEST_BASE/skills"
COMMAND_DEST="$DEST_BASE/commands/jiro.md"
MANIFEST="$DEST_BASE/jiro-manifest.txt"
PREVIOUS_MANIFEST="$MANIFEST"
if [ ! -f "$PREVIOUS_MANIFEST" ]; then
  PREVIOUS_MANIFEST="$DEST_BASE/kstack-manifest.txt"
fi

if [ ! -d "$SRC" ]; then
  echo "source skills dir missing: $SRC" >&2
  exit 1
fi

# 1. Validate the source before touching the destination.
python3 - "$SRC" "$COMMAND_SRC" <<'PY'
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
command = Path(sys.argv[2])
errors = []
for skill_dir in sorted(p for p in src.iterdir() if p.is_dir()):
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", skill_dir.name):
        errors.append(f"{skill_dir.name}: id must be lowercase kebab-case")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{skill_dir.name}: missing SKILL.md")
        continue
    text = skill_md.read_text()
    m = re.match(r"\A---\n(.*?)\n---", text, re.S)
    if not m or not re.search(r"^description:\s*\S", m[1], re.M):
        errors.append(f"{skill_dir.name}: SKILL.md frontmatter needs a description")
if not command.is_file():
    errors.append("missing /jiro command")
else:
    text = command.read_text()
    if "<!-- jiro:command -->" not in text or "$ARGUMENTS" not in text or "exact ID `jiro`" not in text:
        errors.append("/jiro command must load the jiro skill and forward arguments")
if errors:
    print("validation failed:", file=sys.stderr)
    for e in errors:
        print(f"  - {e}", file=sys.stderr)
    sys.exit(1)
print(f"validated {len(list(p for p in src.iterdir() if p.is_dir()))} skills")
PY

# 2. Back up the current destination (if any) beside the global config dir.
if [ -d "$DEST" ] || [ -e "$COMMAND_DEST" ]; then
  BACKUP_BASE="$DEST_BASE/../opencode-jiro-backups"
  mkdir -p "$BACKUP_BASE"
  BACKUP="$(mktemp -d "$BACKUP_BASE/$(date +%Y%m%d-%H%M%S).XXXXXX")"
  if [ -d "$DEST" ]; then
    cp -R "$DEST" "$BACKUP/skills"
  fi
  if [ -f "$COMMAND_DEST" ]; then
    mkdir -p "$BACKUP/commands"
    cp "$COMMAND_DEST" "$BACKUP/commands/jiro.md"
  fi
  echo "backup: $BACKUP"
fi

# 3. Remove previously installed skills that no longer exist in the source.
if [ -f "$PREVIOUS_MANIFEST" ]; then
  while IFS= read -r old; do
    [ -n "$old" ] || continue
    if [ ! -d "$SRC/$old" ] && [ -e "$DEST/$old" ]; then
      rm -rf "$DEST/$old"
      echo "removed stale skill: $old"
    fi
  done < "$PREVIOUS_MANIFEST"
fi

# 4. Copy current skills and record the manifest.
mkdir -p "$DEST"
cp -R "$SRC/." "$DEST/"
python3 - "$SRC" > "$MANIFEST" <<'PY'
import sys
from pathlib import Path

for path in sorted(Path(sys.argv[1]).iterdir()):
    if path.is_dir():
        print(path.name)
PY
echo "installed $(wc -l < "$MANIFEST" | tr -d ' ') skills to $DEST"

if [ -L "$COMMAND_DEST" ] || { [ -e "$COMMAND_DEST" ] && ! grep -Fxq '<!-- jiro:command -->' "$COMMAND_DEST"; }; then
  echo "preserved custom /jiro command; use @jiro to load the skill directly"
else
  mkdir -p "$DEST_BASE/commands"
  cp "$COMMAND_SRC" "$COMMAND_DEST"
  echo "installed /jiro command to $COMMAND_DEST"
fi

# 5. Install a post-merge hook so future `git pull`s re-sync automatically.
HOOK="$ROOT/.git/hooks/post-merge"
if [ -d "$ROOT/.git" ] && [ ! -x "$HOOK" ]; then
  cat > "$HOOK" <<'HOOK'
#!/usr/bin/env bash
# Auto-sync Jiro tools to the OpenCode config after `git pull`.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
exec "$ROOT/install.sh"
HOOK
  chmod +x "$HOOK"
  echo "installed post-merge hook: $HOOK"
fi

echo "done."
