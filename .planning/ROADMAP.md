# Roadmap: Agent Pool Plugin

## Overview

This roadmap takes the Agent Pool plugin from a working prototype (12 agents, 2 skills, 1 hook) to a published, production-quality Claude Code plugin. The work moves through five phases: harden the agents for reliable delegation, verify hooks work in real sessions, build out skills with team intelligence, validate the complete plugin end-to-end, then document and ship. Each phase delivers a coherent capability that builds on the previous one.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Agent Hardening** - Refine all 12 agent definitions for reliable discovery, safety defaults, and context efficiency
- [x] **Phase 2: Hook Verification** - Verify and fix the TeammateIdle hook for portability and real-world use
- [x] **Phase 3: Skills Refinement** - Fix skill frontmatter, build team-templates skill, and sync skills with finalized roster
- [x] **Phase 4: Integration Testing** - Validate the complete plugin end-to-end in a real Agent Teams session
- [ ] **Phase 5: Documentation and Distribution** - Write README and CHANGELOG, push to GitHub with proper versioning

## Phase Details

### Phase 1: Agent Hardening
**Goal**: Every agent definition is production-quality -- discoverable by the Team Lead, safe by default, and efficient with context budget
**Depends on**: Nothing (first phase)
**Requirements**: AGNT-01, AGNT-02, AGNT-03, AGNT-04, AGNT-05
**Success Criteria** (what must be TRUE):
  1. Each of the 12 agents has 2-3 natural-language task examples in its description that clearly signal when the Team Lead should delegate to it
  2. Security-auditor agent has tool restrictions limiting it to read-only tools (Read, Grep, Glob, Bash) and runs in plan permission mode
  3. Technical-writer agent has tool restrictions limiting it to documentation tools (Read, Grep, Glob, Write, Edit) and runs in acceptEdits permission mode
  4. All 12 agent descriptions fit within the 2% context window budget when loaded simultaneously (descriptions are concise, under 200 characters)
**Plans**: 4 plans

Plans:
- [x] 01-01-PLAN.md -- Rewrite frontend agents (javascript-developer, react-specialist, ux-designer)
- [x] 01-02-PLAN.md -- Rewrite backend agents (python-developer, backend-architect, systems-programmer, database-specialist)
- [x] 01-03-PLAN.md -- Rewrite remaining agents (qa-tester, security-auditor, devops-engineer, data-scientist, technical-writer)
- [x] 01-04-PLAN.md -- Rename files with number prefixes, update CLAUDE.md, verify all requirements

### Phase 2: Hook Verification
**Goal**: The TeammateIdle hook is verified working in a real Agent Teams environment, portable across systems, and resilient to plugin installation paths
**Depends on**: Phase 1
**Requirements**: HOOK-01, HOOK-02, HOOK-03
**Success Criteria** (what must be TRUE):
  1. The TeammateIdle hook fires correctly when a teammate goes idle during an Agent Teams session
  2. The hook script has a portable shebang (`#!/usr/bin/env bash`), executable bit is tracked in git, and runs without errors on a clean system
  3. Hook script paths use relative references or `${CLAUDE_PLUGIN_ROOT}` that resolve correctly after plugin installation via cache copying
**Plans**: 1 plan

Plans:
- [x] 02-01-PLAN.md -- Harden hook script for portability (shebang, jq removal, executable bit) and verify hooks.json configuration

### Phase 3: Skills Refinement
**Goal**: All skills use correct frontmatter, the team-templates skill provides pre-built compositions, and existing skills reflect the finalized agent roster
**Depends on**: Phase 1 (requires finalized agent roster)
**Requirements**: SKIL-01, SKIL-02, SKIL-03
**Success Criteria** (what must be TRUE):
  1. All skill YAML frontmatter uses the officially documented field names (`user-invocable` not `user_invocable`, `argument-hint` not `args`)
  2. The team-templates skill provides 5-8 pre-built team compositions for common scenarios (full-stack feature, security hardening, new API, etc.) that a user can invoke directly
  3. browse-pool and assemble-team skills list exactly the same agents that exist in the agents/ directory -- no stale references, no missing agents
**Plans**: 2 plans

Plans:
- [x] 03-01-PLAN.md -- Fix frontmatter and sync roster in browse-pool and assemble-team skills
- [x] 03-02-PLAN.md -- Create team-templates skill with 7 pre-built compositions and update CLAUDE.md

### Phase 4: Integration Testing
**Goal**: The complete plugin is verified working end-to-end -- agents load, skills invoke, hooks fire, and installation succeeds
**Depends on**: Phase 1, Phase 2, Phase 3
**Requirements**: TEST-01, TEST-02
**Success Criteria** (what must be TRUE):
  1. In a real Agent Teams session, the Team Lead can discover agents from the pool, delegate tasks to them, and their system prompts load correctly
  2. Skills (browse-pool, assemble-team, team-templates) are invocable during a session and return correct, useful output
  3. Plugin installs successfully via `claude plugin add` or `--plugin-dir` and all components (agents, skills, hooks) are discoverable after installation
**Plans**: 2 plans

Plans:
- [x] 04-01-PLAN.md -- Fix plugin.json validation bug and run automated structural validation of all components
- [x] 04-02-PLAN.md -- Test runtime behavior via --plugin-dir, installation methods, and produce test report

### Phase 5: Documentation and Distribution
**Goal**: The plugin is documented for users, versioned for updates, and published on GitHub for public installation
**Depends on**: Phase 4
**Requirements**: DOCS-01, DOCS-02, DOCS-03, DIST-01, DIST-02
**Success Criteria** (what must be TRUE):
  1. README.md explains what the plugin does, how to install it, lists the agent roster, and includes usage examples that a new user can follow
  2. CHANGELOG.md exists starting at v1.0.0 with a complete description of the initial release
  3. README documents the Agent Teams experimental prerequisite (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) prominently
  4. Plugin is pushed to GitHub as a public repository that anyone can install via `claude plugin add`
  5. plugin.json contains a semantic version number that will be bumped with each future release
**Plans**: TBD

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Agent Hardening | 4/4 | Complete | 2026-02-19 |
| 2. Hook Verification | 1/1 | Complete | 2026-02-19 |
| 3. Skills Refinement | 2/2 | Complete | 2026-02-19 |
| 4. Integration Testing | 2/2 | Complete | 2026-02-19 |
| 5. Documentation and Distribution | 0/? | Not started | - |
