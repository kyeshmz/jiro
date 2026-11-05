#!/usr/bin/env bash
# One unattended dreaming pass over recent OpenCode sessions.
# See the opencode-memory skill for setup. Settings via environment:
#   OPENCODE_CONFIG_DIR  config folder (default ~/.config/opencode)
#   DREAM_MODEL          model for the dream run, provider/model#variant (optional)
#   DREAM_PARENT_SESSION run the dream as a child of this session ID, so it stays
#                        out of the top-level session list (optional)
#   DREAM_REPORT_SESSION post the summary into this session as a queued message,
#                        e.g. a personal-assistant session (optional)
#   DREAM_NOTIFY         command that receives the summary as its last argument (optional)
#   DREAM_WINDOW_HOURS   window for the first run (default 24)
#   DREAM_PROMPT         prompt template (default: next to this script, then the skill)
set -euo pipefail

CONFIG_DIR="${OPENCODE_CONFIG_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/opencode}"
MEMORY_DIR="$CONFIG_DIR/memory"
DREAMS_DIR="$MEMORY_DIR/dreams"
STATE_FILE="$MEMORY_DIR/.dream-state"
LOCK_DIR="$MEMORY_DIR/.dream.lock"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find_prompt() {
  for p in "${DREAM_PROMPT:-}" "$SCRIPT_DIR/dream-prompt.md" \
    "$SCRIPT_DIR/../references/dream-prompt.md" \
    "$CONFIG_DIR/skills/opencode-memory/references/dream-prompt.md"; do
    [ -n "$p" ] && [ -f "$p" ] && { echo "$p"; return; }
  done
  echo "dream: prompt template not found" >&2
  exit 1
}

notify() {
  if [ -n "${DREAM_REPORT_SESSION:-}" ]; then
    local body
    body="$(python3 -c 'import json,sys;print(json.dumps({"text":sys.argv[1],"description":sys.argv[2],"delivery":"queue","resume":True}))' "$1" "Dream $DATE")"
    opencode api POST "/api/session/$DREAM_REPORT_SESSION/synthetic" --data "$body" >/dev/null 2>&1 ||
      echo "dream: posting to $DREAM_REPORT_SESSION failed" >&2
  fi
  [ -n "${DREAM_NOTIFY:-}" ] || return 0
  sh -c "$DREAM_NOTIFY \"\$1\"" dream "$1" || echo "dream: notify failed" >&2
}

git -C "$CONFIG_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "dream: $CONFIG_DIR is not a git repo (run step 1 of the skill first)" >&2
  exit 1
}
mkdir -p "$DREAMS_DIR"
mkdir "$LOCK_DIR" 2>/dev/null || { echo "dream: another run holds $LOCK_DIR" >&2; exit 0; }
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

DATE="$(date +%F)"
REPORT="$DREAMS_DIR/$DATE.md"
[ -e "$REPORT" ] && REPORT="$DREAMS_DIR/$DATE-$(date +%H%M).md"
LOG="${REPORT%.md}.log"
NOW_S="$(date +%s)"
NOW_MS=$((NOW_S * 1000))
if [ -s "$STATE_FILE" ]; then
  SINCE_MS="$(cat "$STATE_FILE")"
else
  SINCE_MS=$(((NOW_S - ${DREAM_WINDOW_HOURS:-24} * 3600) * 1000))
fi
iso() { python3 -c 'import sys,datetime;print(datetime.datetime.fromtimestamp(int(sys.argv[1])/1000).astimezone().isoformat(timespec="minutes"))' "$1"; }
SINCE_ISO="$(iso "$SINCE_MS")"
NOW_ISO="$(iso "$NOW_MS")"

# Rotate the inbox first so sessions that append during the run start a new one.
INBOX="$DREAMS_DIR/$(basename "${REPORT%.md}")-inbox.md"
if [ -s "$MEMORY_DIR/inbox.md" ]; then mv "$MEMORY_DIR/inbox.md" "$INBOX"; else : >"$INBOX"; fi
touch "$MEMORY_DIR/inbox.md"

# Files outside memory/ that are clean now must still be clean after the run.
dirty_outside() { git -C "$CONFIG_DIR" status --porcelain=v1 --untracked-files=no | grep -v ' memory/' | cut -c4- || true; }
BEFORE="$(dirty_outside)"

export SINCE_ISO NOW_ISO SINCE_MS NOW_MS CONFIG_DIR MEMORY_DIR DATE
export INBOX_FILE="$INBOX" REPORT_FILE="$REPORT"
PROMPT="$(python3 -c '
import os, sys
text = open(sys.argv[1]).read()
for k in ["SINCE_ISO", "NOW_ISO", "SINCE_MS", "NOW_MS", "CONFIG_DIR",
          "MEMORY_DIR", "INBOX_FILE", "REPORT_FILE", "DATE"]:
    text = text.replace("{{" + k + "}}", os.environ[k])
print(text)
' "$(find_prompt)")"

RUN_ARGS=(--format json --auto)
[ -n "${DREAM_MODEL:-}" ] && RUN_ARGS+=(--model "$DREAM_MODEL")
cd "$CONFIG_DIR"
SESSION_ID=""
if [ -n "${DREAM_PARENT_SESSION:-}" ]; then
  SESSION_ID="$(opencode api POST /api/session --data "$(python3 -c 'import json,sys;print(json.dumps({"parentID":sys.argv[1],"title":sys.argv[2]}))' "$DREAM_PARENT_SESSION" "Dreaming ⋅ $DATE")" |
    python3 -c 'import json,sys;d=json.load(sys.stdin);print((d.get("data") or d)["id"])')"
  RUN_ARGS+=(--session "$SESSION_ID")
else
  RUN_ARGS+=(--title "Dreaming ⋅ $DATE")
fi
set +e
opencode run "${RUN_ARGS[@]}" "$PROMPT" >"$LOG" 2>&1
STATUS=$?
set -e
[ -n "$SESSION_ID" ] || SESSION_ID="$(grep -o '"sessionID":"ses_[A-Za-z0-9]*"' "$LOG" | head -1 | cut -d'"' -f4 || true)"
[ -n "$SESSION_ID" ] && opencode api PATCH "/api/session/$SESSION_ID" -d '{"archived":true}' >/dev/null 2>&1 || true

REVERTED=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  if ! printf '%s\n' "$BEFORE" | grep -qxF -- "$f"; then
    git -C "$CONFIG_DIR" checkout -- "$f"
    REVERTED="$REVERTED $f"
  fi
done <<<"$(dirty_outside)"

if [ $STATUS -ne 0 ] || [ ! -s "$REPORT" ]; then
  notify "Dream $DATE failed (exit $STATUS). Log: $LOG"
  echo "dream: run failed, see $LOG" >&2
  exit 1
fi
[ -n "$REVERTED" ] && printf '\n## Reverted by the dream script\nThe run edited files outside memory/, which it may only propose changes to:%s\n' "$REVERTED" >>"$REPORT"

echo "$NOW_MS" >"$STATE_FILE"
git -C "$CONFIG_DIR" add -- memory
if ! git -C "$CONFIG_DIR" diff --cached --quiet -- memory; then
  git -C "$CONFIG_DIR" commit -q -m "dream: $DATE memory pass" \
    -m "Automated dreaming run over sessions from $SINCE_ISO to $NOW_ISO. Session: ${SESSION_ID:-unknown}. Report: memory/dreams/$(basename "$REPORT")." -- memory
fi

SUMMARY="$(grep -m1 '^Summary:' "$REPORT" | sed 's/^Summary: *//' || true)"
notify "Dream $DATE: ${SUMMARY:-finished.} Report: $REPORT. To review or apply proposals, load the opencode-memory skill."
echo "dream: done. Report: $REPORT"
