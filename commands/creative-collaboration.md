# Creative Collaboration Command

Unified creative collaboration toolkit with four modes: brainstorming, advanced elicitation, multi-agent party mode, and structured research.

## Instructions

When this command is invoked:

1. **Load the creative-collaboration skill** which provides four collaboration modes:

   - **Brainstorming** - Interactive ideation with 60+ creative techniques, anti-bias protocols, and a quantity-first approach (100+ ideas before organizing)
   - **Advanced Elicitation** - Structured analytical methods (50 methods across 11 categories) for deepening content and discovering requirements
   - **Party Mode** - Multi-agent expert discussion with diverse personas loaded from an agent manifest
   - **Research** - Comprehensive market, domain, or technical research with web verification and source citations

2. **Mode selection**:
   - Present the four modes and let the user choose
   - If the user's intent is clear from context (e.g., "let's brainstorm" or "research the market for X"), route directly to the appropriate mode
   - Modes can integrate with each other mid-session (e.g., invoke elicitation during brainstorming, feed research into brainstorming)

3. **Brainstorming mode** (`/creative-collaboration brainstorm`):
   - Discover the topic and context
   - Apply creative techniques iteratively from the brain-methods library
   - Push past obvious ideas into novel territory
   - Output: `brainstorming-session-{date}.md`

4. **Advanced Elicitation mode** (`/creative-collaboration elicit`):
   - Analyze context and present 5 best-fit elicitation methods
   - Execute selected methods against the content being analyzed
   - Loop until the user selects "proceed" (x)
   - Can be invoked from within brainstorming or other workflows

5. **Party Mode** (`/creative-collaboration party`):
   - Load agent personas from the agent manifest
   - Orchestrate natural multi-agent conversations with 2-3 relevant agents per round
   - Exit with `*exit`, `goodbye`, `end party`, or `quit`

6. **Research mode** (`/creative-collaboration research`):
   - Determine research type: Market, Domain, or Technical
   - Guided topic discovery and scope clarification
   - 6-step structured workflow per research type with web search verification
   - Output: Research document with findings, citations, analysis, and recommendations
   - Requires web search capability

**Purpose**: A comprehensive creative collaboration toolkit for ideation, structured analysis, multi-persona expert discussions, and systematic research.

The creative-collaboration skill contains complete workflow management, technique libraries, agent orchestration, research methodology, and facilitation guidance for all four modes.
