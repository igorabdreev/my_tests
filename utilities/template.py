"""Методы обновления шаблонов"""
import json
from copy import deepcopy
from typing import Union

import allure
from pydantic import BaseModel

from utilities.logging import logger


def _merge_in_dict(_base: dict, _new: dict) -> dict:
    """Смержить ключи из new в base

    Note:
        Если ключа нет в base -> он добавляется
        Если ключ есть в base и в new -> он обновляется
        Если ключ есть в base, а в new нет -> остаётся неизменным

        Списки:
            Если на уровне списка количество элементов совпадает -> обновляются элементы внутри по логике выше
            Если на уровне списка количество элементов разное -> в список добавляется новый элемент

    Args:
        _base: Базовый словарь, в который будем мержить
        _new: Словарь с новыми значениями, которые будем мержить

    Returns:
        base: Базовый словарь, в который вмержены новые значения
    """
    for key, value in _new.items():
        logger.debug(f'_merge: {key=}, {value=}')
        if key in _base and _base.get(key, 'KEY_NOT_FOUND') != value:
            if isinstance(value, dict) and isinstance(_base[key], dict):
                logger.debug(f'_merge: Мерж словаря по ключу {key=}')
                _base[key] = _merge_in_dict(_base=_base[key], _new=_new[key])

            elif isinstance(value, list) and isinstance(_base[key], list):
                logger.debug(f'_merge: Мерж списка по ключу {key=}')
                _merge_in_lists(_base=_base[key], _new=_new[key])

            elif type(value):
                logger.debug(f'_merge: Перезапись {key=} на {_new[key]} ')
                _base[key] = value

        else:
            _base[key] = value

    return _base


def _merge_in_lists(_base: list, _new: list):
    """Смержить словари внутри списка

    Args:
        _base: Список из шаблона
        _new: Список новых значений
    """
    if (len_b := len(_base)) == (len_n := len(_new)):
        logger.debug(f'_merge_in_lists: Мерж списков при base == new')
        for idx, value_n in enumerate(_new):
            logger.debug(f'_merge_in_lists: {idx=} Мерж словаря в списке')
            _base[idx] = _merge_in_dict(_base=_base[idx], _new=value_n)

    elif len_b > len_n:
        logger.debug(f'_merge_in_lists: Мерж списков при base > new')
        for idx, value_n in enumerate(_new):
            logger.debug(f'_merge_in_lists: {idx=} Мерж словаря в списке')
            _base[idx] = _merge_in_dict(_base=_base[idx], _new=value_n)

    else:
        logger.debug(f'_merge_in_lists: Мерж списков при base < new')
        for idx, value_b in enumerate(_base):
            logger.debug(f'_merge_in_lists: {idx=} Мерж словаря в списке')
            _base[idx] = _merge_in_dict(_base=value_b, _new=_new[idx])

        logger.debug(f'_merge_in_lists: Добавление элементов base сверх новых значений')
        _base.extend(_new[len_b:])


@logger.catch
@allure.step('Обновление шаблона с помощью новых значений')
def update_template(template: Union[BaseModel, dict, list], new_values: Union[dict, list]) -> dict:
    """Обновить шаблоны тела запроса

    Args:
        template: Шаблон тела запроса
        new_values: Значения для обновлений в шаблоне

    Returns:
        template_updated: Обновлённый шаблон
    """

    template = json.loads(template.json()) if type(template) not in {dict, list} else deepcopy(template)
    type_t = type(template)
    template_before_update = deepcopy(template)

    if type_t == (type_n := type(new_values)) == list:
        _merge_in_lists(_base=template, _new=new_values)
        template_updated = template

    elif type_t == type_n == dict:
        template_updated = _merge_in_dict(_base=template, _new=new_values)
    else:
        raise ValueError(
            f'Тип шаблона "{type_t}" не соответствует типу объекта с новыми значениями "{type_n}"'
        )

    tab = '\t'
    text_template = json.dumps(template_before_update)
    text_new_values = json.dumps(new_values)
    text_result = json.dumps(template_updated)
    logger.info(
        f'\n{"-" * 20} Обновление шаблона {"-" * 20}\n'
        f'Шаблон:{tab * 5}{text_template}\n'
        f'Новые значения:{tab * 3}{text_new_values}\n'
        f'Обновленный шаблон:{tab * 2}{text_result}\n'
    )

    allure.attach(body=text_template, name='ШАБЛОН', attachment_type=allure.attachment_type.JSON)
    allure.attach(body=text_new_values, name='НОВЫЕ ЗНАЧЕНИЯ', attachment_type=allure.attachment_type.JSON)
    allure.attach(body=text_result, name='РЕЗУЛЬТАТ', attachment_type=allure.attachment_type.JSON)

    return template_updated
