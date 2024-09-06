import sqlite3
import pandas as pd
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class EmployeeDatabase:
    def __init__(self, db_name='employees.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()
        logging.info(f"Connected to database: {db_name}")

    def create_table(self):
        logging.info("Creating table 'employees' if it does not exist")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ФИО TEXT,
                Дата TEXT,
                Должность TEXT
            )
        ''')
        self.conn.commit()
        logging.info("Table 'employees' created or already exists")

    def load_from_excel(self, file_path):
        try:
            logging.info(f"Loading data from Excel file: {file_path}")
            df = pd.read_excel(file_path)
            logging.info(f"Columns in Excel file: {df.columns}")

            expected_columns = ['ФИО', 'Дата', 'Должность']
            if not all(column in df.columns for column in expected_columns):
                raise ValueError(f"Excel file must contain columns: {expected_columns}")

            # Проверка типов данных
            if not pd.api.types.is_string_dtype(df['ФИО']):
                raise TypeError("Column 'ФИО' must be of string type")
            if not pd.api.types.is_datetime64_any_dtype(df['Дата']):
                raise TypeError("Column 'Дата' must be of datetime type")
            if not pd.api.types.is_string_dtype(df['Должность']):
                raise TypeError("Column 'Должность' must be of string type")

            data = df[expected_columns].values.tolist()
            logging.info(f"Data to be inserted: {data}")

            if not data:
                logging.warning("No data to insert from Excel file.")
                return

            self.cursor.executemany('''
                INSERT INTO employees (ФИО, Дата, Должность) VALUES (?, ?, ?)
            ''', data)
            self.conn.commit()
            logging.info(f"Data loaded from Excel file: {file_path}")
        except Exception as e:
            logging.error(f"Error loading data from Excel file: {e}")

    def close(self):
        self.conn.close()
        logging.info("Database connection closed")

    def update_database(self, file_path, mode='replace'):
        try:
            if mode == 'replace':
                logging.info("Deleting existing data in 'employees' table")
                self.cursor.execute('DELETE FROM employees')
                self.conn.commit()
                logging.info("Existing data in 'employees' table deleted")
            elif mode == 'append':
                logging.info("Appending new data to 'employees' table")
            else:
                raise ValueError("Invalid mode. Use 'replace' or 'append'.")

            self.load_from_excel(file_path)
            logging.info(f"Database updated with data from Excel file: {file_path}")
        except Exception as e:
            logging.error(f"Error updating database from Excel file: {e}")

    def get_birthdays_today(self):
        today = datetime.now().strftime('%m-%d')
        logging.info(f"Fetching birthdays for today: {today}")
        self.cursor.execute("SELECT ФИО FROM employees WHERE strftime('%m-%d', Дата) = ?", (today,))
        birthdays = self.cursor.fetchall()
        return [birthday[0] for birthday in birthdays]

    def print_all_employees(self):
        logging.info("Fetching all employees from the database")
        self.cursor.execute("SELECT * FROM employees")
        rows = self.cursor.fetchall()
        if not rows:
            logging.info("No employees found in the database.")
        else:
            for row in rows:
                logging.info(f"Employee: {row}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
