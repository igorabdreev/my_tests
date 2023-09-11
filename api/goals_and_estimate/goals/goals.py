from services import Services
from requests import Response
from api.custom_requests import Request


class Goals(Request):
    """Класс сервиса "Цели" """

    NAME = Services.APP_GOALS

    def __init__(self, version: int = 1):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})
        self.url = f'{self.url}/api/v{version}'

    def create_goal(self, json: dict) -> Response:
        """ Создать цель

        Args:
            json: тело запроса
        """
        return self.request(method='post', url=f'{self.url}/goals', json=json)

    def get_goal(self, query_params: dict) -> Response:
        """ Получить текущие цели

        Args:
            query_params: query параметры запроса
        """
        return self.request(method='GET', url=f'{self.url}/dashboard/bar', params=query_params)

    def get_modal_window_for_create_goal(self) -> Response:
        """Получение данных для отображения модалки 'Создание цели'

        """
        return self.request(method='GET', url=f'{self.url}/goals')

    def edit_goal(self, goal_id: str, json: dict) -> Response:
        """Редактировать цель

        Args:
            goal_id: id цели
            json: тело запроса
        """
        return self.request(method='PATCH', url=f'{self.url}/goals/{goal_id}', json=json)

    def get_goal_for_goals_panel(self, query_params: dict) -> Response:
        """Получение целей для панели целей

        Args:
            query_params: query параметры запроса
        """

        return self.request(method='GET', url=f'{self.url}/goals/panel', params=query_params)

    def edit_weight_goal(self, goal_id: str, json: dict) -> Response:
        """Редактировать вес цели для цели id

        Args:
            goal_id: id цели
            json: тело запроса
        """

        return self.request(method='PATCH', url=f'{self.url}/goals/{goal_id}/weight', json=json)

    def get_goals_on_id(self, goal_id: str) -> Response:
        """Получить цель по id

        Args:
            goal_id: id цели
        """
        return self.request(method='GET', url=f'{self.url}/goals/{goal_id}')

    def get_weight(self, query_params: dict) -> Response:
        """Получить вес цели на год

        Args:
            query_params: query параметры запроса
        """
        return self.request(method='GET', url=f'{self.url}/goals/weight', params=query_params)

    def get_weight_rebalance(self, query_params: dict) -> Response:
        """Получить вес всех целей на год

        Args:
            query_params: query параметры запроса
        """
        return self.request(method='GET', url=f'{self.url}/goals/weight/rebalance', params=query_params)

    def patch_weight_rebalance(self, json: dict) -> Response:
        """Изменить вес цели

        Args:
            json: тело запроса
        """
        return self.request(method='PATCH', url=f'{self.url}/goals/weight/rebalance', json=json)

    def get_goals_progress(self, query_params: dict) -> Response:
        """Получить общий прогресс по целям

        Args:
            query_params: query параметры запроса
        """
        return self.request(method='GET', url=f'{self.url}/goals/progress', params=query_params)

    def create_key_result(self, goal_id: str, json: dict) -> Response:
        """Создать ключевой результат у цели

        Args:
            goal_id: id цели
            json: тело запроса
        """
        return self.request(method='POST', url=f'{self.url}/goals/{goal_id}/key-result', json=json)

    def delete_key_result(self, goal_id: str, key_result_id: str, key_result_type: str) -> Response:
        """Удалить ключевой результат у цели

        Args:
            goal_id: id цели
            key_result_id: id ключевого результата
            key_result_type: тип ключевого результата (BINARY, MATRIC)
        """
        return self.request(
            method='DELETE',
            url=f'{self.url}/goals/{goal_id}/key-result/{key_result_type}/{key_result_id}'
        )

    def get_events(self, goal_id: str) -> Response:
        """Получить все события внутри цели

        Args:
            goal_id: id цели
        """
        return self.request(method='GET', url=f'{self.url}/goals/{goal_id}/events')

    def done_key_result(self, goal_id: str, key_result_id: str, json: dict) -> Response:
        """Выполнить ключевой результат

        Args:
            goal_id: id цели
            key_result_id: id ключевого результата
            json: тело запроса
        """
        return self.request(
            method='PATCH',
            url=f'{self.url}/goals/{goal_id}/key-result/binary/{key_result_id}/progress',
            json=json
        )

    def delete_goal(self, goal_id: str) -> Response:
        """Удалить цель

        Args:
            goal_id: id цели
        """
        return self.request(method='DELETE', url=f'{self.url}/goals/{goal_id}')
