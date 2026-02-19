# Phase 2: Hook Verification - Context

**Gathered:** 2026-02-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify and fix the TeammateIdle hook for portability and real-world use. This covers: confirming the hook event name is correct, fixing the script for cross-platform portability, and ensuring path resolution works after plugin installation via cache copying. No new hooks are added in this phase — just hardening what exists.

</domain>

<decisions>
## Implementation Decisions

### jq dependency removal
- Replace jq with pure bash alternatives (parameter expansion, grep, or sed) for JSON field extraction
- The script only needs to extract `teammate_name` from a simple JSON object — jq is overkill
- This resolves the STATE.md blocker: "jq dependency in hook scripts may not be available on all systems"
- Fallback behavior if JSON parsing fails: use "unknown" as teammate name (same as current jq fallback)

### Shebang and executable bit
- Change shebang from `#!/bin/bash` to `#!/usr/bin/env bash` for portability across systems where bash isn't at /bin/bash
- Track executable bit in git via `git update-index --chmod=+x hooks/teammate-checklist.sh`
- Both are explicit HOOK-02 requirements

### hooks.json schema verification
- The current nested structure (`hooks.TeammateIdle[].hooks[]`) needs verification against Claude Code's actual plugin hook schema
- Research should find the official hook configuration format and confirm or fix the schema
- If the format is wrong, fix it to match the documented schema exactly

### Hook event name verification
- `TeammateIdle` is the current event name — needs confirmation that this is a real Claude Code hook event
- Research should search Claude Code documentation and plugin-dev references for the actual hook event names
- If the event name is wrong, update hooks.json to use the correct name
- Full runtime verification deferred to Phase 4 (requires live Agent Teams session)

### Path resolution strategy
- Current approach uses `${CLAUDE_PLUGIN_ROOT}` in hooks.json — this is the recommended pattern per HOOK-03
- Verify that Claude Code actually expands this variable when executing hook commands
- If `${CLAUDE_PLUGIN_ROOT}` is not supported, research the correct alternative (relative paths, `__dirname` equivalent, etc.)

### Hook behavior (kept as-is)
- Keep the current "log and allow" behavior — lightweight observability without blocking
- Exit code 0 = allow idle (non-blocking)
- Stderr logging for observability: `[agent-pool] Teammate ${NAME} going idle`
- Aligns with locked project decision: "Lightweight hooks only"
- No quality gates — different specialists have different completion criteria

### Claude's Discretion
- Exact pure-bash JSON parsing technique (grep+sed, parameter expansion, or awk — whatever is most portable)
- Whether to add a bash version check or `set -euo pipefail` for defensive scripting
- Whether teammate-checklist.sh needs renaming to match the hook event name convention

</decisions>

<specifics>
## Specific Ideas

- The hook script is only 22 lines — keep it simple, don't over-engineer
- The script receives JSON on stdin from Claude Code — verify what fields are actually provided (teammate_name, or different field names?)
- If Claude Code doesn't provide JSON on stdin for hooks, the entire input parsing section needs rethinking

</specifics>

<deferred>
## Deferred Ideas

- TaskCompleted hook for quality verification — v2 requirement (QHOK-01), not Phase 2 scope
- SubagentStart/SubagentStop logging hooks — v2 requirement (QHOK-02), not Phase 2 scope
- Adding additional hook events beyond TeammateIdle — out of scope for this phase

</deferred>

---

*Phase: 02-hook-verification*
*Context gathered: 2026-02-19*
