# Agent Pool Plugin

A Claude Code plugin that provides a pre-defined roster of specialist agents for Agent Teams.

## Structure

- `agents/` — Specialist agent definitions (markdown with YAML frontmatter)
- `skills/` — Team management skills (browse-pool, assemble-team)
- `hooks/` — Quality gate hooks for teammate lifecycle events
- `.claude-plugin/plugin.json` — Plugin manifest

## Adding a new agent

1. Create a new `.md` file in `agents/`
2. Add YAML frontmatter with `name` and `description`
3. Write the system prompt in the markdown body
4. The agent will be auto-discovered by Claude Code

## Agent naming

- Use kebab-case: `javascript-developer`, not `JavaScriptDeveloper`
- Names should describe the role, not the person: `security-auditor`, not `security-expert-bob`
- Keep names concise but clear

## Current roster

| Agent | Domain |
|-------|--------|
| javascript-developer | JS/TS, Node.js, frontend/backend |
| react-specialist | React 19, Next.js 15, frontend arch |
| python-developer | Python, FastAPI, Django |
| ux-designer | UI/UX, accessibility, design systems |
| security-auditor | Security, auth, threat modelling |
| backend-architect | APIs, system design, distributed systems |
| qa-tester | Test automation, coverage, QA |
| devops-engineer | CI/CD, Docker, K8s, cloud |
| data-scientist | ML, data analysis, statistics |
| technical-writer | Docs, guides, API references |
| database-specialist | Schema design, queries, migrations |
| systems-programmer | Rust, Go, C/C++, performance |
