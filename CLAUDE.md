# Agent Pool Plugin

A Claude Code plugin providing a pre-defined roster of specialist agents for Agent Teams.

## Concept

When Claude Code's Agent Teams feature creates a team, the Team Lead spawns teammates ad-hoc. This plugin fills a gap: instead of inventing agents on the fly, the Lead pulls from a **curated pool** of domain specialists with proven system prompts, consistent structure, and clear expertise boundaries. Think of it like calling a tradesman from a directory rather than training a random person.

## Project status: IN PROGRESS

See `STATUS.md` for detailed current state and outstanding work.

## Structure

```
agent-pool/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/                   # 12 specialist agent definitions
│   ├── javascript-developer.md
│   ├── react-specialist.md
│   ├── ux-designer.md
│   ├── python-developer.md
│   ├── backend-architect.md
│   ├── systems-programmer.md
│   ├── database-specialist.md
│   ├── qa-tester.md
│   ├── security-auditor.md
│   ├── devops-engineer.md
│   ├── data-scientist.md
│   └── technical-writer.md
├── skills/
│   ├── browse-pool/SKILL.md  # View the agent roster
│   └── assemble-team/SKILL.md # Get team recommendations for a task
├── hooks/
│   ├── hooks.json            # TeammateIdle hook config
│   └── teammate-checklist.sh # Lightweight idle check
├── CLAUDE.md                 # This file
├── STATUS.md                 # Project status and TODO
├── LICENSE                   # MIT
└── .gitignore
```

## Agent format

Each agent is a markdown file in `agents/` with YAML frontmatter:

```markdown
---
name: kebab-case-name
model: inherit
color: blue
description: One-line summary of expertise and when to use this agent.
---

System prompt body goes here...
```

### Required frontmatter fields

| Field | Values | Purpose |
|-------|--------|---------|
| `name` | kebab-case, 3-50 chars | Agent identifier |
| `model` | `inherit`, `sonnet`, `opus`, `haiku` | Which Claude model to use |
| `color` | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` | Terminal display colour |
| `description` | Free text | Used by Claude Code for agent discovery/matching |

### Colour scheme by domain

- **Blue** — Frontend & UI (javascript-developer, react-specialist, ux-designer)
- **Green** — Backend & Systems (python-developer, backend-architect, systems-programmer, database-specialist)
- **Yellow** — Quality (qa-tester)
- **Red** — Security (security-auditor)
- **Cyan** — Infrastructure (devops-engineer)
- **Magenta** — Data & Docs (data-scientist, technical-writer)

### System prompt structure (consistent across all agents)

Each agent system prompt follows the same three-section pattern:

1. **Core expertise** — bullet list of specific technologies and skills
2. **Working standards** — concrete rules the agent follows (not vague principles)
3. **When given a task** — numbered workflow steps for approaching work

## Skill format

Skills live in `skills/<skill-name>/SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: What this skill does.
user_invocable: true
args: optional_arg_description
---

Skill prompt body...
```

## Adding a new agent

1. Create `agents/<name>.md` with the required frontmatter fields
2. Follow the three-section system prompt structure
3. Assign a colour matching the agent's domain category
4. Update the roster table in this file and in `skills/assemble-team/SKILL.md`
5. Claude Code auto-discovers agents from the `agents/` directory

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with frontmatter
2. Set `user_invocable: true` if users should invoke it directly via `/skill-name`

## Current roster

| Colour | Agent | Domain |
|--------|-------|--------|
| Blue | javascript-developer | JS/TS, Node.js, frontend/backend |
| Blue | react-specialist | React 19, Next.js 15, frontend arch |
| Blue | ux-designer | UI/UX, accessibility, design systems |
| Green | python-developer | Python, FastAPI, Django |
| Green | backend-architect | APIs, system design, distributed systems |
| Green | systems-programmer | Rust, Go, C/C++, performance |
| Green | database-specialist | Schema design, queries, migrations |
| Yellow | qa-tester | Test automation, coverage, QA |
| Red | security-auditor | Security, auth, threat modelling |
| Cyan | devops-engineer | CI/CD, Docker, K8s, cloud |
| Magenta | data-scientist | ML, data analysis, statistics |
| Magenta | technical-writer | Docs, guides, API references |
