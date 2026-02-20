# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-20

Expands the pool from 12 to 20 agents across 8 domain categories, adds 5 new team templates for mobile, AI, and IoT scenarios, and updates all three skills to reflect the full roster.

### Added

#### Agents
- 8 new specialists: 3 mobile & platform (react-native-developer, ios-developer, android-developer), 3 AI & ML (llm-application-developer, prompt-engineer, computer-vision-engineer), 2 infrastructure (embedded-engineer, mlops-engineer)
- New domain categories: Mobile & Platform, AI & ML Applications
- Colour assignments expanded: Blue (frontend + mobile), Cyan (infrastructure + embedded/MLOps), Magenta (data/ML + AI/ML + docs)

#### Templates
- Mobile App -- cross-platform mobile development with native module support
- Native iOS+Android -- separate native apps sharing a backend
- AI Application -- LLM-powered features with RAG pipelines and prompt design
- ML Pipeline -- training-focused ML workflows with experiment tracking
- IoT System -- firmware through cloud deployment

### Changed

#### Agents
- 4 existing agents updated with boundary commentary to prevent delegation confusion with new specialists: data-scientist, react-specialist, systems-programmer, devops-engineer

#### Skills
- `browse-pool` updated with 20-agent roster organised into 8 categories
- `assemble-team` updated with 20-agent roster table
- `team-templates` expanded from 7 to 12 templates

#### Documentation
- CLAUDE.md roster table expanded to 20 agents grouped by category
- README.md updated with expanded roster, new mermaid diagram, and 12-template list
- `plugin.json` version bumped to 1.1.0

## [1.0.0] - 2026-02-19

### Added

#### Agents
- 12 specialist agent definitions with YAML frontmatter and three-section system prompts
- Domain colour-coding: Blue (frontend), Green (backend), Yellow (quality), Red (security), Cyan (infrastructure), Magenta (data/docs)
- 4-tier tool restrictions: Read-only, Documentation, Implementation, Full access
- 3 `<example>` blocks per agent for delegation matching
- Permission modes: `plan` for security-auditor and backend-architect, `acceptEdits` for technical-writer
- Model optimisation: `sonnet` for ux-designer and technical-writer, `inherit` for all others

#### Skills
- `browse-pool` -- View the complete agent roster grouped by domain
- `assemble-team` -- Get team recommendations for a task description with argument-hint support
- `team-templates` -- 7 pre-built team compositions (Full-Stack Feature, API Development, Security Hardening, Frontend Overhaul, Data Pipeline, Infrastructure Setup, Documentation Sprint)

#### Hooks
- `TeammateIdle` hook -- Lightweight stderr logging when teammates go idle during Agent Teams sessions

#### Infrastructure
- Plugin manifest (`.claude-plugin/plugin.json`) with agent auto-discovery
- Portable hook script (`#!/usr/bin/env bash`, no external dependencies)
- MIT license

[1.1.0]: https://github.com/SleepyOldOrbs/tradesfolk.wilmo.co.uk/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/SleepyOldOrbs/tradesfolk.wilmo.co.uk/releases/tag/v1.0.0
