# Agent Pool Expansion: Platform Specialists + AI/ML Depth

**Date:** 2026-02-19
**Status:** Approved
**Scope:** 8 new agents (13-20), 5 new team templates

## Summary

Expand the Agent Pool from 12 to 20 specialists by adding two new categories: platform specialists (mobile + embedded) and AI/ML depth agents. The current roster covers general frontend, backend, quality, security, infra, and data/docs well but has no mobile, embedded/IoT, or deep AI/ML coverage.

## New Agents

### Platform Specialists (4 agents)

| # | Name | Colour | Domain | Tools Tier | Permission |
|---|------|--------|--------|------------|------------|
| 13 | `react-native-developer` | Blue | React Native, Expo, mobile UI, native modules, app store builds | Implementation | default |
| 14 | `ios-developer` | Blue | Swift, SwiftUI, UIKit, Core Data, Xcode, App Store | Implementation | default |
| 15 | `android-developer` | Green | Kotlin, Jetpack Compose, Room, Gradle, Play Store | Implementation | default |
| 16 | `embedded-engineer` | Cyan | C/C++ firmware, RTOS, microcontrollers, IoT protocols, constrained environments | Full access | default |

### AI/ML Depth (4 agents)

| # | Name | Colour | Domain | Tools Tier | Permission |
|---|------|--------|--------|------------|------------|
| 17 | `llm-application-developer` | Magenta | RAG pipelines, vector stores, agent orchestration, tool use, LangChain/LlamaIndex | Implementation | default |
| 18 | `prompt-engineer` | Magenta | System prompt design, evaluation, red-teaming, output structuring, few-shot patterns | Documentation | default |
| 19 | `mlops-engineer` | Cyan | Model serving, experiment tracking, training pipelines, GPU infra, MLflow/Kubeflow | Full access | default |
| 20 | `computer-vision-engineer` | Magenta | Image/video processing, OCR, diffusion models, multimodal AI, OpenCV/PyTorch | Implementation | default |

## Colour Rationale

Follows existing scheme:

- **Blue** = Frontend/UI — react-native-developer and ios-developer produce user-facing mobile interfaces
- **Green** = Backend — android-developer uses Kotlin (JVM-adjacent), mirrors python-developer placement
- **Cyan** = Infrastructure — embedded-engineer and mlops-engineer manage hardware/deployment infra
- **Magenta** = Data/AI — llm-application-developer, prompt-engineer, computer-vision-engineer all sit in the AI domain

## Tools Tier Rationale

- **prompt-engineer** gets Documentation tier (Read, Grep, Glob, Write, Edit, Bash) — writes prompts and evaluation criteria, not application code
- **embedded-engineer** and **mlops-engineer** get Full access — need Bash for toolchains, WebFetch for docs/packages
- All others get Implementation tier — standard code-writing agents

## New Team Templates

| # | Template | Lead | Members | Use Case |
|---|----------|------|---------|----------|
| 8 | Mobile App | react-native-developer | ux-designer, qa-tester | Cross-platform mobile feature |
| 9 | Native iOS + Android | ios-developer | android-developer, ux-designer, qa-tester | Platform-native mobile apps |
| 10 | AI Application | llm-application-developer | prompt-engineer, python-developer, qa-tester | LLM-powered features, RAG, agents |
| 11 | ML Pipeline | mlops-engineer | data-scientist, python-developer, devops-engineer | Training, serving, monitoring ML models |
| 12 | IoT System | embedded-engineer | systems-programmer, devops-engineer | Firmware, device management, IoT |

## System Prompt Structure

All 8 new agents follow the same three-section pattern as existing agents:

1. **Core expertise** — bullet list of specific technologies and skills
2. **Working standards** — concrete rules the agent follows
3. **When given a task** — numbered workflow steps

Each agent includes 3 `<example>` blocks in its description for delegation matching.

## Impact

- Agent Pool: 12 -> 20 agents
- Team Templates: 7 -> 12 templates
- Context budget: ~39k chars -> ~65k chars estimated (within bounds)
- Existing agents: unchanged
- Skills: browse-pool and assemble-team updated to reflect new roster
- CLAUDE.md: roster table updated
- README.md and CHANGELOG.md: updated for v1.1.0
