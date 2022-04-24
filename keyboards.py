from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_yes = InlineKeyboardButton(text="Приступим", callback_data="data_yes")
start_no = InlineKeyboardButton(text="Нет", callback_data="data_no")
startMenu = InlineKeyboardMarkup().add(start_yes, start_no)
