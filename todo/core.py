"""Core business logic for task management."""

from datetime import datetime
from typing import Dict, List, Optional, Any
from todo.storage import Storage


class TodoManager:
    """Manages task operations."""
    
    def __init__(self, storage: Storage = None):
        """Initialize TodoManager with storage.
        
        Args:
            storage: Storage instance. Creates default if None.
        """
        self.storage = storage if storage else Storage()
        self.data = self.storage.load()
    
    def add_task(self, description: str) -> Dict[str, Any]:
        """Add a new task.
        
        Args:
            description: Task description.
            
        Returns:
            The created task object.
        """
        task = {
            "id": self.data["next_id"],
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.data["tasks"].append(task)
        self.data["next_id"] += 1
        self.storage.save(self.data)
        
        return task
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """Get all tasks.
        
        Returns:
            List of all tasks.
        """
        return self.data["tasks"]
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as completed.
        
        Args:
            task_id: ID of the task to complete.
            
        Returns:
            True if task was found and marked complete, False otherwise.
        """
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                task["completed"] = True
                self.storage.save(self.data)
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete.
            
        Returns:
            True if task was found and deleted, False otherwise.
        """
        initial_length = len(self.data["tasks"])
        self.data["tasks"] = [task for task in self.data["tasks"] if task["id"] != task_id]
        
        if len(self.data["tasks"]) < initial_length:
            self.storage.save(self.data)
            return True
        return False
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific task by ID.
        
        Args:
            task_id: ID of the task to retrieve.
            
        Returns:
            Task object if found, None otherwise.
        """
        for task in self.data["tasks"]:
            if task["id"] == task_id:
                return task
        return None
