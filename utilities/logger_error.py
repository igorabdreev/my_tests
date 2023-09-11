"""Ошибки, связанные с логером"""


class InvalidLogLevel(Exception):
    """Исключение при попытке задать неподдерживаемый уровень логирования"""

    def __init__(self, log_level: str, available_log_levels: str):
        self.log_level, self.available_log_levels = log_level, available_log_levels

    def __str__(self):
        return f'Указан недопустимый уровень логирования: "{self.log_level}". ' \
               f'Пожалуйста, укажите один из следующих уровней: {self.available_log_levels}'
