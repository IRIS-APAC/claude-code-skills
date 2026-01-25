# Format Command

Auto-format code according to project standards.

## Quick Commands

**Python**: `black . && ruff check --fix .`
**JavaScript/TypeScript**: `prettier --write . && eslint --fix .`
**C#**: `dotnet format`
**Flutter/Dart**: `dart format .`
**Terraform**: `terraform fmt -recursive`
**JSON/YAML/Markdown**: `prettier --write "**/*.{json,yaml,yml,md}"`

## Notes

- Commit before formatting (easy rollback)
- Formatting should not change behavior
- Run linters after formatting to verify

See **git-workflow** skill for formatter configurations and IDE integration.
