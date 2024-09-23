import pandas as pd
import logging


class ExcelComparer:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
        self.df1 = pd.read_excel(file1)
        self.df2 = pd.read_excel(file2)
        self.results = pd.DataFrame()

    def preprocess_column(self, column):
        # Преобразует текст в нижний регистр и удаляет все разделители
        return column.str.lower().str.replace(r'\s+', '', regex=True)

    def compare(self):
        logging.info("Начало сравнения данных.")
        df1_column = self.df1[self.df1.columns[0]]
        df2_column = self.df2[self.df2.columns[0]]

        # Преобразование столбцов
        self.df1[self.df1.columns[0]] = self.preprocess_column(df1_column)
        self.df2[self.df2.columns[0]] = self.preprocess_column(df2_column)

        # Создаем результат с оригинальными данными
        self.results[self.df1.columns[0]] = df1_column

        for index, row in self.df1.iterrows():
            name = row[self.df1.columns[0]]
            matching_row = self.df2[self.df2[self.df2.columns[0]] == name]

            if not matching_row.empty:
                logging.info(f"Обработка данных для: {name}")
                for col in self.df1.columns[1:]:
                    if col in self.df2.columns:
                        value1 = pd.to_numeric(row[col], errors='coerce')
                        value2 = pd.to_numeric(matching_row.iloc[0][col], errors='coerce')
                        self.results.at[index, col] = (value1 - value2) if pd.notna(value1) and pd.notna(
                            value2) else None
            else:
                logging.warning(f"Нет соответствия для: {name}")

    def save_results(self, output_file='results.xlsx'):
        self.results.to_excel(output_file, index=False)
        logging.info(f"Результаты успешно записаны в '{output_file}'.")
