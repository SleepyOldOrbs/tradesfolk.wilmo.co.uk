# Feature Research

**Domain:** Claude Code agent pool plugin (specialist agent roster for Agent Teams)
**Researched:** 2026-02-19
**Confidence:** HIGH (official docs verified, competitor repos analyzed)

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = plugin feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **README.md with install instructions** | Every GitHub plugin has one. Users won't even try the plugin without clear setup steps | LOW | Include: one-liner install, what it does, screenshot/GIF of `/browse-pool`, badge for Claude Code version |
| **`<example>` blocks in agent descriptions** | Official docs show Claude uses the `description` field for auto-delegation. Example blocks improve matching accuracy. Validator already flags this | LOW | Format: `<example>Refactor the auth middleware to use async/await</example>`. 2-3 per agent |
| **Tool restrictions per agent** | Official subagent spec supports `tools` and `disallowedTools`. A read-only agent (technical-writer) should not have Write access by default. Competitors do this | MEDIUM | Use `tools` frontmatter field. E.g., technical-writer: `Read, Grep, Glob`. security-auditor: `Read, Grep, Glob, Bash`. qa-tester: all tools |
| **Verified hook event names** | STATUS.md flags `TeammateIdle` as unverified. Official docs confirm it IS valid, plus `TaskCompleted`. Both are standard hook events for agent teams | LOW | `TeammateIdle` is correct. Also add `TaskCompleted` hook |
| **Plugin tested with real Agent Team session** | Cannot ship without verifying agents are actually discoverable, system prompts load correctly, and skills work end-to-end | LOW | Manual testing, but critical. Document results in STATUS.md |
| **CHANGELOG.md** | Plugin reference docs explicitly recommend including one. Users expect version history for any plugin they install | LOW | Start at v1.0.0 with current state |
| **Semantic versioning in plugin.json** | Docs state: "Claude Code uses the version to determine whether to update your plugin. If you change code but don't bump version, users won't see changes" | LOW | Already has `"version": "1.0.0"` but needs to be kept current |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Team templates skill** | Pre-built team compositions for common scenarios (full-stack feature, security hardening, new API). No competitor does curated team composition recommendations | MEDIUM | Already planned in STATUS.md. 5-8 templates. Invoke with `/agent-pool:team-template full-stack-feature`. Return agent names + roles + suggested task breakdown |
| **Persistent agent memory** | Official spec supports `memory: user\|project\|local`. Agents that learn project patterns across sessions (e.g., code-reviewer remembers recurring issues). No agent pool plugin does this yet | MEDIUM | Add `memory: project` to 2-3 agents (backend-architect, qa-tester). Requires adding memory field to frontmatter + memory instructions in system prompts |
| **Permission modes per agent** | Official spec supports `permissionMode`. Security-auditor in `plan` mode (read-only exploration). Technical-writer in `acceptEdits`. Provides sensible safety defaults | LOW | Add `permissionMode` to frontmatter. Most agents: `default`. security-auditor: `plan`. technical-writer: `acceptEdits` |
| **Skills preloaded into agents** | Official spec supports `skills` field in agent frontmatter. Agents can have domain knowledge injected at startup. E.g., backend-architect gets `api-conventions` skill content | MEDIUM | Requires creating supporting skills in `skills/` directory. Start with 1-2 demonstration skills, e.g., `code-quality-standards` preloaded into qa-tester |
| **TaskCompleted hook with domain-aware validation** | Official spec confirms `TaskCompleted` hook event. Use `type: agent` hook to run a lightweight verification agent that checks work quality based on the specialist type. Exit code 2 blocks completion with feedback | HIGH | Requires a validation script/agent that understands specialist context. More sophisticated than the lightweight TeammateIdle hook. Could be a strong differentiator |
| **maxTurns per agent** | Prevent runaway agents. Official spec supports `maxTurns`. Lightweight agents (technical-writer) get fewer turns; complex agents (backend-architect) get more | LOW | Add to frontmatter. Suggested: haiku-tier agents 15 turns, standard 30, complex 50 |
| **Model tiering strategy** | Competitors (wshobson/agents) use a three-tier model strategy. Route lightweight tasks to haiku, complex to opus. Cost optimization that users appreciate | LOW | Currently all `model: inherit`. Change to: technical-writer/qa-tester `model: sonnet`, backend-architect/security-auditor `model: inherit` (let user decide for expensive agents), others `inherit` |
| **Agent roster validation script** | A script that validates all agent files against the schema (required frontmatter fields, valid colors, description length, example blocks present). Run in CI or pre-commit | LOW | Shell or Node script in `scripts/validate-roster.sh`. Makes contributing agents easier. Useful for community PRs |
| **SubagentStart/SubagentStop hooks** | Official spec supports these events. Log when specialists are spawned/finished. Useful for observability and debugging team sessions | LOW | Add to hooks.json. Lightweight logging, same pattern as existing TeammateIdle hook |
| **Marketplace-ready distribution** | Official plugin docs describe marketplace.json for distributing plugins. Being in a marketplace is the primary discovery mechanism | MEDIUM | Create a marketplace.json or ensure compatibility with existing marketplaces (e.g., Anthropic's official marketplace) |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| **MCP server for dynamic roster** | STATUS.md mentions this as low priority. Programmatic querying sounds powerful | Massive over-engineering for a static roster of 12-20 agents. MCP servers add runtime dependencies, startup latency, and failure modes. The agents are just markdown files -- Claude can read them directly | Keep agents as plain markdown. The `browse-pool` skill already provides discovery. If programmatic access is needed later, a simple JSON index file is sufficient |
| **Auto-spawning agents based on file type** | Automatically assign javascript-developer when .js files are touched | Removes user control. Creates unexpected token costs. The team lead already matches agents to tasks via descriptions. Hooks that auto-spawn agents violate the "team lead coordinates" pattern | Improve description fields and example blocks so the team lead makes better matching decisions naturally |
| **Agent-to-agent dependency chains** | "backend-architect must approve before database-specialist starts" | Creates deadlocks, coordination complexity, and blocks parallel execution -- exactly what agent teams are designed to avoid. Agent teams already have task dependencies for this | Use task dependencies in the shared task list instead. Document recommended workflows in team-templates skill |
| **Dozens of hyper-specialized agents** | Competitor has 127+ agents. More coverage sounds better | Dilutes quality. Users face choice paralysis. Most tasks need 3-5 generalists, not 30 specialists. Agent descriptions compete for context window budget (2% of context). Every added agent slightly degrades matching for all agents | Cap at 15-18 agents max. Each must cover genuinely distinct expertise. Refer users to custom subagent creation for niche needs |
| **Custom system prompt injection / prompt templates** | Let users customize agent prompts without editing files | Breaks the curated quality proposition. The whole value is that these are battle-tested prompts, not templates. Customization leads to broken agents and support burden | Users can override by creating same-named agents in `.claude/agents/` (higher priority scope). Document this escape hatch |
| **GUI / web dashboard for the roster** | Visual management of agents | This is a CLI plugin. Adding a web UI is a different product entirely. Adds massive maintenance surface | The `/browse-pool` skill IS the UI. Terminal output with colour-coding is sufficient for the target audience |
| **Heavy PreToolUse validation hooks** | Block unsafe operations per-agent (e.g., prevent qa-tester from deploying) | Creates friction that slows down legitimate work. Tool restrictions via `tools`/`disallowedTools` are the correct mechanism, not runtime hooks that inspect every tool call | Use `tools` and `disallowedTools` frontmatter fields for static restrictions. Reserve hooks for lightweight observability |

## Feature Dependencies

```
[<example> blocks in descriptions]
    (no dependencies -- can be done first)

[Tool restrictions per agent]
    (no dependencies -- parallel with example blocks)

[Permission modes per agent]
    (no dependencies -- parallel)

[README.md]
    └──benefits-from──> [Verified hook events]
    └──benefits-from──> [Plugin tested with real session]

[Team templates skill]
    └──enhances──> [assemble-team skill] (templates are pre-built team compositions)

[Persistent agent memory]
    └──requires──> [Plugin tested with real session] (need to verify memory paths work)

[TaskCompleted hook]
    └──requires──> [Verified hook events]
    └──enhances──> [TeammateIdle hook] (complementary quality gates)

[Skills preloaded into agents]
    └──requires──> [New supporting skills created in skills/ directory]
    └──enhances──> [Tool restrictions per agent] (skills + tool limits = focused agents)

[Marketplace distribution]
    └──requires──> [README.md]
    └──requires──> [CHANGELOG.md]
    └──requires──> [Semantic versioning]
    └──requires──> [Plugin tested with real session]

[Agent roster validation script]
    └──enhances──> [<example> blocks] (validates they exist)
    └──enhances──> [Tool restrictions] (validates they're valid tool names)
```

### Dependency Notes

- **Team templates requires assemble-team**: Templates are essentially pre-built responses for the assemble-team skill. They share the same agent roster and could reference each other.
- **Persistent memory requires real testing**: Memory paths (`~/.claude/agent-memory/` or `.claude/agent-memory/`) need verification in a live plugin context. The official docs are clear on the mechanism but untested with plugin-scoped agents.
- **Marketplace requires all table stakes**: A plugin in a marketplace is held to higher standards. README, versioning, and changelog are prerequisites.
- **Validation script enhances all agent changes**: Any time agent frontmatter is modified (example blocks, tools, permissions, memory), the validation script catches errors early.

## MVP Definition

### Launch With (v1.0.0)

Minimum viable product -- what's needed for a credible GitHub release.

- [x] 12 specialist agents with consistent three-section system prompts (DONE)
- [x] browse-pool skill (DONE)
- [x] assemble-team skill (DONE)
- [x] TeammateIdle hook (DONE)
- [ ] `<example>` blocks in all agent descriptions -- improves auto-delegation accuracy
- [ ] Tool restrictions on agents that should be read-only or limited -- safety baseline
- [ ] Permission modes for security-auditor (plan) and technical-writer (acceptEdits) -- sensible defaults
- [ ] Verified hook events work in current Claude Code version -- confidence in shipping
- [ ] Plugin tested end-to-end with a real Agent Team session -- cannot ship untested
- [ ] README.md with install instructions, usage examples, roster table -- GitHub landing page
- [ ] CHANGELOG.md -- version history for users

### Add After Validation (v1.x)

Features to add once core is working and users have tried it.

- [ ] Team templates skill -- add once assemble-team is validated with real usage
- [ ] maxTurns per agent -- add once turn-count behaviour is observed in practice
- [ ] Model tiering (sonnet for lightweight agents) -- add once cost impact is understood
- [ ] Agent roster validation script -- add when community contributions start arriving
- [ ] SubagentStart/SubagentStop logging hooks -- add for better debugging experience

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] Persistent agent memory -- powerful but complex; needs real usage patterns to inform which agents benefit
- [ ] Skills preloaded into agents -- requires creating high-quality supporting skills first
- [ ] TaskCompleted hook with domain-aware validation -- high complexity, wait for user demand
- [ ] Marketplace distribution -- wait until plugin is battle-tested by early adopters
- [ ] 3-6 additional specialist agents (mobile-developer, ml-engineer, accessibility-specialist) -- add based on user requests, not speculation

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| `<example>` blocks in descriptions | HIGH | LOW | P1 |
| Tool restrictions per agent | HIGH | LOW | P1 |
| Permission modes per agent | MEDIUM | LOW | P1 |
| README.md | HIGH | LOW | P1 |
| CHANGELOG.md | MEDIUM | LOW | P1 |
| Verify hook events | HIGH | LOW | P1 |
| End-to-end testing | HIGH | LOW | P1 |
| Team templates skill | HIGH | MEDIUM | P2 |
| maxTurns per agent | MEDIUM | LOW | P2 |
| Model tiering | MEDIUM | LOW | P2 |
| Validation script | MEDIUM | LOW | P2 |
| SubagentStart/Stop hooks | LOW | LOW | P2 |
| Persistent agent memory | HIGH | MEDIUM | P3 |
| Skills preloaded into agents | MEDIUM | MEDIUM | P3 |
| TaskCompleted validation hook | MEDIUM | HIGH | P3 |
| Marketplace distribution | HIGH | MEDIUM | P3 |
| Additional specialist agents | MEDIUM | MEDIUM | P3 |

**Priority key:**
- P1: Must have for v1.0.0 launch
- P2: Should have, add in v1.x releases
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | VoltAgent/awesome-subagents (127 agents) | wshobson/agents (73 plugins, 112 agents) | Agent Pool (this plugin) |
|---------|-------------------------------------------|------------------------------------------|--------------------------|
| Agent count | 127+ across 10 categories | 112 across 24 categories | 12 across 6 domains |
| Organization | Flat list by category | Plugin-bundled (agents inside plugins) | Single plugin, agents/ directory |
| Tool restrictions | Per-agent | Per-agent | Not yet (planned P1) |
| Model tiering | Not documented | Three-tier (Opus/Sonnet/Haiku) | All `inherit` (planned P2) |
| Team compositions | Not provided | 7 presets (review, debug, feature, etc.) | assemble-team skill (templates planned P2) |
| Quality hooks | Not provided | Not documented | TeammateIdle hook (TaskCompleted planned P3) |
| Skills | Not bundled | 146 skills across plugins | 2 skills (more planned P3) |
| Memory | Not provided | Conductor plugin has session persistence | Not yet (planned P3) |
| Installation | Script installer, manual copy, marketplace | Marketplace install | Manual / --plugin-dir (marketplace planned P3) |
| Validation | Not provided | Not documented | Planned P2 |
| Documentation | README with categories and descriptions | Progressive disclosure README | CLAUDE.md exists, README planned P1 |

**Key insight:** Competitors compete on breadth (100+ agents). This plugin should compete on **depth and curation** -- fewer agents, better prompts, proper tool restrictions, sensible defaults, and team composition intelligence. The "12 specialists from a directory" metaphor is the differentiator, not "127 agents dumped in a folder."

## Sources

- [Official Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents) -- HIGH confidence. Verified all supported frontmatter fields: name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory
- [Official Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference) -- HIGH confidence. Verified plugin.json schema, hook events (TeammateIdle, TaskCompleted confirmed), component paths, marketplace distribution
- [Official Claude Code plugins guide](https://code.claude.com/docs/en/plugins) -- HIGH confidence. Plugin structure, testing with --plugin-dir, skill format, agent discovery
- [Official Claude Code agent teams documentation](https://code.claude.com/docs/en/agent-teams) -- HIGH confidence. TeammateIdle and TaskCompleted hooks confirmed. Team architecture, task coordination, teammate spawning
- [Official Claude Code skills documentation](https://code.claude.com/docs/en/skills) -- HIGH confidence. SKILL.md frontmatter fields, context: fork, agent field, progressive disclosure
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) -- MEDIUM confidence. 127+ agents, 10 categories, installer script pattern
- [wshobson/agents](https://github.com/wshobson/agents) -- MEDIUM confidence. 73 plugins, 112 agents, three-tier model strategy, progressive disclosure architecture
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) -- MEDIUM confidence. Community patterns, popular tool features, adoption signals

---
*Feature research for: Claude Code agent pool plugin*
*Researched: 2026-02-19*
