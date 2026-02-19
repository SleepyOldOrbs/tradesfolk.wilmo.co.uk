# Phase 2: Hook Verification - Research

**Researched:** 2026-02-19
**Domain:** Claude Code plugin hooks, Agent Teams hook events, portable bash scripting
**Confidence:** HIGH

## Summary

The TeammateIdle hook is a real, documented Claude Code hook event. Official documentation at code.claude.com/docs/en/hooks confirms both the event name and the exact JSON schema received on stdin. The current hooks.json structure in the plugin is correct in its nesting pattern (`hooks.TeammateIdle[].hooks[]`) but needs no schema changes -- it already matches the documented format. The `${CLAUDE_PLUGIN_ROOT}` environment variable is the officially documented way to reference plugin scripts and is expanded by Claude Code when executing hook commands.

The main implementation work is: (1) removing the `jq` dependency from teammate-checklist.sh by using pure bash JSON extraction, (2) changing the shebang to `#!/usr/bin/env bash`, (3) ensuring the executable bit is tracked in git, and (4) verifying the stdin field names match the documented schema (they do -- `teammate_name` and `team_name` are the correct fields).

**Primary recommendation:** Fix the hook script for portability (shebang + jq removal) and verify the hooks.json schema matches official docs -- which it already does. No structural changes needed to hooks.json.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Replace jq with pure bash alternatives (parameter expansion, grep, or sed) for JSON field extraction
- The script only needs to extract `teammate_name` from a simple JSON object -- jq is overkill
- Fallback behavior if JSON parsing fails: use "unknown" as teammate name
- Change shebang from `#!/bin/bash` to `#!/usr/bin/env bash` for portability
- Track executable bit in git via `git update-index --chmod=+x hooks/teammate-checklist.sh`
- Verify hooks.json schema against Claude Code's actual plugin hook schema; fix if wrong
- Verify `TeammateIdle` is a real Claude Code hook event; update if wrong
- Verify `${CLAUDE_PLUGIN_ROOT}` is expanded by Claude Code when executing hook commands
- Keep current "log and allow" behavior -- lightweight observability without blocking
- Exit code 0 = allow idle (non-blocking)
- No quality gates -- different specialists have different completion criteria

### Claude's Discretion
- Exact pure-bash JSON parsing technique (grep+sed, parameter expansion, or awk)
- Whether to add `set -euo pipefail` for defensive scripting
- Whether teammate-checklist.sh needs renaming to match hook event name convention

### Deferred Ideas (OUT OF SCOPE)
- TaskCompleted hook for quality verification -- v2 requirement (QHOK-01), not Phase 2 scope
- SubagentStart/SubagentStop logging hooks -- v2 requirement (QHOK-02), not Phase 2 scope
- Adding additional hook events beyond TeammateIdle -- out of scope for this phase
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| HOOK-01 | TeammateIdle hook event name verified working in a real Agent Teams session | Research confirms `TeammateIdle` is a real, documented hook event per official Claude Code docs. The exact stdin JSON schema is documented with `teammate_name` and `team_name` fields. Full runtime verification deferred to Phase 4. |
| HOOK-02 | Hook script has correct shebang and executable bit tracked in git | Research confirms `#!/usr/bin/env bash` is the portable standard. `git update-index --chmod=+x` is the correct git command for tracking executable bits. |
| HOOK-03 | Hook script paths use relative references that survive plugin cache copying | Research confirms `${CLAUDE_PLUGIN_ROOT}` is the officially documented environment variable for plugin script paths. Plugins are cached to `~/.claude/plugins/cache/` and `${CLAUDE_PLUGIN_ROOT}` resolves to the cached copy location. |
</phase_requirements>

## Standard Stack

This phase involves no library dependencies. It is pure bash scripting and JSON configuration.

### Core
| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| bash | 4.0+ | Hook script runtime | Universal on macOS/Linux; `#!/usr/bin/env bash` ensures portable resolution |
| git | any | Track executable bit | `git update-index --chmod=+x` is the standard way to track file permissions |

### Supporting
| Tool | Purpose | When to Use |
|------|---------|-------------|
| grep | Pure-bash JSON field extraction | Extracting `teammate_name` from stdin JSON without jq |
| sed | String cleanup (removing quotes) | Post-extraction cleanup of JSON values |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| grep+sed for JSON | bash parameter expansion (`${var##*:}`) | Parameter expansion is more fragile with nested JSON; grep+sed is more readable for this use case |
| grep+sed for JSON | awk | awk is equally portable but more complex syntax for simple field extraction |
| grep+sed for JSON | python -c | Python is more reliable for JSON but adds a heavier dependency than jq |

## Architecture Patterns

### Current Plugin Structure (unchanged)
```
hooks/
├── hooks.json              # Hook event configuration
└── teammate-checklist.sh   # TeammateIdle handler script
```

### Pattern 1: Plugin Hook Configuration Schema
**What:** The official hooks.json format for Claude Code plugins
**When to use:** Any plugin that needs event-driven hooks
**Verified against:** Official Claude Code documentation at code.claude.com/docs/en/hooks

The current hooks.json structure is **correct**. The schema is:

```json
{
  "description": "Optional description of what these hooks do",
  "hooks": {
    "EventName": [
      {
        "matcher": "optional-regex-matcher",
        "hooks": [
          {
            "type": "command",
            "command": "the shell command to run"
          }
        ]
      }
    ]
  }
}
```

Key points from official docs:
- The outer `hooks` key contains event name keys
- Each event maps to an array of matcher groups
- Each matcher group has an optional `matcher` field (regex) and a `hooks` array
- Each hook handler has `type` (command/prompt/agent) and type-specific fields
- `TeammateIdle` does NOT support matchers (always fires on every occurrence)
- The `description` field at the top level is optional for plugin hooks

**Current hooks.json is structurally correct** but the `matcher` concept doesn't apply to TeammateIdle. The current file wraps the hook in a matcher group without a `matcher` field, which is the correct way to say "no filter, always fire."

### Pattern 2: TeammateIdle Hook Exit Code Protocol
**What:** How Claude Code interprets hook exit codes for TeammateIdle
**When to use:** All TeammateIdle hook handlers
**Source:** Official docs at code.claude.com/docs/en/hooks#teammateidle

```
Exit 0  = allow the teammate to go idle (proceed normally)
Exit 2  = block idle, feed stderr message back to teammate as feedback
Other   = non-blocking error, stderr shown in verbose mode only
```

**Critical:** TeammateIdle hooks use exit codes ONLY, not JSON decision control. This is different from PreToolUse or Stop hooks which can return JSON. Any JSON printed to stdout is ignored for decision purposes.

### Pattern 3: Plugin Path Resolution
**What:** How `${CLAUDE_PLUGIN_ROOT}` works for plugin scripts
**When to use:** Any hook command that references scripts bundled with the plugin
**Source:** Official docs at code.claude.com/docs/en/plugins-reference#environment-variables

```json
{
  "command": "${CLAUDE_PLUGIN_ROOT}/hooks/teammate-checklist.sh"
}
```

Claude Code expands `${CLAUDE_PLUGIN_ROOT}` to the absolute path of the plugin directory. When plugins are installed via a marketplace, they are cached to `~/.claude/plugins/cache/`. The `${CLAUDE_PLUGIN_ROOT}` variable resolves to this cached location, NOT the original source. This is why relative paths and this variable are critical -- hardcoded absolute paths would break after installation.

### Pattern 4: TeammateIdle stdin JSON Schema
**What:** The exact JSON that Claude Code sends on stdin to TeammateIdle hooks
**When to use:** Parsing input in the hook script
**Source:** Official docs at code.claude.com/docs/en/hooks#teammateidle-input

```json
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../session.jsonl",
  "cwd": "/Users/.../project",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

The fields specific to TeammateIdle are:
- `teammate_name` -- name of the teammate about to go idle
- `team_name` -- name of the team

Common fields present on ALL hook events:
- `session_id` -- current session identifier
- `transcript_path` -- path to conversation JSON
- `cwd` -- current working directory
- `permission_mode` -- current permission mode
- `hook_event_name` -- name of the event ("TeammateIdle")

**This confirms the current script's approach of extracting `teammate_name` is correct.** The field name matches exactly.

### Anti-Patterns to Avoid
- **Using jq in plugin hooks:** Not all systems have jq installed. Plugin hooks should use only bash builtins and standard POSIX utilities (grep, sed, awk) that are guaranteed to exist.
- **Returning JSON on stdout for TeammateIdle:** TeammateIdle uses exit codes only. JSON output is ignored for decision control. Only stderr is used for feedback (on exit 2).
- **Using hardcoded absolute paths in hooks.json:** Plugins are cached to a different location after installation. Always use `${CLAUDE_PLUGIN_ROOT}` for bundled scripts.
- **Using `#!/bin/bash` shebang:** On some systems (NixOS, some macOS setups), bash is not at `/bin/bash`. Use `#!/usr/bin/env bash` instead.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON parsing in bash | Complex regex parser | Simple grep+sed pipeline | Only need one field from a flat JSON object; full parsing is overkill |
| Cross-platform path resolution | Manual path detection logic | `${CLAUDE_PLUGIN_ROOT}` env var | Claude Code provides this variable specifically for plugin scripts |
| Hook schema format | Custom event configuration | Official hooks.json schema | The format is documented and validated by Claude Code |

**Key insight:** The hook script is intentionally simple (22 lines). The "don't hand-roll" principle here means: don't add complexity that isn't needed. A grep+sed one-liner for extracting a single JSON field is the right level of effort.

## Common Pitfalls

### Pitfall 1: jq Not Available
**What goes wrong:** Hook script fails silently when jq is not installed on the target system
**Why it happens:** jq is not a standard Unix utility; it must be installed separately
**How to avoid:** Replace jq with grep+sed or bash parameter expansion (user-locked decision)
**Warning signs:** `command not found: jq` in stderr, hook exits with non-zero code

### Pitfall 2: Executable Bit Not Tracked in Git
**What goes wrong:** Script installs without execute permission; hook silently fails
**Why it happens:** Git does not track Unix permissions by default beyond the executable bit
**How to avoid:** Run `git update-index --chmod=+x hooks/teammate-checklist.sh` and commit
**Warning signs:** `Permission denied` error in Claude Code debug output; hook listed in `/hooks` but never fires

### Pitfall 3: Non-Portable Shebang
**What goes wrong:** Script fails on systems where bash is not at /bin/bash (NixOS, Homebrew bash on macOS)
**Why it happens:** Hardcoded `#!/bin/bash` assumes bash location
**How to avoid:** Use `#!/usr/bin/env bash` which searches PATH
**Warning signs:** `bad interpreter: /bin/bash: no such file or directory`

### Pitfall 4: Assuming JSON Output Controls TeammateIdle
**What goes wrong:** Developer writes complex JSON responses expecting them to control behavior
**Why it happens:** Other hook events (PreToolUse, Stop) use JSON decision control, creating false assumption
**How to avoid:** TeammateIdle uses exit codes only. Exit 0 = allow idle, Exit 2 = block with stderr feedback
**Warning signs:** JSON output on stdout being silently ignored

### Pitfall 5: set -e Breaking Fallback Logic
**What goes wrong:** `set -e` causes the script to exit on the first failing command, including intentional fallback parsing
**Why it happens:** `set -e` is often recommended for "defensive scripting" but interacts poorly with fallback patterns
**How to avoid:** Either don't use `set -e`, or use `|| true` / `|| :` after commands that may fail intentionally
**Warning signs:** Script exits with non-zero code before reaching the fallback `echo "unknown"` logic

### Pitfall 6: Plugin Cache Staleness
**What goes wrong:** Edited hook script changes are not reflected after plugin reinstall
**Why it happens:** Marketplace-installed plugins are cached to `~/.claude/plugins/cache/`; old cache persists
**How to avoid:** Bump version in plugin.json before redistribution; use `--plugin-dir` for local development
**Warning signs:** Changes work with `--plugin-dir` but not after `plugin install`

## Code Examples

### Verified: TeammateIdle hook script (recommended implementation)

```bash
#!/usr/bin/env bash
# TeammateIdle hook -- runs when a specialist agent is about to go idle
# Exit 0 = allow idle, Exit 2 = reject with feedback on stderr
#
# This hook is intentionally lightweight. It reminds teammates to
# verify their work before going idle, but doesn't block on hard checks
# (since different specialists have different completion criteria).

# Read the hook input (JSON from stdin)
INPUT=$(cat)

# Extract teammate_name using grep+sed (no jq dependency)
# Expected input: {"teammate_name": "researcher", "team_name": "my-project", ...}
TEAMMATE_NAME=$(echo "$INPUT" | grep -o '"teammate_name"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*:.*"\([^"]*\)"/\1/')

# Fallback if parsing fails
if [ -z "$TEAMMATE_NAME" ]; then
  TEAMMATE_NAME="unknown"
fi

# Log the idle event for observability
echo "[agent-pool] Teammate ${TEAMMATE_NAME} going idle" >&2

# Allow idle -- the specialist's own system prompt already defines their
# completion criteria. We don't want to block with generic checks that
# don't apply to every specialist type.
exit 0
```
Source: Adapted from official TeammateIdle documentation at code.claude.com/docs/en/hooks#teammateidle

### Verified: hooks.json (confirmed correct schema)

```json
{
  "description": "Quality gates for agent pool teammates",
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks/teammate-checklist.sh\""
          }
        ]
      }
    ]
  }
}
```
Source: Schema matches official plugin hooks documentation at code.claude.com/docs/en/plugins-reference#hooks

### Alternative: Direct execution without wrapping in bash

```json
{
  "description": "Quality gates for agent pool teammates",
  "hooks": {
    "TeammateIdle": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/teammate-checklist.sh"
          }
        ]
      }
    ]
  }
}
```
Note: If the script has correct shebang and executable bit, the `bash` prefix is unnecessary. The official docs show both patterns. Using `bash "..."` is safer as a fallback if executable bit is lost, but direct execution is cleaner.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `#!/bin/bash` hardcoded shebang | `#!/usr/bin/env bash` portable shebang | Long-standing best practice | Works on NixOS, macOS with Homebrew bash, etc. |
| Using jq in hook scripts | Pure bash alternatives (grep/sed) | Plugin portability requirement | No external dependency; works on any system with bash |
| Top-level `decision`/`reason` for PreToolUse | `hookSpecificOutput.permissionDecision` | Deprecated in recent Claude Code versions | TeammateIdle is unaffected (exit code only) but worth noting |

**Deprecated/outdated:**
- PreToolUse top-level `decision` and `reason` fields are deprecated in favor of `hookSpecificOutput.permissionDecision` -- not relevant to TeammateIdle but worth documenting for awareness.

## Discretion Recommendations

### Pure-bash JSON parsing technique: Use grep+sed
**Recommendation:** Use `grep -o` to extract the key-value pair, then `sed` to strip the value.

```bash
TEAMMATE_NAME=$(echo "$INPUT" | grep -o '"teammate_name"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*:.*"\([^"]*\)"/\1/')
```

**Why grep+sed over alternatives:**
- `grep` and `sed` are POSIX-standard and available on every Unix system
- The pattern is readable and handles whitespace variations in JSON
- `[[:space:]]` character class is more portable than `\s`
- Works with both GNU and BSD grep/sed (macOS ships BSD versions)
- Parameter expansion (`${var##*:}`) is more fragile and harder to read for JSON
- `awk` would work but is overkill for extracting a single field

### Defensive scripting: Do NOT add `set -euo pipefail`
**Recommendation:** Do not add `set -euo pipefail` to this script.

**Rationale:**
- `set -e` would cause the script to exit if `grep` finds no match (exit code 1), bypassing the fallback logic
- `set -u` would cause an error on unset variables, but we handle that with explicit checks
- `set -o pipefail` would cause pipe failures to propagate, breaking the grep|sed pipeline if grep finds no match
- The script is 22 lines with a clear fallback path. Defensive flags add complexity without benefit
- The script MUST always exit 0 (allow idle) regardless of parsing errors -- defensive flags work against this

### Script renaming: Keep teammate-checklist.sh
**Recommendation:** Do not rename the script.

**Rationale:**
- The filename `teammate-checklist.sh` describes what the hook does (checks teammate status), not the event name
- Hook event names are a Claude Code internal concept; script names should describe purpose
- Renaming would require updating hooks.json and git history for zero functional benefit
- The STATUS.md and CLAUDE.md both reference this filename

## Open Questions

1. **Is `bash "..."` wrapper needed in hooks.json command?**
   - What we know: Official docs show both `"${CLAUDE_PLUGIN_ROOT}/scripts/format.sh"` (direct) and `bash "..."` (wrapped) patterns. Both work.
   - What's unclear: Whether the executable bit is reliably preserved through plugin cache copying. If it is, direct execution is cleaner.
   - Recommendation: Keep the `bash "..."` wrapper as a safety measure. It ensures the script runs even if the executable bit is lost during cache copying. This is more defensive and the performance difference is negligible.

2. **Does the plugin cache copy preserve executable bits?**
   - What we know: Plugin caching copies files to `~/.claude/plugins/cache/`. The docs mention symlinks are honored.
   - What's unclear: Whether file permissions (chmod +x) are preserved in the copy.
   - Recommendation: Track the executable bit in git AND keep the `bash` wrapper in hooks.json as belt-and-suspenders. This ensures the hook works regardless of how permissions are handled during caching.

## Sources

### Primary (HIGH confidence)
- Official Claude Code Hooks Reference (code.claude.com/docs/en/hooks) -- Complete hook lifecycle, all event names, JSON schemas, exit code behavior, plugin hooks format. **Fetched 2026-02-19.**
- Official Claude Code Agent Teams docs (code.claude.com/docs/en/agent-teams) -- TeammateIdle and TaskCompleted hook usage in agent teams context. **Fetched 2026-02-19.**
- Official Claude Code Plugins Reference (code.claude.com/docs/en/plugins-reference) -- Plugin manifest schema, hooks field, `${CLAUDE_PLUGIN_ROOT}`, plugin caching, directory structure. **Fetched 2026-02-19.**
- Official Claude Code Plugins Guide (code.claude.com/docs/en/plugins) -- Plugin creation, hooks migration, testing with `--plugin-dir`. **Fetched 2026-02-19.**

### Secondary (MEDIUM confidence)
- None needed -- all critical claims verified with primary sources.

### Tertiary (LOW confidence)
- None -- all findings are from official documentation.

## Metadata

**Confidence breakdown:**
- Hook event names and schema: HIGH -- verified against official Claude Code documentation
- stdin JSON format for TeammateIdle: HIGH -- exact schema documented with field names
- `${CLAUDE_PLUGIN_ROOT}` behavior: HIGH -- documented in official plugin reference
- Pure-bash JSON parsing approach: HIGH -- standard POSIX utilities, well-understood behavior
- Plugin cache permission handling: MEDIUM -- not explicitly documented whether chmod is preserved

**Research date:** 2026-02-19
**Valid until:** 2026-03-19 (30 days -- hook system is stable, unlikely to change rapidly)
