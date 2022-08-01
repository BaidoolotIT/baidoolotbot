from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMIN
from database import bot_db


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    cost = State()

async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
            await FSMAdmin.photo.set()
            await message.answer(f"Салам {message.from_user.full_name}\n"
                                 f"Скинь фотку еды!")
    else:
        await message.reply("Пиши в ЛС!!!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Введи название блюда...")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Опиши блюдо...")

async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("Введи цену блюда...")

async def load_cost(message: types.Message, state: FSMContext):
    try:
        if float(message.text) > 1000:
            await message.answer("В Кыргызстане никто не купит еду за столько\nУкажи нормальную цену...")
        elif float(message.text) < 0:
            await message.answer("Не тупи и укажи нормальную цену!!!")
        else:
            async with state.proxy() as data:
                data['cost'] = float(message.text)
                await bot.send_photo(message.from_user.id, data['photo'],
                                     caption=f"Name: {data['name']}\n"
                                             f"Description: {data['description']}\n"
                                             f"Cost: {data['cost']}$")
            try:
                await bot_db.sql_command_insert(state)
                await state.finish()
                await message.answer("Спасибо за новое блюдо!!!")
            except:
                await bot.send_message("Извини, но у нас есть еда с таким названием!!!")
    except:
        await message.answer("Вводи числа животное...")

async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Регистрация отменена!")

async def delelete_data(message: types.Message):
    if message.from_user.id in ADMIN and message.chat.type == "private":
        foods = await bot_db.sql_command_all()
        for food in foods:
            await bot.send_photo(message.from_user.id, food[0],
                                 caption=f"Name: {food[1]}\n"
                                         f"Description: {food[2]}\n\n"
                                         f"Cost: {food[3]}\n\n",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"Delete: {food[1]}",
                                         callback_data=f"Delete {food[1]}"
                                     )
                                 )
                                 )
    else:
        await message.reply("Tы не админ!!!")

async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace('Delete ', ''))
    await call.answer(text="Блюдо удалено", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)

def register_handlers_fsmAdminMenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands='cancel')
    dp.register_message_handler(fsm_start, commands=['menu'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_cost, state=FSMAdmin.cost)
    dp.register_message_handler(delelete_data, commands=['del'])
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith('Delete ')
    )