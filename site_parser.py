import requests
from bs4 import BeautifulSoup
import logging

class SiteParser:
    def __init__(self, url, link_storage):
        self.url = url
        self.link_storage = link_storage
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def fetch_links(self):
        """Получает ссылки с заданного URL и возвращает их в виде множества."""
        print(f"Запрос к {self.url}...")
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Проверка на ошибки HTTP
            soup = BeautifulSoup(response.content, 'html.parser')
            links = set()

            # Ищем все ссылки в документах
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']
                # Полный URL
                if href.startswith('/'):
                    href = 'https://www.garant.ru' + href
                if href.startswith('https://www.garant.ru/news'):
                    links.add(href)

            print(f"Получены {len(links)} ссылок с {self.url}.")
            logging.info(f"Получены {len(links)} ссылок с {self.url}.")
            return links
        except requests.RequestException as e:
            print(f"Ошибка при запросе к {self.url}: {e}")
            logging.error(f"Ошибка при запросе к {self.url}: {e}")
            return set()

    def update_new_links(self):
        """Обновляет новые ссылки, которые еще не были сохранены."""
        print("Обновление новых ссылок...")
        current_links = self.fetch_links()
        sent_links = self.link_storage.load_sent_links()

        # Находим новые ссылки, которые еще не сохранены
        new_links = current_links - sent_links

        if new_links:
            sent_links.update(new_links)
            self.link_storage.save_sent_links(sent_links)
            print(f"Обновлено {len(new_links)} новых ссылок.")
            logging.info(f"Обновлено {len(new_links)} новых ссылок.")
        else:
            print("Нет новых ссылок для обновления.")
            logging.info("Нет новых ссылок для обновления.")

        return new_links

