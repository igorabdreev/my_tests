from selenium.webdriver.common.by import By

from web.locator import Locator
from web.pages.goals_and_estimate.goals.base_page import GoalsBasePage


class AdminPage(GoalsBasePage):
    """Класс станицы Админ сервиса Цели"""

    TEMPLATE_TEXT_LOCATOR = Locator(name='{text}', locator=(By.XPATH, '//*[text()="{text}"]'))

    def open_admin_page(self):
        """Открыть страницу администратора приложения цели"""
        self.open(url=f'{self.url}/admin')

    def check_goal_elements_admin(self):
        """Проверить элементы страницы цели в разделе администратора"""
        for text in [
            'настроить цели', 'вход от имени сотрудника', 'загрузка целей', 'выгрузка целей', 'настроить приложение'
        ]:
            self.find_element(locator=self.TEMPLATE_TEXT_LOCATOR, text=text)

