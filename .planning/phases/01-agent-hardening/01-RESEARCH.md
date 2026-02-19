# Phase 1: Agent Hardening - Research

**Researched:** 2026-02-19
**Domain:** Claude Code subagent definitions (frontmatter configuration, description-driven delegation, tool restrictions, permission modes)
**Confidence:** HIGH

## Summary

Phase 1 transforms all 12 agent definitions from working prototypes into production-quality subagent configurations. The work spans five areas: rewriting descriptions with `<example>` blocks for reliable delegation matching, adding `tools` frontmatter to restrict each agent's capabilities by role, setting `permissionMode` for safety-critical agents, renaming files with number prefixes, and fully rewriting all 12 system prompts.

The official Claude Code documentation (verified at code.claude.com/docs/en/sub-agents, February 2026) confirms all required frontmatter fields are supported: `tools` (comma-separated allowlist), `permissionMode` (`default`, `acceptEdits`, `plan`, `dontAsk`, `bypassPermissions`), and `model` (`inherit`, `sonnet`, `opus`, `haiku`). The `color` field used in current agents is functional but not explicitly documented in the official frontmatter reference.

The key tension in this phase is between description richness (task examples via `<example>` blocks for accurate delegation) and description brevity (the 2% context budget concern). The official plugin-dev reference recommends 2-4 `<example>` blocks per agent, but the prior pitfalls research warns that 12 agents each with 3-4 example blocks will consume significant context. The recommendation is to use 2-3 `<example>` blocks per agent with concise context/commentary, keeping the total description (including examples) targeted rather than trying to stay under a raw 200-character limit which is incompatible with the `<example>` format.

**Primary recommendation:** Rewrite all 12 agent files with the new frontmatter fields (tools, permissionMode, model adjustments), structured `<example>` blocks in descriptions, number-prefixed filenames, and full system prompt rewrites -- in that order. Address the description+examples format first since it affects delegation accuracy for all agents.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Professional tone throughout: "Expert in X. Specializes in Y and Z."
- Strict template: every agent follows an identical description structure
- Medium length: 3-4 lines per description
- 3 natural-language task examples per agent that signal when to delegate
- Include technology keywords for matching (e.g., "React 19, Next.js 15, Tailwind")
- Hint at system prompt depth in descriptions (e.g., "Follows OWASP Top 10, runs threat models")
- Positive framing only -- describe what the agent does, don't call out what it doesn't do
- Claude decides the exact format (natural sentences vs bulleted) for best delegation matching
- Strict by role: every agent gets only the tools it genuinely needs
- Every agent must explicitly declare a `tools` field -- no implicit inheritance
- All agents get Bash access (all need shell commands at times)
- security-auditor: Read, Grep, Glob, Bash, NotebookRead (read-only + notebook inspection)
- technical-writer: Read, Grep, Glob, Write, Edit, Bash (documentation + doc generators)
- qa-tester: full access (needs to read, write tests, and run them)
- devops-engineer: full access (infrastructure work spans all tool types)
- systems-programmer: full access (compilation, editing, testing)
- data-scientist: full access (write scripts, notebooks, analysis)
- ux-designer: Read, Grep, Glob, Write, Edit, Bash (create design docs, CSS changes)
- Other agents (javascript-developer, react-specialist, python-developer, backend-architect, database-specialist): Claude determines appropriate tool sets based on their workflow
- security-auditor: `permissionMode: plan` (read-only exploration by default)
- technical-writer: `permissionMode: acceptEdits` (auto-accept file edits)
- Agents that primarily design/plan (e.g., backend-architect, ux-designer) should also get `permissionMode: plan` where appropriate
- All other agents: `default`
- Keep all 12 agents -- no additions or removals in this phase
- Add number prefixes to filenames: `01-javascript-developer.md`, `02-react-specialist.md`, etc.
- Keep existing names (kebab-case), colour scheme, and domain categories
- Soft guidance on maximum agent count (document 2% context budget concern, don't enforce hard limit)
- Full rewrite of all 12 system prompt bodies -- not just frontmatter
- Maintain the three-section structure: core expertise, working standards, when given a task
- Raise quality to match the new description standard
- Ensure system prompts are consistent in depth, specificity, and formatting across all agents
- Adjust model field for a few agents where it makes sense during this phase
- Lightweight agents (e.g., technical-writer) may be set to `sonnet`
- Complex agents (e.g., backend-architect, security-auditor) keep `inherit` to let user decide
- Claude decides the specific model assignments based on agent complexity
- javascript-developer vs react-specialist: Framework boundary -- React/Next.js tasks go to react-specialist, general JS/TS/Node goes to javascript-developer
- python-developer vs data-scientist: App vs analysis -- web apps/APIs/scripts go to python-developer, ML/data/statistics go to data-scientist
- backend-architect vs language specialists: Design vs implementation -- system design/architecture decisions go to architect, writing code goes to language specialist
- database-specialist vs backend-architect: Data layer only -- schema/queries/migrations/indexes go to db-specialist, API/system design stays with architect

### Claude's Discretion
- Exact format of task examples in descriptions (natural sentences vs bullets)
- Specific tool sets for agents not explicitly listed above (javascript-developer, react-specialist, python-developer, backend-architect, database-specialist)
- Verification approach for description quality within Phase 1
- Specific model assignments for lightweight vs complex agents
- Numbering order for agent file prefixes

### Deferred Ideas (OUT OF SCOPE)
- Guided agent creation skill (`/create-agent` that scaffolds the file) -- future phase (Skills or Post-Launch)
- Agent schema validation at plugin startup -- future phase (Post-Launch Enhancements)
- Detailed CLAUDE.md guide for adding new agents -- Phase 5 (Documentation)
- Agent extensibility documentation for users adding project-specific agents -- Phase 5 (Documentation)
- README escape hatch documentation for overriding tool restrictions -- Phase 5 (Documentation)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| AGNT-01 | All 12 agent descriptions include natural-language task examples that trigger delegation (2-3 examples per agent) | `<example>` block format verified from official plugin-dev reference (triggering-examples.md). Format includes Context, user message, assistant response, and commentary. Recommended 2-3 per agent to balance delegation accuracy with context budget. |
| AGNT-02 | Safety-critical agents have tool restrictions via `tools` frontmatter (security-auditor: Read, Grep, Glob, Bash; technical-writer: Read, Grep, Glob, Write, Edit) | `tools` field confirmed as supported frontmatter field (comma-separated list). User decisions expand security-auditor to include NotebookRead and technical-writer to include Bash. All available tool names verified: Read, Write, Edit, MultiEdit, NotebookEdit, NotebookRead, Grep, Glob, LS, Bash, WebFetch, WebSearch, TodoWrite, TodoRead, Task. |
| AGNT-03 | Security-auditor uses `permissionMode: plan` (read-only exploration by default) | `permissionMode: plan` confirmed as valid value in official docs. Puts agent in plan mode (read-only exploration). |
| AGNT-04 | Technical-writer uses `permissionMode: acceptEdits` (auto-accept file edits) | `permissionMode: acceptEdits` confirmed as valid value in official docs. Auto-accepts file edits without prompting. |
| AGNT-05 | All agent descriptions are concise enough to fit within the 2% context window budget with 12+ agents loaded | The 2% budget applies to skill descriptions, not agent descriptions directly. Agent descriptions are loaded for delegation matching. With `<example>` blocks, each description will be ~400-600 chars. 12 agents at ~500 chars = ~6000 chars total, well within typical context budgets. Keep descriptions focused but don't artificially truncate below the point where `<example>` blocks can function. |
</phase_requirements>

## Standard Stack

This phase is primarily a content/configuration task (rewriting markdown files), not a code implementation. There is no library stack. The "stack" is the Claude Code subagent definition format itself.

### Core

| Component | Version | Purpose | Why Standard |
|-----------|---------|---------|--------------|
| Claude Code subagent format | v2.1+ | Agent definition via markdown + YAML frontmatter | Only supported format for Claude Code agents |
| YAML frontmatter | YAML 1.2 | Configuration fields (name, description, tools, permissionMode, model, color) | Standard Claude Code mechanism |
| `<example>` blocks | N/A | Triggering examples in description field | Officially recommended in plugin-dev agent-development skill reference |

### Supported Frontmatter Fields (verified)

| Field | Required | Type | Values | Notes |
|-------|----------|------|--------|-------|
| `name` | Yes | string | lowercase-hyphens, 3-50 chars | Agent identifier |
| `description` | Yes | string | Free text + `<example>` blocks | Used for auto-delegation matching |
| `tools` | No | comma-separated string | Read, Write, Edit, MultiEdit, NotebookEdit, NotebookRead, Grep, Glob, LS, Bash, WebFetch, WebSearch, TodoWrite, TodoRead, Task | Allowlist; inherits all if omitted |
| `disallowedTools` | No | comma-separated string | Same tool names | Denylist; removed from inherited set |
| `model` | No | string | `sonnet`, `opus`, `haiku`, `inherit` | Defaults to `inherit` |
| `permissionMode` | No | string | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | Controls permission prompts |
| `color` | Unofficial | string | `blue`, `cyan`, `green`, `yellow`, `magenta`, `red` | Works in practice, not in official docs table |
| `maxTurns` | No | number | Any positive integer | Max agentic turns |
| `skills` | No | array | Skill names to preload | Injected at spawn time |
| `mcpServers` | No | object | Server definitions | MCP tools available to agent |
| `hooks` | No | object | Hook definitions | Scoped to agent lifecycle |
| `memory` | No | string | `user`, `project`, `local` | Persistent memory across sessions |

### Available Tool Names (complete list, verified)

These are the tool names that can be used in the `tools` and `disallowedTools` frontmatter fields:

| Tool Name | Category | What It Does |
|-----------|----------|-------------|
| Read | File ops | Read file contents |
| Write | File ops | Create/overwrite files |
| Edit | File ops | Exact string replacements in files |
| MultiEdit | File ops | Batch editing operations |
| NotebookEdit | File ops | Edit Jupyter notebook cells |
| NotebookRead | File ops | Read Jupyter notebook files |
| Grep | Search | Content search using ripgrep |
| Glob | Search | File pattern matching |
| LS | Search | List directory contents |
| Bash | Execution | Execute shell commands |
| WebFetch | Web | Fetch and process web content |
| WebSearch | Web | Search the web |
| TodoWrite | Task mgmt | Create and manage task lists |
| TodoRead | Task mgmt | Read task lists |
| Task | Subagents | Spawn subagents (not applicable for subagent definitions) |

**Note on `NotebookRead`:** The user decision specifies `NotebookRead` for the security-auditor. This tool name appears in Claude Code's tool list and is functionally valid. It allows reading `.ipynb` files without editing them.

## Architecture Patterns

### Pattern 1: Agent Description with `<example>` Blocks

**What:** The description field contains a short professional summary followed by 2-3 `<example>` blocks that show Claude when to delegate to this agent.

**When to use:** Every agent definition in this plugin.

**Format (from official plugin-dev reference at github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/SKILL.md):**

```yaml
description: >
  Use this agent when [triggering conditions]. [Professional summary].

  <example>
  Context: [Situation description]
  user: "[User request]"
  assistant: "[How Claude should respond and trigger this agent]"
  <commentary>
  [Why this agent is appropriate here]
  </commentary>
  </example>

  <example>
  [Additional example...]
  </example>
```

**Key principles:**
- Start with "Use this agent when..." to signal delegation conditions
- Include technology keywords for matching
- 2-3 examples covering explicit requests, implicit triggers, and proactive delegation
- Commentary explains the reasoning, not just restates the request
- Keep each example concise (3-5 lines per block)

### Pattern 2: Tool Restriction by Role

**What:** Each agent declares exactly which tools it can access via the `tools` frontmatter field.

**When to use:** All 12 agents must have explicit `tools` declarations (locked decision).

**Restriction tiers (from user decisions + discretion recommendations):**

| Tier | Tools | Agents |
|------|-------|--------|
| Read-only | Read, Grep, Glob, Bash, NotebookRead | security-auditor |
| Documentation | Read, Grep, Glob, Write, Edit, Bash | technical-writer, ux-designer |
| Implementation | Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit | javascript-developer, react-specialist, python-developer, backend-architect, database-specialist |
| Full access | Read, Grep, Glob, Write, Edit, Bash, MultiEdit, NotebookEdit, WebFetch, WebSearch, TodoWrite | qa-tester, devops-engineer, systems-programmer, data-scientist |

**Rationale for discretion agents (not explicitly specified in user decisions):**
- **javascript-developer, react-specialist, python-developer:** Need Write, Edit, MultiEdit for code implementation. Need NotebookEdit for working with Jupyter notebooks (python). Don't need WebSearch/WebFetch (focused implementation, not research). Recommendation: Implementation tier.
- **backend-architect:** Despite being a design/plan role, architects need to write ADRs, API specs, and sometimes prototype code. Need Write and Edit. Recommendation: Implementation tier with `permissionMode: plan`.
- **database-specialist:** Needs to write migration files, schema definitions, and query files. Recommendation: Implementation tier.

### Pattern 3: Permission Mode by Role

**What:** The `permissionMode` field controls how the agent handles permission prompts.

**Assignments (from user decisions + discretion recommendations):**

| Mode | Agents | Rationale |
|------|--------|-----------|
| `plan` | security-auditor, backend-architect | Read-only exploration by default. Security-auditor should not modify code. Backend-architect operates in design/review mode. |
| `acceptEdits` | technical-writer | Auto-accept file edits since writing docs is the primary job. |
| `default` | All other 9 agents | Standard permission checking. Implementation agents need user approval for destructive operations. |

**Note on ux-designer:** The user decision says "where appropriate" for plan mode on ux-designer. However, ux-designer needs to create design docs, modify CSS files, and update component code. `permissionMode: plan` would prevent file modifications. Recommendation: Keep ux-designer at `default` permission mode since their tool restriction (no MultiEdit, NotebookEdit, WebSearch) already limits scope.

### Pattern 4: Model Assignment by Complexity

**What:** Assign specific models to agents based on task complexity.

**Assignments (discretion area):**

| Model | Agents | Rationale |
|-------|--------|-----------|
| `inherit` | backend-architect, security-auditor, systems-programmer, react-specialist, database-specialist | Complex reasoning, architecture decisions, security analysis -- let user's model selection control quality. |
| `sonnet` | technical-writer, ux-designer | Documentation and design tasks that don't require Opus-level reasoning. Sonnet is faster and cheaper. |
| `inherit` | javascript-developer, python-developer, qa-tester, devops-engineer, data-scientist | Code implementation varies in complexity. Safe default is inherit. |

**Conservative approach:** Only assign `sonnet` to agents where the task is clearly bounded (documentation, design review). All others stay at `inherit` to avoid degrading quality for complex tasks the user explicitly chose these agents for.

### Pattern 5: File Numbering Order

**What:** Add number prefixes to agent filenames for consistent ordering.

**Recommended order (discretion area, grouped by domain):**

| # | Filename | Domain |
|---|----------|--------|
| 01 | 01-javascript-developer.md | Frontend & UI |
| 02 | 02-react-specialist.md | Frontend & UI |
| 03 | 03-ux-designer.md | Frontend & UI |
| 04 | 04-python-developer.md | Backend & Systems |
| 05 | 05-backend-architect.md | Backend & Systems |
| 06 | 06-systems-programmer.md | Backend & Systems |
| 07 | 07-database-specialist.md | Backend & Systems |
| 08 | 08-qa-tester.md | Quality |
| 09 | 09-security-auditor.md | Security |
| 10 | 10-devops-engineer.md | Infrastructure |
| 11 | 11-data-scientist.md | Data & ML |
| 12 | 12-technical-writer.md | Documentation |

**Rationale:** Follows the domain grouping already established in CLAUDE.md and the colour scheme. Frontend first (blue), backend next (green), then quality/security/infra/data (yellow/red/cyan/magenta).

### Anti-Patterns to Avoid

- **Vague descriptions:** "Helps with code" or "General backend work" -- Claude cannot match tasks reliably.
- **Too many `<example>` blocks:** More than 3 per agent bloats the context budget. Stick to 2-3 focused examples.
- **Omitting `tools` field:** Without explicit tools, agents inherit everything including WebSearch, WebFetch, and Task -- the security-auditor could modify files, and the technical-writer could spawn subagents.
- **Using `bypassPermissions`:** Never use on plugin agents. Users must control permission modes.
- **Over-restricting Bash:** All agents need Bash for running commands (git, npm, test runners, linters). Never remove Bash from an agent's tool list.
- **Putting `<example>` blocks in system prompt body instead of description:** The system prompt only loads when the agent is spawned. Examples must be in the description field since that's what Claude reads for delegation decisions.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Tool restriction | Custom PreToolUse hooks to block tools | `tools` frontmatter field | Built-in allowlist is simpler, more reliable, and doesn't require hook scripts |
| Read-only enforcement | Hook scripts that check every operation | `permissionMode: plan` | Native permission mode is comprehensive and doesn't have edge cases |
| Agent ordering | Custom plugin.json loading logic | Number-prefixed filenames | Claude Code loads agents alphabetically from the directory; number prefixes control visual ordering |
| Delegation routing | Custom skill that manually routes tasks | `<example>` blocks in description | Claude's built-in description matching is the intended mechanism |

**Key insight:** Claude Code's subagent system already has built-in mechanisms for tool restriction, permission control, and delegation matching. The entire Phase 1 is about using these existing mechanisms correctly, not building custom alternatives.

## Common Pitfalls

### Pitfall 1: Description Length vs Context Budget Tension

**What goes wrong:** The success criteria state "descriptions under 200 characters" but the user decision requires "3-4 lines with 3 task examples" and `<example>` blocks. These are incompatible -- a single `<example>` block with Context/user/assistant/commentary is ~200-300 characters alone.

**Why it happens:** The 200-character limit was likely set before the decision to use `<example>` blocks, or it refers to the description summary text only (not including example blocks).

**How to avoid:** Interpret the 200-character guidance as applying to the description summary text (the "Expert in X. Specializes in Y and Z." portion). The `<example>` blocks sit below the summary and serve a different function (triggering logic). The total description including examples will be ~400-800 characters per agent. At 12 agents, this is ~5,000-10,000 characters total -- well within the 2% context budget (which is ~16,000 characters at minimum or much higher on large context windows).

**Warning signs:** If `/context` shows budget warnings after installing the plugin, descriptions need trimming. This should be verified during Phase 4 integration testing.

### Pitfall 2: `NotebookRead` May Not Be a Valid Tool Name

**What goes wrong:** The user decision specifies `NotebookRead` in the security-auditor's tool list. While NotebookRead appears in some tool lists, it is not consistently documented across all sources. Some sources list it, others list only `NotebookEdit`.

**Why it happens:** Tool names evolve across Claude Code versions. The distinction between `Read` (which can read `.ipynb` files) and `NotebookRead` (dedicated notebook reader) may be version-dependent.

**How to avoid:** Include `NotebookRead` as specified in the user decision. If it fails validation or doesn't work, fall back to just `Read` (which can also read notebook files). Test during Phase 4.

**Warning signs:** Agent errors when trying to read notebooks, or the tool name being unrecognised in `claude --debug` output.

### Pitfall 3: Agent Name Must Match Filename (Minus Prefix and Extension)

**What goes wrong:** After renaming files from `javascript-developer.md` to `01-javascript-developer.md`, the `name` field in frontmatter must still be `javascript-developer` (not `01-javascript-developer`). Claude Code uses the `name` field, not the filename, for agent identification.

**Why it happens:** Developers assume filename = agent name. The official docs say the `name` field is the unique identifier.

**How to avoid:** Keep the `name` field unchanged when adding number prefixes to filenames. The number prefix is purely for file ordering in the directory listing and has no effect on agent functionality.

**Warning signs:** Agent Teams reference agents by name. If the name field changes, browse-pool and assemble-team skills will reference stale names.

### Pitfall 4: `tools` Format -- Comma-Separated vs Array

**What goes wrong:** The `tools` field can be specified as either a comma-separated string (`tools: Read, Grep, Glob, Bash`) or a YAML array (`tools: ["Read", "Grep", "Glob", "Bash"]`). Mixing formats across agents creates inconsistency.

**Why it happens:** Official docs show both formats in different examples. Both work.

**How to avoid:** Use comma-separated format consistently across all agents. This matches the simpler examples in the official docs and is more readable in YAML frontmatter.

**Example:** `tools: Read, Grep, Glob, Bash` (not `tools: ["Read", "Grep", "Glob", "Bash"]`).

### Pitfall 5: Overlapping Agent Descriptions Cause Wrong Delegation

**What goes wrong:** If javascript-developer and react-specialist both have examples about "building a React component," Claude may delegate to the wrong one. Similarly, python-developer and data-scientist could overlap on "write a Python script."

**Why it happens:** Descriptions and examples don't clearly express the boundary between related agents.

**How to avoid:** Each agent's description and examples must explicitly signal the boundary:
- javascript-developer examples: vanilla JS, Node.js, TypeScript typing, build tooling (NOT React)
- react-specialist examples: React components, Next.js routes, state management (NOT vanilla JS)
- python-developer examples: web APIs, CLI tools, package scripts (NOT ML/data analysis)
- data-scientist examples: data analysis, model training, statistical tests (NOT web APIs)
- backend-architect examples: system design, API contracts, architecture review (NOT writing code)
- database-specialist examples: schema design, query optimisation, migration planning (NOT API design)

Include commentary in examples that explains the boundary: "This is a React component task, so it goes to react-specialist, not javascript-developer."

## Code Examples

### Example 1: Complete Agent File (security-auditor with all new fields)

```markdown
---
name: security-auditor
description: >
  Use this agent for security reviews, threat modelling, vulnerability assessment, and auth implementation audits.
  Expert in application security. Specializes in OWASP Top 10, authentication patterns, and supply chain security.
  Follows structured threat modelling and severity-ranked reporting.

  <example>
  Context: User has implemented authentication for a new API
  user: "Review the auth implementation for security issues"
  assistant: "I'll use the security-auditor agent to perform a thorough security review of the authentication code."
  <commentary>
  Explicit security review request for auth code. Triggers security-auditor for OWASP-aligned analysis.
  </commentary>
  </example>

  <example>
  Context: User is about to deploy a feature that handles user data
  user: "Check if the user data handling is secure"
  assistant: "I'll use the security-auditor agent to audit the data handling for vulnerabilities."
  <commentary>
  Data protection concern triggers security-auditor for input validation, encryption, and access control review.
  </commentary>
  </example>

  <example>
  Context: User wants to audit dependencies before a release
  user: "Run a security audit on our dependencies"
  assistant: "I'll use the security-auditor agent to check for known vulnerabilities in the dependency tree."
  <commentary>
  Supply chain security request. Security-auditor handles dependency auditing with npm audit / pip-audit.
  </commentary>
  </example>
model: inherit
color: red
tools: Read, Grep, Glob, Bash, NotebookRead
permissionMode: plan
---

You are a senior security engineer assigned to this team.

## Core expertise
...
```

### Example 2: Complete Agent File (technical-writer with acceptEdits)

```markdown
---
name: technical-writer
description: >
  Use this agent for writing documentation, API references, guides, and architectural decision records.
  Expert in technical documentation. Specializes in developer guides, API docs, and documentation architecture.
  Writes task-oriented content following the Divio documentation system.

  <example>
  Context: User has built a new API endpoint
  user: "Write API docs for the new endpoints"
  assistant: "I'll use the technical-writer agent to create comprehensive API documentation."
  <commentary>
  Documentation request for API endpoints. Technical-writer handles API reference creation.
  </commentary>
  </example>

  <example>
  Context: User needs onboarding documentation for new developers
  user: "Create a getting started guide for this project"
  assistant: "I'll use the technical-writer agent to write a developer onboarding guide."
  <commentary>
  Guide creation request. Technical-writer specializes in tutorial and guide writing.
  </commentary>
  </example>

  <example>
  Context: Team made an architectural decision that needs recording
  user: "Document why we chose PostgreSQL over MongoDB"
  assistant: "I'll use the technical-writer agent to write an Architecture Decision Record."
  <commentary>
  ADR request. Technical-writer handles architectural documentation and decision records.
  </commentary>
  </example>
model: sonnet
color: magenta
tools: Read, Grep, Glob, Write, Edit, Bash
permissionMode: acceptEdits
---

You are a senior technical writer assigned to this team.

## Core expertise
...
```

### Example 3: Description Format Template (for consistent application)

```yaml
description: >
  Use this agent for [primary tasks, comma-separated].
  Expert in [domain]. Specializes in [specific area 1], [specific area 2], and [specific area 3].
  [Hint at system prompt depth -- methodology, standards followed, approach].

  <example>
  Context: [Concise situation, 5-10 words]
  user: "[Natural user request]"
  assistant: "I'll use the [agent-name] agent to [specific action]."
  <commentary>
  [Why this agent is the right choice. Include boundary clarification if agent overlaps with another.]
  </commentary>
  </example>

  <example>
  [Second example -- different phrasing, different scenario]
  </example>

  <example>
  [Third example -- proactive or implicit trigger]
  </example>
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `model: inherit` for all agents | Per-agent model selection (`sonnet`, `opus`, `haiku`, `inherit`) | Always available | Can route lightweight agents to cheaper/faster models |
| No `tools` field (inherit all) | Explicit `tools` allowlist per agent | Always available | Safety enforcement at the platform level |
| Plain text descriptions | `<example>` blocks in descriptions | Plugin-dev reference (2025) | Better delegation accuracy through structured examples |
| No `permissionMode` | Five permission modes available | Always available | Safety-critical agents can be locked down |
| `args` in skill frontmatter | `argument-hint` is the correct field name | Official docs (verified) | Current `args` field may be silently ignored |

**Deprecated/outdated:**
- `user_invocable` in skill frontmatter: Should be `user-invocable` (hyphenated). Current skills use underscore format which may still work but is not per spec.
- `args` in skill frontmatter: Should be `argument-hint`. Phase 3 will address this for skills.

## Open Questions

1. **Does `NotebookRead` work as a tool name in the `tools` field?**
   - What we know: It appears in some tool lists and is functionally distinct from `Read`.
   - What's unclear: Whether it's accepted in the `tools` frontmatter or if `Read` already handles `.ipynb` files.
   - Recommendation: Include it per user decision. Verify during Phase 4 integration testing. Fallback to just `Read` if it doesn't work.

2. **Does renaming files with number prefixes affect plugin auto-discovery?**
   - What we know: Claude Code auto-discovers agents from `agents/` by scanning for `.md` files. The `name` field in frontmatter (not filename) is the identifier.
   - What's unclear: Whether number-prefixed filenames could cause any ordering or loading issues.
   - Recommendation: Proceed with renaming. The `name` field stays unchanged. Test that all 12 agents are still discoverable after renaming in Phase 4.

3. **How do `<example>` blocks interact with the 2% context budget?**
   - What we know: Agent descriptions are loaded for delegation matching. The 2% budget is documented for skill descriptions specifically. Agent descriptions also consume context but through a different mechanism.
   - What's unclear: Whether agent descriptions have their own budget limit or share the skill budget.
   - Recommendation: Keep total description size reasonable (~500-800 chars per agent including examples). Test with `/context` during Phase 4.

4. **Should `backend-architect` get `permissionMode: plan`?**
   - What we know: User decision says "where appropriate" for design/plan agents. Backend-architect primarily does design work.
   - What's unclear: Whether architects sometimes need to write files (ADRs, API specs, prototypes).
   - Recommendation: Set `permissionMode: plan` for backend-architect. Architects can still use Bash to run analysis commands and Read to explore code. If they need to write files, the user can override permission mode per session.

## Implementation Approach

### Recommended Task Ordering

1. **Define the description template** -- Lock down the exact format (summary + 3 examples) that all 12 agents will follow. Write one complete example (e.g., security-auditor) as the reference.
2. **Write all 12 descriptions** -- Apply the template to every agent. Focus on delegation boundaries to avoid overlap.
3. **Add tool restrictions to all 12 agents** -- Add the `tools` field per the tier assignments above.
4. **Set permission modes** -- Add `permissionMode` where needed (3 agents: security-auditor, technical-writer, backend-architect).
5. **Adjust model assignments** -- Change `model` for lightweight agents (technical-writer, ux-designer to `sonnet`).
6. **Rewrite all 12 system prompts** -- Full rewrite maintaining the three-section structure but raising quality and consistency.
7. **Rename files with number prefixes** -- Git rename (preserves history) all 12 files.
8. **Update CLAUDE.md** -- Reflect new frontmatter fields, numbering, and any structural changes.

### Verification Approach (Discretion Area)

Since integration testing is in Phase 4, Phase 1 verification should be lightweight:

1. **Structural verification:** Every agent file has all required frontmatter fields (name, description with examples, tools, model, color).
2. **Description boundary check:** Read all 12 descriptions in sequence and verify no two agents have overlapping example scenarios.
3. **Tool restriction validation:** Cross-reference each agent's `tools` field against the tier table.
4. **System prompt consistency:** Verify all 12 system prompts follow the same three-section structure with comparable depth.
5. **Character budget estimate:** Sum total description characters across all 12 agents. Target: under 10,000 characters total (well within any reasonable context budget).

## Sources

### Primary (HIGH confidence)
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) -- Complete frontmatter reference, tool restrictions, permission modes, model options, example patterns
- [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference) -- Plugin manifest schema, agent auto-discovery, component structure
- [Agent Development SKILL.md - GitHub](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/SKILL.md) -- Description format with `<example>` blocks, agent file structure template, AI-assisted generation prompt
- [Triggering Examples Reference - GitHub](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/agent-development/references/triggering-examples.md) -- Complete `<example>` block format guide, example types, best practices

### Secondary (MEDIUM confidence)
- [Claude Code Built-in Tools Reference](https://www.vtrivedy.com/posts/claudecode-tools-reference) -- Complete internal tool list with descriptions
- [Architecture Research (project)](/.planning/research/ARCHITECTURE.md) -- Verified architecture patterns, component responsibilities, data flows
- [Pitfalls Research (project)](/.planning/research/PITFALLS.md) -- Known pitfalls with prevention strategies

### Tertiary (LOW confidence)
- `color` field: Works in practice across all current agents, but not listed in the official supported frontmatter fields table. Likely supported but undocumented.
- `NotebookRead` tool name: Appears in some tool lists but not consistently documented. Needs Phase 4 verification.
- [GitHub Issue #8501](https://github.com/anthropics/claude-code/issues/8501) -- Reports documentation gaps in frontmatter fields; closed as NOT_PLANNED.

## Metadata

**Confidence breakdown:**
- Frontmatter fields (tools, permissionMode, model): HIGH -- verified directly from official docs at code.claude.com
- `<example>` block format: HIGH -- verified from official plugin-dev reference on GitHub
- Tool names list: HIGH -- cross-referenced multiple sources
- Description context budget impact: MEDIUM -- the 2% budget is documented for skills; agent description budget is less clearly documented
- `color` field support: MEDIUM -- functional but not in official field table
- `NotebookRead` as valid tool: LOW -- appears in some lists, not consistently documented

**Research date:** 2026-02-19
**Valid until:** 2026-03-19 (30 days -- subagent system is relatively stable)
