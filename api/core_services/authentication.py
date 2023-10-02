"""Класс и методы сервиса "Аутентификация" """
from datetime import datetime

from allure import step
from requests import Response

from api.custom_requests import Request
from dto.core_services.template.env_token import env_state
from users.user import Admin, TechnicalUser, User
from utilities.config import Config
from utilities.logging import logger


class Authentication(Request):
    """Класс сервиса "Аутентификация" """

    def __init__(self):
        self.url = Config.keycloak_url

    def get_token(self, user: Admin or TechnicalUser or User, needs_allure: bool = True, **kwargs) -> str:
        """Получить аутентификационный токен по API

        Args:
            user: пользователь
            needs_allure: Флаг логгирования в allure
                - True ->   Логгирует в allure
                - False ->  НЕ логгирует в allure
            kwargs: значения для обновления окружения
        """

        def _get_token(msg: str):
            """Получить токен пользователя

            Args:
                msg: сообщение для логирования
            """
            (json := env_state.copy()).update(kwargs)

            self.get_environment(json=json, needs_allure=needs_allure)

            self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
            response = mapping[user.realm](
                user=user,
                url=f'{self.url}/auth/realms/{user.realm}/protocol/openid-connect/token',
                needs_allure=needs_allure
            )

            if response.status_code != 200:
                logger.error(
                    _msg := f'В процессе аутентификации "{user.description}" произошла ошибка:'
                            f'\tКод: {response.status_code}'
                            f'\tОтвет: \n{response.json()}'
                )
                raise Exception(_msg)

            self.headers["Authorization"] = f"Bearer {response.json()['access_token']}"
            self.token_cache[user.login] = self.headers["Authorization"], datetime.now()
            logger.debug(msg)

        mapping: dict[str, callable] = {
            'master': self._get_admin_token,
            'sberbank-ta': self._get_technical_user_token,
            'PAOSberbank': self._get_user_token
        }
        logger.info(f'Аутентифицируемся под "{user}"')

        if user.login in self.token_cache:
            token, time_of_create = self.token_cache[user.login]

            if (datetime.now() - time_of_create).seconds < 180:
                self.headers["Authorization"] = token
                logger.debug('Взяли токен из кеша')

            else:
                _get_token(msg='Токен протух, запросили новый')

        else:
            _get_token(msg='Токена не было в кеше, запросили новый')

        logger.success("Аутентификация прошла успешно!")
        return self.headers["Authorization"].replace('Bearer ', '')

    def get_environment(self, json: dict, needs_allure: bool = True):
        """ Обновить токен окружения в headers

        Args:
            json: тело запроса
            needs_allure: Флаг логгирования в allure
                - True ->   Логгирует в allure
                - False ->  НЕ логгирует в allure
        """

        def _get_token(msg: str):
            """Получить токен окружения

            Args:
                msg: сообщение для логирования
            """
            self.headers['Content-Type'] = 'application/json'
            response = self.request(
                method='POST',
                url=f'{self.url}/auth/tools/ids-reverse-proxy/environment/dev',
                json=json,
                needs_allure=needs_allure
            )

            if response.status_code != 200:
                logger.error(msg_ := 'Не удалось получить токен окружения!')
                raise Exception(msg_)

            self.headers['x-environment-state'] = response.json()['environment']
            self.env_cache[json_tuple] = self.headers['x-environment-state'], datetime.now()
            logger.debug(msg)

        logger.info('Получаем токен окружения')

        if (json_tuple := tuple(json.items())) in self.env_cache:
            token, time_of_create = self.env_cache[json_tuple]

            if (datetime.now() - time_of_create).seconds < 180:
                self.headers['x-environment-state'] = token
                logger.info("Взяли токен окружения из кеша")

            else:
                _get_token(msg="Токен окружения протух, получили новый")

        else:
            _get_token(msg="Токена такого окружения не было в кеше, получили новый")

        logger.success('Получили токен окружения')

    def _get_user_token(self, user: User, url: str, needs_allure: bool = True) -> Response:
        """Аутентифицироваться по API под ПУЗом

        Args:
            user: пользователь ПУЗ
            url: url получения токена ПУЗ
            needs_allure: Флаг логгирования в allure
                - True ->   Логгирует в allure
                - False ->  НЕ логгирует в allure
        """
        self.headers['x-hrp-username'] = user.login
        return self.request(
            url=url,
            method='POST',
            data={'grant_type': 'password', 'client_id': user.client_id},
            needs_allure=needs_allure
        )

    def _get_admin_token(self, user: Admin, url: str, needs_allure: bool = True) -> Response:
        """Аутентифицироваться по API под АУЗом

        Args:
            user: пользователь АУЗ
            url: url получения токена АУЗ,
            needs_allure: Флаг логгирования в allure
                - True ->   Логгирует в allure
                - False ->  НЕ логгирует в allure
        """
        return self.request(
            url=url,
            method='POST',
            data={
                'grant_type': 'password',
                'client_id': user.client_id,
                'client_secret': user.client_secret,
                'username': user.login,
                'password': Config.vault.get_value_from_vault(
                    key_name='password',
                    secret_name=user.login,
                    vault_path=user.vault_path
                )
            },
            needs_allure=needs_allure
        )

    def _get_technical_user_token(self, user: TechnicalUser, url: str, needs_allure: bool = True) -> Response:
        """Аутентифицироваться по API под ТУЗ

        Args:
            user: пользователь ТУЗ
            url: url получения токена ТУЗ
            needs_allure: Флаг логгирования в allure
                - True ->   Логгирует в allure
                - False ->  НЕ логгирует в allure
        """
        return self.request(
            url=url,
            method='POST',
            data={
                'grant_type': 'password',
                'client_id': user.client_id,
                'username': user.login
            },
            needs_allure=needs_allure
        )

    @step('Отправить запрос на удаление пользователя из Keycloak')
    def delete_user_by_id(self, user: Admin or TechnicalUser or User, user_id: str) -> Response:
        """Удалить пользователя из Keycloak по user_id

        Args:
            user:       пользователь, данные которого нужно удалить
            user_id:    идентификатор пользователя (поле id из данных пользователя в Keycloak)
        """
        return self.request(method='DELETE', url=f'{self.url}/auth/admin/realms/{user.realm}/users/{user_id}')
