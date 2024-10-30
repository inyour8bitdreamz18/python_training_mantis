from selenium import wd
from fixture.session import SessionHelper

# Если нужно постоянно тестировать данные из БД, то добавляем DBHelper в Application
# Если нет, то создаем отдельную фикстуру для работы с БД

class Application:

    def __init__(self, browser, base_url):
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
        self.base_url = base_url

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



