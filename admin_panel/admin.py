from django.forms import CheckboxSelectMultiple
from django.contrib import admin
from unfold.admin import ModelAdmin
from django.db import models as dmodels
from . import models
  

@admin.register(models.Users)
class UsersAdmin(ModelAdmin):
    formfield_overrides = {
        dmodels.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    list_display = ('user_id', 'fullname', 'phone', 'school', 'school_class', 'balance')


@admin.register(models.Payments)
class PaymentsAdmin(ModelAdmin):
    list_display = ('user_id', 'amount', 'datetime')


@admin.register(models.Olympiads)
class OlympiadsAdmin(ModelAdmin):
    list_display = ('olympiad_name', 'olympiad_science', 'olympiad_price', 'olympiad_start_datetime', 'olympiad_duration_minutes', 'olympiad_stop_datetime')


@admin.register(models.Tests)
class TestsAdmin(ModelAdmin):
    list_display = ('test_olympiad_name', 'test_question', 'test_correct_variant')


@admin.register(models.Results)
class ResultsAdmin(ModelAdmin):
    list_display = ('user_id', 'olympiad_name', 'right_answers_count', 'wrong_answers_count')


@admin.register(models.Certificates)
class CertificatesAdmin(ModelAdmin):
    list_display = ('user_id', 'fullname', 'olympiad_name', 'created_at')