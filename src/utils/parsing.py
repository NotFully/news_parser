import re
import aiogram
from aiogram import F, types
import asyncio
from pydantic import BaseModel


from kb.inline import get_under_news_keyboard
from utils.db.keywords import Keyword
from utils.db.my_channels import Channel
from utils.db.news import News
from utils.db.user import User

from utils.parsers.rbc import rbc # отлично работает
from utils.parsers.yahoo import yahoo # отлично работает
# from utils.parsers.bbc import bbc # не парсится
from utils.parsers.ria import ria # отлично работает
from utils.parsers.forbes import forbes # отлично работает
from utils.parsers.gazeta import gazeta # отлично работает
from utils.parsers.finam import finam # нету глобального поиска, будет искать только новости по слову "криптовалюты"
from utils.parsers.kommersant import kommersant # отлично работает
from utils.parsers.lenta import lenta # отлично работает
from utils.parsers.mk import mk # отлично работает

# from utils.parsers.telethon_parser import telethon
from utils.parsers.telegram import telegram


class ResultItem(BaseModel):
    title: str
    keyword: str
    channel: str
    url: str


async def send(
        bot: aiogram.Bot,
        user_id: list,
        title: str,
        keyword: str,
        channel: str,
        link: str,
        new_id: int):
    for user in user_id:
        await bot.send_message(
            chat_id=user,
            text=f'''
🔔 Уведомление от парсера:
Новость:
"{title}" 
Ссылка: {link} 


Ключевое слово <code>{keyword}</code> 
Для канала <code>{channel}</code> 
    ''',
            disable_web_page_preview=False,
            parse_mode='HTML',
            reply_markup=get_under_news_keyboard(news_id=new_id),
            disable_notification=True
            )


async def publication_news(
        bot: aiogram.Bot,
        user_id: int,
        news_id: int,
    ):
    get_news = News().get_news(news_id=news_id)
    channel_name = getattr(get_news, 'for_channel')
    channel_id = Channel().get_channel_url_by_name(channel_name)
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


class SourceCollector:
    """
    Собирает новости по ключевому слову по всем источникам
    """
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

    async def collect(self, keyword: str, channel: str) -> list[ResultItem]:
        return [
            *await telegram(keyword=keyword, channel=channel),
            await rbc(keyword=keyword, channel=channel),
            await yahoo(keyword=keyword, channel=channel),
            await ria(keyword=keyword, channel=channel),
            await forbes(keyword=keyword, channel=channel),
            await gazeta(keyword=keyword, channel=channel),
            await finam(keyword=keyword, channel=channel),
            await kommersant(keyword=keyword, channel=channel),
            await lenta(keyword=keyword, channel=channel),
            await mk(keyword=keyword, channel=channel)
        ]


async def async_generator(data):
    for item in data:
        await asyncio.sleep(0.05)
        yield item


class Parser:
    def __init__(self, bot: aiogram.Bot, dp: aiogram.Dispatcher):
        self.bot = bot
        self.dp = dp

    async def start(self):
        await self.channel_loop()

    async def channel_loop(self):
        my_channels = Channel().get_channels()

        async for i in async_generator(my_channels):
            # пробегаемся по каналам
            channel_id = i['id']
            channel_name = i['name']

            print(f'\n-----------------{channel_name}---------------')
            channel_keywords = Keyword().get_keywords_by_channel_id(channel_id)

            # определяем сборщик новостей для одного текущего канал
            source_collector = SourceCollector(self.bot, self.dp)
            async for k in async_generator(channel_keywords):
                print(f'--------{k["name"]}-------')

                # @self.dp.callback_query(F.data.startswith('yes_news:'))
                # async def get_confirmed_news(call: types.CallbackQuery):
                #     """
                #     Ловим callback-подтверждение прямо в цикле. Если что, есть ещё и похожий в handlers/news.py
                #     """
                #
                #     await call.message.delete()
                #
                #     news = News().get_news(int(call.data.split(':')[1]))
                #     await publication_news(bot=self.bot, user_id=User().get_first_trusted_user(), news_id=getattr(news, 'news_id'))

                keyword_result_by_all_sources = await source_collector.collect(k['name'], channel=channel_name)
                print(f'Результаты: {keyword_result_by_all_sources}')

                if keyword_result_by_all_sources:
                    async for news_item in async_generator(keyword_result_by_all_sources):
                        try:
                            News().add_news(
                                title=news_item.title,
                                link=news_item.url,
                                keyword=news_item.keyword,
                                for_channel=news_item.channel
                            )

                            new_news_id = News().get_last_news_id()
                            await send(
                                bot=self.bot,
                                user_id=User().get_first_trusted_user(),
                                title=news_item.title,
                                keyword=news_item.keyword,
                                channel=news_item.channel,
                                link=news_item.url,
                                new_id=new_news_id # передаем id новости, чтобы потом искать по БД
                            )
                            print('sended')

                        except AttributeError:
                            continue

        print('parsing ended')


