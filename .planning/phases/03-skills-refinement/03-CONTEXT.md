# Phase 3: Skills Refinement - Context

**Gathered:** 2026-02-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix skill frontmatter to use correct field names, create a new team-templates skill with pre-built compositions, and sync existing skills (browse-pool, assemble-team) with the finalized Phase 1 agent roster. No new agents are added. No changes to hooks or agent definitions.

</domain>

<decisions>
## Implementation Decisions

### Frontmatter field names (SKIL-01)
- Change `user_invocable: true` to `user-invocable: true` (hyphen, not underscore) in all skills
- Change `args: task_description` to `argument-hint: task_description` in assemble-team skill
- Research should confirm the exact field names from official Claude Code plugin-dev documentation
- If research reveals other required/optional frontmatter fields, add them too

### Team template compositions (SKIL-02)
- Create a new skill at `skills/team-templates/SKILL.md`
- Provide 7 pre-built team compositions covering common development scenarios:
  1. **Full-stack feature** — react-specialist + python-developer (or javascript-developer) + qa-tester
  2. **API development** — backend-architect + python-developer + database-specialist + qa-tester
  3. **Security hardening** — security-auditor + backend-architect + devops-engineer
  4. **Frontend overhaul** — react-specialist + ux-designer + javascript-developer
  5. **Data pipeline** — data-scientist + python-developer + database-specialist
  6. **Infrastructure setup** — devops-engineer + systems-programmer + backend-architect
  7. **Documentation sprint** — technical-writer + backend-architect (for architecture context)
- Each template should list: team name, agents included, what it's for, suggested lead
- The skill should be user-invocable so users can type `/team-templates` to see options
- Include `argument-hint` for optionally filtering by scenario name

### Roster sync (SKIL-03)
- browse-pool must list exactly the 12 agents from agents/ directory with their updated descriptions
- assemble-team must have the same 12 agents in its "Available specialists" table
- Update domain descriptions to reflect the Phase 1 rewrite (e.g., react-specialist now covers React 19, Next.js 15, server components)
- Keep the same domain grouping categories (Frontend & UI, Backend & Systems, etc.)
- Verify no stale agent references remain (old names, missing agents, phantom agents)

### Skill output style
- Keep the current conversational style in browse-pool and assemble-team (ending with "Shall I assemble this team?" etc.)
- team-templates should present compositions as a numbered list the user can reference by name or number
- All skills should be concise — users want quick answers, not walls of text

### Claude's Discretion
- Exact wording of team template descriptions
- Whether to add a brief "When to use" note for each template
- Column structure for the assemble-team specialist table (whether to add tool tier or permission info)
- Whether browse-pool should read agent files dynamically or use a hardcoded list (hardcoded is simpler and consistent with current approach)

</decisions>

<specifics>
## Specific Ideas

- The team-templates skill should feel like a quick-reference card — scan it in seconds, pick a template
- Each template should suggest a team lead (the agent best suited to coordinate that type of work)
- The assemble-team "Available specialists" table could include the description one-liner from each agent's frontmatter for better context

</specifics>

<deferred>
## Deferred Ideas

- Dynamic roster reading from agent files at skill invocation time — adds complexity, hardcoded list is fine for v1
- Template customization (user modifies templates) — out of scope, users can manually adjust
- Agent compatibility matrix (which agents work well together) — v2 feature

</deferred>

---

*Phase: 03-skills-refinement*
*Context gathered: 2026-02-19*
