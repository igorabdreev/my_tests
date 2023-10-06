from uuid import UUID
from requests import Response
from api.custom_requests import Request
# from dto.app_goals.sc-hema.goal_enum import Period
from services import Services


class Statistics(Request):
    """Класс сервиса "Цели" для роутов statistics"""

    NAME = Services.APP_GOALS

    def __init__(self, version: int):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})
        self.url = f'{self.url}/api/v{version}/goals/statistics/board'

    # def get_statistics_direct_widget(self, year: int, period) -> Response:
    #     """Получить данные для вкладки прямое подчинение"""
    #     return self.request(method='GET', url=f'{self.url}/direct/widget', params={'year': year, 'period': period})

    # def get_statistics_direct_table(self, period, year: int, page_number: int, page_size: int) -> Response:
    #     """Получить данные для вкладки таблица прямое подчинение"""
    #     return self.request(
    #         method='GET',
    #         url=f'{self.url}/direct/table',
    #         params={'year': year, 'period': period, 'pageNumber': page_number, 'pageSize': page_size}
    #     )
    #
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
    #
    # def get_statistics_structure_widget(self, period, year: int, department_id: UUID) -> Response:
    #     """Получить данные для вкладки структура - виджет"""
    #     return self.request(
    #         method='GET',
    #         url=f'{self.url}/structure/widget',
    #         params={'year': year, 'period': period, 'departmentId': department_id}
    #     )

    # def get_statistics_structure_tabel(
    #         self,
    #         period: ,
    #         year: int,
    #         department_id: UUID,
    #         page_number: int,
    #         page_size: int
    # ) -> Response:
    #     """Получить данные для вкладки структура - таблица"""
    #     return self.request(
    #         method='GET',
    #         url=f'{self.url}/structure/table',
    #         params={
    #            'period': period,
    #            'year': year,
    #            'departmentId': department_id,
    #            'pageNumber': page_number,
    #            'pageSize': page_size
    #         }
    #     )
