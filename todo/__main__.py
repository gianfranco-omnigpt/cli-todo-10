"""CLI entry point and command parser."""

import sys
from todo.core import TodoManager


def print_usage():
    """Print usage information."""
    print("Usage:")
    print('  python -m todo add "Task description"  - Add a new task')
    print('  python -m todo list                    - List all tasks')
    print('  python -m todo done <id>               - Mark task as complete')
    print('  python -m todo delete <id>             - Delete a task')


def format_task(task):
    """Format a task for display.
    
    Args:
        task: Task dictionary.
        
    Returns:
        Formatted string representation of the task.
    """
    status = "✓" if task["completed"] else " "
    return f"[{status}] {task['id']}. {task['description']}"


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    manager = TodoManager()
    
    if command == "add":
        if len(sys.argv) < 3:
            print('Error: Please provide a task description')
            print('Usage: python -m todo add "Task description"')
            sys.exit(1)
        
        # Join all remaining arguments as the description
        description = ' '.join(sys.argv[2:])
        # Remove quotes if present
        if description.startswith('"') and description.endswith('"'):
            description = description[1:-1]
        elif description.startswith("'") and description.endswith("'"):
            description = description[1:-1]
        
        task = manager.add_task(description)
        print(f"Added task {task['id']}: {task['description']}")
    
    elif command == "list":
        tasks = manager.list_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print(f"Tasks ({len(tasks)}):")
            for task in tasks:
                print(f"  {format_task(task)}")
    
    elif command == "done":
        if len(sys.argv) < 3:
            print('Error: Please provide a task ID')
            print('Usage: python -m todo done <id>')
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid task ID '{sys.argv[2]}'. Must be a number.")
            sys.exit(1)
        
        if manager.complete_task(task_id):
            print(f"Task {task_id} marked as complete.")
        else:
            print(f"Error: Task {task_id} not found.")
            sys.exit(1)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print('Error: Please provide a task ID')
            print('Usage: python -m todo delete <id>')
            sys.exit(1)
        
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid task ID '{sys.argv[2]}'. Must be a number.")
            sys.exit(1)
        
        if manager.delete_task(task_id):
            print(f"Task {task_id} deleted.")
        else:
            print(f"Error: Task {task_id} not found.")
            sys.exit(1)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
