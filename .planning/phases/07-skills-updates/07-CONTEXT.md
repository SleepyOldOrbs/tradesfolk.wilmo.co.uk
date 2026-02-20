# Phase 7: Skills Updates - Context

**Gathered:** 2026-02-20
**Status:** Ready for planning

<domain>
## Phase Boundary

Update three existing skills (browse-pool, assemble-team, team-templates) to reflect the expanded 20-agent roster. Add 5 new team templates and reorganize categories. No new skills or new skill types.

</domain>

<decisions>
## Implementation Decisions

### Template compositions
- **Mobile App**: react-native-developer (lead) + ios-developer + android-developer + qa-tester. Cross-platform with native devs for hybrid projects needing native modules.
- **Native iOS+Android**: backend-architect (lead) + ios-developer + android-developer + qa-tester. Architect ensures consistent API contracts across platforms.
- **AI Application**: llm-application-developer (lead) + prompt-engineer + backend-architect + qa-tester. Full stack AI app team.
- **ML Pipeline**: data-scientist (lead) + mlops-engineer + python-developer. Training-focused: experiment tracking, model training, data processing.
- **IoT System**: embedded-engineer (lead) + systems-programmer + devops-engineer. Hardware/firmware through to deployment.

### Category organization (browse-pool)
- Split current "Data & ML" category into two:
  - **Data Science** — data-scientist only
  - **AI & Machine Learning** — llm-application-developer, prompt-engineer, mlops-engineer, computer-vision-engineer
- New **Mobile & Platform** category containing: react-native-developer, ios-developer, android-developer, embedded-engineer
- Existing categories unchanged: Frontend & UI, Backend & Systems, Quality & Security, Infrastructure & Operations, Documentation
- Total: 8 categories (was 6, adding Mobile & Platform and AI & Machine Learning, splitting Data & ML into Data Science + AI & ML)

### Recommendation guidance (assemble-team)
- Add two new "always include" rules:
  - "Always include react-native-developer or native devs for mobile tasks"
  - "Always include prompt-engineer for tasks involving LLM prompts, evaluations, or AI-powered features"
- Raise team size caps: Small 1-2, Medium 2-4, Large 3-6 (was 3-5)
- Add a category column to the roster table: Agent | Category | Domain (three columns instead of two)

### Claude's Discretion
- Ordering of categories in browse-pool (user said "you decide" — after Frontend & UI feels natural)
- IoT System template composition (user moved on — embedded-engineer lead + systems-programmer + devops-engineer)
- Exact wording of "when to use" descriptions for all 5 new templates
- Any formatting improvements to existing skill content

</decisions>

<specifics>
## Specific Ideas

- Mobile & Platform category groups all platform-specific agents including embedded — "Platform" covers hardware too
- Backend-architect leads the Native iOS+Android template because the key value is consistent API contracts across platforms
- AI Application template is a full 4-person team including QA because evaluation/testing is critical for AI features
- ML Pipeline template is deliberately training-focused (not full lifecycle) — deployment/serving is separate

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 07-skills-updates*
*Context gathered: 2026-02-20*
