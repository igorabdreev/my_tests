import datetime
from pytest import mark
from allure import story, title, link
from api.goals_and_estimate.goals.goals_statistic import Statistics
from tests.constants import ERROR_BODY_VALID_MSG, ERROR_STATUS_MSG
from tests.goals_and_estimate.allure_constants import GoalsAPI
from users.goals import EMPLOYEE_GOALS
from utilities import model
from utilities.tools import get_link


@story('Проверки на получение данных для вкладки статистика')
@mark.dpm
@mark.usefixtures('set_up', 'auth_api')
@mark.parametrize('auth_api', [EMPLOYEE_GOALS], indirect=True)
class TestGoalStatistics(GoalsAPI):
    current_year: int

    @staticmethod
    def set_up():
        TestGoalStatistics.current_year = datetime.datetime.now().year

    # @mark.prom
    # @link(*get_link(test=41153))
    @title('Получить данные для вкладки коллеги - виджет')
    # @mark.parametrize('period')
    def test_get_statistics_team_widget(self, auth_api: str):
        response = Statistics(version=2).get_statistics_team_widget(year=self.current_year, period='Q1')
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    # @mark.prom
    # @link(*get_link(test=41154))
    @title('Получить данные для вкладки коллеги - таблица')
    # @mark.parametrize('period')
    @mark.parametrize('page_size', [10, 20, 50])
    def test_get_statistics_team_table(self, page_size: int):
        assert (
                   response := Statistics(version=2).get_statistics_team_table(
                       period='Q1',
                       year=self.current_year,
                       page_number=1,
                       page_size=page_size
                   )
               ).status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
        print(response.json())
