from enum import Enum

from Handlers.exeptions import TheresNoRole


class States(Enum):
    OPEN = 0
    CLOSED = 1
    WORKING = 2


class Task:
    def __init__(self, task_id, owner: str | int, name: str, status: States):
        self._id: int = task_id
        self.owner: str | int = owner
        self.name: str = name
        self.status: States = status
        self.child_tasks: list[Task] = []

    def add_child_task(self, task) -> None:
        self.child_tasks.append(task)

    def get_child_tasks(self) -> list:
        return self.child_tasks

    def get_id(self):
        return self._id

    def __str__(self):
        return f"{self.name} - {self.status}"


class TaskBuilder(Task):
    def __init__(self, task: Task):
        super().__init__(task.get_id(), task.name, task.status, task.owner)
        self.parent = task

    def add_child_task(self, task) -> Task:
        self.parent.child_tasks.append(task)
        return self


class ConventionStates:
    @staticmethod
    def str_to_role(state: str) -> States:
        if state in States:
            return States[state]
        else:
            raise TheresNoRole("The state doesn't exist")
