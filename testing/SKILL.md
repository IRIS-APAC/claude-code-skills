---
name: testing
description: "Testing strategy, coverage analysis, and quality assurance. Use when: (1) Planning test strategy for a story, (2) Analyzing test coverage, (3) Reviewing test quality in PRs, (4) Creating mocks for integrations, (5) Defining testing standards. Referenced by developer-analysis (test strategy in design) and git-workflow (PR review test verification)."
model: sonnet
---
# Testing Strategy and Quality Assurance

Comprehensive testing guidance for ensuring code quality, coverage, and reliability.

## Overview

This skill provides testing **strategy and quality assurance guidance** that is **referenced by other skills**:

- **developer-analysis** - References this when planning testing strategy in design proposals
- **git-workflow** - References this when reviewing test quality in PRs
- **project-management** - References this when defining testing requirements in stories

**What this skill covers**:

- Test strategy planning (what to test, how much, when)
- Coverage analysis and targets
- Mock/stub/fake creation patterns
- Test organisation and structure
- Testing external integrations
- Performance and security testing
- Language-specific patterns

**What this skill does NOT do**:

- Execute tests (use language-specific test runners)
- Replace existing test documentation in your project
- Dictate specific test frameworks (uses project standards)

## Critical Rules

### 1. Coverage Requirements
- ✅ **Minimum: 80% line coverage** (blocking requirement for PR approval)
- ✅ **Target: 90%+ line coverage** (aim for this on all new code)
- ✅ **Critical code: 100% coverage** (auth, payments, data loss scenarios)
- ❌ **NEVER merge** PRs with <80% coverage
- ❌ **NEVER skip tests** for "simple" code

### 2. Testing Pyramid Distribution
- ✅ **60% Unit tests** - Fast, isolated, mock dependencies
- ✅ **30% Integration tests** - Component interactions, real dependencies where practical
- ✅ **10% E2E tests** - Critical user workflows only
- ❌ **NEVER invert pyramid** (more E2E than unit = slow, brittle)

### 3. Test Quality Standards
- ✅ **Test behaviour, NOT implementation** - Verify what code does, not how
- ✅ **Include edge cases and errors** - Empty input, null values, exceptions, timeouts
- ✅ **Use descriptive names** - `test_<what>_<condition>_<expected_outcome>`
- ✅ **Keep tests independent** - No shared state, setup within each test
- ❌ **NEVER test only happy path** - Edge cases catch real bugs
- ❌ **NEVER mock what you're testing** - Only mock dependencies

### 4. Acceptance Criteria Coverage
- ✅ **Every AC must have tests** (both unit and integration)
- ✅ **Mark ACs complete** only when tests pass
- ✅ **Include security tests** for auth, validation, input sanitisation
- ❌ **NEVER skip AC testing** - Untested ACs are incomplete

### 5. External Integration Testing
- ✅ **Create mocks for external APIs** (use Mockoon for HTTP mocks)
- ✅ **Test error scenarios** (500 errors, timeouts, rate limits)
- ✅ **Document mock setup** in test files and design proposals
- ❌ **NEVER test against live external services** in CI (unreliable, slow)

## Model Selection

**Recommended model**: Sonnet (Haiku for simple test execution)

**Why Sonnet for most operations**:

- **Test strategy planning** - Requires reasoning about risk, complexity, and coverage
- **Coverage analysis** - Understanding what coverage metrics mean and where gaps are
- **Test quality review** - Assessing if tests verify behaviour vs implementation
- **Mock strategy** - Deciding between mocks, stubs, fakes for different scenarios
- **Edge case identification** - Deep thinking to surface non-obvious test scenarios

**When Haiku is appropriate**:

- Running existing test suites (straightforward command execution)
- Formatting test output for reporting
- Simple test result parsing

**Operations by model**:

- ✅ Sonnet: Test strategy, coverage analysis, test quality review, mock design
- ✅ Haiku: Test execution, result formatting, simple reporting

## Quick Start

### Planning Test Strategy for a Story

1. **Identify test layers needed** (see Testing Pyramid below)
2. **Define coverage targets** (80% minimum, 90%+ target)
3. **List key test scenarios** (happy path, edge cases, error scenarios)
4. **Decide mock strategy** (external APIs, databases, services)
5. **Document in design proposal** (see`developer-analysis` skill)

### Reviewing Test Quality in PR

1. **Verify all ACs have tests** (both unit and integration)
2. **Check coverage report** (>80% minimum, aim for 90%+)
3. **Assess test quality** (testing behaviour, not implementation)
4. **Review test naming** (descriptive, follows conventions)
5. **Validate edge cases** (error scenarios, boundary conditions)

See `references/test-strategy.md` for comprehensive testing workflow.

## Testing Pyramid

**Target distribution** (by number of tests):

```
       /\
      /  \     E2E (10%)
     /----\
    /      \   Integration (30%)
   /--------\
  /          \ Unit (60%)
 /------------\
```

**Unit tests (60% of tests)**:

- Test individual functions/methods in isolation
- Fast execution (<1ms per test)
- Mock all external dependencies
- Focus on logic, edge cases, error handling

**Integration tests (30% of tests)**:

- Test component interactions
- Slower execution (~100ms per test)
- Use real dependencies where practical (in-memory DB, test containers)
- Focus on data flow, API contracts, service integration

**End-to-end tests (10% of tests)**:

- Test complete user workflows
- Slowest execution (~1s+ per test)
- Use production-like environment
- Focus on critical paths, user journeys

**Why this distribution**:

- Unit tests catch most bugs early (fast feedback)
- Integration tests catch interface issues
- E2E tests catch workflow issues
- Inverted pyramid (more E2E than unit) = slow, brittle tests

### Testing Pyramid is a Guideline, Not a Rule

⚠️ **Important**: The 60/30/10 split is a **guideline**, not an absolute requirement. Adjust based on your project context.

**When to deviate from the pyramid**:

✅ **More integration tests** (e.g., 50/40/10) when:
- Building API services (integration tests verify endpoints work)
- Heavy database operations (testing queries with real DB catches issues)
- Microservices (service-to-service integration is critical)
- Complex data transformations (integration tests verify end-to-end flow)

✅ **More E2E tests** (e.g., 50/30/20) when:
- User-facing workflows are business-critical (e.g., checkout flow in e-commerce)
- Compliance/regulatory requirements (must prove complete workflow works)
- Visual regression important (testing UI rendering and interactions)
- Complex multi-step workflows (booking systems, approval workflows)

✅ **More unit tests** (e.g., 80/15/5) when:
- Pure algorithmic code (search algorithms, data processing)
- Complex business logic (pricing rules, eligibility calculations)
- Libraries/frameworks (public APIs with minimal external dependencies)
- Mathematical/scientific computing (pure functions, deterministic outputs)

❌ **Avoid anti-patterns**:
- **Inverted pyramid** (70% E2E, 20% integration, 10% unit) - Slow, brittle, expensive to maintain
- **Only unit tests** (100% unit, 0% integration/E2E) - Misses integration issues and real-world failures
- **Only E2E tests** (100% E2E) - Slow feedback, hard to debug, flaky tests

**Example context-specific distributions**:

| Project Type | Unit | Integration | E2E | Rationale |
|--------------|------|-------------|-----|-----------|
| **REST API** | 50% | 40% | 10% | Heavy integration testing for endpoints |
| **UI-heavy app** | 50% | 30% | 20% | More E2E for critical user flows |
| **Algorithm library** | 80% | 15% | 5% | Pure logic, minimal integration |
| **Microservices** | 55% | 35% | 10% | Service integration critical |
| **Data pipeline** | 50% | 45% | 5% | Data transformation integration |

**Key principles** (always apply):
1. ✅ **Fast feedback** - Majority of tests should run quickly (<5s total for unit tests)
2. ✅ **Test critical paths** - Always have tests for auth, payments, data loss scenarios
3. ✅ **Avoid brittle tests** - Don't rely too heavily on slow, flaky E2E tests
4. ✅ **Balance speed and confidence** - More integration tests = slower, but catches more real issues

**How to decide your distribution**:
1. Start with 60/30/10 as baseline
2. Identify your highest-risk areas (APIs? UI workflows? Business logic?)
3. Add more tests at the appropriate level for those areas
4. Measure test suite speed - if too slow, shift toward more unit tests
5. Monitor production bugs - if integration issues slip through, add more integration tests

**When in doubt**: Err toward more tests at lower levels (unit > integration > E2E) for faster, more reliable feedback.

## Coverage Targets

**Minimum**: 80% line coverage (blocking requirement for PR approval)
**Target**: 90%+ line coverage (aim for this)

**What coverage means**:

- **Line coverage**: % of code lines executed by tests
- **Branch coverage**: % of decision branches (if/else) tested
- **Function coverage**: % of functions called by tests

**Coverage is necessary but not sufficient**:

- ✅ 90% coverage with behaviour tests = good
- ❌ 90% coverage with implementation tests = brittle
- ❌ 90% coverage testing only happy path = incomplete

See `references/coverage-guide.md` for coverage analysis workflow.

## Test Quality Principles

### 1. Test Behaviour, Not Implementation

❌ **Bad - Testing implementation**:

```python
def test_search_calls_database():
    search = SearchService()
    search.search("query")
    assert search.db.query.called  # Testing HOW, not WHAT
```

✅ **Good - Testing behaviour**:

```python
def test_search_returns_matching_results():
    search = SearchService()
    results = search.search("python")
    assert len(results) > 0
    assert all("python" in r.title.lower() for r in results)  # Testing WHAT
```

### 2. Test Edge Cases and Errors

**Every feature needs**:

- ✅ Happy path tests (basic functionality works)
- ✅ Edge case tests (boundary conditions, empty input, null values)
- ✅ Error tests (invalid input, exceptions, timeouts)

**Example test scenarios**:

```python
# Happy path
def test_parse_pdf_extracts_text(): ...

# Edge cases
def test_parse_pdf_handles_empty_pdf(): ...
def test_parse_pdf_handles_single_page(): ...
def test_parse_pdf_handles_large_pdf(): ...

# Error scenarios
def test_parse_pdf_raises_on_corrupted_file(): ...
def test_parse_pdf_raises_on_password_protected(): ...
def test_parse_pdf_raises_on_invalid_format(): ...
```

### 3. Use Descriptive Test Names

❌ **Bad test names**:

```python
def test_search(): ...
def test_error(): ...
def test_1(): ...
```

✅ **Good test names**:

```python
def test_search_returns_results_matching_query(): ...
def test_search_returns_empty_list_when_no_matches(): ...
def test_search_raises_value_error_for_empty_query(): ...
```

**Naming pattern**: `test_<what>_<condition>_<expected_outcome>`

### 4. Keep Tests Independent

❌ **Bad - Tests depend on each other**:

```python
def test_create_user():
    user = create_user("alice")
    assert user.id == 1

def test_update_user():
    user = get_user(1)  # Depends on test_create_user running first!
    update_user(user, name="bob")
```

✅ **Good - Tests are independent**:

```python
def test_create_user():
    user = create_user("alice")
    assert user.name == "alice"

def test_update_user():
    user = create_user("alice")  # Setup within test
    update_user(user, name="bob")
    assert user.name == "bob"
```

### 5. Use Fixtures/Factories for Test Data

✅ **Good - Reusable test data**:

```python
@pytest.fixture
def sample_user():
    return User(id=1, name="alice", email="alice@example.com")

def test_user_serialization(sample_user):
    data = sample_user.to_dict()
    assert data["name"] == "alice"

def test_user_validation(sample_user):
    assert sample_user.is_valid()
```

## Mocking Strategy

See `references/mocking-patterns.md` for comprehensive mock/stub/fake patterns.

**Quick decision guide**:

**Use mocks when**:

- Verifying interactions (was method called? with what args?)
- External service calls (HTTP APIs, databases)
- Side effects (file I/O, network calls)

**Use stubs when**:

- Providing fixed responses
- Simulating external data sources
- Replacing slow dependencies

**Use fakes when**:

- In-memory implementation of real service (e.g., fake database)
- More realistic than stubs
- Need stateful behaviour

**Use real dependencies when**:

- Fast to set up (in-memory databases, test containers)
- Integration tests
- Adds confidence without significant speed penalty

**External service mocking**:

- Use Mockoon for API mocks (see`epic-planning.md` in`project-management` skill)
- Create OpenAPI/GraphQL specs for API contracts
- Include error scenarios in mock responses

## Test Organisation

### File Structure

**Co-locate tests with source** (if project allows):

```
src/
  search/
    __init__.py
    service.py
    test_service.py  # Tests next to implementation
```

**Or separate test directory**:

```
src/
  search/
    __init__.py
    service.py
tests/
  unit/
    search/
      test_service.py
  integration/
    search/
      test_search_api.py
```

### Test File Naming

- `test_<module>.py` for Python
- `<module>.test.ts` or`<module>.spec.ts` for TypeScript/JavaScript
- Follow project conventions

### Test Class Organisation

```python
class TestSearchService:
    """Tests for SearchService."""

    class TestHappyPath:
        """Happy path scenarios."""
        def test_returns_results_for_valid_query(self): ...

    class TestEdgeCases:
        """Edge cases and boundary conditions."""
        def test_returns_empty_for_no_matches(self): ...
        def test_handles_special_characters_in_query(self): ...

    class TestErrorHandling:
        """Error scenarios."""
        def test_raises_on_invalid_query(self): ...
        def test_handles_service_timeout(self): ...
```

## Testing External Integrations

**For stories involving external APIs or services**:

1. **Create API contract** (OpenAPI, GraphQL schema)
2. **Create mock using Mockoon** (see`epic-planning.md`)
3. **Write integration tests against mock**
4. **Include error scenarios** (timeouts, 500 errors, rate limits)
5. **Document integration testing** in story "Testing Strategy" section

**Example**:

```python
@pytest.fixture
def auth_api_mock():
    """Mock authentication API using Mockoon."""
    # Assumes Mockoon container running on localhost:3001
    return "http://localhost:3001"

def test_authenticate_success(auth_api_mock):
    client = AuthClient(auth_api_mock)
    token = client.authenticate("user", "pass")
    assert token is not None

def test_authenticate_handles_invalid_credentials(auth_api_mock):
    client = AuthClient(auth_api_mock)
    with pytest.raises(AuthenticationError):
        client.authenticate("user", "wrongpass")
```

## Performance Testing

**When to add performance tests**:

- Performance is an explicit requirement in story ACs
- System has performance SLAs
- Previous performance regressions occurred

**Performance test pattern**:

```python
def test_search_performance():
    """Search completes within 100ms for typical query."""
    start = time.time()
    results = search_service.search("python")
    duration = time.time() - start

    assert duration < 0.1, f"Search took {duration}s, expected <0.1s"
    assert len(results) > 0, "Should return results"
```

**Load testing** (separate from unit/integration tests):

- Use dedicated tools (Locust, k6, Apache JMeter)
- Run against staging environment
- Document in`docs/PERFORMANCE.md`

## Security Testing

**Security test checklist** (see `developer-analysis` skill for full OWASP coverage):

- [ ] Input validation tests (SQL injection, XSS, command injection)
- [ ] Authentication tests (invalid tokens, expired sessions)
- [ ] Authorisation tests (access control, privilege escalation)
- [ ] Rate limiting tests (abuse prevention)
- [ ] Secrets management tests (no hardcoded credentials)

**Example**:

```python
def test_search_sanitizes_sql_injection():
    """Search safely handles SQL injection attempts."""
    malicious_query = "'; DROP TABLE users; --"
    results = search_service.search(malicious_query)
    # Should safely escape query, not execute SQL
    assert isinstance(results, list)

def test_api_requires_authentication():
    """API rejects unauthenticated requests."""
    client = APIClient()  # No auth token
    with pytest.raises(UnauthorizedError):
        client.search("query")
```

## Language-Specific Patterns

### Python (pytest)

```python
import pytest

# Fixtures
@pytest.fixture
def sample_data():
    return {"key": "value"}

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    ("python", 10),
    ("java", 5),
    ("", 0),
])
def test_search_counts(input, expected):
    assert search_service.count(input) == expected

# Exception testing
def test_raises_on_invalid_input():
    with pytest.raises(ValueError, match="Invalid input"):
        process_input(None)

# Mocking
from unittest.mock import Mock, patch

@patch('module.external_api')
def test_with_mock(mock_api):
    mock_api.get.return_value = {"data": "value"}
    result = service.fetch_data()
    assert result["data"] == "value"
```

### TypeScript/JavaScript (Jest)

```typescript
import { describe, test, expect, jest } from '@jest/globals';

describe('SearchService', () => {
  test('returns results for valid query', () => {
    const service = new SearchService();
    const results = service.search('typescript');
    expect(results.length).toBeGreaterThan(0);
  });

  test('throws error for invalid query', () => {
    const service = new SearchService();
    expect(() => service.search('')).toThrow('Invalid query');
  });

  test('handles async operations', async () => {
    const service = new SearchService();
    const results = await service.searchAsync('typescript');
    expect(results).toBeDefined();
  });

  test('mocks external API', () => {
    const mockApi = jest.fn().mockResolvedValue({ data: 'value' });
    const service = new SearchService(mockApi);
    // ...
  });
});
```

### Flutter/Dart

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';

// Unit tests
void main() {
  group('SearchService', () {
    test('returns results for valid query', () {
      final service = SearchService();
      final results = service.search('flutter');
      expect(results.length, greaterThan(0));
    });

    test('throws exception for empty query', () {
      final service = SearchService();
      expect(() => service.search(''), throwsArgumentError);
    });

    test('handles async operations', () async {
      final service = SearchService();
      final results = await service.searchAsync('flutter');
      expect(results, isNotNull);
      expect(results, isA<List<SearchResult>>());
    });
  });
}

// Widget tests
void main() {
  testWidgets('displays search results', (WidgetTester tester) async {
    // Build widget
    await tester.pumpWidget(MaterialApp(
      home: SearchPage(),
    ));

    // Enter text and trigger search
    await tester.enterText(find.byType(TextField), 'flutter');
    await tester.tap(find.byIcon(Icons.search));
    await tester.pumpAndSettle(); // Wait for animations/async

    // Verify results displayed
    expect(find.text('Flutter result'), findsOneWidget);
    expect(find.byType(SearchResultCard), findsWidgets);
  });

  testWidgets('shows error message on search failure', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: SearchPage(service: FailingSearchService()),
    ));

    await tester.tap(find.byIcon(Icons.search));
    await tester.pump(); // Trigger frame

    expect(find.text('Search failed'), findsOneWidget);
    expect(find.byType(ErrorWidget), findsOneWidget);
  });
}

// Mocking with mockito
@GenerateMocks([SearchApi, AuthService])
void main() {
  late MockSearchApi mockApi;
  late SearchService service;

  setUp(() {
    mockApi = MockSearchApi();
    service = SearchService(mockApi);
  });

  test('calls API with correct parameters', () async {
    when(mockApi.search(any)).thenAnswer((_) async => [
      SearchResult(id: 1, title: 'Result'),
    ]);

    await service.performSearch('flutter');

    verify(mockApi.search('flutter')).called(1);
    verifyNoMoreInteractions(mockApi);
  });

  test('handles API errors', () async {
    when(mockApi.search(any)).thenThrow(NetworkException('No connection'));

    expect(
      () => service.performSearch('flutter'),
      throwsA(isA<NetworkException>()),
    );
  });
}

// Golden tests (snapshot testing)
void main() {
  testWidgets('matches golden file', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: SearchResultCard(
        title: 'Flutter Tutorial',
        description: 'Learn Flutter testing',
      ),
    ));

    await expectLater(
      find.byType(SearchResultCard),
      matchesGoldenFile('goldens/search_result_card.png'),
    );
  });
}

// Integration tests (integration_test directory)
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('complete search flow', (WidgetTester tester) async {
    app.main();
    await tester.pumpAndSettle();

    // Navigate to search
    await tester.tap(find.byIcon(Icons.search));
    await tester.pumpAndSettle();

    // Enter query
    await tester.enterText(find.byType(TextField), 'flutter');
    await tester.testTextInput.receiveAction(TextInputAction.search);
    await tester.pumpAndSettle();

    // Verify results
    expect(find.text('Flutter Tutorial'), findsOneWidget);
  });
}
```

**Flutter testing best practices**:

- **Widget tests** (60%) - Test UI components in isolation
- **Unit tests** (30%) - Test business logic and services
- **Integration tests** (10%) - Test complete user flows
- Use `pump()` for single frame, `pumpAndSettle()` for all animations
- Use `find.byType()`, `find.text()`, `find.byKey()` for widget discovery
- Golden tests for visual regression testing
- Mock external dependencies with `mockito` package
- Use `setUp()` and `tearDown()` for test fixtures
- Run tests: `flutter test` (unit/widget), `flutter test integration_test` (integration)
- Coverage: `flutter test --coverage` → `genhtml coverage/lcov.info -o coverage/html`

## Australian English

All test names, comments, and documentation use **Australian English spelling**:

- ✅ normalise, organisation, authorisation, colour, behaviour
- ❌ normalize, organization, authorization, color, behavior

This is a **project-wide standard**, not optional.

## Related Skills

- **developer-analysis** - Uses this skill when planning testing strategy in design proposals
- **git-workflow** - Uses this skill when reviewing test quality in PRs (see`pr-review.md`)
- **project-management** - Uses this skill when defining testing requirements in stories

## References

Detailed guides in `references/` folder:

- `test-strategy.md` - Comprehensive testing strategy and workflow
- `coverage-guide.md` - Coverage targets, analysis, and gap identification
- `mocking-patterns.md` - Mock/stub/fake patterns for different scenarios

## Further Reading

- Testing pyramid: Martin Fowler's blog
- Test-driven development (TDD): Kent Beck
- Growing Object-Oriented Software, Guided by Tests: Freeman & Pryce
- Working Effectively with Legacy Code: Michael Feathers
