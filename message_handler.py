import telebot
import logging
from document_handler import DocumentHandler
from keyboard import Keyboard
from document_sender import DocumentSender
from file_handler import FileHandler
import os
from excel_comparer import ExcelComparer


class MessageHandler:
    def __init__(self, bot: telebot.TeleBot, document_sender: DocumentSender, file_handler: FileHandler,
                 document_handler: DocumentHandler):
        self.file1 = None
        self.file2 = None
        self.bot = bot
        self.document_sender = document_sender
        self.file_handler = file_handler
        self.document_handler = document_handler
        self.setup_handlers()
        self.user_states = {}

    def setup_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_message)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['кадровые заявления', 'персонал'])(
            self.handle_personnel)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['отпуск'])(self.handle_leave)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['увольнение'])(self.handle_termination)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['назад'])(self.handle_back)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['иное'])(self.handle_other)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление на отпуск за свой счет'])(
            self.handle_leave_without_pay)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['материальная помощь к отпуску'])(
            self.handle_material_assistance)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление о переносе отпуска'])(
            self.handle_leave_transfer)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление на увольнение'])(
            self.handle_resignation)
        self.bot.message_handler(func=lambda message: message.text.lower() in ['заявление на отзыв увольнения'])(
            self.handle_withdrawal)
        self.bot.message_handler(func=lambda message: message.text.lower() == 'сравнить xlsx')(self.request_first_file)
        self.bot.message_handler(content_types=['document'])(self.handle_document)
        self.bot.message_handler(func=self.is_pdf_conversion)(self.handle_pdf_conversion)
        self.bot.message_handler(func=self.is_pdf_to_word)(self.convert_pdf_to_word)
        self.bot.message_handler(func=self.is_pdf_to_excel)(self.convert_pdf_to_excel)
        self.bot.message_handler(func=self.is_split_pdf)(self.handle_split_pdf)
        self.bot.message_handler(func=lambda message: True)(self.handle_unknown)

    def is_pdf_conversion(self, message):
        return message.text.lower() == 'конвертация pdf'

    def is_pdf_to_word(self, message):
        return message.text.lower() == 'pdf в word'

    def is_pdf_to_excel(self, message):
        return message.text.lower() == 'pdf в excel'

    def is_split_pdf(self, message):
        return message.text.lower() == 'разделить pdf'

    def start_message(self, message):
        try:
            self.bot.send_message(
                message.chat.id,
                "Добро пожаловать! Выберите действие.",
                reply_markup=Keyboard.MAIN_KEYBOARD
            )
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
            self.bot.send_message(message.chat.id, 'Выберите тип заявления:',
                                  reply_markup=Keyboard.TERMINATION_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке 'увольнение': {e}")

    def handle_back(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите раздел:', reply_markup=Keyboard.MAIN_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке 'назад': {e}")

    def handle_other(self, message):
        try:
            self.bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=Keyboard.OTHER_KEYBOARD)
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

    def handle_pdf_conversion(self, message):
        try:
            self.bot.send_message(
                message.chat.id,
                "Пожалуйста, отправьте PDF файл для конвертации.",
                reply_markup=Keyboard.PDF_CONVERSION_KEYBOARD
            )
        except Exception as e:
            logging.error(f"Ошибка при обработке 'конвертация pdf': {e}")

    def convert_pdf_to_word(self, message):
        try:
            logging.info(f"Конвертация PDF в Word для пользователя {message.from_user.id}")
            output_filename = 'temp_file.docx'

            # Добавьте логирование текущей директории
            logging.debug(f"Текущая директория: {os.getcwd()}")

            # Предположим, что метод конвертации создает файл
            self.document_handler.convert_pdf_to_word(message.chat.id, output_filename)

            # Проверка существования файла
            if os.path.exists(output_filename):
                self.bot.send_message(message.chat.id, "PDF успешно конвертирован в Word.")
                try:
                    with open(output_filename, 'rb') as doc:
                        self.bot.send_document(message.chat.id, doc)
                    logging.info(f"Документ '{output_filename}' успешно отправлен в чат {message.chat.id}")
                except Exception as e:
                    logging.error(f"Ошибка при отправке документа '{output_filename}': {e}")
                    self.bot.send_message(message.chat.id, "Произошла ошибка при отправке документа.")
            else:
                logging.error("Файл не найден после конвертации.")
                self.bot.send_message(message.chat.id, "Конвертация завершена, но файл не найден.")
        except Exception as e:
            logging.error(f"Ошибка при конвертации PDF в Word: {e}")
            self.bot.send_message(message.chat.id, "Произошла ошибка при конвертации в Word.")

    def convert_pdf_to_excel(self, message):
        try:
            logging.info(f"Конвертация PDF в Excel для пользователя {message.from_user.id}")
            self.document_handler.convert_pdf_to_excel(message.chat.id, 'temp_file')
            self.bot.send_message(message.chat.id, "PDF успешно конвертирован в Excel.")
        except Exception as e:
            logging.error(f"Ошибка при конвертации PDF в Excel: {e}")
            self.bot.send_message(message.chat.id, "Произошла ошибка при конвертации в Excel.")

    def handle_split_pdf(self, message):
        try:

            self.document_handler.split_pdf(message.from_user.id)
            self.bot.send_message(message.chat.id, "PDF успешно разделен.")
        except Exception as e:
            logging.error(f"Ошибка при обработке команды 'разделить PDF': {e}")
            self.bot.send_message(message.chat.id, "Произошла ошибка при обработке команды.")

    def handle_unknown(self, message):
        try:
            self.bot.send_message(message.chat.id, '', reply_markup=Keyboard.MAIN_KEYBOARD)
        except Exception as e:
            logging.error(f"Ошибка при обработке неизвестной команды: {e}")

    def handle_document(self, message):
        state = self.user_states.get(message.chat.id)
        logging.info(f"Handling document for user {message.chat.id} with state {state}")

        if state == 'waiting_for_first_file':
            self.file1 = message.document.file_id
            self.user_states[message.chat.id] = 'waiting_for_second_file'
            self.bot.send_message(message.chat.id, "Первый файл получен. Теперь отправьте второй файл Excel.")
            logging.info(f"First file received from user {message.chat.id}")

        elif state == 'waiting_for_second_file':
            self.file2 = message.document.file_id
            self.bot.send_message(message.chat.id, "Второй файл получен. Пожалуйста, подождите, пока я сравню файлы.")
            logging.info(f"Second file received from user {message.chat.id}")
            self.compare_files(message)

    def request_first_file(self, message):
        logging.info(f"Requesting first file from user {message.chat.id}")
        self.user_states[message.chat.id] = 'waiting_for_first_file'
        self.bot.send_message(message.chat.id, "Пожалуйста, отправьте первый файл Excel.")

    def compare_files(self, message):
        logging.info(f"Comparing files for user {message.chat.id}")

        file_info1 = self.bot.get_file(self.file1)
        file_info2 = self.bot.get_file(self.file2)

        downloaded_file1 = self.bot.download_file(file_info1.file_path)
        downloaded_file2 = self.bot.download_file(file_info2.file_path)

        with open('file1.xlsx', 'wb') as f1:
            f1.write(downloaded_file1)

        with open('file2.xlsx', 'wb') as f2:
            f2.write(downloaded_file2)

        comparer = ExcelComparer('file1.xlsx', 'file2.xlsx')
        comparer.compare()
        comparer.save_results()

        with open('results.xlsx', 'rb') as doc:
            self.bot.send_document(message.chat.id, doc)
            logging.info(f"Comparison results sent to user {message.chat.id}")

        self.user_states[message.chat.id] = None