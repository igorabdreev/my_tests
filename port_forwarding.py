"""Модуль для прокидывания портов на локальную систему из Kubernetes"""
import argparse
import socket
import subprocess

from requests import exceptions, request

from utilities.config import Config
from utilities.logging import logger
from utilities.tools import wums

ACTIVE_PORTS = {}
KUBECTL_PROCESSES = []


def get_local_url(service_name: str, local_port: str = '') -> str:
    """ Создать проброс порта сервиса на локальную систему из Kubernetes и получить локальный адрес
        для доступа к сервису

    Note:
        Проброс портов будет работать только при подключенном WireGuard, и если в локальной системе
        настроены утилита kubectl и конфигурационный файл для подключения к кластеру cluster-project
        Инструкция по настройке:

    Args:
        service_name: Имя сервиса в Kubernetes
        local_port: Порт для доступа к сервису из локальной системы
    """
    if Config.debug or __name__ == '__main__':
        if service_name in ACTIVE_PORTS:
            url = f'http://localhost:{ACTIVE_PORTS[service_name]}'

        else:
            if not local_port:
                with socket.socket() as sock:
                    sock.bind(('', 0))
                    local_port = sock.getsockname()[1]

            connection = subprocess.Popen(f"oc port-forward svc/{service_name} {local_port}:8080", shell=True)
            url = f'http://localhost:{local_port}'

            if connection.returncode != 0:
                logger.info(f'Установка соединения с сервисом "{service_name}" по адресу {url}...')
                wums(method=is_url_alive, timeout=10, retry_interval=2, url=url)

                KUBECTL_PROCESSES.append(connection)
                ACTIVE_PORTS[service_name] = local_port

        return url

    else:
        return f'http://{service_name}:8080'


def is_url_alive(url: str) -> bool:
    """Отправить запрос к сервису для проверки его доступности

    Args:
        url: Ссылка на сервис прокинутый из kubernetes на localhost
    """
    try:
        request(method='GET', url=url)
        return True

    except exceptions.ConnectionError:
        logger.info(f"Попытка установить соединение с {url}")


if __name__ == '__main__':
    (parser := argparse.ArgumentParser()).add_argument(
        '--services',
        nargs='+',
        required=True,
        help='Введите имя одного или более сервисов через пробел'
    )

    # Прокидываем порты на локальную систему для требуемых сервисов
    [get_local_url(service_name=service) for service in parser.parse_args().services]

    input("\nДля завершения нажмите любую клавишу\n")

    # Завершаем проброс портов
    [proc.kill() for proc in KUBECTL_PROCESSES]
