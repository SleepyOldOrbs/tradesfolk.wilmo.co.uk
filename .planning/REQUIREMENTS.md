# Requirements: Agent Pool v1.1.0

**Defined:** 2026-02-20
**Core Value:** Every specialist agent must have a battle-tested system prompt with clear expertise boundaries so the Team Lead can reliably match tasks to the right expert.

## v1.1 Requirements

### Agent Authoring

- [x] **AGNT-06**: react-native-developer agent with three-section system prompt covering React Native 0.78+, Expo SDK 53, New Architecture, and 3 `<example>` blocks with disambiguation from react-specialist
- [x] **AGNT-07**: ios-developer agent with three-section system prompt covering Swift 6.2, SwiftUI, SwiftData, and 3 `<example>` blocks
- [x] **AGNT-08**: android-developer agent (colour: Blue) with three-section system prompt covering Kotlin 2.3, Jetpack Compose, and 3 `<example>` blocks
- [x] **AGNT-09**: embedded-engineer agent with three-section system prompt covering C/C++, FreeRTOS/Zephyr, IoT protocols, and 3 `<example>` blocks with disambiguation from systems-programmer
- [x] **AGNT-10**: llm-application-developer agent with three-section system prompt covering LangChain/LangGraph, RAG pipelines, vector stores, MCP, and 3 `<example>` blocks with disambiguation from data-scientist
- [x] **AGNT-11**: prompt-engineer agent (Documentation tier tools) with three-section system prompt covering DSPy, Promptfoo, evaluation, and 3 `<example>` blocks with disambiguation from llm-application-developer
- [x] **AGNT-12**: mlops-engineer agent (Full access tools) with three-section system prompt covering MLflow, Kubeflow, vLLM, model serving, and 3 `<example>` blocks with disambiguation from devops-engineer
- [x] **AGNT-13**: computer-vision-engineer agent with three-section system prompt covering PyTorch, OpenCV, YOLO, diffusion models, and 3 `<example>` blocks with disambiguation from data-scientist
- [x] **AGNT-14**: All 8 new agent descriptions standardised at 1,800-2,200 characters to maintain context budget
- [x] **AGNT-15**: Existing agents with overlap (data-scientist, react-specialist, systems-programmer, devops-engineer) updated with boundary commentary to prevent delegation confusion

### Skills Updates

- [x] **SKIL-04**: browse-pool skill updated with 20-agent roster in 8 categories (adding Mobile & Platform, AI & Machine Learning, splitting Data & ML)
- [x] **SKIL-05**: assemble-team skill updated with 20-row roster table (3-column: Agent, Category, Domain)
- [x] **SKIL-06**: team-templates skill updated with 5 new templates (Mobile App, Native iOS+Android, AI Application, ML Pipeline, IoT System) for total of 12

### Documentation

- [x] **DOCS-04**: CLAUDE.md roster table updated to 20 agents with correct colours, tool tiers, and permissions
- [x] **DOCS-05**: README.md updated with 20-agent roster, 12-template list, and expanded mermaid diagram
- [x] **DOCS-06**: CHANGELOG.md v1.1.0 entry documenting all additions
- [x] **DOCS-07**: plugin.json version bumped to 1.1.0

### Verification

- [x] **VRFY-01**: All 20 agents load via auto-discovery when plugin is loaded with `--plugin-dir`
- [x] **VRFY-02**: Total description payload measured and documented (target: under 50k characters)
- [x] **VRFY-03**: Colour assignments consistent across agent files, browse-pool, CLAUDE.md, and README

## v2 Requirements

### Enhanced Agents

- **EAGN-01**: maxTurns set per agent (lightweight agents: 15, standard: 30, complex: 50)
- **EAGN-02**: Model tiering strategy (lightweight agents on sonnet, complex agents inherit)
- **EAGN-03**: Dynamic agent discovery in skills (replace hardcoded rosters)

### Quality Hooks

- **QHOK-01**: TaskCompleted hook with domain-aware quality validation
- **QHOK-02**: SubagentStart/SubagentStop logging hooks for observability

### Tooling

- **TOOL-01**: Agent roster validation script (validates frontmatter schema, required fields, valid colors, description length)

### Advanced Features

- **ADVF-01**: Persistent agent memory (`memory: project`) for 2-3 key agents
- **ADVF-02**: Skills preloaded into agents via `skills` frontmatter field
- **ADVF-03**: Marketplace-ready distribution (marketplace.json, verified install flow)
- **ADVF-04**: Cross-agent collaboration guidelines document
- **ADVF-05**: Additional team templates beyond 12

## Out of Scope

| Feature | Reason |
|---------|--------|
| MCP server for dynamic roster | Over-engineering for a static roster of 20 agents. Markdown files are directly readable |
| Auto-spawning agents based on file type | Removes user control, creates unexpected token costs. Team Lead already handles matching |
| Agent-to-agent dependency chains | Creates deadlocks, blocks parallel execution. Use task dependencies instead |
| Dozens of hyper-specialized agents (30+) | Dilutes quality, causes choice paralysis, exceeds context budget. Cap at 20 for v1.1 |
| Custom system prompt injection / templates | Breaks curated quality proposition. Users can override via `.claude/agents/` |
| GUI / web dashboard | This is a CLI plugin. Terminal output with colour-coding is sufficient |
| Heavy PreToolUse validation hooks | Creates friction. Use `tools`/`disallowedTools` frontmatter for static restrictions |
| Normalising existing agents 01-12 descriptions | Risk of breaking validated delegation behaviour. Additive changes only in v1.1 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AGNT-06 | Phase 6 | Complete |
| AGNT-07 | Phase 6 | Complete |
| AGNT-08 | Phase 6 | Complete |
| AGNT-09 | Phase 6 | Complete |
| AGNT-10 | Phase 6 | Complete |
| AGNT-11 | Phase 6 | Complete |
| AGNT-12 | Phase 6 | Complete |
| AGNT-13 | Phase 6 | Complete |
| AGNT-14 | Phase 6 | Complete |
| AGNT-15 | Phase 6 | Complete |
| SKIL-04 | Phase 7 | Complete |
| SKIL-05 | Phase 7 | Complete |
| SKIL-06 | Phase 7 | Complete |
| DOCS-04 | Phase 8 | Complete |
| DOCS-05 | Phase 8 | Complete |
| DOCS-06 | Phase 8 | Complete |
| DOCS-07 | Phase 8 | Complete |
| VRFY-01 | Phase 9 | Complete |
| VRFY-02 | Phase 9 | Complete |
| VRFY-03 | Phase 9 | Complete |

**Coverage:**
- v1.1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-02-20*
*Last updated: 2026-02-20 after Phase 6 completion*
