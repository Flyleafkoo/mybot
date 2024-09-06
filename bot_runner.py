import logging
from link_sender import LinkSender
from site_parser import SiteParser
from link_storage import LinkStorage
from document_sender import DocumentSender
from message_handler import MessageHandler
from scheduler import Scheduler, run_scheduler
import telebot
from threading import Thread
import time
from EmployeeDatabase import EmployeeDatabase
from file_handler import FileHandler
from document_handler import DocumentHandler

logging.basicConfig(level=logging.INFO)


class BotRunner:
    def __init__(self, token, group_ids, specific_group_id):
        self.token = token
        self.group_ids = group_ids
        self.specific_group_id = specific_group_id
        self.bot = telebot.TeleBot(token)
        self.document_sender = DocumentSender(self.bot)
        self.file_handler = FileHandler(self.bot)
        self.employee_database = EmployeeDatabase()
        self.document_handler = DocumentHandler(self.bot, self.file_handler, self.employee_database)

        # Передаем `document_handler` в `MessageHandler`
        self.message_handler = MessageHandler(self.bot, self.document_sender, self.file_handler, self.document_handler)

        self.scheduler = Scheduler(token, group_ids, specific_group_id, self.employee_database)
        self.link_storage = LinkStorage()
        self.site_parser = SiteParser('https://www.garant.ru/ia/aggregator/?tag_id=1606', self.link_storage)
        self.link_sender = LinkSender(self.bot, self.link_storage, self.site_parser, self.group_ids)

        # Настройка логирования
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('bot.log')
        console_handler = logging.StreamHandler()
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(file_handler)
        logging.getLogger().addHandler(console_handler)

    def start(self):
        self.message_handler.setup_handlers()
        self.setup_document_handler()
        Thread(target=run_scheduler).start()
        Thread(target=self.link_sender.run_sender).start()

        while True:
            try:
                logging.info("Запуск бота...")
                self.bot.polling(none_stop=True, interval=0)
            except Exception as e:
                logging.error(f"Произошла ошибка: {e}")
                logging.info("Попытка переподключения через 30 секунд...")
                time.sleep(30)

    def setup_document_handler(self):
        @self.bot.message_handler(content_types=['document'])
        def handle_document(message):
            if message.document.mime_type == 'application/pdf':
                self.document_handler.handle_pdf(message)
            else:
                self.document_handler.handle_document(message)
