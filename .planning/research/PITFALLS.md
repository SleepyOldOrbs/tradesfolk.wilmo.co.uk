# Pitfalls Research

**Domain:** Agent Pool expansion -- adding 8 specialist agents to an existing 12-agent Claude Code plugin
**Researched:** 2026-02-20
**Confidence:** HIGH (based on measured analysis of existing codebase, v1.0 pitfalls experience, and Claude Code plugin mechanics)

## Critical Pitfalls

### Pitfall 1: Context budget overrun from 20-agent description payload

**What goes wrong:**
The design document estimates "~39k chars -> ~65k chars" for the expansion. The actual measured description payload across the existing 12 agents is 30,245 characters -- already far above the PROJECT.md claim of "3,903 chars total." There is a 2x variance between early agents (01-07 average 1,740 chars per description) and late agents (08-12 average 3,624 chars per description). If the 8 new agents follow the late-agent pattern (which is likely since those were written later and are more polished), the total description payload reaches approximately 59,237 characters. Combined with system prompt bodies, the full 20-agent file payload hits approximately 79,514 characters. Claude Code loads all agent descriptions into context for delegation matching at session start. This is shared budget with other plugins and skills. At 20 verbose agents, a user with one or two other plugins installed could hit context budget pressure, causing slower sessions, reduced working memory for actual tasks, or silent skill/agent exclusion.

**Why it happens:**
The description field serves double duty: it must be specific enough for accurate delegation matching (including example blocks), but every character consumed by descriptions is context that cannot be used for actual work. There is no enforcement mechanism -- you can write 10,000-character descriptions and nothing fails at write time. The pain only manifests during usage as degraded delegation accuracy and context pressure.

**How to avoid:**
1. Standardise description length across ALL 20 agents. Target 1,800-2,200 characters per description including example blocks. This yields ~40,000-44,000 total description chars for 20 agents -- a 33-45% increase from current, not the 95% increase that the late-agent pattern would produce.
2. Before writing any new agent, audit and normalise the existing agents 08-12 whose descriptions are roughly double the size of agents 01-07. The late agents use a `>-` YAML folding style (which strips trailing newlines) and embed full example blocks differently. Standardise on one format.
3. Measure total description payload after every agent addition. Keep a running tally. Do not "estimate" -- use `wc -c` on extracted descriptions.
4. The design document's "~65k chars estimated (within bounds)" claim has no basis -- there are no documented hard bounds for agent description budgets. Treat this as an assumption to validate, not a fact.

**Warning signs:**
- Total description payload exceeds 50,000 characters after adding 8 agents
- New agent descriptions exceed the longest existing description (security-auditor at 3,884 chars)
- Running `/context` after loading the plugin shows budget warnings
- Agent delegation accuracy drops (Claude picks wrong agents for tasks)

**Phase to address:**
Phase 1 (agent authoring). Establish a per-description character budget BEFORE writing any new agents. Normalise existing agents 08-12 as part of this phase, not as a separate task.

---

### Pitfall 2: Delegation confusion between overlapping new and existing agents

**What goes wrong:**
Several of the 8 new agents have significant expertise overlap with existing agents, creating ambiguous delegation zones. The most dangerous overlaps:

- **llm-application-developer vs data-scientist**: The existing data-scientist already covers "deep learning: PyTorch, transformers (Hugging Face), fine-tuning, LoRA/QLoRA" and "NLP: embeddings, RAG, prompt engineering, evaluation metrics." The new llm-application-developer covers "RAG pipelines, vector stores, agent orchestration, tool use, LangChain/LlamaIndex." A task like "build a RAG pipeline with LangChain" could plausibly route to either agent. Without crisp boundary definitions, Claude will inconsistently delegate these tasks.

- **prompt-engineer vs data-scientist**: The existing data-scientist already lists "prompt engineering" under NLP expertise. The new prompt-engineer specialises in "system prompt design, evaluation, red-teaming." The boundary needs to be crystal clear: prompt-engineer handles prompt crafting and evaluation; data-scientist handles model training and statistical analysis.

- **mlops-engineer vs devops-engineer**: The existing devops-engineer covers "Kubernetes, Helm, ArgoCD, cloud infrastructure, monitoring, Prometheus, Grafana." The new mlops-engineer covers "model serving, experiment tracking, training pipelines, GPU infra, MLflow/Kubeflow." Both manage infrastructure -- one for applications, one for models. But tasks like "set up GPU instances for model training" or "deploy a model to Kubernetes" sit in both domains.

- **embedded-engineer vs systems-programmer**: The existing systems-programmer covers "Rust, Go, C/C++, memory management, RAII, system calls." The new embedded-engineer covers "C/C++ firmware, RTOS, microcontrollers." Both write C/C++ code for constrained environments. A task like "write a C driver for an I2C sensor" could match either.

- **react-native-developer vs react-specialist**: Both work with React. The existing react-specialist covers "React 19, Next.js 15 App Router, server components." The new react-native-developer covers "React Native, Expo, mobile UI." A task like "build a React component for a mobile app" is ambiguous -- is it web-responsive (react-specialist) or React Native (react-native-developer)?

**Why it happens:**
Each agent is written in isolation, optimising for its own domain completeness. The description author naturally includes adjacent skills to make the agent feel comprehensive. But Claude's semantic matching sees ALL descriptions simultaneously and must choose ONE agent. When two agents both claim expertise in an area, Claude's choice becomes non-deterministic.

**How to avoid:**
1. For every new agent, write explicit "NOT this agent" guidance in the description commentary. Example: "RAG pipeline implementation goes to llm-application-developer. RAG evaluation and A/B testing of RAG quality goes to data-scientist."
2. Every example block in a new agent MUST include a commentary line that names the most likely confusion agent and explains why this agent is the correct choice. This is the delegation disambiguation pattern already used in the existing agents (e.g., javascript-developer examples distinguish from react-specialist).
3. Audit existing agent descriptions for skill claims that now overlap with new agents. The data-scientist description currently claims "prompt engineering" under NLP -- this should be softened to "prompt evaluation metrics" or removed, since a dedicated prompt-engineer now handles that domain.
4. Create a "delegation decision tree" as a reference during authoring: for any ambiguous task, which agent gets it and why?

**Warning signs:**
- Two agents' descriptions both mention the same specific technology (e.g., both mention "LangChain")
- Example blocks for two different agents show similar tasks
- During testing, the same task prompt routes to different agents in different sessions
- Users report unexpected agent selection for domain-specific tasks

**Phase to address:**
Phase 1 (agent authoring). Write overlap-resolution commentary into every description. Additionally, update existing agent descriptions where new agents take over specific sub-domains.

---

### Pitfall 3: Stale hard-coded roster in skills causes 8-agent blindspot

**What goes wrong:**
Both `browse-pool/SKILL.md` and `assemble-team/SKILL.md` contain hard-coded lists of all agents. The `assemble-team` skill has a table of 12 agents that Claude uses to make team recommendations. The `team-templates` skill has 7 templates referencing specific agent names. If these are not updated atomically with agent additions, the skills become a lie: they recommend teams from a 12-agent roster while 20 agents exist. Claude will never suggest the new agents through `assemble-team` because they are not in the skill's reference table. Users who rely on `/browse-pool` will not see the new agents listed.

This is worse than a missing feature -- it is active misinformation. The skill body IS the agent roster for recommendation purposes. Claude does not dynamically discover agents when executing a skill; it reads the skill body text.

**Why it happens:**
Skills are static markdown files. There is no mechanism to auto-generate skill content from the agents directory. The developer adds 8 agent files to `agents/`, tests that they load via auto-discovery (they do), and assumes the skills "just work." But auto-discovery controls which agents Claude CAN spawn, while skill content controls which agents Claude RECOMMENDS.

**How to avoid:**
1. Treat skill updates as a mandatory gated dependency of agent additions -- new agents are not "done" until skills reference them.
2. Update all three skills (`browse-pool`, `assemble-team`, `team-templates`) in the same commit or phase as agent additions.
3. After updating, verify the count: `browse-pool` lists 20 agents in 6+ domain categories, `assemble-team` table has 20 rows, `team-templates` has 12 templates.
4. Add to the project's "Looks Done But Isn't" checklist: "Diff agents/ directory listing against skill roster tables."

**Warning signs:**
- `/browse-pool` shows 12 agents when 20 exist
- `/assemble-team` never recommends any of the 8 new agents
- New team templates reference agents that `assemble-team` does not list

**Phase to address:**
Phase 3 (skill updates). Skills MUST be updated in the same phase that adds agents, not in a later phase. If agents are added in Phase 1, skill updates happen at the end of Phase 1.

---

### Pitfall 4: New team templates introduce untested agent combinations

**What goes wrong:**
The design adds 5 new team templates, bringing the total from 7 to 12. Each template is a specific combination of agents with a designated lead. The risk is that templates combine agents that have never worked together, creating team dynamics issues:

- **AI Application** (llm-application-developer lead + prompt-engineer + python-developer + qa-tester): This is a 4-agent team where the lead is a brand-new agent. The lead's system prompt determines how it delegates to teammates. If the llm-application-developer's "When given a task" section does not account for prompt-engineer as a collaborator, the team lead may ignore the prompt-engineer or duplicate their work.

- **IoT System** (embedded-engineer lead + systems-programmer + devops-engineer): The embedded-engineer is new, leading a team of two existing agents. The embedded-engineer must understand when to defer to systems-programmer (for high-level C/C++ design) versus handling firmware itself.

- **Native iOS + Android** (ios-developer lead + android-developer + ux-designer + qa-tester): Both ios-developer and android-developer are new. The template pairs them, but their system prompts may not reference each other's platforms, leading to duplicated work or conflicting architectural decisions.

**Why it happens:**
Templates are written as static lists of agent names. There is no mechanism to verify that the agents in a template have complementary system prompts, non-overlapping responsibilities, or a lead whose workflow accounts for the specific teammates.

**How to avoid:**
1. For every new template, write a 2-sentence justification explaining why THIS lead and THESE members. Not just "when to use" but "why this combination works."
2. The lead agent's system prompt should include awareness of roles it commonly collaborates with. For example, llm-application-developer should mention "defer prompt design and evaluation to a prompt specialist when available."
3. Do not assign brand-new agents as team leads until their system prompts have been tested. For the first release, consider giving leads to established agents. For example, the "AI Application" template could be led by python-developer (who already has tested system prompts) with llm-application-developer as a member.
4. Limit new templates to 3-4 members. The "Native iOS + Android" template with 4 members (2 new agents) is the riskiest composition.

**Warning signs:**
- Template lead is a brand-new agent that has never been tested as lead
- Template combines two or more brand-new agents
- Template members have overlapping domains (e.g., ios-developer and android-developer both working on "the mobile app" without clear platform separation)
- Template exceeds 4 members (team coordination overhead exceeds benefit)

**Phase to address:**
Phase 2 (team templates). Templates should be authored AFTER agent system prompts are finalised, not concurrently.

---

### Pitfall 5: Breaking existing agent descriptions while "normalising" for expansion

**What goes wrong:**
To manage context budget (Pitfall 1) and resolve delegation overlaps (Pitfall 2), there will be pressure to modify existing agent descriptions. Any change to an existing working agent description risks degrading its delegation accuracy. The current 12 agents have been validated -- they work. The temptation to "normalise" description format, trim length, or add overlap-resolution commentary could inadvertently weaken the trigger phrases that make delegation work. For example, shortening the security-auditor description from 3,884 chars to 2,200 chars to match a budget target means removing ~43% of its content. If the removed content includes key delegation triggers, the security-auditor stops being recommended for relevant tasks.

**Why it happens:**
Expansion creates cascading changes. You cannot add 8 agents to a shared context budget without adjusting the existing 12. But existing agents are the stable foundation -- they are validated and working. Treating them as equally mutable as the new agents is a category error.

**How to avoid:**
1. Apply a "do not break what works" principle: changes to existing agents should be additive (adding overlap-resolution commentary) or cosmetic (format normalisation), never subtractive (removing delegation trigger content).
2. If existing descriptions must be shortened, extract the SPECIFIC phrases used in example commentaries and ensure they survive the edit. The commentary phrases are the delegation routing mechanism.
3. Test existing agent delegation AFTER any modifications. Run the same test prompts used during v1.0 validation and verify the same agents are selected.
4. Version control existing descriptions separately: create a snapshot of all 12 current descriptions before any modifications, so you can diff and revert if delegation degrades.

**Warning signs:**
- Existing agent tests that passed in v1.0 now fail (wrong agent selected)
- Description changes remove `<example>` blocks or commentary text
- Batch reformatting changes every agent file in a single commit (impossible to isolate regressions)
- "Normalisation" removes more than 20% of any existing agent's description

**Phase to address:**
Phase 1 (agent authoring). If existing agents need modification, do it as a separate sub-task with its own validation step, not interleaved with new agent creation.

---

### Pitfall 6: Inconsistent system prompt structure in new agents

**What goes wrong:**
The three-section pattern (Core expertise / Working standards / When given a task) is the established convention across all 12 existing agents. New agents written by a different author or in a different session may drift from this pattern: using different heading names ("Technical skills" instead of "Core expertise"), different section ordering, different levels of specificity, or different line lengths. Even subtle inconsistencies like using numbered lists in "Core expertise" instead of bullet lists, or using imperative voice in "Working standards" ("Always validate input") versus declarative voice ("Validates all input"), degrade the uniform team feel that makes this plugin professional.

Additionally, the existing agents have remarkably consistent system prompt body lengths: 3,681 to 4,332 characters (17% variance). New agents that are significantly shorter (under 3,000 chars) signal a shallow prompt; significantly longer (over 5,000 chars) waste context for marginal benefit.

**Why it happens:**
When writing 8 agents across multiple sessions, each session has a slightly different context about "what good looks like." Without a concrete reference template with character counts and structural requirements, each agent drifts. The drift is small per-agent but cumulative across 8 agents.

**How to avoid:**
1. Create a concrete agent template BEFORE writing any of the 8 new agents. The template should include: exact heading names, bullet vs numbered list requirements, voice/tense requirements, target character ranges for each section, and a worked example.
2. Use one existing "gold standard" agent as the explicit reference. Recommendation: `01-javascript-developer.md` -- it has the cleanest structure, correct heading names, consistent voice, and sits within the target size range (3,828 chars body, 1,743 chars description).
3. Target system prompt body length: 3,800-4,200 characters. This matches the established range.
4. Write all 8 new agents in the same session or phase to maintain voice consistency.
5. After writing, diff each new agent against the template to verify structural compliance.

**Warning signs:**
- New agent headings do not match "Core expertise" / "Working standards" / "When given a task"
- New agent system prompt body is under 3,000 or over 5,000 characters
- New agents use a different list style (numbered vs bulleted) in sections that use bullets in existing agents
- New agents include sections not present in existing agents (e.g., "Limitations", "Do not", "Personality")

**Phase to address:**
Phase 1 (agent authoring). Establish the template and review criteria before writing the first new agent.

---

### Pitfall 7: Colour assignment creates visual confusion with existing agents

**What goes wrong:**
The design assigns android-developer to Green (backend domain) and embedded-engineer + mlops-engineer to Cyan (infrastructure domain). These are defensible individually but create specific confusion risks:

- **android-developer (Green)**: Placed in Green because "Kotlin is JVM-adjacent." But Green currently means "Backend & Systems" -- python-developer, backend-architect, systems-programmer, database-specialist. An Android mobile developer is fundamentally a frontend/UI developer for the Android platform. Placing it alongside backend-architect and database-specialist is categorically misleading. Users who filter by colour expecting "backend agents" will find a mobile UI developer.

- **Two Cyan agents**: Currently Cyan has exactly one agent (devops-engineer). Adding embedded-engineer and mlops-engineer triples the Cyan count. This dilutes Cyan's meaning from "DevOps" to a broader "Infrastructure + Hardware + ML Ops" category, which is vague.

- **Three Magenta agents**: Adding llm-application-developer, prompt-engineer, and computer-vision-engineer to the existing data-scientist and technical-writer makes Magenta the largest colour group (5 agents). The visual grouping becomes meaningless when it contains both "write API documentation" (technical-writer) and "build RAG pipelines" (llm-application-developer).

**Why it happens:**
The original colour scheme was designed for 12 agents with clear domain boundaries. Scaling to 20 agents means more agents per colour, diluting the categorical signal. The scheme was never designed for the nuanced distinctions between mobile-frontend, AI-application, and ML-infrastructure.

**How to avoid:**
1. Accept that the 6-colour scheme cannot cleanly encode 20 agents into meaningful categories. Do not force it. Some colours will become broad categories, and that is acceptable.
2. Move android-developer to Blue (frontend/UI), matching ios-developer. Both are mobile UI developers -- platform consistency matters more than language family. The design document itself says ios-developer is Blue because it "produces user-facing mobile interfaces." Android-developer produces exactly the same thing.
3. Document the colour scheme evolution in CLAUDE.md: explain that colours are approximate domain groupings, not strict categories, and that the roster table is the authoritative reference for agent capabilities.
4. Do NOT add new colours. Claude Code supports a fixed set of terminal colours. Introducing new colours would require plugin-level changes and is not worth the complexity.

**Warning signs:**
- android-developer appears in "Backend & Systems" grouping in browse-pool
- Magenta group has 5 agents with unrelated specialties
- Users ask "why is the Android developer green?" (colour violates intuition)

**Phase to address:**
Phase 1 (agent authoring). Colour assignments should be finalised before agent files are created. Changing colours after the fact requires updating agent files, browse-pool, CLAUDE.md roster table, and any documentation.

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hard-coding 20-agent roster in three separate skill files | Self-contained skills, no dynamic generation needed | Every agent addition requires updating 3 files plus CLAUDE.md roster table (4 manual edits) | Acceptable for 20 agents; becomes untenable above 25 |
| Using same `model: inherit` for all 8 new agents | Consistent with existing pattern, user controls model choice | prompt-engineer tasks are lightweight text analysis that overspend on Opus; embedded-engineer tasks may need Opus-level reasoning for firmware debugging | Acceptable for v1.1; revisit per-agent model assignments if cost complaints emerge |
| Not testing cross-agent delegation with all 20 loaded | Saves significant testing time (20 agents x multiple test prompts) | Undiscovered delegation conflicts between new agents and existing agents | Never -- at minimum test the 5 overlap pairs identified in Pitfall 2 |
| Writing new agents without updating existing agents' descriptions | Preserves validated existing agents | Existing agents still claim expertise in domains now covered by specialists (data-scientist claims "prompt engineering") | Only for initial v1.1.0 release; schedule existing agent description cleanup for v1.1.1 |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| browse-pool grouping | Adding new agents to existing groups without reconsidering group names | Add "Platform & Mobile" group for react-native-developer, ios-developer, android-developer; add "AI & ML" group for llm-application-developer, prompt-engineer, computer-vision-engineer; keep mlops-engineer and embedded-engineer in "Infrastructure" |
| assemble-team recommendations | Adding new agents to the roster table but not updating the "team sizing guidelines" section | Update sizing guidelines to account for mobile+backend (3-4 agents), AI/ML pipeline (3-5 agents), and platform-native development (4-5 agents including per-platform specialists) |
| team-templates numbering | Adding templates 8-12 without reviewing whether existing templates 1-7 should now reference new agents | Review all 7 existing templates: "Data Pipeline" (template 5) should now reference mlops-engineer as an optional member; "Full-Stack Feature" should mention react-native-developer for mobile contexts |
| CLAUDE.md roster table | Updating the table but not the "Context budget" paragraph that claims "~39,000 characters" | Update all quantitative claims in CLAUDE.md: agent count (20), template count (12), context budget measurement, domain groupings |
| plugin.json version | Forgetting to bump version from 1.0.0 to 1.1.0 | Bump version as the FIRST change in the expansion work, not the last |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| 20 agent descriptions consuming delegation matching budget | Slower task delegation, Claude occasionally ignoring available agents | Keep per-description target under 2,200 chars; total under 44,000 chars | When total description payload exceeds ~60,000 chars across all installed plugins |
| 12 team templates making skill body too large | `/team-templates` skill body consumes excessive context when invoked | Keep each template description to 3-4 lines; total skill body under 200 lines | When skill body exceeds ~400 lines and Claude truncates template details |
| Description example blocks duplicating across agents | Same example triggers multiple agents, wasting context | Ensure no two agents share task descriptions in their examples | When 3+ agents have overlapping example scenarios |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Giving prompt-engineer Implementation tier (Write/Edit) instead of Documentation tier | A prompt-engineer agent could modify application code when it should only write prompt files and evaluation criteria | Follow the design document: prompt-engineer gets Documentation tier (Read, Grep, Glob, Write, Edit, Bash) -- note this DOES include Write/Edit but NOT MultiEdit/NotebookEdit. This is correct for writing prompt documents but limits bulk code changes |
| Giving embedded-engineer Full access without considering what "Full access" means for firmware code | Full access includes WebFetch and WebSearch, which are fine, but also includes TodoWrite and potentially allows downloading untrusted toolchain binaries | Acceptable for embedded-engineer (needs Bash for cross-compilation toolchains). Document in the agent's working standards that downloaded binaries must be verified |
| New agents with `permissionMode: default` getting auto-approved for destructive operations | If a user sets global `--dangerously-skip-permissions`, all `default` mode agents bypass approval | This is the user's choice, not a plugin concern. Document that `default` means "follows user's permission settings" in CLAUDE.md |

## "Looks Done But Isn't" Checklist

- [ ] **Agent count verification:** All 20 agents load via auto-discovery -- verify with `ls agents/*.md | wc -l` (20 files) and Claude Code's `/agents` command (20 listed)
- [ ] **Description consistency:** All 20 agents use the same YAML frontmatter style -- verify no mix of `>` and `>-` folding operators, which produce different whitespace
- [ ] **Example blocks present:** All 8 new agents have exactly 3 `<example>` blocks -- verify with `grep -c '<example>' agents/1[3-9]*.md agents/20*.md`
- [ ] **Tool tier correctness:** prompt-engineer has Documentation tier, embedded-engineer and mlops-engineer have Full access, all others have Implementation -- verify tools field in each agent's frontmatter
- [ ] **browse-pool completeness:** Skill lists all 20 agents in correct domain groupings -- count agents listed and compare to `agents/` directory
- [ ] **assemble-team completeness:** Skill table has 20 rows -- count rows in the markdown table
- [ ] **team-templates completeness:** 12 templates listed, numbered 1-12 -- verify count and sequential numbering
- [ ] **CLAUDE.md roster table:** 20 rows in the roster table, all columns filled -- verify against agent files
- [ ] **Context budget measured:** Total description chars calculated and documented -- run `wc -c` measurement, not estimated
- [ ] **Overlap disambiguation:** Each new agent's examples explicitly name the confusion agent in commentary -- verify all 8 new agents reference their overlap neighbor
- [ ] **Colour assignments match:** Colour in agent frontmatter matches CLAUDE.md roster table matches browse-pool grouping -- verify no mismatches across all three locations
- [ ] **plugin.json version:** Version bumped to 1.1.0 -- verify before any publishing step

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Context budget overrun (>60k chars descriptions) | MEDIUM | Audit all 20 descriptions for length; trim longest first; focus on removing redundant technology lists, not example blocks; re-measure after each trim |
| Delegation confusion between overlapping agents | LOW | Add disambiguation commentary to description examples; test with ambiguous prompts; adjust until routing is consistent |
| Stale skill rosters (skills show 12 agents when 20 exist) | LOW | Update all three skill files; this is pure text editing with no behavioral risk |
| Broken team template combinations | LOW | Change template leads from new agents to established agents; reduce template member count to 3 |
| Existing agent descriptions broken by normalisation | MEDIUM | Revert to pre-modification descriptions from git; re-apply changes more conservatively; test each change in isolation |
| Inconsistent system prompt structure | LOW | Diff new agents against reference template; fix heading names, list styles, section order; no behavioral impact from structure-only changes |
| Colour scheme confusion | LOW | Update colour in agent frontmatter (one field change per file); update browse-pool grouping; update CLAUDE.md table |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Context budget overrun | Phase 1: Agent authoring | Measure total description chars with `wc -c`; must be under 50,000 chars |
| Delegation confusion (overlaps) | Phase 1: Agent authoring | Test each overlap pair with 3 ambiguous prompts; verify consistent routing |
| Stale skill rosters | Phase 3: Skill updates | Diff `agents/` file count against browse-pool agent count and assemble-team table rows |
| Untested team templates | Phase 2: Team templates | Verify each template lead's system prompt references awareness of its template members |
| Breaking existing agents | Phase 1: Agent authoring | Re-run v1.0 delegation test prompts after any existing agent modifications |
| Inconsistent prompt structure | Phase 1: Agent authoring | Diff each new agent against reference template for heading names, list style, char count |
| Colour scheme confusion | Phase 1: Agent authoring | Visual review of browse-pool groupings; verify android-developer is categorised as mobile/frontend not backend |
| CLAUDE.md and docs staleness | Phase 4: Documentation | Compare all quantitative claims (agent count, template count, context budget) against measured reality |
| plugin.json version not bumped | Phase 4: Documentation | Verify `plugin.json` shows 1.1.0 before any distribution step |
| README/CHANGELOG outdated | Phase 4: Documentation | Verify CHANGELOG has v1.1.0 entry listing all 8 new agents and 5 new templates |

## Sources

- Measured analysis of 12 existing agent files in `/var/www/tradesfolk.wilmo.co.uk/agents/` (character counts, description lengths, structural patterns)
- Approved design document: `docs/plans/2026-02-19-agent-pool-expansion-design.md`
- Project context: `.planning/PROJECT.md` (validated requirements, key decisions, constraints)
- v1.0 pitfalls research: `.planning/research/PITFALLS.md` (2026-02-19) -- foundational pitfalls for plugin mechanics
- Existing skill files: `skills/browse-pool/SKILL.md`, `skills/assemble-team/SKILL.md`, `skills/team-templates/SKILL.md`
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents) -- Description matching, context budget
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills) -- Skill budget limits

---
*Pitfalls research for: Agent Pool expansion (12 to 20 agents, v1.1.0)*
*Researched: 2026-02-20*
