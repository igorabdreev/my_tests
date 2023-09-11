"""Пути до драйверов и дефолтные настройки."""
from pathlib import Path

WEB_DRIVERS_DIR = Path('web') / 'drivers'
TIMEOUT = 15


class ChromeConfig:
    """Класс для хранения конфигурации Chrome драйвера."""
    exec_path_darwin = WEB_DRIVERS_DIR / 'chromedriver_mac'
    exec_path_linux = WEB_DRIVERS_DIR / 'chromedriver_linux'
    exec_path_win32 = WEB_DRIVERS_DIR / 'chromedriver.exe'
    exec_path_win64 = WEB_DRIVERS_DIR / 'chromedriver.exe'
    default_options = [
        '--window-size=1920,1080',
        '--ignore-certificate-errors',
        '--disable-gpu',
        '--no-sandbox',
        'lang=ru'
    ]


class YandexConfig(ChromeConfig):
    """Класс для хранения конфигурации Yandex драйвера."""
    exec_path_darwin = WEB_DRIVERS_DIR / 'yandexdriver_mac'
    exec_path_linux = WEB_DRIVERS_DIR / 'yandexdriver_linux'
    exec_path_win32 = WEB_DRIVERS_DIR / 'yandexdriver.exe'
    exec_path_win64 = WEB_DRIVERS_DIR / 'yandexdriver.exe'


class SafariConfig:
    """Класс для хранения конфигурации Safari драйвера."""
    exec_path_darwin = WEB_DRIVERS_DIR / 'safari_mac'
    default_options = []


class SelenoidConfig:
    """Класс для хранения конфигурации Selenoid."""
    HUB_URL = "http://tkles-hrplt0112.vm.esrt.cloud.sbrf.ru:4444/wd/hub"
    CLIPBOARD_URL = "http://tkles-hrplt0112.vm.esrt.cloud.sbrf.ru:8080/ws/clipboard/"
    DOWNLOAD_URL = "http://tkles-hrplt0112.vm.esrt.cloud.sbrf.ru:4444/download/"
    OPTIONS = 'selenoid:options'
    CAPABILITIES = {
        'chrome': {
            'browserName': 'chrome',
            'browserVersion': '86.0',

            OPTIONS: {
                'enableVNC': True,
                'enableVideo': False
            }
        },
        'yandex': {
            'browserName': 'chrome',
            'browserVersion': 'yandex: 21.9',

            OPTIONS: {
                'enableVNC': True,
                'enableVideo': False
            }
        },
        'safari': {
            'browserName': 'safari',
            'browserVersion': '14.0',

            OPTIONS: {
                'enableVNC': True,
                'enableVideo': False
            }
        }
    }
