"""Класс и методы для создания браузеров"""
import sys
from pathlib import Path

from selenium.webdriver import Chrome, Safari, Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.safari.service import Service as SafariService

from api.decorators import unavailable_host_exception_handler
from utilities.logging import logger
from web.driver_config import ChromeConfig, SafariConfig, YandexConfig, SelenoidConfig


class Driver:
    """Класс для создания экземпляров различных браузеров"""

    @staticmethod
    def __create_chrome_driver(root: Path, add_opts: list = None, is_selenoid: bool = None) -> Remote or Chrome:
        """Создать экзепляр Chrome драйвера

        Args:
            root: корень проекта
            add_opts: дополнительные опции
            is_selenoid: запуск через Selenoid
        """
        options = ChromeOptions()

        for arg in ChromeConfig.default_options + add_opts:
            options.add_argument(arg)

        if is_selenoid:
            return Remote(
                command_executor=SelenoidConfig.HUB_URL,
                desired_capabilities=SelenoidConfig.CAPABILITIES['chrome'],
                options=options
            )

        else:
            return Chrome(
                service=ChromeService(executable_path=root / getattr(ChromeConfig, f'exec_path_{sys.platform}')),
                options=options
            )

    @staticmethod
    def __create_yandex_driver(root: Path, add_opts: list = None, is_selenoid: bool = None) -> Remote or Chrome:
        """Создать экзепляр Yandex драйвера

        Args:
            root: корень проекта
            add_opts: дополнительные опции
            is_selenoid: запуск через Selenoid
        """
        options = ChromeOptions()

        for arg in YandexConfig.default_options + add_opts:
            options.add_argument(arg)

        if is_selenoid:
            return Remote(
                command_executor=SelenoidConfig.HUB_URL,
                desired_capabilities=SelenoidConfig.CAPABILITIES['yandex'],
                options=options
            )

        else:
            return Chrome(
                service=ChromeService(executable_path=root / getattr(YandexConfig, f'exec_path_{sys.platform}')),
                options=options
            )

    @staticmethod
    def __create_safari_driver(root: Path, add_opts: list = None, is_selenoid: bool = None) -> Remote or Safari:
        """Создать экзепляр Safari драйвера

        Args:
            root: корень проекта
            add_opts: дополнительные опции
            is_selenoid: Запуск через Selenoid
        """
        options = SafariOptions()

        for arg in SafariConfig.default_options + add_opts:
            options.add_argument(arg)

        if is_selenoid:
            return Remote(
                command_executor=SelenoidConfig.HUB_URL,
                desired_capabilities=SelenoidConfig.CAPABILITIES['safari'],
                options=options
            )

        else:
            return Safari(
                service=SafariService(executable_path=root / getattr(SafariConfig, f'exec_path_{sys.platform}')),
                options=options
            )

    @staticmethod
    @unavailable_host_exception_handler
    def get_driver(root: Path, browser_name: str, add_opts: list = None, is_selenoid: bool = None) -> Remote or Chrome:
        """Получить экземпляр драйвера

        Args:
            root: путь до корня проекта
            is_selenoid: запуск через Selenoid
            browser_name: название браузера
            add_opts: дополнительные опции
        """
        logger.info(
            f'Переданы настройки браузера:\n'
            f'\tБраузер:       \t{browser_name}\n'
            f'\tДоп. настройки:\t{add_opts}\n'
            f'\tSelenoid:      \t{is_selenoid}'
        )
        return {
            'chrome': Driver.__create_chrome_driver,
            'yandex': Driver.__create_yandex_driver,
            'safari': Driver.__create_safari_driver
        }[browser_name](root=root, add_opts=add_opts, is_selenoid=is_selenoid)
