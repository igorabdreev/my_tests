"""Параметры для подключения к хранилищу секретов HashiCorp Vault"""


class VaultConfig:
    """Класс с параметрами для подключения к хранилищу секретов HashiCorp Vault"""
    url: str
    namespace: str
    mount: str
