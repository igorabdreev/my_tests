from tests.goals_and_estimate.allure_constants import GoalsAPI
from api.goals_and_estimate.goals.goals_kpi import Goals_kpi
from api.goals_and_estimate.goals.goals import Goals
from generators.randoms import get_random_string
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
            # TestGoals.current_year_end = get_datetime_with_offset(fmt='%Y-%m-%d', days=1)
            # TestGoals.current_year = int(get_datetime_with_offset(fmt='%Y'))
        TestGoals.user_uuid = get_user_data_from_keycloak(user=DIRECTOR_GOALS, field=KeycloakGen.person_id)

    @link(*get_link(test=39545))
    @title('Создать цель кпи')
    @mark.dependency(name='create_goal')
    def test_create_goal_kpi(self, auth_api: str):
        response = Goals().create_goal(
            json={
                'assignees': [],
                'description': '',
                'startDate': "2023-01-01",
                'endDate': "2023-12-31",
                'keyResults': [{"id": "-1",
                                "type": "KPI",
                                "title": get_random_string(),
                                "description": "",
                                "targetValue": 1000,
                                "valueMin": 800,
                                "valueMax": 1200,
                                "progressMin": 85,
                                "progressMax": 120,
                                "metric": "штук",
                                "status": "DONE",
                                "startDate": "2023-10-06T06:14:28.732Z",
                                "endDate": "2023-12-31"}],
                'periodEnd': 'Q1',
                'periodStart': 'Q4',
                'reporterId': self.user_uuid,
                'title': get_random_string(),
                'type': 'STANDARD',
                'visibility': 'VISIBLE',
                'weight': {'Q1': 5, 'Q2': 5, 'Q3': 5, 'Q4': 5, 'Y': 5},
                'yearGoal': True,
                'fileIds': []
            }
        )
        assert response.status_code == 201, ERROR_STATUS_MSG.format(code=response.status_code)
        TestGoals.goal_id = response.json()['id']
        TestGoals.key_result_id = Goals(version=2).get_goals_on_id(goal_id=self.goal_id).json()['goal']['keyResults']['keyResults'][0]['id']


    @link(*get_link(test=39575))
    @title('Выполнить ключевой результат kpi')
    @mark.dependency(depends=['create_goal'])
    def test_done_key_result_kpi(self, auth_api: str):
        response = Goals_kpi().done_key_result_kpi(
                goal_id=self.goal_id,
                key_result_id=self.key_result_id,
                json={
                    "comment": '',
                    "date": self.current_year_start,
                    "value": '1200'

                }
            )

        assert response.status_code == 204, ERROR_STATUS_MSG.format(code=response.status_code)
        Goals().delete_goal(goal_id=self.goal_id)

