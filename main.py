import asyncio
from aiogram.utils import executor
from config import dp
import logging
from handlers import client, callback, fsmAdminMenu, notification, admin, extra, news
from database1.bot_db import sql_create

async def on_startup(_):
    asyncio.create_task(notification.scheduler())
    sql_create()
extra.register_handlers_extra(dp)
fsmAdminMenu.register_handlers_fsmAdminMenu(dp)
client.register_handlers_client(dp)
fsmAdminMenu.register_handlers_fsmAdminMenu(dp)
callback.register_handlers_callback(dp)
admin.register_handlers_admin(dp)
news.register_handlers_news(dp)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)