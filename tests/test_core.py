"""Unit tests for core module."""

import tempfile
import unittest
from datetime import datetime
from todo.core import TodoManager
from todo.storage import Storage


class TestTodoManager(unittest.TestCase):
    """Test cases for TodoManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = Storage(self.temp_file.name)
        self.manager = TodoManager(self.storage)
    
    def tearDown(self):
        """Clean up test fixtures."""
        import os
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task("Buy groceries")
        
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Buy groceries")
        self.assertFalse(task["completed"])
        self.assertIn("created_at", task)
    
    def test_add_multiple_tasks(self):
        """Test adding multiple tasks increments ID."""
        task1 = self.manager.add_task("Task 1")
        task2 = self.manager.add_task("Task 2")
        
        self.assertEqual(task1["id"], 1)
        self.assertEqual(task2["id"], 2)
    
    def test_list_tasks(self):
        """Test listing tasks."""
        self.manager.add_task("Task 1")
        self.manager.add_task("Task 2")
        
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]["description"], "Task 1")
        self.assertEqual(tasks[1]["description"], "Task 2")
    
    def test_list_tasks_empty(self):
        """Test listing tasks when empty."""
        tasks = self.manager.list_tasks()
        self.assertEqual(tasks, [])
    
    def test_complete_task(self):
        """Test marking task as complete."""
        task = self.manager.add_task("Task to complete")
        result = self.manager.complete_task(task["id"])
        
        self.assertTrue(result)
        updated_task = self.manager.get_task(task["id"])
        self.assertTrue(updated_task["completed"])
    
    def test_complete_task_invalid_id(self):
        """Test completing non-existent task."""
        result = self.manager.complete_task(999)
        self.assertFalse(result)
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = self.manager.add_task("Task to delete")
        result = self.manager.delete_task(task["id"])
        
        self.assertTrue(result)
        self.assertEqual(len(self.manager.list_tasks()), 0)
    
    def test_delete_task_invalid_id(self):
        """Test deleting non-existent task."""
        result = self.manager.delete_task(999)
        self.assertFalse(result)
    
    def test_get_task(self):
        """Test getting a specific task."""
        task = self.manager.add_task("Specific task")
        retrieved = self.manager.get_task(task["id"])
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["description"], "Specific task")
    
    def test_get_task_invalid_id(self):
        """Test getting non-existent task."""
        retrieved = self.manager.get_task(999)
        self.assertIsNone(retrieved)
    
    def test_task_persistence(self):
        """Test that tasks persist across manager instances."""
        self.manager.add_task("Persistent task")
        
        # Create new manager with same storage
        new_manager = TodoManager(self.storage)
        tasks = new_manager.list_tasks()
        
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Persistent task")
    
    def test_special_characters_in_description(self):
        """Test handling special characters in task description."""
        special_desc = "Task with 特殊字符 and émojis 🎉"
        task = self.manager.add_task(special_desc)
        
        self.assertEqual(task["description"], special_desc)
        retrieved = self.manager.get_task(task["id"])
        self.assertEqual(retrieved["description"], special_desc)


if __name__ == '__main__':
    unittest.main()
