# Test Coverage Analysis Guide

Comprehensive guide for understanding, analyzing, and improving test coverage.

## Coverage Metrics

### Line Coverage

**Definition**: Percentage of code lines executed by tests.

**Example**:
```python
def divide(a, b):
    if b == 0:          # Line 1
        raise ValueError("Cannot divide by zero")  # Line 2
    return a / b        # Line 3

# Test only happy path
def test_divide():
    assert divide(10, 2) == 5  # Executes lines 1, 3 (skips line 2)

# Coverage: 66% (2/3 lines)
```

**To achieve 100% line coverage**: Add test for division by zero:
```python
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)  # Executes all lines

# Coverage: 100% (3/3 lines)
```

### Branch Coverage

**Definition**: Percentage of decision branches (if/else, try/except) executed by tests.

**Example**:
```python
def get_discount(price, is_member):
    if is_member:        # Branch point
        return price * 0.9  # Branch 1 (True)
    else:
        return price        # Branch 2 (False)

# Test only member case
def test_member_discount():
    assert get_discount(100, True) == 90  # Covers branch 1 only

# Branch coverage: 50% (1/2 branches)
```

**To achieve 100% branch coverage**: Add test for non-member case:
```python
def test_no_discount_for_non_members():
    assert get_discount(100, False) == 100  # Covers branch 2

# Branch coverage: 100% (2/2 branches)
```

### Function Coverage

**Definition**: Percentage of functions called by tests.

**Example**:
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

# Test only add function
def test_add():
    assert add(2, 3) == 5

# Function coverage: 50% (1/2 functions)
```

## Coverage Targets

### Minimum: 80% Line Coverage

**Why 80% minimum**:
- Ensures majority of code is tested
- Catches most common bugs
- Balances thoroughness with effort
- Industry standard for production code

**What 80% means**:
- 80% of code lines executed by tests
- NOT that code is 80% bug-free
- NOT that all critical paths are tested

**When to accept <80%**:
- Generated code (migrations, auto-generated files)
- Deprecated code (scheduled for removal)
- Prototype/spike code (not production)

### Target: 90%+ Line Coverage

**Why aim for 90%+**:
- Higher confidence in code correctness
- Fewer bugs escape to production
- Easier to refactor with confidence
- Better documentation through tests

**How to achieve 90%+**:
- Test all acceptance criteria (unit + integration)
- Test edge cases and error scenarios
- Test recently added code thoroughly
- Prioritize critical paths

### Critical Code: 100% Coverage

**What needs 100% coverage**:
- Security-critical code (authentication, authorization)
- Financial transactions
- Data loss scenarios
- Core business logic

**Example**:
```python
def charge_credit_card(amount, card):
    """Critical: Financial transaction must be 100% tested."""
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if not card.is_valid():
        raise InvalidCardError("Card is invalid")
    if card.balance < amount:
        raise InsufficientFundsError("Insufficient funds")

    transaction = create_transaction(amount, card)
    card.balance -= amount
    return transaction

# Must test ALL scenarios:
# - Valid transaction
# - Negative/zero amount
# - Invalid card
# - Insufficient funds
# - Edge cases (exactly card.balance, very large amount)
```

## Reading Coverage Reports

### pytest-cov Output

```bash
$ pytest --cov=src tests/

---------- coverage: platform linux, python 3.11 -----------
Name                     Stmts   Miss  Cover
--------------------------------------------
src/search/service.py       45      5    89%
src/search/query.py         32      8    75%
src/auth/service.py         28      2    93%
src/api/routes.py           56     12    79%
--------------------------------------------
TOTAL                      161     27    83%
```

**Interpreting results**:
- **Stmts**: Total statements (lines) in file
- **Miss**: Statements not covered by tests
- **Cover**: Coverage percentage

**Red flags**:
- ❌ `src/search/query.py: 75%` - Below 80% minimum
- ❌ `src/api/routes.py: 79%` - Just below 80%, needs improvement

**Good coverage**:
- ✅ `src/auth/service.py: 93%` - Above 90% target
- ✅ `src/search/service.py: 89%` - Close to 90% target

### HTML Coverage Report

```bash
$ pytest --cov=src --cov-report=html tests/
$ open htmlcov/index.html
```

**Benefits of HTML report**:
- Visual highlighting of uncovered lines (red)
- Covered lines (green)
- Partial coverage (yellow)
- Click through to see exact lines missing

**Example HTML report interpretation**:

```python
def search(query, filters=None):
    if not query:                       # ✅ Green (covered)
        raise ValueError("Empty query") # ❌ Red (not covered)

    results = db.query(query)           # ✅ Green (covered)

    if filters:                         # ⚠️ Yellow (partial - only True branch)
        results = apply_filters(results, filters)  # ✅ Green

    return results                      # ✅ Green
```

**Coverage gaps**:
1. Line 2: Exception not tested (need test for empty query)
2. Line 6: Else branch not tested (need test without filters)

## Identifying Coverage Gaps

### Strategy 1: Review Coverage Report

**Steps**:
1. Generate HTML coverage report
2. Open report in browser
3. Sort files by coverage (lowest first)
4. Click on files with <80% coverage
5. Identify red/yellow lines
6. Write tests for uncovered code

**Example**:
```bash
# Generate report
pytest --cov=src --cov-report=html tests/

# Open report (highlights uncovered lines in red)
open htmlcov/src/search/service.py.html
```

### Strategy 2: Coverage by Module

**Check coverage by module**:
```bash
$ pytest --cov=src --cov-report=term-missing tests/

Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
src/search/service.py       45      5    89%   12-14, 23, 45
src/search/query.py         32      8    75%   5, 18-25
```

**Interpreting "Missing" column**:
- `12-14`: Lines 12, 13, 14 not covered (range)
- `23`: Line 23 not covered (single line)
- `45`: Line 45 not covered (single line)

**Action**: Review those line numbers in code, write tests to cover them.

### Strategy 3: Branch Coverage Analysis

**Check branch coverage**:
```bash
$ pytest --cov=src --cov-report=term:skip-covered --cov-branch tests/
```

**Flags**:
- `--cov-branch`: Include branch coverage (if/else)
- `--cov-report=term:skip-covered`: Only show files with <100% coverage

**Example output**:
```
Name                   Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
src/auth/service.py       28      2     12      3    87%
```

**Interpreting branch coverage**:
- **Branch**: Total branches (if/else, try/except)
- **BrPart**: Partially covered branches (only one path tested)
- **Cover**: Overall coverage including branches

**Action**: Find branches with BrPart > 0, write tests for untested paths.

## Improving Coverage Strategically

### Priority 1: Critical Code to 100%

**Identify critical code**:
- Authentication/authorisation
- Payment processing
- Data deletion/modification
- Security-sensitive operations

**Ensure 100% coverage**:
```python
# Critical: User authentication
def authenticate_user(email, password):
    user = get_user_by_email(email)

    if not user:
        raise UserNotFoundError("User not found")  # Must test

    if not verify_password(password, user.password_hash):
        log_failed_login_attempt(user)
        raise AuthenticationError("Invalid credentials")  # Must test

    if user.is_locked:
        raise AccountLockedError("Account is locked")  # Must test

    return create_session(user)  # Must test

# All scenarios MUST be tested:
def test_authenticate_success(): ...
def test_authenticate_user_not_found(): ...
def test_authenticate_invalid_password(): ...
def test_authenticate_account_locked(): ...
```

### Priority 2: Files Below 80% to 80%+

**Identify files below 80%**:
```bash
pytest --cov=src --cov-report=term tests/ | grep -E "[0-7][0-9]%"
```

**Focus on low-hanging fruit**:
- Simple getter/setter methods
- Error handling paths
- Edge cases (empty input, null values)

**Example**:
```python
# Coverage: 75% (3/4 lines covered)
def get_user_display_name(user):
    if user.display_name:
        return user.display_name  # ✅ Tested
    return user.email  # ❌ Not tested

# Add simple test to reach 100%:
def test_get_display_name_defaults_to_email():
    user = User(email="alice@example.com", display_name=None)
    assert get_user_display_name(user) == "alice@example.com"
```

### Priority 3: New Code to 90%+

**Ensure all new code has high coverage**:
- Every new function: test happy path + edge cases + errors
- Every new class: test public methods
- Every new module: aim for 90%+ coverage

**Pre-commit hook** (prevent low-coverage commits):
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run tests with coverage
pytest --cov=src --cov-report=term-missing tests/ --cov-fail-under=80

if [ $? -ne 0 ]; then
    echo "❌ Coverage below 80%. Commit blocked."
    exit 1
fi
```

### Priority 4: Refactor Untestable Code

**Signs of untestable code**:
- Hard to mock (tightly coupled dependencies)
- Global state (singletons, global variables)
- Side effects (file I/O, network calls) mixed with logic
- No clear input/output

**Refactoring for testability**:

**Before** (hard to test):
```python
def process_order():
    # Tightly coupled to database
    db = Database()
    db.connect()
    order = db.get_order(123)

    # Mixed logic and side effects
    total = sum(item.price for item in order.items)
    if total > 100:
        send_email(order.customer.email, "Order confirmed")  # Hard to test

    db.update_order(order, status="processed")
```

**After** (testable):
```python
def calculate_order_total(items):
    """Pure function - easy to test."""
    return sum(item.price for item in items)

def should_send_confirmation(total):
    """Pure function - easy to test."""
    return total > 100

def process_order(order, db, email_service):
    """Dependencies injected - easy to mock."""
    total = calculate_order_total(order.items)

    if should_send_confirmation(total):
        email_service.send(order.customer.email, "Order confirmed")

    db.update_order(order, status="processed")

# Tests are now straightforward:
def test_calculate_order_total():
    items = [Item(price=50), Item(price=60)]
    assert calculate_order_total(items) == 110

def test_should_send_confirmation():
    assert should_send_confirmation(101) == True
    assert should_send_confirmation(99) == False

def test_process_order():
    mock_db = Mock()
    mock_email = Mock()
    order = Order(items=[Item(price=150)], customer=Customer(email="a@ex.com"))

    process_order(order, mock_db, mock_email)

    mock_email.send.assert_called_once_with("a@ex.com", "Order confirmed")
    mock_db.update_order.assert_called_once()
```

## Coverage Anti-Patterns

### Anti-Pattern 1: Testing Implementation, Not Behaviour

❌ **Bad** (test breaks when implementation changes):
```python
def test_search_calls_database_query():
    service = SearchService(mock_db)
    service.search("python")

    # Testing HOW (implementation)
    mock_db.query.assert_called_with("SELECT * FROM docs WHERE title LIKE ?", "%python%")
```

✅ **Good** (test behaviour, not implementation):
```python
def test_search_returns_matching_results():
    service = SearchService(real_test_db)
    results = service.search("python")

    # Testing WHAT (behaviour)
    assert all("python" in r.title.lower() for r in results)
```

### Anti-Pattern 2: Chasing 100% Coverage Blindly

❌ **Bad** (testing getters/setters for coverage):
```python
def test_user_name_getter():
    user = User(name="alice")
    assert user.name == "alice"  # Pointless test

def test_user_name_setter():
    user = User()
    user.name = "alice"
    assert user.name == "alice"  # Pointless test
```

✅ **Good** (test meaningful behaviour):
```python
def test_user_validation_requires_name():
    user = User(name="")
    with pytest.raises(ValidationError, match="Name is required"):
        user.validate()
```

### Anti-Pattern 3: Not Testing Edge Cases

❌ **Bad** (only happy path):
```python
def test_divide():
    assert divide(10, 2) == 5  # Only tests happy path
```

✅ **Good** (test edge cases and errors):
```python
def test_divide_success():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_negative_numbers():
    assert divide(-10, 2) == -5
    assert divide(10, -2) == -5
```

## Coverage in PR Reviews

**Reviewer checklist**:
- [ ] Overall coverage ≥80% (check CI output)
- [ ] New code coverage ≥90% (check coverage report)
- [ ] Critical code coverage = 100% (security, finance, data loss)
- [ ] All ACs have corresponding tests
- [ ] Tests include edge cases and error scenarios

**If coverage <80%**:
```bash
gh pr review 42 --request-changes -b "Coverage is 78%, below 80% minimum.

Please add tests for:
- src/search/query.py lines 18-25 (error handling)
- src/api/routes.py lines 45-48 (validation)

Run: pytest --cov=src --cov-report=html tests/
Then open: htmlcov/index.html to see uncovered lines."
```

**If coverage ≥80% but quality concerns**:
```bash
gh pr review 42 --request-changes -b "Coverage is 85%, but tests only cover happy path.

Please add tests for:
- Empty query handling
- Invalid input validation
- Timeout scenarios

See testing skill: test-strategy.md for edge case checklist."
```

## Australian English

All test names, comments, and documentation use **Australian English spelling**:
- ✅ normalise, organisation, authorisation, behaviour
- ❌ normalize, organization, authorization, behavior
