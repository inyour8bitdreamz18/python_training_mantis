import pytest
from fixture.application import Application
import json
import os.path
import ftputil


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

# pytest позволяет использовать фикстуру в др фикстурах
@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))

# Чтобы не читать config_file при каждом запуске, также как и с fixture, вынесем глобальную переменную target
@pytest.fixture
def app(request, config):
    # Создает Фикстуру
    global fixture
    global target
    # Через объект request дали доступ к конфигам
    browser = request.config.getoption("--browser")
    web_config = config["web"]
    webadmin_config = config["webadmin"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    # Пароль админа нужно указывать при запуске, и он нигде не сохраняется
    fixture.session.ensure_login(username=webadmin_config['username'], password=webadmin_config['password'])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")

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


