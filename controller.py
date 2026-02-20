from model import TaskModel
from view import PyQtView


class TaskController:
    def __init__(self):
        self.model = TaskModel()
        self.view = PyQtView(self)