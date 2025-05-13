from asgiref.sync import sync_to_async
from admin_panel.models import *
from datetime import datetime


@sync_to_async(thread_sensitive=True)
def get_this_user(user_id):
    return Users.objects.filter(user_id=user_id).first()


@sync_to_async(thread_sensitive=True)
def registrate_this_user(user_id, username, fullname, phone, province, city, school, school_class):
    return Users.objects.create(user_id=user_id, username=username, fullname=fullname, phone=phone, province=province, city=city, school=school, school_class=school_class)


@sync_to_async(thread_sensitive=True)
def get_all_olympiads():
    all_olympiads = Olympiads.objects.all()
    return all_olympiads

################################################################################
@sync_to_async(thread_sensitive=True)
def get_my_olympiads(user_id):
    user = Users.objects.get(user_id=user_id)
    my_olympiads = user.olympiad_ids.all()
    return my_olympiads


@sync_to_async
def olympiad_start_status(olympiad_id):
    olympiad = Olympiads.objects.get(id=olympiad_id)
    if olympiad.olympiad_start_datetime < datetime.now() and olympiad.olympiad_stop_datetime > datetime.now():
        return "started"
    elif olympiad.olympiad_start_datetime > datetime.now() and olympiad.olympiad_stop_datetime > datetime.now():
        return "not_started"
    elif olympiad.olympiad_stop_datetime < datetime.now():
        return "stopped"
################################################################################


@sync_to_async(thread_sensitive=True)
def get_this_olympiad(olympiad_id=None, id=None):
    if olympiad_id:
        return Olympiads.objects.filter(olympiad_id=olympiad_id).first()
    if id:
        return Olympiads.objects.filter(id=id).first()


@sync_to_async
def get_olympiad_tests(olympiad_id):
    olympiad = Olympiads.objects.get(id=olympiad_id)
    tests = Tests.objects.filter(test_olympiad_name=olympiad.id)
    return tests


@sync_to_async(thread_sensitive=True)
def check_balance_for_olympiad_subscription(user_id, olympiad_id):
    user = Users.objects.get(user_id=user_id)
    olympiad = Olympiads.objects.get(id=olympiad_id)
    if user.balance < olympiad.olympiad_price:
        return False
    else:
        return True
    

@sync_to_async
def add_olympiad_subscription(user_id, olympiad_id):
    user = Users.objects.get(user_id=user_id)
    olympiad = Olympiads.objects.get(id=olympiad_id)
    user.balance -= olympiad.olympiad_price
    user.olympiad_ids.add(olympiad)
    user.save()


@sync_to_async
def user_before_subscribed_olympiad_check(user_id, olympiad_id):
    user = Users.objects.get(user_id=user_id)
    olympiad = Olympiads.objects.get(id=olympiad_id)
    if olympiad in user.olympiad_ids.all():
        return True
    else:
        return False


@sync_to_async(thread_sensitive=True)
def get_my_certificates(user_id):
    my_certificates = Certificates.objects.filter(user_id=user_id)
    return my_certificates




@sync_to_async(thread_sensitive=True)
def get_my_balance(user_id):
    return Users.objects.get(user_id=user_id).balance


@sync_to_async(thread_sensitive=True)
def add_new_payment(user_id, amount):
    return Payments.objects.create(user_id=user_id, amount=amount, datetime=datetime.now())


@sync_to_async(thread_sensitive=True)
def update_my_balance(user_id, amount):
    return Users.objects.filter(user_id=user_id).update(balance=amount)


@sync_to_async(thread_sensitive=True)
def get_all_users():
    return Users.objects.all()


@sync_to_async(thread_sensitive=True)
def save_user_results(user_id, olympiad_name, olympiad_id, olympiad_start_datetime, olympiad_stop_datetime, right_answers_count, wrong_answers_count):
    try:
        Results(
            user_id=user_id,
            olympiad_name=olympiad_name,
            olympiad_id=olympiad_id,
            olympiad_start_datetime=olympiad_start_datetime,
            olympiad_stop_datetime=olympiad_stop_datetime,
            right_answers_count=right_answers_count,
            wrong_answers_count=wrong_answers_count
        ).save()
        return True
    except:
        return False
    

@sync_to_async(thread_sensitive=True)
def user_marked_status(user_id, olympiad_id):
    return Results.objects.filter(user_id=user_id, olympiad_id=olympiad_id).exists()


@sync_to_async(thread_sensitive=True)
def student_age_confirmation(user_id, olympiad_id):
    user = Users.objects.get(user_id=user_id)
    allow_classes = Olympiads.objects.get(id=olympiad_id).allow_classes
    if user.school_class in eval(allow_classes):
        return True
    else:
        return False