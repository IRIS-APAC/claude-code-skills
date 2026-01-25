# Mocking Patterns and Strategies

Comprehensive guide for mocking external dependencies in tests.

## Test Doubles Overview

**Test double**: Generic term for any replacement of a production object for testing purposes.

### Types of Test Doubles

**Mock**: Verifies interactions (method calls, arguments)
**Stub**: Provides fixed responses
**Fake**: Working implementation (simpler than real)
**Spy**: Records calls for later verification
**Dummy**: Placeholder (never used)

## When to Use Each Type

### Mocks: Verify Interactions

**Use mocks when**:
- Testing that a method/function is called
- Verifying arguments passed to a method
- Ensuring side effects occur (email sent, log written)

**Example**:
```python
from unittest.mock import Mock

def test_order_confirmation_sends_email():
    """Verify that email is sent when order is confirmed."""
    mock_email_service = Mock()
    order_service = OrderService(mock_email_service)

    order_service.confirm_order(order_id=123)

    # Verify interaction: email service was called
    mock_email_service.send_confirmation.assert_called_once_with(
        to="customer@example.com",
        subject="Order confirmed",
        order_id=123
    )
```

**When NOT to use mocks**:
- ❌ Don't mock what you're testing (test the real implementation)
- ❌ Don't over-mock (makes tests brittle)
- ❌ Don't mock simple data structures (use real objects)

### Stubs: Provide Fixed Responses

**Use stubs when**:
- External service returns data you need for testing
- Need predictable responses
- Don't care about verification (just need data)

**Example**:
```python
from unittest.mock import Mock

def test_user_can_login_with_valid_credentials():
    """Test login flow with stubbed authentication service."""
    # Stub: Returns fixed response
    stub_auth_service = Mock()
    stub_auth_service.authenticate.return_value = {"token": "abc123", "user_id": 42}

    login_controller = LoginController(stub_auth_service)
    response = login_controller.login("user@example.com", "password")

    # We don't verify authenticate was called, just that login succeeds
    assert response["token"] == "abc123"
    assert response["user_id"] == 42
```

**Stub different scenarios**:
```python
def test_login_handles_invalid_credentials():
    stub_auth_service = Mock()
    stub_auth_service.authenticate.side_effect = AuthenticationError("Invalid credentials")

    login_controller = LoginController(stub_auth_service)

    with pytest.raises(AuthenticationError):
        login_controller.login("user@example.com", "wrongpassword")
```

### Fakes: Simplified Working Implementation

**Use fakes when**:
- Need stateful behaviour (not just fixed responses)
- Want more realistic testing than mocks/stubs
- Real implementation is slow or complex

**Example** (fake database):
```python
class FakeDatabase:
    """In-memory fake database for testing."""
    def __init__(self):
        self.users = {}
        self._id_counter = 1

    def create_user(self, name, email):
        user = {
            "id": self._id_counter,
            "name": name,
            "email": email
        }
        self.users[self._id_counter] = user
        self._id_counter += 1
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def update_user(self, user_id, **kwargs):
        if user_id not in self.users:
            raise ValueError("User not found")
        self.users[user_id].update(kwargs)
        return self.users[user_id]

# Test with fake database
def test_user_lifecycle():
    db = FakeDatabase()
    user_service = UserService(db)

    # Create user
    user = user_service.create("alice", "alice@example.com")
    assert user["id"] == 1

    # Retrieve user
    retrieved = user_service.get(user["id"])
    assert retrieved["name"] == "alice"

    # Update user
    updated = user_service.update(user["id"], name="alice smith")
    assert updated["name"] == "alice smith"
```

**When to use fakes**:
- ✅ Database (in-memory SQLite, test containers)
- ✅ File system (in-memory file system)
- ✅ Message queue (in-memory queue)
- ✅ Cache (simple dict-based cache)

### Spies: Record Interactions

**Use spies when**:
- Need to verify interactions but also want real behaviour
- Want to test both "what" and "how"

**Example**:
```python
from unittest.mock import Mock

def test_cache_is_used_after_first_call():
    """Verify that cache is used on second call (spy on cache)."""
    real_db = Database()
    spy_cache = Mock(wraps=RealCache())  # Spy: wraps real implementation

    service = UserService(real_db, spy_cache)

    # First call: should miss cache, hit database
    user1 = service.get_user(123)
    spy_cache.get.assert_called_once_with("user:123")
    spy_cache.set.assert_called_once_with("user:123", user1)

    # Second call: should hit cache
    spy_cache.get.reset_mock()  # Reset spy call counts
    user2 = service.get_user(123)
    spy_cache.get.assert_called_once_with("user:123")
    spy_cache.set.assert_not_called()  # Should not set again
```

## Mock Patterns

### Pattern 1: Return Fixed Value

```python
from unittest.mock import Mock

mock_service = Mock()
mock_service.get_data.return_value = {"key": "value"}

result = mock_service.get_data()
assert result == {"key": "value"}
```

### Pattern 2: Return Different Values on Successive Calls

```python
mock_service = Mock()
mock_service.get_status.side_effect = ["pending", "processing", "complete"]

assert mock_service.get_status() == "pending"
assert mock_service.get_status() == "processing"
assert mock_service.get_status() == "complete"
```

### Pattern 3: Raise Exception

```python
mock_service = Mock()
mock_service.process.side_effect = ValueError("Invalid input")

with pytest.raises(ValueError, match="Invalid input"):
    mock_service.process()
```

### Pattern 4: Custom Function Behaviour

```python
def custom_function(x):
    return x * 2

mock_service = Mock()
mock_service.calculate.side_effect = custom_function

assert mock_service.calculate(5) == 10
assert mock_service.calculate(10) == 20
```

### Pattern 5: Verify Method Called with Specific Arguments

```python
mock_service = Mock()
mock_service.send_email("user@example.com", "Subject", "Body")

# Exact match
mock_service.send_email.assert_called_once_with(
    "user@example.com",
    "Subject",
    "Body"
)

# Partial match
mock_service.send_email.assert_called_once()
assert mock_service.send_email.call_args[0][0] == "user@example.com"  # First arg
```

### Pattern 6: Verify Method Called N Times

```python
mock_service = Mock()

mock_service.log("message 1")
mock_service.log("message 2")
mock_service.log("message 3")

# Verify called exactly 3 times
assert mock_service.log.call_count == 3

# Verify NOT called
mock_service.other_method.assert_not_called()
```

### Pattern 7: Mock Async Functions

```python
from unittest.mock import AsyncMock
import pytest

@pytest.mark.asyncio
async def test_async_function():
    mock_service = AsyncMock()
    mock_service.fetch_data.return_value = {"data": "value"}

    result = await mock_service.fetch_data()
    assert result == {"data": "value"}
```

## Patch Patterns (Monkey Patching)

### Pattern 1: Patch Function in Module

```python
from unittest.mock import patch

# Module: src/service.py
import requests

def fetch_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Test: tests/test_service.py
@patch('src.service.requests.get')
def test_fetch_user(mock_get):
    """Patch requests.get to avoid real HTTP call."""
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "alice"}
    mock_get.return_value = mock_response

    user = fetch_user(1)
    assert user["name"] == "alice"
    mock_get.assert_called_once_with("https://api.example.com/users/1")
```

### Pattern 2: Patch Class Constructor

```python
from unittest.mock import patch

# Module: src/service.py
from database import Database

class UserService:
    def __init__(self):
        self.db = Database()  # Real database connection

# Test: tests/test_service.py
@patch('src.service.Database')
def test_user_service(mock_database_class):
    """Patch Database class to use mock."""
    mock_db_instance = Mock()
    mock_database_class.return_value = mock_db_instance

    service = UserService()
    # service.db is now mock_db_instance
```

### Pattern 3: Patch Environment Variables

```python
from unittest.mock import patch
import os

@patch.dict(os.environ, {"API_KEY": "test-key-123"})
def test_api_client_uses_env_var():
    client = APIClient()  # Reads API_KEY from environment
    assert client.api_key == "test-key-123"
```

### Pattern 4: Patch Context Manager

```python
from unittest.mock import patch, mock_open

@patch('builtins.open', mock_open(read_data='file content'))
def test_read_file():
    """Patch file operations."""
    with open('file.txt', 'r') as f:
        content = f.read()

    assert content == 'file content'
```

### Pattern 5: Patch Multiple Things

```python
from unittest.mock import patch

@patch('src.service.requests.get')
@patch('src.service.cache.get')
@patch('src.service.cache.set')
def test_with_multiple_patches(mock_cache_set, mock_cache_get, mock_requests_get):
    """Patch multiple dependencies."""
    mock_cache_get.return_value = None  # Cache miss
    mock_requests_get.return_value = Mock(json=lambda: {"data": "value"})

    result = fetch_with_cache("key")

    mock_cache_get.assert_called_once_with("key")
    mock_requests_get.assert_called_once()
    mock_cache_set.assert_called_once_with("key", {"data": "value"})
```

## External Service Mocking with Mockoon

**When to use Mockoon**:
- Testing integrations with external HTTP APIs
- Need realistic request/response simulation
- Testing error scenarios (500 errors, timeouts, rate limits)

**Mockoon setup** (see `project-management/references/epic-planning.md` for details):

```bash
# Create mock from OpenAPI spec
mockoon-cli start \
  --data ./docs/api/auth-service.yaml \
  --port 3001 \
  --watch
```

**Test with Mockoon mock**:
```python
@pytest.fixture(scope="session")
def auth_api_mock():
    """Start Mockoon mock for authentication API."""
    import subprocess
    process = subprocess.Popen([
        "mockoon-cli", "start",
        "--data", "mocks/auth-api.mockoon.json",
        "--port", "3001"
    ])
    time.sleep(2)  # Wait for mock to start
    yield "http://localhost:3001"
    process.terminate()

def test_authenticate_success(auth_api_mock):
    client = AuthClient(base_url=auth_api_mock)
    token = client.authenticate("user", "password")
    assert token is not None

def test_authenticate_handles_500_error(auth_api_mock):
    """Mockoon configured to return 500 for specific scenario."""
    client = AuthClient(base_url=auth_api_mock)
    with pytest.raises(ServerError):
        client.authenticate("error", "password")
```

## Database Mocking Strategies

### Strategy 1: In-Memory SQLite (Fake)

**When to use**: Fast, no external dependencies, good for simple queries.

```python
import pytest
import sqlite3

@pytest.fixture
def test_db():
    """Create in-memory SQLite database."""
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO users VALUES (1, 'alice')")
    conn.execute("INSERT INTO users VALUES (2, 'bob')")
    conn.commit()
    yield conn
    conn.close()

def test_get_user(test_db):
    service = UserService(test_db)
    user = service.get_user(1)
    assert user["name"] == "alice"
```

### Strategy 2: Test Containers (Real)

**When to use**: Need production-like database, complex queries, realistic behaviour.

```python
from testcontainers.postgres import PostgresContainer
import pytest

@pytest.fixture(scope="session")
def postgres_db():
    """Start PostgreSQL container for testing."""
    with PostgresContainer("postgres:15") as postgres:
        conn_string = postgres.get_connection_url()
        yield conn_string

def test_with_real_postgres(postgres_db):
    db = Database(postgres_db)
    db.create_user("alice", "alice@example.com")
    user = db.get_user_by_email("alice@example.com")
    assert user["name"] == "alice"
```

### Strategy 3: Mock Database Client (Mock)

**When to use**: Unit testing service layer without database dependency.

```python
from unittest.mock import Mock

def test_user_service_creates_user():
    """Unit test with mocked database."""
    mock_db = Mock()
    mock_db.insert.return_value = {"id": 1, "name": "alice"}

    service = UserService(mock_db)
    user = service.create_user("alice", "alice@example.com")

    # Verify service calls database correctly
    mock_db.insert.assert_called_once_with(
        "users",
        {"name": "alice", "email": "alice@example.com"}
    )
    assert user["id"] == 1
```

## Anti-Patterns: Avoid Over-Mocking

### Anti-Pattern 1: Mocking Everything

❌ **Bad** (too much mocking):
```python
def test_user_service():
    mock_user = Mock()
    mock_user.name = "alice"
    mock_user.email = "alice@example.com"
    mock_user.id = 1
    # Why mock a simple data object?
```

✅ **Good** (use real objects):
```python
def test_user_service():
    user = User(id=1, name="alice", email="alice@example.com")
    # Simple data objects don't need mocking
```

### Anti-Pattern 2: Testing Mocks, Not Code

❌ **Bad** (testing the mock):
```python
def test_get_user():
    mock_db = Mock()
    mock_db.get_user.return_value = User(id=1, name="alice")

    user = mock_db.get_user(1)  # Just calling the mock!
    assert user.name == "alice"  # Testing mock behaviour, not real code
```

✅ **Good** (testing real code):
```python
def test_get_user():
    fake_db = FakeDatabase()
    fake_db.insert(User(id=1, name="alice"))

    service = UserService(fake_db)
    user = service.get_user(1)  # Testing real service code
    assert user.name == "alice"
```

### Anti-Pattern 3: Mocking What You're Testing

❌ **Bad** (mocking system under test):
```python
def test_search_service():
    service = Mock(spec=SearchService)  # Mocking what we're testing!
    service.search.return_value = [{"title": "Result"}]

    results = service.search("query")
    assert len(results) == 1  # Meaningless test
```

✅ **Good** (test real implementation):
```python
def test_search_service():
    mock_db = Mock()
    mock_db.query.return_value = [{"title": "Result"}]

    service = SearchService(mock_db)  # Real service, mock dependency
    results = service.search("query")
    assert len(results) == 1
```

### Anti-Pattern 4: Brittle Mocks (Testing Implementation)

❌ **Bad** (test breaks when implementation details change):
```python
def test_order_processing():
    mock_db = Mock()

    service = OrderService(mock_db)
    service.process_order(123)

    # Brittle: assumes exact query string
    mock_db.execute.assert_called_with(
        "UPDATE orders SET status = ? WHERE id = ?",
        ("processed", 123)
    )
```

✅ **Good** (test behaviour, not implementation):
```python
def test_order_processing():
    fake_db = FakeDatabase()
    fake_db.insert(Order(id=123, status="pending"))

    service = OrderService(fake_db)
    service.process_order(123)

    # Test outcome, not how it's achieved
    order = fake_db.get_order(123)
    assert order.status == "processed"
```

## Australian English

All test names, comments, and documentation use **Australian English spelling**:
- ✅ normalise, organisation, authorisation, behaviour
- ❌ normalize, organization, authorization, behavior
