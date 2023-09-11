"""Базовый класс страницы для работы с сервисом "Цели" (базовые компоненты страницы) """
from selenium.webdriver.remote.webdriver import WebDriver

from web.pages.base import BasePage


class GoalsBasePage(BasePage):
    """Базовый класс для работы со страницами Цели."""

    def __init__(self, driver: WebDriver):
        """
        Args:
            driver: Инстанс WebDriver.
        """
        super().__init__(driver=driver)
        self.url = f'{self.url}/platform/goals'
