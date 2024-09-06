import os
from PyPDF2 import PdfReader, PdfWriter
from keyboard import Keyboard

class PDFSplitter:
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder

    def split_pdf(self):
        # Чтение PDF файла
        reader = PdfReader(self.input_file)
        num_pages = len(reader.pages)

        # Создание выходной папки, если она не существует
        os.makedirs(self.output_folder, exist_ok=True)

        # Разделение PDF на страницы
        for i in range(num_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            output_file_path = os.path.join(self.output_folder, f"page_{i + 1}.pdf")
            with open(output_file_path, 'wb') as output_file:
                writer.write(output_file)