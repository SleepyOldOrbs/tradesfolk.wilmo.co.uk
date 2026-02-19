#!/usr/bin/env bash
# TeammateIdle hook — runs when a specialist agent is about to go idle
# Exit 0 = allow idle, Exit 2 = reject with feedback on stderr
#
# This hook is intentionally lightweight. It reminds teammates to
# verify their work before going idle, but doesn't block on hard checks
# (since different specialists have different completion criteria).

# Read the hook input (JSON from stdin)
INPUT=$(cat)

# Extract teammate info using grep+sed (no external JSON parser needed).
# The grep pattern matches "teammate_name": "value" using POSIX character
# classes for BSD/GNU compatibility. The sed pattern extracts just the value.
TEAMMATE_NAME=$(echo "$INPUT" | grep -o '"teammate_name"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*:.*"\([^"]*\)"/\1/')

# Fall back to "unknown" if parsing fails (empty input, malformed JSON, etc.)
if [ -z "$TEAMMATE_NAME" ]; then
  TEAMMATE_NAME="unknown"
fi

# Log the idle event for observability
echo "[agent-pool] Teammate ${TEAMMATE_NAME} going idle" >&2

# Allow idle — the specialist's own system prompt already defines their
# completion criteria. We don't want to block with generic checks that
# don't apply to every specialist type.
exit 0
