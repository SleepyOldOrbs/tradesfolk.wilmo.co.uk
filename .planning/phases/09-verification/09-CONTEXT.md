# Phase 9: Verification - Context

**Gathered:** 2026-02-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Verify the expanded 20-agent plugin is working correctly: all agents load via auto-discovery, total context budget is within limits, and colour assignments are consistent across all reference files. This phase validates existing work — it does not add new agents, skills, or features.

</domain>

<decisions>
## Implementation Decisions

### Discovery validation
- Run both structural file validation AND document the `--plugin-dir` live load command for manual testing
- Validate all 6 required YAML frontmatter fields are present and non-empty: name, model, color, tools, permissionMode, description
- Verify each agent description contains at least 1 `<example>` block (don't enforce exact count)
- Check that each agent body contains the three-section system prompt structure (core expertise, working standards, task workflow)

### Context budget measurement
- Measure the description field only from YAML frontmatter (that's what Claude Code loads for discovery/matching)
- Report total character count across all 20 agents, confirm under 50,000 characters
- Include per-agent breakdown sorted by size in the verification report
- If total exceeds 50K: report the overage only, do not modify files in this verification phase

### Colour consistency
- Agent files (the `color` field in YAML frontmatter) are the canonical source of truth
- Cross-check colours against: README.md and team-templates skill
- If mismatches found: fix the non-canonical files to match agent file colours AND document what was changed in the report
- Also validate that colour-to-domain groupings follow CLAUDE.md conventions (blue=frontend/mobile, green=backend/systems, yellow=quality, red=security, cyan=infrastructure, magenta=data/ML/AI/docs)

### Verification output
- Produce a structured Markdown report with sections per check, pass/fail status, and data tables
- Store the report at `.planning/phases/09-verification/09-VERIFICATION.md`
- Include a final overall PASS/FAIL verdict based on all three success criteria
- Commit the verification report to git as a project artifact

### Claude's Discretion
- Exact structural validation approach (regex, parsing, or manual inspection)
- How to present the `--plugin-dir` command for manual live testing
- Report formatting details and section ordering

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 09-verification*
*Context gathered: 2026-02-20*
