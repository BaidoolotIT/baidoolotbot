from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMIN

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    cost = State()

async def fsm_start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id in ADMIN:
            await FSMAdmin.photo.set()
            await message.answer(f"салам {message.from_user.full_name}\n"
                                 f"Скинь фотку еды!")
        else:
            await message.answer("ты не мой Босс")
    else:
        await message.reply("пиши в ЛС!")

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("введи название блюда")

async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("опиши блюдо")

async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMAdmin.next()
    await message.answer("Введи цену блюда")

async def load_cost(message: types.Message, state: FSMContext):
    try:
        if int(message.text) > 5000:
            await message.answer("кто за такие цены будет еду покупаать\nнормальную цену скажи")
        elif int(message.text) < 0:
            await message.answer("малсынба?")
        else:
            async with state.proxy() as data:
                data['cost'] = int(message.text)
                await bot.send_photo(message.from_user.id, data['photo'],
                                     caption=f"Name: {data['name']}\n"
                                             f"Description: {data['description']}\n"
                                             f"Cost: {data['cost']}$")
            await state.finish()
            await message.answer("новое блюдо, круто")
    except:
        await message.answer("Вводи числа мал")

async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Регистрация отменена")

def register_handlers_fsmAdminMenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state="*", commands='cancel')
    dp.register_message_handler(fsm_start, commands=['menu'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo, content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_cost, state=FSMAdmin.cost)