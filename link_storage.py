import json
import os
import logging

class LinkStorage:
    def __init__(self, file_path='sent_links.json'):
        self.file_path = file_path
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_sent_links(self):
        """Загружает ссылки из файла и возвращает их в виде множества строк."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)
                    # Проверяем, что данные являются списком строк
                    if all(isinstance(item, str) for item in data):
                        links = set(data)  # Возвращаем множество строк
                        logging.info(f"Загружены ссылки: {links}")
                        return links
                    else:
                        logging.error("Формат данных в файле неверный. Ожидался список строк.")
                        return set()
            except json.JSONDecodeError as e:
                logging.error(f"Ошибка чтения JSON файла: {e}")
                return set()
            except IOError as e:
                logging.error(f"Ошибка при открытии файла: {e}")
                return set()
            except Exception as e:
                logging.error(f"Неизвестная ошибка при загрузке ссылок: {e}")
                return set()
        else:
            logging.warning("Файл с ссылками не найден. Возвращается пустой набор.")
            return set()

    def save_sent_links(self, sent_links):
        """Сохраняет ссылки в файл."""
        try:
            with open(self.file_path, 'w') as file:
                # Преобразуем множество строк в список
                json.dump(list(sent_links), file, indent=4)
                logging.info(f"Ссылки сохранены: {sent_links}")
        except IOError as e:
            logging.error(f"Ошибка записи в файл: {e}")
        except Exception as e:
            logging.error(f"Неизвестная ошибка при сохранении ссылок: {e}")
