"""Декоратор для форматирования локатора"""
from typing import Callable

from selenium.webdriver.remote.webelement import WebElement

from utilities.logging import logger


def format_locator(decorated: Callable) -> Callable:
    """Декоратор для форматирования локатора, до выполнения метода

    Args:
        decorated: декорируемая функция
    """

    def inner(*args, **kwargs) -> WebElement:
        """Обертка над методами класса BasePage

        Args:
            **kwargs: прочие аргументы
        """
        logger.debug(
            f'Переданные значения:\n'
            f'\tArgs:\t{args}\n'
            f'\tKwargs:\t{kwargs}\n'
        )

        if kwargs:
            locator_before_format = kwargs['locator']
            kwargs['locator'] = kwargs['locator'](**kwargs)

            if locator_before_format.locator != kwargs['locator'].locator:
                logger.info(
                    f'Форматируем локатор перед методом {decorated.__name__}\n'
                    f'\tБыло:\t{locator_before_format}\n'
                    f'\tСтало:\t{kwargs["locator"]}'
                )

        return decorated(*args, **kwargs)

    return inner
