"""Классы и методы для хранения данных тестовых пользователей и работы с ними"""
from utilities.config import Config


class User:
    """Класс тестового пользователя"""
    realm: str
    client_id = 'fakeuser'
    base_vault_folder = 'auth_data'

    def __init__(self, login: str, vault_path: str = '', description: str = ''):
        """
        Args:
            login: логин пользователя для аутентификации на платформе
            vault_path: путь до секрета в Vault
            description: описание (например: Пекарь пекарни Пышные булки)
        """
        self.login = login.lower()
        self.vault_path = f'{self.base_vault_folder}/{vault_path}'
        self.description = description

    @property
    def realm(self):
        return 'PAOSberbank'

    def __str__(self):
        return f'Пользователь "{self.description}" с логином "{self.login}"'

    def __repr__(self):
        return f'User({self.login=}, {self.description=})'


class Admin(User):
    """Класс администратора"""
    client_id = 'ta-manager'
    realm = 'master'

    @property
    def client_secret(self):
        return {
            'dev': 'c5776de7-6593-4597-9114-8f208b3b9301',
            'ift': '8538ac01-03f0-4bd6-82fd-bd8e905b8269'
        }[Config.stand]

    def __str__(self):
        return f'Администратор "{self.description}" с логином "{self.login}"'

    def __repr__(self):
        return f'Admin({self.login=}, {self.description=})'


class TechnicalUser(User):
    """Класс технического пользователя"""
    client_id = 'Free-for-charge'
    realm = 'sberbank-ta'

    def __str__(self):
        return f'ТУЗ "{self.description}" с логином "{self.login}"'

    def __repr__(self):
        return f'TechnicalUser({self.login=}, {self.description=})'
