# Architecture Research

**Domain:** Claude Code plugin (agent roster for Agent Teams)
**Researched:** 2026-02-19
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Claude Code Runtime                             │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  CLAUDE.md   │  │  settings.json│  │  .mcp.json   │              │
│  │  (memory)    │  │  (permissions)│  │  (MCP servers)│              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                       │
│  ┌──────┴─────────────────┴──────────────────┴───────┐              │
│  │               Plugin Loader                        │              │
│  │  Reads .claude-plugin/plugin.json                  │              │
│  │  Auto-discovers: agents/, skills/, hooks/, .mcp.json│             │
│  └──────┬──────────┬──────────┬──────────┬───────────┘              │
│         │          │          │          │                           │
│  ┌──────┴───┐ ┌────┴────┐ ┌──┴───┐ ┌───┴──────┐                    │
│  │  Agents  │ │  Skills │ │ Hooks│ │MCP Servers│                    │
│  │  (.md)   │ │(SKILL.md)│ │(.json)│ │(.mcp.json)│                  │
│  └──────┬───┘ └────┬────┘ └──┬───┘ └───┬──────┘                    │
│         │          │         │          │                           │
│  ┌──────┴──────────┴─────────┴──────────┴────────────┐              │
│  │            Agent Teams / Subagent System            │              │
│  │                                                     │              │
│  │  Team Lead ─┬─ Teammate A (spawned from agent def) │              │
│  │             ├─ Teammate B (spawned from agent def) │              │
│  │             └─ Teammate C (spawned from agent def) │              │
│  │                                                     │              │
│  │  Shared: Task List, Mailbox, Hooks                  │              │
│  └─────────────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| `plugin.json` | Plugin identity, metadata, component path declarations | JSON manifest in `.claude-plugin/` directory. Only `name` is required if manifest is present; auto-discovery handles the rest |
| `agents/*.md` | Subagent definitions with system prompts, tool access, model selection | Markdown files with YAML frontmatter. Discovered from `agents/` automatically |
| `skills/*/SKILL.md` | Reusable capabilities Claude can invoke by context match or `/name` | Markdown with YAML frontmatter in `skills/<name>/SKILL.md` directories |
| `hooks/hooks.json` | Event handlers for lifecycle events (TeammateIdle, TaskCompleted, PreToolUse, etc.) | JSON config referencing shell scripts, prompts, or agent verifiers |
| `.mcp.json` | External tool integrations via Model Context Protocol | JSON config with server definitions (command, args, env) |
| `commands/*.md` | Legacy slash commands (now merged into skills system) | Simple markdown files; skills are preferred for new work |

## Recommended Project Structure

```
agent-pool/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (name, version, metadata)
├── agents/                      # Auto-discovered agent definitions
│   ├── javascript-developer.md
│   ├── react-specialist.md
│   ├── ux-designer.md
│   ├── python-developer.md
│   ├── backend-architect.md
│   ├── systems-programmer.md
│   ├── database-specialist.md
│   ├── qa-tester.md
│   ├── security-auditor.md
│   ├── devops-engineer.md
│   ├── data-scientist.md
│   └── technical-writer.md
├── skills/                      # Auto-discovered skills
│   ├── browse-pool/
│   │   └── SKILL.md
│   ├── assemble-team/
│   │   └── SKILL.md
│   └── team-templates/          # Planned
│       └── SKILL.md
├── hooks/                       # Event handlers
│   ├── hooks.json               # Hook configuration
│   └── teammate-checklist.sh    # TeammateIdle script
├── CLAUDE.md                    # Plugin dev instructions
├── README.md                    # User-facing documentation
├── LICENSE                      # MIT
└── .gitignore
```

### Structure Rationale

- **agents/:** One file per specialist. Auto-discovered by Claude Code from the directory. No registration needed beyond placing the file here. File name = agent identifier.
- **skills/:** Directory-per-skill pattern (`skills/<name>/SKILL.md`) allows supporting files alongside the skill (templates, reference docs, scripts). Claude Code discovers these automatically.
- **hooks/:** Centralised hook configuration in `hooks.json` with scripts alongside. Uses `${CLAUDE_PLUGIN_ROOT}` for path resolution so scripts work regardless of install location.
- **.claude-plugin/:** Contains only the manifest. All other components live at the plugin root, not nested inside this directory (a common mistake that causes components to silently not load).

## Architectural Patterns

### Pattern 1: Agent as Markdown with YAML Frontmatter

**What:** Each agent is a standalone `.md` file. YAML frontmatter declares metadata (name, model, color, description). The markdown body is the system prompt injected when the agent is spawned.

**When to use:** Always -- this is the standard Claude Code agent format.

**Trade-offs:** Simple to author and version-control. No programmatic logic possible in the definition itself (all logic is in the system prompt text). The `description` field is critical because Claude uses it for auto-delegation decisions.

**Example (current format, verified against official docs):**
```markdown
---
name: javascript-developer
description: Expert JavaScript/TypeScript developer...
model: inherit
---

You are a senior JavaScript and TypeScript developer assigned to this team.

## Core expertise
- TypeScript strict mode, generics, utility types...

## Working standards
- Always use `const` by default...

## When given a task
1. Read existing code first...
```

**Supported frontmatter fields (from official docs):**

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase letters and hyphens |
| `description` | Yes | Used by Claude for auto-delegation matching |
| `tools` | No | Allowlist of tools; inherits all if omitted |
| `disallowedTools` | No | Denylist; removed from inherited set |
| `model` | No | `sonnet`, `opus`, `haiku`, `inherit` (default: `inherit`) |
| `permissionMode` | No | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | Max agentic turns before stopping |
| `skills` | No | Skills to preload into agent context |
| `mcpServers` | No | MCP servers available to this agent |
| `hooks` | No | Lifecycle hooks scoped to this agent |
| `memory` | No | `user`, `project`, `local` for persistent memory |

**Note on `color`:** The `color` field is used in the current agent-pool agents but is not explicitly documented as a standard frontmatter field in the official reference. It likely works (Claude Code displays agent colours in the terminal), but its exact accepted values should be verified by testing. LOW confidence on the exact color values accepted.

### Pattern 2: Skills as Context-Matched Capabilities

**What:** Skills are `SKILL.md` files in named directories. Claude auto-discovers them and can invoke them based on description matching or the user can invoke them via `/skill-name`.

**When to use:** For capabilities that Claude should use autonomously or that users should trigger on demand. The browse-pool and assemble-team skills fit this pattern well.

**Trade-offs:** Skills are lightweight (just markdown). They can include supporting files in the same directory. The `description` field drives auto-invocation -- poor descriptions mean Claude never triggers the skill.

**Key frontmatter fields (from official docs):**

| Field | Required | Notes |
|-------|----------|-------|
| `name` | No | Defaults to directory name. Becomes the `/command` |
| `description` | Recommended | Claude uses this for auto-invocation decisions |
| `disable-model-invocation` | No | `true` = user-only, Claude cannot auto-invoke |
| `user-invocable` | No | `false` = hidden from `/` menu, Claude-only |
| `allowed-tools` | No | Tools available without permission when skill is active |
| `model` | No | Model override when skill is active |
| `context` | No | `fork` to run in isolated subagent context |
| `agent` | No | Which subagent type when `context: fork` |
| `hooks` | No | Hooks scoped to skill lifecycle |
| `argument-hint` | No | Autocomplete hint for expected arguments |

**The current `args` field** used in assemble-team (`args: task_description`) is not in the official spec. The official equivalent is `argument-hint`. This should be verified -- it may still work, or it may be silently ignored. MEDIUM confidence.

### Pattern 3: Hooks for Quality Gates

**What:** Hooks are event handlers that fire at specific Claude Code lifecycle points. For Agent Teams, the two key hooks are `TeammateIdle` (fires when a teammate is about to go idle) and `TaskCompleted` (fires when a task is being marked complete).

**When to use:** To enforce quality criteria before teammates stop working or before tasks are closed.

**Trade-offs:** Hooks are powerful but can block agent workflows if they exit with code 2. The current TeammateIdle hook is deliberately lightweight (logs and allows idle), which is the right approach for a generic plugin where different specialists have different completion criteria. Heavier hooks risk being counterproductive for agents like technical-writer or ux-designer.

**Hook types (from official docs):**
- `command` -- runs a shell script (current implementation)
- `prompt` -- sends a prompt to an LLM for yes/no evaluation
- `agent` -- spawns a subagent that can use tools to verify conditions

**TeammateIdle and TaskCompleted use exit codes only**, not JSON decision control. Exit 0 = allow, Exit 2 = block with stderr as feedback.

## Data Flow

### Plugin Loading Flow

```
Claude Code starts / Plugin enabled
    ↓
Plugin Loader reads .claude-plugin/plugin.json
    ↓
Auto-discovers components in default locations:
    agents/ → registers each .md as available subagent
    skills/ → registers each SKILL.md as available skill
    hooks/hooks.json → merges with user/project hooks
    .mcp.json → starts MCP servers
    ↓
Skills descriptions loaded into Claude's context budget
Agent descriptions available for auto-delegation matching
Hooks active for configured events
```

### Agent Team Interaction Flow

```
User asks for a team or Claude proposes one
    ↓
Team Lead (main Claude session) creates team
    ↓
Lead reads agent descriptions from plugin
    ↓
Lead spawns teammates (each gets own context window)
    ↓
Each teammate receives:
  - Agent's system prompt (markdown body)
  - CLAUDE.md from project
  - MCP servers
  - Skills (if listed in agent's skills field)
    ↓
Teammates work independently:
  - Claim tasks from shared task list
  - Message each other via mailbox
  - Use tools within their allowed set
    ↓
TeammateIdle hook fires → teammate-checklist.sh runs
    ↓
TaskCompleted hook fires → (future: quality check)
    ↓
Lead synthesises results
```

### Skill Invocation Flow

```
User types /browse-pool or /assemble-team <task>
    ↓
OR Claude auto-invokes based on description match
    ↓
Skill content (SKILL.md body) loaded into context
$ARGUMENTS replaced with user input
    ↓
Claude follows skill instructions
    ↓
For assemble-team: analyses task → recommends agents → asks for confirmation
For browse-pool: lists agents by category → offers to assemble team
```

### Key Data Flows

1. **Agent discovery:** Plugin loader reads `agents/` directory at startup. Each `.md` file's `name` and `description` fields are indexed. When the Team Lead or user needs an agent, Claude matches the task description against agent descriptions.

2. **System prompt injection:** When a teammate is spawned, the full markdown body of the agent's `.md` file becomes that teammate's system prompt. The teammate does NOT inherit the parent conversation history -- only the system prompt, CLAUDE.md, and any preloaded skills.

3. **Hook execution:** When a teammate goes idle, Claude Code sends JSON to stdin of the hook script containing `teammate_name` and `team_name`. The script reads this, performs its check, and exits with 0 (allow) or 2 (block + feedback on stderr).

4. **Skill context loading:** Skill descriptions (not full content) are always in Claude's context so it knows what is available. Full SKILL.md content loads only when invoked. This is important for context budget -- many skills with long descriptions can exceed the 2% of context window budget.

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 12 agents (current) | Current flat-directory approach works well. All agents load at startup. Context budget for descriptions is not a concern at this size |
| 20-30 agents | Still manageable. Keep descriptions concise. Consider grouping agent descriptions into the browse-pool skill so the full list is only loaded when needed, not always in context |
| 50+ agents | Consider splitting into domain-specific plugins (frontend-pool, backend-pool, etc.) so users only load the agents relevant to their project. A single plugin with 50+ agent descriptions may hit the skill context budget |

### Scaling Priorities

1. **First bottleneck: context budget for descriptions.** Every agent's `description` field is loaded into Claude's context so it can decide when to auto-delegate. With 12 agents, this is fine. At 30+ agents with verbose descriptions, it starts consuming meaningful context. Keep descriptions under 2 sentences. Use `<example>` blocks sparingly (they add context per agent).

2. **Second bottleneck: team-template complexity.** As team-templates grow beyond a handful of presets, the skill content becomes long. Consider supporting files alongside SKILL.md (the directory structure supports this) to keep the main skill focused and load detailed templates on demand.

## Anti-Patterns

### Anti-Pattern 1: Putting Components Inside .claude-plugin/

**What people do:** Place agents/, skills/, or hooks/ inside the `.claude-plugin/` directory alongside `plugin.json`.

**Why it's wrong:** Claude Code only looks for `plugin.json` inside `.claude-plugin/`. All other component directories must be at the plugin root. Components inside `.claude-plugin/` are silently ignored -- no error, just invisible agents and skills.

**Do this instead:** Keep `.claude-plugin/` for the manifest only. Place agents/, skills/, hooks/ at the plugin root level.

### Anti-Pattern 2: Vague Agent Descriptions

**What people do:** Write descriptions like "Helps with code" or "General backend work."

**Why it's wrong:** Claude uses the `description` field to decide when to auto-delegate tasks to an agent. Vague descriptions mean Claude either never delegates (too generic to match) or delegates to the wrong agent (overlapping generic descriptions).

**Do this instead:** Write specific, actionable descriptions: "Expert JavaScript/TypeScript developer. Handles frontend and backend JS -- React, Next.js, Node.js, async patterns, bundling, and performance. Use for implementing features, refactoring JS/TS code, debugging runtime issues, and modernising legacy JavaScript."

### Anti-Pattern 3: Heavy TeammateIdle Hooks for a Generic Plugin

**What people do:** Add hooks that run test suites or linters before allowing any teammate to go idle.

**Why it's wrong:** A generic agent-pool plugin provides agents across all domains. A "run tests" hook doesn't make sense for the technical-writer agent. A "run linter" hook doesn't apply to the ux-designer. Heavy hooks block agents from completing for the wrong reasons.

**Do this instead:** Keep TeammateIdle hooks lightweight and observability-focused (the current approach is correct). Let each agent's system prompt define its own completion criteria. If specific quality gates are needed, define them as hooks within individual agent frontmatter, not globally.

### Anti-Pattern 4: Using `commands/` Instead of `skills/`

**What people do:** Create slash commands in `commands/` for new plugin capabilities.

**Why it's wrong:** The `commands/` directory is legacy. Skills (`skills/<name>/SKILL.md`) are the current standard. Skills support directory structure (supporting files), more frontmatter options, and better auto-invocation matching.

**Do this instead:** Use `skills/<name>/SKILL.md` for all new capabilities. Existing commands in `commands/` still work but should be migrated.

### Anti-Pattern 5: Agent Descriptions with <example> Blocks that Consume Context

**What people do:** Add many `<example>` blocks to each agent description, making descriptions 5-10 lines each.

**Why it's wrong:** Agent descriptions are loaded into Claude's context budget at all times. With 12 agents, each having 3-4 example blocks, that is 36-48 extra context entries consuming the skill description budget (2% of context window).

**Do this instead:** Use 1-2 targeted example blocks per agent that show the most differentiating use cases. Keep the description text concise. The system prompt (markdown body) can contain unlimited detail -- it only loads when the agent is spawned.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Claude Code runtime | Plugin auto-discovery from directory structure | No registration API. Plugin placed in directory = loaded at startup |
| Agent Teams | Agents spawned as teammates by Team Lead | Each agent gets own context window. Does not inherit lead's history |
| Subagent system | Agents invocable as subagents outside of teams | Same mechanism, but within a single session |
| GitHub (future) | Plugin installed via `claude plugin install` from marketplace or direct path | Requires publishing to a marketplace or pointing at a local directory |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| plugin.json ↔ component directories | Path declarations (or auto-discovery) | Manifest declares paths; if omitted, defaults are used |
| agents ↔ skills | Agents can preload skills via `skills` frontmatter field | Skills injected into agent's context at spawn time |
| agents ↔ hooks | Agents can define hooks in their own frontmatter | Scoped to agent lifecycle; cleaned up when agent finishes |
| hooks ↔ scripts | hooks.json references scripts via `${CLAUDE_PLUGIN_ROOT}` | Scripts receive JSON on stdin, communicate via exit codes and stdout |
| skills ↔ skills | No direct communication | Skills are independent. The team-templates skill can reference agents by name, but there's no programmatic dependency |
| browse-pool ↔ agents | Skill prompt text lists agent names statically | Not dynamically queried. Must be updated when agents are added |
| assemble-team ↔ agents | Skill prompt text contains agent roster table | Same as above -- static reference, must be manually synced |

## Build Order (Dependencies Between Components)

Based on the architecture above, here is the recommended build order for remaining features:

### Tier 1: No Dependencies (can be done in parallel)

| Work Item | Rationale |
|-----------|-----------|
| Add `<example>` blocks to agent descriptions | Pure content change to existing agent .md files. No structural dependency. Keep to 1-2 examples per agent to avoid context bloat |
| Verify hook event names work | Testing the existing TeammateIdle hook with a real Agent Team session. No code change needed if it works; small fix if event name differs |
| Add additional agents (mobile-developer, ml-engineer, etc.) | New .md files in agents/ directory. No changes to existing components needed |

### Tier 2: Depends on Agent Roster Being Stable

| Work Item | Rationale |
|-----------|-----------|
| Add team-templates skill | References agents by name. Should be built after the agent roster is finalised (after Tier 1 additions are decided). Otherwise the templates reference agents that don't exist yet |
| Update browse-pool and assemble-team | Both skills contain static agent roster tables. Must be updated whenever agents are added. Should happen after Tier 1 agent additions |

### Tier 3: Depends on Features Being Complete

| Work Item | Rationale |
|-----------|-----------|
| Add TaskCompleted hook | Requires understanding which quality checks are appropriate after the agent roster and team-templates are finalised |
| README.md | User-facing documentation. Should describe the final feature set, not a work-in-progress. Write last |
| GitHub publishing | Requires README.md and a stable feature set. Final step |

### Tier 4: Optional / Future

| Work Item | Rationale |
|-----------|-----------|
| MCP server for dynamic roster | Only needed if static skill-based discovery proves insufficient. The current skill-based approach (browse-pool, assemble-team) should be tested first |
| Agent persistent memory | Individual agents could use the `memory` frontmatter field to learn across sessions. Not needed for MVP but valuable for long-running specialist agents |
| Hooks in agent frontmatter | Individual agents could define their own PreToolUse or Stop hooks. Useful for database-specialist (validate queries) or security-auditor (enforce read-only). Consider after core features are stable |

## Key Architectural Decision: Static vs Dynamic Agent Discovery

The current design uses **static references** in skills (browse-pool and assemble-team contain hardcoded agent roster tables). This means:

- Adding a new agent requires updating 3 places: the new .md file, browse-pool's list, and assemble-team's table
- Removing an agent requires updating the same 3 places
- Forgetting to update a skill creates an inconsistency

The alternative is **dynamic discovery** via an MCP server that reads the agents/ directory at runtime and returns the current roster programmatically.

**Recommendation: Keep static for now.** The roster changes infrequently (adding 1-3 agents is a one-time effort), and the static approach is simpler, easier to debug, and requires no running server. Revisit if the roster exceeds 20 agents or changes frequently. MEDIUM confidence -- this is a judgment call, not a technical constraint.

## Verified Facts vs Assumptions

| Claim | Confidence | Source |
|-------|------------|--------|
| Plugin auto-discovers agents/, skills/, hooks/ from default locations | HIGH | Official plugin reference docs |
| `name` is the only required manifest field | HIGH | Official plugin reference docs |
| TeammateIdle fires when a teammate is about to go idle | HIGH | Official hooks reference docs |
| TeammateIdle uses exit codes only (no JSON decision control) | HIGH | Official hooks reference docs |
| TaskCompleted fires when a task is being marked complete | HIGH | Official hooks reference docs |
| `color` field works in agent frontmatter | MEDIUM | Used in existing agents, not explicitly documented as supported field |
| `args` field in skill frontmatter works | LOW | Not in official spec. `argument-hint` is the documented field |
| `<example>` blocks in descriptions improve agent matching | MEDIUM | Plugin validator flagged it, but not explicitly documented in official docs |
| Skills descriptions budget is 2% of context window | HIGH | Official skills docs |

## Sources

- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) -- complete plugin schema and component specs
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) -- all hook events, input/output formats, exit codes
- [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams) -- team architecture, coordination model
- [Claude Code Skills](https://code.claude.com/docs/en/skills) -- skill format, frontmatter, invocation control
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) -- agent frontmatter, tools, hooks, memory
- [Plugins in the Agent SDK](https://platform.claude.com/docs/en/agent-sdk/plugins) -- SDK loading, verification
- [GitHub: claude-code/plugins/README.md](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) -- plugin directory and patterns

---
*Architecture research for: Claude Code Agent Pool Plugin*
*Researched: 2026-02-19*
