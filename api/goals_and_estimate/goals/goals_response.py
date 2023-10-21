from typing import Any, Optional, Union
import requests
import json

from pydantic import BaseModel
from requests import Response
from utilities import model


class GoalServiceResponse:
    """ Класс, расширяющий стандартный Response, поддержкой работы с моделями"""
    # response: Response
    # data: Optional[dict[Any, Any]]
    # model: type[BaseModel]

    def __init__(
        self,
        response: requests.Response,
        data_root: Optional[str] = None,
        data_model: Optional[type[BaseModel]] = None
    ):
        self.model = data_model
        self.response = response
        if response.content:
            self.data = response.json().get(data_root) if data_root else response.json()
        else:
            self.data = None

    @property
    def status_code(self) -> int:
        """ Вернуть код ответа """
        return self.response.status_code

    def json(self) -> Optional[dict[Any, Any]]:
        """ Вернуть весь ответ как json """
        return self.response.json() if self.response.content else None

    def is_success(self) -> Optional[bool]:
        """ Проверить success в ответе """
        return self.response.json().get('success') if self.response.content else None

    def dto(self) -> Union[list[BaseModel], BaseModel]:
        """ Вернуть ответ от указанного корневого элемента как dto """
        if isinstance(self.data, list):
            return [self.model.parse_obj(item) for item in self.data]
        else:
            return self.model.parse_obj(self.data)

    def model_is_valid(self) -> bool:
        """ Вернуть валидность модели для ответа от указанного корневого элемента"""
        if self.model is None:
            raise Exception('Модель не определена')

        if isinstance(self.data, list):
            return all([model.is_valid(model=self.model, response=item) for item in self.data])
        else:
            return model.is_valid(model=self.model, response=self.data)