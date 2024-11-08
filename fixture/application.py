from selenium import wd
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.signup import SignHelper
from fixture.mail import MailHelper
from fixture.soap import SoapHelper


# Если нужно постоянно тестировать данные из БД, то добавляем DBHelper в Application
# Если нет, то создаем отдельную фикстуру для работы с БД

class Application:

    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = wd.Firefox()
        elif browser == "chrome":
            self.wd = wd.Chrome()
        elif browser == "ie":
            self.wd = wd.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)

        #self.wd.implicitly_wait(30)
        #ссылка на файл SessionHelper, GroupHelper, ContactHelper
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)
        self.config = config
        self.base_url = config["web"]["baseUrl"]

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
