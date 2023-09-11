from tests.goals_and_estimate.allure_constants import GoalsAPI
from allure import story, title, link
from api.goals_and_estimate.goals.goals import Goals
from tests.constants import ERROR_STATUS_MSG
from users.goals import DIRECTOR_GOALS
from pytest import mark
from generators.randoms import get_random_string
from utilities.tools import get_link
from generators.keycloak import get_user_data_from_keycloak
from generators.date import get_datetime_with_offset
from generators.enums import KeycloakGen


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
        TestGoals.current_year_end = get_datetime_with_offset(fmt='%Y-%m-%d', days=1)
        TestGoals.current_year = int(get_datetime_with_offset(fmt='%Y'))
        TestGoals.user_uuid = get_user_data_from_keycloak(user=DIRECTOR_GOALS, field=KeycloakGen.person_id)

    @link(*get_link(test=39545))
    @title('Создать цель')
    @mark.dependency(name='create_goal')
    def test_create_goal(self, auth_api: str):
        response = Goals().create_goal(
            json={
                'assignees': [],
                'description': '',
                'endDate': self.current_year_end,
                'keyResults': [],
                'periodEnd': 'Q4',
                'periodStart': 'Q4',
                'reporterId': self.user_uuid,
                'startDate': self.current_year_start,
                'title': get_random_string(),
                'type': 'STANDARD',
                'visibility': 'VISIBLE',
                'weight': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0},
                'yearGoal': False,
                'fileIds': []
            }
        )
        assert response.status_code == 201, ERROR_STATUS_MSG.format(code=response.status_code)
        TestGoals.goal_id = response.json()['id']

    @link(*get_link(test=39509))
    @title('Получить текущие цели')
    @mark.dependency(depends=['create_goal'])
    def test_get_goal(self, auth_api: str):
        response = Goals().get_goal(
            query_params={
                'year': self.current_year,
                'period': 'ALL'

            }
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39576))
    @title('Редактировать цель')
    @mark.dependency(depends=['create_goal'])
    def test_edit_goal(self, auth_api: str):
        response = Goals(version=2).edit_goal(
            goal_id=self.goal_id,
            json={
                "title": get_random_string(),
                "description": get_random_string(),
                "visibility": "VISIBLE",
                "isRiskState": True,
                "riskComment": get_random_string(),
                "startDate": self.current_year_start,
                "endDate": self.current_year_end,
                "periodStart": "Q1",
                "periodEnd": "Q4",
                "isYearGoal": True,
                'weight': {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0}
            }
        )
        assert response.status_code == 204, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39529))
    @title('Получение целей для панели целей')
    @mark.dependency(depends=['create_goal'])
    def test_get_goal_for_goals_bar(self, auth_api: str):
        response = Goals().get_goal_for_goals_panel(
            query_params={
                'year': self.current_year,
                'period': 'ALL',
                'view': 'STANDARD'
            }
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39545))
    @title('Получение данных для отображения модалки "Создание цели"')
    @mark.dependency(depends=['create_goal'])
    def test_get_modal_window_for_create_goal(self, auth_api: str):
        response = Goals().get_modal_window_for_create_goal()
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39576))
    @title('Редактировать вес цели для цели id')
    @mark.dependency(depends=['create_goal'])
    def test_edit_weight_goal(self, auth_api: str):
        response = Goals().edit_weight_goal(
            goal_id=self.goal_id,
            json={
                "Q1": 10,
                "Q2": 10,
                "Q3": 10,
                "Q4": 10,
                "Y": 10
            }
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39543))
    @title('Получить цель по id')
    @mark.dependency(depends=['create_goal'])
    def test_get_goals_on_id(self, auth_api: str):
        response = Goals().get_goals_on_id(
            goal_id=self.goal_id
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39530))
    @title('Получить вес цели на год')
    @mark.dependency(depends=['create_goal'])
    def test_get_weight(self, auth_api: str):
        response = Goals().get_weight(
            query_params={'year': self.current_year}
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39531))
    @title('Получить вес всех целей на год')
    @mark.dependency(name='get_weight_rebalance', depends=['create_goal'])
    def test_get_weight_rebalance(self, auth_api: str):
        response = Goals().get_weight_rebalance(
            query_params={'year': self.current_year}
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)
        TestGoals.goal_weight_id = response.json()[2]['goalWeightId']
        TestGoals.goalid = response.json()[2]['goalId']

    @link(*get_link(test=39542))
    @title('Изменить вес всех целей на год')
    @mark.dependency(depends=['get_weight_rebalance'])
    def test_patch_weight_rebalance(self, auth_api: str):
        response = Goals().patch_weight_rebalance(
            json={
                'goalWeightsRebalance': [
                    {
                        'goalWeightId': self.goal_weight_id,
                        'goalId': self.goalid,
                        'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'Y': 0
                    }
                ]
            }
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39597))
    @title('Получить общий прогресс по целям')
    @mark.dependency(depends=['create_goal'])
    def test_get_goals_progress(self, auth_api: str):
        response = Goals().get_goals_progress(
            query_params={
                'year': self.current_year,
                'period': 'ALL',
                'personId': self.user_uuid
            }
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39548))
    @title('Создать ключевой результат у цели')
    @mark.dependency(name='create_key_result', depends=['create_goal'])
    def test_create_key_result(self, auth_api: str):
        response = Goals().create_key_result(
            goal_id=self.goalid,
            json={
                'description': get_random_string(),
                'endDate': self.current_year_end,
                'title': get_random_string(),
                'type': "BINARY"
            }
        )
        assert response.status_code == 201, ERROR_STATUS_MSG.format(code=response.status_code)
        TestGoals.key_result = response.json()['id']

    @link(*get_link(test=39575))
    @title('Выполнить ключевой результат')
    @mark.dependency(depends=['create_key_result'])
    def test_done_key_result(self, auth_api: str):
        response = Goals().done_key_result(
            goal_id=self.goalid,
            key_result_id=self.key_result,
            json={'status': "DONE"}
        )
        assert response.status_code == 204, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39575))
    @title('Удалить ключевой результат у цели')
    @mark.dependency(depends=['create_key_result'])
    def test_delete_key_result(self, auth_api: str):
        response = Goals().delete_key_result(
            goal_id=self.goalid,
            key_result_id=self.key_result,
            key_result_type="binary"
        )
        assert response.status_code == 204, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39571))
    @title('Получить все события внутри цели')
    @mark.dependency(depends=['create_goal'])
    def test_get_events(self, auth_api: str):
        response = Goals().get_events(
            goal_id=self.goal_id
        )
        assert response.status_code == 200, ERROR_STATUS_MSG.format(code=response.status_code)

    @link(*get_link(test=39547))
    @title('Удалить цель')
    @mark.dependency(depends=['create_goal'])
    def test_delete_goal(self, auth_api: str):
        response = Goals().delete_goal(
            goal_id=self.goal_id
        )
        assert response.status_code == 204, ERROR_STATUS_MSG.format(code=response.status_code)
