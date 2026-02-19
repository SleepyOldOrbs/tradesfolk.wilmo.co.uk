# Pitfalls Research

**Domain:** Claude Code plugin development (agent pool with specialist subagents, skills, hooks)
**Researched:** 2026-02-19
**Confidence:** HIGH (verified against official Claude Code docs at code.claude.com)

## Critical Pitfalls

### Pitfall 1: Agent description field is the sole discovery mechanism -- vague or bloated descriptions break task delegation

**What goes wrong:**
Claude Code uses semantic matching on the `description` field to decide when to delegate tasks to subagents. Descriptions that are too vague ("Helpful developer agent"), too generic ("Handles code tasks"), or too long (paragraph-length summaries) cause either missed delegation (Claude never picks the agent) or false positives (Claude picks the wrong agent for a task). The STATUS.md mentions adding `<example>` blocks to descriptions, but the official Claude Code subagent documentation (as of February 2026) does not define an `<example>` tag as a recognized frontmatter or description feature. The official docs say: "Write a clear description so Claude knows when to use it" and recommend phrases like "use proactively" for eager delegation. No structured `<example>` syntax is documented in the subagent specification.

**Why it happens:**
The plugin validator may have flagged a suggestion (not a hard requirement) about example blocks. Developers then treat validator suggestions as specification requirements, adding non-standard markup to the description field without verifying it has any effect on Claude's matching behaviour. Meanwhile, the actual description quality -- the thing that controls routing -- gets neglected.

**How to avoid:**
1. Write descriptions that answer "when should Claude delegate to this agent?" not "what can this agent do?"
2. Include specific task triggers: "Use for implementing features, refactoring JS/TS code, debugging runtime issues" (the current javascript-developer description already does this well).
3. If adding example-style content, use natural language within the description rather than XML-like tags that may not be parsed: "Good tasks: refactor auth middleware, add TypeScript types to API client, fix async race conditions."
4. Test each agent's description by asking Claude Code to handle tasks in that domain and verifying it selects the right agent.
5. Keep descriptions under 200 characters. Claude loads all agent descriptions into context; 12 agents with 500-character descriptions burns context budget unnecessarily.

**Warning signs:**
- Claude ignores available agents and spawns generic subagents instead.
- Claude delegates to the wrong specialist (e.g., sends a database migration task to the javascript-developer).
- `/agents` shows agents but Claude never invokes them in practice.

**Phase to address:**
Phase 1 (agent description refinement). This must be addressed before testing with real Agent Team sessions.

---

### Pitfall 2: TeammateIdle hook relies on an experimental feature gated behind a flag

**What goes wrong:**
The `TeammateIdle` hook event only fires within Agent Teams sessions, and Agent Teams are experimental, disabled by default, and gated behind the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable. Publishing a plugin that prominently features TeammateIdle hooks will confuse users who install the plugin for standard subagent use -- the hook simply never fires. Worse, the hook event name is correct per official docs, but the JSON input schema (`teammate_name`, `team_name`) differs from what the current `teammate-checklist.sh` expects (`teammate_name` -- correct, but accessed via `.teammate_name`, not `.teammate_name // "unknown"` which uses jq's alternative operator on a field that does exist when the hook fires).

**Why it happens:**
Agent Teams shipped alongside Opus 4.6 in February 2026 but remain experimental. The feature could change hook event names, input schemas, or even be removed. Plugins that depend on experimental features risk breaking silently when the feature stabilises.

**How to avoid:**
1. Document clearly in README that TeammateIdle hooks require Agent Teams to be enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).
2. Keep the hook lightweight and non-essential -- the current approach (log and allow idle) is correct. Do not make the hook a blocking quality gate unless users opt in.
3. Test the hook with an actual Agent Teams session before publishing. The official docs confirm the input includes `teammate_name` and `team_name` fields.
4. Add a graceful fallback: if the hook script receives empty or malformed input (because the schema changed), exit 0 rather than failing.

**Warning signs:**
- Hook script never fires during testing (forgot to enable Agent Teams flag).
- Hook fires but `jq` returns null for expected fields (schema changed).
- Users file issues saying "hooks don't work" (they're not using Agent Teams).

**Phase to address:**
Phase 2 (hook verification and testing). Test with Agent Teams enabled before release; document the prerequisite prominently.

---

### Pitfall 3: Plugin path references break after installation due to cache copying

**What goes wrong:**
When users install a plugin through a marketplace, Claude Code copies the plugin directory to `~/.claude/plugins/cache/`. Any paths that reference files outside the plugin root fail silently. The current `hooks.json` uses `${CLAUDE_PLUGIN_ROOT}` correctly, but if the `team-templates` skill or future additions reference external files (e.g., `../shared/`, or absolute paths from the development machine), they will break post-installation.

**Why it happens:**
During development, the plugin is used in-place (via `--plugin-dir` or direct path), so all relative paths resolve correctly. The copy-to-cache behaviour only manifests when installed through a marketplace or `claude plugin install`. Developers never see the breakage during local testing.

**How to avoid:**
1. Always use `${CLAUDE_PLUGIN_ROOT}` in hook commands and script references.
2. Never reference files outside the plugin directory.
3. Test the installation path, not just the development path: add the plugin to a local marketplace, install it, and verify hooks fire and skills load.
4. All paths in `plugin.json` must be relative and start with `./`.
5. If scripts need external tools (like `jq` in `teammate-checklist.sh`), document the dependency -- `jq` may not be installed on all users' systems.

**Warning signs:**
- Hooks work during development but fail silently after marketplace installation.
- "Script not found" errors in `claude --debug` output.
- Skills reference supporting files that don't exist in the cached copy.

**Phase to address:**
Phase 3 (pre-publish verification). Test the full install-from-marketplace flow before publishing.

---

### Pitfall 4: Skill description budget overflow silently excludes skills from Claude's context

**What goes wrong:**
Claude Code loads skill descriptions into context at session start, capped at 2% of the context window (with a fallback of 16,000 characters). If the plugin has many skills with verbose descriptions, some skills get silently excluded. Claude then cannot discover or auto-invoke those skills. With 2 current skills and a planned `team-templates` skill, this is unlikely now, but adding more skills or very long descriptions pushes toward the limit -- especially when users have other plugins installed that also consume the budget.

**Why it happens:**
The budget is shared across all installed plugins and user-level skills. Plugin authors test in isolation and don't account for other plugins consuming the same budget. The exclusion is silent -- no error, no warning (unless the user runs `/context`).

**How to avoid:**
1. Keep skill descriptions concise: one sentence, under 100 characters.
2. Put detailed instructions in the SKILL.md body, not the description.
3. Test with other plugins installed to verify your skills still appear.
4. Run `/context` after installation to check for budget warnings.

**Warning signs:**
- `/browse-pool` and `/assemble-team` stop appearing in autocomplete.
- Claude does not auto-invoke skills that previously worked.
- `/context` shows "excluded skills" warning.

**Phase to address:**
Phase 1 (skill definition). Keep descriptions lean from the start.

---

### Pitfall 5: Publishing without version bumping means users never see updates

**What goes wrong:**
Claude Code uses the `version` field in `plugin.json` to determine whether to update a cached plugin. If you push code changes to GitHub but forget to bump the version from `1.0.0`, existing users' plugin cache retains the old version indefinitely. They will never see your fixes, new agents, or new skills.

**Why it happens:**
The official docs explicitly warn: "If you change your plugin's code but don't bump the version in `plugin.json`, your plugin's existing users won't see your changes due to caching." Developers accustomed to Git-based workflows assume pulling the latest commit is enough.

**How to avoid:**
1. Bump `version` in `.claude-plugin/plugin.json` with every release.
2. Follow semver: new agents/skills = minor bump, bug fixes = patch bump, breaking changes = major bump.
3. Add a pre-push check or CI step that verifies the version was bumped if any plugin files changed.
4. Consider adding a CHANGELOG.md to track what changed per version.

**Warning signs:**
- Users report issues that you've already fixed.
- `claude plugin update` reports "already up to date" despite pushed changes.
- Version in plugin.json hasn't changed across multiple commits.

**Phase to address:**
Phase 4 (GitHub publishing). Establish version bumping discipline before first public release.

---

### Pitfall 6: Hook scripts not executable or missing shebang cause silent failures

**What goes wrong:**
Hook scripts that lack the executable bit (`chmod +x`) or a proper shebang line (`#!/bin/bash`) fail silently. Claude Code logs the failure in debug mode but does not surface it to the user. The hook is simply skipped, and the plugin appears to work but with degraded functionality.

**Why it happens:**
Git does not preserve file permissions on all platforms. A script that's executable on the developer's machine may lose its execute bit when cloned on another system. Additionally, the shebang line must match the target system -- `#!/bin/bash` works on Linux and macOS but `#!/usr/bin/env bash` is more portable.

**How to avoid:**
1. Use `git update-index --chmod=+x hooks/teammate-checklist.sh` to ensure Git tracks the executable bit.
2. Use `#!/usr/bin/env bash` as the shebang for portability.
3. Document in README that users may need to run `chmod +x` on hook scripts after cloning.
4. Test on a fresh clone, not just the development copy.

**Warning signs:**
- Hooks never fire on a fresh clone/install.
- `claude --debug` shows "Hook command completed with status 126" (permission denied) or "status 127" (command not found).
- Works on your machine but not on others.

**Phase to address:**
Phase 2 (hook verification). Verify executable bits are tracked in Git before publishing.

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| All agents use `model: inherit` | User's config decides; no surprises | Complex agents (backend-architect doing system design) may underperform on cheaper models | Acceptable for v1; revisit if specific agents consistently produce poor output on Haiku |
| Single hook script for all teammates | Simple, one file to maintain | Cannot enforce domain-specific checks (qa-tester should verify tests exist, technical-writer should verify docs) | Acceptable while TeammateIdle is experimental; refactor when Agent Teams stabilise |
| Hard-coding agent roster in `assemble-team` skill | Self-contained skill, no dynamic discovery | Adding a new agent requires updating the skill manually; forgetting creates a stale roster | Acceptable for <20 agents; add a dynamic roster mechanism if the pool exceeds 20 |
| No `tools` or `disallowedTools` in agent frontmatter | Agents inherit all tools; maximum flexibility | A technical-writer agent with Write/Edit access could modify code files it shouldn't | Never for security-auditor (should be read-only); address in v1 for safety-critical agents |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Claude Code plugin cache | Testing only via `--plugin-dir` (in-place), never through marketplace install | Test the full install path: create a local marketplace, install the plugin, verify all components load |
| Agent Teams + TeammateIdle hook | Assuming Agent Teams is enabled by default | Document the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` prerequisite; make the hook gracefully inert when Agent Teams is disabled |
| GitHub marketplace publishing | Using relative source paths in marketplace.json when distributing via URL | Use GitHub source type (`"source": "github", "repo": "owner/repo"`) for cross-platform compatibility |
| Plugin + user-level agents | Plugin agents conflict with user's personal agents of the same name | Use distinctive agent names; plugin agents use `plugin-name:agent-name` namespacing automatically, but check for clashes with common names |
| `jq` dependency in hook scripts | Assuming `jq` is installed on all target systems | Either bundle a simple parser, use Python's `json` module, or document `jq` as a prerequisite with installation instructions |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Too many agents bloat context with descriptions | Claude becomes slower, context budget warnings appear | Keep the roster focused (12-15 max); each agent description <200 chars | At ~20+ agents with verbose descriptions, especially when users have other plugins |
| Blocking hooks in TeammateIdle | Teammates cannot go idle; infinite retry loops if the check always fails | Always exit 0 for advisory checks; only exit 2 for hard gates with clear pass criteria | When the hook check depends on external state (e.g., CI pipeline) that may be unavailable |
| Skill body too long loads excessive context | Skill invocation consumes significant context budget | Keep SKILL.md under 500 lines; use supporting files for reference material | When skill body exceeds ~2000 lines; especially impactful for skills Claude auto-invokes frequently |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Hook script processes stdin without input validation | Malformed JSON input could cause unexpected script behaviour; shell injection if values are interpolated into commands | Always quote variables; validate JSON structure before extracting fields; use `jq -r` not `eval` |
| Plugin agents with `permissionMode: bypassPermissions` | Agent can execute any operation without user approval, including destructive file operations | Never set `bypassPermissions` on plugin agents; let users control permission modes |
| Hook scripts that write to arbitrary paths based on input | Path traversal attacks if `teammate_name` or other input contains `../` | Sanitise all input before using in file paths; use fixed output locations |

## "Looks Done But Isn't" Checklist

- [ ] **Agent descriptions:** Often missing "when to use" guidance -- verify each description explains what tasks trigger delegation, not just what the agent knows
- [ ] **Hook executable bits:** Often lost in Git -- verify `git ls-files -s hooks/` shows `100755` for shell scripts
- [ ] **Skill frontmatter `name` field:** Often mismatches directory name -- verify the `name` in SKILL.md matches the directory under `skills/`
- [ ] **Plugin version bump:** Often forgotten before publishing -- verify `plugin.json` version incremented from last release
- [ ] **assemble-team roster:** Often stale after adding agents -- verify the skill's agent table matches the actual `agents/` directory contents
- [ ] **CLAUDE.md accuracy:** Often outdated after structural changes -- verify directory tree and agent roster table match reality
- [ ] **README.md install instructions:** Often untested -- verify the documented install command actually works on a fresh machine
- [ ] **`jq` dependency:** Often assumed but not documented -- verify hook scripts either handle missing `jq` gracefully or README lists it as a prerequisite
- [ ] **Agent Teams flag:** Often forgotten in documentation -- verify README mentions `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is needed for hooks

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Vague agent descriptions causing wrong delegation | LOW | Edit description field in agent .md files; no schema changes, takes effect on session restart |
| Hook script not executable on user machines | LOW | Run `chmod +x` and recommit with `git update-index --chmod=+x`; push version bump |
| Cache staleness (version not bumped) | LOW | Bump version in plugin.json, push; users run `claude plugin update` |
| Plugin paths break after marketplace install | MEDIUM | Audit all paths for `${CLAUDE_PLUGIN_ROOT}` usage; fix and re-publish with version bump |
| Skill budget overflow excluding skills | LOW | Shorten descriptions; no code changes needed beyond SKILL.md frontmatter |
| TeammateIdle schema change in future Claude Code version | MEDIUM | Update hook script to handle new schema; add graceful fallback for unrecognised fields; publish patch version |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Vague/bloated agent descriptions | Phase 1: Agent description refinement | Test delegation by asking Claude to handle domain-specific tasks; confirm correct agent selected |
| `<example>` blocks -- non-standard markup | Phase 1: Agent description refinement | Check official docs before adding; use natural language examples in description instead |
| TeammateIdle experimental dependency | Phase 2: Hook verification | Enable Agent Teams flag, start a team session, verify hook fires with correct JSON input |
| Hook script not executable | Phase 2: Hook verification | Fresh clone on different machine; `ls -la hooks/` shows `x` bit; `claude --debug` shows hook execution |
| Skill budget overflow | Phase 1: Skill definition | Run `/context` after installing plugin alongside other plugins; verify no exclusion warnings |
| Plugin cache path breakage | Phase 3: Pre-publish verification | Install via local marketplace; verify all hooks fire, all skills load, all agents appear |
| Version not bumped | Phase 4: GitHub publishing | Compare `plugin.json` version to last release tag; CI check on push |
| assemble-team roster stale | Phase 1 or whenever agents added | Diff `agents/` directory listing against the table in `assemble-team/SKILL.md` |
| jq dependency undocumented | Phase 4: README and documentation | Test hook on system without jq; document requirement or remove dependency |
| Agent names conflicting with user agents | Phase 4: Publishing | Plugin namespacing handles this automatically (`agent-pool:agent-name`), but verify with `/agents` after install |

## Sources

- [Plugins reference - Claude Code Docs](https://code.claude.com/docs/en/plugins-reference) -- Official plugin manifest schema, component specifications, debugging
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) -- Agent frontmatter fields, description matching, model options, tool restrictions
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills) -- Skill format, frontmatter fields, budget limits, invocation control
- [Hooks reference - Claude Code Docs](https://code.claude.com/docs/en/hooks) -- Hook events, TeammateIdle/TaskCompleted specifics, exit codes, JSON schemas
- [Orchestrate teams of Claude Code sessions - Claude Code Docs](https://code.claude.com/docs/en/agent-teams) -- Agent Teams experimental status, teammate coordination, hooks integration
- [Create and distribute a plugin marketplace - Claude Code Docs](https://code.claude.com/docs/en/plugin-marketplaces) -- Marketplace publishing, version management, source types, validation
- [Claude Code plugins README - GitHub](https://github.com/anthropics/claude-code/blob/main/plugins/README.md) -- Plugin structure examples
- [Awesome Claude Code Subagents - VoltAgent/GitHub](https://github.com/VoltAgent/awesome-claude-code-subagents) -- Community agent patterns and organisation

---
*Pitfalls research for: Claude Code plugin (agent pool with specialist subagents)*
*Researched: 2026-02-19*
