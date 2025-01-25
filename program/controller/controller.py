from uuid import UUID
from typing import Literal
from datetime import datetime
from tkinter import messagebox
from model.model import ProjectRoot, Project, Task
from model.status import TaskStatus
from view.view import MainWindow
from view.CustomFrames.DetailFrame import *



class Controller:
    """コントローラークラス。シングルトンパターンを適用している。
    """
    _instance = None

    def __new__(cls, model:ProjectRoot, view:MainWindow):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def eventhandler_with_attr(func):
        """
        イベント以外の追加引数を受け取るイベントハンドラ用のデコレータ。
        このデコレータによって装飾されたハンドラは適切にラップされ、
        イベント引数のみを受け取るイベントハンドラと同様に使用できます。

        ```
        @eventhandler_with_attr
        update_project_attribute(self, event, attr_name)
        # 上記のように、デコレータを使用してイベントハンドラを定義すると、
        # そのハンドラは以下のように呼び出されます。
        update_project_attribute(attr_name="name")
        ```
        """
        def wrapper(self, *args, **kwargs):
            return lambda event: func(self, event, *args, **kwargs)
        return wrapper

    def __init__(self, model:ProjectRoot, view:MainWindow):
        self.model = model
        self.view  = view

        # ビューのイベントハンドラを設定
        self.view._project_list_frame._project_treeview.bind("<ButtonRelease>", self.__on_project_treeview_select)
        self.view._task_list_frame._task_treeview.bind("<ButtonRelease>", self.__on_task_treeview_select)
        self.view._project_list_frame._add_project_button.bind("<ButtonRelease>", self.__on_add_project_button_click)
        self.view._task_list_frame._add_task_button.bind("<ButtonRelease>", self.__on_add_task_button_click)
        # ビューの右クリックメニューのイベントハンドラを設定
        self.view._project_list_frame._right_click_menu.add_command(label="Delete", command=self.__on_delete_project_menu_click)
        self.view._task_list_frame._right_click_menu.add_command(label="Delete", command=self.__on_delete_task_menu_click)

        self.__construct_initial_view() # 初期状態のビューを構築


    def __construct_initial_view(self):
        """初期状態のビューを構築する
        """
        # プロジェクト一覧とタスク一覧を取得
        projects = self.model.get_children()
        # view._project_list_frameにプロジェクト一覧を表示
        self.view._project_list_frame.add_project_rows(projects)

    ##########################################
    ########## イベントハンドラ ##############
    ##########################################

    def __on_project_treeview_select(self, event):
        """プロジェクト一覧のTreeViewで行が選択された際の処理

        1. 選択されたプロジェクトのタスク一覧を取得
        2. view._task_list_frameのタスク一覧表示を更新
        3. view._detail_frameの表示を更新
        """
        if not self.view._project_list_frame._project_treeview.identify_row(event.y):
            # プロジェクト以外の場所がクリックされた場合は何もしない
            return
        selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
        selected_project = self.model.get_child_by_id(selected_project_id)
        self.view._task_list_frame.delete_all_task_rows()
        self.view._task_list_frame.add_task_rows(selected_project.get_children())
        self.__refresh_project_detail_frame(selected_project)

    def __on_task_treeview_select(self, event):
        """タスク一覧のTreeViewで行が選択された際の処理

        A. タスクが選択された場合
            1. 選択されたタスクの詳細をview._detail_frameに表示
            2. view._detail_frameの表示を更新

        B. タスク以外の場所がクリックされた場合
            1. 選択を解除
        """
        if not self.view._task_list_frame._task_treeview.identify_row(event.y):
            # タスク以外の場所がクリックされた場合は選択を解除
            self.view._task_list_frame._task_treeview.selection_remove(*self.view._task_list_frame._task_treeview.selection())
            return
        selected_task_id = UUID(self.view._task_list_frame._task_treeview.selection()[0])
        selected_task = self.model.get_child_by_id(selected_task_id, recursive=True)
        self.__refresh_task_detail_frame(selected_task)

    def __on_add_project_button_click(self, event):
        """プロジェクト追加ボタンがクリックされた際の処理

        1. モデルに新しいプロジェクトを追加
        2. view._project_list_frameに新しいプロジェクトを表示
        3. モデルの変更を保存
        """
        new_project = self.model.create_child()
        new_project.name = "New Project"
        self.view._project_list_frame.add_project_row(new_project)
        self.__refresh_project_detail_frame(new_project)
        self.model.save()

    def __on_add_task_button_click(self, event):
        """タスク追加ボタンがクリックされた際の処理

        1. 選択されているプロジェクトに新しいタスクを追加
        2. view._task_list_frameに新しいタスクを表示
        3. モデルの変更を保存
        """
        if len(self.view._project_list_frame._project_treeview.selection()) == 0:
            # タスクの親となるべきプロジェクトが選択されていない場合は警告を表示
            messagebox.showwarning("Error", "No parental project is selected")
        else:
            selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
            selected_project = self.model.get_child_by_id(selected_project_id)
            new_task = selected_project.create_child()
            new_task.name = "New Task"
            self.view._task_list_frame.add_task_row(new_task)
            self.__refresh_task_detail_frame(new_task)
            self.model.save()

    def __on_delete_project_menu_click(self):
        """プロジェクトの右クリックメニューのDeleteがクリックされた際の処理

        1. 選択されているプロジェクトを削除
        2. view._project_list_frameの表示を更新
        3. モデルの変更を保存
        TODO: 4. view._detail_frameの表示を更新
        """
        # [Model] 選択されているプロジェクトを削除
        selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
        self.model.delete_child(selected_project_id)
        # [View] view._project_list_frameから選択されているプロジェクトを削除
        self.view._project_list_frame._project_treeview.delete(selected_project_id)
        # [View] プロジェクトに紐づいていたタスクをview._task_list_frameから削除
        self.view._task_list_frame.delete_all_task_rows()
        # [Model] モデルの変更を保存
        self.model.save()

    def __on_delete_task_menu_click(self):
        """タスクの右クリックメニューのDeleteがクリックされた際の処理

        1. 選択されているタスクを削除
        2. view._task_list_frameの表示を更新
        3. モデルの変更を保存
        TODO: 4. view._detail_frameの表示を更新
        BUG: 子タスクを削除することが出来ない。project→taskの検索しかしていないため。
        """
        # [Model] 選択されているタスクを削除
        selected_project_id = UUID(self.view._project_list_frame._project_treeview.selection()[0])
        selected_task_id = UUID(self.view._task_list_frame._task_treeview.selection()[0])
        selected_project = self.model.get_child_by_id(selected_project_id)
        selected_task = selected_project.get_child_by_id(selected_task_id)
        selected_project.delete_child(selected_task.id)
        # [View] view._task_list_frameから選択されているタスクを削除
        self.view._task_list_frame._task_treeview.delete(selected_task.id)
        # [Model] モデルの変更を保存
        self.model.save()


    @eventhandler_with_attr
    def __update_project_attribute(
        self, 
        event, 
        attr_name: Literal['id', 'name', 'due', 'status', 'memo', 'children'],
        project_id: UUID
    ):
        """DetailFrameのEntryの値が変更された際の処理

        Parameters
        ----------
        event : tkinter.Event
            発生したイベント
        attr_name : Literal['id', 'name', 'due', 'status', 'memo', 'children']
            更新する属性の名前（ProjectDict のキー）
        project_id : UUID
            更新するプロジェクトのID

        1. Entryの値を取得
        2. モデルの値を更新
        3. view._project_list_frameの表示を更新
        4. モデルの変更を保存
        """
        allowed_attrs = {'id', 'name', 'due', 'status', 'memo', 'children'}
        if attr_name not in allowed_attrs:
            raise ValueError(f"Invalid attribute name: {attr_name}")
        
        # 入力値の取得
        input_value = event.widget.get()

        # 属性ごとの型変換
        if attr_name == 'due':
            try:
                converted_value = datetime.strptime(input_value, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("入力エラー", "有効な日付形式 (YYYY-MM-DD) を入力してください。")
                return
        elif attr_name == 'status':
            try:
                converted_value = TaskStatus(input_value)
            except ValueError:
                messagebox.showerror("入力エラー", f"無効なステータス: {input_value}")
                return
        elif attr_name == 'id':
            try:
                converted_value = UUID(input_value)
            except ValueError:
                messagebox.showerror("入力エラー", f"無効なUUID: {input_value}")
                return
        elif attr_name == 'memo' or attr_name == 'name':
            converted_value = str(input_value)
        elif attr_name == 'children':
            # children属性は直接更新しない
            messagebox.showwarning("操作不可", "children属性は直接更新できません。")
            return
        else:
            # その他の属性は文字列として扱う
            converted_value = input_value

        # [Model] モデルの値を更新
        selected_project = self.model.get_child_by_id(project_id)
        setattr(selected_project, attr_name, converted_value)

        # [View] view._project_list_frameの表示を更新
        self.view._project_list_frame.update_project_row(selected_project)
        # [Model] モデルの変更を保存
        self.model.save()


    ##########################################
    ########## イベントハンドラ以外 ##########
    ##########################################

    def __refresh_project_detail_frame(self, selected_project:Project):
        """
        既存のDetailFrameを削除し、
        選択されたプロジェクトの詳細をview._detail_frameに表示する
        """
        # 既存のDetailFrameを削除して、新しいDetailFrameを作成し、paned_windowに追加
        self.view._detail_frame.destroy()
        self.view._detail_frame = ProjectDetailFrame(self.view._paned_window)
        self.view._paned_window.add(self.view._detail_frame.frame)
        # 選択されたプロジェクトの情報をDetailFrameに表示
        self.view._detail_frame.name_entry.set(selected_project.name)
        self.view._detail_frame.due_entry.set(selected_project.due)
        self.view._detail_frame.status_combobox.set(selected_project.status.name)
        self.view._detail_frame.memo_entry.set(selected_project.memo)
        # Entryの値が変更された際のイベントハンドラを設定
        self.view._detail_frame.name_entry.entry.bind("<FocusOut>", self.__update_project_attribute(attr_name="name", project_id=selected_project.id))
        self.view._detail_frame.due_entry.entry.bind("<FocusOut>", self.__update_project_attribute(attr_name="due", project_id=selected_project.id))
        self.view._detail_frame.status_combobox.combobox.bind("<FocusOut>", self.__update_project_attribute(attr_name="status", project_id=selected_project.id))
        self.view._detail_frame.memo_entry.entry.bind("<FocusOut>", self.__update_project_attribute(attr_name="memo", project_id=selected_project.id))

    def __refresh_task_detail_frame(self, selected_task:Task):
        """
        既存のDetailFrameを削除し、
        選択されたタスクの詳細をview._detail_frameに表示する
        """
        # 既存のDetailFrameを削除して、新しいDetailFrameを作成し、paned_windowに追加
        self.view._detail_frame.destroy()
        self.view._detail_frame = TaskDetailFrame(self.view._paned_window)
        self.view._paned_window.add(self.view._detail_frame.frame)
        # 選択されたタスクの情報をDetailFrameに表示
        self.view._detail_frame.name_entry.set(selected_task.name)
        self.view._detail_frame.due_entry.set(selected_task.due)
        self.view._detail_frame.status_combobox.set(selected_task.status.name)
        self.view._detail_frame.memo_entry.set(selected_task.memo)
        self.view._detail_frame.assignee_entry.set(selected_task.assignee)
        self.view._detail_frame.estimation_entry.set(selected_task.estimation)
        self.view._detail_frame.priority_entry.set(selected_task.priority)
        # TODO:Entryの値が変更された際のイベントハンドラを設定