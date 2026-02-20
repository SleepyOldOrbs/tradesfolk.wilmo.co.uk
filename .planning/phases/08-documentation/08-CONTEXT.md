# Phase 8: Documentation - Context

**Gathered:** 2026-02-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Update all project documentation (CLAUDE.md, README.md, CHANGELOG.md, plugin.json) to accurately reflect the expanded 20-agent, 12-template plugin. No new features or agents — this phase is purely documentation and version bumping.

</domain>

<decisions>
## Implementation Decisions

### README presentation
- Agent roster grouped by category (not a flat table) — separate sections per domain
- Team templates grouped by domain theme (e.g., Frontend, Backend, Mobile, AI/ML) — not a flat numbered list
- Intro paragraph updated to "20 specialists across 8 domain categories"
- Add one new workflow example showcasing a v1.1 agent (mobile or AI scenario)
- Mermaid diagram: top-down (TD) orientation, all 8 category nodes shown, category labels only (no individual agent names), include agent counts per category (e.g., "Frontend & UI (3)")

### CHANGELOG format
- v1.1.0 entry starts with a brief summary paragraph ("Expands the pool from 12 to 20 agents...")
- New agents listed as a grouped summary ("8 new specialists: 3 mobile, 3 AI/ML, 2 infrastructure") — not individually
- Include a "Changed" section noting boundary commentary added to 4 existing agents (data-scientist, react-specialist, systems-programmer, devops-engineer)
- 5 new team templates listed individually by name (Mobile App, Native iOS+Android, AI Application, ML Pipeline, IoT System)
- Follows existing Keep a Changelog format

### CLAUDE.md restructuring
- Roster table grouped by category to match README (consistent across both docs)
- Update skills section with 20-agent and 12-template counts
- Remove specific character count from context budget note — just say "within acceptable bounds"
- Update all other factual references throughout (agent counts, template counts, category counts)

### Colour scheme
- Reassign terminal colours so each of the 8 categories gets visual distinction
- Only 6 colours available (blue, cyan, green, yellow, magenta, red) — at least 2 pairs must share
- Claude's Discretion on which categories share colours — pick the most logical domain-overlap pairing

### Claude's Discretion
- Exact colour pairing decisions (which 2 pairs of categories share colours)
- Which v1.1 scenario to use for the new workflow example (mobile or AI)
- Mermaid diagram styling details
- CLAUDE.md section ordering and any structural improvements

</decisions>

<specifics>
## Specific Ideas

- User wants new categories (Mobile & Platform, AI & ML) to feel visually distinct — not just lumped in with existing domains
- The colour reassignment may require updating agent files themselves (changing `color:` frontmatter) — this is acceptable as part of documentation consistency
- Grouped presentation style preferred throughout: both README and CLAUDE.md should organize agents by category, not as flat lists

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 08-documentation*
*Context gathered: 2026-02-20*
