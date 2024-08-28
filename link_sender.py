import time
import logging
import random
from threading import Thread
from datetime import datetime

class LinkSender:
    def __init__(self, bot, link_storage, site_parser, group_ids):
        self.bot = bot
        self.link_storage = link_storage
        self.site_parser = site_parser
        self.group_ids = group_ids
        self.scheduler_thread = Thread(target=self.schedule_link_updates)
        self.scheduler_thread.start()

    def schedule_link_updates(self):
        while True:
            try:
                self.site_parser.update_new_links()
                logging.info("Обновление ссылок выполнено.")
            except Exception as e:
                logging.error(f"Ошибка при обновлении ссылок: {e}")
            time.sleep(43200)  # 12 часов в секундах

    def is_valid_link(self, link):
        return link.startswith("https://www.garant.ru/news")

    def is_advertisement(self, link):
        # Пример фильтрации рекламных ссылок (можно настроить)
        ad_keywords = ['ads', 'advert', 'promotions']
        return any(keyword in link for keyword in ad_keywords)

    def send_links(self):
        try:
            links = self.link_storage.load_sent_links()
            if links:
                filtered_links = [link for link in links if self.is_valid_link(link) and not self.is_advertisement(link)]
                if filtered_links:
                    link = random.choice(filtered_links)  # Выбираем случайную ссылку
                    self.link_storage.save_sent_links(set(filtered_links) - {link})  # Удаляем выбранную ссылку
                    for group_id in self.group_ids:
                        try:
                            logging.info(f"Попытка отправки ссылки в группу {group_id}: {link}")
                            self.bot.send_message(group_id, link)
                            logging.info(f"Ссылка отправлена в группу {group_id}: {link}")
                        except Exception as e:
                            logging.error(f"Ошибка при отправке ссылки в группу {group_id}: {e}")
        except Exception as e:
            logging.error(f"Ошибка при отправке ссылок: {e}")

    def run_sender(self):
        while True:
            now = datetime.now()
            if now.hour in [9, 17]:  # 6:00 и 18:00
                self.send_links()
                # Ждем 1 час, чтобы избежать повторного отправления в течение одного часа
                time.sleep(3600)
            time.sleep(60)  # Проверяем время каждую минуту
