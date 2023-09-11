"""Базовые функции и фикстуры для работы Pytest"""
from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest, fixture
from _pytest.reports import TestReport
from selenium.webdriver.chrome.webdriver import WebDriver

from allure import attach, attachment_type, step, title
from utilities.config import Config
from utilities.logging import create_logger, log_fixture, logger
from utilities.tools import rm_tree
from utilities.vault.config import VaultConfig
from utilities.vault.connector import VaultConnector
from web.driver_factory import Driver


class Options:
    stand: str = '--stand'
    browser: str = '--browser'
    debug_run: str = '--debug_run'
    headless: str = '--headless'
    role_id: str = '--role_id'
    secret_id: str = '--secret_id'
    selenoid: str = '--selenoid'
    log_level: str = '--log_level'
    vault_url: str = '--vault_url'
    vault_namespace: str = '--vault_namespace'
    vault_mount: str = '--vault_mount'
    keycloak_url: str = '--keycloak_url'
    web_url: str = '--web_url'


def pytest_addoption(parser: pytest.Parser):
    """Парсер для аргументов командной строки и значений ini-файла.

    Args:
        parser: Инстанс Parser.
    """
    parser.addoption(
        Options.stand,
        action='store',
        default='ift',
        help='Стенд для запуска тестов',
        choices=['dev', 'ift']
    )

    parser.addoption(
        Options.browser,
        action='store',
        default='chrome',
        help='Браузер',
        choices=['chrome', 'yandex', 'safari']
    )

    parser.addoption(
        Options.headless,
        action='store_true',
        help='Укажите параметр, если хотите запустить браузер в headless режиме'
    )

    parser.addoption(
        Options.role_id,
        action='store',
        help='Роль пользователя для Vault'
    )

    parser.addoption(
        Options.secret_id,
        action='store',
        help='Параметр аппроли для Vault'
    )

    parser.addoption(
        Options.selenoid,
        action='store_true',
        help='Укажите параметр, если хотите запустить браузер через Selenoid'
    )

    parser.addoption(
        Options.debug_run,
        action='store_true',
        help="Укажите параметр, если хотите запустить тесты локально с пробросом портов из Kubernetes"
    )

    parser.addoption(
        Options.log_level,
        action='store',
        default='INFO',
        help='Уровень логгирования',
        choices=['DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL']
    )

    parser.addoption(
        Options.vault_url,
        action='store',
        help='URL волта'
    )

    parser.addoption(
        Options.vault_namespace,
        action='store',
        help='Namespace волта для подключения'
    )

    parser.addoption(
        Options.vault_mount,
        action='store',
        help='Mount в котором лежат ключи синтетики'
    )

    parser.addoption(
        Options.keycloak_url,
        action='store',
        help='URL кейклока',
    )
    parser.addoption(
        Options.web_url,
        action='store',
        help='Базовый URL WEB-страниц'
    )


def _get_option(name: str, config: pytest.Config):
    """Получение необходимого параметра для запуска по имени

    Args:
        name: Название параметра
    """
    if not (result := config.getoption(name)):
        logger.critical(message := f'Не указан {name} в параметрах запуска!')
        raise RuntimeError(message)

    if name in ["--role_id", "--secret_id"]:
        logger.info(f'Получен параметр {name}')
    else:
        logger.info(f'Получен параметр {name}={result}')
    return result


def pytest_configure(config: pytest.Config):
    """Положить параметры запуска в конфиг

    Этот хук вызывается для каждого плагина и начального файла conftest после анализа параметров командной строки.
    После этого хук вызывается для других файлов conftest по мере их импорта.

    Args:
        config: Класс Config для доступа к значениям конфигурации, менеджеру плагинов и хукам плагинов
    """
    Config.log_level = _get_option(name=Options.log_level, config=config)
    create_logger(log_level=Config.log_level, params=config.option)

    Config.debug = config.getoption(Options.debug_run)

    if Config.temp_dir.exists():
        logger.info(f'Очистка директории {Config.temp_dir}')
        rm_tree(path=Config.temp_dir)
        logger.success(f'Директория очищена {Config.temp_dir}')

    Config.temp_dir.mkdir(parents=True, exist_ok=True)

    Config.stand = _get_option(name=Options.stand, config=config)
    Config.keycloak_url = _get_option(name=Options.keycloak_url, config=config).format(stand=Config.stand)
    Config.web_url = _get_option(name=Options.web_url, config=config).format(stand=Config.stand)

    VaultConfig.url = _get_option(name=Options.vault_url, config=config)
    VaultConfig.namespace = _get_option(name=Options.vault_namespace, config=config)
    VaultConfig.mount = _get_option(name=Options.vault_mount, config=config)

    Config.vault = VaultConnector(
        role_id=_get_option(Options.role_id, config=config),
        secret_id=_get_option(Options.secret_id, config=config)
    )


@fixture(scope='session')
@title('Получить флаг запуска в SELENOID')
def is_selenoid(request: SubRequest) -> bool:
    """Получить настройку "Selenoid" из параметров запуска, используется для прогона с использованием SELENOID

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
    """
    log_fixture(request=request)
    return request.config.getoption(Options.selenoid)


@fixture(scope='session')
@title('Получить название браузера')
def browser_name(request: SubRequest) -> str:
    """Получить название браузера из параметров запуска

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
    """
    log_fixture(request=request)
    return _get_option(name=Options.browser, config=request.config)


@fixture(scope='module', params=[()])
@title('Инициализировать драйвер с параметрами')
def driver(request: SubRequest, is_selenoid: bool, browser_name: str) -> WebDriver:
    """Инициализировать экземпляр драйвера

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
        browser_name: Фикстура, имя браузера для прогона
        is_selenoid: Фикстура, Параметр запуска на удалённом сервере Selenoid
    """
    log_fixture(request=request)

    with step(f'Создать инстанс браузера {browser_name}, Selenoid={is_selenoid}'):
        Config.driver = Driver.get_driver(
            root=Path(request.config.rootpath),
            browser_name=browser_name,
            add_opts=[option for option in request.param],
            is_selenoid=is_selenoid
        )

    yield Config.driver

    try:
        Config.driver.quit()
        logger.info('Сессия драйвера закрыта!')

    except Exception:
        logger.warning('Сессия закрылась по таймауту!')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сохранить скриншот при падении"""
    outcome = yield
    rep: TestReport = outcome.get_result()

    if rep.when == 'call' and any(map(lambda x: x in item.fixturenames, ['auth_by_page', 'driver', 'open_page'])) \
            and rep.failed:
        try:
            logger.info(f'Сохраняем скриншот с падения теста: {rep.nodeid}')
            attach(
                name=f'screenshot_{rep.nodeid}',
                body=Config.driver.get_screenshot_as_png(),
                attachment_type=attachment_type.PNG
            )
            logger.debug('Скриншот сохранён!')

        except Exception:
            logger.warning('Не удалось сохранить скриншот c падения!')
