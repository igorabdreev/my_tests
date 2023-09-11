from typing import Callable

from allure import attach, attachment_type, step

from utilities.logging import logger


def log_result_to_allure(name: str) -> Callable:
    """Декорировать функцию, в которой есть получаение токена

    Args:
        name: Имя генератора
    """

    def wrapper(decorated: Callable):
        def inner(**kwargs) -> str or dict or list or bool or int:
            """Обертка над генератором

            Args:
                **kwargs: прочие аргументы
            """
            if needs_allure := kwargs.get('needs_allure', True):
                (allure_step := step(name)).__enter__()

            logger.info(f'Запускаем генератор "{name}"')
            result = decorated(**kwargs)
            logger.success(f'Генератор отработал!\n\tРезультат: {result}')

            if needs_allure:
                attach(body=str(result), name='РЕЗУЛЬТАТ', attachment_type=attachment_type.TEXT)
                allure_step.__exit__(exc_type=None, exc_val=None, exc_tb=None)

            return result

        return inner

    return wrapper
