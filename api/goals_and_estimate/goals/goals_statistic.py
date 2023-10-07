from requests import Response
from api.custom_requests import Request
from services import Services


class Statistics(Request):
    """Класс сервиса "Цели" для роутов statistics"""

    NAME = Services.APP_GOALS

    def __init__(self, version: int):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})
        self.url = f'{self.url}/api/v{version}/goals/statistics/board'


    def get_statistics_team_widget(self, year: int, period: str) -> Response:
        """Получить данные для вкладки коллеги - виджет"""
        return self.request(method='GET', url=f'{self.url}/team/widget', params={'year': year, 'period': period})

    def get_statistics_team_table(self, period, year: int, page_number: int, page_size: int) -> Response:
        """Получить данные для вкладки коллеги - таблица"""
        return self.request(
            method='GET',
            url=f'{self.url}/team/table',
            params={'year': year, 'period': period, 'pageNumber': page_number, 'pageSize': page_size}
        )
