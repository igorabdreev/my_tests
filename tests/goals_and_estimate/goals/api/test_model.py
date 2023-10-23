from tests.goals_and_estimate.allure_constants import GoalsAPI
from api.goals_and_estimate.request_body.request_body import Request_body
from allure import story, title, link
from api.goals_and_estimate.goals.goals_request import Goals
from tests.constants import ERROR_STATUS_MSG
from users.goals import DIRECTOR_GOALS
from pytest import mark
from generators.randoms import get_random_string
from utilities.tools import get_link
from generators.keycloak import get_user_data_from_keycloak
from generators.date import get_datetime_with_offset
from generators.enums import KeycloakGen

@mark.usefixtures('set_up')
class TestGoals(GoalsAPI):
    goal_id: str
    goal_weight_id: str

    @staticmethod
    def set_up():
        TestGoals.current_year_start = get_datetime_with_offset(fmt='%Y-%m-%d')
        TestGoals.current_year_end = get_datetime_with_offset(fmt='%Y-%m-%d', days=1)
        TestGoals.current_year = int(get_datetime_with_offset(fmt='%Y'))
        # TestGoals.user_uuid = get_user_data_from_keycloak(user=DIRECTOR_GOALS, field=KeycloakGen.person_id)



    @link(*get_link(test=39545))
    @title('Создать цель')
    @mark.dependency(name='create_goal')
    def test_create_goal(self):
        response = Goals().create_goal(
            json=Request_body.json_create_goal(current_year_start=self.current_year_start,
                                               current_year_end=self.current_year_end,
                                               user_uuid= 'safdfgsfhggfshg')
        )

        # assert response.status_code == 201, ERROR_STATUS_MSG.format(code=response.status_code)
        assert response.model_is_valid()
        # TestGoals.goal_id = response.json()['id']
        print(response.json())

    @link(*get_link(test=39509))
    @title('Получить текущие цели')
    # @mark.dependency(depends=['create_goal'])
    def test_get_goal(self):
        response = Goals().get_goal(
            query_params={
                'year': self.current_year,
                'period': 'ALL'

            }
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
        assert response.model_is_valid()