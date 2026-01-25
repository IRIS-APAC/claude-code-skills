---
name: developer-analysis
description: "Engineering analysis before implementation. Use when: (1) Starting work on a story, (2) Analyzing requirements and identifying ambiguities, (3) Creating POC scripts for third-party integrations, (4) Proposing technical design for user approval, (5) Reconciling with existing architecture. Proactively use BEFORE writing any implementation code to ensure alignment and reduce rework."
model: opus
---

# Developer Analysis

Pre-implementation engineering analysis workflows to ensure clear understanding, validated integrations, and approved designs before writing code.

## Overview

This skill covers the **analysis phase** that happens after a story is assigned to you but **before** you start implementing. It bridges the gap between project management (story creation) and git workflow (implementation).

**Benefits**:
- Clarifies ambiguous requirements early
- Validates third-party integrations with POC scripts
- Proposes design for user approval before time investment
- Ensures alignment with existing architecture
- Prevents rework from misunderstanding requirements
- Documents design decisions for future reference

## Critical Rules

**CRITICAL**: Before writing any implementation code, perform thorough analysis of story requirements.

### 1. Mandatory Analysis Before Implementation
- ✅ **ALWAYS perform analysis** before writing implementation code
- ✅ **Challenge assumptions** - Question vague requirements, missing constraints, and technical assumptions
- ✅ **Create POC scripts** for third-party integrations BEFORE full implementation
- ✅ **Propose design** and get user approval before coding
- ❌ **NEVER start coding** without understanding the "why" behind requirements
- ❌ **NEVER accept vague requirements** without clarification

### 2. POC Scripts for Third-Party Integrations
- ✅ **Create POC first** for external APIs, new libraries, uncertain integrations
- ✅ **Store in** `scripts/poc/` with documentation in `scripts/poc/README.md`
- ✅ **De-risk integration** work before committing to full implementation
- ❌ **NEVER integrate** external services without testing them first

### 3. Design Proposal Pattern
- ✅ **Always propose design** before implementing (post as comment on story ticket)
- ✅ **Wait for user approval** before coding
- ✅ **Include**: approach, technical decisions, POC findings, components, trade-offs, testing strategy
- ❌ **NEVER skip** design approval for non-trivial stories

### 4. Configuration and Reusability
- ✅ **Externalize configuration** - Use .env, YAML, JSON for environment-specific values
- ✅ **Never commit secrets** - Use .env files in .gitignore, provide .env.example
- ✅ **Validate configuration** - Fail fast with clear error messages for missing/invalid config
- ❌ **NEVER hardcode** API endpoints, credentials, or magic numbers
- ❌ **NEVER commit** .env files with secrets

### 5. When to Use This Skill

Use this skill proactively when:
1. **Starting work on any non-trivial story** - Before first commit
2. **Requirements are unclear** - Identify and clarify ambiguities
3. **Third-party integration needed** - Create POC script first
4. **Multiple implementation approaches possible** - Propose design for approval
5. **Architecture reconciliation needed** - Check alignment with existing patterns
6. **Complex technical decisions required** - Document trade-offs and get approval

## Model Selection

**CRITICAL**: This skill requires extended thinking capabilities for deep analysis.

**Recommended model**: Opus or Sonnet with extended thinking mode

**Why extended thinking is required**:
- **Challenging assumptions** - Requires careful reasoning to identify flaws in user requirements
- **Analyzing ambiguous requirements** - Need to think through multiple interpretations
- **Evaluating design trade-offs** - Complex comparison of multiple approaches
- **Identifying hidden edge cases** - Deep thinking to surface non-obvious scenarios
- **Security and architecture analysis** - Thorough reasoning about system implications
- **Design proposal creation** - Structured thinking about component interactions

**When to use standard model**:
- Simple POC script execution (once approach is validated)
- Straightforward MCP tool calls for ticket updates

## Quick Start

### Story Analysis Workflow (9 Steps)

1. **Read thoroughly** - Story, ACs, comments, references, linked docs
2. **Check technical pointers** - Documentation links, reference implementations
3. **Analyze existing architecture** - Reconcile approach with documented patterns
4. **Identify ambiguities** - Find unclear requirements, missing constraints
5. **Clarify with user** - Ask questions, get decisions
6. **Create POC script** (for third-party integrations) - Prove it works first!
7. **Propose design approach** - Get approval before implementing
8. **Update story ticket** - Add "Design" section to story description
9. **Begin implementation** - Move to "In Progress", use POC as reference

See `references/story-analysis.md` for complete workflow with examples.

## Best Practices

### 1. Challenge Assumptions and Requirements

**CRITICAL**: Good engineering analysis requires critical thinking and challenging the user's assumptions.

**Why challenge**:
- Prevents implementing the wrong solution
- Surfaces hidden complexity early
- Identifies better alternatives
- Ensures requirements are well-thought-out
- Reduces rework from misunderstood needs

**What to challenge**:

**Vague requirements**:
```
User: "Make the search faster"
Challenge: "What's the current performance? What's the target? Which queries are slow?
           Are we optimising for average case or worst case?"
```

**Missing constraints**:
```
User: "Add user authentication"
Challenge: "What about session management? Password reset? Multi-factor auth?
           Account lockout after failed attempts? GDPR compliance for user data?"
```

**Technical assumptions**:
```
User: "Use Redis for caching"
Challenge: "Have we considered cache invalidation strategy? What's the eviction policy?
           How do we handle cache stampede? Is Redis the right fit vs in-memory cache?"
```

**Over-engineering**:
```
User: "Build a microservices architecture for user management"
Challenge: "Do we need microservices for 100 users? Would a monolith be simpler to start?
           What's the deployment complexity? Do we have the team to maintain it?"
```

**Under-engineering**:
```
User: "Just store passwords in the database"
Challenge: "What about password hashing? Salt? Key derivation function (bcrypt/Argon2)?
           This is a security risk - we need proper password storage."
```

**Unvalidated third-party integrations**:
```
User: "Integrate with the XYZ API"
Challenge: "Have we tested the API? What's the rate limit? Error handling?
           Should we create a POC script first to validate it works?"
```

**Missing edge cases**:
```
User: "Parse the PDF and extract text"
Challenge: "What about scanned PDFs (OCR needed)? Password-protected PDFs?
           Corrupted files? Non-text PDFs (images only)? What's the error handling?"
```

**How to challenge effectively**:
- ✅ Ask clarifying questions (don't assume)
- ✅ Propose alternatives with trade-offs
- ✅ Point out risks and missing requirements
- ✅ Suggest POC scripts for uncertain integrations
- ✅ Reference existing architecture patterns
- ❌ Don't accept vague requirements without clarification
- ❌ Don't implement without understanding the "why"
- ❌ Don't skip edge cases and error scenarios

**Example challenge workflow**:
```
1. Read story: "Add file upload feature"
2. Identify gaps:
   - What file types? Size limits? Virus scanning?
   - Where stored? S3? Local filesystem?
   - What about duplicate files? Overwrites?
   - Progress indication for large files?
   - Error handling for network failures?
3. Challenge user with questions
4. Get clarifications
5. Update story with detailed requirements
6. Proceed with design
```

### 2. Modular Design and Reuse

**CRITICAL**: Maximize reuse and maintainability through modular design.

**Principles**:
- **DRY (Don't Repeat Yourself)** - Extract common logic into reusable modules
- **Single Responsibility** - Each module/class/function does one thing well
- **Interface Segregation** - Design focused interfaces, not monolithic ones
- **Dependency Injection** - Pass dependencies, don't hardcode them
- **Composition over Inheritance** - Prefer composing behavior from small modules

**Examples**:

✅ **Good - Modular design**:
```python
# Reusable validation module
class Validator:
    @staticmethod
    def validate_email(email: str) -> bool:
        return bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email))

# Reusable authentication module
class Authenticator:
    def __init__(self, validator: Validator):
        self.validator = validator

    def authenticate(self, email: str, password: str) -> bool:
        if not self.validator.validate_email(email):
            raise ValueError("Invalid email format")
        # ... auth logic
```

❌ **Bad - Monolithic, non-reusable**:
```python
# Everything in one place, no reuse
class UserLogin:
    def login(self, email: str, password: str) -> bool:
        # Validation hardcoded here
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Invalid email")
        # Auth logic here
        # Can't reuse validation or auth separately
```

**When designing, ask**:
- Can this logic be reused in other contexts?
- Is this module focused on one responsibility?
- Can I test this module in isolation?
- Would another developer understand this module's purpose immediately?

### 3. Configuration and Parameterization

**CRITICAL**: Make software configurable and reusable by externalizing configuration.

**Why configuration matters**:
- Enables code reuse across environments (dev/staging/prod)
- Separates configuration from code (12-factor app principle)
- Allows customization without code changes
- Improves testability with different configs
- Prevents hardcoded secrets and magic numbers
- Supports deployment flexibility

**What to configure**:

**Environment-specific values**:
```
✅ Configure:
- API endpoints (dev: localhost:3000, prod: api.example.com)
- Database connections (dev DB, staging DB, prod DB)
- Feature flags (enable beta features in staging)
- Log levels (DEBUG in dev, INFO in prod)
- Timeouts and retry policies
- Resource limits (connection pools, rate limits)

❌ Don't hardcode:
- API_URL = "https://api.example.com"  # Use config instead
- MAX_RETRIES = 3  # Should be configurable
- LOG_LEVEL = "DEBUG"  # Should vary by environment
```

**Secrets and credentials**:
```
✅ Use environment variables or secret managers:
- API keys, tokens, passwords
- Database credentials
- Encryption keys
- Third-party service credentials

❌ NEVER commit:
- Secrets in config files (.env in .gitignore)
- Hardcoded passwords in code
- API keys in source code
```

**Business logic parameters**:
```
✅ Configure when values might change:
- Pagination limits (items per page)
- Validation rules (password minimum length)
- Thresholds (max file size, rate limits)
- Timeouts (request timeout, cache TTL)

❌ Don't over-configure:
- Core business rules that never change
- Fundamental algorithms
- Critical security constraints
```

**Configuration file formats**:

**Environment Variables (.env)**:
```bash
# .env (for secrets and environment-specific values)
# NEVER commit this file - add to .gitignore

DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=secret-key-123
REDIS_URL=redis://localhost:6379
LOG_LEVEL=DEBUG
```

**When to use**:
- ✅ Secrets and credentials
- ✅ Environment-specific overrides
- ✅ Docker/container deployments
- ✅ 12-factor app configuration
- ❌ Complex nested structures
- ❌ Committed configuration (use YAML/TOML instead)

**YAML (.yaml/.yml)**:
```yaml
# config/settings.yaml (committed to repo)
# Use for structured, readable configuration

app:
  name: "My Application"
  version: "1.0.0"

server:
  host: "${SERVER_HOST:-localhost}"  # Default to localhost
  port: ${SERVER_PORT:-8000}
  timeout: 30

database:
  pool_size: ${DB_POOL_SIZE:-10}
  max_overflow: 20

features:
  beta_enabled: false
  new_search: true
```

**When to use**:
- ✅ Application settings (committed to repo)
- ✅ Multi-environment configs
- ✅ Hierarchical configuration
- ✅ Human-readable, team-edited configs
- ❌ Secrets (use .env instead)

**JSON (.json)**:
```json
{
  "app": {
    "name": "My Application",
    "version": "1.0.0"
  },
  "server": {
    "host": "localhost",
    "port": 8000
  },
  "features": {
    "beta_enabled": false
  }
}
```

**When to use**:
- ✅ API responses, data interchange
- ✅ Machine-generated configs
- ✅ Configuration consumed by JavaScript
- ❌ Human-edited configs (YAML more readable)
- ❌ Comments needed (JSON doesn't support)

**TOML (.toml)**:
```toml
# config.toml (committed to repo)
# Rust, Python projects often use TOML

[app]
name = "My Application"
version = "1.0.0"

[server]
host = "localhost"
port = 8000
timeout = 30

[database]
pool_size = 10
url = "${DATABASE_URL}"  # From environment variable
```

**When to use**:
- ✅ Python (pyproject.toml), Rust (Cargo.toml)
- ✅ Typed configuration
- ✅ Readable, supports comments
- ❌ Complex nested structures (YAML better)

**12-Factor App Configuration Principles**:

1. **Store config in environment** - Use environment variables for env-specific values
2. **Strict separation** - Never commit secrets to version control
3. **Environment parity** - Same code runs in all environments with different config
4. **Config validation** - Validate configuration at startup, fail fast

**Configuration layering pattern**:

```python
# Layer 1: Default values (in code or default.yaml)
DEFAULT_CONFIG = {
    "server": {"port": 8000, "host": "localhost"},
    "database": {"pool_size": 10}
}

# Layer 2: Environment-specific file (config/production.yaml)
# Overrides defaults

# Layer 3: Environment variables (highest priority)
# Overrides file-based config

# Final config = Layer 1 + Layer 2 + Layer 3
```

**Configuration validation and type safety**:

**Python example (Pydantic)**:
```python
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    """Type-safe configuration with validation."""

    # Required fields
    database_url: str
    api_key: str

    # Optional with defaults
    server_port: int = 8000
    log_level: str = "INFO"
    max_connections: int = 100

    # Validation
    @validator('log_level')
    def validate_log_level(cls, v):
        allowed = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        if v not in allowed:
            raise ValueError(f'log_level must be one of {allowed}')
        return v

    @validator('max_connections')
    def validate_max_connections(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('max_connections must be between 1 and 1000')
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

# Usage
settings = Settings()  # Loads from .env, validates on startup
print(settings.server_port)  # Type-safe access
```

**TypeScript example (Zod)**:
```typescript
import { z } from 'zod';

const configSchema = z.object({
  database: z.object({
    url: z.string().url(),
    poolSize: z.number().min(1).max(100).default(10),
  }),
  server: z.object({
    port: z.number().min(1).max(65535).default(8000),
    host: z.string().default('localhost'),
  }),
  logLevel: z.enum(['DEBUG', 'INFO', 'WARNING', 'ERROR']).default('INFO'),
});

type Config = z.infer<typeof configSchema>;

// Load and validate configuration
const config: Config = configSchema.parse({
  database: {
    url: process.env.DATABASE_URL,
    poolSize: parseInt(process.env.DB_POOL_SIZE || '10'),
  },
  server: {
    port: parseInt(process.env.PORT || '8000'),
  },
  logLevel: process.env.LOG_LEVEL || 'INFO',
});
```

**Flutter/Dart example**:
```dart
class AppConfig {
  final String apiBaseUrl;
  final String apiKey;
  final int timeout;
  final bool enableAnalytics;

  const AppConfig({
    required this.apiBaseUrl,
    required this.apiKey,
    this.timeout = 30,
    this.enableAnalytics = false,
  });

  // Factory for different environments
  factory AppConfig.development() {
    return const AppConfig(
      apiBaseUrl: 'http://localhost:3000',
      apiKey: 'dev-key',
      enableAnalytics: false,
    );
  }

  factory AppConfig.production() {
    return const AppConfig(
      apiBaseUrl: 'https://api.example.com',
      apiKey: String.fromEnvironment('API_KEY'),
      enableAnalytics: true,
    );
  }

  // Load from environment
  factory AppConfig.fromEnvironment() {
    const env = String.fromEnvironment('ENVIRONMENT', defaultValue: 'dev');

    return env == 'production'
        ? AppConfig.production()
        : AppConfig.development();
  }
}
```

**Avoid magic numbers and hardcoded values**:

❌ **Bad - Magic numbers**:
```python
def calculate_discount(price):
    if price > 100:  # What does 100 mean?
        return price * 0.15  # What's 0.15?
    return price * 0.05
```

✅ **Good - Named constants**:
```python
DISCOUNT_THRESHOLD = 100  # Minimum price for premium discount
PREMIUM_DISCOUNT_RATE = 0.15  # 15% discount for orders > £100
STANDARD_DISCOUNT_RATE = 0.05  # 5% standard discount

def calculate_discount(price, config=None):
    config = config or get_config()

    threshold = config.get('discount_threshold', DISCOUNT_THRESHOLD)
    premium_rate = config.get('premium_discount_rate', PREMIUM_DISCOUNT_RATE)
    standard_rate = config.get('standard_discount_rate', STANDARD_DISCOUNT_RATE)

    if price > threshold:
        return price * premium_rate
    return price * standard_rate
```

**Configuration documentation**:

**Include in design proposal**:
```markdown
## Configuration

**Required environment variables**:
- `DATABASE_URL` - PostgreSQL connection string (format: postgresql://user:pass@host:port/db)
- `API_KEY` - Third-party service API key
- `REDIS_URL` - Redis connection string (default: redis://localhost:6379)

**Optional environment variables**:
- `SERVER_PORT` - HTTP server port (default: 8000)
- `LOG_LEVEL` - Logging level: DEBUG|INFO|WARNING|ERROR (default: INFO)
- `MAX_CONNECTIONS` - Database connection pool size (default: 10, range: 1-100)

**Configuration files**:
- `config/default.yaml` - Default configuration (committed)
- `config/production.yaml` - Production overrides (committed)
- `.env` - Local environment variables (NOT committed, copy from .env.example)

**Example `.env` file**:
```bash
DATABASE_URL=postgresql://localhost:5432/myapp
API_KEY=your-api-key-here
LOG_LEVEL=DEBUG
```
```

**Create `.env.example`**:
```bash
# .env.example (committed to repo as template)
# Copy this to .env and fill in real values

# Database (required)
DATABASE_URL=postgresql://localhost:5432/myapp

# External Services (required)
API_KEY=your-api-key-here

# Server Configuration (optional)
SERVER_PORT=8000
LOG_LEVEL=INFO

# Feature Flags (optional)
ENABLE_BETA_FEATURES=false
```

**Testing with configuration**:

**Test with different configs**:
```python
def test_service_with_custom_config():
    """Test service behaviour with custom configuration."""
    test_config = {
        "max_retries": 5,
        "timeout": 10,
        "api_url": "http://localhost:9999"
    }

    service = MyService(config=test_config)

    # Test with test-specific configuration
    result = service.process()
    assert result is not None

def test_service_with_default_config():
    """Test service with default configuration."""
    service = MyService()  # Uses default config

    result = service.process()
    assert result is not None

@pytest.fixture
def test_settings():
    """Fixture providing test configuration."""
    return Settings(
        database_url="sqlite:///:memory:",  # In-memory DB for tests
        api_key="test-key",
        log_level="DEBUG"
    )

def test_with_settings_fixture(test_settings):
    """Test using fixture configuration."""
    service = MyService(settings=test_settings)
    result = service.process()
    assert result is not None
```

**Configuration anti-patterns**:

❌ **Anti-pattern 1: Configuration in code**:
```python
# ❌ Bad
API_URL = "https://api.example.com"  # Hardcoded
DB_PASSWORD = "secret123"  # Security risk!
```

✅ **Good**:
```python
import os

API_URL = os.getenv("API_URL")
DB_PASSWORD = os.getenv("DB_PASSWORD")  # From environment

# Validate required config
if not API_URL or not DB_PASSWORD:
    raise ValueError("Missing required configuration")
```

❌ **Anti-pattern 2: No validation**:
```python
# ❌ Bad - No validation, fails at runtime
timeout = int(os.getenv("TIMEOUT"))  # Crashes if not set
```

✅ **Good**:
```python
# ✅ Good - Validate and provide defaults
timeout = int(os.getenv("TIMEOUT", "30"))

if timeout < 1 or timeout > 300:
    raise ValueError(f"TIMEOUT must be between 1 and 300, got {timeout}")
```

❌ **Anti-pattern 3: Over-configuration**:
```python
# ❌ Bad - Configuring things that should never change
ALGORITHM_NAME = os.getenv("ENCRYPTION_ALGORITHM", "AES-256-GCM")
# Security-critical algorithms shouldn't be configurable
```

✅ **Good**:
```python
# ✅ Good - Security-critical values are hardcoded
ENCRYPTION_ALGORITHM = "AES-256-GCM"  # Never configurable

# Only configure non-security-critical aspects
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # From environment
```

**Include in design proposal**:
- What configuration is needed
- Default values for optional config
- Validation rules for each config value
- Where configuration is stored (.env, YAML, etc.)
- How to set up configuration for local development

### 4. Architecture Reconciliation

**Before proposing design**, check alignment with existing architecture:

**Check**:
- Does the story align with documented architecture patterns?
- Are there conflicts with existing design decisions?
- Should architecture be updated to accommodate this story?
- Are there cross-cutting concerns (logging, error handling, auth) to follow?

**Common architecture docs to check**:
- `/docs/architecture/` - Architecture documentation
- `/docs/design/` - Design documents
- `ARCHITECTURE.md` - Root-level architecture overview
- `/docs/adr/` - Architecture Decision Records (ADRs)
- Epic-level design docs

**If conflicts exist**:
- Raise them with user BEFORE implementing
- Propose either: (a) adjust the story, or (b) update the architecture
- Document the decision in an ADR if significant

### 4. Proof-of-Concept (POC) Scripts

**CRITICAL**: For third-party integrations, create POC scripts BEFORE full implementation.

**When to create POC**:
- Integrating with external APIs (Entra, AWS services, SaaS)
- Using new libraries or frameworks for the first time
- Uncertain about how a third-party service works
- Complex authentication flows
- Complex end-to-end integration flows
- Data transformation from external sources

**Where to store**:
- `scripts/poc/` - Proof-of-concept scripts
- `scripts/poc/README.md` - Documentation of findings

**Benefits**:
- De-risks integration work
- Validates assumptions about third-party APIs
- Creates working reference for full implementation
- Documents working code patterns
- Faster to iterate on simple script than full implementation

See `references/story-analysis.md` section 6 for detailed POC workflow and examples.

### 5. Design Proposal Pattern

**Always propose design before implementing**:

**Design proposal should include**:
- **High-level approach** - What you'll build
- **Key technical decisions** - Libraries, patterns, approaches chosen
- **POC findings** - If POC script was created, reference learnings
- **Component breakdown** - What modules/files created or modified
- **Integration points** - How it connects to existing code
- **Trade-offs** - Why this approach over alternatives
- **Testing strategy** - How you'll test it
- **Modular design** - How modules will be reusable and maintainable

**Post as comment on story ticket** BEFORE implementing.

**Wait for user approval** before coding.

### 6. Dependency Analysis

**Identify dependencies early**:

**Types of dependencies**:
- **Story dependencies** - Other stories that must be completed first
- **Library dependencies** - External packages required
- **Service dependencies** - External APIs or services needed
- **Data dependencies** - Required data sources or formats
- **Team dependencies** - Work from other teams needed

**Document in design proposal**:
- What dependencies exist
- How they'll be managed
- What happens if dependency is unavailable
- Fallback or mitigation strategies

### 7. Security Review Checklist

**Before implementing, consider security**:

**Common security concerns**:
- **Authentication** - How will users be authenticated?
- **Authorization** - What permissions are required?
- **Input validation** - All user input validated?
- **Output encoding** - Prevent XSS, injection attacks?
- **Secrets management** - No hardcoded secrets, use environment variables?
- **Data encryption** - Sensitive data encrypted at rest and in transit?
- **Rate limiting** - Prevent abuse and DoS?
- **Audit logging** - Security events logged?

**Cloud authentication** (AWS, Azure, GitHub Actions):
- **CRITICAL**: Use zero-secrets architecture (OIDC, Workload Identity Federation)
- ✅ GitHub Actions → AWS/Azure: Use OIDC (no long-lived credentials)
- ✅ AWS → Azure integration: Use Workload Identity Federation (no Client Secret)
- ✅ Local development: Use `az login` or `aws sso login` (no shared secrets)
- ✅ JWT validation: Use public keys (no Client Secret needed)
- ❌ NEVER store long-lived credentials (AWS Access Keys, Azure Client Secrets)
- ❌ NEVER commit secrets to version control

See `references/authentication-patterns.md` for complete zero-secrets architecture patterns.

**OWASP Top 10**:
- Injection (SQL, NoSQL, OS command, LDAP)
- Broken authentication
- Sensitive data exposure
- XML External Entities (XXE)
- Broken access control
- Security misconfiguration
- Cross-Site Scripting (XSS)
- Insecure deserialization
- Using components with known vulnerabilities
- Insufficient logging and monitoring

**Include in design proposal**:
- Security considerations for this story
- How security concerns are addressed
- Any security trade-offs made

### 8. Performance Baseline

**For performance-sensitive work, establish baseline**:

**Establish baseline before implementation**:
- Current performance metrics (response time, throughput, resource usage)
- Target performance metrics
- Acceptable performance ranges
- How performance will be measured
- Tools for performance testing

**Include in design proposal**:
- Performance requirements
- How performance will be verified
- Performance trade-offs considered

### 9. Technical Spikes

**For highly uncertain work, consider technical spike**:

**When to use spike**:
- Very uncertain about feasibility
- Multiple approaches possible, unclear which is best
- New technology or framework
- Complex integration with unknown constraints

**Spike workflow**:
1. Time-box the spike (e.g., 4 hours, 1 day)
2. Define spike goals clearly
3. Create experimental code (doesn't need to be production quality)
4. Document findings
5. Propose approach based on learnings
6. Throw away spike code (don't use in production)

**Spike deliverable**: Design proposal with findings and recommended approach.

## Australian English

All documentation uses **Australian English spelling**:
- ✅ normalise, organisation, authorisation, optimise, colour, behaviour, analyse
- ❌ normalize, organization, authorization, optimize, color, behavior, analyze

This is a **project-wide standard**, not optional.

## Related Skills

- **project-management** - For writing stories, planning epics (before developer analysis)
- **git-workflow** - For implementation, commits, PRs (after developer analysis)
- **agile-board** - For board operations, moving tickets to "In Progress"

## Workflow Integration

**Complete development workflow**:
1. **Project Management** - Story created with ACs, estimated, added to sprint
2. **Developer Analysis** (THIS SKILL) - Analyze, POC, propose design, get approval
3. **Git Workflow** - Implement, commit, create PR, review, merge
4. **Agile Board** - Move ticket through pipelines (In Progress → Review/QA → Done)

## Documentation Standards

**CRITICAL**: Maintain documentation throughout development lifecycle, not as an afterthought.

### When to Document

**During Phase 2: Analysis**:
- ✅ Create/update Architecture Decision Records (ADRs) for significant design decisions
- ✅ Document POC findings in `scripts/poc/README.md`
- ✅ Include documentation plan in design proposal

**During Phase 3: Implementation**:
- ✅ Add inline code documentation for complex logic
- ✅ Update API documentation (OpenAPI/Swagger) for new endpoints
- ✅ Update README if setup/configuration changes

**During Phase 4: Pull Request**:
- ✅ Ensure PR description includes documentation updates
- ✅ Verify README accuracy for changed features
- ✅ Check API docs are regenerated (if applicable)

### 1. README Maintenance

**When to update README**:
- ✅ New features added (add to Features section)
- ✅ Setup/installation changes (dependencies, environment variables)
- ✅ Configuration changes (new .env variables, config files)
- ✅ API endpoints added/changed (link to API docs)
- ✅ Breaking changes (highlight in CHANGELOG and README)

**README structure** (standard pattern):
```markdown
# Project Name

Brief description (1-2 sentences)

## Features

- Feature 1
- Feature 2

## Prerequisites

- Node.js 18+
- PostgreSQL 15+
- Redis 7+

## Installation

```bash
npm install
cp .env.example .env
# Edit .env with your values
```

## Configuration

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `API_KEY` - Third-party service API key

## Usage

```bash
npm run dev  # Development
npm run build  # Production build
npm test  # Run tests
```

## API Documentation

See [API Docs](docs/api.md) or visit `/api/docs` when running.

## Architecture

See [Architecture Overview](docs/architecture/README.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

**What NOT to put in README**:
- ❌ Inline code examples for every function (use API docs instead)
- ❌ Detailed implementation details (use ADRs or code comments)
- ❌ Historical information (use CHANGELOG)

### 2. API Documentation (OpenAPI/Swagger)

**For REST APIs**, generate OpenAPI specification from code:

**Python (FastAPI)**:
```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API for managing users and authentication",
    version="1.0.0",
    docs_url="/api/docs",  # Swagger UI at /api/docs
    redoc_url="/api/redoc"  # ReDoc at /api/redoc
)

@app.post("/users", tags=["Users"], summary="Create a new user")
async def create_user(user: UserCreate) -> User:
    """
    Create a new user account.

    Args:
        user: User registration data

    Returns:
        Created user object

    Raises:
        HTTPException: 400 if email already exists
    """
    ...
```

**TypeScript (Express + tsoa)**:
```typescript
import { Body, Controller, Post, Route, Tags, SuccessResponse } from 'tsoa';

@Route('users')
@Tags('Users')
export class UsersController extends Controller {
  /**
   * Create a new user account
   * @param user User registration data
   * @returns Created user object
   */
  @Post()
  @SuccessResponse(201, 'Created')
  public async createUser(@Body() user: UserCreate): Promise<User> {
    ...
  }
}
```

**When to update API docs**:
- ✅ New endpoints added
- ✅ Request/response schemas changed
- ✅ Query parameters added/removed
- ✅ Authentication requirements changed
- ✅ Error responses modified

**Include in API docs**:
- ✅ Endpoint path and HTTP method
- ✅ Request body schema (with examples)
- ✅ Response schema (with examples)
- ✅ Query parameters and headers
- ✅ Authentication requirements
- ✅ Error responses (400, 401, 403, 404, 500)
- ✅ Rate limits (if applicable)

### 3. Architecture Decision Records (ADRs)

**What are ADRs**: Documents that capture important architectural decisions and their rationale.

**When to create an ADR**:
- ✅ Choosing between architectural patterns (monolith vs microservices, REST vs GraphQL)
- ✅ Major technology decisions (database, framework, library)
- ✅ Security architecture decisions (authentication method, encryption approach)
- ✅ Breaking changes to existing architecture
- ✅ Trade-offs with significant impact

**ADR template** (`docs/adr/NNNN-title.md`):
```markdown
# ADR-0001: Use PostgreSQL for Primary Database

**Status**: Accepted

**Date**: 2026-01-25

**Deciders**: Engineering team, Product lead

## Context

We need to choose a primary database for our application. Requirements:
- ACID compliance for financial transactions
- Complex queries with joins
- Horizontal scalability for future growth
- Strong community support

## Decision

We will use **PostgreSQL 15** as our primary database.

## Rationale

**Why PostgreSQL**:
- ✅ Full ACID compliance (critical for financial data)
- ✅ Excellent support for complex queries and joins
- ✅ JSON support for flexible schema (JSONB)
- ✅ Strong ecosystem (extensions, tools, hosting)
- ✅ Proven scalability (read replicas, partitioning)
- ✅ Team has PostgreSQL experience

**Alternatives considered**:
- **MySQL**: Less robust JSON support, InnoDB limitations
- **MongoDB**: NoSQL, lacks ACID guarantees for multi-document transactions
- **DynamoDB**: Vendor lock-in, limited query flexibility

## Consequences

**Positive**:
- Strong data integrity guarantees
- Flexible schema with JSONB
- Excellent performance for complex queries
- Easy to find PostgreSQL expertise

**Negative**:
- Slightly more complex setup than MySQL
- Horizontal scaling requires read replicas and partitioning strategy
- Must manage connection pooling carefully

**Mitigations**:
- Use managed PostgreSQL service (RDS, Cloud SQL) to simplify operations
- Implement connection pooling (pgBouncer) from day one
- Plan partitioning strategy for high-volume tables

## Implementation Notes

- Use PostgreSQL 15+ for performance improvements
- Store in `DATABASE_URL` environment variable
- Use Alembic/Flyway for migrations
- Enable WAL archiving for point-in-time recovery
```

**ADR numbering**: Use sequential numbers (0001, 0002, 0003)

**ADR statuses**:
- **Proposed**: Under discussion
- **Accepted**: Decision made, implementation in progress
- **Superseded**: Replaced by a newer ADR (link to replacement)
- **Deprecated**: No longer recommended, but still in use
- **Rejected**: Considered but not chosen

**Where to store ADRs**: `docs/adr/` or `docs/architecture/decisions/`

### 4. Inline Code Documentation

**When to add inline comments**:
- ✅ Complex algorithms or logic that isn't self-evident
- ✅ Non-obvious business rules
- ✅ Workarounds for known issues
- ✅ Performance optimisations with unusual code patterns
- ✅ Security-sensitive code (explain why it's done this way)

**When NOT to add comments**:
- ❌ Obvious code that's self-documenting
- ❌ Restating what the code does (use better naming instead)
- ❌ Historical information (use git history)
- ❌ Commented-out code (delete it, use git history)

**Good inline documentation**:

```python
# ❌ Bad - Restates the obvious
# Get user from database
user = db.get_user(user_id)

# ✅ Good - Explains non-obvious business rule
# Users are soft-deleted, so we must filter by active=True
# to avoid showing deleted accounts in search results
active_users = db.query(User).filter_by(active=True).all()

# ✅ Good - Explains performance trade-off
# Use in-memory cache for user permissions to avoid N+1 queries.
# Cache is invalidated on permission changes via Redis pub/sub.
cached_permissions = permission_cache.get(user_id)
```

**Function/method documentation**:

**Python (docstrings)**:
```python
def calculate_discount(price: Decimal, user_tier: str) -> Decimal:
    """
    Calculate discount based on user tier and purchase price.

    Business rule: Premium users get 15% discount on orders >£100,
    standard users get 5% on all orders.

    Args:
        price: Pre-discount price in GBP
        user_tier: User tier ("premium" or "standard")

    Returns:
        Discount amount in GBP (always positive)

    Raises:
        ValueError: If price is negative or user_tier is invalid

    Example:
        >>> calculate_discount(Decimal("150.00"), "premium")
        Decimal("22.50")
    """
    if price < 0:
        raise ValueError("Price cannot be negative")

    if user_tier not in ("premium", "standard"):
        raise ValueError(f"Invalid tier: {user_tier}")

    if user_tier == "premium" and price > 100:
        return price * Decimal("0.15")

    return price * Decimal("0.05")
```

**TypeScript (JSDoc)**:
```typescript
/**
 * Calculate discount based on user tier and purchase price.
 *
 * Business rule: Premium users get 15% discount on orders >£100,
 * standard users get 5% on all orders.
 *
 * @param price - Pre-discount price in GBP
 * @param userTier - User tier ("premium" or "standard")
 * @returns Discount amount in GBP (always positive)
 * @throws {Error} If price is negative or userTier is invalid
 *
 * @example
 * ```ts
 * calculateDiscount(150.00, "premium") // Returns 22.50
 * ```
 */
function calculateDiscount(price: number, userTier: string): number {
  if (price < 0) {
    throw new Error("Price cannot be negative");
  }

  if (!["premium", "standard"].includes(userTier)) {
    throw new Error(`Invalid tier: ${userTier}`);
  }

  if (userTier === "premium" && price > 100) {
    return price * 0.15;
  }

  return price * 0.05;
}
```

**What to document in functions**:
- ✅ Purpose (what it does, why it exists)
- ✅ Parameters (type, meaning, constraints)
- ✅ Return value (type, meaning)
- ✅ Exceptions/errors raised
- ✅ Side effects (database writes, external API calls)
- ✅ Examples (for complex functions)

### 5. CHANGELOG Maintenance

**When to update CHANGELOG**:
- ✅ New features added
- ✅ Bug fixes
- ✅ Breaking changes
- ✅ Deprecations
- ✅ Security fixes

**CHANGELOG format** (Keep a Changelog):
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- User authentication with JWT tokens
- Password reset via email

### Changed
- Improved search performance with PostgreSQL full-text search

### Fixed
- Fixed duplicate results in search API

## [1.2.0] - 2026-01-20

### Added
- New `/api/users` endpoint for user management
- Support for user profile images

### Changed
- **BREAKING**: Authentication now requires `Authorization: Bearer <token>` header
  (previously used `X-API-Key`)

### Deprecated
- `GET /api/v1/search` - Use `POST /api/v2/search` instead

### Removed
- Removed legacy XML API endpoints

### Fixed
- Fixed race condition in session management

### Security
- Updated dependencies to address CVE-2026-12345
```

### 6. Documentation in Design Proposals

**Include in design proposal** (Phase 2: Analysis):

```markdown
## Documentation Updates

**README changes**:
- Add new environment variable `AUTH0_DOMAIN` to Configuration section
- Update Prerequisites to include Redis 7+

**API documentation**:
- New endpoints: `POST /auth/login`, `POST /auth/logout`, `POST /auth/refresh`
- Update OpenAPI spec with authentication bearer token requirement

**Architecture Decision Record**:
- Create ADR-0005: Use Auth0 for authentication
  - Rationale: Managed service, MFA support, social logins
  - Trade-offs: Monthly cost, vendor lock-in

**Inline documentation**:
- Add function docstrings to `auth_service.py`
- Document JWT token structure and expiry logic
```

### 7. Documentation Review Checklist (PR Review)

**Reviewer should verify**:
- [ ] README updated if setup/config changed
- [ ] API docs regenerated if endpoints changed
- [ ] ADR created for significant architectural decisions
- [ ] Function/class docstrings added for new code
- [ ] CHANGELOG updated with user-facing changes
- [ ] .env.example updated with new environment variables
- [ ] Comments explain "why", not "what"
- [ ] No commented-out code committed

## Australian English in Documentation

All documentation uses **Australian English spelling**:
- ✅ normalise, organisation, authorisation, optimise, colour, behaviour
- ❌ normalize, organization, authorization, optimize, color, behavior

This applies to:
- README files
- API documentation
- ADRs
- Code comments
- CHANGELOG
- All written communication

## References

Detailed guides in `references/` folder:
- `story-analysis.md` - **Complete 9-step analysis workflow** with POC scripts, design proposals, examples
- `authentication-patterns.md` - **Zero-secrets architecture** for AWS, Azure, and GitHub Actions authentication

## Future Best Practices

Additional guidance planned for:
- Data modeling and schema design
- API design patterns
- Testing strategy planning
- Migration planning
- Rollback strategies
- Feature flag implementation
- Observability planning (logging, metrics, tracing)
