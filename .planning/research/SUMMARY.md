# Project Research Summary

**Project:** Agent Pool -- Claude Code Plugin
**Domain:** Claude Code plugin development (specialist agent roster for Agent Teams)
**Researched:** 2026-02-19
**Confidence:** HIGH

## Executive Summary

The Agent Pool plugin is a pure-configuration Claude Code plugin -- markdown files, JSON manifests, and shell scripts with zero runtime dependencies. There is no application framework, no database, no build step. The "stack" is the Claude Code plugin system itself, which auto-discovers agents from `agents/*.md`, skills from `skills/*/SKILL.md`, and hooks from `hooks/hooks.json`. The existing codebase already has the foundational structure right: 12 specialist agents with consistent three-section system prompts, two working skills, and a lightweight TeammateIdle hook. The core architecture is sound and needs refinement, not rebuilding.

The recommended approach is to focus on making the existing agents more discoverable (better description fields, tool restrictions, permission modes), verifying everything works end-to-end with a real Agent Teams session, and then packaging for distribution with proper documentation. The competitive landscape shows two strategies: breadth (100+ agents) or depth (fewer agents, better defaults). This plugin should compete on depth -- curated prompts, sensible tool restrictions, permission modes, and team composition intelligence. The "12 specialists from a directory" metaphor is the differentiator. Do not chase agent count.

The key risks are: (1) agent descriptions are the sole mechanism Claude uses for task delegation, and weak descriptions mean the plugin silently fails to add value; (2) TeammateIdle hooks depend on the experimental Agent Teams feature which is gated behind a flag and may change; (3) plugin path references can break silently when installed via marketplace due to cache copying; and (4) the `color` field and `<example>` blocks in descriptions are not fully documented in official specs and may not work as expected. All of these are mitigable with testing and documentation, but they must be addressed before publishing.

## Key Findings

### Recommended Stack

This plugin has no traditional stack. It is static files consumed by the Claude Code runtime. See `.planning/research/STACK.md` for the complete plugin API reference.

**Core technologies:**
- **Claude Code Plugin System (v1.0.33+):** Plugin manifest, auto-discovery of agents/skills/hooks -- this IS the platform
- **Markdown + YAML frontmatter:** Official format for agent and skill definitions, no alternatives exist
- **JSON:** Plugin manifest (`plugin.json`), hooks config (`hooks.json`), MCP config (`.mcp.json`)
- **Bash + jq:** Hook command handlers; scripts receive JSON on stdin, return decisions via exit codes

**Critical version note:** Agent Teams requires Claude Code v2.0+ and the experimental flag `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. The `color` field in agent frontmatter is functional but undocumented.

### Expected Features

See `.planning/research/FEATURES.md` for the full prioritization matrix and competitor analysis.

**Must have (table stakes for v1.0.0):**
- `<example>` blocks (or natural-language equivalents) in all 12 agent descriptions -- improves auto-delegation accuracy
- Tool restrictions on safety-critical agents (security-auditor: read-only, technical-writer: read + edit)
- Permission modes (security-auditor: `plan`, technical-writer: `acceptEdits`)
- Verified hook events work in current Claude Code version
- End-to-end testing with a real Agent Team session
- README.md with install instructions and usage examples
- CHANGELOG.md for version tracking

**Should have (v1.x differentiators):**
- Team templates skill -- pre-built compositions for common scenarios (full-stack feature, security hardening)
- maxTurns per agent to prevent runaways
- Model tiering (lightweight agents on sonnet, complex agents inherit)
- Agent roster validation script for contributors
- SubagentStart/SubagentStop logging hooks

**Defer (v2+):**
- Persistent agent memory (`memory: project`)
- Skills preloaded into agents via `skills` frontmatter
- TaskCompleted hook with domain-aware validation
- Marketplace distribution
- Additional specialist agents beyond 15-18 max

### Architecture Approach

The architecture is directory-convention-based: Claude Code auto-discovers components from standard locations. The plugin manifest (`plugin.json`) lives in `.claude-plugin/` and is the only file in that directory. All other components (agents, skills, hooks) live at the plugin root. Static references in skills (browse-pool and assemble-team contain hardcoded agent roster tables) create a maintenance coupling -- adding an agent requires updating three places. This is acceptable for a roster under 20 agents but should be revisited if the pool grows. See `.planning/research/ARCHITECTURE.md` for full data flow and build order.

**Major components:**
1. **`agents/*.md`** -- Specialist definitions with YAML frontmatter (name, description, model, color, tools, permissionMode) and system prompt body
2. **`skills/*/SKILL.md`** -- User/Claude-invocable capabilities (browse-pool for discovery, assemble-team for recommendations, team-templates planned)
3. **`hooks/hooks.json` + scripts** -- Event handlers for TeammateIdle (and future TaskCompleted); scripts use jq + bash, communicate via exit codes
4. **`.claude-plugin/plugin.json`** -- Plugin identity and metadata; only `name` required if using auto-discovery defaults

### Critical Pitfalls

See `.planning/research/PITFALLS.md` for the full list with recovery strategies.

1. **Vague agent descriptions break delegation** -- Claude uses description text as the sole mechanism for matching tasks to agents. Write descriptions that answer "when should Claude delegate to this agent?" with specific task triggers. Keep under 200 characters.
2. **TeammateIdle depends on experimental Agent Teams** -- The hook only fires when Agent Teams is enabled via flag. Document the prerequisite. Keep the hook non-blocking so the plugin is useful with or without Agent Teams.
3. **Plugin paths break after marketplace install** -- Cache copying means paths outside the plugin root silently fail. Always use `${CLAUDE_PLUGIN_ROOT}` in hook commands. Test the install path, not just the dev path.
4. **Hook scripts lose executable bits in Git** -- Use `git update-index --chmod=+x` to track permissions. Use `#!/usr/bin/env bash` for portability.
5. **Version not bumped = users never see updates** -- Claude Code caches plugins by version. Bump `plugin.json` version with every release or existing users get stale code.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Agent Hardening

**Rationale:** The agent descriptions are the single most important thing to get right -- they control whether the plugin adds any value at all. Tool restrictions and permission modes are table stakes that competitors already have. This phase has zero structural dependencies and can begin immediately.

**Delivers:** Production-quality agent definitions with proper discovery, safety defaults, and sensible constraints.

**Addresses:** `<example>` blocks / natural-language task triggers in descriptions, `tools`/`disallowedTools` for safety-critical agents, `permissionMode` for security-auditor and technical-writer, concise descriptions under context budget.

**Avoids:** Pitfall 1 (vague descriptions), Pitfall 4 (skill budget overflow from bloated descriptions).

### Phase 2: Hook Verification and Testing

**Rationale:** The existing TeammateIdle hook must be verified before publishing. This requires enabling Agent Teams and running a real session. This phase also catches issues with executable bits, jq dependency, and the experimental feature gate.

**Delivers:** Verified, working hooks; documented prerequisites; end-to-end test confirmation that agents are discoverable and system prompts load correctly.

**Addresses:** Hook event verification, end-to-end testing with Agent Team session, hook script portability (shebang, chmod).

**Avoids:** Pitfall 2 (experimental feature dependency), Pitfall 6 (non-executable scripts).

### Phase 3: Skills and Team Intelligence

**Rationale:** Depends on a stable agent roster (Phase 1). Team templates reference agents by name, so the roster should be finalized first. The assemble-team and browse-pool skills also need updating if any agents were added or renamed.

**Delivers:** Team templates skill with 5-8 pre-built compositions, updated browse-pool and assemble-team skills synced to the finalized roster.

**Addresses:** Team templates skill (P2 differentiator), roster sync between skills and agents directory.

**Avoids:** Architecture anti-pattern of stale static references.

### Phase 4: Documentation and Distribution

**Rationale:** README should describe the final feature set, not a work-in-progress. Marketplace publishing requires README, CHANGELOG, tested install flow, and stable versioning. This is the last phase because all features must be complete and verified.

**Delivers:** README.md, CHANGELOG.md, verified marketplace install flow, GitHub public repo.

**Addresses:** README with install instructions, CHANGELOG, semantic versioning discipline, marketplace-ready packaging.

**Avoids:** Pitfall 3 (path breakage after install), Pitfall 5 (version not bumped).

### Phase 5: Post-Launch Enhancements (v1.x)

**Rationale:** These features add value but require real-world usage data to inform implementation. maxTurns values need observation of actual agent behavior. Model tiering needs cost/quality tradeoff data. Validation script needs contributor demand.

**Delivers:** maxTurns per agent, model tiering, validation script, SubagentStart/Stop logging hooks.

**Addresses:** P2 features from the prioritization matrix.

### Phase Ordering Rationale

- **Phase 1 before Phase 2:** Agent descriptions must be refined before end-to-end testing, otherwise the test validates broken discovery behavior.
- **Phase 2 before Phase 3:** Hook verification confirms the Agent Teams integration works, which is prerequisite knowledge for building team templates.
- **Phase 3 before Phase 4:** Skills must be finalized before documentation, otherwise README describes incomplete functionality.
- **Phase 5 deferred:** These features require real usage feedback and have no blockers on launch readiness.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2:** The `<example>` block format needs empirical testing -- official docs do not confirm the XML-like syntax. May need to use natural-language equivalents instead. Test both approaches.
- **Phase 3:** The `args` field in assemble-team's skill frontmatter is not in the official spec (`argument-hint` is the documented field). Verify before building new skills.
- **Phase 5:** The `memory` field for persistent agent memory needs testing in a plugin context to confirm memory file paths resolve correctly after installation.

Phases with standard patterns (skip research-phase):
- **Phase 1:** Agent frontmatter fields (`tools`, `disallowedTools`, `permissionMode`) are thoroughly documented in official Claude Code docs with high confidence.
- **Phase 4:** Plugin distribution via marketplace is well-documented with clear requirements.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Official Claude Code docs verified via Context7. Plugin system is stable (v1.0.33+). Zero ambiguity on manifest schema, component paths, and auto-discovery. |
| Features | HIGH | Official docs verified all supported frontmatter fields. Competitor analysis provides clear positioning guidance. MVP scope is well-defined. |
| Architecture | HIGH | Directory-convention architecture is dictated by Claude Code itself -- no design decisions to get wrong. Data flows verified against official docs. |
| Pitfalls | HIGH | All pitfalls verified against official docs. Recovery costs are universally low. The `color` field and `<example>` blocks are the only areas with medium confidence. |

**Overall confidence:** HIGH

### Gaps to Address

- **`<example>` blocks in descriptions:** The STACK and ARCHITECTURE research both note that `<example>` block syntax is suggested by the plugin validator and generated by `/agents`, but not explicitly documented in the official subagent specification. The PITFALLS research recommends natural-language alternatives. Test both approaches empirically during Phase 1/2.
- **`color` field acceptance:** Functional but undocumented. The exact set of accepted color values should be verified by testing. Currently using: blue, cyan, green, yellow, magenta, red. The value `purple` may also be accepted.
- **`args` vs `argument-hint` in skill frontmatter:** The current assemble-team skill uses `args` which is not in the official spec. Verify whether it works or needs migration to `argument-hint`.
- **Agent Teams stability:** The feature is experimental. Hook event schemas could change. Build hooks defensively with graceful fallbacks.
- **jq dependency:** Hook scripts assume `jq` is installed. Either document as prerequisite, bundle a fallback parser, or remove the dependency.

## Sources

### Primary (HIGH confidence)
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference) -- complete manifest schema, component specs, CLI commands
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) -- all 14 hook events, input/output schemas, exit codes
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) -- agent frontmatter fields, tools, permissions, memory
- [Claude Code Skills](https://code.claude.com/docs/en/skills) -- SKILL.md format, frontmatter, invocation control, budget limits
- [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams) -- team architecture, TeammateIdle/TaskCompleted hooks
- [Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) -- distribution, versioning, source types
- Context7: `/websites/code_claude_en_plugins-reference` -- verified manifest schema
- Context7: `/anthropics/claude-code` -- verified hook events list

### Secondary (MEDIUM confidence)
- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) -- 127+ agents, community patterns
- [wshobson/agents](https://github.com/wshobson/agents) -- 73 plugins, three-tier model strategy, team presets
- [GitHub Issue #8501](https://github.com/anthropics/claude-code/issues/8501) -- `color` field discrepancy documentation
- Context7: `/affaan-m/everything-claude-code` -- community agent patterns

### Tertiary (LOW confidence)
- `<example>` block syntax in agent descriptions -- suggested by validator, generated by `/agents` command, but not in official subagent spec. Needs empirical validation.
- `args` field in skill frontmatter -- used in current code but not in official spec. May be silently ignored.

---
*Research completed: 2026-02-19*
*Ready for roadmap: yes*
