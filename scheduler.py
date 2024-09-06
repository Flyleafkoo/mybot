import schedule
import time
import logging
from datetime import datetime, timedelta
import telebot


def run_scheduler():
    logging.info("Запуск планировщика...")
    while True:
        logging.debug("Проверка расписания...")
        schedule.run_pending()
        time.sleep(100)


class Scheduler:
    def __init__(self, bot_token, group_ids, specific_group_id, employee_database):
        self.bot = telebot.TeleBot(bot_token)
        self.group_ids = group_ids
        self.specific_group_id = specific_group_id
        self.employee_database = employee_database
        self.setup_logging()
        self.setup_schedule()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('bot.log')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(console_handler)

    def setup_schedule(self):
        schedule.every().day.at("08:47").do(self.send_good_morning)
        schedule.every().day.at("08:30").do(self.daily_check)
        schedule.every().day.at("08:51").do(self.send_birthday_messages)

    def daily_check(self):
        now = datetime.now()
        if now.hour == 9:
            self.send_monthly_update()
            self.send_last_workday_message()
            self.send_25th_day_message()

    def send_good_morning(self):
        now = datetime.now()
        if now.weekday() >= 5:  # 5 - суббота, 6 - воскресенье
            logging.info("Сегодня выходной, утреннее сообщение не отправляется.")
            return

        logging.info("Отправка утреннего сообщения начинается")
        try:
            if not self.group_ids:
                logging.warning("Список group_ids пуст!")
                return
            for group_id in self.group_ids:
                try:
                    logging.info(f"Отправка сообщения в группу: {group_id}")
                    result = self.bot.send_message(group_id, 'Доброе утро! Желаю всем отличного дня!')
                    logging.info(f"Результат отправки: {result}")
                except Exception as e:
                    logging.error(f"Ошибка при отправке в группу {group_id}: {e}")
        except Exception as e:
            logging.error(f"Ошибка при отправке утреннего сообщения: {e}")

    def send_monthly_update(self):
        now = datetime.now()
        fifteenth, last_weekday = self.get_message_dates()

        logging.debug(
            f"Текущая дата: {now.date()}, 15-е число: {fifteenth.date()}, последний рабочий день: {last_weekday.date()}")

        if now.date() == fifteenth.date() or now.date() == last_weekday.date():
            message = "Уважаемые коллеги, не забываем о необходимости сдачи отчета о проделанной работе"
            self._send_to_groups(message)
        else:
            logging.info("Сегодня не нужный день для отправки ежемесячного обновления")

    def send_last_workday_message(self):
        now = datetime.now()
        last_day = (now.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        while last_day.weekday() >= 5:
            last_day -= timedelta(days=1)
        if now.date() == last_day.date():
            if self.specific_group_id:
                message = "Уважаемые коллеги, не забудьте начислить амортизацию!"
                self._send_to_specific_group(message)
        else:
            logging.info("Сегодня не последний рабочий день месяца")

    def send_25th_day_message(self):
        def send_25th_day_message(self):
            now = datetime.now()
            if now.day == 25 and now.weekday() < 5:  # Проверка, что 25-е — будний день
                message = "Уважаемые коллеги, не забываем сформировать журналы!"
                self._send_to_groups(message)
            else:
                # Если 25-е выпадает на выходные, отправить в последний рабочий день перед выходными
                days_to_subtract = (now.weekday() - 4) % 7
                previous_workday = now - timedelta(days=days_to_subtract)
                if previous_workday.day == 25:
                    message = "Уважаемые коллеги, не забываем сформировать журналы!"
                    self._send_to_groups(message)
                else:
                    logging.info("Сегодня не 25 число и не выходной день")

    def send_first_workday_message(self):
        now = datetime.now()
        first_day = now.replace(day=1)

        # Найти первый рабочий день месяца
        if first_day.weekday() >= 5:  # Если первый день месяца — выходной
            first_workday = first_day + timedelta(days=(7 - first_day.weekday()))
        else:
            first_workday = first_day

        # Если сегодня первый рабочий день месяца
        if now.date() == first_workday.date():
            if self.specific_group_id:
                message = "Доброе утро! Не забудьте провести инвентаризацию по правам пользования за прошедший месяц."
                self._send_to_specific_group(message)
        else:
            logging.info("Сегодня не первый рабочий день месяца")

    def get_message_dates(self):
        now = datetime.now()
        fifteenth = now.replace(day=15)
        last_day_of_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        last_weekday = last_day_of_month - timedelta(days=(last_day_of_month.weekday() + 1) % 7)
        return fifteenth, last_weekday

    def _send_to_groups(self, message):
        for group_id in self.group_ids:
            try:
                logging.info(f"Отправка сообщения в группу: {group_id}")
                result = self.bot.send_message(group_id, message)
                logging.info(f"Результат отправки: {result}")
            except Exception as e:
                logging.error(f"Ошибка при отправке в группу {group_id}: {e}")

    def _send_to_specific_group(self, message):
        try:
            logging.info(f"Отправка сообщения в конкретную группу: {self.specific_group_id}")
            result = self.bot.send_message(self.specific_group_id, message)
            logging.info(f"Результат отправки: {result}")
        except Exception as e:
            logging.error(f"Ошибка при отправке в группу {self.specific_group_id}: {e}")

    def send_birthday_messages(self):
        birthdays = self.employee_database.get_birthdays_today()
        if birthdays:
            message = "С ДНЕМ РОЖДЕНИЯ! 🎉 " + ", ".join(birthdays)
            self._send_to_groups(message)
        else:
            logging.info("Сегодня нет именинников.")
