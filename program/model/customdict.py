"""
このモジュールは、Project, Taskクラスに保存されているデータを規定している
"""

from typing import TypedDict, List
from uuid import UUID
from datetime import datetime
from model.status import TaskStatus
from model.priority import Priority




class ProjectDict(TypedDict):
    id    : UUID
    name  : str
    due   : str       # date型をisoformat()で文字列化したもの
    status: str       # TaskStatus型を文字列化したもの
    memo  : str
    children: List['TaskDict']


class TaskDict(TypedDict):
    id        : UUID
    name      : str
    due       : str       # date型をisoformat()で文字列化したもの
    status    : str       # TaskStatus型を文字列化したもの
    memo      : str
    assignee  : str
    estimation: str
    priority  : Priority
    children  : dict