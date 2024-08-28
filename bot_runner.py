# bot_runner.py
import logging
from link_sender import LinkSender
from site_parser import SiteParser
from link_storage import LinkStorage
from document_sender import DocumentSender
from message_handler import MessageHandler
from scheduler import Scheduler
import telebot
from threading import Thread
import time


class BotRunner:
    def __init__(self, token, group_ids, specific_group_id):
        self.token = token
        self.group_ids = group_ids
        self.specific_group_id = specific_group_id
        self.bot = telebot.TeleBot(token)
        self.message_handler = MessageHandler(self.bot, DocumentSender(self.bot))
        self.scheduler = Scheduler(token, group_ids, specific_group_id)
        self.link_storage = LinkStorage()
        self.site_parser = SiteParser('https://www.garant.ru/ia/aggregator/?tag_id=1606',
                                      self.link_storage)  # Замените на ваш URL
        self.link_sender = LinkSender(self.bot, self.link_storage, self.site_parser, self.group_ids)

        # Настройка логирования
        logging.basicConfig(level=logging.INFO, filename='bot.log',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def start(self):
        self.message_handler.setup_handlers()  # Убедитесь, что обработчики настроены
        Thread(target=self.scheduler.run_scheduler).start()
        Thread(target=self.link_sender.run_sender).start()

        while True:
            try:
                logging.info("Запуск бота...")
                self.bot.polling(none_stop=True, interval=0)
            except Exception as e:
                logging.error(f"Произошла ошибка: {e}")
                logging.info("Попытка переподключения через 30 секунд...")
                time.sleep(30)  # Ожидание перед повторной попыткой
