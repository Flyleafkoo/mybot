# link_sender.py
import time
import logging
import re
from threading import Thread


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
            self.site_parser.update_new_links()
            time.sleep(43200)  # 12 часов в секундах

    def is_valid_link(self, link):
        # Регулярное выражение для проверки ссылки по типу 'glavkniga.ru/news' и продолжения
        pattern = re.compile(r'^https?://(?:www\.)?glavkniga\.ru/news.*$', re.IGNORECASE)
        return pattern.match(link) is not None

    def is_advertisement(self, link):
        # Пример использования регулярного выражения для фильтрации рекламных ссылок
        ad_keywords = ['ads', 'advert', 'promotions']
        if any(keyword in link for keyword in ad_keywords):
            return True

        # Также можно добавить список известных рекламных доменов
        ad_domains = ['adserver.com', 'adsnetwork.com']
        if any(domain in link for domain in ad_domains):
            return True

        return False

    def send_links(self):
        links = self.link_storage.load_sent_links()
        if links:
            # Фильтрация ссылок, оставляя только те, что соответствуют требуемому шаблону и не являются рекламными
            filtered_links = [link for link in links if self.is_valid_link(link) and not self.is_advertisement(link)]
            if filtered_links:
                link = filtered_links.pop()
                self.link_storage.save_sent_links(filtered_links)
                for group_id in self.group_ids:
                    try:
                        self.bot.send_message(group_id, link)
                        logging.info(f"Ссылка отправлена в группу {group_id}: {link}")
                    except Exception as e:
                        logging.error(f"Ошибка при отправке ссылки в группу {group_id}: {e}")

    def run_sender(self):
        while True:
            now = time.localtime()
            if 9 <= now.tm_hour < 17:  # 9:00 до 17:00
                self.send_links()
            time.sleep(3600)  # 1 час
