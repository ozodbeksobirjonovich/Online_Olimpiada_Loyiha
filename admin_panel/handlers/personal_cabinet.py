from aiogram import F
from aiogram.types import (
    LabeledPrice,
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    PreCheckoutQuery,
    ContentType
)
from aiogram.fsm.context import FSMContext
from admin_panel.handlers.router import r
from admin_panel.models import *
from admin_panel.states import *
from admin_panel.config import *
from admin_panel.keyboards import *
from admin_panel.model_functions import *
import asyncio
from datetime import timedelta, datetime

tempdata = {}

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
@r.callback_query(F.data == "all_olympiads")
async def process_all_olympiads(callback: CallbackQuery):
    await callback.answer()
    all_olympiads = await get_all_olympiads()
    if all_olympiads:
        for olympiad in all_olympiads:
            if await user_before_subscribed_olympiad_check(callback.from_user.id, olympiad.id):
                await callback.message.answer(f"""❌ Siz allaqachon "{olympiad.olympiad_name}" olimpiadasiga obuna bo'lgansiz!""")
            else:
                olympiad_button = InlineKeyboardMarkup(
                    inline_keyboard=[[InlineKeyboardButton(text="✔ Obuna bo'lish", callback_data="olympiad_join_" + str(olympiad.id))]]
                )
                await callback.message.answer(
                    f"🎯 Olimpiada IDsi: {olympiad.id}\n"
                    f"🏆 Olimpiada nomi: {olympiad.olympiad_name}\n"
                    f"📚 Olimpiada fani: {olympiad.olympiad_science}\n"
                    f"""👨‍⚖️ Olimpiadaga qatnashuvchilar: {", ".join([f"{i}-sinf" for i in eval(olympiad.allow_classes)])}\n"""
                    f"📆 Boshlanish sanasi: {olympiad.olympiad_start_datetime}\n"
                    f"📆 Tugash sanasi: {olympiad.olympiad_stop_datetime}\n"
                    f"💰 Olimpiada narxi: {olympiad.olympiad_price} so'm\n"
                    f"📝 Olimpiada haqida: {olympiad.olympiad_description}\n",
                    reply_markup=olympiad_button
                )
    else:
        await callback.message.answer("🙁 Hozircha faol olimpiadalar yo'q!")


@r.callback_query(F.data.startswith("olympiad_join_"))
async def process_olympiad_join(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    olympiad_id = int(callback.data.split("_")[2])

    if await student_age_confirmation(callback.from_user.id, olympiad_id):
        if await check_balance_for_olympiad_subscription(callback.from_user.id, olympiad_id):
            subscribe_check_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="✅ Ha", callback_data="olympiad_subscribe_" + str(olympiad_id)),
                        InlineKeyboardButton(text="❌ Yo'q", callback_data="cancel_olympiad_subscribe")
                    ]
                ]
            )
            await callback.message.answer("❓ Ushbu olimpiadaga obuna bo'lsangiz, olimpiadaga qatnashish summasi balansingizdan yechib olinadi! Rozimisiz???", reply_markup=subscribe_check_button)
        else:
            await callback.message.answer("❌ Hisobingizda yetarli mablag' mavjud emas!")
    else:
        await callback.message.answer("❌ Siz ushbu olimpiadaga qatnasha olmaysiz. Chunki ushbu olimpiada uchun ruxsat berilgan yoshda emassiz!")

@r.callback_query(F.data == "cancel_olympiad_subscribe")
async def process_cancel_olympiad_subscribe(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("❌ Obuna bekor qilindi!")


@r.callback_query(F.data.startswith("olympiad_subscribe_"))
async def process_olympiad_subscribe(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    olympiad_id = int(callback.data.split("_")[2])
    await add_olympiad_subscription(callback.from_user.id, olympiad_id)
    await callback.message.delete()
    await callback.message.answer("✅ Tabriklaymiz. Siz ushbu olimpiadaga obuna bo'ldingiz!", reply_markup=student_panel)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
@r.callback_query(F.data == "my_olympiads")
async def process_my_olympiads(callback: CallbackQuery):
    await callback.answer()
    my_olympiads = await get_my_olympiads(callback.from_user.id)
    if my_olympiads:
        for olympiad in my_olympiads:
            olympiad_button = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="▶ Boshlash", callback_data="olympiad_start_" + str(olympiad.id))]]
            )

            await callback.message.answer(
                f"🎯 Olimpiada IDsi: {olympiad.id}\n"
                f"🏆 Olimpiada nomi: {olympiad.olympiad_name}\n"
                f"📚 Olimpiada fani: {olympiad.olympiad_science}\n"
                f"📆 Boshlanish sanasi: {olympiad.olympiad_start_datetime}\n"
                f"📆 Tugash sanasi: {olympiad.olympiad_stop_datetime}\n"
                f"💰 Olimpiada narxi: {olympiad.olympiad_price} so'm\n"
                f"📝 Olimpiada haqida: {olympiad.olympiad_description}\n",
                reply_markup=olympiad_button
            )
    else:
        await callback.message.answer("🙁 Mening olimpiadalarim mavjud emas!")


@r.callback_query(F.data.startswith("olympiad_start_"))
async def process_olympiad_start(callback: CallbackQuery):
    await callback.answer()

    if await user_marked_status(callback.from_user.id, callback.data.split("_")[2]):
        await callback.message.answer("❌ Siz bu olimpiadaga qatnashib bo'lgansiz!")
    else:
        olympiad_id = int(callback.data.split("_")[2])
        olympiad = await get_this_olympiad(id=olympiad_id)
        olympiad_status = await olympiad_start_status(olympiad_id)

        if olympiad_status == "started":
            duration = olympiad.olympiad_duration_minutes
            olympiad_start_buttons = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="✅ Tasdiqlayman", callback_data="olympiad_play_" + str(olympiad.id))]]
            )
            await callback.message.answer(f"📢 Shartlar:\n\n1. Testlarni tarqatish ta'qiqlanadi!\n2. Testlarni o'zingiz (birovning yordamisiz) ishlang.\n3. Chalg'itadigan savollardan ehtiyot bo'ling.\n7. Yaxshi o'ylab, so'ng belgilang.\n\n✅ Olimpiada boshlanganidan keyin, belgilangan vaqt ichida uni ishlashingiz shart. Aks holda belgilamagan testlaringiz uchun ball hisoblanmaydi.\n\nOlimpiada boshlashni tasdiqlaysizmi!", reply_markup=olympiad_start_buttons)
        elif olympiad_status == "not_started":
            await callback.message.answer("❌ Olimpiada hali boshlanmagan!")
        elif olympiad_status == "stopped":
            await callback.message.answer("❌ Olimpiada tugallangan!")


@r.callback_query(F.data.startswith("olympiad_play_"))
async def process_olympiad_play(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    olympiad_id = int(callback.data.split("_")[2])
    tests = await get_olympiad_tests(olympiad_id)
    olympiad = await get_this_olympiad(id=olympiad_id)
    
    tempdata[callback.from_user.id] = {}
    tempdata[callback.from_user.id]["olympiad_id"] = olympiad_id
    tempdata[callback.from_user.id]["olympiad_name"] = olympiad.olympiad_name
    tempdata[callback.from_user.id]["current_index"] = 0
    tempdata[callback.from_user.id]["tests_count"] = len(tests)
    tempdata[callback.from_user.id]["question"] = tests[tempdata[callback.from_user.id]["current_index"]].test_question
    tempdata[callback.from_user.id]["answer"] = tests[tempdata[callback.from_user.id]["current_index"]].test_correct_variant
    tempdata[callback.from_user.id]["variant_1"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_1
    tempdata[callback.from_user.id]["variant_2"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_2
    tempdata[callback.from_user.id]["variant_3"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_3
    tempdata[callback.from_user.id]["variant_4"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_4
    tempdata[callback.from_user.id]["right_answers"] = 0
    tempdata[callback.from_user.id]["wrong_answers"] = 0

    for second in range(3, 0, -1):
        await callback.message.answer(f"Tayyorlaning! {second} soniya qoldi!")
        await asyncio.sleep(1)

    tempdata[callback.from_user.id]["olympiad_start_datetime"] = datetime.now()

    variants = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔵", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_1']}"),
                InlineKeyboardButton(text="🟢", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_2']}"),
                InlineKeyboardButton(text="🟡", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_3']}"),
                InlineKeyboardButton(text="🔴", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_4']}"),
            ]
        ]
    )

    await callback.message.answer(
        f"👨‍⚖️ Telegram FIO: {callback.from_user.full_name if callback.from_user.full_name else 'Mavjud emas!'}\n"
        f"🔑 Telegram ID: {callback.from_user.id}\n"
        f"🎯 Username: {callback.from_user.username if callback.from_user.username else 'Mavjud emas!'}\n\n"
        f"""📢 Savol: {tempdata[callback.from_user.id]['question']}\n\n"""
        f"""🔵 {tempdata[callback.from_user.id]['variant_1']}\n"""
        f"""🟢 {tempdata[callback.from_user.id]['variant_2']}\n"""
        f"""🟡 {tempdata[callback.from_user.id]['variant_3']}\n"""
        f"""🔴 {tempdata[callback.from_user.id]['variant_4']}\n\n"""
        f"⏬ Javobni tanlang! ⏬",
        reply_markup=variants
    )

    await state.set_state(TestingState.test)


@r.callback_query(TestingState.test, F.data.startswith("test@@@@@state@@@@@"))
async def process_test_state(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    tests = await get_olympiad_tests(tempdata[callback.from_user.id]["olympiad_id"])

    if callback.data.split("@@@@@state@@@@@")[1] == tempdata[callback.from_user.id]["answer"]:
        tempdata[callback.from_user.id]["right_answers"] += 1
    else:
        tempdata[callback.from_user.id]["wrong_answers"] += 1

    tempdata[callback.from_user.id]["current_index"] += 1

    if tempdata[callback.from_user.id]["current_index"] < tempdata[callback.from_user.id]["tests_count"]:

        tempdata[callback.from_user.id]["question"] = tests[tempdata[callback.from_user.id]["current_index"]].test_question
        tempdata[callback.from_user.id]["answer"] = tests[tempdata[callback.from_user.id]["current_index"]].test_correct_variant
        tempdata[callback.from_user.id]["variant_1"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_1
        tempdata[callback.from_user.id]["variant_2"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_2
        tempdata[callback.from_user.id]["variant_3"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_3
        tempdata[callback.from_user.id]["variant_4"] = tests[tempdata[callback.from_user.id]["current_index"]].test_variant_4

        variants = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="🔵", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_1']}"),
                    InlineKeyboardButton(text="🟢", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_2']}"),
                    InlineKeyboardButton(text="🟡", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_3']}"),
                    InlineKeyboardButton(text="🔴", callback_data=f"test@@@@@state@@@@@{tempdata[callback.from_user.id]['variant_4']}"),
                ]
            ]
        )

        await callback.message.edit_text(
            f"👨‍⚖️ Telegram FIO: {callback.from_user.full_name if callback.from_user.full_name else 'Mavjud emas!'}\n"
            f"🔑 Telegram ID: {callback.from_user.id}\n"
            f"🎯 Username: {callback.from_user.username if callback.from_user.username else 'Mavjud emas!'}\n\n"
            f"""📢 Savol: {tempdata[callback.from_user.id]['question']}\n\n"""
            f"""🔵 {tempdata[callback.from_user.id]['variant_1']}\n"""
            f"""🟢 {tempdata[callback.from_user.id]['variant_2']}\n"""
            f"""🟡 {tempdata[callback.from_user.id]['variant_3']}\n"""
            f"""🔴 {tempdata[callback.from_user.id]['variant_4']}\n\n"""
            f"⏬ Javobni tanlang! ⏬",
            reply_markup=variants
        )

        await state.set_state(TestingState.test)

    else:

        tempdata[callback.from_user.id]["olympiad_stop_datetime"] = datetime.now()
        await callback.message.delete()

        if await save_user_results(
            user_id=callback.from_user.id,
            right_answers_count=tempdata[callback.from_user.id]["right_answers"],
            wrong_answers_count=tempdata[callback.from_user.id]["wrong_answers"],
            olympiad_name=tempdata[callback.from_user.id]["olympiad_name"],
            olympiad_id=tempdata[callback.from_user.id]["olympiad_id"],
            olympiad_start_datetime=tempdata[callback.from_user.id]["olympiad_start_datetime"],
            olympiad_stop_datetime=tempdata[callback.from_user.id]["olympiad_stop_datetime"],
        ):
            await callback.message.answer(
                f"✅ Tabriklaymiz. Siz testlarni yakunladingiz! Umumiy natijalarni olimpiada yakunlanganidan so'ng, e'lon qilamiz!\n\n"
                f"✅ To'g'ri javoblar soni: {tempdata[callback.from_user.id]['right_answers']}\n"
                f"❌ Noto'g'ri javoblar soni: {tempdata[callback.from_user.id]['wrong_answers']}",
                reply_markup=student_panel
            )
            del tempdata[callback.from_user.id]
            await state.clear()
        else:
            await callback.message.answer("❌ Testlar bazasida xatolik yuz berdi. Iltimos qaytadan urinib ko'ring!")
            await state.clear()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
@r.callback_query(F.data == "my_certifications")
async def process_my_certifications(callback: CallbackQuery):
    await callback.answer()
    my_certificates = await get_my_certificates(callback.from_user.id)
    if my_certificates:
        for certificate in my_certificates:
            certificate_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔽 Yuklab olish", callback_data="certificate_info_" + str(certificate.id))]
                ]
            )
            await callback.answer(
                f"🎯 Sertifikat IDsi: {certificate.user_id}\n"
                f"👤 Sertifikat egasi: {certificate.fullname}\n"
                f"🏆 Olimpiada nomi: {certificate.olympiad_name}\n"
                f"🕑 Berilgan muddati: {certificate.created_at}",
                reply_markup=certificate_button
            )
    else:
        await callback.message.answer("🙁 Mening sertifikatlarim hozircha mavjud emas!")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
@r.callback_query(F.data == "my_balance")
async def process_my_balance(callback: CallbackQuery):
    await callback.answer()
    balance = await get_my_balance(callback.from_user.id)
    fill_balance_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💰 To'lov qilish", callback_data="fill_balance")],
        ]
    )
    await callback.message.answer(f"🏦 Sizning balansingiz: {balance} so'm", reply_markup=fill_balance_button)


@r.callback_query(F.data == "fill_balance")
async def process_fill_balance(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("💰 To'lov qilmoqchi bo'lgan summani kiriting: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(PaymentState.amount)


@r.message(PaymentState.amount)
async def process_amount(message: Message, state: FSMContext):
    await state.update_data(amount=message.text)

    await message.answer(f"Agar to'lovni bot orqali amalga oshira olmasangiz, {message.text} miqdoridagi summani quyidagi karta raqamiga amalga oshiring va @beruniyolimpiadasisupport_bot ga botdagi ma'lumotlaringizni hamda chekni skrinshot qilib yuboring!\n\nKarta raqami: 8600 0529 0657 1284\nKarta egasi: Rustam Xayitov!")
    
    await message.answer_invoice(
        title="Payme orqali to'lov",
        description="Olimpiada uchun to'lovlarni amalga oshirish!",
        currency="UZS",
        payload=str(uuid.uuid4()),
        provider_token=payme_token,
        product_start_parameter="time-machine-example",
        prices=[LabeledPrice(label="To'lov", amount=int(message.text) * 100)],
    )
    await state.clear()


@r.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery) -> None:
    await pre_checkout_q.answer(ok=True)


@r.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message) -> None:
    await message.answer(
        f"✅ To'lov muvaffaqiyatli o'tdi\n\n"
        f"💰 To'lov miqdori: {message.successful_payment.total_amount / 100} so'm\n"
        f"💳 To'lov turi: {message.successful_payment.currency}\n"
    )
    await add_new_payment(message.from_user.id, message.successful_payment.total_amount / 100)
    await update_my_balance(message.from_user.id, message.successful_payment.total_amount / 100)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
@r.callback_query(F.data == "my_profile")
async def process_my_profile(callback: CallbackQuery):
    await callback.answer()
    user = await get_this_user(callback.from_user.id)
    await callback.message.answer(
        f"👤 ID: {user.user_id}\n"
        f"👤 Username: @{user.username if user.username else 'Mavjud emas'}\n"
        f"👤 Ism-familiya: {user.fullname}\n"
        f"📞 Telefon-raqamim: {user.phone}\n"
        f"🏙 Viloyat: {user.province}\n"
        f"🏢 Tuman: {user.city}\n"
        f"🏛 Maktab: {user.school}\n"
        f"🏫 Sinf: {user.school_class}"
    )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#