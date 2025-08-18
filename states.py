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