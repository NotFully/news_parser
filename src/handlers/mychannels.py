from . import *
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated
from utils.db.user import User

from utils.db.my_channels import Channel

router = Router()


@router.my_chat_member(ChatMemberUpdatedFilter( member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated, bot):
    """
    Ловит событие добавления бота как Админа и заносит этот канал в БД
    """
    # print(event)
    Channel().add_channel(name=event.chat.title, url_id=event.chat.id)
    await bot.send_message(
        chat_id=User().get_first_trusted_user(),
        text=f'''
✅ Поздравляю! 
Я успешно добавлен в канал {event.chat.title} как Администратор. Теперь я могу публиковать там новости.

Список Мои каналы обновлён'''
    )


@router.message(F.text == 'Мои каналы')
async def _my_channels(message: types.Message, state: FSMContext, bot: Bot):
    await state.clear()

    if my_channels() == None:
         await message.answer(
             text='Пока ваших каналов нету :( \nДля получения списка ваших каналов, добавьте меня хотя бы в один канал с правами Администратора',
         )
    else:

        await message.answer(
            text='📢 Здесь расположены ваши каналы, в которых будут публиковаться новости. Для добавления канала - добавьте меня в свой канал с правами Администратора',
            reply_markup=my_channels()
        )


# просмотр канала с клавиатурой только для удаления
@router.callback_query(F.data.startswith('channel:'), StateFilter(None))
async def get_one_my_channel(call: types.CallbackQuery):
    channel_id = int(call.data.split(":")[1])
    channel = Channel().get_channel_name_by_id(channel_id=channel_id)

    await call.message.edit_text(
        text=f'📢 Вы выбрали канал {channel}',
        reply_markup=under_channel_for_my_channels(channel_id=channel_id)
    )


# удаление канала
@router.callback_query(F.data.startswith('remove_channel'))
async def remove_my_channel(call: types.CallbackQuery):
    channel_id = int(call.data.split(":")[1])
    channel = Channel().get_channel_name_by_id(channel_id)

    try:
        Channel().remove_channel(channel_id=channel_id)
        await call.message.delete()
        await call.message.answer(text='☑ Канал успешно удалён.')
        if my_channels() == None:
            await call.message.edit_text(
                text='Пока ваших каналов нету :( \nДля получения списка ваших каналов, добавьте меня хотя бы в один канал с правами Администратора',
            )
        else:

            await call.message.edit_text(
                text='📢 Здесь расположены ваши каналы, в которых будут публиковаться новости. Для добавления канала - добавьте меня в свой канал с правами Администратора',
                reply_markup=my_channels()
            )
    except Exception as e:
        await call.message.answer(text=f'Ошибка при удалении канала - {e}.')


class AddingMyChannel(StatesGroup):
    to_set_name = State()
    to_set_link = State()




