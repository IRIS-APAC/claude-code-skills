# Test Strategy and Planning

Comprehensive guide for planning and executing testing strategy.

## When to Plan Test Strategy

**During developer analysis** (before implementation):
1. Review story acceptance criteria
2. Identify test layers needed (unit, integration, E2E)
3. List key test scenarios
4. Decide mock strategy for external dependencies
5. Document in design proposal

**During implementation**:
1. Write tests alongside code (TDD or test-alongside)
2. Ensure each AC has corresponding tests
3. Add tests for edge cases discovered during development

**During PR review**:
1. Verify all ACs have tests
2. Check coverage meets minimum (80%) and target (90%+)
3. Assess test quality (behaviour vs implementation)

## Test Strategy Template

Include in design proposal (see `developer-analysis` skill):

```markdown
## Testing Strategy

**Test layers**:
- Unit tests: `<modules to test>` (60% of tests)
- Integration tests: `<component interactions to test>` (30% of tests)
- E2E tests (if needed): `<user workflows to test>` (10% of tests)

**Key scenarios**:
- Happy path: `<primary use case>`
- Edge cases: `<boundary conditions, empty input, etc.>`
- Error scenarios: `<invalid input, exceptions, timeouts>`

**Mock strategy**:
- External APIs: Mockoon mock for `<service>`
- Database: In-memory SQLite / test containers
- File I/O: Temporary test directories

**Coverage target**: 90%+ (minimum 80%)

**Test execution time target**: <5s for unit tests, <30s for integration tests
```

## Test-Driven Development (TDD)

**TDD cycle** (Red-Green-Refactor):

1. **Red**: Write failing test first
2. **Green**: Write minimal code to make test pass
3. **Refactor**: Improve code while keeping tests green

**Example TDD workflow**:

```python
# Step 1: RED - Write failing test
def test_search_returns_results_for_valid_query():
    service = SearchService()
    results = service.search("python")
    assert len(results) > 0  # Fails - method doesn't exist yet

# Step 2: GREEN - Minimal implementation
class SearchService:
    def search(self, query: str) -> list:
        return [{"title": "Python result"}]  # Hardcoded to pass

# Step 3: REFACTOR - Real implementation
class SearchService:
    def __init__(self, db):
        self.db = db

    def search(self, query: str) -> list:
        return self.db.query("SELECT * FROM docs WHERE title LIKE ?", f"%{query}%")
```

**When to use TDD**:
- ✅ Well-defined requirements (clear ACs)
- ✅ Complex logic (algorithms, business rules)
- ✅ Bug fixes (write failing test first, then fix)

**When NOT to use TDD**:
- ❌ Exploratory work (spike, POC)
- ❌ UI/UX experimentation
- ❌ Unclear requirements (write code first to understand problem)

## Test Scenarios Checklist

**For every feature, test**:

### Happy Path (Primary Use Cases)
- [ ] Basic functionality works
- [ ] Returns expected output for valid input
- [ ] Side effects occur as expected

### Edge Cases (Boundary Conditions)
- [ ] Empty input
- [ ] Null/None values
- [ ] Single item
- [ ] Large datasets
- [ ] Maximum/minimum values
- [ ] Special characters
- [ ] Unicode/international characters

### Error Scenarios
- [ ] Invalid input types
- [ ] Out-of-range values
- [ ] Missing required fields
- [ ] Duplicate entries
- [ ] Concurrent access
- [ ] External service failures (timeouts, errors)
- [ ] Resource exhaustion (memory, disk space)

### Security Scenarios (If Applicable)
- [ ] SQL injection attempts
- [ ] XSS attempts
- [ ] Command injection attempts
- [ ] Path traversal attempts
- [ ] Authentication bypass attempts
- [ ] Authorisation escalation attempts

## Writing Effective Unit Tests

**Unit test template**:

```python
def test_<function>_<scenario>_<expected_outcome>():
    """Brief description of what this test verifies."""
    # Arrange: Set up test data and dependencies
    service = SearchService(mock_db)
    query = "python"

    # Act: Execute the function being tested
    results = service.search(query)

    # Assert: Verify expected outcome
    assert len(results) > 0
    assert all("python" in r.title.lower() for r in results)
```

**AAA pattern** (Arrange-Act-Assert):
1. **Arrange**: Set up test data, mocks, dependencies
2. **Act**: Call the function/method being tested
3. **Assert**: Verify the outcome

**Good unit test characteristics**:
- ✅ **Fast**: <1ms execution time
- ✅ **Isolated**: No external dependencies (mocked)
- ✅ **Repeatable**: Same result every time
- ✅ **Self-validating**: Pass/fail, no manual verification
- ✅ **Timely**: Written close to code (TDD or test-alongside)

## Writing Effective Integration Tests

**Integration test template**:

```python
def test_search_api_integration():
    """Test search API end-to-end with real database."""
    # Arrange: Set up test database with sample data
    db = create_test_database()
    db.insert_documents([
        {"id": 1, "title": "Python Guide"},
        {"id": 2, "title": "Java Tutorial"},
    ])
    api = SearchAPI(db)

    # Act: Call API endpoint
    response = api.post("/search", json={"query": "python"})

    # Assert: Verify response
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert results[0]["title"] == "Python Guide"

    # Cleanup: Remove test database
    db.close()
```

**Integration test characteristics**:
- ✅ **Tests component interactions**: API + Database, Service + External API
- ✅ **Uses real dependencies where practical**: In-memory DB, test containers
- ✅ **Slower than unit tests**: ~100ms execution acceptable
- ✅ **Tests data flow**: Request → Service → Database → Response

## Testing External Dependencies

### Strategy 1: Mockoon for External APIs

**When to use**:
- External HTTP APIs (REST, GraphQL)
- Complex request/response scenarios
- Need to test error conditions (500, timeouts, rate limits)

**Setup**:
1. Create OpenAPI/GraphQL spec
2. Create Mockoon environment file
3. Start Mockoon in test setup
4. Run tests against mock

**Example**:
```python
@pytest.fixture(scope="session")
def auth_api_mock():
    """Start Mockoon mock for auth API."""
    process = subprocess.Popen([
        "mockoon-cli", "start",
        "--data", "mocks/auth-api.mockoon.json",
        "--port", "3001"
    ])
    yield "http://localhost:3001"
    process.terminate()

def test_authenticate_with_valid_credentials(auth_api_mock):
    client = AuthClient(base_url=auth_api_mock)
    token = client.authenticate("user", "password")
    assert token is not None
```

### Strategy 2: Test Containers

**When to use**:
- Database integration tests
- Message queue integration tests
- Need realistic behaviour without external dependencies

**Example** (Python with testcontainers):
```python
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def postgres_db():
    """Start PostgreSQL container for testing."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres.get_connection_url()

def test_database_operations(postgres_db):
    db = Database(postgres_db)
    db.create_user("alice")
    user = db.get_user("alice")
    assert user.name == "alice"
```

### Strategy 3: In-Memory Implementations

**When to use**:
- Fast alternative to real database
- Simple data structures
- No need for complex queries

**Example**:
```python
class InMemoryDatabase:
    """Fake database for testing."""
    def __init__(self):
        self.users = {}

    def create_user(self, name):
        user_id = len(self.users) + 1
        self.users[user_id] = {"id": user_id, "name": name}
        return self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(user_id)

def test_with_in_memory_db():
    db = InMemoryDatabase()
    user = db.create_user("alice")
    assert user["name"] == "alice"
```

## Test Data Management

### Fixtures (pytest)

```python
@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(id=1, name="alice", email="alice@example.com")

@pytest.fixture
def sample_users():
    """Create multiple sample users for testing."""
    return [
        User(id=1, name="alice", email="alice@example.com"),
        User(id=2, name="bob", email="bob@example.com"),
    ]

def test_user_serialization(sample_user):
    data = sample_user.to_dict()
    assert data["name"] == "alice"
```

### Factory Pattern

```python
class UserFactory:
    """Factory for creating test users."""
    _id_counter = 1

    @classmethod
    def create(cls, **kwargs):
        """Create a user with default values."""
        defaults = {
            "id": cls._id_counter,
            "name": "testuser",
            "email": "test@example.com"
        }
        cls._id_counter += 1
        return User(**{**defaults, **kwargs})

def test_with_factory():
    user1 = UserFactory.create(name="alice")
    user2 = UserFactory.create(name="bob")
    assert user1.id != user2.id  # Unique IDs
```

## Test Maintenance

### When to Update Tests

**Tests should be updated when**:
- ✅ Behaviour changes (AC modified)
- ✅ Bug fixed (add regression test)
- ✅ Refactoring changes public interface
- ✅ Test is flaky (intermittent failures)

**Tests should NOT be updated when**:
- ❌ Refactoring internal implementation (tests should still pass)
- ❌ Test is failing correctly (fix code, not test)

### Refactoring Tests

**Signs tests need refactoring**:
- Duplicated setup code across tests
- Tests are brittle (break on minor changes)
- Tests are slow
- Test names don't describe what they test

**Refactoring patterns**:

**Extract fixture**:
```python
# Before: Duplicated setup
def test_create_user():
    db = Database("test.db")
    db.connect()
    service = UserService(db)
    user = service.create("alice")
    assert user.name == "alice"

def test_delete_user():
    db = Database("test.db")
    db.connect()
    service = UserService(db)
    # ...

# After: Extracted fixture
@pytest.fixture
def user_service():
    db = Database("test.db")
    db.connect()
    return UserService(db)

def test_create_user(user_service):
    user = user_service.create("alice")
    assert user.name == "alice"
```

**Parametrize tests**:
```python
# Before: Repetitive tests
def test_search_python():
    results = search("python")
    assert "python" in results

def test_search_java():
    results = search("java")
    assert "java" in results

# After: Parametrized
@pytest.mark.parametrize("query", ["python", "java", "typescript"])
def test_search_returns_results(query):
    results = search(query)
    assert query in results
```

## Regression Testing

**What is regression testing**:
- Testing that previously working features still work
- Prevents bugs from reappearing
- Adds test when bug is fixed

**Regression test workflow**:
1. **Bug reported**: "Search returns duplicate results"
2. **Write failing test**: Reproduces the bug
3. **Fix bug**: Modify code to make test pass
4. **Commit test + fix**: Test prevents regression

**Example**:
```python
def test_search_returns_unique_results():
    """Regression test for bug #123: Search returned duplicates."""
    results = search_service.search("python")
    result_ids = [r.id for r in results]
    assert len(result_ids) == len(set(result_ids)), "Results should be unique"
```

**Tagging regression tests**:
```python
import pytest

@pytest.mark.regression
@pytest.mark.bug_123
def test_search_returns_unique_results():
    """Regression test for bug #123."""
    ...
```

## Continuous Integration (CI)

**Test execution in CI pipeline**:

```yaml
# Example .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=term --cov-report=xml

      - name: Check coverage threshold
        run: |
          coverage report --fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
```

**CI requirements**:
- [ ] All tests run on every commit
- [ ] Coverage threshold enforced (80% minimum)
- [ ] Test failures block merge
- [ ] Fast feedback (<5 minutes for unit tests)

## Test Reporting

**Coverage report format**:
```
## Test Results: 288/288 Passing ✅

**Coverage**: 89% (target: 90%, minimum: 80%)

**Module breakdown**:
- src/search/: 92% (42/42 tests passing)
- src/auth/: 88% (28/28 tests passing)
- src/api/: 86% (35/35 tests passing)

**Command**:
```bash
pytest --cov=src tests/ -v
======================== 288 passed in 4.26s =========================
```

Include in PR description (see `git-workflow/references/pr-template.md`).

## Australian English

All test names, comments, and documentation use **Australian English spelling**:
- ✅ normalise, organisation, authorisation, behaviour
- ❌ normalize, organization, authorization, behavior
