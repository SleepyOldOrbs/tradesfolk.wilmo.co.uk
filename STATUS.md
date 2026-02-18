# Agent Pool — Project Status

Last updated: 2026-02-18

## What's done

- [x] Plugin manifest (`.claude-plugin/plugin.json`) — valid, tested
- [x] 12 specialist agent definitions in `agents/` — all have name, model, color, description, and three-section system prompts
- [x] 2 skills: `browse-pool` and `assemble-team`
- [x] TeammateIdle hook (lightweight, logs and allows idle)
- [x] MIT LICENSE, .gitignore
- [x] Plugin validated — passed with 0 critical issues
- [x] Git repo initialised with 2 commits

## What needs doing

### High priority

- [ ] **Add `<example>` blocks to agent descriptions** — The plugin validator flagged that agent `description` fields should include `<example>` blocks showing sample invocations. This helps Claude Code match tasks to agents automatically. Format:
  ```yaml
  description: >
    Expert JavaScript developer...
    <example>Refactor the auth middleware to use async/await</example>
    <example>Add TypeScript types to the API client</example>
  ```

- [ ] **Test the plugin with a real Agent Team session** — Install the plugin locally, start an Agent Team, and verify:
  - Agents are discoverable via `/browse-pool`
  - `/assemble-team` recommends appropriate specialists
  - Spawned teammates receive their system prompts correctly
  - The TeammateIdle hook fires and logs as expected

- [ ] **Verify hook event names** — The `TeammateIdle` hook event may not be standard. Confirm it works in the current Claude Code version. If not, find the correct event name or remove the hook.

### Medium priority

- [ ] **Consider more specialist agents** — Potential additions:
  - `mobile-developer` — React Native, Flutter, iOS/Android
  - `ml-engineer` — MLOps, model deployment, inference optimisation (distinct from data-scientist)
  - `api-designer` — OpenAPI specs, API-first design (overlaps with backend-architect)
  - `accessibility-specialist` — dedicated WCAG/ARIA expert (overlaps with ux-designer)
  - Only add if they cover genuinely distinct expertise not already in the pool

- [ ] **Add a `team-templates` skill** — Pre-built team compositions for common scenarios:
  - "Full-stack feature" = javascript-developer + backend-architect + qa-tester
  - "Security hardening" = security-auditor + devops-engineer + backend-architect
  - "New API" = backend-architect + database-specialist + qa-tester + technical-writer

- [ ] **Push to GitHub** — Create a public repo so others can install the plugin

### Low priority

- [ ] **Add a README.md** — User-facing docs for GitHub (install instructions, screenshots, usage examples). Keep CLAUDE.md as the Claude Code project instructions
- [ ] **TaskCompleted hook** — Add a hook that runs when a specialist marks a task complete, verifying basic quality criteria
- [ ] **MCP server for dynamic roster** — Optional: an MCP server that lets the team lead query the agent pool programmatically (list agents, filter by skill, get agent details)

## Design decisions

1. **All agents use `model: inherit`** — Lets the user's config decide the model. Agents that need more capability (e.g. backend-architect for complex design) could be changed to `model: opus` later, but `inherit` is the safe default.

2. **Colour-coding by domain** — Makes it easy to visually distinguish agent types in the terminal. Blue for frontend, green for backend, etc.

3. **Three-section system prompt pattern** — Every agent follows: Core expertise, Working standards, When given a task. This consistency means the team lead knows what to expect from any specialist.

4. **Lightweight hooks** — The TeammateIdle hook just logs and allows idle. We deliberately avoided heavy quality gates that would block agents in ways that don't apply universally (e.g. "run tests" doesn't apply to the technical-writer).

5. **Skills over commands** — Used skills (browse-pool, assemble-team) rather than slash commands because skills are simpler to define and more naturally fit the "ask Claude to do something" pattern.

## How to install (for testing)

Claude Code local plugin installation — from any project directory:

```bash
claude plugin add /path/to/agent-pool
```

Or add the path to your Claude Code settings under `enabledPlugins`.

## Git log

```
1d28fae Add model/color fields to agents, LICENSE, and .gitignore
d19d672 Initial agent-pool plugin: 12 specialist agents, 2 skills, hooks
```
