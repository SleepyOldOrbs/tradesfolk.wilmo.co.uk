# Phase 3: Skills Refinement - Research

**Researched:** 2026-02-19
**Domain:** Claude Code plugin skills — frontmatter specification, skill body structure, team template patterns
**Confidence:** HIGH

## Summary

The official Claude Code skills documentation (https://code.claude.com/docs/en/skills) provides a complete frontmatter reference table. The current skill files in this plugin use two incorrect field names: `user_invocable` should be `user-invocable` (hyphenated), and `args` should be `argument-hint`. Both are confirmed by the official specification.

The frontmatter reference also reveals additional optional fields the plugin could leverage (`allowed-tools`, `disable-model-invocation`, `model`, `context`, `agent`, `hooks`), though most are not needed for these three skills. The key discovery is that ALL frontmatter fields use **kebab-case** (hyphens), never snake_case (underscores).

The team-templates skill should be user-invocable with `disable-model-invocation: true` since it is an informational selection menu users trigger manually, not something Claude should auto-invoke. The browse-pool and assemble-team skills should keep their current defaults (both user-invocable and model-invocable).

**Primary recommendation:** Fix frontmatter field names to match official spec exactly, create team-templates as a concise numbered-list skill, and sync all agent references against the 12 agents in the agents/ directory.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Change `user_invocable: true` to `user-invocable: true` (hyphen, not underscore) in all skills
- Change `args: task_description` to `argument-hint: task_description` in assemble-team skill
- If research reveals other required/optional frontmatter fields, add them too
- Create a new skill at `skills/team-templates/SKILL.md`
- 7 pre-built team compositions: full-stack feature, API development, security hardening, frontend overhaul, data pipeline, infrastructure setup, documentation sprint
- Each template lists: team name, agents included, what it's for, suggested lead
- User-invocable via `/team-templates` with `argument-hint` for optional scenario filtering
- browse-pool must list exactly the 12 agents from agents/ directory with updated descriptions
- assemble-team must have the same 12 agents in its "Available specialists" table
- Keep current conversational style in browse-pool and assemble-team
- team-templates presents compositions as a numbered list referenceable by name or number
- All skills should be concise

### Claude's Discretion
- Exact wording of team template descriptions
- Whether to add a brief "When to use" note for each template
- Column structure for the assemble-team specialist table (whether to add tool tier or permission info)
- Whether browse-pool should read agent files dynamically or use a hardcoded list (hardcoded is simpler and consistent with current approach)

### Deferred Ideas (OUT OF SCOPE)
- Dynamic roster reading from agent files at skill invocation time
- Template customization (user modifies templates)
- Agent compatibility matrix (which agents work well together)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SKIL-01 | Skill frontmatter uses correct field names per official spec (`user-invocable` not `user_invocable`, `argument-hint` not `args`) | Complete frontmatter reference table from official docs confirms exact field names. See "Standard Stack" and "Architecture Patterns" sections below. |
| SKIL-02 | Team-templates skill provides 5-8 pre-built team compositions for common scenarios | Skill creation patterns documented. 7 compositions defined in CONTEXT.md. See "Architecture Patterns > Pattern 2" for template skill structure. |
| SKIL-03 | browse-pool and assemble-team skills synced with finalized agent roster | All 12 agent names and descriptions extracted from agents/ directory. See "Code Examples > Agent Roster Reference" for exact data to sync. |
</phase_requirements>

## Standard Stack

### Core — Official SKILL.md Frontmatter Fields

Source: https://code.claude.com/docs/en/skills (Frontmatter reference table)

| Field | Required | Type | Default | Purpose |
|-------|----------|------|---------|---------|
| `name` | No | string | directory name | Display name. Lowercase letters, numbers, hyphens only (max 64 chars). |
| `description` | Recommended | string | first paragraph of content | What the skill does. Claude uses this to decide when to auto-load. |
| `argument-hint` | No | string | none | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | No | boolean | `false` | When `true`, only the user can invoke (via `/name`). Claude will not auto-trigger. |
| `user-invocable` | No | boolean | `true` | When `false`, hidden from `/` menu. Only Claude can invoke it. |
| `allowed-tools` | No | string | all tools | Comma-separated list of tools Claude can use without permission when skill is active. |
| `model` | No | string | inherit | Model to use when this skill is active. |
| `context` | No | string | inline | Set to `fork` to run in a forked subagent context. |
| `agent` | No | string | general-purpose | Which subagent to use when `context: fork`. |
| `hooks` | No | object | none | Hooks scoped to this skill's lifecycle. |

**Confidence: HIGH** — Sourced directly from official documentation at code.claude.com.

### Key Naming Convention

ALL frontmatter fields use **kebab-case** (hyphens): `user-invocable`, `argument-hint`, `disable-model-invocation`, `allowed-tools`. There are ZERO snake_case fields in the specification.

### String Substitutions Available in Skill Content

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### Alternatives Considered

Not applicable — this is the official specification. There are no alternatives to the field names.

## Architecture Patterns

### Pattern 1: Correct Frontmatter for Each Skill

**browse-pool** — Informational skill, both user and model can invoke:

```yaml
---
name: browse-pool
description: Browse the available specialist agent pool. Shows all agents with their expertise areas and recommended use cases. Use this to see who's available before assembling a team.
---
```

No `user-invocable` field needed (defaults to `true`). No `disable-model-invocation` needed (defaults to `false`). No `argument-hint` needed (takes no arguments).

**assemble-team** — Action skill, both user and model can invoke, takes task description argument:

```yaml
---
name: assemble-team
description: Assemble a team of specialist agents from the pool for a specific task. Describe the task and this skill will recommend which specialists to pull in, or specify agents by name.
argument-hint: task description
---
```

Note: `argument-hint` value should NOT use brackets with colons (e.g., `[optional: task description]`) due to a known YAML parsing bug that crashes the TUI (GitHub issue #22161). Simple unquoted strings like `task description` or quoted strings like `"task description"` are safe.

**team-templates** — Selection skill, user-invocable, should NOT auto-trigger:

```yaml
---
name: team-templates
description: Pre-built team compositions for common development scenarios. Pick a template to quickly assemble a specialist team.
argument-hint: scenario name
disable-model-invocation: true
---
```

`disable-model-invocation: true` prevents Claude from auto-triggering this when someone mentions team composition. This is an informational reference card the user chooses to view.

### Pattern 2: Team Template Skill Body Structure

The skill body should be a concise numbered list. Based on official Anthropic skill design principles (from the skill-creator skill in the anthropics/skills repository):

- Keep SKILL.md under 500 lines
- Use imperative/instructional voice
- Be concise — users want quick answers

Recommended structure for team-templates:

```markdown
Present the following pre-built team compositions. If the user provides $ARGUMENTS, filter to matching templates.

## Templates

### 1. Full-Stack Feature
**Agents:** react-specialist, javascript-developer, qa-tester
**Lead:** react-specialist
**For:** Building end-to-end features with frontend, backend JS, and tests.

### 2. API Development
...

After presenting, ask: "Pick a template by name or number, or describe your task for a custom recommendation."
```

### Pattern 3: Invocation Behaviour Matrix

This table clarifies how each skill should behave:

| Skill | User invocable | Model invocable | Has arguments | Rationale |
|-------|---------------|-----------------|---------------|-----------|
| browse-pool | Yes (default) | Yes (default) | No | Claude should be able to show the roster when asked "who's available?" |
| assemble-team | Yes (default) | Yes (default) | Yes: task description | Claude should be able to recommend teams proactively for described tasks |
| team-templates | Yes (default) | No (`disable-model-invocation: true`) | Optional: scenario name | User-triggered reference card; Claude should use assemble-team for active recommendations |

### Anti-Patterns to Avoid

- **Using snake_case in frontmatter:** `user_invocable`, `argument_hint` — these are not recognised by Claude Code. Always use kebab-case.
- **Brackets with colons in argument-hint:** `argument-hint: [optional: task]` crashes the TUI. Use plain text or quote the value.
- **Overly long skill bodies:** Keep under 500 lines. Skill descriptions are always in context; the body loads only when invoked. Long bodies waste context window.
- **Inconsistent agent lists:** If browse-pool lists 12 agents but assemble-team lists 11, Claude gets confused about who is available. All skills must agree on the roster.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Argument parsing | Custom `$ARGUMENTS` splitting logic | Built-in `$ARGUMENTS`, `$ARGUMENTS[N]`, `$N` | Claude Code handles argument substitution natively |
| Skill discovery | Manual registration in plugin.json | Auto-discovery from `skills/` directory | Claude Code auto-discovers `SKILL.md` files in `skills/<name>/` directories |
| Dynamic roster | MCP server or script to read agent files | Hardcoded agent list in skill body | Static list is simpler, matches current approach, avoids runtime complexity |

**Key insight:** Skills are static markdown files processed at load time. Dynamic behaviour should be in the skill's instructions to Claude, not in infrastructure.

## Common Pitfalls

### Pitfall 1: YAML Parsing of argument-hint with Brackets
**What goes wrong:** Using `argument-hint: [optional: task description]` causes YAML to parse the value as an array `[{optional: "task description"}]` instead of a string, which crashes React in the TUI.
**Why it happens:** YAML interprets `[key: value]` as a flow sequence (array of objects), not a string.
**How to avoid:** Use plain text (`argument-hint: task description`) or quote the value (`argument-hint: "task description"`). Avoid square brackets entirely, or if needed, always quote.
**Warning signs:** TUI hangs or shows React error #31 when invoking the skill.
**Source:** https://github.com/anthropics/claude-code/issues/22161

### Pitfall 2: Confusing user-invocable and disable-model-invocation
**What goes wrong:** Setting `user-invocable: false` when you actually want to prevent Claude from auto-triggering the skill. Or setting `disable-model-invocation: true` when you want to hide a skill from the menu.
**Why it happens:** The two fields control different directions of invocation.
**How to avoid:** Remember:
  - `user-invocable: false` = hidden from `/` menu, only Claude can use it
  - `disable-model-invocation: true` = Claude cannot auto-trigger, only user via `/name`
  - Default (both omitted) = both user and Claude can invoke
**Warning signs:** Skill appearing/not appearing in `/` menu unexpectedly, or Claude using skills at wrong times.

### Pitfall 3: Stale Agent References Across Skills
**What goes wrong:** One skill lists an agent that was renamed or removed, or misses a newly added agent.
**Why it happens:** Skills maintain independent hardcoded lists of agents. When the agent roster changes, each skill must be updated independently.
**How to avoid:** After any agent roster change, grep all skills for agent name references and update. In this phase: verify browse-pool, assemble-team, and team-templates all list exactly the same 12 agents.
**Warning signs:** Claude recommends an agent that does not exist, or omits an available agent.

### Pitfall 4: Skill Description Too Long for Context Budget
**What goes wrong:** Skill descriptions (frontmatter `description` field) are always loaded into Claude's context. With 12+ agents and 3+ skills, total description text can exceed the 2% context window budget.
**Why it happens:** The context budget is approximately 2% of the context window (roughly 16,000 chars fallback). Each agent description and skill description counts against this.
**How to avoid:** Keep skill `description` field to 1-2 sentences. Put detailed instructions in the body (which only loads when invoked).
**Warning signs:** Running `/context` shows a warning about excluded skills.

## Code Examples

Verified patterns from official sources.

### Correct Frontmatter — browse-pool (SKIL-01)

```yaml
# Source: https://code.claude.com/docs/en/skills (Frontmatter reference)
---
name: browse-pool
description: Browse the available specialist agent pool. Shows all agents with their expertise areas and recommended use cases.
---
```

Removed: `user_invocable: true` (wrong field name, and default is `true` anyway).

### Correct Frontmatter — assemble-team (SKIL-01)

```yaml
# Source: https://code.claude.com/docs/en/skills (Frontmatter reference)
---
name: assemble-team
description: Assemble a team of specialist agents from the pool for a specific task. Describe the task and this skill will recommend which specialists to pull in.
argument-hint: task description
---
```

Changed: `args: task_description` to `argument-hint: task description`. Removed `user_invocable: true`.

### Correct Frontmatter — team-templates (SKIL-02, new)

```yaml
# Source: https://code.claude.com/docs/en/skills (Frontmatter reference)
---
name: team-templates
description: Pre-built team compositions for common development scenarios. Pick a template to quickly assemble a specialist team.
argument-hint: scenario name
disable-model-invocation: true
---
```

### Agent Roster Reference (SKIL-03)

Current agent roster from `agents/` directory (all 12 agents):

| Agent | Domain Summary |
|-------|---------------|
| javascript-developer | JS/TS implementation, Node.js backend, build tooling, code modernisation |
| react-specialist | React components, Next.js architecture, server components, frontend performance |
| ux-designer | Accessibility audits, design systems, responsive layouts, UI/UX patterns |
| python-developer | Python web dev, API implementation, CLI tools, scripting |
| backend-architect | API design, system architecture, service boundaries, technical decisions |
| systems-programmer | Rust, Go, C/C++, performance-critical code, concurrency |
| database-specialist | Schema design, query optimisation, migration planning, indexing |
| qa-tester | Test automation, test strategy, coverage analysis, E2E testing |
| security-auditor | Code audits, threat modelling, vulnerability assessment, auth reviews |
| devops-engineer | CI/CD pipelines, containerisation, cloud infrastructure, IaC |
| data-scientist | Data analysis, ML model training, experiment design, statistical methods |
| technical-writer | API documentation, developer guides, tutorials, ADRs |

**Domain grouping for browse-pool:**
- Frontend & UI: javascript-developer, react-specialist, ux-designer
- Backend & Systems: python-developer, backend-architect, systems-programmer, database-specialist
- Quality & Security: qa-tester, security-auditor
- Infrastructure & Operations: devops-engineer
- Data & ML: data-scientist
- Documentation: technical-writer

### Team Template Compositions (SKIL-02)

The 7 compositions from CONTEXT.md:

| # | Name | Agents | Lead | Purpose |
|---|------|--------|------|---------|
| 1 | Full-Stack Feature | react-specialist, javascript-developer, qa-tester | react-specialist | End-to-end feature with frontend, backend JS, and tests |
| 2 | API Development | backend-architect, python-developer, database-specialist, qa-tester | backend-architect | New API with data layer and test coverage |
| 3 | Security Hardening | security-auditor, backend-architect, devops-engineer | security-auditor | Security review, architecture fixes, infrastructure hardening |
| 4 | Frontend Overhaul | react-specialist, ux-designer, javascript-developer | react-specialist | UI redesign, accessibility, component refactoring |
| 5 | Data Pipeline | data-scientist, python-developer, database-specialist | data-scientist | Data processing, ML pipelines, storage design |
| 6 | Infrastructure Setup | devops-engineer, systems-programmer, backend-architect | devops-engineer | CI/CD, containerisation, cloud deployment |
| 7 | Documentation Sprint | technical-writer, backend-architect | technical-writer | API docs, guides, architecture documentation |

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `commands/` directory with `.md` files | `skills/` directory with `SKILL.md` in subdirectories | Claude Code ~1.0.33+ | Skills support supporting files, frontmatter, auto-discovery. Commands still work but skills are recommended. |
| `user_invocable` (snake_case) | `user-invocable` (kebab-case) | Always was kebab-case in official spec | Snake_case was never official; likely a misconception. Plugin should fix this. |
| `args` field | `argument-hint` field | Always was `argument-hint` in official spec | `args` was never an official field; likely a misconception. Plugin should fix this. |

**Deprecated/outdated:**
- `commands/` directory: Still works but `skills/` is the recommended approach. This plugin already uses `skills/`, so no change needed.
- Snake_case frontmatter fields: Were never valid. Fix immediately.

## Open Questions

1. **Does omitting `user-invocable` (when `true` is desired) behave identically to explicitly setting it?**
   - What we know: Official docs say default is `true`. Omitting it should be equivalent.
   - What's unclear: Whether there is any edge case where explicit `true` differs from omission.
   - Recommendation: Omit the field entirely since `true` is the default. Cleaner YAML. Only include `user-invocable: false` when you need to hide a skill from the user menu.

2. **Context budget with 12 agents + 3 skills**
   - What we know: Budget is ~2% of context window (~16,000 chars fallback). Agent descriptions and skill descriptions all count.
   - What's unclear: Exact character consumption of the current roster.
   - Recommendation: Keep skill `description` fields short (1-2 sentences). This will be validated in Phase 4 (TEST-01) by checking `/context` output.

## Sources

### Primary (HIGH confidence)
- https://code.claude.com/docs/en/skills — Complete skills documentation including frontmatter reference table. All field names, types, defaults, and descriptions.
- https://code.claude.com/docs/en/plugins-reference — Plugin technical reference. Skills directory structure, auto-discovery, naming conventions.
- https://code.claude.com/docs/en/plugins — Plugin creation guide. Manifest schema, skill structure.

### Secondary (MEDIUM confidence)
- https://github.com/anthropics/claude-code/issues/22161 — `argument-hint` YAML parsing bug with brackets. Confirmed the field name and documented the gotcha.
- https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md — Anthropic's official skill-creator skill. Confirmed skill body best practices (concise, imperative, under 500 lines).

### Tertiary (LOW confidence)
- https://mikhail.io/2025/10/claude-code-skills/ — Community blog post on skill internals. Useful context but may be outdated.

## Metadata

**Confidence breakdown:**
- Standard stack (frontmatter fields): HIGH — directly from official docs at code.claude.com
- Architecture (skill structure patterns): HIGH — examples from official docs and anthropics/skills repo
- Pitfalls: HIGH — known bug confirmed via GitHub issue, invocation model from official docs
- Team template content: MEDIUM — compositions defined by user in CONTEXT.md, structure follows official patterns

**Research date:** 2026-02-19
**Valid until:** 2026-03-19 (stable — Claude Code plugin spec unlikely to change rapidly)
