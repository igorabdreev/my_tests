"""Декоратор для создания скриншота"""
from typing import Callable

import allure
import pytest
from selenium.webdriver.remote.webelement import WebElement

from utilities.logging import logger
from utilities.config import Config


def make_screenshot(decorated: Callable) -> Callable:
    """Декоратор для создания скриншота после выполнения шага

    Args:
        decorated: декорируемый метод
    """

    def inner(*args, **kwargs) -> WebElement:
        """Обертка над методами класса BasePage"""
        try:
            value = decorated(*args, **kwargs)

        except Exception:
            pytest.fail(reason=f'Ошибка при выполнении метода "{decorated.__name__}"')

        try:
            allure.attach(
                name=f'screenshot_{decorated.__name__}',
                body=Config.driver.get_screenshot_as_png(),
                attachment_type=allure.attachment_type.PNG
            )
            logger.debug('Скриншот сохранён')

        except Exception:
            logger.warning('Не удалось сохранить скриншот!')

        return value

    return inner
