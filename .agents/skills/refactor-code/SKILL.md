---
name: python-refactor
description: "Refactor Python code to improve readability, maintainability, and follow PEP 8 standards. Use when: cleaning up legacy code, improving code quality, reducing complexity, or applying Python best practices."
---

# Python Code Refactoring

## Purpose
Refactor Python code to improve readability, maintainability, performance, and adherence to Python best practices (PEP 8, PEP 257). Transform messy or complex code into clean, idiomatic Python.

## When to Use
- ✅ Cleaning up legacy or poorly structured code
- ✅ Reducing code complexity (high cyclomatic complexity)
- ✅ Removing code duplication
- ✅ Improving naming conventions
- ✅ Applying Python idioms and best practices
- ✅ Splitting large functions or classes
- ✅ Improving error handling
- ✅ Optimizing performance bottlenecks

## When NOT to Use
- ❌ Production-critical code without tests (write tests first)
- ❌ Code that's working and doesn't need changes
- ❌ When requirements are unclear (clarify first)
- ❌ Major architectural changes (use design review instead)

---

## Pre-Conditions

Before refactoring:
1. **Tests exist** — Ensure existing functionality is covered by tests
2. **Understand the code** — Know what it does and why
3. **Version control** — Commit current state before refactoring
4. **Backup available** — Can revert if needed

---

## Refactoring Checklist

### 1. **Remove Unused Code**
- [ ] Remove unused imports
- [ ] Remove unused variables
- [ ] Remove commented-out code
- [ ] Remove dead code paths
- [ ] Remove duplicate code

### 2. **Improve Naming**
- [ ] Use descriptive variable names (`x` → `user_count`)
- [ ] Use snake_case for variables and functions
- [ ] Use PascalCase for classes
- [ ] Use UPPERCASE for constants
- [ ] Avoid abbreviations unless widely known

### 3. **Simplify Logic**
- [ ] Extract complex conditionals into named functions
- [ ] Replace nested ifs with early returns
- [ ] Use list/dict comprehensions where appropriate
- [ ] Simplify boolean expressions
- [ ] Remove unnecessary else after return

### 4. **Function Improvements**
- [ ] Functions should do one thing
- [ ] Keep functions under 20-30 lines
- [ ] Limit parameters (max 3-5)
- [ ] Add type hints
- [ ] Add docstrings

### 5. **Class Improvements**
- [ ] Follow Single Responsibility Principle
- [ ] Keep classes focused and cohesive
- [ ] Use @property for getters/setters
- [ ] Implement magic methods when appropriate
- [ ] Extract large classes into smaller ones

### 6. **Error Handling**
- [ ] Use specific exceptions (not bare `except:`)
- [ ] Add proper error messages
- [ ] Use context managers for resources
- [ ] Fail fast with clear error messages

### 7. **Code Organization**
- [ ] Group related functions
- [ ] Order: constants → classes → functions
- [ ] Keep imports organized (stdlib → third-party → local)
- [ ] Follow PEP 8 formatting

### 8. **Python Idioms**
- [ ] Use `with` for file/resource handling
- [ ] Use `enumerate()` instead of manual counters
- [ ] Use `zip()` for parallel iteration
- [ ] Use `in` for membership testing
- [ ] Use `get()` for dict lookups with defaults

---

## Refactoring Patterns

### Pattern 1: Extract Function
**Before:**
```python
def process_order(order):
    # Validate order
    if not order.get('items'):
        raise ValueError("No items")
    if order['total'] < 0:
        raise ValueError("Invalid total")
    
    # Calculate discount
    discount = 0
    if order['total'] > 100:
        discount = order['total'] * 0.1
    
    # Apply discount
    final_total = order['total'] - discount
    return final_total
```

**After:**
```python
def process_order(order: dict) -> float:
    """Process an order and return final total with discount."""
    _validate_order(order)
    discount = _calculate_discount(order['total'])
    return order['total'] - discount

def _validate_order(order: dict) -> None:
    """Validate order has required fields."""
    if not order.get('items'):
        raise ValueError("Order must contain items")
    if order['total'] < 0:
        raise ValueError("Order total cannot be negative")

def _calculate_discount(total: float) -> float:
    """Calculate discount for orders over $100."""
    return total * 0.1 if total > 100 else 0.0
```

### Pattern 2: Early Return (Reduce Nesting)
**Before:**
```python
def get_user_discount(user):
    if user:
        if user.is_active:
            if user.total_purchases > 1000:
                return 0.15
            else:
                return 0.05
        else:
            return 0
    else:
        return 0
```

**After:**
```python
def get_user_discount(user: dict) -> float:
    """Calculate user discount based on purchase history."""
    if not user or not user.get('is_active'):
        return 0.0
    
    if user.get('total_purchases', 0) > 1000:
        return 0.15
    
    return 0.05
```

### Pattern 3: List Comprehension
**Before:**
```python
def get_active_users(users):
    active = []
    for user in users:
        if user['active']:
            active.append(user['name'])
    return active
```

**After:**
```python
def get_active_users(users: list[dict]) -> list[str]:
    """Return names of all active users."""
    return [user['name'] for user in users if user.get('active')]
```

### Pattern 4: Use Context Manager
**Before:**
```python
def read_config():
    f = open('config.txt', 'r')
    data = f.read()
    f.close()
    return data
```

**After:**
```python
def read_config() -> str:
    """Read configuration from file."""
    with open('config.txt', 'r') as f:
        return f.read()
```

### Pattern 5: Replace Magic Numbers with Constants
**Before:**
```python
def calculate_tax(amount):
    if amount > 10000:
        return amount * 0.25
    return amount * 0.15
```

**After:**
```python
TAX_RATE_HIGH = 0.25
TAX_RATE_STANDARD = 0.15
TAX_THRESHOLD = 10000

def calculate_tax(amount: float) -> float:
    """Calculate tax based on amount."""
    rate = TAX_RATE_HIGH if amount > TAX_THRESHOLD else TAX_RATE_STANDARD
    return amount * rate
```

### Pattern 6: Use Dataclasses
**Before:**
```python
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age
    
    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, age={self.age})"
```

**After:**
```python
from dataclasses import dataclass

@dataclass
class User:
    """Represents a user in the system."""
    name: str
    email: str
    age: int
```

### Pattern 7: Dictionary get() with Default
**Before:**
```python
def get_setting(config, key):
    if key in config:
        return config[key]
    else:
        return 'default_value'
```

**After:**
```python
def get_setting(config: dict, key: str) -> str:
    """Retrieve setting from config with fallback."""
    return config.get(key, 'default_value')
```

### Pattern 8: Use Enumerate
**Before:**
```python
def print_items(items):
    index = 0
    for item in items:
        print(f"{index}: {item}")
        index += 1
```

**After:**
```python
def print_items(items: list) -> None:
    """Print items with their index."""
    for index, item in enumerate(items):
        print(f"{index}: {item}")
```

---

## Complexity Reduction

### Reduce Cyclomatic Complexity

**Before (Complexity: 8):**
```python
def process_payment(amount, method, user):
    if amount <= 0:
        return False
    if method == 'credit':
        if user.credit_limit > amount:
            if user.is_verified:
                return True
    elif method == 'debit':
        if user.balance > amount:
            return True
    elif method == 'paypal':
        if user.paypal_linked:
            return True
    return False
```

**After (Complexity: 3):**
```python
def process_payment(amount: float, method: str, user: User) -> bool:
    """Process payment based on method and user eligibility."""
    if amount <= 0:
        return False
    
    payment_validators = {
        'credit': lambda: user.credit_limit > amount and user.is_verified,
        'debit': lambda: user.balance > amount,
        'paypal': lambda: user.paypal_linked
    }
    
    validator = payment_validators.get(method)
    return validator() if validator else False
```

---

## Code Smell Detection

### Common Code Smells to Fix

#### 1. Long Functions (> 30 lines)
**Fix:** Extract into smaller functions

#### 2. Large Classes (> 200 lines)
**Fix:** Split into multiple classes

#### 3. Too Many Parameters (> 5)
**Fix:** Use dataclasses or config objects

#### 4. Duplicate Code
**Fix:** Extract common logic into functions

#### 5. Magic Numbers/Strings
**Fix:** Use named constants

#### 6. Deep Nesting (> 3 levels)
**Fix:** Use early returns, extract functions

#### 7. Commented-Out Code
**Fix:** Remove it (use version control)

#### 8. Generic Exception Handling
**Fix:** Catch specific exceptions

---

## PEP 8 Standards

### Key Rules
- Line length: max 79 characters (code), 72 (docstrings)
- Indentation: 4 spaces
- Imports: stdlib → third-party → local, alphabetically
- Blank lines: 2 before top-level functions/classes, 1 between methods
- Whitespace: no trailing whitespace
- Naming: snake_case (functions/variables), PascalCase (classes)

### Example Formatting

**Before:**
```python
import os,sys
from flask import Flask,request

class UserManager:
  def __init__(self,db):
      self.db=db
  def get_user(self,id):
        return self.db.query("SELECT * FROM users WHERE id=%s"%id)
```

**After:**
```python
import os
import sys

from flask import Flask, request


class UserManager:
    """Manages user database operations."""
    
    def __init__(self, db):
        self.db = db
    
    def get_user(self, user_id: int) -> dict:
        """Retrieve user by ID."""
        query = "SELECT * FROM users WHERE id=?"
        return self.db.query(query, (user_id,))
```

---

## Type Hints Best Practices

### Add Type Hints
```python
# Before
def calculate_total(items, tax_rate):
    return sum(items) * (1 + tax_rate)

# After
def calculate_total(items: list[float], tax_rate: float) -> float:
    """Calculate total with tax applied."""
    return sum(items) * (1 + tax_rate)
```

### Use typing Module
```python
from typing import Optional, Union, List, Dict

def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """Find user by ID, return None if not found."""
    ...
```

---

## Docstring Standards (PEP 257)

### Function Docstrings
```python
def calculate_discount(price: float, percentage: float) -> float:
    """
    Calculate discount amount.
    
    Args:
        price: Original price
        percentage: Discount percentage (0-100)
    
    Returns:
        Discount amount
    
    Raises:
        ValueError: If percentage is negative or > 100
    """
    if percentage < 0 or percentage > 100:
        raise ValueError("Percentage must be between 0 and 100")
    return price * (percentage / 100)
```

### Class Docstrings
```python
class ShoppingCart:
    """
    Manages items in a shopping cart.
    
    Attributes:
        items: List of items in cart
        total: Current cart total
    """
    pass
```

---

## Anti-Patterns to Avoid

### ❌ Mutable Default Arguments
```python
# BAD
def add_item(item, items=[]):
    items.append(item)
    return items

# GOOD
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### ❌ Bare Except
```python
# BAD
try:
    risky_operation()
except:
    pass

# GOOD
try:
    risky_operation()
except (IOError, ValueError) as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### ❌ String Concatenation in Loops
```python
# BAD
result = ""
for item in items:
    result += str(item)

# GOOD
result = "".join(str(item) for item in items)
```

---

## Validation After Refactoring

### Checklist
- [ ] All tests pass
- [ ] No new linting errors
- [ ] Type hints are valid (`mypy` passes)
- [ ] PEP 8 compliant (`flake8` or `black`)
- [ ] Docstrings added/updated
- [ ] Performance is same or better
- [ ] Code is more readable
- [ ] Complexity reduced

### Tools to Run
```bash
# Format code
black .

# Check style
flake8 .

# Type checking
mypy .

# Run tests
pytest

# Check complexity
radon cc . -a
```

---

## Example: Complete Refactoring

### Before
```python
def process(data):
    result=[]
    for i in range(len(data)):
        if data[i]['active']==True:
            x=data[i]['value']*1.1
            if x>100:
                result.append(x)
    return result
```

### After
```python
MARKUP_RATE = 1.1
MIN_THRESHOLD = 100

def process_active_items(data: list[dict]) -> list[float]:
    """
    Process active items and return values above threshold.
    
    Args:
        data: List of items with 'active' and 'value' fields
    
    Returns:
        List of processed values above minimum threshold
    """
    return [
        _apply_markup(item['value'])
        for item in data
        if _is_active(item) and _apply_markup(item['value']) > MIN_THRESHOLD
    ]

def _is_active(item: dict) -> bool:
    """Check if item is active."""
    return item.get('active', False)

def _apply_markup(value: float) -> float:
    """Apply markup rate to value."""
    return value * MARKUP_RATE
```

---

## Success Indicators

Refactoring is successful when:
- ✅ Code is easier to understand at first glance
- ✅ Functions are focused and single-purpose
- ✅ Naming clearly conveys intent
- ✅ No code duplication
- ✅ Tests still pass
- ✅ Complexity metrics improved
- ✅ Future changes will be easier

---

## Maintenance Notes

**When to update this skill:**
- New Python version with better idioms
- Team adopts new standards or tools
- Common refactoring patterns emerge
- PEP standards evolve