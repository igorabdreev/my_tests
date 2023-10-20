from enum import Enum

from pydantic import BaseModel


class AutoStrEnum(str, Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:
        return name


class GoalsDto(BaseModel):
    """ Базовый класс DTO сервиса Goals """

    class Config:
        use_enum_values = True