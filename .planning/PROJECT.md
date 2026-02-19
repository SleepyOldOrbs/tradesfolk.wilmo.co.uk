# Agent Pool — Claude Code Plugin

## What This Is

A Claude Code plugin that provides a curated roster of specialist agents for the Agent Teams feature. Instead of the Team Lead inventing agents on the fly with generic prompts, it pulls from a pre-defined pool of 12 domain experts with proven system prompts, consistent structure, and clear expertise boundaries. Think of it like calling a tradesman from a directory rather than training a random person.

## Core Value

Every specialist agent must have a battle-tested system prompt with clear expertise boundaries so the Team Lead can reliably match tasks to the right expert without improvisation.

## Requirements

### Validated

- ✓ Plugin manifest (`plugin.json`) — valid, tested, auto-discovers agents and skills
- ✓ 12 specialist agent definitions with YAML frontmatter and three-section system prompts
- ✓ `browse-pool` skill — view the agent roster grouped by domain
- ✓ `assemble-team` skill — get team recommendations for a task description
- ✓ TeammateIdle hook — lightweight logging when teammates go idle
- ✓ Domain colour-coding scheme (blue/green/yellow/red/cyan/magenta)
- ✓ MIT license and .gitignore
- ✓ All 12 agents have 3 `<example>` blocks for delegation matching — Phase 1
- ✓ Safety-critical agents have tool restrictions (security-auditor: read-only, technical-writer: docs-only) — Phase 1
- ✓ Security-auditor uses `permissionMode: plan` — Phase 1
- ✓ Technical-writer uses `permissionMode: acceptEdits` — Phase 1
- ✓ All agent descriptions fit within 2% context budget (3,903 chars total) — Phase 1
- ✓ Hook script portable (no jq, `#!/usr/bin/env bash`, executable bit tracked in git) — Phase 2
- ✓ hooks.json schema and TeammateIdle event name verified against official Claude Code docs — Phase 2
- ✓ `${CLAUDE_PLUGIN_ROOT}` path resolution confirmed for plugin cache copying — Phase 2

### Active

- [ ] Live runtime verification of TeammateIdle hook in Agent Teams session (deferred to Phase 4)
- [ ] End-to-end testing in a real Agent Team session
- [ ] Additional specialist agents (mobile-developer, ml-engineer, etc.) where they cover distinct expertise
- [ ] `team-templates` skill — pre-built team compositions for common scenarios
- [ ] Push to GitHub as a public repo
- [ ] User-facing README.md with install instructions and usage examples
- [ ] TaskCompleted hook for quality verification on task completion
- [ ] Optional MCP server for programmatic roster queries

### Out of Scope

- Runtime agent creation (agents are static markdown files, not generated dynamically) — simplicity and consistency over flexibility
- Model-specific agent variants (one agent per specialty, model is `inherit`) — user's config decides model
- Heavy quality gates in hooks (e.g. mandatory test runs) — not all agents produce testable output
- GUI or web interface — this is a CLI plugin for Claude Code

## Context

- The plugin is for Claude Code's Agent Teams feature, where a Team Lead orchestrates specialist teammates
- All agents are pure markdown files with YAML frontmatter — no build step, no runtime dependencies
- The three-section system prompt pattern (core expertise, working standards, task workflow) is already established and consistent across all 12 agents
- Colour-coding by domain provides visual distinction in the terminal
- The plugin already has 2 commits and passes validation with 0 critical issues
- Installation is via `claude plugin add /path/to/agent-pool`

## Constraints

- **Format**: Pure markdown with YAML frontmatter — no build step, no compiled assets
- **Claude Code compatibility**: Must work with current Claude Code plugin system (agents, skills, hooks directories)
- **Agent count**: Keep the roster focused — only add specialists that cover genuinely distinct expertise not already in the pool
- **Hook weight**: Hooks must be lightweight and non-blocking — no heavy operations that slow down the team

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Most agents use `model: inherit`, except ux-designer and technical-writer use `sonnet` | Inherit lets user config decide; sonnet for lightweight design/docs tasks saves cost | Phase 1: Implemented |
| Colour-coded by domain | Visual distinction in terminal without requiring UI changes | Phase 1: Implemented |
| Three-section prompt pattern | Consistency means Team Lead knows what to expect from any specialist | Phase 1: All 12 agents follow pattern |
| Skills over commands | More natural fit for "ask Claude" interaction pattern | — Pending |
| Lightweight hooks only | Not all agents produce testable output; heavy gates would block inappropriately | — Pending |
| 4-tier tool restrictions | Read-only, Documentation, Implementation, Full access tiers mapped by agent role | Phase 1: Implemented |
| backend-architect uses `permissionMode: plan` | Design/review role — proposes changes rather than making them directly | Phase 1: Implemented |
| Positive framing in agent descriptions | Commentary uses "operates in X mode" not "cannot do Y" — avoids confusion | Phase 1: Implemented |

---
*Last updated: 2026-02-19 after Phase 2 (Hook Verification)*
