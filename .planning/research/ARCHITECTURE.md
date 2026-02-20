# Architecture Research: Agent Pool v1.1.0 Expansion

**Domain:** Claude Code plugin -- 8 new specialist agents integrating into existing 12-agent roster
**Researched:** 2026-02-20
**Confidence:** HIGH

## System Overview: Expansion Impact Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Existing Architecture (unchanged)                     │
│                                                                             │
│  .claude-plugin/plugin.json    hooks/hooks.json    hooks/teammate-checklist │
│  (no changes needed)           (no changes needed)  (no changes needed)     │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                        NEW FILES (8 agent definitions)                       │
│                                                                             │
│  agents/                                                                    │
│  ├── 01-12 existing agents    (unchanged)                                   │
│  ├── 13-react-native-developer.md    NEW                                    │
│  ├── 14-ios-developer.md             NEW                                    │
│  ├── 15-android-developer.md         NEW                                    │
│  ├── 16-embedded-engineer.md         NEW                                    │
│  ├── 17-llm-application-developer.md NEW                                    │
│  ├── 18-prompt-engineer.md           NEW                                    │
│  ├── 19-mlops-engineer.md            NEW                                    │
│  └── 20-computer-vision-engineer.md  NEW                                    │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                        MODIFIED FILES (skills + docs)                        │
│                                                                             │
│  skills/browse-pool/SKILL.md       MODIFIED (add 8 agents to roster)        │
│  skills/assemble-team/SKILL.md     MODIFIED (add 8 agents to roster table)  │
│  skills/team-templates/SKILL.md    MODIFIED (add 5 new templates)           │
│  CLAUDE.md                         MODIFIED (roster table, colour scheme)   │
│  README.md                         MODIFIED (roster table, template list)   │
│  CHANGELOG.md                      MODIFIED (v1.1.0 entry)                  │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                        VERIFICATION                                          │
│                                                                             │
│  Context budget: ~47.7k chars existing + ~32k new = ~80k total              │
│  (agents only; skills/docs context is separate -- see budget section below) │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### New Components (8 agent files)

| File | Agent Name | Responsibility | Domain Group |
|------|-----------|----------------|--------------|
| `13-react-native-developer.md` | react-native-developer | Cross-platform mobile with React Native, Expo, native modules, app store builds | Platform -- Mobile |
| `14-ios-developer.md` | ios-developer | Native iOS with Swift, SwiftUI, UIKit, Core Data, Xcode, App Store | Platform -- Mobile |
| `15-android-developer.md` | android-developer | Native Android with Kotlin, Jetpack Compose, Room, Gradle, Play Store | Platform -- Mobile |
| `16-embedded-engineer.md` | embedded-engineer | Firmware, RTOS, microcontrollers, IoT protocols, constrained environments | Platform -- Embedded |
| `17-llm-application-developer.md` | llm-application-developer | RAG pipelines, vector stores, agent orchestration, tool use, LangChain/LlamaIndex | AI/ML -- Applications |
| `18-prompt-engineer.md` | prompt-engineer | System prompt design, evaluation, red-teaming, output structuring, few-shot patterns | AI/ML -- Prompts |
| `19-mlops-engineer.md` | mlops-engineer | Model serving, experiment tracking, training pipelines, GPU infra, MLflow/Kubeflow | AI/ML -- Operations |
| `20-computer-vision-engineer.md` | computer-vision-engineer | Image/video processing, OCR, diffusion models, multimodal AI, OpenCV/PyTorch | AI/ML -- Vision |

### Modified Components (6 existing files)

| File | Change Required | Scope of Change |
|------|----------------|-----------------|
| `skills/browse-pool/SKILL.md` | Add 8 agents to the categorised roster listing | Add 2 new category sections: "Mobile & Platform" and "AI & Machine Learning". Insert 4 agents into each. Minor restructure of "Data & ML" heading to separate data-scientist from new AI agents |
| `skills/assemble-team/SKILL.md` | Add 8 rows to the "Available specialists" table | Append rows. No structural change to the skill's process or sizing guidelines |
| `skills/team-templates/SKILL.md` | Add 5 new templates (numbers 8-12) | Append 5 new template sections after existing template 7. Update the closing line to mention 12 total templates |
| `CLAUDE.md` | Update roster table, colour scheme docs, tool tier docs, context budget note | Add 8 rows to roster table. Add "Mobile & Platform" and "AI/ML" to colour scheme reference. Update context budget note from ~39k to estimated total |
| `README.md` | Update agent count (12 to 20), roster table, template count (7 to 12), mermaid diagram | Add 8 rows to Agent Roster table. Add mobile and AI/ML domain nodes to mermaid diagram. Update template list. Update version badge |
| `CHANGELOG.md` | Add v1.1.0 release entry | Standard changelog entry listing all 8 new agents and 5 new templates |

### Unchanged Components (no modifications needed)

| Component | Why Unchanged |
|-----------|--------------|
| `.claude-plugin/plugin.json` | Auto-discovers agents from `agents/` directory. New `.md` files are picked up automatically. No manifest changes needed |
| `hooks/hooks.json` | TeammateIdle hook is agent-agnostic. Logs any teammate name. Works with new agents without changes |
| `hooks/teammate-checklist.sh` | Reads teammate name from JSON stdin, logs it. Name-agnostic by design |
| Existing 12 agent `.md` files | No changes to existing agents. New agents occupy their own expertise domains with no overlap that requires rewording existing agents |

## Integration Points Between New and Existing Agents

### Cross-Reference Map

New agents interact with existing agents primarily through team templates and the assemble-team skill's recommendation logic. Here are the explicit integration points:

```
NEW AGENT                    COLLABORATES WITH (existing)      VIA
────────────────────────────────────────────────────────────────────────
react-native-developer  ──→  ux-designer                      Template 8 (Mobile App)
                        ──→  qa-tester                         Template 8 (Mobile App)
                        ──→  react-specialist                  Shared React expertise boundary

ios-developer           ──→  android-developer (new)           Template 9 (Native iOS+Android)
                        ──→  ux-designer                       Template 9
                        ──→  qa-tester                         Template 9

android-developer       ──→  ios-developer (new)               Template 9 (Native iOS+Android)
                        ──→  ux-designer                       Template 9
                        ──→  qa-tester                         Template 9

embedded-engineer       ──→  systems-programmer                Template 12 (IoT System)
                        ──→  devops-engineer                   Template 12 (IoT System)

llm-application-developer ──→ prompt-engineer (new)            Template 10 (AI Application)
                          ──→ python-developer                 Template 10
                          ──→ qa-tester                        Template 10
                          ──→ data-scientist                   RAG/embedding overlap boundary

prompt-engineer         ──→  llm-application-developer (new)   Template 10 (AI Application)
                        ──→  technical-writer                  Shared writing/structuring boundary

mlops-engineer          ──→  data-scientist                    Template 11 (ML Pipeline)
                        ──→  python-developer                  Template 11
                        ──→  devops-engineer                   Template 11, shared infra boundary

computer-vision-engineer ──→ data-scientist                    Shared ML/PyTorch boundary
                         ──→ python-developer                  Implementation support
```

### Expertise Boundary Clarifications

These boundaries must be made explicit in agent descriptions to prevent the Team Lead from delegating to the wrong agent.

| Overlap Area | Agent A | Agent B | Boundary Rule |
|-------------|---------|---------|---------------|
| React code in mobile context | react-specialist | react-native-developer | react-specialist owns web React. react-native-developer owns React Native. If the code runs in a browser, react-specialist. If it runs on a phone, react-native-developer |
| ML model training vs ML model serving | data-scientist | mlops-engineer | data-scientist trains and evaluates models. mlops-engineer deploys, serves, and monitors them in production |
| ML model training vs CV-specific training | data-scientist | computer-vision-engineer | data-scientist handles tabular/NLP/general ML. computer-vision-engineer handles image/video-specific models, augmentation, and vision architectures (CNNs, ViTs, diffusion) |
| Python code in AI context | python-developer | llm-application-developer | python-developer owns general Python (FastAPI, Django, CLI, scripts). llm-application-developer owns LLM integration code (RAG, vector stores, agent frameworks, prompt chains) |
| Prompt writing vs prompt engineering | technical-writer | prompt-engineer | technical-writer writes docs, guides, human-readable content. prompt-engineer designs LLM system prompts, evaluations, and output schemas |
| Infrastructure for ML vs general infra | devops-engineer | mlops-engineer | devops-engineer owns CI/CD, containers, cloud infra. mlops-engineer owns ML-specific infra: GPU scheduling, model registries, experiment tracking, training pipelines |
| Firmware/low-level vs systems programming | systems-programmer | embedded-engineer | systems-programmer owns Rust/Go/C on desktop/server. embedded-engineer owns C/C++ on microcontrollers, RTOS, constrained hardware. If it has an OS with processes, systems-programmer. If it has firmware on bare metal, embedded-engineer |

These boundary rules should be embedded in each agent's description and system prompt "Core expertise" section to guide auto-delegation.

## Agent Definition Format (Consistent with Existing 12)

Every new agent follows the identical format established by agents 01-12. No format changes are needed.

### YAML Frontmatter

```yaml
---
name: kebab-case-name
model: inherit
color: [blue|green|cyan|magenta]
tools: [tool list per tier]
permissionMode: [default|plan]
description: >
  [2-3 sentence expertise summary]

  <example>
  Context: [scenario]
  user: "[request]"
  assistant: "[delegation response]"
  <commentary>
  [Why this agent, not a similar one]
  </commentary>
  </example>

  [2 more example blocks]
---
```

### System Prompt Body (three-section pattern)

```markdown
You are a senior [role] assigned to this team.

## Core expertise

- [technology]: [specific capabilities]
- [technology]: [specific capabilities]
- [8-10 bullet points]

## Working standards

- [concrete rule, not vague principle]
- [concrete rule]
- [8-10 rules]

## When given a task

1. [First step -- always understand context]
2. [Second step -- check existing code/patterns]
3. [Third step -- implement]
4. [Fourth step -- validate/test]
5. [Fifth step -- verify quality criteria]
6. [Sixth step -- clean up / document]
```

### Tool Tier Assignments (from approved design)

| Agent | Tier | Tools String |
|-------|------|-------------|
| react-native-developer | Implementation | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit` |
| ios-developer | Implementation | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit` |
| android-developer | Implementation | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit` |
| embedded-engineer | Full access | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit, WebFetch, WebSearch, TodoWrite` |
| llm-application-developer | Implementation | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit` |
| prompt-engineer | Documentation | `Read, Grep, Glob, Write, Edit, Bash` |
| mlops-engineer | Full access | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit, WebFetch, WebSearch, TodoWrite` |
| computer-vision-engineer | Implementation | `Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit` |

### Colour Assignments (from approved design)

| Agent | Colour | Rationale |
|-------|--------|-----------|
| react-native-developer | Blue | Frontend/UI -- produces mobile user interfaces |
| ios-developer | Blue | Frontend/UI -- produces native iOS interfaces |
| android-developer | Green | Backend-adjacent -- Kotlin/JVM, mirrors python-developer placement |
| embedded-engineer | Cyan | Infrastructure -- manages hardware/deployment |
| llm-application-developer | Magenta | Data/AI domain |
| prompt-engineer | Magenta | Data/AI domain |
| mlops-engineer | Cyan | Infrastructure -- manages ML deployment infra |
| computer-vision-engineer | Magenta | Data/AI domain |

### Model Assignment

All 8 new agents use `model: inherit`. This is consistent with 10 of the 12 existing agents. Only ux-designer and technical-writer use `model: sonnet` (lightweight design/docs tasks). None of the new agents qualify for the sonnet exception: prompt-engineer writes LLM system prompts (higher complexity than docs), and all platform/AI agents need full reasoning capability.

### Permission Mode Assignment

All 8 new agents use `permissionMode: default`. None are read-only audit roles (like security-auditor's `plan` mode) or auto-accept roles (like technical-writer's `acceptEdits`). The prompt-engineer could arguably use `acceptEdits` since it writes prompt text rather than application code, but `default` is safer given that prompt engineering can affect system behaviour significantly.

## Browse-Pool Skill Restructure

The current `browse-pool` skill groups agents into 6 categories. With 20 agents, the categories need restructuring.

### Current Categories (12 agents)

```
Frontend & UI (3): javascript-developer, react-specialist, ux-designer
Backend & Systems (4): python-developer, backend-architect, systems-programmer, database-specialist
Quality & Security (2): qa-tester, security-auditor
Infrastructure & Operations (1): devops-engineer
Data & ML (1): data-scientist
Documentation (1): technical-writer
```

### Proposed Categories (20 agents)

```
Frontend & UI (3): javascript-developer, react-specialist, ux-designer
  (unchanged)

Mobile & Platform (4): react-native-developer, ios-developer, android-developer, embedded-engineer
  (NEW category)

Backend & Systems (4): python-developer, backend-architect, systems-programmer, database-specialist
  (unchanged)

AI & Machine Learning (4): llm-application-developer, prompt-engineer, computer-vision-engineer, data-scientist
  (NEW category -- data-scientist moves here from "Data & ML")

Quality & Security (2): qa-tester, security-auditor
  (unchanged)

Infrastructure & Operations (3): devops-engineer, mlops-engineer, embedded-engineer
  (mlops-engineer added -- BUT see note below about embedded-engineer)
```

**Note on embedded-engineer placement:** The embedded-engineer fits both "Mobile & Platform" (it is a platform specialist) and "Infrastructure" (it manages hardware). The approved design places it in "Mobile & Platform" alongside the other platform specialists. In browse-pool, list it under "Mobile & Platform" because that is its primary identity. The team templates will pair it with devops-engineer and systems-programmer for IoT work, so the infra connection is covered there.

**Note on mlops-engineer placement:** mlops-engineer manages ML infrastructure (GPU scheduling, model serving, training pipelines). It fits "Infrastructure & Operations" better than "AI & Machine Learning" because its work is operations-focused, not model-building-focused.

**Revised proposal (cleaner):**

```
Frontend & UI (3): javascript-developer, react-specialist, ux-designer

Mobile & Platform (4): react-native-developer, ios-developer, android-developer, embedded-engineer

Backend & Systems (4): python-developer, backend-architect, systems-programmer, database-specialist

AI & Machine Learning (4): llm-application-developer, prompt-engineer, computer-vision-engineer, data-scientist

Quality & Security (2): qa-tester, security-auditor

Infrastructure & Operations (2): devops-engineer, mlops-engineer

Documentation (1): technical-writer
```

This gives 7 categories with 20 agents. The maximum category size is 4, keeping the list scannable.

## Team Template Architecture

### Existing Templates (1-7, unchanged)

| # | Name | Lead | Members |
|---|------|------|---------|
| 1 | Full-Stack Feature | react-specialist | javascript-developer, qa-tester |
| 2 | API Development | backend-architect | python-developer, database-specialist, qa-tester |
| 3 | Security Hardening | security-auditor | backend-architect, devops-engineer |
| 4 | Frontend Overhaul | react-specialist | ux-designer, javascript-developer |
| 5 | Data Pipeline | data-scientist | python-developer, database-specialist |
| 6 | Infrastructure Setup | devops-engineer | systems-programmer, backend-architect |
| 7 | Documentation Sprint | technical-writer | backend-architect |

### New Templates (8-12, from approved design)

| # | Name | Lead | Members | Use Case |
|---|------|------|---------|----------|
| 8 | Mobile App | react-native-developer | ux-designer, qa-tester | Cross-platform mobile feature with React Native/Expo |
| 9 | Native iOS + Android | ios-developer | android-developer, ux-designer, qa-tester | Platform-native mobile apps when cross-platform is not suitable |
| 10 | AI Application | llm-application-developer | prompt-engineer, python-developer, qa-tester | LLM-powered features, RAG pipelines, agent orchestration |
| 11 | ML Pipeline | mlops-engineer | data-scientist, python-developer, devops-engineer | Training, serving, and monitoring ML models |
| 12 | IoT System | embedded-engineer | systems-programmer, devops-engineer | Firmware development, device management, IoT protocols |

### Template Design Rules (consistent with existing)

1. Every template has exactly one **lead** -- the domain expert who drives the work
2. Templates have 2-4 **members** (including the lead) -- small, focused teams
3. **qa-tester** appears in templates where behaviour changes are expected (templates 8, 9, 10)
4. **security-auditor** is not on any new template by default -- can be added via assemble-team for specific needs
5. Templates reference agents by their `name` field (kebab-case, matching the frontmatter)

### Template Interaction Patterns

```
Template 8 (Mobile App):
  react-native-developer (lead)
       ├── delegates UI review to ux-designer
       └── delegates test coverage to qa-tester

Template 9 (Native iOS + Android):
  ios-developer (lead)
       ├── parallel with android-developer (same feature, different platform)
       ├── ux-designer reviews both platforms for consistency
       └── qa-tester covers both platform test suites

Template 10 (AI Application):
  llm-application-developer (lead)
       ├── prompt-engineer designs/evaluates prompts
       ├── python-developer handles API/integration code
       └── qa-tester writes evaluation suites and edge cases

Template 11 (ML Pipeline):
  mlops-engineer (lead)
       ├── data-scientist builds/trains models
       ├── python-developer handles data processing code
       └── devops-engineer sets up infrastructure (GPU, storage)

Template 12 (IoT System):
  embedded-engineer (lead)
       ├── systems-programmer handles protocol implementations
       └── devops-engineer handles device fleet management infra
```

## Context Budget Analysis

### Current State (12 agents)

Measured from the existing agent files:

| Component | Characters |
|-----------|-----------|
| 12 agent `.md` files total | 47,706 |
| Average per agent | 3,975 |
| Range | 3,686 -- 4,332 |

The ~39k figure cited in CLAUDE.md refers to description text only (the YAML `description` fields loaded into Claude's context for auto-delegation). The full file sizes are larger because they include the system prompt body, which only loads when the agent is spawned.

### Projected State (20 agents)

| Component | Characters (estimated) |
|-----------|----------------------|
| 8 new agent `.md` files | ~32,000 (8 x 4,000 avg) |
| 20 agent files total | ~79,700 |
| Description text only (20 agents) | ~65,000 (estimated from design doc) |

### Budget Constraints

The critical constraint is **description text loaded into context for auto-delegation**. Per the architecture research from v1.0.0, this consumes part of the skill context budget (2% of context window).

With Claude's 200k token context window, 2% is ~4,000 tokens (~16,000 characters). The current 12-agent descriptions total ~3,903 characters (well within budget). Adding 8 more agents at similar description lengths adds ~2,600 characters, bringing the total to ~6,500 characters.

**This exceeds the 2% budget if all descriptions are loaded simultaneously.** However, the existing agents already work with 3 example blocks each (which pushes individual descriptions to ~500-800 characters). The 2% budget applies to skill descriptions, and agent descriptions may use a separate budget.

**Mitigation strategy:** Keep new agent descriptions concise. Target 300-400 characters per description (2-3 sentences plus 3 example blocks). If context pressure is observed, reduce example blocks from 3 to 2 per agent.

**Confidence:** MEDIUM -- the exact budget accounting for agent descriptions vs skill descriptions is not fully documented. The existing 12 agents with 3 example blocks each work without issues, so 20 agents at the same density is likely fine but should be verified empirically.

## Data Flow (unchanged by expansion)

The plugin's data flow is unaffected by adding agents. The same patterns apply:

1. **Plugin loading:** Claude Code reads `agents/` directory, discovers all `.md` files. Adding 8 files means 8 more auto-discoveries. No code change.
2. **Agent matching:** Team Lead reads all agent descriptions. More descriptions = more options for matching, but the matching mechanism is unchanged.
3. **Teammate spawning:** Same as existing agents. Each new agent gets its own context window with its system prompt.
4. **Hook firing:** TeammateIdle hook receives any teammate name. Name-agnostic by design.
5. **Skill invocation:** browse-pool and assemble-team skills contain static roster references that must be updated manually. This is the one data flow that requires human intervention.

## Anti-Patterns to Avoid During Expansion

### Anti-Pattern 1: Overlapping Descriptions Without Boundary Markers

**What people do:** Write new agent descriptions that sound similar to existing agents (e.g., "Python developer who builds ML applications" for llm-application-developer when python-developer already covers "Python web dev, API implementation, CLI tools").

**Why it is wrong:** Claude uses description matching for auto-delegation. If two agents have overlapping descriptions, the Team Lead may pick the wrong one or alternate unpredictably.

**Do this instead:** Include explicit boundary markers in descriptions. The llm-application-developer description should say "LLM integration code, RAG pipelines, agent orchestration -- NOT general Python web APIs (use python-developer for that)." Negative boundary markers are as important as positive expertise statements.

### Anti-Pattern 2: Inconsistent System Prompt Structure

**What people do:** Write new agent system prompts with different section names, ordering, or depth than existing agents.

**Why it is wrong:** The three-section pattern (Core expertise, Working standards, When given a task) is established across all 12 agents. Inconsistency makes the plugin feel unpolished and may confuse the Team Lead's expectations.

**Do this instead:** Copy an existing agent's structure exactly. Match bullet count ranges (8-10 for Core expertise, 8-10 for Working standards, 6 for When given a task). Start the system prompt with "You are a senior [role] assigned to this team."

### Anti-Pattern 3: Updating Skills Before Agents Are Final

**What people do:** Update browse-pool and assemble-team immediately, then add agents, then realise an agent name changed and have to re-update skills.

**Why it is wrong:** Skills contain static agent references. Updating them before agent names and descriptions are finalised creates a sync problem.

**Do this instead:** Write and finalise all 8 agent files first. Then update skills in a single pass using the final agent names and descriptions.

### Anti-Pattern 4: Adding Too Many Template Variations

**What people do:** Create templates for every possible agent combination (e.g., "React Native + Security", "iOS + ML", "Android + Database").

**Why it is wrong:** The team-templates skill is a quick-start reference, not an exhaustive catalogue. Too many templates make the list overwhelming and hard to scan. The assemble-team skill handles custom combinations.

**Do this instead:** Only create templates for common, well-defined scenarios. The 5 new templates cover the major use cases for the new agent categories. Users should use `/assemble-team` for non-standard combinations.

## Build Order (Dependency-Aware)

### Phase 1: Agent Definitions (no dependencies)

All 8 agent files can be created in parallel. They have no dependencies on each other or on existing files. Each agent is a standalone `.md` file in `agents/`.

**Recommended sub-ordering within Phase 1:**

| Order | Agent | Rationale |
|-------|-------|-----------|
| 1a | prompt-engineer (18) | Simplest -- Documentation tier, no complex technical domain, establishes AI/ML prompt style |
| 1b | llm-application-developer (17) | Pairs with prompt-engineer. Define the expertise boundary between them while both are fresh |
| 1c | mlops-engineer (19) | Completes the AI/ML depth trio. Define boundary with data-scientist and devops-engineer |
| 1d | computer-vision-engineer (20) | Completes AI/ML category. Define boundary with data-scientist |
| 1e | react-native-developer (13) | Highest-overlap agent -- must clearly distinguish from react-specialist. Write this with react-specialist.md open for reference |
| 1f | ios-developer (14) | Straightforward -- no existing agent overlaps with Swift/iOS |
| 1g | android-developer (15) | Straightforward -- no existing agent overlaps with Kotlin/Android |
| 1h | embedded-engineer (16) | Must distinguish from systems-programmer. Write with systems-programmer.md open for reference |

**Why AI/ML before Mobile:** The AI/ML agents have more expertise boundary overlaps with existing agents (data-scientist, python-developer, devops-engineer) that need careful wording. Getting these right first is more important than the mobile agents, which have cleaner boundaries.

### Phase 2: Skill Updates (depends on Phase 1 completion)

Once all 8 agent files are written with final names and descriptions:

| Order | File | Change |
|-------|------|--------|
| 2a | `skills/browse-pool/SKILL.md` | Add 2 new categories, insert 8 agents |
| 2b | `skills/assemble-team/SKILL.md` | Add 8 rows to roster table |
| 2c | `skills/team-templates/SKILL.md` | Add 5 new templates (8-12) |

These three can be done in parallel after Phase 1 is complete.

### Phase 3: Documentation Updates (depends on Phase 2 completion)

| Order | File | Change |
|-------|------|--------|
| 3a | `CLAUDE.md` | Roster table, colour scheme, tool tiers, context budget |
| 3b | `README.md` | Roster table, mermaid diagram, template list, version badge, agent count |
| 3c | `CHANGELOG.md` | v1.1.0 entry |

### Phase 4: Verification (depends on Phase 3 completion)

| Check | Method |
|-------|--------|
| Context budget | Load plugin, verify all 20 agents are discoverable without context errors |
| Agent auto-delegation | Describe tasks that should match new agents, verify correct routing |
| Skill accuracy | Run `/browse-pool`, verify all 20 agents listed. Run `/team-templates`, verify all 12 templates |
| Boundary clarity | Describe ambiguous tasks (e.g., "build a Python ML API"), verify the Team Lead picks the right agent |

## Scaling Considerations

| Scale | Impact |
|-------|--------|
| 20 agents (this milestone) | Manageable. Context budget likely fine. Browse-pool stays scannable with 7 categories. Keep descriptions concise |
| 25-30 agents | browse-pool categories may get unwieldy. Consider sub-grouping or collapsible sections. assemble-team table gets long -- consider moving to a separate reference file |
| 50+ agents | Split into domain-specific plugins (frontend-pool, backend-pool, ai-pool). A single plugin with 50+ agent descriptions will hit context limits. The static reference pattern (skills listing agents by name) becomes a maintenance burden -- consider dynamic discovery via MCP server |

### This milestone's scaling safeguard

At 20 agents, the static reference pattern (skills contain hardcoded agent lists) requires updating 3 skill files + 2 doc files whenever an agent is added. This is tolerable for a one-time expansion of 8 agents, but becomes a maintenance risk if agents are added incrementally. No architectural change is needed now, but if a v1.2.0 expansion is planned, consider dynamic discovery.

## Sources

- Existing agent definitions in `/var/www/tradesfolk.wilmo.co.uk/agents/` (01-12) -- verified format, structure, and character counts
- Existing skill files in `/var/www/tradesfolk.wilmo.co.uk/skills/` -- verified current roster references and template structure
- Approved design document: `/var/www/tradesfolk.wilmo.co.uk/docs/plans/2026-02-19-agent-pool-expansion-design.md`
- Plugin manifest: `/var/www/tradesfolk.wilmo.co.uk/.claude-plugin/plugin.json` -- confirmed no changes needed
- v1.0.0 architecture research: prior `.planning/research/ARCHITECTURE.md` -- plugin loading model, hook mechanics, context budget rules
- Claude Code official documentation (referenced in v1.0.0 research): plugin reference, hooks reference, skills docs, subagents docs

---
*Architecture research for: Agent Pool v1.1.0 Expansion (8 new agents)*
*Researched: 2026-02-20*
