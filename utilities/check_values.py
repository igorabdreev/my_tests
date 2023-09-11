from typing import Union, Callable, Any
import pytest
from pydantic import BaseModel

from utilities.logging import logger


def _compare_lists(_first: list[Any], _second: list[Any], compare_func: Callable) -> list[str]:
    """Сравнение объектов типа список

    Args:
        _first: первый список
        _second: второй список
        compare_func: функция для сравнения словарей
    """
    errors: list[str] = []

    if len(_first) != len(_second):
        logger.debug(msg := f'Длина списков не равна: {len(_first)} != {len(_second)}')
        errors.append(msg)

        return errors

    logger.debug(f'Поэлементное сравнение значений в списках:\n{_first}\n{_second}')
    for i, (item1, item2) in enumerate(zip(_first, _second)):
        if isinstance(item1, list) and isinstance(item2, list):
            nested_errors = _compare_lists(item1, item2, compare_func)

            if nested_errors:
                errors.append(f'Элементы с индексом {i} не равны: {nested_errors}')

        elif isinstance(item1, dict) and isinstance(item2, dict):
            nested_errors = compare_func(item1, item2)

            if nested_errors:
                errors.append(f'Элементы с индексом {i} не равны: {nested_errors}')

        elif item1 != item2:
            logger.debug(msg_list := f'Элементы с индексом {i} не равны: {item1} != {item2}')
            errors.append(msg_list)

    return errors


def _compare_models(_first_model: dict[Any, Any], _second_model: dict[Any, Any]) -> list[str]:
    """ Сравнение объектов типа словарь

    Args:
        _first_model: первый словарь
        _second_model: второй словарь
    """
    errors: list[str] = []
    msg: str = 'Атрибут "{name}" не соответствует: {value1} != {value2}'
    msg_nested: str = 'Атрибут "{name}" не соответствует: {errors}'

    for attr_name, value1 in _first_model.items():
        value2 = _second_model.get(attr_name, None)

        if isinstance(value1, dict):
            logger.debug(f'Сравнение значений словарей с ключом {attr_name}')

            if not isinstance(value2, dict):
                logger.debug(f'Атрибут {value2} не является словарем')
                errors.append(msg.format(name=attr_name, value1=value1, value2=value2))

            else:
                nested_errors = _compare_models(value1, value2)

                if nested_errors:
                    errors.append(msg_nested.format(name=attr_name, errors=nested_errors))

        elif isinstance(value1, list):
            if not isinstance(value2, list):
                logger.debug(f'Атрибут {value2} не является списком')
                errors.append(msg.format(name=attr_name, value1=value1, value2=value2))

            else:
                logger.debug(f'Сравнение значений {value1} и {value2} с ключом {attr_name}')
                nested_errors = _compare_lists(value1, value2, _compare_models)

                if nested_errors:
                    errors.append(msg_nested.format(name=attr_name, errors=nested_errors))

        elif value1 != value2:
            logger.debug(f'Сравнение значений {value1} и {value2} с ключом {attr_name}')
            errors.append(msg.format(name=attr_name, value1=value1, value2=value2))

    return errors


def check_values(first_obj: Union[BaseModel, dict], second_obj: Union[BaseModel, dict]) -> bool:
    """Сравнить значения модели/словаря по ключам.
    Сравниваются только значения ключей, которые существуют в первом объекте,
    игнорируя все дополнительные ключи во втором объекте

    Args:
        first_obj: Первый словарь/модель для сравнения
        second_obj: Второй словарь/модель для сравнения
    """
    errors = _compare_models(
        _first_model=first_obj if isinstance(first_obj, dict) else first_obj.dict(),
        _second_model=second_obj if isinstance(second_obj, dict) else second_obj.dict()
    )

    if errors:
        logger.error(msg := f'Функция проверки значений в модели/словаре\n\t\t\t' + '\n\t\t\t'.join(errors))
        pytest.fail(msg)

    return True
