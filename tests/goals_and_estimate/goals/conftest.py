from api.goals_and_estimate.goals.goals import Goals
from api.goals_and_estimate.goals.goals_statistic import Statistics
from pytest import fixture


@fixture
def get_weight_on_goal():
    """
    Фикстура для получения прогресса виджета на главной странице цели в Q1
    Response:
                r прогресс "Без учета веса целей"
                r2 прогресс "C учетом веса целей"
                response Тело ответа
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


@fixture()
def get_statistics_team_table():
    """
    Фикстура для получения прогресса виджета в статистике в Q1
    Response:
                r1 прогресс "Без учета веса целей"
                r2 прогресс "C учетом веса целей"
                response Тело ответа
    """
    response = Statistics(version=2).get_statistics_team_table(
        period='Q1',
        year=2023,
        page_number=1,
        page_size=10
    )
    r1 = response.json()['table']['data'][0]['progress']['progressWithDisableWeight']
    r2 = response.json()['table']['data'][0]['progress']['progressWithEnableWeight']
    r3 = response.json()['table']['data'][0]['goals']['countGoalsAll']
    return (r1, r2, r3)
