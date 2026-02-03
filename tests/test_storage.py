"""Unit tests for storage module."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from todo.storage import Storage


class TestStorage(unittest.TestCase):
    """Test cases for Storage class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = Storage(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_load_nonexistent_file(self):
        """Test loading from non-existent file returns empty structure."""
        os.unlink(self.temp_file.name)
        data = self.storage.load()
        self.assertEqual(data, {"tasks": [], "next_id": 1})
    
    def test_save_and_load(self):
        """Test saving and loading data."""
        test_data = {
            "tasks": [
                {
                    "id": 1,
                    "description": "Test task",
                    "completed": False,
                    "created_at": "2024-01-15T10:30:00"
                }
            ],
            "next_id": 2
        }
        
        result = self.storage.save(test_data)
        self.assertTrue(result)
        
        loaded_data = self.storage.load()
        self.assertEqual(loaded_data, test_data)
    
    def test_load_corrupted_json(self):
        """Test loading corrupted JSON returns empty structure."""
        with open(self.temp_file.name, 'w') as f:
            f.write("not valid json {{{")
        
        data = self.storage.load()
        self.assertEqual(data, {"tasks": [], "next_id": 1})
    
    def test_load_invalid_structure(self):
        """Test loading invalid data structure returns empty structure."""
        with open(self.temp_file.name, 'w') as f:
            json.dump({"invalid": "structure"}, f)
        
        data = self.storage.load()
        self.assertEqual(data, {"tasks": [], "next_id": 1})
    
    def test_save_creates_directory(self):
        """Test that save creates parent directory if it doesn't exist."""
        nested_path = os.path.join(tempfile.gettempdir(), "test_todo_dir", "todo.json")
        storage = Storage(nested_path)
        
        test_data = {"tasks": [], "next_id": 1}
        result = storage.save(test_data)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(nested_path))
        
        # Cleanup
        os.unlink(nested_path)
        os.rmdir(os.path.dirname(nested_path))


if __name__ == '__main__':
    unittest.main()
