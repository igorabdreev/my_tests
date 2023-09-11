"""Класс для работы с сущностью локатора"""
from re import findall

from utilities.logging import logger


class Locator:
    """Класс локатора"""
    name: str
    locator: tuple[str, str]

    def __init__(self, name: str, locator: tuple[str, str]):
        """
        Args:
            name: название локатора
            locator: значение локатора
        """
        self.name = name
        self.locator = locator

    def __add__(self, selector: str) -> str:
        return self.locator[1] + selector

    def __repr__(self) -> str:
        return f'Locator({self.name=}, {self.locator=})'

    def __str__(self) -> str:
        return f'Элемент "{self.name}" c локатором "{self.locator}"'

    def __call__(self, **kwargs):
        try:
            return Locator(
                name=self.name.format(**kwargs),
                locator=(self.locator[0], self.locator[1].format(**kwargs))
            )

        except KeyError as e:
            pattern = r'\{([A-Za-z_0-9]*)\}'

            kwargs_in_name = findall(pattern=pattern, string=self.name)
            kwargs_in_loc = findall(pattern=pattern, string=self.locator[1])

            missing_kwargs = ', '.join([kwarg for kwarg in {*kwargs_in_name, *kwargs_in_loc} if kwarg not in kwargs])
            logger.error(f'Не переданы значения для форматирования {self}\n\tОтсутствуют значения: {missing_kwargs}')

            e.args = f'Отсутствуют значения [ {missing_kwargs} ] для локатора {self}!',

            raise e
