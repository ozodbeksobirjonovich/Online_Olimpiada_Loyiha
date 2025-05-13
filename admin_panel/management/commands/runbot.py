from django.core.management import BaseCommand
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from admin_panel.handlers.router import r

bot = Bot(token="6627232169:AAFuMMuHrmtReVeQHzVeTNxN8VTnedE3BrY", default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

async def on_startup(_):
    print("Bot ishga tushdi!")


class Command(BaseCommand):
    def handle(self, *args, **options):
        async def main():
            await bot.delete_webhook(drop_pending_updates=True)
            dp.include_router(r)
            await dp.start_polling(bot)

        asyncio.run(main())