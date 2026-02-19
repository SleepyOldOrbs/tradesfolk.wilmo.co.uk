# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.0.0]: https://github.com/SleepyOldOrbs/claude-code-agent-pool/releases/tag/v1.0.0
