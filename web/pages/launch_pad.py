from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from web.pages.base import BasePage
from web.locator import Locator


class LaunchPad(BasePage):
    """Класс главной станицы платформы Пульс"""
    ELEMENT_CONTAINS_TEXT = Locator(
        name="Элемент содержащий текст {text}",
        locator=(By.XPATH, "//*[contains(text(), '{text}')]")
    )
    ELEMENT_WITH_TEXT = Locator(
        name="Элемент с текстом {text}",
        locator=(By.XPATH, "//*[text()='{text}']")
    )

    def __init__(self, driver: WebDriver):
        """
        Args:
            driver: Инстанс WebDriver.
        """
        super().__init__(driver=driver)
        self.url = f'{self.url}/platform/dashboard'
