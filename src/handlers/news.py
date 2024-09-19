import aiogram
from aiogram.types import CallbackQuery

from . import State, StatesGroup, FSMContext, types, Command, Router, F


from utils.db.user import User
from utils.db.news import News
from utils.db.my_channels import Channel

from kb.inline import get_under_news_keyboard


router = Router()


async def publication_news(
        call: CallbackQuery,
        bot: aiogram.Bot,
        user_id: int,
        news_id: int,
    ):
    get_news = News().get_news(news_id=news_id)
    channel_name = getattr(get_news, 'for_channel')
    channel_id = Channel().get_channel_url_by_name(channel_name)
    # print(channel_id)
    try:
        await bot.send_message(
            chat_id=channel_id,
            text=f'''
{getattr(get_news, 'title')}

Источник: {getattr(get_news, 'link')}
''')

    except aiogram.exceptions.TelegramForbiddenError:
        if User().user_is_trusted(user_id=user_id):
            await bot.send_message(
                chat_id=user_id,
                text=f'ОШИБКА: Новость {getattr(get_news, "title")} не была отправлена, так как бота нету в чате {channel_name}'
            )


@router.callback_query(F.data.startswith('yes_news:'))
async def get_confirmed_news(call: types.CallbackQuery, bot: aiogram.Bot):
    """
    Функция копия той, которая есть в parsing.py.
    Но только эта функция ловит кэлбэки, когда цикл парсинга не активен
    """
    await call.answer('Новость опубликована!')

    # удаляем новость в чате с админом
    try:
        await call.message.delete()
    except aiogram.exceptions.TelegramBadRequest:
        pass

    news = News().get_news(int(call.data.split(':')[1]))
    user_id = call.from_user.id

    # print(news)
    await publication_news(call=call, bot=bot, user_id=user_id, news_id=news.news_id)

