import flet as ft
from view.CustomFrames.LabeledItem import LabeledEntry, LabeledText, LabeledCombobox

class DetailFrame:
    def __init__(self):
        self.view = ft.Column(expand=True)
    def get_view(self):
        return self.view
    def destroy(self):
        self.view.controls.clear()
        self.view.update()

class ProjectDetailFrame(DetailFrame):
    def __init__(self):
        super().__init__()
        self.name_entry = LabeledEntry("Name")
        self.due_entry = LabeledEntry("Due")
        self.status_combobox = LabeledCombobox("Status", options=[s.value for s in []])  # 実際のTaskStatusを設定
        self.memo_entry = LabeledText("Memo")
        self.view.controls.extend([
            self.name_entry.get_view(),
            self.due_entry.get_view(),
            self.status_combobox.get_view(),
            self.memo_entry.get_view()
        ])

class TaskDetailFrame(DetailFrame):
    def __init__(self):
        super().__init__()
        self.name_entry = LabeledEntry("Name")
        self.due_entry = LabeledEntry("Due")
        self.status_combobox = LabeledCombobox("Status", options=[s.value for s in []])
        self.estimation_entry = LabeledEntry("Estimation")
        self.priority_combobox = LabeledCombobox("Priority", options=[p.value for p in []])
        self.assignee_entry = LabeledEntry("Assignee")
        self.memo_entry = LabeledText("Memo")
        self.view.controls.extend([
            self.name_entry.get_view(),
            self.due_entry.get_view(),
            self.status_combobox.get_view(),
            self.estimation_entry.get_view(),
            self.priority_combobox.get_view(),
            self.assignee_entry.get_view(),
            self.memo_entry.get_view()
        ])