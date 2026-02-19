# Phase 1: Agent Hardening - Context

**Gathered:** 2026-02-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Refine all 12 agent definitions for production quality: discoverable descriptions with task examples, strict tool restrictions per role, permission modes, context budget efficiency, and full system prompt rewrites. Keep the existing 12 agents — no additions or removals.

</domain>

<decisions>
## Implementation Decisions

### Description style
- Professional tone throughout: "Expert in X. Specializes in Y and Z."
- Strict template: every agent follows an identical description structure
- Medium length: 3-4 lines per description
- 3 natural-language task examples per agent that signal when to delegate
- Include technology keywords for matching (e.g., "React 19, Next.js 15, Tailwind")
- Hint at system prompt depth in descriptions (e.g., "Follows OWASP Top 10, runs threat models")
- Positive framing only — describe what the agent does, don't call out what it doesn't do
- Claude decides the exact format (natural sentences vs bulleted) for best delegation matching

### Tool restrictions
- Strict by role: every agent gets only the tools it genuinely needs
- Every agent must explicitly declare a `tools` field — no implicit inheritance
- All agents get Bash access (all need shell commands at times)
- security-auditor: Read, Grep, Glob, Bash, NotebookRead (read-only + notebook inspection)
- technical-writer: Read, Grep, Glob, Write, Edit, Bash (documentation + doc generators)
- qa-tester: full access (needs to read, write tests, and run them)
- devops-engineer: full access (infrastructure work spans all tool types)
- systems-programmer: full access (compilation, editing, testing)
- data-scientist: full access (write scripts, notebooks, analysis)
- ux-designer: Read, Grep, Glob, Write, Edit, Bash (create design docs, CSS changes)
- Other agents: Claude determines appropriate tool sets based on their workflow

### Permission modes
- security-auditor: `permissionMode: plan` (read-only exploration by default)
- technical-writer: `permissionMode: acceptEdits` (auto-accept file edits)
- Agents that primarily design/plan (e.g., backend-architect, ux-designer) should also get `permissionMode: plan` where appropriate
- All other agents: `default`

### Agent roster
- Keep all 12 agents — no additions or removals in this phase
- Add number prefixes to filenames: `01-javascript-developer.md`, `02-react-specialist.md`, etc.
- Keep existing names (kebab-case), colour scheme, and domain categories
- Soft guidance on maximum agent count (document 2% context budget concern, don't enforce hard limit)

### System prompt rewrites
- Full rewrite of all 12 system prompt bodies — not just frontmatter
- Maintain the three-section structure: core expertise, working standards, when given a task
- Raise quality to match the new description standard
- Ensure system prompts are consistent in depth, specificity, and formatting across all agents

### Model adjustments
- Adjust model field for a few agents where it makes sense during this phase
- Lightweight agents (e.g., technical-writer) may be set to `sonnet`
- Complex agents (e.g., backend-architect, security-auditor) keep `inherit` to let user decide
- Claude decides the specific model assignments based on agent complexity

### Delegation boundaries
- javascript-developer vs react-specialist: Framework boundary — React/Next.js tasks go to react-specialist, general JS/TS/Node goes to javascript-developer
- python-developer vs data-scientist: App vs analysis — web apps/APIs/scripts go to python-developer, ML/data/statistics go to data-scientist
- backend-architect vs language specialists: Design vs implementation — system design/architecture decisions go to architect, writing code goes to language specialist
- database-specialist vs backend-architect: Data layer only — schema/queries/migrations/indexes go to db-specialist, API/system design stays with architect

### Claude's Discretion
- Exact format of task examples in descriptions (natural sentences vs bullets)
- Specific tool sets for agents not explicitly listed above (javascript-developer, react-specialist, python-developer, backend-architect, database-specialist)
- Verification approach for description quality within Phase 1
- Specific model assignments for lightweight vs complex agents
- Numbering order for agent file prefixes

</decisions>

<specifics>
## Specific Ideas

- Descriptions should include technology keywords for matching (React 19, FastAPI, Terraform, etc.) to help Claude match tech-specific tasks
- Descriptions should hint at system prompt depth to signal domain expertise (e.g., "Follows OWASP Top 10" for security-auditor)
- The tradesman-from-a-directory metaphor should be reflected in how agents present themselves — professional, specific, reliable

</specifics>

<deferred>
## Deferred Ideas

- Guided agent creation skill (`/create-agent` that scaffolds the file) — future phase (Skills or Post-Launch)
- Agent schema validation at plugin startup — future phase (Post-Launch Enhancements)
- Detailed CLAUDE.md guide for adding new agents — Phase 5 (Documentation)
- Agent extensibility documentation for users adding project-specific agents — Phase 5 (Documentation)
- README escape hatch documentation for overriding tool restrictions — Phase 5 (Documentation)

</deferred>

---

*Phase: 01-agent-hardening*
*Context gathered: 2026-02-19*
