from aiogram import F
from aiogram.types import Message
from admin_panel.handlers.router import r
from admin_panel.keyboards import *
from admin_panel.models import *
from admin_panel.model_functions import *


@r.message(F.text == "/start")
async def process_start(message: Message):
    if await get_this_user(message.from_user.id):
        await message.answer(f"Assalomu alaykum {message.from_user.full_name}. Shaxsiy kabinetingizga xush kelibsiz!", reply_markup=student_panel)
    else:
        await message.answer("Assalomu alaykum. Men Beruniy Olimpiadasi botiga xush kelibsiz. Botdan foydalanish uchun hoziroq ro'yxatdan o'ting!", reply_markup=register_button)

@r.message(F.text == "/help")
async def process_help(message: Message):
    await message.answer("Agar qandaydir muammoga duch kelsangiz, @beruniyolimpiadasisupport_bot ga yozishingiz mumkin! Biz sizga eng qisqa fursatda javob beramiz!")

@r.message(F.text == "/count")
async def process_count(message: Message):
    await message.answer(f"Botda {len(await get_all_users())} ta foydalanuvchi bor.")