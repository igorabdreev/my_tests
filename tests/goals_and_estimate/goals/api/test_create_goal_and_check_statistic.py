import pytest

from tests.goals_and_estimate.allure_constants import GoalsAPI
from api.goals_and_estimate.request_body.request_body import Request_body
from allure import story, title, link
from api.goals_and_estimate.goals.goals import Goals
from api.goals_and_estimate.goals.goals_statistic import Statistics
from api.goals_and_estimate.request_body.request_body import Request_body
from tests.constants import ERROR_MSG_WIDGET
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
    kr_id: str

    @staticmethod
    def set_up():
        TestCrateGoalsAndCheckStatistic.user_uuid = get_user_data_from_keycloak(user=EMPLOYEE_GOALS,
                                                                                field=KeycloakGen.person_id)
        TestCrateGoalsAndCheckStatistic.current_year = int(get_datetime_with_offset(fmt='%Y'))

    @staticmethod
    @pytest.fixture()
    def get_weight_on_goal():
        """
        Фикстура для получения прогресса виджета на главной странице цели

        """
        response = Goals().get_goal(
            query_params={
                'year': 2023,
                'period': 'Q1'

            }
        )
        r = response.json()['progress']['disableWeight']
        r2 = response.json()['progress']['enableWeight']

        return (r, r2, response)

    @mark.dependency(name='create_goal')
    def test_1(self, auth_api: str):
        """Тест создания цели с КР, выполнения КР и получения
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
        TestCrateGoalsAndCheckStatistic.kr_id = response.json()['keyResults']['keyResultInProgress'][0]['id']
        response = Goals().done_key_result(
            goal_id=self.goal_id,
            key_result_id=self.kr_id,
            json={'status': "DONE"}
        )

    def test_get_weight_on_goal(self, auth_api: str, get_weight_on_goal):
        """Тест для проверки получения прогресса виджета на главной странице цели
        """
        assert get_weight_on_goal[0] == 100, ERROR_MSG_WIDGET.format(
            json=get_weight_on_goal[3].json()['progress']['disableWeight'])
        assert get_weight_on_goal[1] == 50, ERROR_MSG_WIDGET.format(
            json=get_weight_on_goal[3].json()['progress']['enableWeight'])



    def test_statistic_in_statistic(self, auth_api: str, get_weight_on_goal):
        response1 = Statistics(version=2).get_statistics_team_table(
            period='Q1',
            year=self.current_year,
            page_number=1,
            page_size=10
        )

        assert response1.json()['table']['data'][0]['progress']['progressWithDisableWeight'] == get_weight_on_goal[0]
        assert response1.json()['table']['data'][0]['progress']['progressWithEnableWeight'] == get_weight_on_goal[1]
        assert response1.json()['table']['data'][0]['goals']['countGoalsAll'] == 1
        response = Goals().create_key_result(goal_id=self.goal_id,
                                             json=Request_body.json_create_kr_metric(endDate="2023-03-31"))

        # response = TestCrateGoalsAndCheckStatistic.test_get_weight_on_goal()
        print(response)

        Goals().delete_goal(goal_id=self.goal_id)
