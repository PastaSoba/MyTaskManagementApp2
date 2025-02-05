from abc import ABC, abstractmethod
from typing import List, Union
from uuid import UUID, uuid4
from datetime import date
import json

from model.status import TaskStatus
from model.priority import Priority
from model.customdict import ProjectDict, TaskDict




class ABC_Tree(ABC):
    """
    ツリー構造を表す抽象基底クラス

    Attributes
    ----------
    _id : UUID
        ノードの識別子。上書き不可。

        例外的にrestore_from_dict()の内部で指定されるが、
        基本的にインスタンスの作成時に自動生成されるため指定しない。
    """
    def __init__(self, _id: UUID = None):
        self._id      : UUID             = _id if _id else uuid4()
        self._children: List['ABC_Tree'] = []
    
    @property
    def id(self) -> UUID:
        return self._id

    def get_children(self) -> List['ABC_Tree']:
        """
        自ノードの全ての子ノードを返す

        Returns:
            List[ABC_Tree]: 自ノードの全ての子ノードのリスト
        """
        return self._children

    def get_child_by_id(self, id: UUID, recursive: bool=False) -> 'ABC_Tree':
        """
        指定したIDを持つ子ノードを返す

        Args:
            id (UUID): 子ノードのID
            recursive (bool): 再帰的に探索する場合はTrue

        Returns:
            ABC_Tree: 指定したIDを持つ子ノード
        """
        for child in self._children:
            if child.id == id:
                return child
            if recursive:
                try:
                    return child.get_child_by_id(id, True)
                except ValueError:
                    pass
        raise ValueError(f"No child with id {id} found.")

    @abstractmethod
    def create_child(self) -> 'ABC_Tree':
        """
        ノードを作成し、自ノードの子ノードとして追加する。

        Returns:
            ABC_Tree: 追加した子ノード
        """
        pass

    def delete_child(self, id: UUID) -> None:
        """
        指定したIDを持つ子ノードを削除する
        """
        for child in self._children:
            if child.id == id:
                self._children.remove(child)
                return
        raise ValueError(f"No child with id {id} found.")

    @staticmethod
    @abstractmethod
    def restore_from_dict(dict_obj: Union[ProjectDict, TaskDict]) -> 'ABC_Tree':
        """辞書型から自分のクラスのインスタンスを復元する
        """
        pass

    @abstractmethod
    def export_as_dict() -> Union[ProjectDict, TaskDict]:
        """自分のクラスの情報を辞書型に変換する
        """
        pass



class ABC_PnT(ABC_Tree):
    """ProjectクラスとTaskクラスの共通部分を抽象化した抽象基底クラス
    """
    def __init__(self, _id: UUID = None):
        super().__init__(_id)
        self.name  :str        = ""
        self.due   :date       = date.today()
        self.status:TaskStatus = TaskStatus.TODO
        self.memo  :str        = ""












class ProjectRoot(ABC_Tree):
    """プロジェクトのルートノードを表すクラス。シングルトンパターンを適用。
    """
    __FILEPATH = "project.json"
    _instance = None  # シングルトンインスタンスを保持

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProjectRoot, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True  # 初期化済みフラグ

    def create_child(self) -> 'Project':
        new_project = Project()
        self._children.append(new_project)
        return new_project

    @staticmethod
    def load() -> 'ProjectRoot':
        """JSONファイルからプロジェクトのデータを読み込む。シングルトンインスタンスを返す。
        """
        if ProjectRoot._instance is None:
            dict_obj = ProjectRoot.__import_dict_obj_from_json()
            ProjectRoot._instance = ProjectRoot.restore_from_dict(dict_obj)
        return ProjectRoot._instance

    @staticmethod
    def __import_dict_obj_from_json() -> List[ProjectDict]:
        with open(ProjectRoot.__FILEPATH, "r") as f:
            return json.load(f)

    @staticmethod
    def restore_from_dict(dict_obj: List[ProjectDict]) -> 'ProjectRoot':
        root = ProjectRoot()
        for project_dict in dict_obj:
            root._children.append(Project.restore_from_dict(project_dict))
        return root

    def save(self) -> None:
        """プロジェクトのデータをJSONファイルに保存する
        """
        self.__export_dict_as_json()

    def __export_dict_as_json(self) -> None:
        with open(ProjectRoot.__FILEPATH, "w") as f:
            json.dump(self.export_as_dict(), f, indent=4)

    def export_as_dict(self) -> List[ProjectDict]:
        return [child.export_as_dict() for child in self.get_children()]




class Project(ABC_PnT):
    """プロジェクトを表すクラス

    Attributes
    ----------
    id : UUID
        ノードの識別子。上書き不可。

        例外的にrestore_from_dict()の内部で指定されるが、
        基本的にインスタンスの作成時に自動生成されるため指定しない。
    name : str
        プロジェクト名
    due : date
        締め切り日
    status : TaskStatus
        プロジェクトのステータス
    memo : str
        メモ
    """
    def __init__(self, _id: UUID = None):
        super().__init__(_id)

    def create_child(self) -> 'Task':
        new_task = Task()
        self._children.append(new_task)
        return new_task

    @staticmethod
    def restore_from_dict(dict_obj: ProjectDict) -> 'Project':
        project        = Project(_id=UUID(dict_obj["id"]))
        project.name   = dict_obj["name"]
        project.due    = date.fromisoformat(dict_obj["due"])
        project.status = TaskStatus(dict_obj["status"])
        project.memo   = dict_obj["memo"]
        for task_dict in dict_obj["children"]:
            project._children.append(Task.restore_from_dict(task_dict))
        return project

    def export_as_dict(self) -> ProjectDict:
        return {
            "id"    : str(self.id),
            "name"  : self.name,
            "due"   : self.due.isoformat(),
            "status": self.status.value,
            "memo"  : self.memo,
            "children": [child.export_as_dict() for child in self.get_children()]
        }


class Task(ABC_PnT):
    """タスクを表すクラス

    Attributes
    ----------
    id : UUID
        ノードの識別子。上書き不可。

        例外的にrestore_from_dict()の内部で指定されるが、
        基本的にインスタンスの作成時に自動生成されるため指定しない。
    name : str
        タスク名
    due : date
        締め切り日
    status : TaskStatus
        タスクのステータス
    memo : str
        メモ
    assignee : str
        担当者
    estimation : str
        予想所要時間
    priority : Priority
        優先度
    """
    def __init__(self, _id: UUID = None):
        super().__init__(_id)
        self.assignee  :str      = ""
        self.estimation:str      = ""
        self.priority  :Priority = Priority.NOT_YOUR_JOB

    def create_child(self) -> 'Task':
        new_task = Task()
        self._children.append(new_task)
        return new_task

    @staticmethod
    def restore_from_dict(dict_obj: TaskDict) -> 'Task':
        task           = Task(_id=UUID(dict_obj["id"]))
        task.name      = dict_obj["name"]
        task.due       = date.fromisoformat(dict_obj["due"])
        task.status    = TaskStatus(dict_obj["status"])
        task.memo      = dict_obj["memo"]
        task.assignee  = dict_obj["assignee"]
        task.estimation= dict_obj["estimation"]
        task.priority  = Priority(dict_obj["priority"])
        for child_dict in dict_obj["children"]:
            task._children.append(Task.restore_from_dict(child_dict))
        return task

    def export_as_dict(self) -> TaskDict:
        return {
            "id"        : str(self.id),
            "name"      : self.name,
            "due"       : self.due.isoformat(),
            "status"    : self.status.value,
            "memo"      : self.memo,
            "assignee"  : self.assignee,
            "estimation": self.estimation,
            "priority"  : self.priority.value,
            "children"  : [child.export_as_dict() for child in self.get_children()]
        }

    def parent(self) -> Union[Project, 'Task']:
        """
        自分の親ノードを返す。
        自分がProjectの直下のTaskインスタンスにある場合はProjectを返す。
        自分がTaskの下のTaskインスタンス（子Task）にある場合は親Taskを返す。
        Returns:
            Union[Project, Task]: 親ノード
        """
        root = ProjectRoot()
        for project in root.get_children():
            # 自分がproject下の直接Taskインスタンスである場合
            if self in project.get_children():
                return project
            # 自分がTaskの下のTaskインスタンス（子Task）である場合
            for task in project.get_children():
                if self in task.get_children():
                    return task