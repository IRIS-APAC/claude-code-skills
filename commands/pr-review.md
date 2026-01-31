# Pull Request Review Command

Review a pull request for code quality and standards.

## Instructions

When this command is invoked, load the **git-workflow** skill for:
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
