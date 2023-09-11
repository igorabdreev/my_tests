"""Различные функции для инфраструктуры автотестов"""
import pickle
from json import dumps
from pathlib import Path
from time import sleep, time
from typing import Iterable

from allure import step
from allure_commons.types import LinkType
from filelock import FileLock
from jsonpath_rw_ext import parse
from requests import PreparedRequest

from generators.log_result_to_allure import log_result_to_allure
from utilities.config import Config
from utilities.logging import logger


@logger.catch
def get_link(test: int) -> tuple[str, str, str]:
    """ Создать allure link по номеру тест-кейса

    Args:
        test: Номер тест-кейса HRPQA-T{test}
    """
    url_test_case: str = f'HRPQA-T{test}'
    return f'{Config.url_zephyr}/{url_test_case}', LinkType.LINK, url_test_case


@logger.catch
def get_curl(request: PreparedRequest, is_compressed: bool = False, is_insecure: bool = False):
    """Получить curl запроса

    Args:
        request: запрос
        is_compressed: параметр позволяющий сформировать curl для запроса сжатого ответа
        is_insecure: параметр явно позволяет сформировать curl для "небезопасного" SSL соединения и передачи данных
    """
    headers = ' -H '.join([f'"{k}: {v}"' for k, v in request.headers.items()])
    return f"curl -X {request.method} -H {headers} " \
           f"-d '{request.body.decode('latin-1') if isinstance(request.body, bytes) else request.body}' " \
           f"{'--compressed' if is_compressed else ''} " \
           f"{'--insecure' if is_insecure else ''} '{request.url}'"


@log_result_to_allure('Поиск значения в словаре')
def find_value_from_json(
        json: dict,
        jp_expr: str,
        is_missing: bool = False,
        needs_allure: bool = True
) -> str or dict or list or bool or int:
    """ Найти значение в json по JPExpression

    Args:
        json: json, в котором надо найти значение
        is_missing: переключение наличия или отсутствия ключа
        jp_expr: путь до значения
        needs_allure:       Флаг логгирования в allure
            - True ->       Логгирует в allure
            - False ->      НЕ логгирует в allure
    """
    found = [match.value for match in parse(jp_expr).find(json)]
    logger.info(
        f'Поиск значения из JSON\n'
        f'\tПуть:\t\t{jp_expr}\n'
        f'\tJSON:\t\t{dumps(json)}\n'
        f'\tМод:\t\t{"Отсутствие" if is_missing else "Наличие"}\n'
    )

    if is_missing:

        if not found:
            logger.info(f'Значение по пути {jp_expr} не найдено')
            return True

        logger.error(msg := f'Значение по пути {jp_expr} найдено')
        raise ValueError(msg)

    else:

        if not found:
            logger.error(msg := f'Значение по пути {jp_expr} не найдено')
            raise ValueError(msg)

        logger.success(
            f'Получено значение из JSON!\n'
            f'\tЗначение:\t{(result:= found if len(found) > 1 else found[0])}\n'
            f'\tТип:\t\t{type(result)}'
        )
        return result


@step('Вызывать метод, пока он не выполнится')
def wums(
        method: callable,
        timeout: int = Config.timeout,
        retry_interval: int = 1,
        ignoring_exceptions: Iterable = (),
        message: str = "",
        stop_on_error: bool = False,
        ignore_result: bool = False,
        fail_after_time: bool = True,
        expected="None",
        **kwargs
):
    """ Выполнять переданную функцию или метод до определенного результата

        Args:
            method:                  переданная функция/метод объекта, которая будет выполняться
            timeout:                        отведенное время для попыток выполнения method_object
            retry_interval:                 интервал в секундах, между попытками выполнения method_object
            ignoring_exceptions:             список или кортеж игнорируемых исключений, вызываемых во время выполнения
                                                method_object
            message:                        текст сообщения, если сработает TimeoutException.
            stop_on_error:
                True    ->                      продолжить выполнение основного кода, если выполнение method_object вызвало
                                                исключение
                False   ->                      продолжать попытки выполнения method_object при вызове исключения
            ignore_result:
                True    ->                      продолжить выполнение основного кода, если выполнение method_object не
                                                вызвало исключения, несмотря на результат его работы
                False   ->                      продолжить выполнение основного кода, если результат выполнения
                                                method_object равен True или не None
            fail_after_time:
                True    ->                      вызвать исключение TimeoutException по истечении времени
                False   ->                      продолжить выполнение основного кода по истечении времени
            expected:                 значение, ожидаемое от method_object (по умолчанию "None" именно строкой, чтобы
                                                была возможность ожидать None)
            **kwargs:                       словарь аргументов для передачи в method_object

        Returns:
            method_execution_result:        результат выполнения метода method_object
        """
    end = time() + timeout

    while time() < end:
        try:
            logger.debug(f'Вызываем метод "{method.__name__}"')
            result = method(**kwargs)
            logger.debug(f'Метод "{method.__name__}" отработал с результатом "{result}"')

            if (expected == "None" and (result or ignore_result)) or (expected != "None" and result == expected):
                logger.success(f'WUMS "{method.__name__}" закончил работу "{result}"')
                return result

        except Exception as e:
            logger.debug(f'Во время работы метода "{method.__name__}" произошла ошибка:\n\t{e}')

            if stop_on_error:
                logger.debug(f'Прекращаем выполнять метод "{method.__name__}" из-за ошибки:\n\t{e}')
                return e

            elif type(e) not in ignoring_exceptions:
                logger.error(f'Во время работы метода "{method.__name__}" произошла неожиданная ошибка:\n\t{e}')
                raise e

        sleep(retry_interval)

    if fail_after_time:
        raise TimeoutError(message)


@step('Заблокировать выполнение метода для другого потока, если он был ранее запущен иным потоком')
def lock(worker_id: str, fixture: str, method, **kwargs):
    """ Заблокировать к выполнению переданный метод в фикстуре другим потокам, если ранее он был уже вызван
    и предоставить результат его выполнения из файла. Работает со всем типами данных, что возвращает метод.

    Args:
        method:     переданная функция/метод объекта, которая будет выполняться
        worker_id:  id потока
        fixture:    имя используемой фикстуры
        **kwargs:   словарь аргументов для передачи в method_object
    """

    if worker_id == 'master':
        # not executing in with multiple workers, just produce the data and let
        # pytest's fixture caching do its job
        return method(**kwargs)

        # get the temp directory shared by all workers

    if not (dir_lock := Config.test_data_dir / 'temp' / 'session-fixtures' / fixture).exists():
        dir_lock.mkdir(parents=True, exist_ok=True)

    with FileLock(str(data_path := dir_lock / 'data') + '.lock'):

        if data_path.is_file() and data_path.stat().st_size > 0:
            with data_path.open('rb') as data_file:
                return pickle.load(data_file)

        else:
            with data_path.open('wb') as data_file:
                pickle.dump(data := method(**kwargs), data_file, protocol=pickle.HIGHEST_PROTOCOL)
                return data


def rm_tree(path: Path):
    try:
        [child.unlink() if child.is_file() else rm_tree(child) for child in path.iterdir()]
        path.rmdir()

    except FileNotFoundError:
        logger.debug('Папка или файл уже отсутствует')
