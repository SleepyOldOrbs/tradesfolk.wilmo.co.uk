# Phase 4: Integration Testing - Context

**Gathered:** 2026-02-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Validate the complete plugin end-to-end in a real environment. Agents must be discoverable and load correctly, skills must be invocable and return useful output, hooks must fire, and installation via `claude plugin add` must succeed. No new features are added — this phase only tests what already exists.

</domain>

<decisions>
## Implementation Decisions

### Test scope and approach
- Split testing into two tiers: **automated validation** (can run without a live session) and **live session testing** (requires Agent Teams)
- Automated validation covers: plugin.json schema, file structure completeness, frontmatter parsing, agent count verification, skill frontmatter correctness, hook configuration
- Live session testing covers: agent discovery by Team Lead, skill invocation (/browse-pool, /assemble-team, /team-templates), TeammateIdle hook firing, system prompt loading
- Both tiers contribute to TEST-01 and TEST-02

### Automated validation specifics
- Verify `plugin.json` is valid JSON with required fields (name, version, description, agents, skills, hooks)
- Verify all 12 agent files exist in `agents/` and have valid YAML frontmatter (name, description, model, color)
- Verify all 3 skill directories exist with SKILL.md files that have valid frontmatter
- Verify `hooks/hooks.json` is valid JSON with `TeammateIdle` event configured
- Verify `hooks/teammate-checklist.sh` is executable and runs without error
- Run `teammate-checklist.sh` with test JSON input and verify output format
- These checks should be implemented as a shell script or inline bash commands in the plan (not a permanent test suite — keep it simple)

### Plugin installation testing (TEST-02)
- Test installation from the local directory using `claude plugin add /var/www/tradesfolk.wilmo.co.uk`
- After installation, verify the plugin appears in `claude plugin list`
- Verify agents, skills, and hooks are discoverable from an installed context
- If `claude plugin add` is not available or errors, document the issue and test with `--plugin-dir` flag instead
- Uninstall after testing to leave the system clean

### Live session testing (TEST-01)
- This requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable
- Start an Agent Teams session and verify:
  1. Agents from the pool appear when the Team Lead considers delegation
  2. `/browse-pool` returns the 12-agent roster grouped by domain
  3. `/assemble-team build a REST API with auth` returns a sensible team recommendation
  4. `/team-templates` shows 7 pre-built compositions
  5. A spawned teammate receives its system prompt (verify by checking the teammate's behavior matches its specialty)
  6. When a teammate goes idle, the TeammateIdle hook fires and logs to stderr
- If live testing is not possible in this environment (headless server, no interactive session), document what was tested and what is deferred with clear instructions for manual testing

### Test reporting
- Create a test report at `.planning/phases/04-integration-testing/04-TEST-REPORT.md`
- Use a pass/fail checklist format with evidence for each test
- Separate automated results from live session results
- Any failures should include: what failed, expected vs actual, and suggested fix

### Claude's Discretion
- Exact structure of automated validation script/commands
- Whether to use a single script or inline bash commands in the plan
- How to handle edge cases in installation testing (e.g., plugin already installed)
- Level of detail in test report

</decisions>

<specifics>
## Specific Ideas

- The automated validation should be fast — under 30 seconds total
- The live session test instructions should be copy-pasteable so a human can follow them step by step
- The `<example>` block syntax validation (flagged as a concern in Phase 1) should be checked during live testing — do agents actually receive and use their example blocks?
- The TeammateIdle hook deferred from Phase 2 verification should be validated here if a live session is available

</specifics>

<deferred>
## Deferred Ideas

- Permanent automated test suite (e.g., a `test.sh` in the repo) — out of scope, this phase does one-time validation
- CI/CD pipeline for plugin testing — v2 feature
- Performance benchmarking (context window consumption with all agents loaded) — nice to check but not a requirement

</deferred>

---

*Phase: 04-integration-testing*
*Context gathered: 2026-02-19*
