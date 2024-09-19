from . import State, StatesGroup, FSMContext, types, Command, Router, F
from utils.db.user import User

from kb.keyboard import kb_menu
router = Router()


class Registation(StatesGroup):
    to_api_id = State()
    api_hash = State()


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await message.answer(f'''
Привет, {message.from_user.first_name}! 🖐

Я закрытый бот-парсер новостей из разных источников для твоих Telegran-каналов.

У меня есть два основных отдела: Мои каналы и Ключевые слова.
В "Мои каналы" ты можешь добавлять и удалять каналы, а в "Ключевые слова" ты можешь 🪄 управлять словами
''', reply_markup=kb_menu)


@router.message(Command('password'))
async def password(message: types.Message, state: FSMContext):
    # функция заглушки. Только для того, чтобы поймать пароль
    ...

