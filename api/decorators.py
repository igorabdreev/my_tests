"""Decorators for module "api" """
import re
from typing import Callable

from requests import Response

from utilities.logging import logger
from api.custom_exceptions import UnavailableServiceError


def unavailable_host_exception_handler(decorated: Callable) -> Callable:
    """Декоратор для отлова ошибки "max retries unknown host"

    Args:
        decorated: декорируемый генератор
    """

    def inner(*args, **kwargs) -> Response:
        """Обертка над генератором

        Args:
            *args: request's arguments
            **kwargs: request's key-word arguments
        """
        try:
            return decorated(*args, **kwargs)

        except Exception as ex:
            if service_name := re.findall(r"(?<=host=')([\S]+)(?=')", str(ex)):
                logger.warning(msg := f"Сервис недоступен: {service_name[0]}")
                raise UnavailableServiceError(msg) from ex

            raise ex

    return inner
