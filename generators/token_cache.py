"""Декораторы для кастомизации аутентификафии по API"""
from copy import deepcopy
from typing import Callable

from api.custom_requests import Request
from utilities.logging import logger


def gen_auth(decorated: Callable) -> Callable:
    """Декорировать функцию, в которой есть получаение токена

    Args:
        decorated: декорируемый генератор
    """

    def inner(**kwargs) -> str or dict or list or bool or int:
        """Обертка над генератором

        Args:
            **kwargs: прочие аргументы
        """
        try:
            headers = deepcopy(Request.headers)
            logger.debug(f'Сохранили headers')

            generated = decorated(**kwargs)

            Request.headers = headers
            logger.debug(f'Вернули headers в Request.headers')

        except KeyError:
            generated = decorated(**kwargs)

        return generated

    return inner
