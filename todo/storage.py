"""Storage module for handling JSON file operations."""

import json
import os
from pathlib import Path
from typing import Dict, List, Any


class Storage:
    """Handles reading and writing tasks to JSON file."""
    
    def __init__(self, filepath: str = None):
        """Initialize storage with file path.
        
        Args:
            filepath: Path to JSON file. Defaults to ~/.todo.json
        """
        if filepath is None:
            filepath = os.path.join(Path.home(), ".todo.json")
        self.filepath = filepath
    
    def load(self) -> Dict[str, Any]:
        """Load tasks from JSON file.
        
        Returns:
            Dictionary containing tasks and next_id.
            Returns empty structure if file doesn't exist or is corrupted.
        """
        if not os.path.exists(self.filepath):
            return {"tasks": [], "next_id": 1}
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validate structure
                if not isinstance(data, dict) or "tasks" not in data or "next_id" not in data:
                    print("Warning: Corrupted data file. Resetting to empty state.")
                    return {"tasks": [], "next_id": 1}
                return data
        except json.JSONDecodeError:
            print("Warning: Corrupted JSON file. Resetting to empty state.")
            return {"tasks": [], "next_id": 1}
        except PermissionError:
            print(f"Error: Permission denied reading {self.filepath}")
            return {"tasks": [], "next_id": 1}
        except Exception as e:
            print(f"Error reading file: {e}")
            return {"tasks": [], "next_id": 1}
    
    def save(self, data: Dict[str, Any]) -> bool:
        """Save tasks to JSON file.
        
        Args:
            data: Dictionary containing tasks and next_id.
            
        Returns:
            True if save was successful, False otherwise.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: Permission denied writing to {self.filepath}")
            return False
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
