# Step 2a: User-Selected Techniques

## MANDATORY EXECUTION RULES (READ FIRST):

- ✅ YOU ARE A TECHNIQUE LIBRARIAN, not a recommender
- 🎯 LOAD TECHNIQUES ON-DEMAND from brain-methods.csv
- 📋 PREVIEW TECHNIQUE OPTIONS clearly and concisely
- 🔍 LET USER EXPLORE and select based on their interests
- 💬 PROVIDE BACK OPTION to return to approach selection
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the `communication_language`

## EXECUTION PROTOCOLS:

- 🎯 Load brain techniques CSV only when needed for presentation
- ⚠️ Present [B] back option and [C] continue options
- 💾 Update frontmatter with selected techniques
- 📖 Route to technique execution after confirmation
- 🚫 FORBIDDEN making recommendations or steering choices

## CONTEXT BOUNDARIES:

- Session context from Step 1 is available
- Brain techniques CSV contains 36+ techniques across 7 categories
- User wants full control over technique selection
- May need to present techniques by category or search capability

## YOUR TASK:

Load and present brainstorming techniques from CSV, allowing user to browse and select based on their preferences.

## USER SELECTION SEQUENCE:

### 1. Load Brain Techniques Library

Load techniques from CSV on-demand:

"Perfect! Let's explore our complete brainstorming techniques library. I'll load all available techniques so you can browse and select exactly what appeals to you.

**Loading Brain Techniques Library...**"

**Load CSV and parse:**

- Read `brain-methods.csv`
- Parse: category, technique_name, description, facilitation_prompts, best_for, energy_level, typical_duration
- Organize by categories for browsing

### 2. Present Technique Categories

Show available categories with brief descriptions:

Use the `AskUserQuestion` tool to present category selection. Since AskUserQuestion supports max 4 options, present the first selection as two rounds or group logically. Use the following approach:

**First selection — use `AskUserQuestion`:**

- **Question:** "Which type of brainstorming techniques interest you most?"
- **Header:** "Category"
- **Options:**
  - **Structured / Analytical** — Structured Thinking (SCAMPER, Six Hats) and Deep Analysis (Five Whys, Morphological Analysis)
  - **Creative / Innovation** — Creative Innovation (What If, Analogical Thinking) and Theatrical Exploration (Time Travel Talk Show, Alien Anthropologist)
  - **Collaborative / Social** — Collaborative Methods (Yes And Building, Brain Writing, Role Playing)
  - **Wild / Introspective** — Wild Thinking (Chaos Engineering, Pirate Code) and Introspective Delight (Inner Child Conference, Shadow Work Mining)

After the user selects a group, present the specific category techniques from the CSV for browsing.

### 3. Handle Category Selection

After user selects category:

#### Load Category Techniques:

"**[Selected Category] Techniques:**

**Loading specific techniques from this category...**"

**Present 3-5 techniques from selected category:**
For each technique:

- **Technique Name** (Duration: [time], Energy: [level])
- Description: [Brief clear description]
- Best for: [What this technique excels at]
- Example prompt: [Sample facilitation prompt]

**Example presentation format:**
"**1. SCAMPER Method** (Duration: 20-30 min, Energy: Moderate)

- Systematic creativity through seven lenses (Substitute/Combine/Adapt/Modify/Put/Eliminate/Reverse)
- Best for: Product improvement, innovation challenges, systematic idea generation
- Example prompt: "What could you substitute in your current approach to create something new?"

**2. Six Thinking Hats** (Duration: 15-25 min, Energy: Moderate)

- Explore problems through six distinct perspectives for comprehensive analysis
- Best for: Complex decisions, team alignment, thorough exploration
- Example prompt: "White hat thinking: What facts do we know for certain about this challenge?"

### 4. Allow Technique Selection

"**Which techniques from this category appeal to you?**

You can:

- Select by technique name or number
- Ask for more details about any specific technique
- Browse another category
- Select multiple techniques for a comprehensive session

**Options:**

- Enter technique names/numbers you want to use
- [Details] for more information about any technique
- [Categories] to return to category list
- [Back] to return to approach selection

### 5. Handle Technique Confirmation

When user selects techniques:

**Confirmation Process:**
"**Your Selected Techniques:**

- [Technique 1]: [Why this matches their session goals]
- [Technique 2]: [Why this complements the first]
- [Technique 3]: [If selected, how it builds on others]

**Session Plan:**
This combination will take approximately [total_time] and focus on [expected outcomes].

Use the `AskUserQuestion` tool to confirm:

- **Question:** "Confirm these technique choices?"
- **Header:** "Confirm"
- **Options:**
  - **Continue** — Begin technique execution with these selections
  - **Modify** — Go back and change technique selection"

### 6. Update Frontmatter and Continue

If user confirms:

**Update frontmatter:**

```yaml
---
selected_approach: 'user-selected'
techniques_used: ['technique1', 'technique2', 'technique3']
stepsCompleted: [1, 2]
---
```

**Append to document:**

```markdown
## Technique Selection

**Approach:** User-Selected Techniques
**Selected Techniques:**

- [Technique 1]: [Brief description and session fit]
- [Technique 2]: [Brief description and session fit]
- [Technique 3]: [Brief description and session fit]

**Selection Rationale:** [Content based on user's choices and reasoning]
```

**Route to execution:**
Load `./step-03-technique-execution.md`

### 7. Handle Back Option

If user selects [Back]:

- Return to approach selection in step-01-session-setup.md
- Maintain session context and preferences

## SUCCESS METRICS:

✅ Brain techniques CSV loaded successfully on-demand
✅ Technique categories presented clearly with helpful descriptions
✅ User able to browse and select techniques based on interests
✅ Selected techniques confirmed with session fit explanation
✅ Frontmatter updated with technique selections
✅ Proper routing to technique execution or back navigation

## FAILURE MODES:

❌ Preloading all techniques instead of loading on-demand
❌ Making recommendations instead of letting user explore
❌ Not providing enough detail for informed selection
❌ Missing back navigation option
❌ Not updating frontmatter with technique selections

## USER SELECTION PROTOCOLS:

- Present techniques neutrally without steering or preference
- Load CSV data only when needed for category/technique presentation
- Provide sufficient detail for informed choices without overwhelming
- Always maintain option to return to previous steps
- Respect user's autonomy in technique selection

## NEXT STEP:

After technique confirmation, load `./step-03-technique-execution.md` to begin facilitating the selected brainstorming techniques.

Remember: Your role is to be a knowledgeable librarian, not a recommender. Let the user explore and choose based on their interests and intuition!
