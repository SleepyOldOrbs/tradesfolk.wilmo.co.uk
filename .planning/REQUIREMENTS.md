# Requirements: Agent Pool Plugin

**Defined:** 2026-02-19
**Core Value:** Every specialist agent must have a battle-tested system prompt with clear expertise boundaries so the Team Lead can reliably match tasks to the right expert.

## v1 Requirements

### Agent Quality

- [x] **AGNT-01**: All 12 agent descriptions include natural-language task examples that trigger delegation (2-3 examples per agent)
- [x] **AGNT-02**: Safety-critical agents have tool restrictions via `tools` frontmatter (security-auditor: Read, Grep, Glob, Bash; technical-writer: Read, Grep, Glob, Write, Edit)
- [x] **AGNT-03**: Security-auditor uses `permissionMode: plan` (read-only exploration by default)
- [x] **AGNT-04**: Technical-writer uses `permissionMode: acceptEdits` (auto-accept file edits)
- [x] **AGNT-05**: All agent descriptions are concise enough to fit within the 2% context window budget with 12+ agents loaded

### Hooks

- [ ] **HOOK-01**: TeammateIdle hook event name verified working in a real Agent Teams session
- [ ] **HOOK-02**: Hook script has correct shebang (`#!/usr/bin/env bash`) and executable bit tracked in git
- [ ] **HOOK-03**: Hook script paths use relative references that survive plugin cache copying

### Skills

- [ ] **SKIL-01**: Skill frontmatter uses correct field names per official spec (`user-invocable` not `user_invocable`, `argument-hint` not `args`)
- [ ] **SKIL-02**: Team-templates skill provides 5-8 pre-built team compositions for common scenarios (full-stack feature, security hardening, new API, etc.)
- [ ] **SKIL-03**: browse-pool and assemble-team skills are synced with the finalized agent roster

### Testing

- [ ] **TEST-01**: Plugin tested end-to-end in a real Agent Team session (agents discoverable, system prompts load, skills invocable)
- [ ] **TEST-02**: Plugin install via `claude plugin add` or `--plugin-dir` verified working

### Documentation

- [ ] **DOCS-01**: README.md with install instructions, what the plugin does, agent roster table, usage examples
- [ ] **DOCS-02**: CHANGELOG.md starting at v1.0.0 with current state
- [ ] **DOCS-03**: Agent Teams experimental prerequisite documented (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)

### Distribution

- [ ] **DIST-01**: Plugin pushed to GitHub as a public repository
- [ ] **DIST-02**: Semantic versioning maintained in plugin.json (version bumped with every release)

## v2 Requirements

### Enhanced Agents

- **EAGN-01**: maxTurns set per agent (lightweight agents: 15, standard: 30, complex: 50)
- **EAGN-02**: Model tiering strategy (lightweight agents on sonnet, complex agents inherit)
- **EAGN-03**: 3-6 additional specialist agents based on user requests (mobile-developer, ml-engineer, accessibility-specialist)

### Quality Hooks

- **QHOK-01**: TaskCompleted hook with domain-aware quality validation
- **QHOK-02**: SubagentStart/SubagentStop logging hooks for observability

### Tooling

- **TOOL-01**: Agent roster validation script (validates frontmatter schema, required fields, valid colors, description length)

### Advanced Features

- **ADVF-01**: Persistent agent memory (`memory: project`) for 2-3 key agents (backend-architect, qa-tester)
- **ADVF-02**: Skills preloaded into agents via `skills` frontmatter field
- **ADVF-03**: Marketplace-ready distribution (marketplace.json, verified install flow)

## Out of Scope

| Feature | Reason |
|---------|--------|
| MCP server for dynamic roster | Over-engineering for a static roster of 12-20 agents. Markdown files are directly readable |
| Auto-spawning agents based on file type | Removes user control, creates unexpected token costs. Team Lead already handles matching |
| Agent-to-agent dependency chains | Creates deadlocks, blocks parallel execution. Use task dependencies instead |
| Dozens of hyper-specialized agents (30+) | Dilutes quality, causes choice paralysis, exceeds context budget. Cap at 15-18 max |
| Custom system prompt injection / templates | Breaks curated quality proposition. Users can override via `.claude/agents/` |
| GUI / web dashboard | This is a CLI plugin. Terminal output with colour-coding is sufficient |
| Heavy PreToolUse validation hooks | Creates friction. Use `tools`/`disallowedTools` frontmatter for static restrictions |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AGNT-01 | Phase 1: Agent Hardening | Complete |
| AGNT-02 | Phase 1: Agent Hardening | Complete |
| AGNT-03 | Phase 1: Agent Hardening | Complete |
| AGNT-04 | Phase 1: Agent Hardening | Complete |
| AGNT-05 | Phase 1: Agent Hardening | Complete |
| HOOK-01 | Phase 2: Hook Verification | Pending |
| HOOK-02 | Phase 2: Hook Verification | Pending |
| HOOK-03 | Phase 2: Hook Verification | Pending |
| SKIL-01 | Phase 3: Skills Refinement | Pending |
| SKIL-02 | Phase 3: Skills Refinement | Pending |
| SKIL-03 | Phase 3: Skills Refinement | Pending |
| TEST-01 | Phase 4: Integration Testing | Pending |
| TEST-02 | Phase 4: Integration Testing | Pending |
| DOCS-01 | Phase 5: Documentation and Distribution | Pending |
| DOCS-02 | Phase 5: Documentation and Distribution | Pending |
| DOCS-03 | Phase 5: Documentation and Distribution | Pending |
| DIST-01 | Phase 5: Documentation and Distribution | Pending |
| DIST-02 | Phase 5: Documentation and Distribution | Pending |

**Coverage:**
- v1 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Requirements defined: 2026-02-19*
*Last updated: 2026-02-19 after roadmap creation (5-phase structure)*
