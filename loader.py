from configparser import ConfigParser
from dataclasses import dataclass

from aiogram import Bot


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    config: ConfigParser = ConfigParser()
    config.read("config.ini")


@dataclass
class Program(metaclass=Singleton):
    config = Config().config
    bot_token: str = config.get("Settings", "botToken")
    answers_path: str = config.get("Settings", "answersPath")
    database_path: str = config.get("Settings", "databasePath")
    bot: Bot = Bot(bot_token)
