# Pull Request Command

Create a pull request for the current branch.

## Instructions

When this command is invoked:

1. **Verify quality checks**:
   - Run tests and ensure they pass
   - Check test coverage (reference **testing** skill for coverage requirements)
   - Run linters (`/lint`) and fix any issues
   - Ensure all changes are committed
   - **IMPORTANT: No AI attribution** - Do not add "Co-Authored-By: Claude" or similar to commits

2. Load the **git-workflow** skill for:
   - PR template structure
   - Target branch determination (feature/bugfix → `develop`, hotfix → `main`)
   - Review checklist
   - PR creation process with `gh pr create`

The git-workflow and testing skills contain complete PR requirements and quality standards.
