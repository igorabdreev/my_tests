"""Генераторы, которые ходят в PersonProfile"""
import pickle

from api.core_services.authentication import Authentication
from api.core_services.spine_person_profile.segment import Segment
from generators.enums import KeycloakGen, PersonGen
from generators.keycloak import get_user_data_from_keycloak
from generators.log_result_to_allure import log_result_to_allure
from generators.token_cache import gen_auth
from users.technical import TUZ_PP_PAOUPLOADER
from users.user import Admin, TechnicalUser, User
from utilities.config import Config
from utilities.logging import logger
from utilities.tools import find_value_from_json


def _get_segment_data(person_id: str, segment: str, needs_allure: bool = True) -> dict or list:
    """Получить данные из заданного сегмента по personId

    Args:
        person_id: Id пользователя
        segment: название сегмента
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    Authentication().get_token(user=TUZ_PP_PAOUPLOADER, needs_allure=needs_allure)

    response = Segment().find_segment_using_filter(
        json={
            'types': [segment],
            'person': {
                'uuids': [person_id],
                'extKeys': []
            }
        },
        needs_allure=needs_allure
    )

    if response.status_code != 200:
        logger.error(
            _msg := f'В процессе получение данных оргструктуры произошла ошибка:\n'
                    f'\tКод: {response.status_code}\n'
                    f'\tОтвет: \n{response.json()}'
        )
        raise RuntimeError(_msg)

    return response.json()


@gen_auth
@log_result_to_allure('Генератор. Получить значение поля пользователя из Person Profile')
def get_data_from_segment(
        user: User or Admin or TechnicalUser,
        field: PersonGen,
        needs_allure: bool = True
) -> str or dict or list or bool or int:
    """ГЕНЕРАТОР. Получить значение заданного поля из PersonProfile

    Args:
        user: пользователь
        field: поле
        needs_allure:       Флаг логгирования в allure
            - True ->       Логгирует в allure
            - False ->      НЕ логгирует в allure
    """

    try:
        file_name = '_'.join(map(str, (user.login, field.value.segment)))

        if (file_path := Config.temp_dir / file_name).exists() and not needs_allure:
            with file_path.open('rb') as file:
                logger.debug('Достали значение из КЕШа')
                return pickle.load(file)

        person_id = get_user_data_from_keycloak(user=user, field=KeycloakGen.person_id, needs_allure=needs_allure)
        json = _get_segment_data(person_id=person_id, segment=field.value.segment, needs_allure=needs_allure)
        value = find_value_from_json(jp_expr=field.value.jpe, json=json, needs_allure=needs_allure)

        if not needs_allure:
            with file_path.open('wb') as file:
                pickle.dump(value, file)

        return value

    except Exception:
        logger.error(
            msg := f'Ошибка в работе генератора PersonProfile!\n'
                   f'\tСообщение: {user.login} не имеет атрибут "{field.name}"'
        )
        raise Exception(msg)
