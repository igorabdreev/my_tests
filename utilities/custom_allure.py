""" Кастомный allure.step c логированием в консоль """
from allure_commons._allure import StepContext

from utilities.logger_error import InvalidLogLevel
from utilities.logging import logger


def step(title: str, log_level: str = 'INFO') -> StepContext:
    """Кастомный степ с логированием названия степа в консоль

    Args:
        title: название степа
        log_level: уровень логирования.
    """
    log_method = getattr(logger, log_level.lower(), logger.info)

    log_method(title)

    return StepContext(title, {})
