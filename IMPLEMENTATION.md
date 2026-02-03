# Implementation Documentation

## Overview
This document provides detailed information about the implementation of the CLI ToDo application.

## Project Structure

```
cli-todo-10/
├── todo/                    # Main application package
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # CLI entry point and command parser
│   ├── core.py             # Business logic (TodoManager)
│   └── storage.py          # JSON file operations (Storage)
├── tests/                   # Test suite
│   ├── __init__.py         # Test package initialization
│   ├── test_storage.py     # Storage layer tests
│   ├── test_core.py        # Core logic tests
│   └── test_cli.py         # CLI integration tests
├── README.md               # Project documentation
├── IMPLEMENTATION.md       # This file
├── setup.py               # Package installation script
├── requirements.txt       # Dependencies (none - stdlib only)
└── .gitignore            # Git ignore rules

```

## Module Details

### 1. Storage Module (`todo/storage.py`)

**Purpose:** Handles all file I/O operations for persisting tasks.

**Key Features:**
- Reads and writes JSON data to `~/.todo.json`
- Handles corrupted JSON gracefully
- Creates parent directories if needed
- Provides clear error messages for file permission issues

**Class: Storage**
- `__init__(filepath)`: Initialize with custom or default file path
- `load()`: Load tasks from JSON file, returns empty structure on error
- `save(data)`: Save tasks to JSON file, returns boolean success indicator

**Error Handling:**
- Corrupted JSON → Warning message, returns empty structure
- Missing file → Returns empty structure (not an error)
- Permission errors → Clear error message, graceful degradation

### 2. Core Module (`todo/core.py`)

**Purpose:** Implements business logic for task management.

**Key Features:**
- Task creation with auto-incrementing IDs
- Task listing, completion, and deletion
- Data persistence through Storage layer
- ISO 8601 timestamp generation

**Class: TodoManager**
- `__init__(storage)`: Initialize with Storage instance
- `add_task(description)`: Create new task, returns task object
- `list_tasks()`: Return all tasks
- `complete_task(task_id)`: Mark task complete, returns success boolean
- `delete_task(task_id)`: Remove task, returns success boolean
- `get_task(task_id)`: Retrieve specific task by ID

**Design Decisions:**
- Auto-incrementing IDs ensure uniqueness
- Tasks are never truly "archived" - only deleted
- Completed tasks remain in the list (allows users to track history)
- Storage operations happen immediately (no buffering)

### 3. CLI Module (`todo/__main__.py`)

**Purpose:** Command-line interface and argument parsing.

**Key Features:**
- Simple command syntax (add, list, done, delete)
- Clear error messages
- Usage help
- Quote handling for task descriptions

**Functions:**
- `main()`: Entry point, parses commands and calls TodoManager
- `print_usage()`: Display help information
- `format_task(task)`: Format task for display with checkmark

**Command Format:**
```bash
python -m todo add "Description"   # Add task
python -m todo list                # List all tasks
python -m todo done <id>           # Complete task
python -m todo delete <id>         # Delete task
```

**Error Handling:**
- Invalid command → Usage help + error message
- Missing arguments → Specific error message
- Invalid task ID → "Task not found" message
- Non-numeric ID → "Invalid task ID" message

## Data Model

### Task Object
```json
{
  "id": 1,                              // Auto-incrementing integer
  "description": "Buy groceries",        // User-provided string
  "completed": false,                    // Boolean status
  "created_at": "2024-01-15T10:30:00"   // ISO 8601 timestamp
}
```

### Storage File Structure
```json
{
  "tasks": [                // Array of task objects
    { /* task 1 */ },
    { /* task 2 */ }
  ],
  "next_id": 3             // Next ID to assign
}
```

## Testing Strategy

### Unit Tests (`test_storage.py`)
- Load from non-existent file
- Save and load data
- Corrupted JSON handling
- Invalid data structure handling
- Directory creation
- File permissions

### Unit Tests (`test_core.py`)
- Add single task
- Add multiple tasks
- List tasks (empty and populated)
- Complete task (valid and invalid IDs)
- Delete task (valid and invalid IDs)
- Get task by ID
- Data persistence across instances
- Special characters in descriptions

### Integration Tests (`test_cli.py`)
- All CLI commands
- Error conditions
- Edge cases
- Complete workflow scenarios
- Quote handling
- Invalid input validation

**Test Coverage:**
- All core functions tested
- Error paths validated
- Edge cases covered
- Integration tests ensure components work together

## Performance Considerations

**Target: Operations complete in <100ms**

Current implementation meets this target because:
- JSON file operations are fast for small datasets
- No network calls
- Minimal processing (simple list operations)
- Data loaded once per command execution

**Scalability Notes:**
- Current design suitable for personal use (hundreds of tasks)
- For thousands of tasks, consider:
  - Database backend (SQLite)
  - Pagination for list command
  - Lazy loading

## Security Considerations

1. **File Permissions:**
   - User's home directory (~/.todo.json)
   - Standard file permissions apply
   - No sensitive data stored

2. **Input Validation:**
   - Task IDs validated (must be integers)
   - Descriptions accepted as-is (user's own data)
   - No code execution risks

3. **Error Handling:**
   - No stack traces exposed to users
   - Clear error messages without sensitive info
   - Graceful degradation on file errors

## Code Quality

**Standards Followed:**
- PEP 8 style guide
- Type hints for function signatures
- Comprehensive docstrings
- Clear variable names
- Single Responsibility Principle
- DRY (Don't Repeat Yourself)

**Best Practices:**
- Separation of concerns (Storage, Core, CLI)
- Dependency injection (Storage passed to TodoManager)
- Testability (mocking support)
- Error handling at appropriate layers
- User-friendly error messages

## Installation and Usage

### Installation
```bash
# Clone repository
git clone https://github.com/gianfranco-omnigpt/cli-todo-10.git
cd cli-todo-10

# Install in development mode
pip install -e .
```

### Usage Examples
```bash
# Add tasks
todo add "Buy groceries"
todo add "Write documentation"

# List all tasks
todo list

# Complete a task
todo done 1

# Delete a task
todo delete 2
```

### Running Tests
```bash
# All tests
python -m unittest discover tests

# Specific test module
python -m unittest tests.test_core

# With verbose output
python -m unittest discover tests -v
```

## Future Enhancements (Out of Scope)

While not implemented in this version, potential enhancements include:
- Due dates and reminders
- Task priorities
- Categories/tags
- Search functionality
- Undo/redo operations
- Export to other formats
- Cloud synchronization
- Multi-user support

## Dependencies

**Runtime:** None - Python 3.8+ standard library only

**Development:**
- unittest (included in stdlib)
- setuptools (for installation)

This design choice ensures:
- Easy installation
- No dependency conflicts
- Fast execution
- Minimal security surface