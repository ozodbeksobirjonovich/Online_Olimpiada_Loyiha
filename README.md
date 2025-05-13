# Online Olimpiada loyihasi!

Bu loyiha o'quvchilar uchun olimpiadalar o'tkazish va ularni boshqarish imkonini beruvchi Telegram bot va veb-administratsiya paneliga ega tizimdir.

## Imkoniyatlar

- **Telegram Bot**: Foydalanuvchilarni ro'yxatdan o'tkazish va olimpiadalarda qatnashish uchun qulay interfeys
- **Olimpiadalar boshqaruvi**: Olimpiadalarni yaratish, tahrirlash va natijalarni kuzatish
- **To'lov tizimi**: Foydalanuvchilar uchun to'lov tizimi integratsiyasi (Payme va Click orqali)
- **Testlar**: Turli fanlarga oid testlarni qo'shish va boshqarish
- **Sertifikatlar**: Ishtirokchilar uchun sertifikatlar berish imkoniyati
- **Administratsiya paneli**: Django asosidagi boshqaruv paneli

## Texnologiyalar

- **Backend**: Django (Python)
- **Telegram Bot**: Aiogram 3.x
- **Ma'lumotlar bazasi**: SQLite (ishlab chiqarish muhitida MySQL)
- **To'lov tizimlari**: Payme, Click

## O'rnatish

### Talab qilinadigan dasturlar
- Python 3.8+
- pip (Python paket menejeri)
- Virtual muhit yaratish uchun virtualenv yoki venv

### O'rnatish qadamlari

1. Loyiha repozitoriyasini klonlash:
```bash
git clone https://github.com/ozodbeksobirjonovich/Online_Olimpiada_Loyiha.git
cd Online_Olimpiada_Loyiha
```

2. Virtual muhit yaratish va faollashtirish:
```bash
python -m venv venv
# Windows uchun
venv\Scripts\activate
# Linux/Mac uchun
source venv/bin/activate
```

3. Kerakli paketlarni o'rnatish:
```bash
pip install -r requirements.txt
```

4. Muhit o'zgaruvchilarini sozlash:
   `.env.example` faylini `.env` ga nusxalang va quyidagi ma'lumotlarni kiriting:
   ```
   BOT_TOKEN=your_bot_token
   ADMINS=your_admin_id
   PAYME_TOKEN=your_payme_token
   CLICK_TOKEN=your_click_token
   ```

5. Ma'lumotlar bazasini migratsiya qilish:
```bash
python manage.py migrate
```

6. Admin foydalanuvchini yaratish:
```bash
python manage.py createsuperuser
```

7. Loyihani ishga tushirish:
```bash
# Django serverini ishga tushirish
python manage.py runserver

# Bot ni ishga tushirish (alohida terminalni ochib)
python manage.py runbot
```

## Loyihadan foydalanish

### Administrator sifatida
1. `http://localhost:8000/admin` manzilga kirib, admin panel orqali olimpiadalar, testlar va boshqa ma'lumotlarni boshqaring.
2. Yangi olimpiadalarni qo'shing, mavjudlarini tahrirlang va natijalarni ko'rib chiqing.
3. Foydalanuvchilar va to'lov ma'lumotlarini nazorat qiling.

### Foydalanuvchi sifatida (Telegram bot orqali)
1. Botga `/start` buyrug'ini yuborish orqali ro'yxatdan o'ting.
2. Shaxsiy ma'lumotlaringizni to'ldiring (F.I.O, telefon, viloyat, shahar, maktab va sinf).
3. Mavjud olimpiadalar ro'yxati bilan tanishing va qatnashmoqchi bo'lgan olimpiadani tanlang.
4. To'lovni amalga oshiring va olimpiadada ishtirok eting.
5. Natijalarni ko'rish va sertifikatlarni yuklab olish imkoniyatidan foydalaning.

## Bot buyruqlari

- `/start` - Botni ishga tushirish va ro'yxatdan o'tish
- `/help` - Yordam olish uchun
- `/count` - Botdagi foydalanuvchilar sonini ko'rish

## Litsenziya

Bu loyiha ochiq kodli dastur bo'lib, foydalanish va o'zgartirishlar kiritish mumkin.

## Muallif

**Telegram:** [@ozodbek_sobirjonovich](https://t.me/ozodbek_sobirjonovich)

## Qo'llab-quvvatlash

Agar qandaydir muammolarga duch kelsangiz, loyiha muallifi bilan bog'lanishingiz yoki support botga murojaat qilishingiz mumkin: [@ozodbek_sobirjonovich](https://t.me/ozodbek_sobirjonovich)