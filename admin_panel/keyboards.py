from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

register_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🚀 Ro‘yxatdan o'tish", callback_data="register")]]
)

student_panel = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Barcha olimpiadalar", callback_data="all_olympiads")],
        [InlineKeyboardButton(text="🏆 Mening olimpiadalarim", callback_data="my_olympiads")],
        [InlineKeyboardButton(text="🥇 Mening sertifikatlarim", callback_data="my_certifications")],
        [InlineKeyboardButton(text="💰 Mening balansim", callback_data="my_balance")],
        [InlineKeyboardButton(text="📝 Mening ma'lumotlarim", callback_data="my_profile")]
    ]
)

confirm_registration = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Ha", callback_data="confirm_registration"), InlineKeyboardButton(text="❌ Yo'q", callback_data="cancel_registration")],
    ]
)