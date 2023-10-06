import datetime

from pytest import mark

from allure import story, title, link
from api.goals_and_estimate.goals.goals_statistic import Statistics
# from dto.app_goals.schema.goal_dto import OrgTeamShortResponse
# from dto.app_goals.schema.goal_enum import Period
# from dto.app_goals.schema.statistics_dto import (
#     StatisticsBoardDirectTableResponseV2,
#     StatisticsBoardStructureTableResponseV2,
#     StatisticsBoardTeamTableResponseV2,
#     StatisticsBoardWidgetResponseV2
# )
from tests.constants import ERROR_BODY_VALID_MSG, ERROR_STATUS_MSG
from tests.goals_and_estimate.allure_constants import GoalsAPI
from users.goals import DIRECTOR_GOALS
from utilities import model
from utilities.tools import get_link


@story('Проверки на получение данных для вкладки статистика')
@mark.dpm
@mark.usefixtures('set_up', 'auth_api')
@mark.parametrize('auth_api', [DIRECTOR_GOALS], indirect=True)
class TestGoalStatistics(GoalsAPI):
    current_year: int

    @staticmethod
    def set_up():
        TestGoalStatistics.current_year = datetime.datetime.now().year

    # @mark.prom
    # @link(*get_link(test=41155))
    # @title('Получить данные для вкладки прямое подчинение')
    # @mark.parametrize('period')
    # def test_get_statistics_direct_widget(self):
    #     assert (
    #        response := Statistics(version=2).get_statistics_direct_widget(year=self.current_year, period='Q1')
    #     ).status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
        # assert model.is_valid(model=StatisticsBoardWidgetResponseV2, response=response.json()), ERROR_BODY_VALID_MSG

    # @mark.prom
    # @link(*get_link(test=41156))
    # @title('Получить данные для вкладки таблица прямое подчинение')
    # # @mark.parametrize('period', Period)
    # @mark.parametrize('page_size', [10, 20, 50])
    # def test_get_statistics_direct_widget(self, period, page_size: int):
    #     assert (
    #        response := Statistics(version=2).get_statistics_direct_table(
    #            year=self.current_year,
    #            period=period,
    #            page_number=1,
    #            page_size=page_size
    #        )
    #     ).status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
    #     # assert model.is_valid(
    #     #     model=StatisticsBoardDirectTableResponseV2, response=response.json()
    #     # ), ERROR_BODY_VALID_MSG
    #
    # @mark.prom
    # @link(*get_link(test=41153))
    @title('Получить данные для вкладки коллеги - виджет')
    # @mark.parametrize('period')
    def test_get_statistics_team_widget(self, auth_api: str):

        response = Statistics(version=2).get_statistics_team_widget(year=self.current_year, period='Q1')
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
        # assert model.is_valid(model=StatisticsBoardWidgetResponseV2, response=response.json()), ERROR_BODY_VALID_MSG

    @mark.prom
    @link(*get_link(test=41154))
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
        # assert model.is_valid(model=StatisticsBoardTeamTableResponseV2, response=response.json()), ERROR_BODY_VALID_MSG

    # @link(*get_link(test=43802))
    # @title('Получить данные для вкладки структура - виджет')
    # @mark.parametrize('period')
    # def test_get_statistics_structure_widget(self, period, orgstructure_team: list[OrgTeamShortResponse]):
    #     assert (
    #        response := Statistics(version=2).get_statistics_structure_widget(
    #            year=self.current_year,
    #            period=period,
    #            department_id=orgstructure_team[0].id
    #        )
    #     ).status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
    #     assert model.is_valid(model=StatisticsBoardWidgetResponseV2, response=response.json()), ERROR_BODY_VALID_MSG
    #
    # @link(*get_link(test=43803))
    # @title('Получить данные для вкладки структура - таблица')
    # @mark.parametrize('period', Period)
    # @mark.parametrize('page_size', [10, 20, 50])
    # def test_get_statistics_structure_tabel(
    #         self,
    #         period: Period,
    #         page_size: int,
    #         orgstructure_team: list[OrgTeamShortResponse]
    # ):
    #     assert (
    #        response := Statistics(version=2).get_statistics_structure_tabel(
    #            period=period,
    #            year=self.current_year,
    #            department_id=orgstructure_team[0].id,
    #            page_number=1,
    #            page_size=page_size
    #        )
    #     ).status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
    #     assert model.is_valid(
    #         model=StatisticsBoardStructureTableResponseV2, response=response.json()
    #     ), ERROR_BODY_VALID_MSG
