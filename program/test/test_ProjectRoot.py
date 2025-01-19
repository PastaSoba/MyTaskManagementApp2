
import unittest
from unittest.mock import mock_open, patch
from uuid import uuid4
from datetime import date
from model.model import ProjectRoot, Project, Task
from model.status import TaskStatus
from model.priority import Priority

class TestProjectRoot(unittest.TestCase):
    def setUp(self):
        self.project_root = ProjectRoot()
        self.project = self.project_root.create_child()
        self.project.name = "Test Project"
        self.project.due = date.today()
        self.project.status = TaskStatus.TODO
        self.project.memo = "Test Memo"

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "123e4567-e89b-12d3-a456-426614174000", "name": "Test Project", "due": "2024-04-27", "status": "TODO", "memo": "Test Memo", "children": []}]')
    def test_load(self, mock_file):
        loaded_project_root = ProjectRoot.load()
        self.assertEqual(len(loaded_project_root.get_children()), 1)
        loaded_project = loaded_project_root.get_children()[0]
        self.assertEqual(loaded_project.name, "Test Project")
        self.assertEqual(loaded_project.due, date.fromisoformat("2024-04-27"))
        self.assertEqual(loaded_project.status, TaskStatus.TODO)
        self.assertEqual(loaded_project.memo, "Test Memo")

    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_file):
        self.project_root.save()
        expected_dict = [
            {
                "id": str(self.project.id),
                "name": "Test Project",
                "due": self.project.due.isoformat(),
                "status": self.project.status.value,
                "memo": "Test Memo",
                "children": []
            }
        ]
        mock_file.assert_called_with("data/project.json", "w")
        handle = mock_file()
        handle.write.assert_called_once_with(unittest.mock.ANY)
        written_data = handle.write.call_args[0][0]
        self.assertIn('"name": "Test Project"', written_data)
        self.assertIn('"status": "TODO"', written_data)

if __name__ == "__main__":
    unittest.main()