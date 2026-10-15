#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUN="${BUN_BIN:-$(command -v bun || true)}"
if [ -z "$BUN" ] && [ -x "$HOME/.bun/bin/bun" ]; then
  BUN="$HOME/.bun/bin/bun"
fi
if [ -z "$BUN" ]; then
  echo "Bun is required. Install Bun and run bun install in $ROOT." >&2
  exit 1
fi
exec "$BUN" run "$ROOT/scripts/sync-opencode.ts" "$ROOT" "$@"
