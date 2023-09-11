""" Генераторы случайных данных """
from enum import Enum
from random import randint
from string import ascii_lowercase, digits

from mimesis.locales import Locale
from mimesis.providers import Cryptographic, Datetime, Internet, Person
from mimesis.random import Random

from generators.log_result_to_allure import log_result_to_allure

attachment_name = 'РЕЗУЛЬТАТ'
CYRILLIC_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class AlphabetEnum(Enum):
    CYRILLIC = CYRILLIC_ALPHABET
    LATIN = ascii_lowercase
    CYRILLIC_DIGITS = CYRILLIC_ALPHABET + digits
    LATIN_DIGITS = ascii_lowercase + digits
    CYRILLIC_LATIN_DIGITS = CYRILLIC_ALPHABET + ascii_lowercase + digits


@log_result_to_allure(name='Генератор. Получить случайное число')
def get_random_number(start: int = 1, end: int = 999999, length: int = None, needs_allure: bool = True) -> int:
    """ Получить случайное число в заданном диапазоне или заданной длины

    Args:
        start:  начало диапазона
        end:    конец диапазона
        length: длина числа
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return randint(10 ** (length - 1), (10 ** length) - 1) if length else randint(start, end)


@log_result_to_allure(name='Генератор. Получить случайную строку')
def get_random_string(
        alphabet: AlphabetEnum or str = AlphabetEnum.CYRILLIC_LATIN_DIGITS,
        length: int = 10,
        needs_allure: bool = True
) -> str:
    """ Получить случайную строку

    Args:
        alphabet: алфавит
        length: длина строки
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return Random().generate_string(
        str_seq=alphabet.value if isinstance(alphabet, AlphabetEnum) else alphabet,
        length=length
    )


@log_result_to_allure(name='Генератор. Получить случайный UUID')
def get_random_uuid(needs_allure: bool = True):
    """ Получить случайный UUID

    Args:
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return Cryptographic().uuid()


@log_result_to_allure(name='Генератор. Получить случайный телефон')
def get_random_telephone(mask: str = '+7(###)###-##-##', needs_allure: bool = True) -> str:
    """ Получить случайный номер телефона в заданном формате

    Args:
        mask: формат номера телефона
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return Person(locale=Locale.RU).telephone(mask=mask)


@log_result_to_allure(name='Генератор. Получить случайную дату')
def get_random_date(mask: str = '%d.%m.%Y', needs_allure: bool = True) -> str:
    """ Получить случайную дату в заданном формате

    Args:
        mask: формат даты
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return Datetime(locale=Locale.RU).date(2000, 2020).strftime(mask)


@log_result_to_allure(name='Генератор. Получить случайную почту')
def get_random_email(
        domains: tuple = ('mail.ru', 'gmail.com', 'yandex.ru', 'sberbank.ru', 'mail.ca.sbrf.ru'),
        needs_allure: bool = True
) -> str:
    """ Получить случайный e-mail

    Args:
        domains: набор доменов
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return Person(locale=Locale.RU).email(domains=domains)


@log_result_to_allure(name='Генератор. Получить случайную ссылку')
def get_random_link(needs_allure: bool = True):
    """ Получить случайную ссылку

    Args:
        needs_allure: Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return Internet().uri()
