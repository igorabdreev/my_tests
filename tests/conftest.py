from typing import Iterable

from _pytest.fixtures import SubRequest
from allure import step, title
from pytest import fixture
from selenium.webdriver.chrome.webdriver import WebDriver

from api.core_services.authentication import Authentication
from api.custom_requests import Request
from dto.core_services.template.env_token import env_state
from utilities.logging import log_fixture, logger
from web.pages.auth import AuthPage

MISSING_PARAMS_ERROR = 'В фикстуру не переданы обязательные параметры через indirect:'


@fixture
@title('Аутентифицироваться через браузер')
def auth_by_page(request: SubRequest, driver: WebDriver):
    """Аутентифицироваться с помощью логина и пароля на странице.

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
        driver: Инстанс WebDriver.
    """
    log_fixture(request=request)

    if not (user := getattr(request, 'param', None)):
        logger.error(msg := f'{MISSING_PARAMS_ERROR} user')
        raise RuntimeError(msg)

    with step(msg := f'Аутентифицироваться под {user}'):
        logger.info(msg)
        (auth_p := AuthPage(driver=driver)).auth(user=user)
        logger.success(f'Вход совершён!')

    yield driver

    with step(msg := 'Выйти из учётной записи'):
        logger.info(msg)
        auth_p.logout()
        driver.delete_all_cookies()
        logger.success('Выход совершён')


@fixture
@title('Аутентифицироваться и открыть страницу')
def open_page(request: SubRequest, driver: WebDriver):
    """Аутентифицироваться с помощью логина и пароля на странице.

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
        driver: Инстанс WebDriver.
    """
    log_fixture(request=request)

    if not (param := getattr(request, 'param', None)):
        logger.error(msg := f'{MISSING_PARAMS_ERROR} user, page')
        raise RuntimeError(msg)

    if len(param) != 2 or not isinstance(param, Iterable):
        logger.error(msg := 'В фикстуру передано неверное количество параметров через indirect: user, page!')
        raise RuntimeError(msg)

    user, page = param

    with step(msg := f'Аутентифицироваться под {user}'):
        logger.info(msg)
        (auth_p := AuthPage(driver=driver)).auth(user=user)

    with step(msg := f'Открыть страницу {page}'):
        logger.info(msg)
        (page := page(driver=driver)).get()

    yield page

    with step(msg := 'Выйти из учётной записи'):
        logger.info(msg)
        auth_p.logout()
        driver.delete_all_cookies()
        logger.success('Выход совершён')


@fixture(params=[{}])
@title('Фикстура. Получить токен окружения с заданными параметрами')
def env_token(request: SubRequest):
    """
    Если словарь с параметрами окружения не будет передан, будут использованы параметры по умолчанию.

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
            param: словарь с параметрам окружения, которые изменятся
                is-central-office: bool (default: True),
                is-wifi: bool (default: False),
                under-emm: bool (default: False),
                is-vpn: bool (default: False),
                network-segment: str (default: internal, возможные значения будут добавлены позже),
                is-citrix: bool (default: False),
                is-mobile: bool (default: False)
    """
    log_fixture(request=request)

    (json := env_state.copy()).update(request.param)
    Authentication().get_environment(json=json)


@fixture
@title('Фикстура. Аутентифицироваться через API')
def auth_api(request: SubRequest, env_token):
    """Аутентифицироваться по API под заданным пользователем и положить токен в хедеры

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
        env_token: зависимость от фикстуры env_token
    """
    log_fixture(request=request)

    if not (user := getattr(request, 'param', None)):
        logger.error(msg := f'{MISSING_PARAMS_ERROR} user')
        raise RuntimeError(msg)

    yield Authentication().get_token(user=user)

    if (key := 'Authorization') in Request.headers:
        with step(msg := 'Убираем токен из заголовка после теста'):
            logger.debug(msg)
            del Request.headers[key]


@fixture(scope='class')
@title('Setup')
def set_up(request: SubRequest):
    """Запустить setup к тестовому классу

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры
    """
    log_fixture(request=request)

    if not (cls := getattr(request, 'cls', None)):
        logger.error(msg := 'Фикстура может использоваться только на TestClass!')
        raise RuntimeError(msg)

    if not (method := getattr(cls, 'set_up', None)):
        logger.error(msg := 'В классе отсутствует метод "set_up" для выполнения фикстуры "set_up"!')
        raise RuntimeError(msg)

    method()


@fixture
@title('Открыть страницу Аутентификации')
def open_auth_web(request: SubRequest, driver):
    """Открыть страницу аутентификации

    Args:
        request: Подзапрос для получения данных из тестовой функции/фикстуры.
        driver: Инстанс WebDriver.
    """
    log_fixture(request=request)

    with step(msg := 'Открыть страницу входа'):
        logger.info(msg)
        (auth_p := AuthPage(driver=driver)).get()

    yield auth_p
