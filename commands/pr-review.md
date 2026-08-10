# Pull Request Review Command

Review a pull request for code quality and standards.

## Arguments

- **PR number** (optional): When provided (e.g. `pr-review 42` or "review PR 42"), review that specific PR. You **must** switch to that branch before reviewing: `gh pr checkout <PR#>`

## Instructions

When this command is invoked:

1. **If a PR number is specified**: Switch to that branch before reviewing:
   ```bash
   gh pr checkout <PR#>
   ```

2. **Complete the PR test plan before review**:
   - Verify the PR description includes a **Testing** section (or equivalent test plan)
   - All test plan tasks must be **checked off** (`[x]`) before proceeding to approve
   - Do not approve until every test plan item is verified and marked complete
   - If any test plan checkboxes remain `[ ]`, request the author to complete them before approving

3. Load the **git-workflow** skill for:
   - Complete PR review checklist (code quality, testing, documentation, architecture, git)
   - Review best practices and guidelines
   - Feedback templates

   Additionally, load the **testing** skill for:
   - Test coverage verification
   - Test quality assessment

## Approval Requirements

**CRITICAL**: When approving a PR, ALWAYS include a detailed comment using the `-b` flag:

```bash
gh pr review 42 --approve -b "LGTM!

✅ Tests pass
✅ Code quality good
✅ Type hints present
✅ Error handling appropriate

Ready to merge."
```

**Never approve without a comment** - empty approvals provide no context for the audit trail.

**IMPORTANT: No AI attribution** - Do not add "Co-Authored-By: Claude" or similar to review comments or suggestions. However, if a PR being reviewed contains AI attribution, this is NOT a blocking issue - don't reject the PR for that reason alone.

The skills contain comprehensive review checklists and standards.
