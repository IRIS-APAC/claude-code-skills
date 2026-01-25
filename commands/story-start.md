# Story Start Command

Begin work on a user story with proper analysis and setup.

## Instructions

When this command is invoked:

1. **Identify the story**:
   - Ask for story ID/number if not provided
   - Use **agile-board** skill to fetch story details from board (ZenHub/Jira/Linear)
   - Review description, acceptance criteria, and dependencies

2. **Create feature branch**:
   - Use `/branch` command to create properly named branch
   - Format: `feature/epic-X-story-Y.Z-description`
   - Update story status to "In Progress" on the board

3. **Run developer analysis**:
   - Load the **developer-analysis** skill for:
     - Requirements analysis and ambiguity identification
     - Technical design proposal
     - POC script creation for third-party integrations
     - Architecture reconciliation
     - User approval process before implementation

**CRITICAL**: Always run developer-analysis BEFORE writing any implementation code to avoid rework.
