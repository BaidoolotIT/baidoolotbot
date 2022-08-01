import asyncio
import aioschedule
from aiogram import types, Dispatcher
from config import bot

async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text="OK")

async def cod():
    await bot.send_message(chat_id=chat_id, text="Пора кодить")

async def op():
    photo = open("media/video.mp4", "rb")
    await bot.send_video(chat_id=chat_id, photo=photo, caption="ВАААН ПИИИИИС СУЩЕСТВУЕТ!")

async def scheduler():
    aioschedule.every().day.at("18:00").do(cod)
    aioschedule.every().day.at("22:00").do(op)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)

def register_handler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: 'напомни' in word.text)