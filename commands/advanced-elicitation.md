# Advanced Elicitation Command

Apply guided requirement elicitation methods to enhance content, discover deeper insights, and improve document quality.

## Instructions

When this command is invoked:

1. **Load the advanced-elicitation skill** for:
   - Method registry loading from the elicitation methods library
   - Context-aware method selection (5 best-fit methods presented)
   - Iterative application of elicitation techniques
   - Content enhancement through structured analysis

2. **Elicitation flow**:
   - Analyze the current context (content type, complexity, stakeholder needs)
   - Present 5 recommended elicitation methods to choose from
   - Execute selected methods against the content being analyzed
   - Show enhanced version and ask for approval before applying
   - Loop until the user selects "proceed" (x)

3. **Available actions during elicitation**:
   - **1-5**: Select and apply a specific elicitation method
   - **r**: Reshuffle for 5 new method recommendations
   - **a**: List all available methods with descriptions
   - **x**: Proceed with the enhanced content

4. **Integration with other workflows**:
   - Can be invoked during `/iris-brainstorming` for deeper exploration
   - Works with `/iris-party-mode` agents for multi-persona elicitation
   - Enhances sections during requirements and design workflows

**Purpose**: Systematically improve content quality through diverse analytical techniques including stakeholder analysis, risk assessment, creative exploration, and structured reasoning methods.

The advanced-elicitation skill contains the complete method library and execution guidelines.
