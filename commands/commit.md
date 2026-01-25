# Commit Command

Create a git commit following project conventions.

## Quick Steps

1. Review changes: `git status` and `git diff`
2. Stage files: `git add <files>`
3. Commit with message format: `type(scope): description`
4. **IMPORTANT: No AI attribution** - Do not add "Co-Authored-By: Claude" or similar

## Commit Format

```
type(scope): description

Optional body explaining why.
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`

## Notes

- Never use `--no-verify` unless explicitly requested
- If hooks fail, fix issues and create new commit (don't amend)
- Use imperative mood: "add feature" not "added feature"

See **git-workflow** skill for complete commit conventions.
