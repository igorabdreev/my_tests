import csv
from typing import List, Any
from pathlib import Path
from uuid import uuid4

from utilities.config import Config
from utilities.custom_allure import step


def save_to_csv(data: List[List[Any]], file_name: str, headers: List = None, delimiter: str = ';') -> Path:
    """ Создать, записать, сохранить данные в csv-файл

    Args:
        headers: Список заголовков
        data: список списков с данными
        file_name: Имя файла
        delimiter: разделитель
    """

    if not (path_folder := Config.csv_dir / str(uuid4())).exists():
        with step(f'Создать путь до папки с csv "{path_folder}"'):
            path_folder.mkdir(parents=True)

    with step(f'Открыть файл {(path := path_folder / file_name)}'):
        with open(file=path, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)

            with step('Запись заголовков в файл'):

                if headers:
                    if not all(len(row) == len(headers) for row in data):
                        raise ValueError('Количество элементов в заголовке не равно количеству элементов в списках')

                    writer.writerow(headers)

            with step('Запись данных в файл'):
                [writer.writerow(row) for row in data]

    return path
