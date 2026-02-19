---
phase: 01-agent-hardening
plan: 02
subsystem: agents
tags: [python, fastapi, django, architecture, rest, graphql, grpc, rust, go, postgresql, mysql, mongodb, redis]

# Dependency graph
requires:
  - phase: 01-agent-hardening
    provides: "Research findings on frontmatter fields, tool tiers, permission modes, example block format"
provides:
  - "4 production-quality backend domain agents with expanded descriptions, tool restrictions, and permission modes"
  - "python-developer agent with Implementation tier tools and web/API/script delegation examples"
  - "backend-architect agent with Implementation tier tools, permissionMode plan, and design/architecture delegation examples"
  - "systems-programmer agent with Full access tier tools and Rust/Go/C performance delegation examples"
  - "database-specialist agent with Implementation tier tools and schema/query/migration delegation examples"
affects: [01-agent-hardening, 04-integration-testing]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Agent description template: professional summary + 3 example blocks with delegation boundary commentary"
    - "Tool restriction tiers: Implementation (Read/Grep/Glob/Write/Edit/Bash/MultiEdit/NotebookEdit) and Full access (+ WebFetch/WebSearch/TodoWrite)"
    - "permissionMode: plan for design/review-only agents (backend-architect)"

key-files:
  created: []
  modified:
    - agents/python-developer.md
    - agents/backend-architect.md
    - agents/systems-programmer.md
    - agents/database-specialist.md

key-decisions:
  - "Implementation tier tools for python-developer, backend-architect, database-specialist (Read/Grep/Glob/Write/Edit/Bash/MultiEdit/NotebookEdit)"
  - "Full access tier for systems-programmer (adds WebFetch, WebSearch, TodoWrite)"
  - "backend-architect set to permissionMode: plan for design/review mode by default"
  - "All 4 backend agents keep model: inherit for flexibility on complex tasks"

patterns-established:
  - "Description format: 3-line professional summary followed by 3 example blocks with Context/user/assistant/commentary"
  - "Commentary in examples explicitly clarifies delegation boundaries between overlapping agents"
  - "System prompt three-section structure: Core expertise, Working standards, When given a task"

requirements-completed: [AGNT-01, AGNT-02, AGNT-05]

# Metrics
duration: 2min
completed: 2026-02-19
---

# Phase 1 Plan 2: Backend Domain Agents Summary

**4 backend agents rewritten with expanded descriptions (3 example blocks each), tool tier restrictions, permission modes, and production-quality system prompts with clear delegation boundaries**

## Performance

- **Duration:** 2 min
- **Started:** 2026-02-19T11:27:57Z
- **Completed:** 2026-02-19T11:30:19Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Rewrote python-developer with web/API/script examples clearly distinct from data-scientist (ML/statistics)
- Rewrote backend-architect with design/architecture examples (no implementation code), permissionMode: plan
- Rewrote systems-programmer with Rust/Go/C performance examples and Full access tier tools
- Rewrote database-specialist with schema/query/migration examples clearly distinct from backend-architect (API/system design)
- All 4 agents follow consistent description template and three-section system prompt structure

## Task Commits

Each task was committed atomically:

1. **Task 1: Rewrite python-developer and backend-architect** - `6d7f846` (feat)
2. **Task 2: Rewrite systems-programmer and database-specialist** - `cfeea74` (feat)

## Files Created/Modified
- `agents/python-developer.md` - Python web/API specialist with Implementation tier tools
- `agents/backend-architect.md` - Architecture/design specialist with permissionMode: plan
- `agents/systems-programmer.md` - Systems-level specialist with Full access tier tools
- `agents/database-specialist.md` - Database specialist with Implementation tier tools

## Decisions Made
- Implementation tier tools for 3 of 4 backend agents (python-developer, backend-architect, database-specialist): these agents do focused implementation/design work and don't need web search or task management
- Full access tier for systems-programmer: per user decision, systems work spans compilation, testing, research, and task management
- backend-architect gets permissionMode: plan: per user decision, architects operate in design/review mode by default
- All 4 agents keep model: inherit: backend domain tasks vary in complexity, letting user's model selection control quality

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 4 backend domain agents complete with production-quality descriptions, tool restrictions, and permission modes
- Ready for Plan 3 (quality/security/infra domain agents) and Plan 4 (data/docs + file renaming)
- Delegation boundary pattern established and ready for reuse across remaining 8 agents

## Self-Check: PASSED

- All 4 agent files exist and contain expected content
- Both task commits verified (6d7f846, cfeea74)
- All 4 agents have 3 example blocks each
- backend-architect has permissionMode: plan
- systems-programmer has Full access tier tools (WebFetch, WebSearch, TodoWrite)

---
*Phase: 01-agent-hardening*
*Completed: 2026-02-19*
