import re

class SignHelper:

    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector('input[type="submit"]').click()

        # Письмо приходит в папку C:\Users\annuta567\james-2.3.1\apps\james\var\mail\inboxes\user_qwerty
        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        wd.get(url)
        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector('input[value="Update User"]').click()


    # В тексте (не заголовке) письма есть ссылка http://localhost/mantisbt-1.2.20/verify.php?id=2&confirm_hash=2041b6565aac9380a2e0e3fabe74414d
    def extract_confirmation_url(self, text):
        # group(0) - извлекаем все
        return re.search("http://.*$", text, re.MULTILINE).group(0)
