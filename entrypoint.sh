#! /bin/bash

# Скрипт для запуска тестов на тестовых стендах

if [ "${BROWSER}" != "" ]; then
  SELENOID="--selenoid --browser=${BROWSER}"
fi

# Запускаем тесты
pipenv run pytest ${THREADS} -m "${TAGS}" ${SELENOID} --stand=${STAND} \
        --role_id=${ROLE_ID} --secret_id=${SECRET_ID} --keycloak_url=${KEYCLOAK_URL} \
        --vault_url=${VAULT_URL} --vault_namespace=${VAULT_NAMESPACE} --vault_mount=${VAULT_MOUNT} \
        --web_url=${WEB_URL} --disable-warnings --junitxml=reports/report.xml --alluredir=reports/allure-results \
        --log_level=${LOG_LEVEL}

exit_code=$?

# Архивируем результаты Allure
cd reports; echo -e "Tags=${TAGS}\nStand=${STAND}\nBrowser=${BROWSER}" > allure-results/environment.properties
tar -cvzf allure-results.tar.gz allure-results/ report.xml

# Отправляем результаты в Allure Server
curl --location --request POST "${ALLURE_URL}/upload-allure" \
     --form data='{"build": "'${BUILD_NUMBER}'", "job_name": "'${JOB_NAME}'"}' \
     --form allure_file=@allure-results.tar.gz

exit $exit_code
