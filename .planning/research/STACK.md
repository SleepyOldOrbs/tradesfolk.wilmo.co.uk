# Stack Research

**Domain:** Claude Code plugin development (Agent Pool plugin)
**Researched:** 2026-02-19
**Confidence:** HIGH

This plugin is pure configuration -- markdown files, JSON manifests, and shell scripts. There is no application framework, no database, no build step. The "stack" is the Claude Code plugin system itself: its file formats, conventions, APIs, and constraints.

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Claude Code Plugin System | v1.0.33+ (current: v2.1.39) | Plugin manifest, auto-discovery of agents/skills/hooks | This IS the platform. The plugin system auto-discovers components from conventional directory locations. No build step, no bundling -- just markdown and JSON in the right places. |
| Markdown + YAML frontmatter | N/A | Agent definitions, skill definitions | Official format for both agents and skills. Claude Code parses YAML frontmatter from `.md` files. No alternatives exist. |
| JSON | N/A | Plugin manifest (`plugin.json`), hooks config (`hooks.json`), MCP config (`.mcp.json`) | Official format for all configuration. Validated by Claude Code on load. |
| Bash / Shell scripts | N/A | Hook command handlers | Hooks of `type: "command"` execute shell commands. Scripts receive JSON on stdin, return decisions via exit codes and stdout JSON. |
| jq | N/A | JSON parsing in hook scripts | Standard tool for extracting fields from hook input JSON in bash scripts. Used in all official examples. |

### Supporting Libraries

None. This plugin has zero runtime dependencies. No `node_modules`, no `package.json`, no Python environment. Everything is static files that Claude Code reads at startup.

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `claude --plugin-dir ./` | Load plugin for local testing | The primary development workflow. Pass the plugin directory to Claude Code to test without installation. Restart Claude Code to pick up changes. |
| `claude --debug` | Debug plugin loading | Shows which plugins load, manifest validation errors, component registration, hook execution. Essential for troubleshooting. |
| `claude plugin validate` or `/plugin validate` | Validate plugin manifest | Checks JSON syntax, required fields, directory structure. Run after any manifest change. |
| `/agents` | View and manage agents | Interactive interface to see all loaded agents (built-in, user, project, plugin). Confirms your plugin agents are discoverable. |
| `/hooks` | View and manage hooks | Shows all registered hooks with their source labels (`[Plugin]` for plugin hooks). Confirms hook registration. |
| `chmod +x` | Make hook scripts executable | Hooks will silently fail if the script is not executable. Always `chmod +x` after creating hook scripts. |

## Plugin System: Complete API Reference

### Plugin Manifest (`plugin.json`)

**Location:** `.claude-plugin/plugin.json` (only file that goes inside `.claude-plugin/`)
**Confidence:** HIGH (official docs, verified via Context7)

**Required fields:**

| Field | Type | Notes |
|-------|------|-------|
| `name` | string | Kebab-case, no spaces. Becomes the namespace prefix for skills (e.g. `agent-pool:browse-pool`). Only required field. |

**Metadata fields (all optional):**

| Field | Type | Notes |
|-------|------|-------|
| `version` | string | Semver (e.g. `"1.0.0"`). Used for update detection -- if you change code but don't bump version, cached installs won't update. |
| `description` | string | Shown in plugin manager UI. |
| `author` | object | `{ "name": "...", "email": "...", "url": "..." }` -- all sub-fields optional. |
| `homepage` | string | Documentation URL. |
| `repository` | string | Source code URL. |
| `license` | string | SPDX identifier (e.g. `"MIT"`). |
| `keywords` | array | Discovery tags (e.g. `["agents", "specialist"]`). |

**Component path fields (all optional):**

| Field | Type | Default Location | Notes |
|-------|------|------------------|-------|
| `commands` | string or array | `commands/` | Legacy; use `skills/` for new work. |
| `agents` | string or array | `agents/` | Path to agent markdown files. Can be a directory or array of file paths. |
| `skills` | string or array | `skills/` | Path to skill directories. |
| `hooks` | string, array, or object | `hooks/hooks.json` | Path to hooks JSON, or inline hook config. |
| `mcpServers` | string, array, or object | `.mcp.json` | MCP server config. |
| `outputStyles` | string or array | `styles/` | Output style files. |
| `lspServers` | string, array, or object | `.lsp.json` | Language server config. |

**Critical rule:** Custom paths SUPPLEMENT defaults, they don't replace them. If `agents/` exists, it's loaded in addition to any paths specified in `"agents"`.

**Environment variable:** `${CLAUDE_PLUGIN_ROOT}` resolves to the plugin's absolute directory. Use in hooks, MCP configs, and scripts.

### Agent Definitions

**Location:** `agents/*.md` (at plugin root, NOT inside `.claude-plugin/`)
**Confidence:** HIGH for core fields; MEDIUM for `color` field

**Frontmatter fields:**

| Field | Required | Type | Values | Notes |
|-------|----------|------|--------|-------|
| `name` | Yes | string | kebab-case | Unique identifier. Appears as `plugin-name:agent-name` in UI. |
| `description` | Yes | string | free text | **Critical for agent discovery.** Claude uses this to decide when to delegate. Should include `<example>` blocks for better matching (see below). |
| `model` | No | string | `inherit`, `sonnet`, `opus`, `haiku` | Defaults to `inherit` (uses parent conversation's model). |
| `color` | No | string | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`, `purple` | Background color in terminal UI. **Undocumented in official docs but generated by `/agents` command and functionally supported.** |
| `tools` | No | string or array | Tool names (e.g. `Read, Grep, Glob, Bash`) | Restricts available tools. Inherits all tools if omitted. |
| `disallowedTools` | No | string or array | Tool names | Denylist -- removed from inherited or specified tool list. |
| `permissionMode` | No | string | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | Overrides permission handling for this agent. |
| `maxTurns` | No | number | integer | Maximum agentic turns before the agent stops. |
| `skills` | No | array | skill names | Skills preloaded into agent context at startup. Full skill content is injected, not just made available. |
| `mcpServers` | No | object | server configs | MCP servers available to this agent. |
| `hooks` | No | object | hook config | Lifecycle hooks scoped to this agent. Same format as `hooks.json`. |
| `memory` | No | string | `user`, `project`, `local` | Enables persistent cross-session memory. |

**Body (after frontmatter):** The system prompt. This is all the agent receives -- it does NOT get the full Claude Code system prompt or the parent conversation history.

**Example blocks in descriptions (HIGH priority for this plugin):**

The `/agents` command generates descriptions with `<example>` blocks. These help Claude Code match tasks to agents automatically. Format:

```yaml
description: |
  Expert JavaScript developer for frontend and backend JS.
  <example>Refactor the auth middleware to use async/await</example>
  <example>Add TypeScript types to the API client</example>
  <example>Debug the WebSocket connection dropping issue</example>
```

This is the format the plugin validator flagged as missing from the current agent definitions. The multiline `|` YAML syntax is required for descriptions containing example blocks.

### Skill Definitions

**Location:** `skills/<skill-name>/SKILL.md` (each skill is a directory with a SKILL.md entrypoint)
**Confidence:** HIGH (official docs, verified)

**Frontmatter fields:**

| Field | Required | Type | Values | Notes |
|-------|----------|------|--------|-------|
| `name` | No | string | kebab-case, max 64 chars | Display name. If omitted, uses directory name. |
| `description` | Recommended | string | free text | Claude uses this to decide when to auto-load the skill. If omitted, uses first paragraph of content. |
| `argument-hint` | No | string | e.g. `[task-description]` | Hint shown during autocomplete. |
| `disable-model-invocation` | No | boolean | `true`/`false` | If `true`, only users can invoke (not Claude). Default: `false`. |
| `user-invocable` | No | boolean | `true`/`false` | If `false`, hidden from `/` menu. Default: `true`. |
| `allowed-tools` | No | string | Tool names | Restricts tools while skill is active. |
| `model` | No | string | model alias | Model to use when skill is active. |
| `context` | No | string | `fork` | Run in a forked subagent context. |
| `agent` | No | string | agent name | Which subagent to use when `context: fork`. |
| `hooks` | No | object | hook config | Hooks scoped to this skill's lifecycle. |

**String substitutions available in skill content:**

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill. |
| `$ARGUMENTS[N]` / `$N` | Specific argument by 0-based index. |
| `${CLAUDE_SESSION_ID}` | Current session ID. |
| `` !`command` `` | Shell command executed before content is sent (preprocessing). |

**Supporting files:** Skills can include additional files alongside SKILL.md (templates, scripts, reference docs). Reference them from SKILL.md so Claude knows when to load them.

**Plugin namespacing:** Plugin skills are invoked as `/plugin-name:skill-name` to prevent conflicts.

### Hook System

**Location:** `hooks/hooks.json` (at plugin root)
**Confidence:** HIGH (official docs, exhaustively documented)

**File format:**

```json
{
  "description": "Optional description of these hooks",
  "hooks": {
    "EventName": [
      {
        "matcher": "regex-pattern",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/handler.sh",
            "timeout": 600
          }
        ]
      }
    ]
  }
}
```

**All available hook events:**

| Event | When It Fires | Can Block? | Matcher Filters On |
|-------|--------------|------------|-------------------|
| `SessionStart` | Session begins/resumes | No | `startup`, `resume`, `clear`, `compact` |
| `UserPromptSubmit` | User submits prompt | Yes | No matcher support |
| `PreToolUse` | Before tool executes | Yes (allow/deny/ask) | Tool name |
| `PermissionRequest` | Permission dialog shown | Yes (allow/deny) | Tool name |
| `PostToolUse` | After tool succeeds | No (feedback only) | Tool name |
| `PostToolUseFailure` | After tool fails | No (feedback only) | Tool name |
| `Notification` | Notification sent | No | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog` |
| `SubagentStart` | Subagent spawned | No (context injection only) | Agent type name |
| `SubagentStop` | Subagent finishes | Yes | Agent type name |
| `Stop` | Main agent finishes | Yes | No matcher support |
| `TeammateIdle` | Agent team teammate going idle | Yes (exit 2 to reject) | No matcher support |
| `TaskCompleted` | Task marked complete | Yes (exit 2 to reject) | No matcher support |
| `PreCompact` | Before context compaction | No | `manual`, `auto` |
| `SessionEnd` | Session terminates | No | Exit reason |

**Hook handler types:**

| Type | Field | Description |
|------|-------|-------------|
| `command` | `command` | Shell command. Receives JSON on stdin. Exit 0 = success, exit 2 = blocking error. |
| `prompt` | `prompt` | Single-turn LLM evaluation. Returns `{ "ok": true/false, "reason": "..." }`. |
| `agent` | `prompt` | Multi-turn subagent with tool access (Read, Grep, Glob). Up to 50 turns. |

**TeammateIdle specifics (relevant to this plugin):**

- Fires when an agent team teammate is about to go idle.
- Input JSON includes `teammate_name` and `team_name`.
- Exit 0 = allow idle. Exit 2 = reject with stderr feedback (teammate continues working).
- Does NOT support `prompt` or `agent` hook types -- command only.
- Does NOT support matchers -- fires on every occurrence.

**TaskCompleted specifics (relevant to this plugin):**

- Fires when any agent marks a task complete, or when an agent team teammate finishes with in-progress tasks.
- Input JSON includes `task_id`, `task_subject`, `task_description`, `teammate_name`, `team_name`.
- Exit 0 = allow completion. Exit 2 = reject with stderr feedback.
- Does NOT support matchers -- fires on every occurrence.
- Does NOT support `prompt` or `agent` hook types -- command only.

### Agent Teams Integration

**Confidence:** MEDIUM (feature is experimental, API may change)

Agent teams are enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in settings or environment. The team lead spawns teammates, each running in their own Claude Code instance with their own context window.

**How plugin agents work with agent teams:**
- Plugin agents appear in `/agents` alongside built-in and user agents.
- The team lead can spawn any discoverable agent as a teammate.
- Agent descriptions (including `<example>` blocks) help the lead match tasks to specialists.
- TeammateIdle and TaskCompleted hooks fire for ALL teammates, including those spawned from plugin agents.
- Agent hooks defined in frontmatter are scoped to that agent's lifecycle.

### Plugin Distribution

**Confidence:** HIGH (official docs)

**CLI commands:**

| Command | Description |
|---------|-------------|
| `claude plugin install <plugin>` | Install from marketplace |
| `claude plugin uninstall <plugin>` | Remove plugin |
| `claude plugin enable <plugin>` | Enable disabled plugin |
| `claude plugin disable <plugin>` | Disable without removing |
| `claude plugin update <plugin>` | Update to latest version |
| `claude --plugin-dir ./path` | Load plugin for dev/testing |

**Installation scopes:**

| Scope | Settings File | Use Case |
|-------|---------------|----------|
| `user` (default) | `~/.claude/settings.json` | Personal, all projects |
| `project` | `.claude/settings.json` | Team, committed to repo |
| `local` | `.claude/settings.local.json` | Project-specific, gitignored |

**Marketplace distribution:** Plugins are distributed via plugin marketplaces (directories of plugins). Create a `marketplace.json` to list available plugins. Users install from marketplaces with `claude plugin install <name>@<marketplace>`.

**Caching:** Installed marketplace plugins are copied to `~/.claude/plugins/cache/`. This means you MUST bump the version in `plugin.json` when you change code, or users won't see updates.

## What NOT to Do

| Avoid | Why | Do Instead |
|-------|-----|------------|
| Put `agents/`, `skills/`, `hooks/` inside `.claude-plugin/` | Claude Code won't find them. Only `plugin.json` goes inside `.claude-plugin/`. | Keep all component directories at plugin root. |
| Use absolute paths in `plugin.json` | Paths must be relative to plugin root and start with `./`. Absolute paths break after installation (caching copies files). | Use relative paths and `${CLAUDE_PLUGIN_ROOT}` in scripts. |
| Reference files outside plugin directory with `../` | Path traversal doesn't work after installation because external files aren't copied to the cache. | Use symlinks if you need external dependencies (symlinks are honoured during copy). |
| Use `any` as a model value | Not a valid model alias. | Use `inherit`, `sonnet`, `opus`, or `haiku`. |
| Use `args` in agent frontmatter | Not a supported field for agents. `args` is not documented and won't be processed. | Agent arguments come from the task delegation prompt. |
| Forget `chmod +x` on hook scripts | Hook will silently fail. Debug output (`claude --debug`) will show the failure. | Always make hook scripts executable. |
| Add a `package.json` or `node_modules` | This is a pure-config plugin. Adding a build step is unnecessary overhead. | Keep it as static markdown/JSON files. |
| Use `user_invocable` with an underscore | The correct field is `user-invocable` with a hyphen. YAML frontmatter uses kebab-case for Claude Code fields. | Use `user-invocable: true` or `user-invocable: false`. |
| Use single-line descriptions for agents with example blocks | YAML single-line strings can't contain newlines needed for `<example>` blocks. | Use YAML multiline syntax: `description: \|` |
| Assume `TeammateIdle` supports prompt-based hooks | It only supports `type: "command"`. Prompt and agent hook types are not available for this event. | Use shell scripts for TeammateIdle hooks. |

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Plugin (`.claude-plugin/plugin.json`) | Standalone `.claude/agents/` directory | When agents are personal or project-specific and don't need to be shared/distributed. Standalone is simpler but can't be installed by others. |
| Skills (`skills/*/SKILL.md`) | Commands (`commands/*.md`) | Never for new work. `commands/` is legacy. Skills support directories with supporting files, `context: fork`, hooks, and more. Both create `/name` shortcuts. |
| `type: "command"` hooks | `type: "prompt"` or `type: "agent"` hooks | Use prompt hooks for LLM-evaluated quality gates. Use agent hooks when verification requires reading files. But note: TeammateIdle and TaskCompleted only support command hooks. |
| Shell scripts for hooks | Python/Node.js scripts | When hook logic is complex enough to warrant a full language. The `command` field executes any shell command, so `python script.py` or `node script.js` works. jq + bash is simpler for JSON extraction. |
| MCP server in plugin | MCP servers in user config | When the plugin needs external tool integration (APIs, databases). This plugin doesn't -- it's pure configuration. |

## Stack Patterns by Variant

**If adding a new agent:**
- Create `agents/<name>.md` with YAML frontmatter
- Include `name`, `description` (with `<example>` blocks), `model: inherit`, and `color`
- Follow the three-section system prompt pattern: Core expertise, Working standards, When given a task
- Assign color by domain category (blue=frontend, green=backend, yellow=quality, red=security, cyan=infra, magenta=data/docs)

**If adding a new skill:**
- Create `skills/<name>/SKILL.md` with YAML frontmatter
- Include `name`, `description`, `user-invocable`
- Use `$ARGUMENTS` for dynamic input
- Add supporting files alongside SKILL.md if needed (templates, reference docs)
- Skills are namespaced as `agent-pool:<skill-name>` when accessed via the plugin

**If adding a new hook:**
- Add to `hooks/hooks.json` under the appropriate event key
- Use `${CLAUDE_PLUGIN_ROOT}/hooks/script.sh` for script paths
- Make scripts executable (`chmod +x`)
- Scripts receive JSON on stdin; parse with `jq`
- Exit 0 to allow, exit 2 to block (with feedback on stderr)

**If converting to a GitHub-distributed plugin:**
- Push to a public GitHub repo
- Create a `marketplace.json` (or add to an existing marketplace)
- Users install via `claude plugin install agent-pool@marketplace-name`
- Bump `version` in `plugin.json` with every release (cache won't update without version change)

## Version Compatibility

| Component | Compatible With | Notes |
|-----------|-----------------|-------|
| Plugin manifest schema | Claude Code v1.0.33+ | Plugin system introduced in v1.0.33. Current version is v2.1.39. |
| Agent Teams | Claude Code v2.0+ (experimental) | Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` flag. API may change. |
| `color` field in agents | Claude Code v2.0+ (undocumented) | Generated by `/agents` command, functionally works, but not in official docs. May change. |
| TeammateIdle hook | Claude Code v2.0+ | Confirmed as a valid hook event in official docs. The current plugin uses this correctly. |
| TaskCompleted hook | Claude Code v2.0+ | Valid hook event. STATUS.md mentions adding this as a low-priority task. |
| `user-invocable` frontmatter | Claude Code v1.0.33+ | Supported since plugin system launch. Note: hyphenated, not underscored. |

## Sources

- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) -- Complete manifest schema, component specs, CLI commands, debugging (HIGH confidence)
- [Create Plugins Guide](https://code.claude.com/docs/en/plugins) -- Plugin creation tutorial, directory structure, migration from standalone (HIGH confidence)
- [Hooks Reference](https://code.claude.com/docs/en/hooks) -- All 14 hook events, input/output schemas, exit codes, async hooks, prompt hooks (HIGH confidence)
- [Create Custom Subagents](https://code.claude.com/docs/en/sub-agents) -- Agent frontmatter fields, tools, permissions, hooks, memory, examples (HIGH confidence)
- [Extend Claude with Skills](https://code.claude.com/docs/en/skills) -- SKILL.md format, frontmatter fields, string substitutions, supporting files (HIGH confidence)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams) -- Team architecture, TeammateIdle/TaskCompleted hooks, experimental status (MEDIUM confidence -- experimental feature)
- Context7: `/websites/code_claude_en_plugins-reference` -- Verified plugin manifest schema, agent structure, hooks format (HIGH confidence)
- Context7: `/anthropics/claude-code` -- Verified hook events list, hook input/output formats (HIGH confidence)
- Context7: `/affaan-m/everything-claude-code` -- Community patterns for agents with tools field, agent templates (MEDIUM confidence)
- [GitHub Issue #8501](https://github.com/anthropics/claude-code/issues/8501) -- Documents the `color` field discrepancy between `/agents` output and official docs (MEDIUM confidence)

---
*Stack research for: Claude Code plugin development (Agent Pool)*
*Researched: 2026-02-19*
