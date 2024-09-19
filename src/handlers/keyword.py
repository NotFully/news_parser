from . import *


router = Router()


class KeywordsState(StatesGroup):
    for_keyboard_menu = State()

    to_start_change_keyword = State()

    to_set_keyword_name = State()


kwds_help = '''
Слова-рубрики, которые отлично работают по сайтам(писать 
также!): политика, бизнес, экономика, мнения, технологии, 
медиа, финансы, свое дело, в мире, общество, происшествия, 
армия, наука, спорт, культура, религия, туризм, семья, авто, 
стиль, криптовалюты

Также, работает и поиск по ключевым словам сайтов через их
встроенные поиски, например, по слову москва или Путин 
некоторые сайты дают внятные ответы.
У сайта finam.ru работает только ключевое слово "криптовалюты", 
т.к не имеет поиска

Телеграм-каналы парсятся по последнему посту с проверкой ключевого слова.
Допустима ошибка написания как с заглавной, так и с маленькой буквы.
Например, чтобы поймать пост про Госуслуги, можно попробовать установить
несколько слов: Госуслуги, Госуслуг
'''

@router.message(F.text == 'Ключевые слова')
async def keywords(message: types.Message, state: FSMContext):
    await state.clear()

    await state.set_state(KeywordsState.for_keyboard_menu)
    await message.answer(
        text='🔑 Для настройки ключевых слов сначала выберите любой ваш канал:',
        reply_markup=my_channels()
    )


@router.callback_query(F.data.startswith('channel:'), KeywordsState.for_keyboard_menu)
async def _get_one_my_channel(call: types.CallbackQuery, state: FSMContext):
    # await call.message.delete()

    channel_id = int(call.data.split(":")[1])
    channel_name = Channel().get_channel_name_by_id(channel_id=int(call.data.split(":")[1]))

    await call.message.edit_text(
        text=f'Вы выбрали канал {channel_name}',
        reply_markup=under_channel(channel_id=channel_id)
    )


@router.callback_query(F.data.startswith('words_for'), KeywordsState.for_keyboard_menu)
async def keywords_setting(call: types.CallbackQuery, state: FSMContext):
    # await call.message.delete()

    channel_id = int(call.data.split(":")[1])
    channel_name = Channel().get_channel_name_by_id(channel_id=int(call.data.split(":")[1]))

    await state.update_data(channel_id=call.data.split(":")[1])
    await state.update_data(channel_name=channel_name)

    await call.message.edit_text(
        text=f'''
🔑 Ключевые слова канала "{channel_name}" представлены в клавиатуре под сообщением.
{kwds_help}
Для добавления нажмите /set_keyword''',
        reply_markup=get_my_keyword_under_channel(channel_id=channel_id))


@router.callback_query(F.data.startswith('keyword:'), KeywordsState.for_keyboard_menu)
async def see_keyboard_by_channel(call: types.CallbackQuery, state: FSMContext):
    # await call.message.delete()

    now_keyword_id = int(call.data.split(":")[1])
    # типо id старого ключевого слова - это копия id текущего
    await state.update_data(old_keyword_id=now_keyword_id)

    full_data = await state.get_data()
    channel_name = full_data['channel_name']
    keyword_name = Keyword().get_keyword_name_by_id(keyword_id=int(call.data.split(":")[1]))

    await call.message.edit_text(
        text=f'Вы выбрали ключевое слово "{keyword_name}" для канала "{channel_name}"',
        reply_markup=get_under_keyboard_kb(keyword_id=now_keyword_id)
    )


#------------------------------------------------------------------------------------------------
# Удаление ключевого слова
@router.callback_query(F.data.startswith('remove_keyword'), KeywordsState.for_keyboard_menu)
async def remove_keyword(call: types.CallbackQuery, state: FSMContext):
    # await call.message.delete()

    full_data = await state.get_data()
    channel_name = full_data['channel_name']
    channel_id = full_data['channel_id']
    keyword_id = call.data.split(":")[1]

    Keyword().remove_keyword_by_channel(channel_id=channel_id, keyword_id=int(keyword_id))
    await call.message.edit_text(
        text=f'''
🔑 Ключевые слова канала "{channel_name}" представлены в клавиатуре под сообщением.
{kwds_help}
Для добавления нажмите /set_keyword''',
        reply_markup=get_my_keyword_under_channel(channel_id=channel_id))



#-------------------------------------------------------------------------------------------------
# Замена ключевого слова. Изменяется по id старого слова
@router.callback_query(F.data.startswith('change_keyword'), KeywordsState.for_keyboard_menu)
async def start_change_keyword(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    await call.message.answer(
        text='Для изменения ключевого слова, введите новое 👇'
    )
    await state.set_state(KeywordsState.to_start_change_keyword)


@router.message(F.text, KeywordsState.to_start_change_keyword)
async def get_new_keyword_name(message: types.Message, state: FSMContext):
    keyword_name=message.text

    full_data = await state.get_data()
    old_keyword_id = full_data['old_keyword_id']
    Keyword().change_keyword_by_channel(channel_id=full_data['channel_id'], old_keyword_id=old_keyword_id, new_keyword=keyword_name)

    await message.answer(
        text=f'☑ Успешно изменено на {keyword_name}')

    await message.answer(
        text=f'''
🔑 Ключевые слова канала "{full_data['channel_name']}" представлены в клавиатуре под сообщением.
{kwds_help}
Для добавления нажмите /set_keyword''',
        reply_markup=get_my_keyword_under_channel(channel_id=full_data['channel_id']))

    await state.set_state(KeywordsState.for_keyboard_menu)
#-------------------------------------------------------------------------------------------------
# Добавления нового ключевого слова
@router.message(Command('set_keyword'))
async def set_new_keyword(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()

        for_channel = data['channel_name']

        await state.set_state(KeywordsState.to_set_keyword_name)
        await message.answer(
            text=f'Введите ваше ключевое слово для канала {for_channel} 👇'
        )
    except KeyError:
        await message.answer(text='🛑 Ошибка: канал для слова не был определен, попробуйте начать с кнопки Ключевые слова')


@router.message(F.text, KeywordsState.to_set_keyword_name)
async def get_new_keyword_name(message: types.Message, state: FSMContext):
    await state.update_data(keyword_name=message.text)

    full_data = await state.get_data()
    # print(f'Установка нового ключа: full_data={full_data}')
    Keyword().add_keyword_by_channel(
        channel_id=full_data['channel_id'],
        keyword=full_data['keyword_name']
    )
    await message.answer(
        text='✔ Ключевое слово успешно добавлено')

    await message.answer(
        text=f'''
🔑 Ключевые слова канала "{full_data['channel_name']}" представлены в клавиатуре под сообщением.
{kwds_help}
Для добавления нажмите /set_keyword''',
        reply_markup=get_my_keyword_under_channel(channel_id=full_data['channel_id']))

    await state.set_state(KeywordsState.for_keyboard_menu)
