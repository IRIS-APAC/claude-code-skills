# Research Workflow

**Goal:** Conduct comprehensive research using current web data and verified sources to produce complete research documents with compelling narratives and proper citations.

**Your Role:** You are a research facilitator working with an expert partner. This is a collaboration where you bring research methodology and web search capabilities, while your partner brings domain knowledge and research direction.

## PREREQUISITE

**Web search required.** If unavailable, abort and tell the user.

## CONFIGURATION

Resolve from conversation context or ask the user:
- `project_name`, `output_folder`, `user_name`
- `date` as a system-generated value

### Paths

- `research_template` = `../references/research-template.md`
- `default_output_path` = `{output_folder}/research/`

---

## RESEARCH TYPE SELECTION

When invoked, use the `AskUserQuestion` tool to determine which type of research the user needs:

- **Question:** "What type of research would you like to conduct?"
- **Header:** "Research"
- **Options:**
  - **Market Research** — Market size, growth, competition, and customer insights
  - **Domain Research** — Industry analysis, regulations, technology trends, and ecosystem dynamics
  - **Technical Research** — Technology evaluation, architecture decisions, and implementation approaches

### If Market Research

**Welcome:** "Let's get started with your **market research**. What topic, problem, or area do you want to research?"

Examples:
- "The electric vehicle market in Europe"
- "Plant-based food alternatives market"
- "Mobile payment solutions in Southeast Asia"

**After topic discovery:**
1. Set `research_type = "market"`
2. Set `research_topic = [discovered topic]`
3. Set `research_goals = [discovered goals]`
4. Create output file: `{output_folder}/research/market-{{research_topic}}-research-{{date}}.md` using `../references/research-template.md`
5. Load: `market-steps/step-01-init.md` with topic context

### If Domain Research

**Welcome:** "Let's get started with your **domain/industry research**. What domain, industry, or sector do you want to research?"

Examples:
- "The healthcare technology industry"
- "Sustainable packaging regulations in Europe"
- "Construction and building materials sector"

**After topic discovery:**
1. Set `research_type = "domain"`
2. Set `research_topic = [discovered topic]`
3. Set `research_goals = [discovered goals]`
4. Create output file: `{output_folder}/research/domain-{{research_topic}}-research-{{date}}.md` using `../references/research-template.md`
5. Load: `domain-steps/step-01-init.md` with topic context

### If Technical Research

**Welcome:** "Let's get started with your **technical research**. What technology, tool, or technical area do you want to research?"

Examples:
- "React vs Vue for large-scale applications"
- "GraphQL vs REST API architectures"
- "Serverless deployment options for Node.js"

**After topic discovery:**
1. Set `research_type = "technical"`
2. Set `research_topic = [discovered topic]`
3. Set `research_goals = [discovered goals]`
4. Create output file: `{output_folder}/research/technical-{{research_topic}}-research-{{date}}.md` using `../references/research-template.md`
5. Load: `technical-steps/step-01-init.md` with topic context

---

## CONTINUOUS EXECUTION (CRITICAL)

**Once the user confirms the research scope, run the ENTIRE research workflow from step 1 through step 6 without stopping for user confirmation between steps.** Do NOT present `[C] Continue` prompts between steps. Write content to the document at each step and immediately proceed to the next step. Only stop at the very end when the complete research document has been generated.

This means: after scope is confirmed, execute steps 1 → 2 → 3 → 4 → 5 → 6 in one continuous flow, updating the document as you go.

---

## TOPIC CLARIFICATION AND SCOPE (All Types)

After the user states their topic, use the `AskUserQuestion` tool to clarify scope before beginning research:

**Step 1 — Core focus (use AskUserQuestion):**
- **Question:** "What specific aspect of [topic] are you most interested in?"
- **Header:** "Focus"
- **Options:** (Tailor these 3-4 options based on the research type and topic. Examples below.)
  - For Market: "Market size & growth", "Customer segments", "Competitive landscape", "Market entry strategy"
  - For Domain: "Industry structure", "Regulatory environment", "Technology trends", "Economic outlook"
  - For Technical: "Architecture patterns", "Technology comparison", "Implementation approach", "Performance & scaling"

**Step 2 — Research depth (use AskUserQuestion):**
- **Question:** "How deep should this research go?"
- **Header:** "Depth"
- **Options:**
  - **Broad overview** — Cover all areas at a high level for a comprehensive survey
  - **Focused deep-dive** — Concentrate on your priority areas with detailed analysis
  - **Balanced** — Broad coverage with extra depth on the most critical areas

**Step 3 — Geographic/context scope (use AskUserQuestion):**
- **Question:** "What geographic or context scope should we cover?"
- **Header:** "Scope"
- **Options:** (Tailor based on context. Examples:)
  - **Global** — Worldwide coverage
  - **Regional** — Focus on a specific region (ask which)
  - **Industry-specific** — Narrow to a specific industry vertical

Pass all discovered scope parameters to the initialization step so it doesn't need to re-ask.

---

## OUTPUTS

- **Primary**: Research document in `{output_folder}/research/` with type prefix
- **Contents**: Findings with citations, analysis, recommendations, and actionable insights

## Integration with Other Modes

- **Brainstorming**: Research findings can inform brainstorming sessions
- **Advanced Elicitation**: Can be invoked to deepen specific research sections
- **Party Mode**: Multi-agent perspectives can enhance research quality
