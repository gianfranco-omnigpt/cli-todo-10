"""Integration tests for CLI commands."""

import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch
from todo.__main__ import main
from todo.storage import Storage


class TestCLI(unittest.TestCase):
    """Test cases for CLI interface."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Patch the Storage class to use our temp file
        self.storage_patcher = patch('todo.core.Storage')
        self.mock_storage_class = self.storage_patcher.start()
        self.mock_storage_class.return_value = Storage(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.storage_patcher.stop()
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def run_cli(self, args):
        """Helper to run CLI with arguments and capture output.
        
        Args:
            args: List of command-line arguments.
            
        Returns:
            Tuple of (stdout, stderr, exit_code)
        """
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        old_argv = sys.argv
        
        try:
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            sys.argv = ['todo'] + args
            
            exit_code = 0
            try:
                main()
            except SystemExit as e:
                exit_code = e.code
            
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            
            return stdout, stderr, exit_code
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.argv = old_argv
    
    def test_add_task(self):
        """Test adding a task via CLI."""
        stdout, _, exit_code = self.run_cli(['add', 'Buy groceries'])
        
        self.assertEqual(exit_code, 0)
        self.assertIn('Added task 1', stdout)
        self.assertIn('Buy groceries', stdout)
    
    def test_add_task_with_quotes(self):
        """Test adding a task with quoted description."""
        stdout, _, exit_code = self.run_cli(['add', '"Task with spaces"'])
        
        self.assertEqual(exit_code, 0)
        self.assertIn('Task with spaces', stdout)
    
    def test_add_task_no_description(self):
        """Test adding a task without description fails."""
        stdout, _, exit_code = self.run_cli(['add'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Error', stdout)
    
    def test_list_tasks_empty(self):
        """Test listing tasks when none exist."""
        stdout, _, exit_code = self.run_cli(['list'])
        
        self.assertEqual(exit_code, 0)
        self.assertIn('No tasks found', stdout)
    
    def test_list_tasks(self):
        """Test listing tasks."""
        self.run_cli(['add', 'Task 1'])
        self.run_cli(['add', 'Task 2'])
        
        stdout, _, exit_code = self.run_cli(['list'])
        
        self.assertEqual(exit_code, 0)
        self.assertIn('Task 1', stdout)
        self.assertIn('Task 2', stdout)
        self.assertIn('Tasks (2)', stdout)
    
    def test_complete_task(self):
        """Test marking task as complete."""
        self.run_cli(['add', 'Task to complete'])
        stdout, _, exit_code = self.run_cli(['done', '1'])
        
        self.assertEqual(exit_code, 0)
        self.assertIn('Task 1 marked as complete', stdout)
    
    def test_complete_task_invalid_id(self):
        """Test completing non-existent task."""
        stdout, _, exit_code = self.run_cli(['done', '999'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Task 999 not found', stdout)
    
    def test_complete_task_no_id(self):
        """Test completing task without ID."""
        stdout, _, exit_code = self.run_cli(['done'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Error', stdout)
    
    def test_complete_task_invalid_format(self):
        """Test completing task with non-numeric ID."""
        stdout, _, exit_code = self.run_cli(['done', 'abc'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Invalid task ID', stdout)
    
    def test_delete_task(self):
        """Test deleting a task."""
        self.run_cli(['add', 'Task to delete'])
        stdout, _, exit_code = self.run_cli(['delete', '1'])
        
        self.assertEqual(exit_code, 0)
        self.assertIn('Task 1 deleted', stdout)
    
    def test_delete_task_invalid_id(self):
        """Test deleting non-existent task."""
        stdout, _, exit_code = self.run_cli(['delete', '999'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Task 999 not found', stdout)
    
    def test_delete_task_no_id(self):
        """Test deleting task without ID."""
        stdout, _, exit_code = self.run_cli(['delete'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Error', stdout)
    
    def test_invalid_command(self):
        """Test using invalid command."""
        stdout, _, exit_code = self.run_cli(['invalid'])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Unknown command', stdout)
    
    def test_no_command(self):
        """Test running CLI without command."""
        stdout, _, exit_code = self.run_cli([])
        
        self.assertEqual(exit_code, 1)
        self.assertIn('Usage', stdout)
    
    def test_workflow(self):
        """Test complete workflow: add, list, complete, list, delete."""
        # Add tasks
        self.run_cli(['add', 'Task 1'])
        self.run_cli(['add', 'Task 2'])
        
        # List tasks
        stdout, _, _ = self.run_cli(['list'])
        self.assertIn('Task 1', stdout)
        self.assertIn('Task 2', stdout)
        
        # Complete task
        self.run_cli(['done', '1'])
        stdout, _, _ = self.run_cli(['list'])
        self.assertIn('✓', stdout)
        
        # Delete task
        self.run_cli(['delete', '2'])
        stdout, _, _ = self.run_cli(['list'])
        self.assertIn('Tasks (1)', stdout)
        self.assertNotIn('Task 2', stdout)


if __name__ == '__main__':
    unittest.main()
