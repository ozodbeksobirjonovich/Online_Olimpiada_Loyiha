from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    fullname = State()
    phone = State()
    sms_code = State()
    province = State()
    city = State()
    school = State()
    school_class = State()
    confirm_state = State()


class PaymentState(StatesGroup):
    amount = State()


class TestingState(StatesGroup):
    test = State()