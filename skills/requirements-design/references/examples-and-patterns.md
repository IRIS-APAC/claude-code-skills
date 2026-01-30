# Examples and Patterns - Requirements & Design

This appendix contains detailed examples and patterns referenced in the main SKILL.md file.

## Table of Contents
1. [Challenge, Research, Suggest Examples](#challenge-research-suggest-examples)
2. [Code Patterns for Abstraction](#code-patterns-for-abstraction)
3. [Feature Addition Workflows](#feature-addition-workflows)
4. [Handling Conflicts Examples](#handling-conflicts-examples)
5. [Cost Estimation Examples](#cost-estimation-examples)

---

## Challenge, Research, Suggest Examples

### Example 1: Challenging Technology Choices

**Scenario**: User says "We need Redis for caching"

**❌ Passive approach**:
```
You: "OK, I'll document Redis caching requirements..."
```

**✅ Active approach**:
```
You: "Let me understand the caching requirements first:
   - What data needs caching? (API responses, database queries, session data?)
   - What's the access pattern? (read-heavy, write-heavy, TTL needs?)
   - What's your scale? (cache size, request volume?)

   Let me research caching options...
   [WebSearch: "redis vs in-memory cache vs cdn 2026"]

   Based on research, here are three options:

   1. In-Memory Cache (functools.lru_cache)
      - Cost: $0 (built-in)
      - Latency: <1ms
      - Complexity: Low
      - Best for: Single-server, small cache (<100MB)

   2. Redis
      - Cost: ~$30/month (ElastiCache)
      - Latency: 1-5ms
      - Complexity: Medium (deployment, monitoring)
      - Best for: Multi-server, large cache, persistence needed

   3. CDN (CloudFront)
      - Cost: ~$10/month
      - Latency: <50ms globally
      - Complexity: Low (managed service)
      - Best for: Static/semi-static content, geographic distribution

   Given your scale (1000 req/day, single server),
   I recommend in-memory caching first.
   What's your specific use case?"
```

### Example 2: Challenging Vague Requirements

**Scenario**: User says "Build a dashboard"

**❌ Passive approach**:
```
You: "OK, I'll document a dashboard..."
```

**✅ Active approach**:
```
You: "Let me understand what problem the dashboard solves:

   - Who will use it? (executives, analysts, operations team?)
   - What decisions will they make with it?
   - What data do they need to see?
   - How often will they check it? (real-time, daily, weekly?)
   - What actions can they take? (view-only, or interactive controls?)

   Can you walk me through a specific scenario where someone uses this dashboard?

   Also, let me research dashboard patterns...
   [WebSearch: "dashboard design best practices 2026"]

   Based on research, dashboards typically fall into:
   1. Operational (real-time monitoring, alerts)
   2. Analytical (trends, comparisons, drill-down)
   3. Strategic (high-level KPIs, summaries)

   Which type matches your needs?"
```

### Example 3: Suggesting Simpler Alternatives

**Scenario**: User says "We need a Kubernetes cluster with service mesh"

```
You: "Let me understand your requirements:
   - What's your team size and DevOps experience?
   - What's your deployment frequency?
   - What's your scale? (number of services, traffic volume?)

   [WebSearch: "kubernetes vs simpler alternatives 2026"]

   Based on research, Kubernetes + service mesh has significant operational overhead:
   - Requires dedicated DevOps engineer
   - 3-6 months learning curve
   - Complex debugging and troubleshooting
   - Typically justified for 10+ services and frequent deployments

   Here are alternatives based on complexity:

   | Approach | Complexity | Team Needed | Best For |
   |----------|-----------|-------------|----------|
   | Docker Compose | Low | Any dev | 1-5 services, infrequent deploys |
   | ECS Fargate | Medium | 1 DevOps | 5-20 services, AWS-native |
   | Kubernetes | High | Dedicated ops | 20+ services, multi-cloud |

   Your current situation: 3 services, 2 developers

   I recommend: ECS Fargate because:
   - Managed containers (no cluster management)
   - AWS-native (you're already on AWS)
   - Simple deployment (no service mesh complexity)
   - Can scale up to Kubernetes later if needed

   If you still need Kubernetes, let's discuss specific requirements..."
```

### Example 4: Research Process

**Scenario**: User says "Implement OAuth 2.0 authentication"

**Internal research process**:
1. [WebSearch: "OAuth 2.0 best practices 2026"]
   → Learns about PKCE requirement, token storage security

2. [Grep: "oauth.*auth.*token" in codebase]
   → Finds existing auth implementation in another service

3. [Read: similar auth implementation]
   → Understands team's existing patterns

4. [WebSearch: "OAuth 2.0 libraries Python 2026"]
   → Compares authlib vs requests-oauthlib

**Output to user**:
```
"I researched OAuth 2.0 implementation approaches. Here's what I found:

1. Our codebase already has OAuth in user-service:
   - Uses authlib library
   - Implements PKCE flow
   - Token storage in Redis
   - Code: src/auth/oauth.py:45-120

2. Best practices for 2026:
   - PKCE required (not optional anymore)
   - Short-lived access tokens (15 min)
   - Refresh token rotation
   - Token introspection for APIs

3. Library comparison:
   - authlib: More features, actively maintained
   - requests-oauthlib: Simpler, but less complete

Recommendation: Follow existing pattern in user-service for consistency.
I'll document using authlib with PKCE flow, matching your current architecture."
```

### Example 5: Validate Feasibility

**Cost Reality Check**:
```
User: "Store everything in memory for speed"

You: "Let me calculate the cost:
   - Your data volume: 100GB
   - Redis pricing: ~$0.10/GB-hour
   - Monthly cost: 100GB × $0.10 × 730 hours = $7,300/month

   Compare to alternatives:
   - PostgreSQL with indexes: < $500/month, still <50ms queries
   - DynamoDB with DAX cache: ~$800/month for hot data only

   Recommendation: Cache hot data (top 10%), query cold data from database.
   This reduces cost from $7,300 to ~$800/month while maintaining performance."
```

**Timeline Reality Check**:
```
User: "Build a production-ready API in 2 weeks"

You: "Let me validate the timeline:
   - API development: 1 week
   - Testing & QA: 1 week
   - Security review: 3 days
   - Documentation: 2 days
   - Deployment setup: 2 days
   - Total: ~4 weeks minimum

   [WebSearch: "typical API development timeline"]
   Industry average for production API: 4-8 weeks with 2-3 developers

   Options:
   1. Reduce scope: MVP with core features only (achievable in 2 weeks)
   2. Extend timeline: Full features in 4 weeks
   3. Add resources: 2 more developers, achieve in 2-3 weeks

   Which approach fits your constraints?"
```

---

## Code Patterns for Abstraction

### Adapter Pattern (Recommended)

**Purpose**: Abstract vendor-specific implementations behind generic interfaces

```python
from abc import ABC, abstractmethod
from typing import List

# Abstract interface (what we need)
class SSOProvider(ABC):
    @abstractmethod
    def authenticate(self, token: str) -> User:
        """Authenticate user with SSO token"""
        pass

    @abstractmethod
    def get_user_groups(self, user_id: str) -> List[str]:
        """Get user's group memberships"""
        pass

    @abstractmethod
    def refresh_token(self, refresh_token: str) -> str:
        """Refresh access token"""
        pass

# Concrete implementation (Okta-specific)
class OktaSSOProvider(SSOProvider):
    def __init__(self, okta_domain: str, client_id: str):
        self.okta_domain = okta_domain
        self.client_id = client_id

    def authenticate(self, token: str) -> User:
        # Okta-specific implementation using Okta SDK
        okta_user = okta_sdk.verify_token(token)
        return User(id=okta_user.id, email=okta_user.email)

    def get_user_groups(self, user_id: str) -> List[str]:
        # Okta-specific group retrieval
        return okta_sdk.get_user_groups(user_id)

    def refresh_token(self, refresh_token: str) -> str:
        return okta_sdk.refresh_access_token(refresh_token)

# Concrete implementation (Azure AD)
class AzureADProvider(SSOProvider):
    def __init__(self, tenant_id: str, client_id: str):
        self.tenant_id = tenant_id
        self.client_id = client_id

    def authenticate(self, token: str) -> User:
        # Azure AD-specific implementation using MSAL
        azure_user = msal.verify_token(token)
        return User(id=azure_user.oid, email=azure_user.email)

    def get_user_groups(self, user_id: str) -> List[str]:
        # Azure AD-specific group retrieval
        return msal.get_user_groups(user_id)

    def refresh_token(self, refresh_token: str) -> str:
        return msal.acquire_token_by_refresh_token(refresh_token)

# Usage (generic, swappable)
def login_endpoint(request):
    # Get provider from config (dependency injection)
    sso_provider: SSOProvider = get_configured_provider()

    token = request.headers.get('Authorization')
    user = sso_provider.authenticate(token)

    return {"user": user, "groups": sso_provider.get_user_groups(user.id)}

# Easy to swap providers via configuration
def get_configured_provider() -> SSOProvider:
    provider_type = config.get('SSO_PROVIDER')  # 'okta' or 'azure'

    if provider_type == 'okta':
        return OktaSSOProvider(
            okta_domain=config.get('OKTA_DOMAIN'),
            client_id=config.get('OKTA_CLIENT_ID')
        )
    elif provider_type == 'azure':
        return AzureADProvider(
            tenant_id=config.get('AZURE_TENANT_ID'),
            client_id=config.get('AZURE_CLIENT_ID')
        )
    else:
        raise ValueError(f"Unknown SSO provider: {provider_type}")
```

### Configuration-Driven Pattern (Also Recommended)

**Purpose**: Use configuration instead of code changes to switch implementations

```yaml
# config/authentication.yml

# Abstract requirement
authentication:
  type: saml
  issuer_url: ${SSO_ISSUER_URL}        # Environment-specific
  entity_id: ${SSO_ENTITY_ID}
  certificate_url: ${SSO_CERT_URL}
  attribute_mapping:
    user_id: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"
    email: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
    groups: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/group"

# Okta configuration (.env.okta):
SSO_ISSUER_URL=https://company.okta.com/app/xxx/sso/saml
SSO_ENTITY_ID=http://www.okta.com/xxx
SSO_CERT_URL=https://company.okta.com/app/xxx/sso/saml/metadata

# Azure AD configuration (.env.azure):
SSO_ISSUER_URL=https://login.microsoftonline.com/tenant-id/saml2
SSO_ENTITY_ID=spn:app-id
SSO_CERT_URL=https://login.microsoftonline.com/tenant-id/federationmetadata/2007-06/federationmetadata.xml
```

**Benefits**:
- ✅ Switch providers with configuration change only (no code changes)
- ✅ Can test with mock provider in development
- ✅ Can support multiple providers simultaneously (Okta for internal, Azure AD for partners)
- ✅ Solution is reusable across different organizations/contexts

---

## Feature Addition Workflows

### Example 1: Feature Addition (Extend Existing Docs)

**Scenario**: Existing project has SharePoint indexing working. Now adding SharePoint as a new data source.

**Decision**: Extend existing docs (it's a natural evolution)

**Steps**:

1. **Update `requirements-ai-assistant.md`**:
   ```markdown
   **Status**: 🚧 In Progress  (changed from ✅ Complete)

   **Document Version**: 1.1  (incremented from 1.0)

   **Change History**:
   | Version | Date | Changes |
   |---------|------|---------|
   | 1.0 | 2025-01-15 | Initial Phase 1 requirements |
   | 1.1 | 2025-02-10 | Added Epic 3: SharePoint Integration |

   ## 3.4 Epic 3: SharePoint Integration (NEW)

   **Epic Goal**: Index SharePoint content to enable search across enterprise documents

   **Stories**:
   - Story 3.1: Authenticate with SharePoint Graph API
   - Story 3.2: Enumerate SharePoint sites and document libraries
   - Story 3.3: Extract document metadata and content
   - Story 3.4: Transform SharePoint data to common format
   - Story 3.5: Index SharePoint content in OpenSearch

   **Open Questions**:
   | Q7 | SharePoint API rate limits? | ⏳ PENDING | **Action**: Microsoft SA to confirm |
   ```

2. **Update `architecture-ai-assistant.md`**:
   ```markdown
   **Status**: 🚧 In Progress

   **Document Version**: 1.1

   ## 2.3 New Component: SharePoint Connector

   ```
   ┌────────────────────────────────────┐
   │  Existing: SharePoint Connector    │  ← Phase 1
   └────────────────────────────────────┘
                  │
                  ▼
   ┌────────────────────────────────────┐
   │  NEW: SharePoint Connector         │  ← Phase 1.1
   │  - Graph API authentication        │
   │  - Document enumeration            │
   │  - Metadata extraction             │
   │  - Follows same pattern as         │
   │    SharePoint connector            │
   └────────────────────────────────────┘
   ```

   **Design Note**: SharePoint connector reuses the same pipeline pattern
   as SharePoint connector (authenticate → enumerate → extract → transform → index).
   ```

3. **Update `constraints-ai-assistant.md`** (if new constraints):
   ```markdown
   **NEW Constraint**: Must use Microsoft Graph API
   - **Type**: Technical Standard
   - **Rationale**: Official Microsoft API for SharePoint
   - **Impact**: Cannot use legacy SharePoint REST API
   ```

4. **Keep `customer-value` and `solution-design` mostly unchanged** (unless value proposition changes)

### Example 2: New Phase (Create New Document Set)

**Scenario**: Phase 1 delivered SharePoint search. Phase 2 adds SharePoint + advanced features + major UI changes.

**Decision**: Create new phase documents (significant scope expansion)

**Steps**:

1. **Create Phase 2 document set**:
   - `constraints-ai-assistant-phase2.md`
   - `customer-value-ai-assistant-phase2.md`
   - `solution-design-ai-assistant-phase2.md`
   - `requirements-ai-assistant-phase2.md`
   - `architecture-ai-assistant-phase2.md`

2. **In each Phase 2 document, reference Phase 1**:
   ```markdown
   ## Phase 1 Context

   **Phase 1 Documents**: See [requirements-ai-assistant.md](requirements-ai-assistant.md)

   **Phase 1 Delivered**:
   - SharePoint indexing for 13+ collections
   - Hybrid search (BM25 + vector embeddings)
   - Basic RAG with Open WebUI
   - Student-focused MVP
   - ✅ Successfully deployed and in use

   **Phase 2 Scope** (Building on Phase 1):
   - NEW: SharePoint integration
   - NEW: Staff-facing features with RBAC
   - NEW: Advanced UI with faceted search
   - MODIFIED: Extend RAG for enterprise content
   - CARRIED FORWARD: OpenSearch infrastructure (worked well)
   ```

3. **Use "Open Questions" to capture Phase 1 learnings**:
   ```markdown
   ## Open Questions & Unknowns

   | Q1 | Keep OpenSearch from Phase 1 or switch to different vector DB? | ✅ RESOLVED | Keep OpenSearch - worked well, team familiar, scales to Phase 2 needs |
   | Q2 | Reuse authentication approach from Phase 1? | ✅ RESOLVED | Yes, JWT validation pattern proven in Phase 1 |
   | Q3 | Same deployment infrastructure? | ⏳ PENDING | **Action**: DevOps to assess if current ECS cluster can handle Phase 2 load |
   ```

---

## Handling Conflicts Examples

### Example: Authentication Approach Conflict

**Stakeholder Views**:
- **Security team**: "Must use enterprise SSO (Okta)"
- **Dev team**: "Okta integration adds 2 weeks to timeline"
- **Product**: "Must launch in 4 weeks (board commitment)"

**Document in Open Questions**:
```markdown
## Open Question: Authentication Approach

### Stakeholder Perspectives:
- **Security team**: Enterprise SSO required for compliance
- **Dev team**: Okta adds 2 weeks (new integration, testing, security review)
- **Product**: 4-week deadline is firm (board commitment)

### Options Analysis:
| Approach | Timeline | Security | Cost | Trade-offs |
|----------|----------|----------|------|------------|
| **Option 1: Okta SSO** | +2 weeks (6 weeks total) | Excellent | $0 | Delays launch, best security |
| **Option 2: Simple auth + Okta Phase 2** | On time (4 weeks) | Good | +$5K tech debt | Launch on time, add Okta later, acceptable risk for limited beta |
| **Option 3: API keys only** | On time (4 weeks) | Poor | $0 | Security risk, not acceptable |

### Recommendation: Option 2 (Simple Auth + Okta Phase 2)

**Rationale**:
- Meets 4-week launch deadline (board commitment honored)
- Provides reasonable security for MVP/limited beta
  - Email/password with MFA
  - Limited to 50 beta users (controlled access)
  - All traffic over HTTPS
  - Session management with secure cookies
- Clear path to enterprise SSO in Phase 2 (planned for Month 3)
- Risk is acceptable:
  - Beta users are internal staff (lower risk)
  - Data is not sensitive (public course content)
  - Can monitor for any security issues during beta

**Action Required**:
- Product Owner to confirm this approach with Security team
- Security team to define minimum acceptable auth for beta
- Document tech debt in Phase 2 requirements

**Decision Date**: Need decision by Feb 1 to stay on timeline
```

---

## Cost Estimation Examples

### Example 1: Infrastructure Cost Breakdown

```markdown
## Monthly Infrastructure Costs

### Compute
| Component | Configuration | Monthly Cost | Calculation |
|-----------|---------------|--------------|-------------|
| API Service (ECS) | 4 tasks, 0.5 vCPU, 1GB RAM | $45 | 4 × $0.04048/hr × 730hr |
| Worker Service (ECS) | 2 tasks, 1 vCPU, 2GB RAM | $60 | 2 × $0.08195/hr × 730hr |
| **Subtotal** | | **$105** | |

### Data Storage
| Component | Configuration | Monthly Cost | Calculation |
|-----------|---------------|--------------|-------------|
| RDS PostgreSQL | db.t3.medium, 100GB | $70 | $0.096/hr × 730hr |
| S3 Storage | 100GB Standard | $2.30 | 100GB × $0.023/GB |
| OpenSearch | t3.medium, 100GB EBS | $95 | $0.13/hr × 730hr |
| **Subtotal** | | **$167** | |

### Networking & Other
| Component | Configuration | Monthly Cost | Notes |
|-----------|---------------|--------------|-------|
| ALB | 1 load balancer | $16 | $0.0225/hr × 730hr |
| Data Transfer | 50GB/month | $4.50 | $0.09/GB |
| CloudWatch Logs | 10GB/month | $5 | $0.50/GB |
| **Subtotal** | | **$25.50** | |

### **Total Monthly Cost**: **$297.50**

### Cost Projections
- **At 10x scale** (100K users): ~$950/month (economies of scale)
- **At 100x scale** (1M users): ~$4,500/month (with reserved instances)

### Cost Optimization Opportunities
- Use reserved instances: Save 30% ($89/month savings)
- Use S3 Intelligent-Tiering: Save $0.80/month
- Optimize CloudWatch logs retention: Save $2/month
```

### Example 2: Build vs Buy Analysis

```markdown
## Cost Comparison: Build Custom vs Use SaaS

### Option A: Build Custom Search Service
**One-Time Development**:
- Architecture & design: 1 week × $10K = $10K
- Core search implementation: 4 weeks × $10K = $40K
- Testing & QA: 2 weeks × $10K = $20K
- Documentation: 1 week × $5K = $5K
- **Total Development**: **$75K**

**Monthly Recurring**:
- Infrastructure: $300/month
- Maintenance (10% of dev cost): $625/month
- **Monthly Total**: **$925/month**

**Year 1 Total**: $75K + ($925 × 12) = **$86,100**
**Year 2 Total**: $925 × 12 = **$11,100**

### Option B: Use Algolia (SaaS)
**One-Time Setup**:
- Integration: 1 week × $10K = $10K
- Testing: 0.5 weeks × $10K = $5K
- **Total Setup**: **$15K**

**Monthly Recurring**:
- Algolia subscription (10K searches/month): $500/month
- Minimal maintenance: $100/month
- **Monthly Total**: **$600/month**

**Year 1 Total**: $15K + ($600 × 12) = **$22,200**
**Year 2 Total**: $600 × 12 = **$7,200**

### Recommendation: Option B (Algolia SaaS)

**Financial**:
- Year 1 savings: $86,100 - $22,200 = **$63,900 saved**
- Year 2 savings: $11,100 - $7,200 = **$3,900 saved**
- Break-even: Never (SaaS is always cheaper at this scale)

**Non-Financial Benefits**:
- Faster time to market: 1.5 weeks vs 8 weeks
- No infrastructure management
- Auto-scaling built-in
- Better search relevance (Algolia's core competency)
- Regular feature updates included

**When to Reconsider**:
- If search volume exceeds 1M searches/month (custom becomes cheaper)
- If need highly specialized search algorithms
- If data residency requirements prevent SaaS
```

### Example 3: Development Cost Estimation

```markdown
## Epic Cost Estimation

| Epic | Stories | Complexity | Dev Time | Testing Time | Total | Risk Factor | Estimate Range |
|------|---------|-----------|----------|--------------|-------|-------------|----------------|
| Epic 1: Auth | 5 | Medium | 1.5 weeks | 0.5 weeks | 2 weeks | Low | 2-3 weeks |
| Epic 2: API | 12 | High | 2.5 weeks | 1 week | 3.5 weeks | Medium | 3-5 weeks |
| Epic 3: UI | 8 | Medium | 2 weeks | 0.5 weeks | 2.5 weeks | Low | 2-3 weeks |
| Epic 4: Integration | 6 | High | 2 weeks | 1 week | 3 weeks | High | 3-6 weeks |
| **Total** | **31** | | **8 weeks** | **3 weeks** | **11 weeks** | | **10-17 weeks** |

**Assumptions**:
- 1 senior developer full-time
- No major blockers or dependencies
- Standard 2-week sprints
- Buffer included for unknowns

**Cost Calculation**:
- Senior developer rate: $100/hr (fully loaded)
- Total hours: 11 weeks × 40 hrs = 440 hours
- **Total Development Cost**: 440 × $100 = **$44,000**

**Risk Contingency**:
- Low risk (20%): +$8,800 = $52,800
- High risk (50%): +$22,000 = $66,000

**Recommended Budget**: $50,000 - $65,000
```
