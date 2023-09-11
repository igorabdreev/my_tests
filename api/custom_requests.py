"""Класс для отправки API-запросов и его методы"""
from datetime import datetime
from typing import Optional, Union

import requests
from pydantic import BaseModel

from api.decorators import unavailable_host_exception_handler
from port_forwarding import get_local_url
from utilities.config import Config
from utilities.logging import log_request, log_response
from utilities.model import convert_model


class Request:
    """Класс для отправки API-запросов"""

    # У каждого бизнес-класса свой набор, другие дочерние объекты не видят их
    data: dict
    files: dict
    json: dict
    params: dict
    url: str

    # Общие между API классами, видны во всех дочерних объектах
    headers: dict = {}
    token_cache: dict[str, tuple[str, datetime]] = {}
    env_cache: dict[tuple, tuple[str, datetime]] = {}

    NAME: str

    def __init__(self):
        self.url = get_local_url(service_name=self.NAME)

    def __new__(cls, *args, **kwargs):
        """ Создать новый объект класса API

        Args:
            args: позиционные аргументы для инициализации бизнес API
            kwargs: именованные аргументы для инициализации бизнес API
        """
        obj = super(Request, cls).__new__(cls)

        for attr in ['data', 'json', 'params', 'files']:
            obj.__setattr__(attr, {})

        obj.__init__(*args, **kwargs)

        return obj

    @unavailable_host_exception_handler
    def request(
            self,
            url: str,
            headers: Optional[dict] = None,
            data: Optional[Union[dict, list, BaseModel]] = None,
            params: Optional[dict] = None,
            timeout: Optional[Union[int, float]] = 10,
            files: Optional[Union[dict, list]] = None,
            json: Optional[Union[dict, BaseModel]] = None,
            method: str = 'get',
            needs_allure: bool = True,
            **kwargs
    ) -> requests.Response:
        """Отправить запрос и залоггировать запрос и ответ

        Args:
            url: адрес
            method: HTTP-метод
            headers: заголовки, если есть
            data: тело запроса, если есть
            json: тело запроса в формате json
            params: параметры запроса, если есть
            timeout: таймаут ожидания ответа сервера
            files: файлы для отправки
            needs_allure: Флаг логгирования в allure
            **kwargs: кварги для метода преоразования объекта модели
        """
        if isinstance(data := data if data else self.data, BaseModel):
            data = convert_model(model=data, is_json=True, **kwargs)

        if isinstance(json := json if json else self.json, BaseModel):
            json = convert_model(model=json, **kwargs)

        log_request(
            request=requests.Request(
                url=url,
                method=method,
                headers=headers if headers else self.headers,
                params=params if params else self.params,
                data=data,
                files=files if files else self.files,
                json=json
            ).prepare(),
            needs_allure=needs_allure
        )
        response = requests.request(
            url=url,
            method=method,
            headers=headers if headers else self.headers,
            params=params if params else self.params,
            data=data,
            files=files if files else self.files,
            json=json,
            verify=False,
            timeout=None if Config.debug else timeout
        )
        log_response(response=response, needs_allure=needs_allure)

        for attr in [self.data, self.json, self.files, self.params]:
            attr.clear()

        return response

    @unavailable_host_exception_handler
    def session_request(
            self,
            url: str,
            certs: Optional[Union[str, tuple[str, str]]] = None,
            headers: Optional[dict] = None,
            data: Optional[Union[dict, list, BaseModel]] = None,
            params: Optional[dict] = None,
            timeout: Optional[Union[int, float]] = 10,
            files: Optional[Union[dict, list]] = None,
            json: Optional[Union[dict, BaseModel]] = None,
            verify: bool = False,
            needs_allure: bool = True,
            method: str = 'get',
            **kwargs
    ) -> requests.Response:
        """Отправить запрос через сессию и залогировать запрос и ответ

        Args:
            url: адрес
            certs: сертификаты сессии
            method: HTTP-метод
            headers: заголовки, если есть
            data: тело запроса, если есть
            json: тело запроса в формате json
            params: параметры запроса, если есть
            timeout: таймаут ожидания ответа сервера
            files: файлы для отправки
            verify: проверка сертификатов
            needs_allure: Флаг логгирования в allure
            **kwargs: кварги для метода преоразования объекта модели
        """
        if isinstance(data := data if data else self.data, BaseModel):
            data = convert_model(model=data, is_json=True, **kwargs)

        if isinstance(json := json if json else self.json, BaseModel):
            json = convert_model(model=json, **kwargs)

        with requests.Session() as session:
            session.cert = certs

            log_request(
                request=(
                    prepared_request := requests.Request(
                        url=url,
                        method=method,
                        headers=headers if headers else self.headers,
                        params=params if params else self.params,
                        data=data,
                        files=files if files else self.files,
                        json=json,
                    ).prepare()
                ),
                needs_allure=needs_allure
            )

            response = session.send(request=prepared_request, verify=verify, timeout=None if Config.debug else timeout)

        log_response(response=response, needs_allure=needs_allure)

        for attr in [self.data, self.json, self.files, self.params]:
            attr.clear()

        return response
