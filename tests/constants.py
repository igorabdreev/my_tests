"""Переменные для работы в сервисах"""
ERROR_SUCCESS_MSG = 'Поле "success" отлично от true'
ERROR_STATUS_MSG = 'Код статуса ответа {code} не совпадает с ожидаемым: 200'
ERROR_STATUS_CUSTOM_MSG = 'Код статуса ответа {code} не совпадает с ожидаемым: {exp}'
ERROR_BODY_VALID_MSG = f'Ошибка при валидации тела ответа'
ERROR_FORBIDDEN_STATUS_MSG = 'Код статуса ответа не совпадает с ожидаемым: 403'

class Ansver:

    """Переменные для работы в сервисах"""
    ERROR_SUCCESS_MSG = 'Поле "success" отлично от true'
    ERROR_STATUS_MSG = 'Код статуса ответа {code} не совпадает с ожидаемым: 200'
    ERROR_STATUS_CUSTOM_MSG = 'Код статуса ответа {code} не совпадает с ожидаемым: {exp}'
    ERROR_BODY_VALID_MSG = f'Ошибка при валидации тела ответа'
    ERROR_FORBIDDEN_STATUS_MSG = 'Код статуса ответа не совпадает с ожидаемым: 403'
    ERROR_SERVER_MSG = 'Код статуса ответа не совпадает с ожидаемым: 500'

    ERROR_MSG_WITHOUT_WIDGET = 'Прогресс выполнения цели в периоде после создания цели без учета веса на {code} странице отличен от ожидаемого'
    ERROR_MSG_WITHOUT_WIDGET_AFTER_ADD_METRIC = 'Прогресс выполнения цели в периоде после добавления метрики без учета веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITHOUT_WIDGET_AFTER_DONE_METRIC = 'Прогресс выполнения цели в периоде после выполнения метрики без учета веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITHOUT_WIDGET_AFTER_EDIT_METRIC = 'Прогресс выполнения цели в периоде после изменения метрики без учета веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITHOUT_WIDGET_AFTER_DELETE_BINARY = 'Прогресс выполнения цели в периоде после удаления бинарного кр без учета веса цели на {code} отличен от ожидаемого'

    ERROR_MSG_WITH_WIDGET = 'Прогресс выполнения цели в периоде после создания цели с учетом веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITH_WIDGET_AFTER_ADD_METRIC = 'Прогресс выполнения цели в периоде после добавления метрики с учетом веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITH_WIDGET_AFTER_DONE_METRIC = 'Прогресс выполнения цели в периоде после выполнения метрики с учетом веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITH_WIDGET_AFTER_EDIT_METRIC = 'Прогресс выполнения цели в периоде после изменения метрики с учетом веса цели на {code} отличен от ожидаемого'
    ERROR_MSG_WITH_WIDGET_AFTER_DELETE_BINARY = 'Прогресс выполнения цели в периоде после удаления бинарного кр с учетом веса цели на {code} отличен от ожидаемого'

    ERROR_MSG_WITH_WIDGET_AFTER_EDIT_WIDGET = 'Прогресс выполнения цели в периоде после изменения веса цели на {code} отличен от ожидаемого'
