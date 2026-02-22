# Learning Guide - Python

> **Welcome to Service-Track Week 1, Task 7!**
> This is a **learning task**. This guide teaches you the Python concepts you need and tells you exactly where to look and what to fix. Take your time and read carefully.

---

## What You Need To Do (Summary)

1. **Read** `TICKET.md` to understand the task
2. **Read** this guide to learn the Python syntax you'll need
3. **Find the bugs** in the `src/` files (look for `// BUG:` or `# BUG:` comments)
4. **Fix the bugs** using what you learned
5. **Run the tests** to verify your fix: `python -m pytest tests/ -v`
6. **Add new tests** in the `tests/` folder to prove your fix works

---

## Python Quick Reference

### Variables and Types
```python
name = "Alice"              # string
count = 42                  # integer
price = 19.99               # float
items = [1, 2, 3]           # list (ordered, mutable)
config = {"key": "value"}   # dictionary (key-value pairs)
is_active = True            # boolean (True/False, capital first letter)
```

### Functions
```python
def greet(name, greeting="Hello"):
    """This is a docstring - describes what the function does."""
    return f"{greeting}, {name}!"

# Calling it:
result = greet("Alice")            # Uses default greeting
result = greet("Bob", "Hi")        # Custom greeting
```

### Classes
```python
class Calculator:
    def __init__(self):           # Constructor - runs when you create an object
        self.history = []         # 'self' refers to the current object

    def add(self, a, b):          # Method - a function inside a class
        result = a + b
        self.history.append(result)
        return result

    def get_history(self):
        return self.history

# Using it:
calc = Calculator()               # Create an object
calc.add(2, 3)                    # Call a method
print(calc.get_history())         # [5]
```

### Dictionaries (Key-Value Storage)
```python
user = {"name": "Alice", "age": 25}
user["name"]                      # Access: "Alice"
user.get("email", "N/A")          # Safe access with default: "N/A"
user["email"] = "alice@test.com"   # Add/update a key
"name" in user                    # Check if key exists: True
```

### Lists
```python
items = [1, 2, 3]
items.append(4)                   # Add to end: [1, 2, 3, 4]
items.pop()                       # Remove last: [1, 2, 3]
len(items)                        # Length: 3
for item in items:                # Loop through items
    print(item)
```

### Error Handling
```python
try:
    result = risky_operation()
except ValueError as e:           # Catch specific error
    print(f"Bad value: {e}")
except Exception as e:            # Catch any error
    print(f"Error: {e}")
finally:                          # Always runs
    cleanup()
```

### Common Patterns You'll See
```python
# Check if something is None (null)
if value is None:
    return "No value"

# Check if something is falsy (None, 0, "", [], {})
if not value:
    return "Empty"

# String formatting (f-strings)
name = "Alice"
print(f"Hello, {name}!")          # "Hello, Alice!"

# Importing modules
from collections import defaultdict
import json
```

### How to Run Tests
```bash
# From the task folder:
python -m pytest tests/ -v

# Run a specific test:
python -m pytest tests/test_file.py::TestClass::test_name -v
```

### How to Add a Test
```python
# In the test file, add a new method starting with 'test_':
class TestMyFeature:
    def test_something_specific(self):
        obj = MyClass()
        result = obj.method(input_data)
        assert result == expected_value    # Check equality
        assert result is not None          # Check not None
        assert len(result) > 0            # Check not empty
```

---

## Project Structure

| File | Purpose |
|------|---------|
| `TICKET.md` | Your task assignment - **read this first!** |
| `src/escalationEngine.py` | Main source code - **has bugs to fix** |
| `src/slaTracker.py` | Supporting code - **may also have bugs** |
| `tests/test_escalationEngine.py` | Test file - **add your tests here** |
| `docs/DESIGN.md` | Architecture decisions (background reading) |
| `docs/GUIDE.md` | This learning guide |
| `.context/` | Meeting notes and PR comments (background context) |

---

## Where to Look and What to Fix

### Bug #1 - in `src/slaTracker.py` (around line 112)
**What's wrong:** Uses elapsed > target * warning_percent

**How to find it:** Open `src/slaTracker.py` and look for the `BUG:` comment near line 112. Read the comment carefully - it describes exactly what's broken.

**Hint:** Think about what the correct behavior should be (described in `TICKET.md` under Requirements), then compare it to what the code actually does.

### Bug #2 - in `src/slaTracker.py` (around line 145)
**What's wrong:** Compliance rate denominator uses total tickets instead of resolved tickets

**How to find it:** Open `src/slaTracker.py` and look for the `BUG:` comment near line 145. Read the comment carefully - it describes exactly what's broken.

**Hint:** Think about what the correct behavior should be (described in `TICKET.md` under Requirements), then compare it to what the code actually does.


---

## Step-by-Step Workflow

1. Open a terminal and navigate to this task folder
2. Read `TICKET.md` completely
3. Open `src/` files and find the `BUG:` comments
4. Fix each bug (the comment tells you what's wrong)
5. Run the tests:
   ```bash
   python -m pytest tests/ -v
   ```
6. If tests pass, you're done with the fix
7. **Bonus:** Add a new test to `tests/` that specifically tests the bug you fixed

---

## Common Mistakes to Avoid

- Don't change the function signatures (method names, parameters) - only fix the logic inside
- Don't delete the `BUG:` comments - they help reviewers understand what you changed
- Make sure all existing tests still pass after your changes
- If you're stuck, re-read the `TICKET.md` requirements section carefully
