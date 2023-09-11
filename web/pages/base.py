"""Класс базовой страницы и методы для работы с ней."""
from typing import Callable

import allure
import pytest
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utilities.config import Config
from utilities.logging import logger
from utilities.tools import wums
from web import driver_config
from web.format_locator import format_locator
from web.locator import Locator
from web.make_screenshot import make_screenshot


class BasePage:
    """Класс базовой страницы для работы с элементами."""
    url: str

    def __init__(self, driver: WebDriver):
        """
        Args:
            driver: Инстанс WebDriver.
        """
        self._driver = driver
        self.url = Config.web_url
        logger.info(f'Инициализирована страница: {self.__class__.__name__}')

    @property
    def current_url(self) -> str:
        """Получить текущий URL"""
        logger.info(msg := f'URL текущей вкладки: "{(url := self._driver.current_url)}"')
        return url

    @property
    def driver(self) -> WebDriver:
        """Получить драйвер"""
        logger.info('Получаем драйвер')
        return self._driver

    @property
    def current_handle(self) -> str:
        """Получить handle открытой вкладки"""
        logger.info(f'Идентификатор текущей вкладки: "{(handle := self._driver.current_window_handle)}"')
        return handle

    def is_page_loaded(decorated: callable) -> Callable:
        """Декорировать методы открытия страницы

        Args:
            decorated: декорируемый метод
        """

        def inner(self, **kwargs):
            """Обертка над методом

            Args:
                self: объект страницы
                **kwargs: прочие аргументы
            """
            _ = decorated(self, **kwargs)
            wums(method=self._driver.execute_script, expected='complete', script='return document.readyState')
            return _

        return inner

    @is_page_loaded
    @allure.step('Открыть страницу по URL из класса')
    @make_screenshot
    def get(self):
        """Открыть страницу url класса"""
        logger.info(f'Открываем страницу {self.url}')
        self._driver.get(self.url)
        logger.success(f'Страница {self.url} открыта')

    @is_page_loaded
    @allure.step('Открыть страницу по URL')
    @make_screenshot
    def open(self, url: str):
        """Открыть страницу по url

        Args:
            url: Ссылка на страницу
        """
        logger.info(f'Открываем страницу {url}')
        self._driver.get(url)
        logger.success('Страница открыта!')

    @allure.step('Открыть предыдущую страницу по URL')
    @make_screenshot
    def back(self):
        """Открыть предыдущую страницу."""
        logger.info(f'Открываем предыдущую страницу')
        self._driver.back()
        logger.success('Предыдущая страница открыта!')

    @allure.step('Обновить текущую страницу')
    @make_screenshot
    def refresh(self):
        """Обновить текущую страницу."""
        logger.info('Обновляем текущую страницу')
        self._driver.refresh()
        logger.success('Страница обновлена!')

    @format_locator
    @allure.step('Ожидать присутствие элемента в DOM страницы')
    @make_screenshot
    def find_element(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Ожидать присутствия элемента в DOM страницы.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Ожидаем присутствие {locator} в DOM страницы в течение {timeout} секунд')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.presence_of_element_located(locator=locator.locator)
            )
            logger.success(f'{locator} найден в DOM страницы!')

            return element

        except TimeoutException as e:
            logger.error(msg := f'Не удалось найти {locator} в DOM страницы в течение {timeout} секунд')
            e.msg += f'\n{msg}'

            raise e

    @format_locator
    @allure.step('Искать несколько элементов по локатору')
    @make_screenshot
    def find_elements(self, locator: Locator, **kwargs) -> list[WebElement]:
        """Найти список элементов

        Args:
            locator: Инстанс Locator.
            **kwargs: Аргументы для форматирования локатора
        """

        logger.info(f'Ищем {locator}')
        elements = self._driver.find_elements(*locator.locator)
        logger.success('Элементы найдены и занесены в список!')

        return elements

    @format_locator
    @allure.step('Проверить присутствие элемента в DOM страницы')
    @make_screenshot
    def is_element_exists(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> bool:
        """Проверить, что элемент присутствует в DOM страницы.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора"""
        try:
            logger.info(f'Ожидаем присутствие {locator} в DOM страницы в течение {timeout} секунд')
            WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.presence_of_element_located(locator=locator.locator)
            )
            logger.success(f'{locator} найден в DOM страницы!')
            return True

        except TimeoutException:
            logger.info(f'Не удалось найти {locator} в DOM страницы в течение {timeout} секунд')
            return False

    @format_locator
    @allure.step('Ожидать видимость элемента')
    @make_screenshot
    def find_visible_element(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Ожидать присутствия элемента в DOM страницы и его видимости.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Ожидаем видимый {locator} в течение {timeout} секунд')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.visibility_of_element_located(locator=locator.locator)
            )
            logger.success('Элемент найден и виден!')

            return element

        except TimeoutException as e:
            logger.error(msg := f'Не удалось найти видимый {locator} в течение {timeout} секунд')
            e.msg += f'\n{msg}'

            raise e

    @format_locator
    @allure.step('Ожидать кликабельность элемента')
    @make_screenshot
    def find_clickable_element(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Ожидать, что элемент виден и активен и по нему можно кликнуть.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Ожидаем кликабельный {locator} в течение {timeout} секунд')
            element = WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.element_to_be_clickable(mark=locator.locator)
            )
            logger.success('Элемент найден и кликабелен')

            return element

        except TimeoutException as e:
            logger.error(msg := f'Не удалось найти кликабельный {locator} в течение {timeout} секунд')
            e.msg += f'\n{msg}'

            raise e

    @format_locator
    @allure.step('Кликнуть на элемент по локатору')
    @make_screenshot
    def click_by_locator(
            self, locator: Locator,
            timeout: float = driver_config.TIMEOUT,
            scroll: bool = False,
            **kwargs
    ) -> WebElement:
        """Найти элемент по локатору и кликнуть по нему.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            scroll: Использовать прокрутку к элементу перед кликом или нет
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Кликаем на {locator}')
            element = self.find_clickable_element(locator=locator, timeout=timeout)

            if scroll: self.scroll_into_view_by_element(element=element, locator=locator)

            element.click()
            logger.success('Клик успешно произведен!')

            return element

        except Exception as e:
            logger.error(msg := f'Не удалось совершить клик на {locator}')
            e.args = f'\n{msg}',

            raise e

    @allure.step('Кликнуть на элемент')
    @make_screenshot
    def click_by_element(self, element: WebElement, locator: Locator, scroll: bool = False) -> WebElement:
        """Кликнуть по элементу.

        Args:
            element: Инстанс WebElement
            locator: Инстанс Locator
            scroll: Использовать прокрутку к элементу перед кликом или нет
        """
        if scroll: self.scroll_into_view_by_element(element=element, locator=locator)

        try:
            logger.info(f'Кликаем на {locator}')
            element.click()
            logger.success(f'Клик успешно произведен!')

            return element

        except Exception as e:
            logger.error(msg := f'Не удалось совершить клик на {locator}')
            e.args = msg,

            raise e

    @format_locator
    @allure.step('Ввести значение в элемент по локатору')
    @make_screenshot
    def send_keys_by_locator(
            self,
            locator: Locator,
            keys: str,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ) -> WebElement:
        """Найти элемент по локатору и ввести в него значение.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            keys: Строка для ввода.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Заполняем {locator} значением "{keys}"')
            (element := self.click_by_locator(locator=locator, timeout=timeout)).clear()
            element.send_keys(keys)
            logger.success('Ввод  успешно произведен!')

            return element

        except Exception as e:
            logger.error(
                msg := f'Не удалось ввести в {locator}, значение "{keys}", с элементом нельзя взаимодействовать'
            )
            e.args = msg,

            raise e

    @staticmethod
    @allure.step('Ввести значение в элемент')
    @make_screenshot
    def send_keys_by_element(element: WebElement, locator: Locator, keys: str) -> WebElement:
        """Ввести значение в элемент.

        Args:
            element: Инстанс WebElement.
            locator: Инстанс Locator.
            keys: Строка для ввода.
        """
        try:
            logger.info(f'Заполняем {locator} значением "{keys}"')
            element.click()
            element.clear()
            element.send_keys(keys)
            logger.success(f'Ввод успешно произведен!')

            return element

        except Exception as e:
            logger.error(
                msg := f'Не удалось ввести в {locator}, значение "{keys}", с элементом нельзя взаимодействовать'
            )
            e.args = msg,

            raise e

    @format_locator
    @allure.step('Очистить элемент по локатору')
    @make_screenshot
    def clear_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> WebElement:
        """Найти элемент по локатору и очистить в нем текст.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Очищаем текст {locator}')
            (element := self.click_by_locator(locator=locator, timeout=timeout)).clear()
            logger.success('Элемент успешно очищен!')

            return element

        except Exception as e:
            logger.error(msg := f'Не удалось очистить {locator}, элемент находится в недопустимом состоянии')
            e.args = msg,

            raise e

    @staticmethod
    @allure.step('Очистить элемент')
    @make_screenshot
    def clear_by_element(element: WebElement, locator: Locator) -> WebElement:
        """Очистить текст в элементе.

        Args:
            element: Инстанс WebElement.
            locator: Инстанс Locator.
        """
        try:
            logger.info(f'Очищаем текст {locator}')
            element.click()
            element.clear()
            logger.success('Элемент очищен!')

            return element

        except Exception as e:
            logger.error(f'Не удалось очистить {locator}, элемент находится в недопустимом состоянии')
            e.args = f'Не удалось очистить {locator}, элемент находится в недопустимом состоянии'

            raise e

    @format_locator
    @allure.step('Проверить отображение элемента по локатору')
    def is_displayed_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> bool:
        """Найти элемент по локатору и проверить его видимость.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        return self.find_element(locator=locator, timeout=timeout).is_displayed()

    @staticmethod
    @allure.step('Проверить отображение элемента')
    @make_screenshot
    def is_displayed_by_element(element: WebElement) -> bool:
        """Проверить видимость элемента.

        Args:
            element: Инстанс WebElement.
        """
        return element.is_displayed()

    @format_locator
    @allure.step('Проверить активность элемента по локатору')
    @make_screenshot
    def is_enabled_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> bool:
        """Найти элемент по локатору и проверить активен ли он.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        return self.find_element(locator=locator, timeout=timeout).is_enabled()

    @staticmethod
    @allure.step('Проверить активность элемента')
    @make_screenshot
    def is_enabled_by_element(element: WebElement) -> bool:
        """Проверить активен ли элемент.

        Args:
            element: Инстанс WebElement.
        """
        return element.is_enabled()

    @format_locator
    @allure.step('Проверить выбран ли элемент по локатору')
    @make_screenshot
    def is_selected_by_locator(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs) -> bool:
        """Найти элемент по локатору и проверить выбран ли он.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        return self.find_element(locator=locator, timeout=timeout).is_selected()

    @staticmethod
    @allure.step('Проверить выбран ли элемент')
    @make_screenshot
    def is_selected_by_element(element: WebElement) -> bool:
        """Проверить выбран ли элемент.

        Args:
            element: Инстанс WebElement.
        """
        return element.is_selected()

    @format_locator
    @allure.step('Навести мышь на элемент по локатору')
    @make_screenshot
    def move_to_element_by_locator(
            self, locator: Locator,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ) -> WebElement:
        """Переместить мышь в центральную точку элемента в поле зрения через локатор.

        Note:
            Элемент должен находиться в окне просмотра, иначе команда выдаст ошибку.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        logger.info(f'Перемещаем указатель в центр {locator}')
        element = self.find_element(locator=locator, timeout=timeout)
        ActionChains(driver=self._driver).move_to_element(to_element=element).perform()
        logger.success('Указатель перемещён!')

        return element

    @allure.step('Навести мышь на элемент')
    @make_screenshot
    def move_to_element_by_element(self, element: WebElement, locator: Locator) -> WebElement:
        """Переместить мышь в центральную точку элемента в поле зрения.

        Note:
            Элемент должен находиться в окне просмотра, иначе команда выдаст ошибку.

        Args:
            element: Инстанс WebElement.
            locator: Инстанс Locator.
        """
        logger.info(f'Перемещаем указатель в центр {locator}')
        ActionChains(driver=self._driver).move_to_element(to_element=element).perform()
        logger.success('Указатель перемещён!')

        return element

    @format_locator
    @allure.step('Прокрутить страницу до элемента по локатору')
    @make_screenshot
    def scroll_into_view_by_locator(
            self,
            locator: Locator,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ) -> WebElement:
        """Найти элемент по локатору и прокрутить до него страницу.

        Note:
            Верхняя часть элемента будет выровнена по верхней части видимой области через локатор.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        logger.info(f'Прокручиваем страницу до {locator}')
        element = self.find_element(locator=locator, timeout=timeout)
        self._driver.execute_script("arguments[0].scrollIntoView();", element)
        logger.success('Страница прокручена!')

        return element

    @allure.step('Прокрутить страницу до элемента')
    @make_screenshot
    def scroll_into_view_by_element(self, element: WebElement, locator: Locator) -> WebElement:
        """Прокрутить страницу до элемента.

        Note:
            Верхняя часть элемента будет выровнена по верхней части видимой области через локатор.

        Args:
            element: Инстанс WebElement.
            locator: Инстанс Locator.
        """
        logger.info(f'Прокручиваем страницу до {locator}')
        self._driver.execute_script("arguments[0].scrollIntoView();", element)
        logger.success('Страница прокручена!')

        return element

    @format_locator
    @allure.step('Поиск элемента по тексту')
    @make_screenshot
    def find_element_by_formatted_locator(self, locator: Locator, **kwargs) -> WebElement:
        """Найти элемент с текстом на стринице.

        Args:
            locator: Инстанс Locator.
            **kwargs: Аргументы для форматирования локатора
        """
        logger.info(f'Ищем элемент с текстом {locator}')
        element = self.find_element(locator=locator)
        logger.success(f'Элемент отображается!')

        return element

    @format_locator
    @allure.step('Элемент отсутствует на странице')
    @make_screenshot
    def check_elements_missing_on_page(self, locator: Locator, timeout: float = driver_config.TIMEOUT, **kwargs):
        """Проверить отсутствие элемента на странице.

        Args:
            locator: Инстанс Locator.
            timeout: Количество секунд до тайм-аута ожидания.
            **kwargs: Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Ожидаем исчезновения {locator} из DOM дерева')
            WebDriverWait(driver=self._driver, timeout=timeout).until_not(
                method=EC.presence_of_element_located(locator=locator.locator)
            )
            logger.success('Элемент исчез из DOM дерева')

        except Exception as e:
            logger.error(msg := f'{locator} не исчез!')
            e.args = msg,

            raise e

    @allure.step('Переключить драйвер на вкладку со страницей по заданному адресу')
    @make_screenshot
    def switch_tab_by_url(self, url: str) -> None:
        """Переключиться на вкладку по заданному адресу.

        Args:
            url: Заданный адрес страницы.
        """
        try:
            logger.info(f'Переключаем драйвер на вкладку со страницей по адресу "{url}"')
            for handle in self._driver.window_handles:
                self._driver.switch_to.window(handle)

                if self._driver.current_url == url:
                    logger.success(f'Драйвер переключился на вкладку со страницей по адресу "{url}"')
                    return

        except Exception as e:
            logger.error(msg := f'Вкладка со страницей по адресу "{url}" не открылась')
            e.args = msg,

            raise e

    @allure.step('Переключить драйвер на вкладку со страницей по идентификатору')
    @make_screenshot
    def switch_tab_by_handle(self, handle: str) -> None:
        """Переключиться на окно по handle вкладки.

        Args:
            handle: Идентификатор вкладки.
        """
        try:
            logger.info(f'Переключаем драйвер на вкладку по идентификатору "{handle}"')
            self._driver.switch_to.window(handle)
            logger.success(f'Драйвер переключился на вкладку по идентификатору "{handle}"')

        except Exception as e:
            logger.error(msg := f'не удалось открыть вкладку с идентификатором "{handle}"')
            e.args = msg,

            raise e

    @format_locator
    @allure.step('Ожидание присутствия текста в элементе по локатору')
    @make_screenshot
    def wait_text_to_be_in_element_value_by_locator(
            self,
            locator: Locator,
            text: str,
            timeout: float = driver_config.TIMEOUT,
            **kwargs
    ):
        """Ожидать присутствие текста в элементе по локатору.

        Args:
            locator:    Инстанс Locator.
            timeout:    Количество секунд до тайм-аута ожидания.
            text:       Ожидаемый текст
            **kwargs:   Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Ожидаем текст "{text}" в "{locator}"')
            WebDriverWait(driver=self._driver, timeout=timeout).until(
                method=EC.text_to_be_present_in_element_value(locator=locator.locator, text_=text)
            )
            logger.success(f'Текст "{text}" находится в "{locator}"')

        except Exception as e:
            logger.error(msg := f'Текст "{text}" не появился в "{locator}"')
            e.args = msg,

            raise e

    @allure.step('Проверить видимость всех элементов')
    @make_screenshot
    def check_visibility_of_all_elements(self, locators: list[Locator], timeout: float = driver_config.TIMEOUT):
        """Проверить видимость всех элементов.

        Args:
            locators: Список объектов Locator.
            timeout: Количество секунд до тайм-аута ожидания.
        """
        errors = []
        for locator in locators:
            try:
                logger.info(f'Ожидаем видимый {locator} в течение {timeout} секунд')
                WebDriverWait(driver=self._driver, timeout=timeout).until(
                    method=EC.visibility_of_element_located(locator=locator.locator)
                )
                logger.success('Элемент найден и виден!')

            except TimeoutException:
                errors.append(str(locator))

        if errors:
            logger.error(msg := "Не удалось найти видимые элементы:\n\t{}".format("\n\t".join(errors)))
            pytest.fail(reason=msg)

    @format_locator
    @allure.step('Прикрепить файл в поле по локатору')
    @make_screenshot
    def attach_file(self, attachment_name, locator, **kwargs):
        """ Прикрепить файл к веб-элементу.

        Args:
            attachment_name: Наименование прикрепляемого файла из папки с тестовыми данными.
            locator: Наименование элемента.
            **kwargs:   Аргументы для форматирования локатора
        """
        try:
            logger.info(f'Прикрепление  файла {attachment_name} в поле {locator}')
            file_path = str(Config.test_data_dir / attachment_name)
            self.find_element(locator=locator).send_keys(file_path)
            logger.success(f'Файл {attachment_name} прикреплен')

        except Exception as e:
            logger.error(msg := f'Не удалось прикрепить файл {attachment_name} в поле {locator}')
            e.args = msg,

            raise e
