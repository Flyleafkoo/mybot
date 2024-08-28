import logging

import requests
from bs4 import BeautifulSoup

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename='site_parser.log', format='%(asctime)s - %(levelname)s - %(message)s')

class SiteParser:
    def __init__(self, url, link_storage):
        self.url = url
        self.link_storage = link_storage

    def fetch_links(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Проверка успешности запроса
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]  # Извлечение всех ссылок
            logging.info(f"Найдено {len(links)} ссылок на странице {self.url}")
            return links
        except requests.RequestException as e:
            logging.error(f"Ошибка при запросе страницы: {e}")
            return []

    def update_new_links(self):
        current_links = self.fetch_links()
        sent_links = self.link_storage.load_sent_links()
        new_links = set(current_links) - sent_links
        if new_links:
            sent_links.update(new_links)
            self.link_storage.save_sent_links(sent_links)
        logging.info(f"Обновлено {len(new_links)} новых ссылок.")
        return new_links