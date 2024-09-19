from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup
from aiogram import types


kb1 = [[
	types.KeyboardButton(text='Мои каналы'),
	types.KeyboardButton(text='Ключевые слова'),
]]
kb_menu = ReplyKeyboardMarkup(keyboard=kb1, resize_keyboard=True, input_field_placeholder='Выберите команду')


