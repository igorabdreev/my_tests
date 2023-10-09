from tests.goals_and_estimate.allure_constants import GoalsAPI
from api.goals_and_estimate.request_body.request_body import Request_body
from api.goals_and_estimate.goals.goals_kpi import Goals_kpi
from api.goals_and_estimate.goals.goals import Goals
from tests.constants import ERROR_STATUS_MSG
from allure import story, title, link
from pytest import mark
from users.goals import DIRECTOR_GOALS
from utilities.tools import get_link
from generators.enums import KeycloakGen
from generators.keycloak import get_user_data_from_keycloak
from generators.date import get_datetime_with_offset


@mark.dpm
@mark.usefixtures('set_up')
@mark.parametrize('auth_api', [DIRECTOR_GOALS], indirect=True)
@story('Цели')
class TestGoals(GoalsAPI):
    goal_id: str
    goal_weight_id: str

    @staticmethod
    def set_up():
        TestGoals.current_year_start = get_datetime_with_offset(fmt='%Y-%m-%d')
        TestGoals.user_uuid = get_user_data_from_keycloak(user=DIRECTOR_GOALS, field=KeycloakGen.person_id)

    @link(*get_link(test=39545))
    @title('Создать цель кпи')
    @mark.dependency(name='create_goal')
    def test_create_goal_kpi(self, auth_api: str):
        response = Goals().create_goal(
            json=Request_body.json_create_goal_with_kpi(user_uuid=self.user_uuid)
        )
        assert response.status_code == 201, ERROR_STATUS_MSG.format(code=response.status_code)
        TestGoals.goal_id = response.json()['id']
        TestGoals.key_result_id = \
        Goals(version=2).get_goals_on_id(goal_id=self.goal_id).json()['goal']['keyResults']['keyResults'][0]['id']

    @link(*get_link(test=39575))
    @title('Выполнить ключевой результат kpi')
    @mark.dependency(depends=['create_goal'])
    def test_done_key_result_kpi(self, auth_api: str):
        response = Goals_kpi().done_key_result_kpi(
            goal_id=self.goal_id,
            key_result_id=self.key_result_id,
            json=Request_body.json_done_key_result_kpi(value="1200", date=self.current_year_start)
        )

        assert response.status_code == 204, ERROR_STATUS_MSG.format(code=response.status_code)
        Goals().delete_goal(goal_id=self.goal_id)
