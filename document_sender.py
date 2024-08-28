import telebot
import os
import logging

# Настройка логирования
logging.basicConfig(filename='bot_errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentSender:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def send_document(self, chat_id: int, filename: str):
        file_path = os.path.join(os.getcwd(), filename)
        try:
            with open(file_path, 'rb') as doc:
                self.bot.send_document(chat_id, doc)
        except Exception as e:
            logging.error(f"Ошибка при отправке документа '{filename}': {e}")