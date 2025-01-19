import unittest
from uuid import uuid4
from datetime import date
from model.model import Project
from model.status import TaskStatus

class TestProject(unittest.TestCase):
    def setUp(self):
        self.project_id = uuid4()
        self.project = Project(_id=self.project_id)
        self.project.name = "Test Project"
        self.project.due = date.today()
        self.project.status = TaskStatus.TODO
        self.project.memo = "Test Memo"

    def test_initialization(self):
        self.assertEqual(self.project.id, self.project_id)
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.due, date.today())
        self.assertEqual(self.project.status, TaskStatus.TODO)
        self.assertEqual(self.project.memo, "Test Memo")

    def test_restore_from_dict(self):
        project_dict = self.project.export_as_dict()
        restored_project = Project.restore_from_dict(project_dict)
        self.assertEqual(restored_project.id, self.project.id)
        self.assertEqual(restored_project.name, self.project.name)
        self.assertEqual(restored_project.due, self.project.due)
        self.assertEqual(restored_project.status, self.project.status)
        self.assertEqual(restored_project.memo, self.project.memo)

    def test_export_as_dict(self):
        project_dict = self.project.export_as_dict()
        self.assertEqual(project_dict["id"], str(self.project.id))
        self.assertEqual(project_dict["name"], "Test Project")
        self.assertEqual(project_dict["due"], self.project.due.isoformat())
        self.assertEqual(project_dict["status"], TaskStatus.TODO.value)
        self.assertEqual(project_dict["memo"], "Test Memo")

if __name__ == "__main__":
    unittest.main()