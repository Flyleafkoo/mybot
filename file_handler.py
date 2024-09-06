import os
import telebot
from telebot.types import Message
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class FileHandler:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot
        self.file_path = None

    def handle_document(self, message: Message) -> bool:
        """
        Обрабатывает полученный документ.
        :param message: Сообщение с документом от пользователя.
        :return: True, если файл является Excel-файлом, иначе False.
        """
        if message.document:
            file_info = self.bot.get_file(message.document.file_id)
            file_extension = os.path.splitext(file_info.file_path)[1].lower()

            if file_extension in ['.xls', '.xlsx']:
                try:
                    # Проверка и создание директории, если она не существует
                    download_dir = 'downloads'
                    if not os.path.exists(download_dir):
                        os.makedirs(download_dir)

                    downloaded_file = self.bot.download_file(file_info.file_path)
                    self.file_path = os.path.join(download_dir, message.document.file_name)
                    with open(self.file_path, 'wb') as new_file:
                        new_file.write(downloaded_file)

                    # Проверка, что файл действительно является Excel-файлом
                    pd.read_excel(self.file_path)
                    logging.info(f"Файл успешно сохранен: {self.file_path}")
                    return True
                except Exception as e:
                    logging.error(f"Ошибка при сохранении файла: {e}")
                    return False
            else:
                logging.warning(f"Получен файл с недопустимым расширением: {file_extension}")
                return False
        else:
            logging.warning("Получено сообщение без документа.")
            return False
