import pytest
from tests.goals_and_estimate.allure_constants import GoalsAPI
from api.goals_and_estimate.request_body.request_body import Request_body
from allure import story, title, link
from api.goals_and_estimate.goals.goals import Goals
from api.goals_and_estimate.goals.goals_statistic import Statistics
from api.goals_and_estimate.request_body.request_body import Request_body
from tests.constants import Ansver

from users.goals import EMPLOYEE_GOALS
from pytest import mark
from generators.randoms import get_random_string
from utilities.tools import get_link
from generators.keycloak import get_user_data_from_keycloak
from generators.date import get_datetime_with_offset
from generators.enums import KeycloakGen


@mark.usefixtures('set_up')
@mark.parametrize('auth_api', [EMPLOYEE_GOALS], indirect=True)
class TestCrateGoalsAndCheckStatistic(GoalsAPI):
    goal_id: str
    key_result_b: str
    key_result_m: str

    @staticmethod
    def set_up():
        TestCrateGoalsAndCheckStatistic.user_uuid = get_user_data_from_keycloak(user=EMPLOYEE_GOALS,
                                                                                field=KeycloakGen.person_id)
        TestCrateGoalsAndCheckStatistic.current_year = int(get_datetime_with_offset(fmt='%Y'))

    @mark.dependency(name='create_goal')
    def test_1(self, auth_api: str):
        """
        Тест создания цели с КР, выполнения КР и получения
        goal_id - id цели
        kr_id - id КР
        """
        response = Goals().create_goal(
            json=Request_body.json_create_goal_with_kr(user_uuid=self.user_uuid, yearGoal=False, startDate="2023-01-01",
                                                       endDate="2023-03-31",
                                                       startDate_kr="2023-01-01", endDate_kr="2023-03-31",
                                                       weight={'Q1': 50, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0}
                                                       )
        )
        TestCrateGoalsAndCheckStatistic.goal_id = response.json()['id']
        TestCrateGoalsAndCheckStatistic.key_result_b = response.json()['keyResults']['keyResultInProgress'][0]['id']

    @mark.dependency(depends=['create_goal'])
    def test_done_key_result(self, auth_api: str):
        """Выполнить бинарный КР
        """
        Goals().done_key_result(
            goal_id=self.goal_id,
            key_result_id=self.key_result_b,
            json={'status': "DONE"}
        )

    def test_get_weight_on_goal(self, auth_api: str, get_weight_on_goal):
        """Тест для проверки получения прогресса виджета на главной странице цели
        """
        assert get_weight_on_goal[0] == 100, Ansver.ERROR_MSG_WITHOUT_WIDGET.format(
            json=get_weight_on_goal[0])
        assert get_weight_on_goal[1] == 50, Ansver.ERROR_MSG_WITH_WIDGET.format(
            json=get_weight_on_goal[1])

    def test_statistic_in_statistic(self, auth_api: str, get_statistics_team_table, get_weight_on_goal):
        """Тест для проверки прогресса виджета в статистике в Q1 с виджетом на главной
        """
        assert get_statistics_team_table[0] == get_weight_on_goal[0]
        assert get_statistics_team_table[1] == get_weight_on_goal[1]
        assert get_statistics_team_table[2] == 1

    def test_create_key_result(self, auth_api: str):
        """Создание метрического КР
        """
        response = Goals().create_key_result(goal_id=self.goal_id,
                                             json=Request_body.json_create_kr_metric(endDate="2023-03-31"))
        print(response.json())
        TestCrateGoalsAndCheckStatistic.key_result_m = response.json()['id']

    def test_get_weight_on_goal_after_add_metric(self, auth_api: str, get_weight_on_goal):
        """Тест для проверки получения прогресса виджета на главной странице цели после добавления метрики
        """
        assert get_weight_on_goal[0] == 50, Ansver.ERROR_MSG_WITHOUT_WIDGET_AFTER_ADD_METRIC.format(
            json=get_weight_on_goal[0])
        assert get_weight_on_goal[1] == 25, Ansver.ERROR_MSG_WITH_WIDGET_AFTER_ADD_METRIC.format(
            json=get_weight_on_goal[1])

    def test_statistic_in_statistic_after_add_metric(self, auth_api: str, get_statistics_team_table,
                                                     get_weight_on_goal):
        """Тест для проверки прогресса виджета в статистике в Q1 с виджетом на главной после добавления метрики
        """
        assert get_statistics_team_table[0] == get_weight_on_goal[0]
        assert get_statistics_team_table[1] == get_weight_on_goal[1]
        assert get_statistics_team_table[2] == 1

    def test_done_key_result_metric(self, auth_api: str):
        """Выполнить метрический КР
        """
        Goals().done_key_result_metric(
            goal_id=self.goal_id,
            key_result_id=self.key_result_m,
            json={'currentProgress': 80}
        )

    def test_get_weight_on_goal_after_done_metric(self, auth_api: str, get_weight_on_goal):
        """Тест для проверки получения прогресса виджета на главной странице цели после выполнения метрики
        """
        assert get_weight_on_goal[0] == 90, Ansver.ERROR_MSG_WITHOUT_WIDGET_AFTER_DONE_METRIC.format(
            json=get_weight_on_goal[0])
        assert get_weight_on_goal[1] == 45, Ansver.ERROR_MSG_WITH_WIDGET_AFTER_DONE_METRIC.format(
            json=get_weight_on_goal[1])

    def test_statistic_in_statistic_after_done_metric(self, auth_api: str, get_statistics_team_table,
                                                      get_weight_on_goal):
        """Тест для проверки прогресса виджета в статистике в Q1 с виджетом на главной после выполнения метрики
        """
        assert get_statistics_team_table[0] == get_weight_on_goal[0]
        assert get_statistics_team_table[1] == get_weight_on_goal[1]
        assert get_statistics_team_table[2] == 1

        def test_edit_key_result_metric(self, auth_api: str):
            """
            Изменение значения метрики
            """
            Goals().done_key_result_metric(
                goal_id=self.goal_id,
                key_result_id=self.key_result_m,
                json={'currentProgress': 40}
            )

    def test_get_weight_on_goal_after_edit_weight(self, auth_api: str, get_weight_on_goal):
        """Тест для проверки получения прогресса виджета на главной странице цели после изменения метрики
        """
        assert get_weight_on_goal[0] == 90, Ansver.ERROR_MSG_WITHOUT_WIDGET_AFTER_EDIT_METRIC.format(
            json=get_weight_on_goal[0])
        assert get_weight_on_goal[1] == 45, Ansver.ERROR_MSG_WITH_WIDGET_AFTER_EDIT_METRIC.format(
            json=get_weight_on_goal[1])

    def test_statistic_in_statistic_after_edit_weight(self, auth_api: str, get_statistics_team_table,
                                                          get_weight_on_goal):
        """Тест для проверки прогресса виджета после изменения прогресса метрического КР
        """
        assert get_weight_on_goal[0] == get_statistics_team_table[0]
        assert get_statistics_team_table[1] == get_weight_on_goal[1]

    # def test_edit_weight_goal(self, auth_api: str):
    #     """Изменение веса цели
    #     """
    #     Goals().edit_weight_goal(
    #         goal_id=self.goal_id,
    #         json=Request_body().json_create_weight()
    #     )
    #
    #
    # def test_statistic_in_statistic_after_edit_weight(self, auth_api: str, get_statistics_team_table, get_weight_on_goal):
    #     """Тест для проверки прогресса виджета в после изменения веса
    #     """
    #     assert get_weight_on_goal[1] == 22, ERROR_MSG_WIDGET.format(
    #         json=get_weight_on_goal[1])
    #     assert get_statistics_team_table[1] == get_weight_on_goal[1]



    def test_delete_key_result(self, auth_api: str):
        Goals().delete_key_result(
            goal_id=self.goal_id,
            key_result_id=self.key_result_b,
            key_result_type="binary"
        )

    def test_get_weight_on_goal_after_delete_kr(self, auth_api: str, get_weight_on_goal):
        """Тест для проверки получения прогресса виджета на главной странице цели после изменения метрики
        """
        assert get_weight_on_goal[0] == 80, Ansver.ERROR_MSG_WITHOUT_WIDGET_AFTER_DELETE_METRIC.format(
            json=get_weight_on_goal[0])
        assert get_weight_on_goal[1] == 40, Ansver.ERROR_MSG_WITH_WIDGET_AFTER_DELETE_METRIC.format(
            json=get_weight_on_goal[1])

    def test_statistic_in_statistic_after_delete_kr(self, auth_api: str, get_statistics_team_table,
                                                          get_weight_on_goal):
        """Тест для проверки прогресса виджета после изменения прогресса метрического КР
        """
        assert get_weight_on_goal[0] == get_statistics_team_table[0]
        assert get_statistics_team_table[1] == get_weight_on_goal[1]

        Goals().delete_goal(goal_id=self.goal_id)

    # Добавить описание ошибки в статистики
    # Ждать пока починят обновление статистики при изменении веса
    # Добавить dependency