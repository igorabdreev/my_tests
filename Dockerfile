# Сборка образа с проектом автотестирования

# Выбор базового образа
FROM python3.9.6

# Установка рабочей директории
WORKDIR /tmp/aft_tests

# Копирование Pipfile и Pipfile.lock
COPY Pipfile* ./

# Флаг установки виртуального окружения в папку с проектом
ENV PIPENV_VENV_IN_PROJECT=1

# Прокидывание токена
ARG TOKEN=${TOKEN}

# Установка необходимых пакетов
# Установка виртуального окружения
RUN pip install --no-cache-dir --upgrade \
        -i http://token:$TOKEN@sberosc.sigma.sbrf.ru/repo/pypi/simple \
        --trusted-host=sberosc.sigma.sbrf.ru \
        pip==23.1.2 pipenv==2023.6.12 setuptools==68.0.0 \
    && pipenv install

# Копирование проекта
COPY . .

# Установка прав доступа
RUN chown -R 2000:2000 /tmp/aft_tests \
    && chmod -R 777 test_data reports \
    && chmod +x entrypoint.sh

# Установка пользователя в контейнере
USER 2000

# Определение скрипта при запуске контейнера
ENTRYPOINT ["./entrypoint.sh"]