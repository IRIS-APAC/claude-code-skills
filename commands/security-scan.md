# Security Scan Command

Run security scans for vulnerabilities.

## Dependency Scanning

**Python**: `pip-audit` or `safety check`
**JavaScript**: `npm audit` (auto-fix: `npm audit fix`)
**C#**: `dotnet list package --vulnerable`

## Code Scanning

**Static analysis**: `semgrep --config=auto .`
**Python security**: `bandit -r .`
**Secret detection**: `gitleaks detect`

## Severity Priority

- **Critical**: Fix immediately
- **High**: Fix before next release
- **Medium**: Plan for upcoming sprint
- **Low**: Address when convenient

## Notes

- Never commit secrets (use `.env` files, gitignored)
- Rotate any accidentally committed secrets
- Keep dependencies updated
- Run before each release
