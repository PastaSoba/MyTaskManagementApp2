import unittest
from uuid import UUID, uuid4
from datetime import date
from model.model import Task, TaskStatus, Priority

class TestTask(unittest.TestCase):
    
    def setUp(self):
        self.task_id = uuid4()
        self.task = Task(_id=self.task_id)
        self.task.name = "Test Task"
        self.task.due = date(2023, 12, 31)
        self.task.status = TaskStatus.PROGRESS
        self.task.memo = "This is a test task."
        self.task.assignee = "John Doe"
        self.task.estimation = "5h"
        self.task.priority = Priority.EMERGENCY_IMPORTANT

    def test_initialization(self):
        self.assertEqual(self.task.id, self.task_id)
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.due, date(2023, 12, 31))
        self.assertEqual(self.task.status, TaskStatus.PROGRESS)
        self.assertEqual(self.task.memo, "This is a test task.")
        self.assertEqual(self.task.assignee, "John Doe")
        self.assertEqual(self.task.estimation, "5h")
        self.assertEqual(self.task.priority, Priority.EMERGENCY_IMPORTANT)
        self.assertEqual(self.task.get_children(), [])

    def test_restore_from_dict(self):
        dict_obj = {
            "id": str(self.task_id),
            "name": "Restored Task",
            "due": "2023-11-30",
            "status": "TODO",
            "memo": "Restored memo",
            "assignee": "Jane Doe",
            "estimation": "3h",
            "priority": "3: Emergency",
            "children": []
        }
        restored_task = Task.restore_from_dict(dict_obj)
        self.assertEqual(restored_task.id, self.task_id)
        self.assertEqual(restored_task.name, "Restored Task")
        self.assertEqual(restored_task.due, date(2023, 11, 30))
        self.assertEqual(restored_task.status, TaskStatus.TODO)
        self.assertEqual(restored_task.memo, "Restored memo")
        self.assertEqual(restored_task.assignee, "Jane Doe")
        self.assertEqual(restored_task.estimation, "3h")
        self.assertEqual(restored_task.priority, Priority.EMERGENCY)
        self.assertEqual(restored_task.get_children(), [])

    def test_export_as_dict(self):
        export_dict = self.task.export_as_dict()
        expected_dict = {
            "id": str(self.task_id),
            "name": "Test Task",
            "due": "2023-12-31",
            "status": self.task.status.value,
            "memo": "This is a test task.",
            "assignee": "John Doe",
            "estimation": "5h",
            "priority": self.task.priority.value,
            "children": []
        }
        self.assertEqual(export_dict, expected_dict)

    def test_create_child(self):
        child_task = self.task.create_child()
        self.assertIn(child_task, self.task.get_children())
        self.assertIsInstance(child_task, Task)

    def test_delete_child(self):
        child_task = self.task.create_child()
        self.task.delete_child(child_task.id)
        self.assertNotIn(child_task, self.task.get_children())
        with self.assertRaises(ValueError):
            self.task.delete_child(child_task.id)

if __name__ == "__main__":
    unittest.main()