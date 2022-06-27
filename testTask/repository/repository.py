from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

from testTask.models.config import DbConfig


class SQLCommand(ABC):
    args_for_execute: Tuple[str, Tuple] = ()

    @classmethod
    @abstractmethod
    def _init_command(cls, *args, **kwargs):
        pass

    def __new__(cls, *args, **kwargs) -> tuple:
        cls._init_command(*args, **kwargs)
        if cls.args_for_execute:
            return cls.args_for_execute
        else:
            raise "You are not implement command method"


class DatabaseInterface(ABC):

    def __init__(self, config: Dict):
        self.config_file: DbConfig = DbConfig(**config)

    @abstractmethod
    async def connect(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def disconnect(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def execute(self, command: Tuple) -> List[Tuple]:
        pass
