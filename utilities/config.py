from pathlib import Path

from selenium.webdriver.chrome.webdriver import WebDriver

from utilities.vault.connector import VaultConnector


class Config:
    """Абстрактный класс с параметрами запуска. Заполняется при старте проекта"""
    driver: WebDriver
    vault: VaultConnector
    debug: bool = False
    stand: str
    keycloak_url: str
    log_level = "INFO"
    test_data_dir: Path = Path('test_data').absolute()
    temp_dir: Path = test_data_dir / 'temp'
    xlsx_dir: Path = temp_dir / 'xlsx'
    csv_dir: Path = temp_dir / 'csv'
    lock_dir: Path = temp_dir / 'session-fixtures'
    timeout: int = 30
    url_zephyr: str = 'https://jira.sberbank.ru/secure/Tests.jspa#/testCase'
    web_url: str
