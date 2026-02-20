# Phase 9: Verification - Research

**Researched:** 2026-02-20
**Domain:** Plugin validation and cross-file consistency checking
**Confidence:** HIGH

## Summary

Phase 9 is a verification-only phase with no new features, no external dependencies, and no code generation. The work is entirely introspective: validate YAML frontmatter fields, measure description payloads, and cross-check colour assignments across four reference files. All validation can be performed with Bash, grep, and awk against existing markdown files.

**Primary recommendation:** Use structured Bash scripts to extract and compare data from agent files, browse-pool skill, CLAUDE.md, and README.md. Produce a single verification report with pass/fail verdicts and data tables.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Run both structural file validation AND document the `--plugin-dir` live load command for manual testing
- Validate all 6 required YAML frontmatter fields: name, model, color, tools, permissionMode, description
- Verify each agent description contains at least 1 `<example>` block (don't enforce exact count)
- Check three-section system prompt structure (core expertise, working standards, task workflow)
- Measure description field only from YAML frontmatter for context budget
- Report total character count across all 20 agents, confirm under 50,000 characters
- Include per-agent breakdown sorted by size in report
- If total exceeds 50K: report overage only, do not modify files
- Agent files are canonical source of truth for colour assignments
- Cross-check colours against: README.md and team-templates skill
- Fix non-canonical files if mismatches found AND document changes
- Validate colour-to-domain groupings follow CLAUDE.md conventions
- Produce structured Markdown report with sections per check, pass/fail, data tables
- Store report at `.planning/phases/09-verification/09-VERIFICATION.md`
- Include final overall PASS/FAIL verdict
- Commit verification report to git

### Claude's Discretion
- Exact structural validation approach (regex, parsing, or manual inspection)
- How to present the `--plugin-dir` command for manual live testing
- Report formatting details and section ordering

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| VRFY-01 | All 20 agents load via auto-discovery with `--plugin-dir` | Document the command; structural validation confirms files are well-formed for auto-discovery |
| VRFY-02 | Total description payload measured and under 50K chars | Bash extraction of YAML description fields with character counting |
| VRFY-03 | Colour assignments consistent across agent files, browse-pool, CLAUDE.md, README.md | Regex extraction and diff comparison across four sources |
</phase_requirements>

## Standard Stack

### Core

No external libraries needed. All validation uses built-in shell tools.

| Tool | Purpose | Why Standard |
|------|---------|--------------|
| Bash + grep/awk | YAML field extraction and text processing | Available everywhere, no dependencies |
| Markdown (Write tool) | Verification report output | Matches project's documentation format |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Shell scripts | Python YAML parser | More robust parsing but adds dependency; shell is sufficient for frontmatter extraction |
| Manual inspection | Automated regex | Automation is faster and reproducible; regex adequate for well-structured YAML frontmatter |

## Architecture Patterns

### Validation Approach

The agent files use a consistent pattern: YAML frontmatter between `---` delimiters, followed by the system prompt body. The description field is the only multi-line YAML value that matters for context budget.

**Extraction strategy for description field:**
- Parse between the opening `---` and closing `---` markers
- Extract the `description:` field (which may use `>` or `>-` folded scalar syntax)
- Character count the raw text content (excluding YAML syntax markers)

**Colour cross-check strategy:**
- Extract `name` and `color` from each agent file (canonical source)
- Extract agent-colour pairs from browse-pool skill, CLAUDE.md roster table, and README.md roster
- Diff all four sources; report mismatches

### Report Structure

```
09-VERIFICATION.md
├── Header (date, phase, overall verdict)
├── Section 1: Structural Validation (frontmatter fields, example blocks, prompt sections)
├── Section 2: Context Budget (per-agent table, total, verdict)
├── Section 3: Colour Consistency (cross-file comparison table, mismatches)
├── Section 4: Manual Testing (--plugin-dir command)
└── Overall Verdict
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML parsing | Full YAML parser | grep/awk on frontmatter | Frontmatter is simple key-value; full parser is overkill |
| File diffing | Custom diff engine | Side-by-side comparison tables | Human-readable tables in the report are sufficient |

## Common Pitfalls

### Pitfall 1: Multi-line YAML description extraction
**What goes wrong:** The `description:` field uses YAML folded scalar (`>` or `>-`) spanning multiple lines. Simple `grep "description:"` only gets the first line.
**How to avoid:** Use awk to capture from `description:` until the next frontmatter field (a line starting with a non-space character followed by a colon) or the closing `---`.

### Pitfall 2: Colour names in different formats
**What goes wrong:** Agent files use lowercase (`blue`), but README or CLAUDE.md tables might use title case (`Blue`). Case-insensitive comparison needed.
**How to avoid:** Normalise all colour values to lowercase before comparing.

### Pitfall 3: Agent naming variations across files
**What goes wrong:** An agent might be referenced as `react-specialist` in one file and `react specialist` or `React Specialist` in another.
**How to avoid:** Use the `name` field from agent YAML as canonical; search for exact kebab-case matches in other files.

## Open Questions

None. The verification scope is well-defined by CONTEXT.md decisions and the three success criteria.

## Sources

### Primary (HIGH confidence)
- Project CONTEXT.md (09-CONTEXT.md) - validation decisions
- Project ROADMAP.md - phase success criteria
- Project REQUIREMENTS.md - VRFY-01, VRFY-02, VRFY-03 definitions

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - shell tools, no external deps
- Architecture: HIGH - straightforward file inspection
- Pitfalls: HIGH - well-understood text processing patterns

**Research date:** 2026-02-20
**Valid until:** Indefinite (tooling is stable)
