import poplib # Стандартная библиотека, для получения
import email # Для анализа текста
import time


class MailHelper:

    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        # Письмо может прийти не туда, поэтому будем делать 5 раз
        for i in range(5):
            pop = poplib.POP3(self.app.config['james']['host'])
            pop.user(username)
            pop.pass_(password)
            # Определяем количество писем .stat() - предоставляет стат. инфо
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    # Получаем письмо, (n+1) т.к. индексация начинается с 1
                    # Возвращает кортеж
                    maglines = pop.retr(n+1)[1]
                    # Так как мы получаем байтовые строки, нужно использовать перекодировку
                    magtext = "\n".join(map(lambda x: x.decode('utf-8'), maglines))
                    mag = email.message_from_string(magtext)
                    if mag.get("Subject") == subject:
                        # Закрываем сессию методом quit() - закрытие с сохранением
                        # .close() - закрытие без сохранения
                        pop.dele(n+1)
                        pop.quit()
                        return mag.get_payload()

            pop.close()
            time.sleep(3) # Ждем письмо
        return None
