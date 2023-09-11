"""Настрйки логгера и методы работы с ним"""
import json
import sys
from argparse import Namespace

import allure
from _pytest.fixtures import SubRequest
from loguru import logger
from requests import PreparedRequest, Response

from utilities.logger_error import InvalidLogLevel
from utilities.tools import get_curl


def create_logger(log_level: str, params: Namespace):
    """ Создать логгер и установить уровень логирования

    Args:
        log_level: уровень логирования
        params: параметры запуска проекта
    """
    try:
        logger.remove()

        if getattr(params, 'xmlpath', None):
            logger.add(
                sink=sys.stdout,
                level=log_level,
                format='\n{time:HH:mm:ss.SSS} | <level>{level}</level> | <level>{message}</level>'
            )

        else:
            logger.add(
                sink=sys.stdout,
                format='\n<fg #ff7e00>{time:HH:mm:ss.SSS}</fg #ff7e00> | '
                       '<level>{level}</level> | '
                       '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | '
                       '<level>{message}</level>',
                level=log_level,
                colorize=True
            )

    except ValueError:
        logger.error(f'Ошибка при установке уровня логгирования {log_level=}')
        raise InvalidLogLevel(
            log_level=log_level,
            available_log_levels=getattr(logger, '_core').levels.keys()
        )


def attach_body(body: str or bytes):
    """Прикрепить в allure тело запроса

    Args:
        body: Тело запроса
    """
    try:
        body: str = body if type(body) == str else body.decode()
        allure.attach(
            body=json.dumps(obj=json.loads(body), indent=2),
            name='BODY',
            attachment_type=allure.attachment_type.JSON
        )

    except Exception:
        allure.attach(body=body, name='BODY', attachment_type=allure.attachment_type.TEXT)


def log_request(
        request: PreparedRequest,
        is_compressed: bool = False,
        is_insecure: bool = False,
        needs_allure: bool = True
):
    """Залогировать запрос

    Args:
        request: запрос
        is_compressed: параметр, позволяющий сформировать curl для запроса сжатого ответа
        is_insecure: параметр, позволяющий сформировать curl для "небезопасного" SSL соединения и передачи данных
        needs_allure:       Флаг логгирования в allure
            - True ->       Логгирует в allure
            - False ->      НЕ логгирует в allure
    """
    curl = None
    msg = f'HTTP-Method: <blue><normal>{request.method}</normal></blue>\n' \
          f'\t URL:     <blue><normal>{request.url}</normal></blue>\n' \
          f'\t Headers: <blue><normal>{request.headers}</normal></blue>\n'

    if 'boundary' not in request.headers and request.method != 'GET':
        msg += f'\t Body:    <blue><normal>{request.body}</normal></blue>\n'

    if 'boundary' not in request.headers:
        curl = get_curl(request=request, is_compressed=is_compressed, is_insecure=is_insecure)
        msg += f'\t CURL:    <blue><normal>{curl}</normal></blue>'

    try:
        logger.opt(colors=True).info(msg)

    except ValueError:
        logger.debug(f'Ошибка при логгировании последнего запроса:\n\tCURL: {curl if curl else "None"}')
        logger.opt(colors=False).info(msg.replace('<blue><normal>', '').replace('</normal></blue>', ''))

    if needs_allure:
        with allure.step(f'Запрос: [{request.method}] {request.url}'):
            allure.attach(
                body=json.dumps(dict(request.headers), indent=2),
                name='HEADERS',
                attachment_type=allure.attachment_type.JSON
            )
            attach_body(body=request.body)

            if curl:
                allure.attach(body=curl, name='CURL', attachment_type=allure.attachment_type.TEXT)


def log_response(response: Response, needs_allure: bool = True) -> None:
    """Залоггировать ответ

    Args:
        response: ответ
        needs_allure: Флаг логгирования в allure
    """
    color = {
        1: 'light-blue',
        2: 'green',
        3: 'yellow',
        4: 'red',
        5: 'red'
    }.get(response.status_code // 100, "y")

    try:
        logger.opt(colors=True).info(
            f'Code: <{color}><n>{response.status_code}</n></{color}>\n'
            f'\t Headers: <{color}><n>{response.headers}</n></{color}>\n'
            f'\t Body:    <{color}><n>{response.text}</n></{color}>'
        )

    except ValueError:
        logger.opt(colors=True).info(
            f'Code: <{color}><normal>{response.status_code}</normal></{color}>\n'
            f'\t Headers: <{color}><normal>{response.headers}</normal></{color}>\n'
        )
        logger.info(f'Body: {response.text}')

    if needs_allure:
        with allure.step(f'Ответ: [{response.status_code}] {response.url}'):
            allure.attach(
                body=json.dumps(dict(response.headers), indent=2),
                name='HEADERS',
                attachment_type=allure.attachment_type.JSON
            )
            attach_body(body=response.content)


def log_fixture(request: SubRequest):
    """Вывести техническую информацию о фикстуре в дебаг

    Args:
        request: Объект класса SubRequest со служебной информацией о запуске
    """
    logger.debug(
        f'[{request.scope}] Фикстура: {request.fixturename}\n'
        f'\tПуть:      {request.path if hasattr(request, "path") else "None"}\n'
        f'\tКласс:     {request.cls if hasattr(request, "cls") else "None"}\n'
        f'\tТест:      {request.node.nodeid}\n'
        f'\tПараметры: {request.param if hasattr(request, "param") else "None"}\n'
    )
