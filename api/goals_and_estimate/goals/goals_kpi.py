from services import Services
from requests import Response
from api.custom_requests import Request
from api.goals_and_estimate.goals.goals_request import Goals

class Goals_kpi(Request):
    """Класс сервиса "Цели" """

    NAME = Services.APP_GOALS

    def __init__(self, version: int = 1):
        super().__init__()
        self.headers.update({"Content-Type": "application/json"})
        self.url = f'{self.url}/api/v{version}'

    def done_key_result_kpi(self, goal_id: str, key_result_id: str, json: dict) -> Response:
        """Выполнить ключевой результат кпи

        Args:
            goal_id: id цели
            key_result_id: id ключевого результата
            json: тело запроса
        """
        return self.request(
            method='POST',
            url=f'{self.url}/goals/{goal_id}/key-result/kpi/{key_result_id}/progress',
            json=json
        )