import telebot

class Keyboard:
    MAIN_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    MAIN_KEYBOARD.add(
        telebot.types.KeyboardButton('Кадровые заявления'),
        telebot.types.KeyboardButton('Иное')
    )

    PERSONNEL_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    PERSONNEL_KEYBOARD.add(
        telebot.types.KeyboardButton('Отпуск'),
        telebot.types.KeyboardButton('Увольнение'),
        telebot.types.KeyboardButton('Назад')
    )

    LEAVE_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    LEAVE_KEYBOARD.add(
        telebot.types.KeyboardButton('Заявление на отпуск за свой счет'),
        telebot.types.KeyboardButton('Материальная помощь к отпуску'),
        telebot.types.KeyboardButton('Заявление о переносе отпуска'),
        telebot.types.KeyboardButton('Назад')
    )

    TERMINATION_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    TERMINATION_KEYBOARD.add(
        telebot.types.KeyboardButton('Заявление на увольнение'),
        telebot.types.KeyboardButton('Заявление на отзыв увольнения'),
        telebot.types.KeyboardButton('Назад')
    )

    OTHER_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    OTHER_KEYBOARD.add(
        telebot.types.KeyboardButton('Конвертация PDF'),
        telebot.types.KeyboardButton('Назад'),
    )

    PDF_CONVERSION_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    PDF_CONVERSION_KEYBOARD.add(
        telebot.types.KeyboardButton('PDF в Word'),
        telebot.types.KeyboardButton('PDF в Excel'),
        telebot.types.KeyboardButton('Разделить PDF'),
        telebot.types.KeyboardButton('Назад')
    )