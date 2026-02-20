# Roadmap: Agent Pool Plugin

## Milestones

- ✅ **v1.0.0 Initial Release** - Phases 1-5 (shipped 2026-02-19)
- 🚧 **v1.1.0 Agent Pool Expansion** - Phases 6-9 (in progress)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

<details>
<summary>v1.0.0 Initial Release (Phases 1-5) - SHIPPED 2026-02-19</summary>

- [x] **Phase 1: Agent Hardening** - Refine all 12 agent definitions for reliable discovery, safety defaults, and context efficiency
- [x] **Phase 2: Hook Verification** - Verify and fix the TeammateIdle hook for portability and real-world use
- [x] **Phase 3: Skills Refinement** - Fix skill frontmatter, build team-templates skill, and sync skills with finalized roster
- [x] **Phase 4: Integration Testing** - Validate the complete plugin end-to-end in a real Agent Teams session
- [x] **Phase 5: Documentation and Distribution** - Write README and CHANGELOG, push to GitHub with proper versioning

</details>

### v1.1.0 Agent Pool Expansion

- [x] **Phase 6: Agent Authoring** - Author 8 new specialist agents and update 4 existing agents with boundary commentary
- [x] **Phase 7: Skills Updates** - Update browse-pool, assemble-team, and team-templates with 20-agent roster and 5 new templates (2026-02-20)
- [x] **Phase 8: Documentation** - Update CLAUDE.md roster, README.md, CHANGELOG.md, and bump plugin.json to v1.1.0 (2026-02-20)
- [x] **Phase 9: Verification** - Verify auto-discovery, context budget, and cross-file colour consistency for all 20 agents (2026-02-20)

## Phase Details

<details>
<summary>v1.0.0 Initial Release (Phases 1-5) - SHIPPED 2026-02-19</summary>

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
- [x] 01-01: Rewrite frontend agents (javascript-developer, react-specialist, ux-designer)
- [x] 01-02: Rewrite backend agents (python-developer, backend-architect, systems-programmer, database-specialist)
- [x] 01-03: Rewrite remaining agents (qa-tester, security-auditor, devops-engineer, data-scientist, technical-writer)
- [x] 01-04: Rename files with number prefixes, update CLAUDE.md, verify all requirements

### Phase 2: Hook Verification
**Goal**: The TeammateIdle hook is verified working in a real Agent Teams environment, portable across systems, and resilient to plugin installation paths
**Depends on**: Phase 1
**Requirements**: HOOK-01, HOOK-02, HOOK-03
**Success Criteria** (what must be TRUE):
  1. The TeammateIdle hook fires correctly when a teammate goes idle during an Agent Teams session
  2. The hook script has a portable shebang, executable bit tracked in git, and runs without errors on a clean system
  3. Hook script paths use relative references or `${CLAUDE_PLUGIN_ROOT}` that resolve correctly after plugin installation
**Plans**: 1 plan

Plans:
- [x] 02-01: Harden hook script for portability and verify hooks.json configuration

### Phase 3: Skills Refinement
**Goal**: All skills use correct frontmatter, the team-templates skill provides pre-built compositions, and existing skills reflect the finalized agent roster
**Depends on**: Phase 1
**Requirements**: SKIL-01, SKIL-02, SKIL-03
**Success Criteria** (what must be TRUE):
  1. All skill YAML frontmatter uses officially documented field names
  2. The team-templates skill provides 7 pre-built team compositions for common scenarios
  3. browse-pool and assemble-team skills list exactly the same agents that exist in agents/
**Plans**: 2 plans

Plans:
- [x] 03-01: Fix frontmatter and sync roster in browse-pool and assemble-team skills
- [x] 03-02: Create team-templates skill with 7 pre-built compositions and update CLAUDE.md

### Phase 4: Integration Testing
**Goal**: The complete plugin is verified working end-to-end
**Depends on**: Phase 1, Phase 2, Phase 3
**Requirements**: TEST-01, TEST-02
**Success Criteria** (what must be TRUE):
  1. Team Lead can discover agents from the pool, delegate tasks, and system prompts load correctly
  2. Skills are invocable during a session and return correct output
  3. Plugin installs successfully and all components are discoverable
**Plans**: 2 plans

Plans:
- [x] 04-01: Fix plugin.json validation bug and run automated structural validation
- [x] 04-02: Test runtime behavior via --plugin-dir and produce test report

### Phase 5: Documentation and Distribution
**Goal**: The plugin is documented, versioned, and published on GitHub
**Depends on**: Phase 4
**Requirements**: DOCS-01, DOCS-02, DOCS-03, DIST-01, DIST-02
**Success Criteria** (what must be TRUE):
  1. README.md explains what the plugin does, how to install it, and lists the agent roster
  2. CHANGELOG.md exists at v1.0.0 with complete initial release description
  3. Plugin is pushed to GitHub as a public repository
**Plans**: 2 plans

Plans:
- [x] 05-01: Create README.md, CHANGELOG.md, update .gitignore, verify plugin.json version
- [x] 05-02: Push to GitHub as public repository, create v1.0.0 release

</details>

### Phase 6: Agent Authoring
**Goal**: The agent pool grows from 12 to 20 specialists, each with battle-tested system prompts and clear expertise boundaries that prevent delegation confusion
**Depends on**: Phase 5 (v1.0 complete)
**Requirements**: AGNT-06, AGNT-07, AGNT-08, AGNT-09, AGNT-10, AGNT-11, AGNT-12, AGNT-13, AGNT-14, AGNT-15
**Success Criteria** (what must be TRUE):
  1. All 8 new agent files exist in `agents/` with valid YAML frontmatter and three-section system prompts (core expertise, working standards, task workflow)
  2. Each new agent description contains exactly 3 `<example>` blocks with disambiguation commentary that clearly distinguishes it from overlapping agents
  3. Every new agent description is between 1,800 and 2,200 characters to maintain context budget
  4. Existing agents with overlap (data-scientist, react-specialist, systems-programmer, devops-engineer) have added boundary commentary directing delegation to the appropriate new specialist
  5. Tool tiers and permission modes are correct: prompt-engineer at Documentation tier, embedded-engineer and mlops-engineer at Full access, all others at Implementation tier
**Plans**: 4 plans

Plans:
- [x] 06-01-PLAN.md -- Author AI/ML agents (prompt-engineer, llm-application-developer, computer-vision-engineer)
- [x] 06-02-PLAN.md -- Author mobile agents (react-native-developer, ios-developer, android-developer)
- [x] 06-03-PLAN.md -- Author infrastructure agents (mlops-engineer, embedded-engineer)
- [x] 06-04-PLAN.md -- Add boundary commentary to 4 existing agents

### Phase 7: Skills Updates
**Goal**: All three skills reflect the complete 20-agent roster so users can discover, get recommendations for, and compose teams from the full pool
**Depends on**: Phase 6 (agent names, descriptions, and categories must be final)
**Requirements**: SKIL-04, SKIL-05, SKIL-06
**Success Criteria** (what must be TRUE):
  1. Running `/browse-pool` displays all 20 agents organized into 7 categories (adding Mobile & Platform and AI & Machine Learning)
  2. Running `/assemble-team` with a task description can recommend agents from the full 20-agent roster
  3. `/team-templates` lists 12 templates total (7 existing + 5 new: Mobile App, Native iOS+Android, AI Application, ML Pipeline, IoT System) with correct agent references
**Plans**: 2 plans

Plans:
- [x] 07-01-PLAN.md -- Update browse-pool and assemble-team skills with 20-agent roster
- [x] 07-02-PLAN.md -- Add 5 new team templates (Mobile App, Native iOS+Android, AI Application, ML Pipeline, IoT System)

### Phase 8: Documentation
**Goal**: All project documentation accurately describes the 20-agent, 12-template plugin so users and contributors see the complete picture
**Depends on**: Phase 7 (skills structure and template names must be final)
**Requirements**: DOCS-04, DOCS-05, DOCS-06, DOCS-07
**Success Criteria** (what must be TRUE):
  1. CLAUDE.md roster table lists all 20 agents with correct colours, tool tiers, and permission modes
  2. README.md shows the 20-agent roster, 12-template list, and an updated mermaid diagram reflecting the expanded pool
  3. CHANGELOG.md contains a v1.1.0 entry documenting all 8 new agents, 5 new templates, and updated skills
  4. `plugin.json` version field reads `1.1.0`
**Plans**: 2 plans

Plans:
- [x] 08-01-PLAN.md -- Update CLAUDE.md roster and bump plugin.json to v1.1.0
- [x] 08-02-PLAN.md -- Update README.md and create CHANGELOG.md v1.1.0 entry

### Phase 9: Verification
**Goal**: The expanded plugin is confirmed working -- all 20 agents load, context budget is within limits, and colour assignments are consistent everywhere
**Depends on**: Phase 8 (all files must be in final state)
**Requirements**: VRFY-01, VRFY-02, VRFY-03
**Success Criteria** (what must be TRUE):
  1. Loading the plugin with `--plugin-dir` discovers all 20 agents under the `agent-pool:` prefix
  2. Total description payload across all 20 agents is measured and documented, confirmed under 50,000 characters
  3. Colour assignments for every agent are identical across agent files, browse-pool skill, CLAUDE.md roster table, and README.md
**Plans**: 1 plan

Plans:
- [x] 09-01-PLAN.md -- Validate structural integrity, measure context budget, cross-check colour consistency

## Progress

**Execution Order:**
Phases execute in numeric order: 6 -> 7 -> 8 -> 9

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Agent Hardening | v1.0 | 4/4 | Complete | 2026-02-19 |
| 2. Hook Verification | v1.0 | 1/1 | Complete | 2026-02-19 |
| 3. Skills Refinement | v1.0 | 2/2 | Complete | 2026-02-19 |
| 4. Integration Testing | v1.0 | 2/2 | Complete | 2026-02-19 |
| 5. Documentation and Distribution | v1.0 | 2/2 | Complete | 2026-02-19 |
| 6. Agent Authoring | v1.1 | 4/4 | Complete | 2026-02-20 |
| 7. Skills Updates | v1.1 | 2/2 | Complete | 2026-02-20 |
| 8. Documentation | v1.1 | 2/2 | Complete | 2026-02-20 |
| 9. Verification | v1.1 | 1/1 | Complete | 2026-02-20 |
