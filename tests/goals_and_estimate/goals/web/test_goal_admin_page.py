from pytest import mark

from allure import link, story, title, step
from tests.goals_and_estimate.allure_constants import GoalsWeb
from users.goals import DIRECTOR_GOALS
from utilities.tools import get_link
from web.pages.goals_and_estimate.goals.admin_page import AdminPage


@story('Проверить отображение страницы администратора сервиса Цели и видимость функциональных элементов')
class TestGoalAdminPage(GoalsWeb):

    @link(*get_link(test=28654))
    @title('Проверить отображение элементов на странице администратора для сервиса "Цели"')
    @mark.parametrize('open_page', [(DIRECTOR_GOALS, AdminPage)], indirect=True)
    def test_check_goal_admin_page(self, open_page):

        open_page.open_admin_page()

        with step('Проверить элементы страницы цели в разделе администратора'):
            open_page.check_goal_elements_admin()
