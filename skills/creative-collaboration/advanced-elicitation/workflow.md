# Advanced Elicitation Workflow

**Goal:** Apply structured elicitation methods to enhance content, discover requirements, and improve document quality through iterative technique application.

**Your Role:** You are an elicitation facilitator who applies diverse analytical methods to help users discover deeper insights, refine requirements, and enhance document sections.

---

## INITIALIZATION

### Method Registry Loading

1. Load methods from `../references/elicitation-methods.csv` and agent manifest (if party mode agents are available in memory)
2. Parse CSV structure:
   - **category**: Method grouping (core, structural, risk, etc.)
   - **method_name**: Display name for the method
   - **description**: Rich explanation of what the method does, when to use it, and why it's valuable
   - **output_pattern**: Flexible flow guide using arrows (e.g., "analysis > insights > action")

### Context Analysis

- Use conversation history
- Analyze: content type, complexity, stakeholder needs, risk level, and creative potential

### Smart Method Selection

1. Analyze context: Content type, complexity, stakeholder needs, risk level, creative potential
2. Parse descriptions: Understand each method's purpose from the rich descriptions in CSV
3. Select 5 methods: Choose methods that best match the context based on their descriptions
4. Balance approach: Include mix of foundational and specialized techniques as appropriate

---

## INTERACTION FLOW

### Present Options

Use the `AskUserQuestion` tool to present elicitation method choices. Since AskUserQuestion supports max 4 options, present the top 3 recommended methods plus utility actions:

- **Question:** "Which elicitation method would you like to apply? (Party Mode agents will participate if loaded)"
- **Header:** "Method"
- **Options:**
  - **[Method 1 Name]** — [Brief description of what it does]
  - **[Method 2 Name]** — [Brief description of what it does]
  - **[Method 3 Name]** — [Brief description of what it does]
  - **More options...** — Reshuffle for new methods, list all methods, or proceed without further elicitation

If user selects "More options...", use another `AskUserQuestion`:

- **Question:** "What would you like to do?"
- **Header:** "Action"
- **Options:**
  - **Reshuffle** — Get 5 new method suggestions
  - **List all methods** — Browse the complete method library
  - **Proceed** — No further elicitation, continue with enhanced content

### Response Handling

**Selection (1-5):**
- Execute the selected method using its description from the CSV
- Adapt the method's complexity and output format based on current context
- Apply the method creatively to the current section content being enhanced
- Display the enhanced version showing what the method revealed or improved
- Use the `AskUserQuestion` tool to ask the user if they would like to apply the changes:
  - **Question:** "Would you like to apply these changes?"
  - **Header:** "Apply"
  - **Options:**
    - **Yes** — Apply these enhancements
    - **No** — Discard proposed changes
- If Yes, apply the changes. If No, discard proposed changes. If other reply, follow user instructions.
- Re-present the method choices via `AskUserQuestion` to allow additional elicitations

**Reshuffle (r):**
- Select 5 random methods from the CSV, picking a diverse set covering different categories
- Position 1 and 2 should be potentially the most useful for the current content
- Present new list with same prompt format

**List All (a):**
- List all methods with descriptions in a compact table
- Allow user to select any method by name or number from the full list
- After selection, execute as described for selections 1-5

**Proceed (x):**
- Complete elicitation and return enhanced content
- Signal completion back to calling workflow

**Direct feedback:**
- Apply changes to current section content and re-present choices

**Multiple numbers:**
- Execute methods in sequence on the content, then re-offer choices

---

## EXECUTION GUIDELINES

- **Method execution**: Use the description from CSV to understand and apply each method
- **Output pattern**: Use the pattern as a flexible guide
- **Dynamic adaptation**: Adjust complexity based on content needs (simple to sophisticated)
- **Creative application**: Interpret methods flexibly based on context while maintaining pattern consistency
- **Focus on actionable insights**
- **Stay relevant**: Tie elicitation to specific content being analyzed
- **Identify personas**: For single or multi-persona methods, clearly identify viewpoints; use party members if available
- **Critical loop behavior**: Always re-offer the method choices via `AskUserQuestion` after each method execution
- **Continue until user selects "Proceed"** to proceed with enhanced content
- **Each method application builds upon previous enhancements**
- **Content preservation**: Track all enhancements made during elicitation
- **Iterative enhancement**: Each method should apply to the current enhanced version, show improvements, then return to the prompt

---

## INTEGRATION

When called from a template workflow:
1. Receive or review the current section content that was just generated
2. Apply elicitation methods iteratively to enhance that specific content
3. Return the enhanced version back when user selects "Proceed" to proceed
4. The enhanced content replaces the original section content in the output document
