from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_hi = KeyboardButton('Хай')

greet_kb = ReplyKeyboardMarkup()
greet_kb.add(button_hi)