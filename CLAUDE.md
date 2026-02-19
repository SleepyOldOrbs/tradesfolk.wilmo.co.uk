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
│   ├── 01-javascript-developer.md
│   ├── 02-react-specialist.md
│   ├── 03-ux-designer.md
│   ├── 04-python-developer.md
│   ├── 05-backend-architect.md
│   ├── 06-systems-programmer.md
│   ├── 07-database-specialist.md
│   ├── 08-qa-tester.md
│   ├── 09-security-auditor.md
│   ├── 10-devops-engineer.md
│   ├── 11-data-scientist.md
│   └── 12-technical-writer.md
├── skills/
│   ├── browse-pool/SKILL.md  # View the agent roster
│   ├── assemble-team/SKILL.md # Get team recommendations for a task
│   └── team-templates/SKILL.md # Pre-built team compositions
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
tools: Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit
permissionMode: default
description: >
  Use this agent for [task type]. Expert in [domain]. Specializes in [specifics].

  <example>
  Context: [scenario]
  user: "[request]"
  assistant: "[delegation response]"
  <commentary>
  [Why this agent is the right match]
  </commentary>
  </example>
---

System prompt body goes here...
```

### Required frontmatter fields

| Field | Values | Purpose |
|-------|--------|---------|
| `name` | kebab-case, 3-50 chars | Agent identifier |
| `model` | `inherit`, `sonnet`, `opus`, `haiku` | Which Claude model to use |
| `color` | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` | Terminal display colour |
| `tools` | Comma-separated tool names | Allowlist of tools the agent can use |
| `permissionMode` | `default`, `acceptEdits`, `plan`, `dontAsk`, `bypassPermissions` | How the agent handles permission prompts |
| `description` | Free text with `<example>` blocks | Used by Claude Code for agent discovery/matching |

### Tool tiers

| Tier | Tools | Used By |
|------|-------|---------|
| Read-only | Read, Grep, Glob, Bash, NotebookRead | security-auditor |
| Documentation | Read, Grep, Glob, Write, Edit, Bash | technical-writer, ux-designer |
| Implementation | Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit | javascript-developer, react-specialist, python-developer, backend-architect, database-specialist |
| Full access | Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit, WebFetch, WebSearch, TodoWrite | qa-tester, devops-engineer, systems-programmer, data-scientist |

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
argument-hint: hint text
---

Skill prompt body...
```

## Adding a new agent

1. Create `agents/<NN>-<name>.md` with the required frontmatter fields (use the next available number prefix)
2. Follow the three-section system prompt structure
3. Include 3 `<example>` blocks in the description for delegation matching
4. Assign a colour matching the agent's domain category
5. Choose the appropriate tools tier and permission mode
6. Update the roster table in this file and in `skills/assemble-team/SKILL.md`
7. Claude Code auto-discovers agents from the `agents/` directory

## Adding a new skill

1. Create `skills/<name>/SKILL.md` with frontmatter
2. Skills are user-invocable by default; add `disable-model-invocation: true` to prevent Claude from auto-triggering

## Context budget

With 12 agents loaded, total description text (including `<example>` blocks) is approximately 39,000 characters. This is within acceptable bounds for Claude Code's context window. Keep agent descriptions focused and avoid unnecessary verbosity to maintain room for other context sources.

## Current roster

| Colour | Agent | File | Domain | Tools Tier | Permission |
|--------|-------|------|--------|------------|------------|
| Blue | javascript-developer | `01-javascript-developer.md` | JS/TS, Node.js, frontend/backend | Implementation | default |
| Blue | react-specialist | `02-react-specialist.md` | React 19, Next.js 15, frontend arch | Implementation | default |
| Blue | ux-designer | `03-ux-designer.md` | UI/UX, accessibility, design systems | Documentation | default |
| Green | python-developer | `04-python-developer.md` | Python, FastAPI, Django | Implementation | default |
| Green | backend-architect | `05-backend-architect.md` | APIs, system design, distributed systems | Implementation | plan |
| Green | systems-programmer | `06-systems-programmer.md` | Rust, Go, C/C++, performance | Full access | default |
| Green | database-specialist | `07-database-specialist.md` | Schema design, queries, migrations | Implementation | default |
| Yellow | qa-tester | `08-qa-tester.md` | Test automation, coverage, QA | Full access | default |
| Red | security-auditor | `09-security-auditor.md` | Security, auth, threat modelling | Read-only | plan |
| Cyan | devops-engineer | `10-devops-engineer.md` | CI/CD, Docker, K8s, cloud | Full access | default |
| Magenta | data-scientist | `11-data-scientist.md` | ML, data analysis, statistics | Full access | default |
| Magenta | technical-writer | `12-technical-writer.md` | Docs, guides, API references | Documentation | acceptEdits |
