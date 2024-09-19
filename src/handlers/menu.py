from . import *

from kb.keyboard import kb_menu

router = Router()


@router.message(Command('menu'))
async def menu(message: types.Message):
    await message.answer(
        text='Вы в меню. Выберите действие:',
        reply_markup=kb_menu
    )

