import telebot

class Keyboard:
    MAIN_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    MAIN_KEYBOARD.add(telebot.types.KeyboardButton('Кадровые заявления'))
    MAIN_KEYBOARD.add(telebot.types.KeyboardButton('Иное'))

    PERSONNEL_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    PERSONNEL_KEYBOARD.add(telebot.types.KeyboardButton('Отпуск'))
    PERSONNEL_KEYBOARD.add(telebot.types.KeyboardButton('Увольнение'))
    PERSONNEL_KEYBOARD.add(telebot.types.KeyboardButton('Назад'))

    LEAVE_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    LEAVE_KEYBOARD.add(telebot.types.KeyboardButton('Заявление на отпуск за свой счет'))
    LEAVE_KEYBOARD.add(telebot.types.KeyboardButton('Материальная помощь к отпуску'))
    LEAVE_KEYBOARD.add(telebot.types.KeyboardButton('Заявление о переносе отпуска'))
    LEAVE_KEYBOARD.add(telebot.types.KeyboardButton('Назад'))

    TERMINATION_KEYBOARD = telebot.types.ReplyKeyboardMarkup(row_width=2)
    TERMINATION_KEYBOARD.add(telebot.types.KeyboardButton('Заявление на увольнение'))
    TERMINATION_KEYBOARD.add(telebot.types.KeyboardButton('Заявление на отзыв увольнения'))
    TERMINATION_KEYBOARD.add(telebot.types.KeyboardButton('Назад'))