import json
from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum

from Handlers.exeptions import NoneInAnswer, TheresNoRole
from loader import Program


answers_path = Program().answers_path


class Answer(ABC):
    def __init__(self, _name: str):
        self._name: str = _name
        self.text: any = None

    def set_text(self, text: str) -> None:
        self.text = text

    @abstractmethod
    def get(self):
        raise NotImplementedError

    def __str__(self) -> str:
        if self.text is not None:
            return f"{self.text}"
        else:
            raise NoneInAnswer("Answer is None")


class JSONAnswer(Answer):
    def get(self) -> Answer:
        try:
            with open(answers_path, "r", encoding="UTF-8") as answers:
                self.set_text(json.loads(answers.read()).get(self._name))
        except (FileNotFoundError, json.JSONDecodeError):
            self.set_text("None")
        return self


class Role(Enum):
    BANNED = -2
    EXIT = -1
    USER = 0
    MODERATOR = 1
    ADMIN = 2
    SUPER_ADMIN = 3


@dataclass
class User:
    id: int
    role: Role


class ConventionRole:
    @staticmethod
    def str_to_role(role: str) -> Role:
        if role in Role:
            return Role[role]
        else:
            raise TheresNoRole("The role doesn't exist")
