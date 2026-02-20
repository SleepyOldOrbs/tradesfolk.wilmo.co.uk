# Project Research Summary

**Project:** Agent Pool v1.1.0 -- 8 New Specialist Agents
**Domain:** Claude Code plugin expansion (12 to 20 agents, 7 to 12 team templates)
**Researched:** 2026-02-20
**Confidence:** HIGH

## Executive Summary

The Agent Pool v1.1.0 expansion adds 8 specialist agents to the existing 12-agent roster, covering two new domain categories: Platform (react-native-developer, ios-developer, android-developer, embedded-engineer) and AI/ML (llm-application-developer, prompt-engineer, mlops-engineer, computer-vision-engineer). The expansion also introduces 5 new team templates and requires updates to 3 existing skills and 3 documentation files. This is a content expansion, not an architectural change -- the plugin system, auto-discovery mechanism, hooks, and manifest are all unchanged. Every new agent is a standalone markdown file in `agents/` following the identical three-section system prompt pattern established in v1.0. All 8 agents can be written in parallel because they have no build-time dependencies on each other.

The recommended approach is: write AI/ML agents first (they have the most overlap with existing agents and need the most careful boundary definitions), then mobile/platform agents (cleaner boundaries), then update all three skills in a single pass, then update documentation. The stack research identified specific technology versions and framework choices for each agent domain -- these feed directly into system prompt "Core expertise" sections. The feature research confirmed all 8 agents are P1 (must-ship) and defined clear table-stakes, differentiators, and anti-features per agent. The architecture research validated that no existing files need structural changes and that the plugin auto-discovery will pick up new agents without manifest changes.

The primary risk is context budget pressure from 20 agent descriptions loaded simultaneously for delegation matching. Measured analysis shows the existing 12 agents have a 2x variance in description length (early agents average 1,740 chars vs late agents averaging 3,624 chars). If new agents follow the late-agent pattern, total description payload reaches ~59k characters -- a likely problem. The mitigation is to standardise all 20 descriptions at 1,800-2,200 characters each, keeping total payload under 44k. The second risk is delegation confusion between overlapping agents (5 specific overlap pairs identified). The mitigation is explicit negative boundary markers in descriptions and disambiguation commentary in example blocks. Both risks are addressable during agent authoring, not after.

## Key Findings

### Recommended Stack

The stack research mapped specific technologies, versions, and frameworks for each of the 8 new agent domains. These are not "choices" the project needs to make -- they are the technologies each agent must demonstrate expertise in within its system prompt. See `.planning/research/STACK.md` for the full technology tables.

**Core technology highlights per agent:**
- **react-native-developer:** React Native 0.78+ (New Architecture mandatory), Expo SDK 53, React 19, Expo Router, MMKV, EAS Build/Submit/Update, Maestro for E2E testing
- **ios-developer:** Swift 6.2 (strict concurrency), SwiftUI (Liquid Glass), SwiftData, Swift Testing framework, Xcode 17, Fastlane
- **android-developer:** Kotlin 2.3.0 (K2 compiler), Jetpack Compose 1.10.1, Hilt/Koin, Room, Navigation Compose, Compose Multiplatform for KMP
- **embedded-engineer:** C17/C23, C++17/C++20 (embedded subset), FreeRTOS/Zephyr RTOS, ESP-IDF, STM32 HAL, PlatformIO, MQTT/BLE/Matter protocols
- **llm-application-developer:** LangChain + LangGraph + LlamaIndex, pgvector/ChromaDB/Qdrant, MCP (97M+ monthly SDK downloads), Vercel AI SDK, Pydantic
- **prompt-engineer:** DSPy for programmatic optimization, Promptfoo for evaluation/red-teaming, LLM-as-Judge methodology, model-specific prompt patterns (Documentation tier)
- **mlops-engineer:** MLflow 3.x, Kubeflow, vLLM/BentoML/KServe for serving, W&B, DVC, Evidently AI for drift detection, GPU infrastructure
- **computer-vision-engineer:** PyTorch 2.x, OpenCV 4.x, YOLO26/Detectron2/SAM 2, Hugging Face Diffusers/Transformers, Albumentations, ONNX/TensorRT for deployment

**Model assignment:** All 8 new agents use `model: inherit` (consistent with 10 of the 12 existing agents). None qualify for the `sonnet` exception used by ux-designer and technical-writer.

**Cross-agent technology overlaps** (8 identified): Python is shared across 5 agents, React across 2, C/C++ across 2, Docker/K8s across 2, PyTorch across 2. The stack research includes a boundary table defining which agent is primary for each shared technology.

### Expected Features

See `.planning/research/FEATURES.md` for the full per-agent table-stakes/differentiators/anti-features analysis and the feature dependency graph.

**Must have (table stakes for v1.1.0):**
- All 8 agent markdown files with YAML frontmatter and three-section system prompts
- 3 `<example>` blocks per agent description with disambiguation commentary
- Correct tool tiers per approved design (Documentation for prompt-engineer, Full access for embedded-engineer and mlops-engineer, Implementation for all others)
- 5 new team templates (Mobile App, Native iOS+Android, AI Application, ML Pipeline, IoT System)
- Updated browse-pool (20 agents in 7 categories), assemble-team (20-row roster table), team-templates (12 templates)
- CLAUDE.md roster table updated to 20 agents
- Context budget verified under 50k characters total description payload

**Should have (ship alongside):**
- README.md updated with 20-agent roster and 12-template list
- CHANGELOG.md v1.1.0 entry

**Defer (v1.2+):**
- New supporting skills for AI/ML agents (e.g., "rag-patterns" skill)
- Additional team templates beyond the 12 planned
- Cross-agent collaboration guidelines document
- Dynamic agent discovery in skills (replacing hardcoded rosters)

**Anti-features (explicitly out of scope):**
Each agent has 3-4 anti-features defined. The most important boundaries: react-native-developer does NOT write native iOS/Android code (delegate to ios-developer/android-developer). llm-application-developer does NOT craft prompts (delegate to prompt-engineer). mlops-engineer does NOT design model architectures (delegate to data-scientist). embedded-engineer does NOT build cloud backends (delegate to devops-engineer/backend-architect). These anti-features are as important as the features -- they prevent scope bleed that would degrade delegation accuracy.

### Architecture Approach

The expansion is purely additive: 8 new files in `agents/`, updates to 6 existing files, zero structural changes to the plugin system. The plugin manifest (`plugin.json`) auto-discovers agents from the `agents/` directory and does not need modification. Hooks are agent-name-agnostic and work unchanged. The only coupling is the static agent rosters hardcoded in three skill files -- these must be manually synced after agent additions. See `.planning/research/ARCHITECTURE.md` for the full component map and build order.

**Major components:**
1. **8 new agent files** (`agents/13-*.md` through `agents/20-*.md`) -- standalone specialist definitions with identical format to existing agents
2. **3 modified skill files** -- browse-pool gains 2 new categories (Mobile & Platform, AI & Machine Learning), assemble-team gains 8 roster rows, team-templates gains 5 new templates
3. **3 modified documentation files** -- CLAUDE.md (roster table, colour scheme, context budget), README.md (roster, diagram, templates), CHANGELOG.md (v1.1.0 entry)

**Key architectural decisions:**
- Browse-pool restructured to 7 categories (from 6) with max 4 agents per category for scannability
- data-scientist moves from "Data & ML" into the new "AI & Machine Learning" category alongside the 3 new AI agents
- mlops-engineer placed in "Infrastructure & Operations" (not AI/ML) because it is operations-focused
- embedded-engineer placed in "Mobile & Platform" (not Infrastructure) because it is a platform specialist

### Critical Pitfalls

See `.planning/research/PITFALLS.md` for the full list with recovery strategies, technical debt analysis, and the "Looks Done But Isn't" checklist.

1. **Context budget overrun from 20-agent descriptions** -- Measured late-agent descriptions average 3,624 chars (2x early agents). Standardise ALL 20 descriptions at 1,800-2,200 chars. Measure with `wc -c` after every addition. Do not exceed 50k total.
2. **Delegation confusion between 5 overlapping agent pairs** -- llm-app-dev/data-scientist, prompt-engineer/data-scientist, mlops/devops, embedded/systems-programmer, react-native/react-specialist. Write explicit "NOT this agent" commentary in every description example. Audit existing agents for claims now covered by new specialists.
3. **Stale hardcoded rosters in skills** -- Skills are the recommendation mechanism, not agent auto-discovery. If browse-pool still shows 12 agents when 20 exist, new agents are invisible to `/browse-pool` and `/assemble-team`. Update all 3 skills atomically with agent additions.
4. **Untested team template combinations** -- 3 of 5 new templates have brand-new agents as leads. Verify each lead's system prompt accounts for its template members. Consider testing templates before release.
5. **Breaking existing agents during normalisation** -- Do not remove delegation triggers from working descriptions. Changes to existing agents should be additive (overlap commentary) not subtractive (content removal). Snapshot existing descriptions before modification.
6. **Colour assignment for android-developer** -- The design assigns Green (backend), but Android development is mobile UI work. Recommend moving to Blue (frontend/UI) to match ios-developer. This is a minor change but prevents unintuitive categorisation.

## Implications for Roadmap

Based on combined research across all four files, the expansion naturally breaks into 4 phases with a clear dependency chain.

### Phase 1: Agent Authoring (AI/ML Agents First)

**Rationale:** AI/ML agents have the most expertise overlap with existing agents (data-scientist, python-developer, devops-engineer) and require the most careful boundary definitions. Writing these first ensures the hardest disambiguation problems are solved before moving to the cleaner mobile/platform agents. The architecture research recommends this sub-ordering for boundary clarity.

**Delivers:** 8 fully-authored agent `.md` files with YAML frontmatter, three-section system prompts, and 3 `<example>` blocks per description.

**Sub-ordering:**
1. prompt-engineer (18) -- simplest, Documentation tier, establishes AI/ML prompt style
2. llm-application-developer (17) -- pairs with prompt-engineer, define boundary while both are fresh
3. mlops-engineer (19) -- completes AI/ML infrastructure, define boundary with devops-engineer
4. computer-vision-engineer (20) -- completes AI/ML category, define boundary with data-scientist
5. react-native-developer (13) -- highest overlap with existing react-specialist, needs careful distinction
6. ios-developer (14) -- clean boundary, no existing agent conflicts
7. android-developer (15) -- clean boundary, resolve colour assignment (recommend Blue)
8. embedded-engineer (16) -- distinguish from systems-programmer

**Addresses features:** All 8 agent files, correct tool tiers, permission modes, `<example>` blocks, description length standardisation

**Avoids pitfalls:** Context budget overrun (standardise descriptions), delegation confusion (write overlap commentary), inconsistent structure (use 01-javascript-developer.md as template), colour confusion (resolve android-developer colour)

**Pre-conditions:** Establish per-description character budget (1,800-2,200 chars) and create agent template before writing first agent. Optionally normalise existing agents 08-12 description lengths.

### Phase 2: Skill Updates

**Rationale:** Skills contain static agent rosters that MUST reflect the actual agents directory. Updating skills after agent authoring ensures names, descriptions, and category assignments are final. All 3 skill updates can be done in parallel.

**Delivers:** Updated browse-pool (20 agents, 7 categories), assemble-team (20-row roster table), team-templates (12 templates including 5 new).

**Addresses features:** 5 new team templates, browse-pool restructure with Mobile & Platform and AI & Machine Learning categories, assemble-team roster expansion

**Avoids pitfalls:** Stale rosters (update atomically), untested templates (write after agent prompts are final), template overload (stick to 5 new templates, use assemble-team for custom combos)

**Verification:** `ls agents/*.md | wc -l` must equal 20. browse-pool agent count must equal 20. assemble-team table rows must equal 20. team-templates must list 12 templates.

### Phase 3: Documentation Updates

**Rationale:** Documentation describes the final feature set. CLAUDE.md contains the authoritative roster table, colour scheme, and context budget measurements. README.md contains the public-facing description. Both depend on Phase 1 (agent files) and Phase 2 (skill structure) being complete.

**Delivers:** Updated CLAUDE.md (roster table, colour scheme, tool tiers, context budget), README.md (roster, mermaid diagram, template list), CHANGELOG.md (v1.1.0 entry), plugin.json version bump to 1.1.0.

**Addresses features:** README update, CHANGELOG entry, context budget documentation, version bump

**Avoids pitfalls:** Stale quantitative claims (measure context budget, do not estimate), docs-staleness (update all counts: 20 agents, 12 templates, measured character totals)

### Phase 4: Verification

**Rationale:** The "Looks Done But Isn't" checklist from pitfalls research identifies 12 verification items that cannot be skipped. This phase exists to catch the gap between "files exist" and "everything works."

**Delivers:** Verified plugin with confirmed agent auto-discovery, delegation accuracy for overlap pairs, context budget measurement, complete skill rosters, consistent colour assignments.

**Verification checklist:**
- All 20 agents load via auto-discovery
- Description consistency (same YAML folding style across all 20)
- All 8 new agents have exactly 3 `<example>` blocks
- Tool tier correctness verified per agent
- 5 overlap pairs tested with ambiguous prompts
- Total description chars measured and documented
- Colour assignments match across agent files, browse-pool, and CLAUDE.md
- plugin.json version is 1.1.0

### Phase Ordering Rationale

- **Phase 1 before Phase 2:** Agent names and descriptions must be final before skills reference them. The architecture research explicitly warns against updating skills before agents are final (Anti-Pattern 3).
- **Phase 2 before Phase 3:** Documentation describes skills and templates. Writing docs before skills are updated means documenting incomplete functionality.
- **Phase 3 before Phase 4:** Verification checks documentation accuracy alongside functional correctness.
- **AI/ML agents before mobile agents within Phase 1:** The 4 AI/ML agents have more existing-agent overlap (data-scientist, python-developer, devops-engineer, technical-writer) than the 4 mobile agents. Solving the harder disambiguation first prevents inconsistent boundary decisions.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 1 (AI/ML sub-group):** The boundary between llm-application-developer and data-scientist needs precise wording. Both touch RAG, embeddings, and evaluation. The existing data-scientist description claims "prompt engineering" under NLP expertise -- this needs modification. Research into current data-scientist description wording is advisable.
- **Phase 1 (embedded-engineer):** Firmware technology moves fast. The Zephyr vs FreeRTOS landscape, ESP-IDF versions, and Rust embedded maturity should be verified against latest sources at authoring time.
- **Phase 4 (context budget):** No documented hard limit exists for agent description budgets. The 2% context window figure from v1.0 research applies to skills, and agent descriptions may use a separate budget. Empirical testing is the only reliable validation method.

Phases with standard patterns (skip research-phase):
- **Phase 1 (mobile agents):** ios-developer, android-developer, and react-native-developer have clean boundaries with no existing agent overlap in their core domains (Swift, Kotlin, React Native). The technology stacks are well-documented by Apple, Google, and Expo respectively.
- **Phase 2 (skill updates):** Pure text editing. The skill format is unchanged from v1.0. Add rows and categories to existing tables.
- **Phase 3 (documentation):** Standard markdown documentation. No research needed.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Technology versions verified via official docs and release notes for all 8 domains. Cross-agent overlap table provides clear boundaries. 26 sources cited with confidence ratings. |
| Features | HIGH | Table-stakes/differentiators/anti-features verified against official platform docs (Apple, Google, Expo), industry roadmaps, and ecosystem analysis. Feature dependency graph confirms no sequential dependencies between agents. 15 sources cited. |
| Architecture | HIGH | Existing plugin architecture verified from codebase measurement. Character counts measured (not estimated). Build order derived from dependency analysis. Anti-patterns identified from v1.0 experience. |
| Pitfalls | HIGH | All 7 pitfalls grounded in measured data (actual description char counts, actual tool tier assignments). Recovery costs assessed as LOW-MEDIUM across the board. "Looks Done But Isn't" checklist provides concrete verification steps. |

**Overall confidence:** HIGH

### Gaps to Address

- **Context budget hard limit:** No official documentation specifies the maximum total description payload for agent auto-discovery. The v1.0 "2% of context window" figure applies to skills, not agents. Must be validated empirically during Phase 4 with all 20 agents loaded.
- **android-developer colour assignment:** The design says Green but the pitfalls research recommends Blue. This needs a decision before Phase 1 begins. Recommendation: Blue (matches ios-developer; both produce mobile UIs).
- **Existing agent description modifications:** The data-scientist currently claims "prompt engineering" expertise, which conflicts with the new prompt-engineer agent. Scope and timing of existing agent modifications needs a decision: during Phase 1 (risk of breaking validated agents) or deferred to v1.1.1 (risk of delegation confusion).
- **prompt-engineer model assignment:** The stack research recommends `model: sonnet` (Documentation tier, similar to ux-designer/technical-writer). The architecture research says `model: inherit` (all 8 new agents). Decision needed. Recommendation: `model: inherit` for v1.1.0 (safer default), revisit if cost is a concern.
- **YAML folding style inconsistency:** Existing agents 01-07 use different YAML description folding than 08-12. New agents need a consistent style. Establish the standard before authoring.

## Sources

### Primary (HIGH confidence)
- [React Native Releases](https://reactnative.dev/docs/releases) -- RN 0.78+ New Architecture, React 19
- [Expo SDK 52/53](https://expo.dev/changelog/) -- Managed workflow, EAS, New Architecture default
- [Swift 6.2 Release Blog](https://www.swift.org/blog/swift-6.2-released/) -- Concurrency, Observations
- [Kotlin 2.3.0 Release](https://blog.jetbrains.com/kotlin/2025/12/kotlin-2-3-0-released/) -- K2 compiler
- [Jetpack Compose December 2025](https://android-developers.googleblog.com/2025/12/whats-new-in-jetpack-compose-december.html) -- Compose 1.10.1
- [Zephyr RTOS](https://embeddedcomputing.com/technology/open-source/linux-freertos-related/) -- v4.3, embedded world 2026
- [LangGraph](https://www.langchain.com/langgraph) -- Multi-agent orchestration
- [MCP - Model Context Protocol](https://modelcontextprotocol.io/) -- Open standard, 97M+ monthly SDK downloads
- [DSPy Framework](https://dspy.ai/) -- Programmatic prompt optimization
- [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/index) -- Diffusion model framework
- [Claude Code Subagents Docs](https://code.claude.com/docs/en/sub-agents) -- Description matching, context budget
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills) -- Skill budget limits
- Existing codebase: `/var/www/tradesfolk.wilmo.co.uk/agents/` -- measured character counts, structural analysis

### Secondary (MEDIUM confidence)
- [Best Vector Databases 2026](https://www.firecrawl.dev/blog/best-vector-databases-2025) -- Pinecone, ChromaDB, Qdrant comparison
- [MLOps Platforms 2026](https://addepto.com/mlops-platforms-in-2026/) -- MLflow 3, Kubeflow, W&B
- [Computer Vision Models 2026](https://www.analyticsvidhya.com/blog/2025/03/computer-vision-models/) -- YOLO26, SAM 2
- [OpenCV 5.0 Roadmap](https://github.com/opencv/opencv/wiki/OE-5.-OpenCV-5) -- API revision status
- [IBM Prompt Engineering Guide 2026](https://www.ibm.com/think/prompt-engineering) -- Prompt patterns
- [Promptfoo Red-Team Documentation](https://www.promptfoo.dev/docs/red-team/) -- Evaluation tools
- Approved design document: `docs/plans/2026-02-19-agent-pool-expansion-design.md`

### Tertiary (LOW confidence)
- [W&B Migration from MLflow](https://medium.com/@pablop44/why-everyone-is-migrating-from-mlflow-to-weights-biases-w-b-in-2025-5926f978e03e) -- Single source, marketing bias
- Context budget hard limits for agent descriptions -- no official documentation; inferred from v1.0 research and empirical observation

---
*Research completed: 2026-02-20*
*Ready for roadmap: yes*
