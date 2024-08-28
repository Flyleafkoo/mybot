import telebot
from keyboard import Keyboard
from document_sender import DocumentSender
import logging

class MessageHandler:
    def __init__(self, bot: telebot.TeleBot, document_sender: DocumentSender):
        self.bot = bot
        self.document_sender = document_sender
        self.setup_handlers()

    def setup_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_message)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['кадровые заявления', 'персонал'])(self.handle_personnel)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['отпуск'])(self.handle_leave)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['увольнение'])(self.handle_termination)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['назад'])(self.handle_back)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['иное'])(self.handle_other)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление на отпуск за свой счет'])(self.handle_leave_without_pay)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['материальная помощь к отпуску'])(self.handle_material_assistance)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление о переносе отпуска'])(self.handle_leave_transfer)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление на увольнение'])(self.handle_resignation)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление на отзыв увольнения'])(self.handle_withdrawal)
        self.bot.message_handler(func=lambda message: True)(self.handle_unknown)

    def start_message(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите раздел:', reply_markup=Keyboard.MAIN_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке команды /start: {e}")

    def handle_personnel(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите подраздел:', reply_markup=Keyboard.PERSONNEL_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке 'кадровые заявления': {e}")

    def handle_leave(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите тип заявления:', reply_markup=Keyboard.LEAVE_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке 'отпуск': {e}")

    def handle_termination(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите тип заявления:', reply_markup=Keyboard.TERMINATION_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке 'увольнение': {e}")

    def handle_back(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите раздел:', reply_markup=Keyboard.MAIN_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке 'назад': {e}")

    def handle_other(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Вы выбрали Иное.')
        except Exception as e:
            logging.error(f"Ошибка при обработке 'иное': {e}")

    def handle_leave_without_pay(self, message):
        try:
            self.document_sender.send_document(message.chat.id, 'Заявление на отпуск за свой счет.docx')
            self.bot.send_message(message.chat.id, 'Вы выбрали Заявление на отпуск за свой счет.')
        except Exception as e:
            logging.error(f"Ошибка при обработке 'заявление на отпуск за свой счет': {e}")

    def handle_material_assistance(self, message):
        try:
            self.document_sender.send_document(message.chat.id, 'Материальная помощь к отпуску.docx')
            self.bot.send_message(message.chat.id, 'Вы выбрали Материальную помощь к отпуску.')
        except Exception as e:
            logging.error(f"Ошибка при обработке 'материальная помощь к отпуску': {e}")

    def handle_leave_transfer(self, message):
        try:
            self.document_sender.send_document(message.chat.id, 'Заявление о переносе отпуска.docx')
            self.bot.send_message(message.chat.id, 'Вы выбрали Заявление о переносе отпуска.')
        except Exception as e:
            logging.error(f"Ошибка при обработке 'заявление о переносе отпуска': {e}")

    def handle_resignation(self, message):
        try:
            self.document_sender.send_document(message.chat.id, 'Заявление на увольнение.docx')
            self.bot.send_message(message.chat.id, 'Вы выбрали Заявление на увольнение.')
        except Exception as e:
            logging.error(f"Ошибка при обработке 'заявление на увольнение': {e}")

    def handle_withdrawal(self, message):
        try:
            self.document_sender.send_document(message.chat.id, 'Заявление на отзыв заявления об увольнении.docx')
            self.bot.send_message(message.chat.id, 'Вы выбрали Заявление на отзыв увольнения.')
        except Exception as e:
            logging.error(f"Ошибка при обработке 'заявление на отзыв увольнения': {e}")

    def handle_unknown(self, message):
        try:
            self.bot.send_message()
        except Exception as e:
            logging.error(f"Ошибка при обработке неизвестной команды: {e}")