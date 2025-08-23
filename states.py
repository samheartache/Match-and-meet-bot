from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    sex = State()
    search_desire = State()
    searched_by = State()
    name = State()
    age = State()
    description = State()
    photo = State()
    city = State()


class Edit(StatesGroup):
    sex = State()
    search_desire = State()
    searched_by = State()
    name = State()
    age = State()
    description = State()
    photo = State()
    city = State()
    reg_again = State()
    delete = State()


class GlobalStates(StatesGroup):
    profile_edit = State()
    menu = State()


class SearchStates(StatesGroup):
    search_profile = State()
    rate_profile = State()
    send_message = State()