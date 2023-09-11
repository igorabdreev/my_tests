"""Пользовательские учетные записи сервиса Цели"""
from users.user import User

VAULT = 'goals_users'

DIRECTOR_GOALS = User(
    login='HRP-5937-R04',
    vault_path=VAULT,
    description='Руководитель Цели'
)

DIRECTOR_GOALS_2 = User(
    login='HRP-5937-R01',
    vault_path=VAULT,
    description='Руководитель Цели'
)

EMPLOYEE_GOALS = User(
    login='HRP-5937-S09',
    vault_path=VAULT,
    description='Сотрудник 1 Цели'
)

EMPLOYEE_GOALS_2 = User(
    login='HRP-5937-S12',
    vault_path=VAULT,
    description='Сотрудник 1 Цели'
)