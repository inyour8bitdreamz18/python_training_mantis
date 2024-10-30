import pytest
from fixture.application import Application
import json
import os.path



# Функция, инициализирующая Фикстуру (обязательна метка перед самой функцией)
# @pytest.fixture(scope="session") убрали scope, чтобы избежать падения браузера

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        # Сначала преобразуем в абсолютный путь os.path.abspath(__file__), а затем найдем директорию os.path.dirname()
        # А потом приклеим наш путь с директорией к конфиг файлу (мы вычисляем путь относительно конфиг файла)
        # Теперь тесты будут запускаться вне зависимости от рабочей директории
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


# Чтобы не читать config_file при каждом запуске, также как и с fixture, вынесем глобальную переменную target
@pytest.fixture
def app(request):
    # Создает Фикстуру
    global fixture
    global target
    # Через объект request дали доступ к конфигам
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    return fixture


# Разрушает Фикстуру и разлогинивается
# autouse=True - автоматически будет вызываться
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture



# Cохранили конфиги для вызова тестов через консоль
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    # Пароль, юзернейм и урл сохранили в отдельный файл target.json
    parser.addoption("--target", action="store", default="target.json")


