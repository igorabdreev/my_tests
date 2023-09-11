"""Генераторы, которые ходят в Keycloak"""
import jwt

from api.core_services.authentication import Authentication
from generators.enums import KeycloakGen
from generators.log_result_to_allure import log_result_to_allure
from generators.token_cache import gen_auth
from users.user import Admin, TechnicalUser, User


@gen_auth
@log_result_to_allure('Генератор. Получить данные пользователя из Keycloak')
def get_user_data_from_keycloak(
        user: User or Admin or TechnicalUser,
        field: KeycloakGen,
        needs_allure: bool = True
) -> str:
    """ГЕНЕРАТОР. Получить пользовательские данные заданного типа из Keycloak

    Args:
        user: пользователь
        field: тип данных пользователя, которые надо получить, аттрибут класса PersonGen
        needs_allure: Флаг логгирования в allure
            - True -> логгирует в allure
            - False -> НЕ логгирует в allure
    """
    try:
        return jwt.decode(
            jwt=Authentication().get_token(user=user, needs_allure=needs_allure),
            algorithms=['RS256'],
            options={"verify_signature": False}
        )[field.value]

    except KeyError as e:
        e.args = f'Не удалось получить поле "{field.value}" у пользователя "{user}"',
        raise e
