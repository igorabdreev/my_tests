"""Класс и методы для получения конфигов баз данных из Vault"""
from utilities.config import Config


class DbCredentialsProvider:
    """Класс для получения конфигурационных данных из HashiCorp Vault для подключения к БД"""
    vault_var_mapping = {}

    def __init__(self, vault_path: str, db_name: str):
        """
        Args:
            vault_path: путь до секрета
            db_name:    название базы данных
        """
        self.vault_path = vault_path
        self.db_name = db_name
        self.vault_connector = Config.vault

    def get_credentials(self) -> dict:
        """Получить конфигурационные данные для подключения к БД"""
        return {
            key: self.vault_connector.get_value_from_vault(
                vault_path=self.vault_path,
                secret_name=self.db_name,
                key_name=value
            )
            for key, value in self.vault_var_mapping.items()
        }
