"""Класс страницы аутентификации."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from users.user import User
from utilities.config import Config
from web.driver_config import TIMEOUT
from web.locator import Locator
from web.pages.base import BasePage


class AuthPage(BasePage):
    """Класс страницы аутентификации"""

    # Локаторы
    INPUT_USERNAME = Locator(name="Username пользователя", locator=(By.XPATH, '//input[@id="username"]'))
    INPUT_PASSWORD = Locator(name="Пароль пользователя", locator=(By.XPATH, '//input[@id="password"]'))
    LOGIN_BUTTON = Locator(name='Кнопка "Вход"', locator=(By.XPATH, '//input[@id="kc-login"]'))
    CUSTOMER = Locator(name="customer", locator=(By.XPATH, '//a[@id="social-customer"]'))
    TEXT_TOKEN = Locator(name='Текст "Token"', locator=(By.XPATH, '//b[contains(text(),"Token")]'))

    def __init__(self, driver: WebDriver):
        """
        Args:
            driver: Инстанс WebDriver.
        """
        super().__init__(driver=driver)
        self.url_logout = f'{self.url}/logout'
        self.url = f'{self.url}/checkTokens'

    @allure.step('Аутентифицироваться через браузер')
    def auth(self, user: User):
        """Аутентифицироваться с помощью username и пароля.

        Args:
            user: пользователь
        """
        self.get()

        if 'qa.thehrp.ru' in self.url:
            self.click_by_locator(locator=self.CUSTOMER)

        self.send_keys_by_element(
            element=self.click_by_locator(locator=self.INPUT_USERNAME),
            locator=self.INPUT_USERNAME,
            keys=user.login
        )

        self.send_keys_by_element(
            element=self.click_by_locator(locator=self.INPUT_PASSWORD),
            locator=self.INPUT_PASSWORD,
            keys=Config.vault.get_value_from_vault(
                key_name='password',
                vault_path=user.vault_path,
                secret_name=user.login
            )
        )

        self.click_by_locator(locator=self.LOGIN_BUTTON)

        self.find_visible_element(locator=self.TEXT_TOKEN)

    @allure.step('Выйти из учётной записи в браузере')
    def logout(self):
        """Выйти из учётной записи"""
        self.open(url=self.url_logout)
        WebDriverWait(driver=self._driver, timeout=TIMEOUT).until(method=EC.url_contains('success'))
