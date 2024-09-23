import os, io
import logging
from io import BytesIO
import pandas as pd
from PDFConverter import PDFConverter
from PDF_Splitter import PDFSplitter
from keyboard import Keyboard

excel_files = []

class DocumentHandler:
    def __init__(self, bot, file_handler, employee_database):
        self.bot = bot
        self.file_handler = file_handler
        self.employee_database = employee_database
        self.converter = PDFConverter()

    def handle_pdf(self, message):
        try:
            file_info = self.bot.get_file(message.document.file_id)
            file_path = file_info.file_path
            downloaded_file = self.bot.download_file(file_path)

            # Создаем объект BytesIO из загруженных данных
            with BytesIO(downloaded_file) as file_stream:
                with open('temp_file.pdf', 'wb') as new_file:
                    new_file.write(file_stream.read())

            logging.info("Файл успешно загружен.")
        except Exception as e:
            logging.error(f"Ошибка при загрузке файла: {e}")

            self.bot.send_message(
                message.chat.id,
                "Выберите формат для конвертации:",
                reply_markup=Keyboard.PDF_CONVERSION_KEYBOARD
            )

        except Exception as e:
            logging.error(f"Ошибка при обработке PDF документа: {e}")

    def convert_pdf_to_word(self, chat_id, *args):
        try:
            pdf_path = 'temp_file.pdf'
            word_path = 'converted_file.docx'

            # Проверка существования исходного PDF файла
            if not os.path.exists(pdf_path):
                logging.error(f"Исходный файл '{pdf_path}' не найден.")
                self.bot.send_message(chat_id, "Исходный файл не найден.")
                return

            logging.info(f"Начало конвертации PDF '{pdf_path}' в Word.")

            # Конвертация PDF в Word
            self.converter.pdf_to_word(pdf_path, word_path)

            # Отправка файла
            with open(word_path, 'rb') as doc_file:
                self.bot.send_document(chat_id, doc_file)
            logging.info("PDF успешно конвертирован в Word и отправлен.")

            # Удаление временного файла
            os.remove(word_path)

        except Exception as e:
            logging.error(f"Ошибка при конвертации PDF в Word: {e}")
            self.bot.send_message(chat_id, "Произошла ошибка при конвертации в Word.")

    def convert_pdf_to_excel(self, chat_id, *args):
        try:
            excel_path = 'converted_file.xlsx'
            # Убедитесь, что метод pdf_to_excel вызывается с двумя аргументами
            self.converter.pdf_to_excel('temp_file.pdf', excel_path)
            with open(excel_path, 'rb') as excel_file:
                self.bot.send_document(chat_id, excel_file)
            logging.info("PDF успешно конвертирован в Excel и отправлен.")
            os.remove(excel_path)
        except Exception as e:
            logging.error(f"Ошибка при конвертации PDF в Excel: {e}")

    def split_pdf(self, chat_id):
        try:
            pdf_path = 'temp_file.pdf'
            output_folder = f"output_{chat_id}"

            # Создание объекта PDFSplitter и вызов метода split_pdf
            splitter = PDFSplitter(pdf_path, output_folder)
            splitter.split_pdf()

            # Отправка каждой страницы пользователю
            for filename in os.listdir(output_folder):
                page_path = os.path.join(output_folder, filename)
                with open(page_path, 'rb') as page_file:
                    self.bot.send_document(chat_id, page_file)

            # Удаление временных файлов
            for filename in os.listdir(output_folder):
                os.remove(os.path.join(output_folder, filename))
            os.rmdir(output_folder)

        except Exception as e:
            logging.error(f"Ошибка при разделении PDF: {e}")
            self.bot.send_message(chat_id, "Произошла ошибка при разделении PDF.")

