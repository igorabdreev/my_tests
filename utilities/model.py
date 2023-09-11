"""Методы валидации тел ответа по схеме Pydantic"""
import json
from typing import Type

import allure
import pytest
from pydantic import BaseModel, ValidationError

from utilities.logging import logger


@logger.catch
@allure.step('Валидация тела ответа по схеме')
def is_valid(model: Type[BaseModel], response: dict) -> bool:
    """Валидировать тело ответа по схеме

    Args:
        model: Схема тела ответа
        response: JSON ответа
    """
    with allure.step('Проверка тела по схеме'):
        _model, _response = model.schema_json(), json.dumps(response)
        allure.attach(_response, name='Тело ответа')
        allure.attach(_model, name='Модель')

        try:
            model.validate(response)
            return True

        except ValidationError as e:
            logger.error(
                f'Ошибка валидации тела ответа!\n'
                f'\tОшибка:\n{e}\n'
                f'\tМодель: {_model}\n'
                f'\tТело:   {_response}'
            )
            pytest.fail(reason=str(e))


def convert_model(model: BaseModel, is_json: bool = False, **kwargs) -> list or dict or str:
    """ Преобразование модели в объект для отправки в request: str, dict, data

    Args:
        model: объект модели
        is_json: True - результат возвращается в формате json
                 False -  результат возвращается в dict/list
        **kwargs: кварги для метода преобразования
    """
    is_list: bool = False

    result = model.json(**kwargs) if is_json else model.dict(**kwargs)

    if '__root__' in result:
        result = result["__root__"]
        is_list = True

    logger.debug(
        f'Преобразование модели:\n'
        f'\tМодель: {model}\n'
        f'\tПреобразование: {"json" if is_json else "list" if is_list else "dict"}\n'
        f'\tРезультат: {result}'
    )

    return result
