import tkinter as tk
import tkinter.ttk as ttk
from view.CustomFrames.LabeledItem import *
from model.status import TaskStatus
from model.priority import Priority


class DetailFrame:
    def __init__(self, parent: ttk.PanedWindow):
        self.frame = ttk.Frame(parent)
    def destroy(self):
        self.frame.destroy()


class ProjectDetailFrame(DetailFrame):
    def __init__(self, parent: ttk.PanedWindow):
        super().__init__(parent)
        self.name_entry = LabeledEntry(self.frame, 'Name')
        self.due_entry = LabeledEntry(self.frame, 'Due')
        self.status_combobox = LabeledCombobox(self.frame, 'Status', [status.value for status in TaskStatus])
        self.memo_entry = LabeledEntry(self.frame, 'Memo')


class TaskDetailFrame(DetailFrame):
    def __init__(self, parent: ttk.PanedWindow):
        super().__init__(parent)
        self.name_entry = LabeledEntry(self.frame, 'Name')
        self.due_entry = LabeledEntry(self.frame, 'Due')
        self.status_combobox = LabeledCombobox(self.frame, 'Status', [status.value for status in TaskStatus])
        self.memo_entry = LabeledEntry(self.frame, 'Memo')
        self.assignee_entry = LabeledEntry(self.frame, 'Assignee')
        self.estimation_entry = LabeledEntry(self.frame, 'Estimation')
        self.priority_combobox = LabeledCombobox(self.frame, 'Priority', [priority.value for priority in Priority])