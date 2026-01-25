# Story Analysis Workflow

This document describes the workflow for analysing stories before implementation begins.

## Overview

**CRITICAL**: Before writing any code, perform a thorough analysis of the story requirements.

**Benefits**:
- Clarifies ambiguous requirements
- Identifies missing information early
- Proposes design for user approval
- Prevents rework from misunderstanding requirements
- Ensures alignment with existing architecture

## Workflow

### 1. Read Story Requirements Thoroughly

**Read the entire story**, including:
- Title and description
- Acceptance criteria (all of them)
- Any linked epics or parent stories
- Any linked documentation or technical references
- All comments on the ticket

**Look for**:
- Technical pointers (documentation links, reference implementations)
- Architecture diagrams or design docs
- Related stories or prior work
- Dependencies on other stories

### 2. Check for Technical References

**Search for technical pointers** mentioned in the story:
- **Documentation links**: Follow and read any linked docs
- **Reference implementations**: Review existing code that does similar things
- **Architecture docs**: Check if there's existing architecture documentation
- **Design patterns**: Look for established patterns in the codebase

**Example pointers to look for**:
- "See `docs/architecture/auth-flow.md` for the authentication pattern"
- "Follow the same approach as the existing search service"
- "Implement according to the API specification in Appendix D"
- "Use the pattern from Story 1.3"

### 3. Analyse Existing Architecture

**If architecture documentation exists**, reconcile the story against it:

**Check**:
- Does the story align with existing architecture patterns?
- Are there conflicts with documented design decisions?
- Should the architecture be updated to accommodate this story?

**Common architecture docs to check**:
- `/docs/architecture/` folder
- `/docs/design/` folder
- `ARCHITECTURE.md` in the repo root
- Design documents in the story's epic
- ADRs (Architecture Decision Records) if the project uses them

**If conflicts exist**:
- Raise them with the user BEFORE implementing
- Propose either: (a) adjust the story, or (b) update the architecture

### 4. Identify Ambiguities

**Review each acceptance criterion** and identify anything ambiguous:

**Common ambiguities**:
- **Undefined behaviour**: "Display error message" - what message? Where? How?
- **Missing constraints**: "Validate email" - what counts as valid?
- **Unclear scope**: "Improve performance" - by how much? Which operations?
- **Vague acceptance**: "User-friendly interface" - what makes it user-friendly?

**Example**:
```markdown
## Acceptance Criteria
- [ ] User can log in with email/password

**Ambiguities**:
- What happens if the password is wrong?
- How many attempts before lockout?
- Should we support "forgot password" flow?
- Do we validate email format?
- Session expiry duration?
```

### 5. Clarify with User

**Ask questions** for anything ambiguous or unclear:

**Use AskUserQuestion** to clarify:
- Multiple valid approaches (which to use?)
- Missing requirements (what should happen when...?)
- Conflicting requirements (AC 1 says X, but AC 3 implies Y?)
- Scope questions (is X in scope for this story?)

**Example**:
```
Questions on Story 1.4 - User Login:

1. Password validation: Should we enforce password complexity? (min length, special chars, etc.)
2. Failed login attempts: How many failed attempts before account lockout?
3. Session expiry: How long should sessions last? (24 hours, 7 days, 30 days?)
4. Email validation: Should we verify email exists (send verification email) or just validate format?
```

### 6. Create Proof-of-Concept Scripts (for Third-Party Integrations)

**CRITICAL**: For stories involving third-party system integration, create proof-of-concept scripts BEFORE full implementation.

**When to create POC scripts**:
- Integrating with external APIs (Entra, AWS services, third-party SaaS)
- Using new libraries or frameworks
- Uncertain about how a third-party service works
- Complex authentication flows
- Data transformation from external sources

**Benefits**:
- De-risks integration work
- Validates assumptions about third-party APIs
- Creates working reference for full implementation
- Documents working code patterns
- Faster to iterate on simple script than full implementation

**POC script process**:

**1. Create simple standalone script**:
```python
# scripts/poc_entra_jwt_validation.py
"""
Proof of concept: JWT validation with Entra OIDC

Tests:
- Fetching JWKS keys from Entra
- Validating a JWT token
- Extracting claims

Run: python scripts/poc_entra_jwt_validation.py
"""

import requests
import jwt
from jwt import PyJWKClient

# Configuration
TENANT_ID = "your-tenant-id"
CLIENT_ID = "your-client-id"
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"

# Test token (get from Azure portal or real login)
TEST_TOKEN = "eyJ..."

def fetch_jwks_keys():
    """Fetch JWKS keys from Entra"""
    response = requests.get(JWKS_URL)
    print(f"JWKS fetch status: {response.status_code}")
    return response.json()

def validate_token(token):
    """Validate JWT token using JWKS"""
    jwks_client = PyJWKClient(JWKS_URL)

    # Get signing key
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    # Decode and validate
    decoded = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
    )

    print(f"Token valid! User: {decoded.get('email')}")
    print(f"Claims: {decoded}")
    return decoded

if __name__ == "__main__":
    print("Testing Entra JWT validation...")

    # Test 1: Fetch JWKS keys
    keys = fetch_jwks_keys()
    print(f"Found {len(keys['keys'])} signing keys")

    # Test 2: Validate token
    try:
        claims = validate_token(TEST_TOKEN)
        print("✅ Token validation successful")
    except Exception as e:
        print(f"❌ Token validation failed: {e}")
```

**2. Store in `/scripts/poc/` directory**:
```bash
# Organize POC scripts
scripts/
  poc/
    entra_jwt_validation.py
    opensearch_hybrid_query.py
    s3_presigned_urls.py
    README.md  # Explains what each POC does
```

**3. Document findings in POC README**:
```markdown
# Proof of Concept Scripts

## entra_jwt_validation.py

**Purpose**: Test JWT validation with Entra OIDC

**Findings**:
- JWKS keys cached by pyjwt library automatically
- Token validation requires exact audience and issuer match
- Claims available: email, name, oid, tid
- Performance: JWKS fetch ~200ms, validation <5ms

**Key learnings**:
- Must use RS256 algorithm (not HS256)
- Audience must match client ID exactly
- Issuer includes /v2.0 suffix

**Dependencies**:
- pyjwt[crypto]
- requests

**Next steps**: Integrate into FastAPI middleware
```

**4. Use POC as reference during implementation**:
- Copy working patterns from POC
- Reference POC findings in design proposal
- Link POC script in story Technical Notes
- Keep POC script for future reference

**Example workflow**:

**Story**: Implement JWT validation with Entra OIDC

**Step 1**: Create POC script (30 minutes)
- Tests token validation
- Documents what works
- Identifies issues early

**Step 2**: Document findings
- Working code patterns identified
- Dependencies confirmed
- Performance baseline established

**Step 3**: Design full implementation
- Reference POC findings in design
- Copy working patterns
- Add error handling, logging, tests

**Step 4**: Implement with confidence
- POC proves integration works
- Reference implementation available
- No guesswork needed

**Where to store POCs**:
- ✅ `/scripts/poc/` - Proof of concept scripts
- ✅ `/scripts/poc/README.md` - Documentation of findings
- ✅ Keep POCs in repo for future reference
- ❌ Don't delete POCs after implementation (they're documentation)

**POC vs Full Implementation**:

**POC Script**:
- Quick and dirty
- No error handling
- No tests
- Hardcoded values OK
- Purpose: Prove it works

**Full Implementation**:
- Production quality
- Comprehensive error handling
- Unit + integration tests
- Configurable values
- Purpose: Ship to production

### 7. Propose Design Approach

**BEFORE implementing**, propose a design approach for user approval (reference POC findings if created):

**Design proposal should include**:
- High-level approach (what you'll build)
- Key technical decisions (libraries, patterns, approaches)
- **POC findings** (if POC script was created)
- Component breakdown (what modules/files will be created/modified)
- Integration points (how it connects to existing code)
- Trade-offs (why this approach over alternatives)
- Testing strategy (how you'll test it)

**Format** (with POC reference):
```markdown
## Design Proposal: User Login (Story 1.4)

### Approach
Implement JWT-based authentication using Entra OIDC.

### POC Findings
Created POC script (`scripts/poc/entra_jwt_validation.py`) that validates approach:
- ✅ Successfully validated JWT tokens from Entra
- ✅ JWKS key fetching works (200ms first fetch, cached thereafter)
- ✅ Token validation fast (<5ms after key fetch)
- ✅ Claims extraction confirmed (email, name, oid, tid available)
- **Key learning**: Must use RS256 algorithm and exact audience/issuer match
- **Performance baseline**: ~200ms cold start, <5ms warm

POC proves integration works. Full implementation will add error handling, logging, and tests.

### Key Decisions
- **Authentication method**: JWT tokens (industry standard, stateless, **proven in POC**)
- **Library**: `pyjwt[crypto]` (well-tested, widely used, **validated in POC**)
- **Key caching**: 1-hour TTL for JWKS keys (balances performance vs security, **POC shows 200ms fetch time**)
- **Claims validation**: Required claims only (iss, aud, exp, nbf) - **POC confirms available**

### Components
- `src/auth/jwt_validator.py` - New module for JWT validation
- `src/auth/middleware.py` - Update to add JWT middleware
- `src/api/routes.py` - Update to add login endpoint
- `tests/unit/test_jwt_validator.py` - Unit tests
- `tests/integration/test_auth_flow.py` - Integration tests

### Integration Points
- Integrates with existing `src/api/app.py` FastAPI application
- Uses existing `src/config.py` for configuration (Entra client ID, tenant ID)
- Follows existing error handling pattern from `src/api/errors.py`

### Trade-offs
- **JWT vs sessions**: JWT chosen for stateless auth (scales better, no server-side storage)
- **Key caching**: 1-hour TTL introduces potential 1-hour delay for key rotation, but Entra rotates keys monthly so acceptable
- **Claims validation**: Only validating required claims (optional claims deferred to Story 1.5 for scope)

### Testing Strategy
- Unit tests: JWT parsing, validation, error cases (invalid token, expired token, wrong issuer)
- Integration tests: Full auth flow (login, get token, use token, token expiry)
- Manual testing: Test with real Entra app
- Target coverage: 90%+

### Questions for Review
1. Is 1-hour key cache TTL acceptable, or should we use a shorter TTL?
2. Should we implement rate limiting on the login endpoint in this story, or defer to a separate story?
3. Do we want to log all login attempts (success and failure) for security monitoring?
```

**Post this as a comment on the story ticket** BEFORE implementing.

### 8. Get User Approval

**Wait for user approval** of the design before implementing:

**User may**:
- Approve as-is → proceed with implementation
- Request changes → update design, get re-approval
- Clarify requirements → update ACs on the ticket, update design

**Benefits of approval**:
- Ensures alignment before time is invested
- Catches architectural issues early
- Documents design decisions for future reference
- Prevents rework from misaligned implementation

### 9. Update Story Ticket

**After approval**, update the story ticket:

**Add a "Design" section** to the story description:
```markdown
## Design

**Approved**: [Date]

[Copy of approved design proposal]

**Changes from original**:
- [Any changes made during approval discussion]
```

This creates a permanent record of the approved design.

## Example Workflow

### Example Story

**Title**: Implement hybrid search combining keyword and vector search

**Description**:
Implement hybrid search that combines BM25 keyword search with vector semantic search using OpenSearch.

**Acceptance Criteria**:
- [ ] Search combines BM25 and vector results
- [ ] Results are ranked using RRF score normalisation
- [ ] Filters are applied consistently
- [ ] API follows standard contract

**References**:
- See Appendix D for API contract
- See Story 1.2 for existing search implementation

### Analysis Process

**1. Read thoroughly**: Read the story, ACs, references

**2. Check technical references**:
```bash
# Read referenced design docs
cat docs/Design/system-requirements.md

# Review previous related story implementation
git log --all --grep="Story 1.2" --oneline
git show <commit-hash>
```

**3. Analyse existing architecture**:
```bash
# Check for architecture docs
ls docs/architecture/
cat docs/architecture/search-design.md
```

Found: Architecture doc specifies filter allowlist pattern must be used.

**4. Identify ambiguities**:
- "RRF score normalisation" - what's the formula?
- "Filters applied consistently" - applied to both BM25 and vector, or only final results?
- "API follows standard contract" - which fields are required vs optional?

**5. Clarify with user**:
Post comment on ticket:
```
Questions:

1. RRF formula: Should we use standard RRF (1/(k+rank)) or weighted RRF? If weighted, what weights for BM25 vs vector?
2. Filter application: Apply filters to BM25 and vector separately, or to merged results?
3. API response: Story says "follow standard contract" but doesn't specify which fields. Should response include `score`, `rank`, or both?
```

User responds:
- RRF: Standard RRF with k=60
- Filters: Apply to BM25 and vector separately (better performance)
- API: Include both `score` and `rank` fields

**6. Propose design**:
Post design proposal as comment (see format above)

**7. Get approval**:
User approves with one change: Use k=100 instead of k=60 (recent research suggests better results)

**8. Update ticket**:
Add "Design" section to story description with approved design.

**9. Begin implementation**:
Move ticket to "In Progress" and start coding.

## Common Mistakes

### ❌ Wrong: Start coding immediately

**Problem**: Jump straight into implementation without analysis

**Why wrong**: Likely to misunderstand requirements, miss edge cases, not align with architecture

**Correct**: Always analyse first, propose design, get approval

### ❌ Wrong: Ignore existing architecture

**Problem**: Implement in a way that conflicts with documented patterns

**Why wrong**: Creates inconsistency, technical debt, may require rework

**Correct**: Check architecture docs, reconcile approach, raise conflicts early

### ❌ Wrong: Assume ambiguous requirements

**Problem**: Make assumptions about unclear requirements without asking

**Why wrong**: Often guess wrong, have to redo work

**Correct**: Identify ambiguities, ask user to clarify before implementing

### ❌ Wrong: Propose design in vacuum

**Problem**: Design without considering existing codebase

**Why wrong**: May not integrate well, duplicate existing functionality, miss reusable patterns

**Correct**: Review existing code, follow established patterns, integrate cleanly

### ❌ Wrong: Skip design approval

**Problem**: Implement without getting user sign-off on approach

**Why wrong**: User may disagree with approach, require rework

**Correct**: Always get design approval before implementing

## Tools and Techniques

### Finding Reference Implementations

**Search git history**:
```bash
# Find commits related to similar work
git log --all --grep="search" --oneline

# View specific commit
git show <commit-hash>

# Find when a file was changed
git log --all --oneline -- src/search/service.py
```

**Search codebase**:
```bash
# Find similar functions
grep -r "def.*search" src/

# Find imports of a library
grep -r "from opensearch" src/
```

### Checking Architecture Documentation

**Common locations**:
```bash
# Architecture folder
ls docs/architecture/

# Design folder
ls docs/design/

# Root documentation
cat ARCHITECTURE.md

# ADRs (Architecture Decision Records)
ls docs/adr/
```

### Reconciling with Architecture

**Questions to ask**:
- Does this follow the documented patterns?
- Should I update the architecture to accommodate this?
- Is there a conflict that needs resolution?
- Are there cross-cutting concerns (logging, error handling, auth) that need to be followed?

## Related Documentation

- [story-templates.md](story-templates.md) - Template for writing stories
- [estimation-guide.md](estimation-guide.md) - Estimating story complexity
- [epic-planning.md](epic-planning.md) - Planning epics and interfaces

## Summary

**Before implementing ANY story**:
1. ✅ Read thoroughly (story, ACs, comments, references)
2. ✅ Check technical pointers (docs, reference implementations)
3. ✅ Analyse existing architecture (reconcile approach)
4. ✅ Identify ambiguities (unclear requirements)
5. ✅ Clarify with user (ask questions)
6. ✅ **Create POC script** (for third-party integrations - prove it works first!)
7. ✅ Propose design approach (get approval, reference POC findings)
8. ✅ Update story ticket (add "Design" section)
9. ✅ Begin implementation (move to "In Progress", use POC as reference)

**Result**: Clear understanding of requirements, validated integration (POC), approved design, alignment with architecture, reduced rework.

**POC Benefits**: De-risks integration, creates working reference, documents patterns, validates assumptions, faster iteration.
