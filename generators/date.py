"""Генераторы даты и времени"""
from datetime import date, datetime, timedelta

from generators.log_result_to_allure import log_result_to_allure


@log_result_to_allure(name='Генератор. Получить текущую дату и/или время в формате')
def get_current_datetime(fmt: str = "%d.%m.%YT%H:%M:%S", needs_allure: bool = True) -> str:
    """Получить текущую дату

    Args:
        fmt: формат даты
        needs_allure:   Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    return datetime.now().strftime(fmt)


@log_result_to_allure(name='Генератор. Получить дату и/или время со смещением')
def get_datetime_with_offset(
        fmt: str = "%d.%m.%YT%H:%M:%S",
        to_the_future: bool = True,
        utc: bool = False,
        working_day: bool = False,
        holiday: bool = False,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
        needs_allure: bool = True
) -> str:
    """ Получить текущую дату со сдвигом

    Args:
        fmt:            формат времени. Например "%Y-%m-%dT%H:%M:%S+03:00"
        to_the_future:  флаг указывающий сдвиг в будущее
        working_day:    смещать дату на рабочий день
        holiday:        смещать дату на выходной день
        seconds:        количество секунд сдвига
        minutes:        количество минут сдвига
        hours:          количество часов сдвига
        days:           количество дней сдвига
        weeks:          количество недель сдвига
        utc:            флаг необходимости использования часового пояса UTC
        needs_allure:   Флаг логгирования в allure
            - True ->   Логгирует в allure
            - False ->  НЕ логгирует в allure
    """
    date_with_offset = datetime.utcnow() if utc else datetime.today()
    delta = timedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)
    date_with_offset = date_with_offset + delta if to_the_future else date_with_offset - delta

    if working_day:
        number_of_day = date.isoweekday(date_with_offset)

        if number_of_day in (6, 7):
            date_with_offset += timedelta(days=(8 - number_of_day))

    if holiday:
        date_with_offset += timedelta(days=(6 - date.isoweekday(date_with_offset)))

    return date_with_offset.strftime(fmt)
