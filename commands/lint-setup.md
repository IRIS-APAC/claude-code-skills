# Lint Setup Command

Set up linting and pre-commit hooks automatically.

## Automated Setup

Run the setup script from the **git-workflow** skill:

```bash
python /path/to/skills/git-workflow/scripts/setup-linting.py
```

This script:
- Detects project languages automatically
- Installs appropriate linters and formatters
- Configures pre-commit hooks
- Sets up IDE integration
- Provides CI/CD integration steps

## Notes

- Pre-commit hooks run before each commit
- Never bypass hooks with `--no-verify` (unless explicitly requested)
- Test the setup by attempting a commit

See **git-workflow** skill for manual setup instructions and language-specific configurations.
