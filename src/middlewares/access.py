from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable


from utils.db.user import User


class CheckUserHaveAccess(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        user_id = int(event.from_user.id)
        user = User()

        if user.user_is_trusted(user_id=user_id):
            return await handler(event, data)
        else:
            if event.text != '/start':
                if user.check_password(possible_password=event.text.split(' ')[1]):
                    user.add_user(user_id=user_id, username=event.from_user.username)
                    await event.answer('✅ Вы успешно вошли по паролю! \nПерезапустите бота командой /start')
                else:
                    await event.answer(text='Неправильный пароль! Повторите ввод пароля командой /password <пароль>')
            else:
                await event.answer(text='Неправильный пароль! Повторите ввод пароля командой /password <пароль>')



