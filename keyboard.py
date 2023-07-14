from aiogram import types

class Keyboard:

    def keyboard_first_step(self):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Негативные комментарии", "Положительные комментарии", "Нейтральные комментарии", "Все", "В начало"]
        keyboard.add(*buttons)

        return keyboard

    def keyboard_second_step(self):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Количество", "Комментарии", "Вернуться"]
        keyboard.add(*buttons)

        return keyboard

    def keyboard_starting(self):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["/start"]
        keyboard.add(*buttons)

        return keyboard

