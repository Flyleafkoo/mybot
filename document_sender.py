import telebot
import os
import logging

# Настройка логирования
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentSender:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def send_document(self, chat_id: int, filename: str):
        file_path = os.path.join(os.getcwd(), filename)
        try:
            with open(file_path, 'rb') as doc:
                self.bot.send_document(chat_id, doc)
            logging.info(f"Документ '{filename}' успешно отправлен в чат {chat_id}")
        except Exception as e:
            logging.error(f"Ошибка при отправке документа '{filename}': {e}")
