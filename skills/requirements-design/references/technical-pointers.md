# Technical Pointers Guide

This guide helps provide implementation guidance and references for development teams. When breaking down requirements into stories, include technical pointers to accelerate implementation and ensure consistency.

---

## Purpose of Technical Pointers

**For each story or epic, provide**:
1. **Specifications**: Links to relevant technical standards and protocols
2. **Implementation Patterns**: Design patterns and architectural approaches
3. **Code References**: Similar implementations in the codebase
4. **External Resources**: Documentation, tutorials, and examples
5. **Testing Strategies**: How to test this capability

**Benefits**:
- Reduces research time for developers
- Ensures consistency with existing patterns
- Prevents reinventing the wheel
- Improves code quality through proven approaches
- Accelerates onboarding for new team members

---

## 1. Specifications and Standards

### When to Provide Specs

- **Authentication/Authorization**: OAuth 2.0, OpenID Connect, SAML specs
- **API Design**: OpenAPI/Swagger, REST conventions, GraphQL specs
- **Data Formats**: JSON Schema, Protocol Buffers, Avro
- **Protocols**: HTTP/2, WebSockets, gRPC
- **Security**: OWASP guidelines, encryption standards
- **Accessibility**: WCAG guidelines
- **Compliance**: GDPR, HIPAA, PCI-DSS requirements

### Format for Specification References

**Specification**: [Name]
**Version**: [Version number]
**Link**: [Official specification URL]
**Relevant Sections**: [Specific sections to focus on]
**Summary**: [1-2 sentences on why this matters for this story]

### Example

**Story 1.2: Implement OAuth 2.0 Authentication**

**Technical Pointers - Specifications**:

1. **OAuth 2.0 Authorization Framework**
   - **Version**: RFC 6749
   - **Link**: https://datatracker.ietf.org/doc/html/rfc6749
   - **Relevant Sections**:
     - Section 4.1: Authorization Code Grant (our use case)
     - Section 10: Security Considerations
   - **Summary**: Defines the authorization code flow we'll use for server-side authentication

2. **OpenID Connect Core**
   - **Version**: 1.0
   - **Link**: https://openid.net/specs/openid-connect-core-1_0.html
   - **Relevant Sections**:
     - Section 3.1.2: ID Token
     - Section 5.1: Standard Claims
   - **Summary**: Extends OAuth 2.0 with identity layer; defines ID token structure

3. **JSON Web Token (JWT)**
   - **Version**: RFC 7519
   - **Link**: https://datatracker.ietf.org/doc/html/rfc7519
   - **Relevant Sections**:
     - Section 4: JWT Claims
     - Section 7: Validating a JWT
   - **Summary**: Format for ID tokens and access tokens; validation requirements

---

## 2. Implementation Patterns

### Common Patterns by Domain

#### Authentication & Authorization
- **Repository Pattern**: For user data access
- **Strategy Pattern**: For different auth providers (SAML, OAuth, API keys)
- **Middleware/Decorator Pattern**: For auth checks in request pipeline
- **Claims-Based Authorization**: For fine-grained permissions

#### API Design
- **Controller/Handler Pattern**: Separate routing from business logic
- **DTO (Data Transfer Objects)**: For request/response validation
- **Service Layer Pattern**: Business logic separate from API layer
- **Repository Pattern**: Data access abstraction

#### Data Processing
- **Pipeline Pattern**: Sequential processing steps
- **Batch Processing Pattern**: Process records in chunks
- **Event Sourcing**: For audit trails and replayability
- **CQRS**: Separate read and write models for performance

#### Integration
- **Adapter Pattern**: Wrap external APIs with consistent interface
- **Circuit Breaker**: Prevent cascading failures
- **Retry with Exponential Backoff**: Handle transient failures
- **Saga Pattern**: Distributed transactions

#### Async/Background Processing
- **Producer-Consumer Pattern**: Queue-based workload distribution
- **Worker Pool Pattern**: Fixed number of concurrent workers
- **Pub/Sub Pattern**: Event-driven architecture

### Format for Pattern References

**Pattern**: [Name]
**When to Use**: [Scenario where this pattern applies]
**Benefits**: [Why use this pattern]
**Considerations**: [Trade-offs or gotchas]
**Implementation Example**: [Link or code snippet]

### Example

**Story 2.3: Implement SharePoint API Client**

**Technical Pointers - Patterns**:

1. **Adapter Pattern**
   - **When to Use**: Wrapping external APIs to provide consistent interface
   - **Benefits**:
     - Isolates external API changes from our codebase
     - Allows mocking in tests
     - Provides opportunity to add cross-cutting concerns (logging, metrics)
   - **Considerations**: Adds layer of indirection; keep adapter thin
   - **Implementation Example**:
     ```python
     class SharePointClient:
         """Adapter for SharePoint API"""
         def search(self, query: str, collection: str) -> SearchResult:
             # Wrap external API call
             response = self._http_client.get(f"{self.base_url}/search", params={...})
             # Transform to our domain model
             return self._to_search_result(response.json())
     ```

2. **Circuit Breaker Pattern**
   - **When to Use**: Calling unreliable external services
   - **Benefits**:
     - Prevents cascading failures
     - Allows graceful degradation
     - Gives external service time to recover
   - **Considerations**: Needs tuning (failure threshold, timeout, recovery time)
   - **Implementation Example**: Use `circuitbreaker` library or implement using Redis
     ```python
     from circuitbreaker import circuit

     @circuit(failure_threshold=5, recovery_timeout=60)
     def call_search_service_api(url):
         response = requests.get(url, timeout=10)
         response.raise_for_status()
         return response.json()
     ```

3. **Retry with Exponential Backoff**
   - **When to Use**: Handling transient failures (rate limits, network blips)
   - **Benefits**:
     - Automatic recovery from temporary issues
     - Reduces load on failing service
   - **Considerations**: Set max retries and max delay to avoid infinite loops
   - **Implementation Example**:
     ```python
     from tenacity import retry, stop_after_attempt, wait_exponential

     @retry(
         stop=stop_after_attempt(3),
         wait=wait_exponential(multiplier=1, min=1, max=10)
     )
     def fetch_from_search_service(url):
         return requests.get(url, timeout=10)
     ```

---

## 3. Code References

### When to Provide Code References

- **Similar implementations**: "We already do X in module Y"
- **Reusable utilities**: "Use the retry decorator from shared/utils"
- **Patterns established**: "Follow the same structure as existing API handlers"
- **Examples to learn from**: "See how auth is done in service Z"

### How to Reference Code

**Use specific file paths and line numbers**:
- Format: `src/module/file.py:142-156`
- Provides clickable links in most IDEs and viewers

**Provide context**:
- Explain what to look for
- Highlight key patterns or techniques
- Note if code should be reused or just used as reference

### Format for Code References

**Reference**: [File path or module name]
**Purpose**: [What to learn from this code]
**Key Points**: [Specific techniques or patterns]
**Reusability**: [Can we import/reuse this, or is it just an example?]

### Example

**Story 1.2: Implement Embedding Generation Service**

**Technical Pointers - Code References**:

1. **AWS Bedrock Client Pattern**
   - **Reference**: `src/integrations/sharepoint/client.py:45-78`
   - **Purpose**: Example of AWS SDK client with SigV4 signing and retry logic
   - **Key Points**:
     - Uses boto3 session with explicit region
     - Implements exponential backoff for throttling
     - Logs request ID for traceability
   - **Reusability**: Extract `create_bedrock_client()` to `src/core/aws/bedrock.py` and reuse

2. **Batch Processing Pattern**
   - **Reference**: `src/pipelines/search_service/parser.py:120-145`
   - **Purpose**: Example of batching items for efficient processing
   - **Key Points**:
     - Collects items in chunks of 100
     - Processes batch via single API call
     - Distributes results back to original order
   - **Reusability**: Similar pattern, implement for embeddings

3. **Cache Implementation**
   - **Reference**: `src/core/cache/redis_cache.py`
   - **Purpose**: Reusable Redis caching module
   - **Key Points**:
     - Generic key-value cache with TTL
     - Handles connection pooling
     - Provides cache decorators for functions
   - **Reusability**: Import and use `@cached(ttl=300)` decorator

---

## 4. External Resources

### Types of Resources

**Official Documentation**:
- API docs from service providers
- Framework/library documentation
- Cloud provider guides

**Tutorials & Guides**:
- Step-by-step implementation guides
- Video tutorials
- Blog posts from trusted sources

**Example Repositories**:
- Official examples from libraries
- Well-maintained community projects
- Proof-of-concept implementations

**Community Resources**:
- Stack Overflow discussions (specific to our problem)
- GitHub issues (workarounds for known issues)
- Reddit/forum discussions (architectural decisions)

### Vetting Resources

**Prefer**:
- ✅ Official documentation
- ✅ Maintained libraries (recent commits, responsive issues)
- ✅ Tutorials from reputable sources (AWS blogs, framework authors)
- ✅ Stack Overflow answers with high votes and recent activity

**Avoid**:
- ❌ Outdated tutorials (check publish date, library versions)
- ❌ Unmaintained libraries (no commits in > 1 year)
- ❌ Copy-pasted code without understanding
- ❌ Security anti-patterns

### Format for External Resources

**Resource**: [Title]
**Type**: [Documentation | Tutorial | Example | Discussion]
**Link**: [URL]
**Relevance**: [How this helps with the story]
**Key Takeaways**: [Specific insights or techniques]
**Date/Version**: [When published or last updated]

### Example

**Story 3.2: Implement Hybrid Search with OpenSearch**

**Technical Pointers - External Resources**:

1. **OpenSearch Hybrid Search Documentation**
   - **Type**: Official Documentation
   - **Link**: https://opensearch.org/docs/latest/search-plugins/hybrid-search/
   - **Relevance**: Our primary implementation guide for hybrid search
   - **Key Takeaways**:
     - Hybrid query combines BM25 and kNN vector search
     - Requires search pipeline for score normalization
     - Can use RRF or custom normalization
   - **Version**: OpenSearch 2.11+ (we're using Serverless which is compatible)

2. **Tutorial: Building Semantic Search with OpenSearch**
   - **Type**: Tutorial (AWS Blog)
   - **Link**: https://aws.amazon.com/blogs/database/building-semantic-search-with-amazon-opensearch-serverless/
   - **Relevance**: AWS-specific guidance for Serverless (our deployment target)
   - **Key Takeaways**:
     - Serverless has different IAM requirements (data access policies)
     - Embedding models accessed via Bedrock connectors
     - Performance characteristics differ from managed clusters
   - **Date**: 2024-09-15 (recent)

3. **GitHub Example: Hybrid Search with Python Client**
   - **Type**: Example Repository
   - **Link**: https://github.com/opensearch-project/opensearch-py/blob/main/samples/hybrid_search.py
   - **Relevance**: Python implementation example (our language)
   - **Key Takeaways**:
     - Query structure for hybrid search
     - Score normalization configuration
     - Python client API usage patterns
   - **Date**: Last updated 2024-11 (maintained)

4. **Stack Overflow: Hybrid Search Filter Handling**
   - **Type**: Community Discussion
   - **Link**: https://stackoverflow.com/questions/78654321/opensearch-hybrid-filter-duplicates
   - **Relevance**: Known issue with applying filters to hybrid queries
   - **Key Takeaways**:
     - Filters must be applied to both BM25 and kNN subqueries separately
     - OpenSearch 3.0 introduced common filter support
     - Workaround for older versions shown in accepted answer
   - **Date**: 2024-10 (recent issue, active discussion)

---

## 5. Testing Strategy

### Test Types by Layer

**Unit Tests**:
- Test individual functions/classes in isolation
- Mock external dependencies
- Fast (milliseconds)
- High coverage (>80%)

**Integration Tests**:
- Test interactions between components
- Use test databases, mock external APIs
- Moderate speed (seconds)
- Cover critical paths

**End-to-End Tests**:
- Test complete user journeys
- Use real or realistic test environments
- Slow (minutes)
- Cover happy paths and key error scenarios

**Performance Tests**:
- Test under load
- Measure latency, throughput, resource usage
- Use production-like data volumes
- Run periodically, not every commit

**Security Tests**:
- Test authentication and authorization
- Scan for vulnerabilities (OWASP Top 10)
- Penetration testing (external)
- Run before releases

### Format for Testing Pointers

**Test Layer**: [Unit | Integration | E2E | Performance | Security]
**Test Cases**: [Key scenarios to cover]
**Tools**: [Testing frameworks and libraries]
**Mocking Strategy**: [How to mock dependencies]
**Test Data**: [Where to get or how to generate test data]

### Example

**Story 2.2: Implement HTML to Markdown Parser**

**Technical Pointers - Testing Strategy**:

**Unit Tests**:
- **Test Cases**:
  - Clean HTML → valid markdown
  - HTML with tables → markdown tables
  - HTML with lists → markdown lists
  - HTML with images → markdown image syntax
  - Malformed HTML → error handling
  - Empty input → empty output
- **Tools**: pytest, pytest-cov (coverage)
- **Mocking Strategy**: No external dependencies to mock (pure function)
- **Test Data**: Create fixture HTML files in `tests/fixtures/html/`

**Integration Tests**:
- **Test Cases**:
  - Parse real SharePoint HTML → verify structure preserved
  - Parse HTML from S3 → verify caching works
  - Parse large HTML (>1MB) → verify memory efficiency
- **Tools**: pytest, pytest-mock
- **Mocking Strategy**: Mock S3 client using moto library
- **Test Data**: Sample SharePoint pages (sanitized, no PII)

**Performance Tests**:
- **Test Cases**:
  - Parse 100 pages → measure total time (target: < 10s)
  - Parse single large page (1MB) → measure time (target: < 500ms)
  - Memory usage during batch parsing → verify no leaks
- **Tools**: pytest-benchmark, memory_profiler
- **Test Data**: Generate HTML pages of various sizes

**Edge Cases to Test**:
- HTML with JavaScript (should strip scripts)
- HTML with inline CSS (should remove styles)
- HTML with malicious content (XSS attempts)
- HTML with unicode characters (should preserve)
- HTML with nested structures (should handle depth)

---

## 6. Performance Considerations

### When Performance Matters

**Latency-Sensitive**:
- API endpoints (user-facing)
- Real-time processing
- Synchronous operations

**Throughput-Sensitive**:
- Batch processing
- Background jobs
- Data ingestion pipelines

**Resource-Sensitive**:
- Memory-intensive operations (large datasets)
- CPU-intensive operations (encryption, parsing)
- I/O-intensive operations (database queries, file operations)

### Performance Optimization Techniques

**Caching**:
- Where: Frequently accessed, infrequently changing data
- Tools: Redis, in-memory cache (functools.lru_cache)
- Invalidation: TTL-based, event-based

**Batching**:
- Where: API calls, database queries, message processing
- Approach: Collect items, process in bulk, distribute results
- Trade-off: Latency vs throughput

**Async/Concurrency**:
- Where: I/O-bound operations (network, disk)
- Tools: asyncio (Python), promises (JavaScript), goroutines (Go)
- Trade-off: Complexity vs performance

**Indexing**:
- Where: Database queries on frequently filtered/sorted columns
- Approach: B-tree index (equality, range), hash index (equality only)
- Trade-off: Read performance vs write performance

**Connection Pooling**:
- Where: Database connections, HTTP clients
- Approach: Reuse connections instead of creating new
- Tools: Database drivers (psycopg2), HTTP clients (requests.Session)

**Pagination**:
- Where: APIs returning large result sets
- Approach: Offset-based (simple) or cursor-based (efficient for large datasets)
- Trade-off: Simplicity vs performance at scale

### Format for Performance Pointers

**Performance Goal**: [Specific target - latency, throughput, resource usage]
**Bottlenecks**: [Known or expected bottlenecks]
**Optimization Approach**: [How to achieve the goal]
**Monitoring**: [How to measure performance]

### Example

**Story 3.3: Optimize Search API Latency**

**Technical Pointers - Performance**:

**Performance Goal**: P95 latency < 500ms for search API

**Bottlenecks**:
1. OpenSearch query time (200-300ms)
2. Embedding generation (50-100ms)
3. S3 content fetch (100-200ms if included)
4. Result serialization (10-20ms)

**Optimization Approaches**:

1. **Cache Query Embeddings**
   - Problem: Repeated queries generate same embeddings
   - Solution: Redis cache with key=sha256(query), TTL=5min
   - Expected savings: 50-100ms per cached query
   - Implementation: `@cached(ttl=300, key_func=lambda q: sha256(q))`

2. **Defer S3 Fetch**
   - Problem: Fetching full content adds 100-200ms
   - Solution: Return summaries only by default; separate endpoint for full content
   - Expected savings: 100-200ms for most queries
   - Implementation: `include_content` flag defaults to False

3. **Parallel Processing**
   - Problem: Embedding and OpenSearch query could run in parallel
   - Solution: Use asyncio to overlap embedding generation and query preparation
   - Expected savings: 20-30ms
   - Implementation: Convert to async functions

4. **OpenSearch Query Optimization**
   - Problem: Complex queries are slow
   - Solution: Simplify query structure, use filters instead of queries where possible
   - Expected savings: 50-100ms
   - Implementation: Profile queries, optimize based on slow query logs

**Monitoring**:
- CloudWatch metric: `SearchLatencyP95`
- Alerts: Alert if P95 > 500ms for 5 minutes
- Dashboard: Show P50, P95, P99 over time
- Tracing: X-Ray to identify specific bottlenecks per request

---

## 7. Security Considerations

### Security Checklist by Domain

**Authentication**:
- [ ] Use strong cryptographic algorithms (AES-256, RSA-2048+)
- [ ] Validate tokens properly (signature, expiry, audience)
- [ ] Use HTTPS only (no plain HTTP)
- [ ] Implement rate limiting
- [ ] Log authentication failures (for monitoring)

**Authorization**:
- [ ] Enforce server-side (never trust client)
- [ ] Default deny (explicit permissions required)
- [ ] Principle of least privilege
- [ ] Validate permissions on every request
- [ ] Log authorization failures

**Input Validation**:
- [ ] Validate all user input (API requests, file uploads)
- [ ] Use allowlists (not denylists) where possible
- [ ] Sanitize before processing
- [ ] Protect against injection (SQL, NoSQL, command)
- [ ] Limit input size (prevent DoS)

**Data Protection**:
- [ ] Encrypt sensitive data at rest
- [ ] Encrypt data in transit (TLS 1.3)
- [ ] Don't log sensitive data (passwords, tokens, PII)
- [ ] Use secure random for secrets (not pseudo-random)
- [ ] Rotate secrets regularly

**Dependencies**:
- [ ] Keep dependencies updated
- [ ] Scan for known vulnerabilities
- [ ] Review licenses for compliance
- [ ] Pin versions (reproducible builds)

### Format for Security Pointers

**Security Concerns**: [What could go wrong?]
**Mitigations**: [How to prevent these issues]
**Testing**: [How to verify security]
**References**: [OWASP guidelines, CVEs, etc.]

### Example

**Story 1.3: Implement User Search API with Filtering**

**Technical Pointers - Security**:

**Security Concerns**:
1. **SQL Injection**: User-supplied filters could inject SQL
2. **Authorization Bypass**: Users could access data they shouldn't
3. **Information Disclosure**: Error messages could leak sensitive data
4. **DoS**: Large result sets could overwhelm system

**Mitigations**:

1. **Prevent SQL Injection**
   - Use parameterized queries (never string concatenation)
   - Use ORM with proper escaping (SQLAlchemy, TypeORM)
   - Validate filter fields against allowlist
   - Example:
     ```python
     # BAD: SQL injection risk
     query = f"SELECT * FROM docs WHERE title LIKE '%{user_input}%'"

     # GOOD: Parameterized query
     query = "SELECT * FROM docs WHERE title LIKE %s"
     cursor.execute(query, (f"%{user_input}%",))
     ```

2. **Enforce Authorization**
   - Check user permissions before every query
   - Add user ID filter to all queries
   - Don't trust client-supplied filters (enforce server-side)
   - Example:
     ```python
     # Enforce user context
     filters = {
         'user_id': current_user.id,  # Always filter by current user
         **request.filters  # Add requested filters
     }
     ```

3. **Prevent Information Disclosure**
   - Return generic error messages to users
   - Log detailed errors server-side only
   - Don't expose database structure in errors
   - Example:
     ```python
     try:
         result = db.query(...)
     except DatabaseError as e:
         logger.error(f"Query failed: {e}")  # Log details
         raise HTTPException(500, "Search failed")  # Generic to user
     ```

4. **Prevent DoS**
   - Limit result size (max 100 per request)
   - Implement pagination (don't allow fetching all)
   - Rate limit requests (per user/IP)
   - Timeout long-running queries
   - Example:
     ```python
     MAX_PAGE_SIZE = 100
     page_size = min(request.page_size, MAX_PAGE_SIZE)
     ```

**Testing**:
- Security unit tests: Test with malicious input (SQL injection strings)
- Penetration testing: OWASP ZAP or Burp Suite
- Code review: Security-focused review checklist
- Dependency scanning: `safety check` for known vulnerabilities

**References**:
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- OWASP SQL Injection: https://owasp.org/www-community/attacks/SQL_Injection
- CWE-89 (SQL Injection): https://cwe.mitre.org/data/definitions/89.html

---

## 8. Putting It All Together

### Technical Pointers Template for a Story

```markdown
## Story [ID]: [Title]

[Story description and acceptance criteria...]

---

### Technical Pointers

#### Specifications
1. [Spec name] - [Link] - [Relevance]
2. [...]

#### Implementation Patterns
1. [Pattern name] - [When to use] - [Implementation example]
2. [...]

#### Code References
1. [File path] - [What to learn] - [Reusability]
2. [...]

#### External Resources
1. [Resource] - [Link] - [Key takeaways]
2. [...]

#### Testing Strategy
- **Unit Tests**: [Test cases]
- **Integration Tests**: [Test cases]
- **Performance Tests**: [Targets]
- **Security Tests**: [Concerns to test]

#### Performance Considerations
- **Goal**: [Target]
- **Approach**: [Optimization strategy]
- **Monitoring**: [Metrics to track]

#### Security Considerations
- **Concerns**: [What could go wrong]
- **Mitigations**: [How to prevent]
- **Testing**: [How to verify]
```

---

## Best Practices

### 1. Be Specific
- Link to exact documentation pages (not just homepage)
- Reference specific code lines (not just files)
- Provide concrete examples (not just abstract descriptions)

### 2. Stay Current
- Check publication dates on tutorials
- Verify library versions match your project
- Update references when specifications change

### 3. Prioritize Quality
- Official docs > blog posts
- Maintained libraries > abandoned projects
- High-voted Stack Overflow > one-off answers

### 4. Balance Detail
- Too much: Overwhelming, hard to maintain
- Too little: Not actionable, still requires research
- Just right: Enough to get started, links for deeper learning

### 5. Maintain Over Time
- Update technical pointers when implementations change
- Add new references as team learns
- Remove outdated references

---

## Summary

Effective technical pointers:
1. **Save time** by providing curated references
2. **Improve quality** through proven patterns and standards
3. **Ensure consistency** across the codebase
4. **Accelerate learning** for new team members
5. **Reduce risk** through security and performance guidance

The goal is to equip developers with everything they need to implement stories confidently and correctly.
