from django.db import models
import uuid


class Users(models.Model):
    user_id = models.CharField(max_length=255, verbose_name="User ID")
    username = models.CharField(max_length=255, null=True, verbose_name="Username")
    fullname = models.CharField(max_length=255, verbose_name="To'liq ismi")
    phone = models.CharField(max_length=255, verbose_name="Telefon raqami")
    province = models.CharField(max_length=255, verbose_name="Viloyati")
    city = models.CharField(max_length=255, verbose_name="Shahar/Tumani")
    school = models.IntegerField(verbose_name="Maktab raqami")
    school_class = models.IntegerField(verbose_name="Sinf raqami")
    balance = models.IntegerField(default=0, verbose_name="Balans")
    olympiad_ids = models.ManyToManyField('Olympiads', verbose_name="Olimpiadalar", blank=True)

    def __str__(self):
        return self.fullname
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Payments(models.Model):
    user_id = models.CharField(max_length=255, verbose_name="User ID")
    amount = models.IntegerField(verbose_name="Summa")
    datetime = models.DateTimeField(verbose_name="Sana va vaqti")

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'To\'lov'
        verbose_name_plural = 'To\'lovlar'


class Olympiads(models.Model):
    olympiad_id = models.UUIDField(default=uuid.uuid4, verbose_name="Olimpiada ID")
    olympiad_name = models.CharField(max_length=255, verbose_name="Olimpiada nomi")
    olympiad_description = models.TextField(verbose_name="Olimpiada haqida ma'lumot")
    olympiad_science = models.CharField(max_length=255, verbose_name="Olimpiada fani")
    olympiad_price = models.IntegerField(verbose_name="Olimpiada narxi")
    olympiad_start_datetime = models.DateTimeField(verbose_name="Olimpiada boshlanish vaqti")
    olympiad_duration_minutes = models.IntegerField(verbose_name="Olimpiada davomiyligi")
    olympiad_stop_datetime = models.DateTimeField(verbose_name="Olimpiada tugash vaqti")
    allow_classes = models.CharField(max_length=255, verbose_name="Qaysi sinflar qatnasha olishadi??? (Misol uchun [1, 2, 3])")

    def __str__(self):
        return self.olympiad_name
    
    class Meta:
        db_table = 'olympiads'
        verbose_name = 'Olimpiada'
        verbose_name_plural = 'Olimpiadalar'


class Tests(models.Model):
    test_olympiad_name = models.ForeignKey('Olympiads', on_delete=models.CASCADE, verbose_name="Olimpiada nomi")
    test_question = models.TextField(verbose_name="Savol")
    test_variant_1 = models.CharField(max_length=255, verbose_name="Variant 1")
    test_variant_2 = models.CharField(max_length=255, verbose_name="Variant 2")
    test_variant_3 = models.CharField(max_length=255, verbose_name="Variant 3")
    test_variant_4 = models.CharField(max_length=255, verbose_name="Variant 4")
    test_correct_variant = models.CharField(max_length=255, verbose_name="To'g'ri javob (to'liq)")

    def __str__(self):
        return self.test_olympiad_name.olympiad_name


    class Meta:
        db_table = 'tests'
        verbose_name = 'Test'
        verbose_name_plural = 'Testlar'


class Results(models.Model):
    user_id = models.CharField(max_length=255, verbose_name="User ID")
    olympiad_id = models.IntegerField(verbose_name="Olimpiada ID")
    olympiad_name = models.CharField(max_length=255, verbose_name="Olimpiada nomi")
    olympiad_start_datetime = models.DateTimeField(verbose_name="Olimpiada boshlanish vaqti")
    olympiad_stop_datetime = models.DateTimeField(verbose_name="Olimpiada tugash vaqti")
    right_answers_count = models.IntegerField(verbose_name="To'g'ri javoblar soni")
    wrong_answers_count = models.IntegerField(verbose_name="Xato javoblar soni")

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = 'results'
        verbose_name = 'Natija'
        verbose_name_plural = 'Natijalar'


class Certificates(models.Model):
    user_id = models.CharField(max_length=255, verbose_name="User ID")
    fullname = models.CharField(max_length=255, verbose_name="Foydalanuvchi to'liq ismi")
    olympiad_name = models.ForeignKey(Olympiads, on_delete=models.CASCADE, verbose_name="Olimpiada nomi")
    created_at = models.DateTimeField(verbose_name="Sana va vaqti")

    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = 'certificates'
        verbose_name = 'Sertifikat'
        verbose_name_plural = 'Sertifikatlar'