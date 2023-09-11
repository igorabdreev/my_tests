"""Генераторы, для получения данных из Оргструктуры"""
import pickle

from api.core_services.authentication import Authentication
from api.core_services.spine_orgstructure.person import Person
from generators.enums import (
    KeycloakGen,
    OrgstructureDataPathGen,
    OrgstructureGen
)
from generators.keycloak import get_user_data_from_keycloak
from generators.log_result_to_allure import log_result_to_allure
from generators.token_cache import gen_auth
from users.technical import TUZ_PP_PAOUPLOADER
from users.user import Admin, TechnicalUser, User
from utilities.config import Config
from utilities.logging import logger
from utilities.tools import find_value_from_json


@gen_auth
@log_result_to_allure(name='Получить данные из Оргструктуры по uuid сотрудника и параметрам структуры')
def get_structure_data_by_type(
        user: User or Admin or TechnicalUser,
        data_path: OrgstructureDataPathGen,
        layer: OrgstructureGen = OrgstructureGen.oshs,
        level: int or any = 0,
        direction: OrgstructureGen = OrgstructureGen.down,
        needs_allure: bool = True
) -> str or dict or list or bool or int:
    """ Получить данные из Оргструктуры по uuid сотрудника и параметрам структуры.

    Args:
        user:               uuid пользователя.
        layer:              тип оргструктуры:
            - OSHS ->       ОШС-структура.
            - SBERGILE ->   Sbergile-структура.
        level:              уровень запрашиваемой структуры относительно той, в которой находится сотрудник.
                            Уровень домашней структуры сотрудника = 0.
        direction:          направление чтения структуры:
            - DOWN ->       по дереву структуры вниз.
            - UP ->         по дереву структуры вверх.
        data_path:          Искать id или наименование:
            - id ->         Ид структуры
            - name ->       Наименование структуры
        needs_allure:       Флаг логгирования в allure
            - True ->       Логгирует в allure
            - False ->      НЕ логгирует в allure

    Returns:
        structure_data:     данные структуры сотрудника.
    """
    file_name = '_'.join(map(str, (user.login, data_path.value, layer.value, level, direction.value)))

    if (file_path := Config.temp_dir / file_name).exists() and not needs_allure:
        with file_path.open('rb') as file:
            logger.debug('Достали значение из КЕШа')
            return pickle.load(file)

    Authentication().get_token(user=TUZ_PP_PAOUPLOADER, needs_allure=needs_allure)

    response = Person().get_person_head_or_subordinate(
        person_id=get_user_data_from_keycloak(user=user, field=KeycloakGen.person_id, needs_allure=needs_allure),
        layer=layer,
        level=level,
        direction=direction,
        view='ONLY_STRUCTURE',
        needs_allure=needs_allure
    )

    if response.status_code != 200:
        logger.error(
            msg := f'В процессе получение данных оргструктуры произошла ошибка:\n'
                   f'\tКод: {response.status_code}\n'
                   f'\tОтвет: \n{response.json()}'
        )
        raise Exception(msg)

    try:
        value = find_value_from_json(json=response.json(), jp_expr=f'$.data[0]{data_path}', needs_allure=needs_allure)

        if not needs_allure:
            with file_path.open('wb') as file:
                pickle.dump(value, file)

        return value

    except Exception:
        logger.error(msg := f'У {user} нет данных по пути "{data_path}"!')
        raise Exception(msg)
