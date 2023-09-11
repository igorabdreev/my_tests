""" Коннектор для работы с хранилищем секретов HashiCorp Vault """
import hvac
from hvac.exceptions import InvalidPath

import utilities
from utilities.vault.config import VaultConfig


class VaultConnector:
    """ Класс для работы с хранилищем секретов """

    def __init__(self, role_id, secret_id):
        """
        Args:
            role_id: id роли для входа в vault
            secret_id: параметр аппроли
        """
        self.conf = utilities.vault.config.VaultConfig
        self.client = hvac.Client(url=self.conf.url, namespace=self.conf.namespace, verify=False)
        self.role_id = role_id
        self.secret_id = secret_id
        utilities.logging.logger.debug(f'Создан коннект к Vault')

    def auth_with_approle(self):
        """ Аутентифицироваться в хранилище через approle. TTL токена 5 мин """
        self.client.auth.approle.login(role_id=self.role_id, secret_id=self.secret_id)

    def get_value_from_vault(self, key_name: str, vault_path: str = None, secret_name: str = None,
                             full_vault_path: str = None) -> str:
        """ Получить из хранилища значение для секрета по ключу

        Args:
            key_name:        имя ключа секрета;
            vault_path:      путь в хранилище, где расположен секрет;
            secret_name:     имя секрета;
            full_vault_path: полный путь до секрета в хранилище.
        """
        self.auth_with_approle()

        utilities.logging.logger.debug('Получение секрета из Vault')

        try:
            return self.client.secrets.kv.v1.read_secret(
                path=full_vault_path or f"{vault_path}/{secret_name}",
                mount_point=self.conf.mount
            )["data"][key_name]

        except InvalidPath:
            return self.client.secrets.kv.v1.read_secret(
                path=full_vault_path or f"{vault_path}/{secret_name.upper()}",
                mount_point=self.conf.mount
            )["data"][key_name]

    def create_keyfile_from_vault_value(self, key_name: str, file_path: str, vault_path: str = None,
                                        secret_name: str = None, full_vault_path: str = None):
        """ Получить из хранилища значение для секрета по ключу и сохранить его в файл

        Args:
            key_name:        имя ключа секрета;
            file_path:       путь до файла, в который будет сохранено значение из хранилища;
            vault_path:      путь в хранилище, где расположен секрет;
            secret_name:     имя секрета;
            full_vault_path: полный путь до секрета в хранилище.
        """
        with open(file_path, 'w') as file:
            file.write(self.get_value_from_vault(
                key_name=key_name,
                vault_path=vault_path,
                secret_name=secret_name,
                full_vault_path=full_vault_path
            ))

        return file_path
