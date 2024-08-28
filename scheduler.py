import schedule
import time
import logging
from datetime import datetime, timedelta
import telebot



class Scheduler:
    def __init__(self, bot_token, group_ids, specific_group_id):
        self.bot = telebot.TeleBot(bot_token)
        self.group_ids = group_ids
        self.specific_group_id = specific_group_id
        self.setup_schedule()

    def setup_schedule(self):
        schedule.every().day.at("08:30").do(self.send_good_morning)
        schedule.every().day.at("09:00").do(self.daily_check)

    def run_scheduler(self):
        print("Запуск планировщика...")
        while True:
            print("Проверка расписания...")
            schedule.run_pending()
            time.sleep(360)

    def daily_check(self):
        now = datetime.now()
        if now.hour == 9:
            self.send_monthly_update()
            self.send_last_workday_message()
            self.send_25th_day_message()

    def send_good_morning(self):
        print("Отправка утреннего сообщения начинается")
        try:
            if not self.group_ids:
                print("Список group_ids пуст!")
                return
            for group_id in self.group_ids:
                try:
                    print(f"Отправка сообщения в группу: {group_id}")
                    result = self.bot.send_message(group_id, 'Доброе утро! Желаю всем отличного дня!')
                    print(f"Результат отправки: {result}")
                except Exception as e:
                    print(f"Ошибка при отправке в группу {group_id}: {e}")
                    logging.error(f"Ошибка при отправке в группу {group_id}: {e}")
        except Exception as e:
            print(f"Ошибка при отправке утреннего сообщения: {e}")
            logging.error(f"Ошибка при отправке утреннего сообщения: {e}")

    def send_monthly_update(self):
        now = datetime.now()
        fifteenth, last_weekday = self.get_message_dates()

        if now.date() == fifteenth.date() or now.date() == last_weekday.date():
            message = "Уважаемые коллеги, не забываем о необходимости сдачи отчета о проделанной работе"
            for group_id in self.group_ids:
                try:
                    print(f"Отправка ежемесячного обновления в группу: {group_id}")
                    result = self.bot.send_message(group_id, message)
                    print(f"Результат отправки: {result}")
                except Exception as e:
                    print(f"Ошибка при отправке в группу {group_id}: {e}")
                    logging.error(f"Ошибка при отправке в группу {group_id}: {e}")
        else:
            print("Сегодня не нужный день для отправки ежемесячного обновления")

    def send_last_workday_message(self):
        now = datetime.now()
        last_day = (now.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        while last_day.weekday() >= 5:
            last_day -= timedelta(days=1)
        if now.date() == last_day.date():
            if self.specific_group_id:
                message = "Уважаемые коллеги, не забудьте начислить амортизацию!"
                try:
                    print(f"Отправка сообщения в конкретную группу: {self.specific_group_id}")
                    result = self.bot.send_message(self.specific_group_id, message)
                    print(f"Результат отправки: {result}")
                except Exception as e:
                    print(f"Ошибка при отправке в группу {self.specific_group_id}: {e}")
                    logging.error(f"Ошибка при отправке в группу {self.specific_group_id}: {e}")
        else:
            print("Сегодня не последний рабочий день месяца")

    def send_25th_day_message(self):
        now = datetime.now()
        if now.day == 25:
            # Отправка сообщения 25 числа
            message = "Уважаемые коллеги, не забываем сформировать журналы!"
            for group_id in self.group_ids:
                try:
                    print(f"Отправка сообщения в группу: {group_id}")
                    result = self.bot.send_message(group_id, message)
                    print(f"Результат отправки: {result}")
                except Exception as e:
                    print(f"Ошибка при отправке в группу {group_id}: {e}")
                    logging.error(f"Ошибка при отправке в группу {group_id}: {e}")
        elif now.weekday() in [5, 6]:  # Если сегодня выходной
            # Определение предыдущего рабочего дня
            days_to_subtract = (now.weekday() - 4) % 7  # 4 = пятница (рабочий день перед выходными)
            previous_workday = now - timedelta(days=days_to_subtract)
            if previous_workday.day == 25:
                # Отправка сообщения в предыдущий рабочий день
                message = "Уважаемые коллеги, не забываем сформировать журналы!"
                for group_id in self.group_ids:
                    try:
                        print(f"Отправка сообщения в группу: {group_id}")
                        result = self.bot.send_message(group_id, message)
                        print(f"Результат отправки: {result}")
                    except Exception as e:
                        print(f"Ошибка при отправке в группу {group_id}: {e}")
                        logging.error(f"Ошибка при отправке в группу {group_id}: {e}")
        else:
            print("Сегодня не 25 число и не выходной день")

    def send_first_workday_message(self):
        now = datetime.now()
        first_day = now.replace(day=1)

        # Найти первый рабочий день месяца
        if first_day.weekday() >= 5:  # Если первый день месяца — выходной
            first_workday = first_day + timedelta(days=(7 - first_day.weekday()))  # Сдвинуть на следующий понедельник
        else:
            first_workday = first_day  # Первый день месяца — рабочий день

        # Если первый день месяца совпадает с первым рабочим днем месяца
        if now.date() == first_workday.date():
            if self.specific_group_id:
                message = "Доброе утро! Не забудьте провести инвентаризацию за прошедший месяц."
                try:
                    print(f"Отправка сообщения в конкретную группу: {self.specific_group_id}")
                    result = self.bot.send_message(self.specific_group_id, message)
                    print(f"Результат отправки: {result}")
                except Exception as e:
                    print(f"Ошибка при отправке в группу {self.specific_group_id}: {e}")
                    logging.error(f"Ошибка при отправке в группу {self.specific_group_id}: {e}")
        else:
            print("Сегодня не первый рабочий день месяца")

    def get_message_dates(self):
        now = datetime.now()
        fifteenth = now.replace(day=15)
        last_day_of_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        last_weekday = last_day_of_month - timedelta(days=(last_day_of_month.weekday() + 1) % 7)
        return fifteenth, last_weekday
