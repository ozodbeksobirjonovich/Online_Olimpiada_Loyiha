from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from admin_panel.handlers.router import r
from admin_panel.models import *
from admin_panel.states import *
from admin_panel.keyboards import *
from admin_panel.sms import send_sms
from admin_panel.regions import all_districts
from admin_panel.model_functions import *
from random import randint
import re


@r.message(F.text == "/cancel")
async def process_cancel(message: Message, state: FSMContext):
    await message.answer("❌ Bekor qilindi!")
    await state.clear()


@r.callback_query(F.data == "register")
async def process_register(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("👨‍⚖️ Ism-familiyangizni kiriting...")
    await state.set_state(Registration.fullname)


@r.message(Registration.fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("📞 Telefon raqamingizni yuboring (SMS tasdiqlash kodi yuborish uchun)... (+998901234567)")
    await state.set_state(Registration.phone)


@r.message(Registration.phone)
async def process_phone(message: Message, state: FSMContext):
    if re.match(r"^\+998\d{9}$", message.text):
        await state.update_data(phone=message.text)
        sms_code = randint(1000, 9999)
        await state.update_data(sms_code=sms_code)
        send_sms(message.text, f"Beruniy olimpiadasi uchun tasdiqlash kodi: {sms_code}")
        await message.answer("📩 Siz 4 xonali SMS kod yuborildi. Uni botga kiriting. (Bekor qilish uchun /cancel buyrug'ini yuboring!)")
        await state.set_state(Registration.sms_code)
    else:
        await message.answer("❌ Iltimos telefon raqamni to'g'ri kiriting. (Bekor qilish uchun /cancel buyrug'ini yuboring!)")
        await state.set_state(Registration.phone)


@r.message(Registration.sms_code)
async def process_sms_code(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == str(data["sms_code"]):

        province = ReplyKeyboardBuilder()
        for i in all_districts.keys():
            province.row(types.KeyboardButton(text=i))
        province.adjust(2)

        await message.answer("🚞 Qaysi viloyatda yashaysiz?", reply_markup=province.as_markup(resize_keyboard=True))
        await state.set_state(Registration.province)
    else:
        await message.answer("❌ SMS kod noto'g'ri kiritildi! Qayta ro'yxatdan o'tishingizni so'raymiz!", reply_markup=register_button)
        await state.clear()


@r.message(Registration.province)
async def process_province(message: Message, state: FSMContext):
    await state.update_data(province=message.text)

    districts = ReplyKeyboardBuilder()
    for i in all_districts[message.text]:
        districts.row(types.KeyboardButton(text=i))
    districts.adjust(2)

    await message.answer("🏙 Qaysi tuman/shaharda yashaysiz?", reply_markup=districts.as_markup(resize_keyboard=True))
    await state.set_state(Registration.city)


@r.message(Registration.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("🏫 Nechanchi maktabda o'qiysiz? (raqamda kiriting...)\n\n❌P.s: Yolg'on ma'lumotlarni kiritmang. U sizning olimpiadadan chetlashtirilishingizga olib kelishi mumkin!")
    await state.set_state(Registration.school)


@r.message(Registration.school)
async def process_school(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(school=message.text)
        await message.answer("🏫 Nechanchi sinfda o'qiysiz? (raqamda kiriting...)\n\n❌P.s: Yolg'on ma'lumotlarni kiritmang. U sizning olimpiadadan chetlashtirilishingizga olib kelishi mumkin!")
        await state.set_state(Registration.school_class)
    else:
        await message.answer("❌ Iltimos raqam kiriting. (Bekor qilish uchun /cancel buyrug'ini yuboring!)")
        await state.set_state(Registration.school)


@r.message(Registration.school_class)
async def process_school_class(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(school_class=message.text)
        data = await state.get_data()
        await message.answer(
            f"✅ Sizning ma'lumotlaringiz ✅\n\n"
            f"FIO: {data['fullname']}\n"
            f"Telefon raqam: {data['phone']}\n"
            f"Viloyat: {data['province']}\n"
            f"Tuman: {data['city']}\n"
            f"Maktab: {data['school']}\n"
            f"Sinf: {data['school_class']}\n\n"
            f"Ushbu ma'lumotlar to'g'riligini tasdiqlaysizmi???",
            reply_markup=confirm_registration
        )
        await state.set_state(Registration.confirm_state)
    else:
        await message.answer("❌ Iltimos raqam kiriting. (Bekor qilish uchun /cancel buyrug'ini yuboring!)")
        await state.set_state(Registration.school_class)


@r.callback_query(Registration.confirm_state)
async def process_confirm_state(callback: CallbackQuery, state: FSMContext):
    if callback.data == "confirm_registration":

        data = await state.get_data()

        await registrate_this_user(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            fullname=data["fullname"],
            phone=data["phone"],
            province=data["province"],
            city=data["city"],
            school=data["school"],
            school_class=data["school_class"],
        )

        await callback.message.edit_text("✅ Siz ro'yxatdan o'tdingiz!", reply_markup=student_panel)
        await state.clear()
    elif callback.data == "cancel_registration":
        await callback.message.edit_text("❌ Ro'yxatdan o'tish bekor qilindi!")
        await state.clear()