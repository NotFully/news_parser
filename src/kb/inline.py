from aiogram.utils.keyboard import (InlineKeyboardBuilder,
									ReplyKeyboardBuilder,
									ReplyKeyboardMarkup,
									InlineKeyboardMarkup,
									)
from aiogram import types

from utils.db.my_channels import Channel
from utils.db.keywords import Keyword


def my_channels() -> InlineKeyboardMarkup | None:
	builder = InlineKeyboardBuilder()
	for i in Channel().get_channels():
		builder.row(
			types.InlineKeyboardButton(
				text=i['name'],
				callback_data=f'channel:{i["id"]}'))

	if builder != [[]]:
		return builder.as_markup(resize_keyboard=True)
	return None


def under_channel(channel_id: int) -> InlineKeyboardMarkup | None:
	# клава каналов для раздела ключевые слова
	kb1 = [[
		types.InlineKeyboardButton(text='🔑 Настроить ключевые слова', callback_data=f'words_for:{channel_id}')
	]]
	return InlineKeyboardMarkup(inline_keyboard=kb1)


def under_channel_for_my_channels(channel_id: int):
	# клава для меню каналов, в которой можно только удалть
	kb1 = [[
		types.InlineKeyboardButton(text='Удалить канал', callback_data=f'remove_channel:{channel_id}'),
	]]
	return InlineKeyboardMarkup(inline_keyboard=kb1)


def get_my_keyword_under_channel(channel_id: int) -> InlineKeyboardMarkup | None:
	builder = InlineKeyboardBuilder()

	keywords = Keyword().get_keywords_by_channel_id(channel_id=channel_id)
	print(keywords)

	for i in keywords:
		builder.row(
			types.InlineKeyboardButton(
				text=i['name'],
				callback_data=f'keyword:{i["id"]}'))

	return builder.as_markup(resize_keyboard=True)


def get_under_keyboard_kb(keyword_id: int):
	kb1 = [
		[types.InlineKeyboardButton(text='🔧 Изменить ключевое слово', callback_data=f'change_keyword:{keyword_id}')],
		[types.InlineKeyboardButton(text='➖ Удалить ключевое слово', callback_data=f'remove_keyword:{keyword_id}')]
	]
	return InlineKeyboardMarkup(inline_keyboard=kb1)


def get_under_news_keyboard(news_id: int):
	kb1 = [[
		types.InlineKeyboardButton(text='Опубликовать', callback_data=f'yes_news:{news_id}')
	]]
	return InlineKeyboardMarkup(inline_keyboard=kb1)
