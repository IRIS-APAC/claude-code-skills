# Requirements & Design Command

Gather requirements and create world-class design documentation for a project or feature.

## Instructions

When this command is invoked:

1. **Detect first-timers**:
   - Ask: "Is this your first time running a requirements gathering session?"
   - If **Yes**: Offer interactive walkthrough with explanations at each step
   - If **No**: Proceed with standard process

2. **Load the requirements-design skill** for:
   - Capturing non-negotiable constraints (platforms, compliance, budget, timeline)
   - Challenging assumptions and researching alternatives
   - Creating 5 core documents:
     1. **Constraints** - Project boundaries and guiding principles
     2. **Customer Value** - Value proposition (Working Backwards methodology)
     3. **Solution Design** - High-level delivery approach
     4. **Requirements** - Detailed functional/non-functional specifications
     5. **Architecture** - Technical blueprint with component diagrams
   - Optional: Story decomposition, effort estimation, technical pointers

3. **Active architecture guidance**:
   - Questions vague requirements ("build a dashboard" → "What problem does it solve?")
   - Challenges technology choices ("we need Redis" → researches alternatives)
   - Validates feasibility (cost, timeline, operational overhead)
   - Suggests better alternatives with pros/cons/costs

4. **Integration with other skills**:
   - After completing documents, offer to invoke:
     - `/developer-analysis` - Create technical POCs and mocks
     - `/testing` - Define test strategy from requirements
     - `/project-management` - Create board tickets and plan sprints

**Output**: All 5 documents in `docs/Design/` directory, production-ready for implementation.

**Typical session**: 2-4 hours for complete requirements and design documentation.

The skill contains comprehensive templates, first-timer guidance, and end-to-end examples.
