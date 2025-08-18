from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import validators
import messages
import keyboards.replies as kb_r
from keyboards.builders import choice_keyboard
from states import Register, Edit, GlobalStates
from utils import profile_template
from database import requests

router = Router()


@router.callback_query(F.data == 'signup')
async def start_signup(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.set_state(Register.sex)
    await callback.message.answer(text='Введите ваш пол', reply_markup=choice_keyboard(['Мужской', 'Женский'], size=(2, 1)))


@router.message(Register.sex)
async def handle_sex(message: Message, state: FSMContext):
    if validators.sex_validate(data=message.text):
        sex = 1 if message.text == 'Мужской' else 0
        await state.update_data(sex=sex)
        await state.update_data(tg_id=message.from_user.id)
        await state.set_state(Register.search_desire)
        await message.answer(text='Чьи анкеты вы хотите смотреть?', reply_markup=kb_r.search_desire)
        return
    else:
        await message.answer(text='Выберите пол корректно', reply_markup=choice_keyboard(['Мужской', 'Женский'], size=(2, 1)))
        return


@router.message(Register.search_desire)
async def handle_search_desire(message: Message, state: FSMContext):
    if validators.search_desire_validate(message.text):
        search_desire = {'Парней': 1, 'Девушек': 0, 'Не важно': None}.get(message.text)
        await state.update_data(search_desire=search_desire)
        await state.set_state(Register.searched_by)
        await message.answer(text='Кому отображать вашу анкету?', reply_markup=kb_r.searched_by)
    else:
        await message.answer('Выберите корретно', reply_markup=kb_r.search_desire)
        return 


@router.message(Register.searched_by)
async def handle_searched_by(message: Message, state: FSMContext):
    if validators.searched_by_validate(message.text):
        searched_by = {'Девушкам': 0, 'Парням': 1, 'Не важно': None}.get(message.text)
        await state.update_data(searched_by=searched_by)
        await state.set_state(Register.name)
        await message.answer(text='Введите ваше имя', reply_markup=choice_keyboard(f'{message.from_user.username}'))
    else:
        await message.answer('Выберите корретно', reply_markup=kb_r.search_desire)
        return 


@router.message(Register.name)
async def handle_name(message: Message, state: FSMContext):
    if validators.name_validate(message.text):
        await state.update_data(username=message.text)
        await state.set_state(Register.age)
        await message.answer('Введите ваш возраст')
    else:
        await message.answer('Введите имя корректно', reply_markup=choice_keyboard(f'{message.from_user.username}'))
        return


@router.message(Register.age)
async def handle_age(message: Message, state: FSMContext):
    if validators.age_validate(message.text):
        await state.update_data(age=int(message.text))
        await state.set_state(Register.city)
        await message.answer('Введите город')
    else:
        await message.answer('Введите возраст корректно')
        return


@router.message(Register.city)
async def handle_city(message: Message, state: FSMContext):
    if validators.city_validate(message.text):
        await state.update_data(city=message.text)
        await state.set_state(Register.description)
        await message.answer('Отправьте описание для своего профиля', reply_markup=choice_keyboard('❌ Не указывать'))
    else:
        await message.answer('Введите город корректно')
        return


@router.message(Register.description)
async def handle_description(message: Message, state: FSMContext):
    if validators.description_validate(message.text):
        if message.text == '❌ Не указывать':
            await state.update_data(description=None)
        else:
            await state.update_data(description=message.text)
        await state.set_state(Register.photo)
        await message.answer('Отправьте фото для своей анкеты')
    else:
        await message.answer('Отправьте описание корректно')
        return


@router.message(Register.photo)
async def handle_photo(message: Message, state: FSMContext):
    if validators.photo_validate(message.photo):
        photo = message.photo[-1].file_id
        await state.update_data(photo=photo)
        data = await state.get_data()
        await requests.insert_user(user_data=data, tg_id=message.from_user.id)
        await send_profile(message=message, state=state, after_register=True)
        await message.answer(text=messages.FINISH_REGISTER, reply_markup=kb_r.menu_keyboard)
        await state.clear()
        return
    else:
        await message.answer('Отправьте фото корректно')
        return


@router.message(F.text == '👤 Моя анкета')
async def send_profile(message: Message, state: FSMContext, after_register=False):
    await state.set_state(GlobalStates.profile_edit)
    await message.answer('Вот ваша анкета: ')
    user = await requests.select_user_profile(tg_id=message.from_user.id)
    if not after_register:
        if user.description:
            await message.answer_photo(
            photo=user.photo, caption=profile_template(username=user.username, age=user.age, city=user.city,\
            description=user.description, sex=user.sex, search_desire=user.search_desire, searched_by=user.searched_by)
            , reply_markup=kb_r.profile_keyboard)
    else:
        await message.answer_photo(
            photo=user.photo, caption=profile_template(username=user.username, age=user.age, city=user.city,\
            description=user.description, sex=user.sex, search_desire=user.search_desire, searched_by=user.searched_by)
            )


@router.message(GlobalStates.profile_edit)
async def profile_edit(message: Message, state: FSMContext):
    if message.text == '⭐️ Изменить имя':
        await message.answer('Введите новое имя', reply_markup=choice_keyboard('Назад'))
        await state.set_state(Edit.name)
    elif message.text == '🎂 Изменить возраст':
        await message.answer('Введите новый возраст', reply_markup=choice_keyboard('Назад'))
        await state.set_state(Edit.age) 
    elif message.text == '🚹 Выбрать пол':
        await message.answer('Введите ваш пол', reply_markup=choice_keyboard(['Мужской', 'Женский', 'Назад'], size=(2, 3)))
        await state.set_state(Edit.sex)
    elif message.text == '🏙️ Изменить город':
        await message.answer('Введите новый город', reply_markup=choice_keyboard('Назад'))
        await state.set_state(Edit.city)
    elif message.text == '📄 Изменить описание':
        await message.answer('Введите новое описание', reply_markup=choice_keyboard('Назад'))
        await state.set_state(Edit.description)
    elif message.text == '📷 Изменить фото':
        await message.answer('Отправьте новое фото', reply_markup=choice_keyboard('Назад'))
        await state.set_state(Edit.photo)
    elif message.text == '📝 Заполнить анкету заново':
        await state.set_state(Register.sex)
        await message.answer(text='Введите ваш пол', reply_markup=choice_keyboard(['Мужской', 'Женский'], size=(2, 1)))
    elif message.text == 'Назад в меню':
        from handlers.commands import help

        await help(message=message, state=state)
    else:
        await message.answer('Нет такого варианта ответа')
        return


@router.message(Edit.name)
async def change_name(message: Message, state: FSMContext):
    name = message.text
    if validators.name_validate(name) and name != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='username', new_value=message.text)
        await send_profile(message=message, state=state)
        await message.answer(text='Ваше имя успешно обновлено 🎉')
    elif name == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Введите имя корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.age)
async def change_age(message: Message, state: FSMContext):
    age = message.text
    if validators.name_validate(age) and age != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='age', new_value=int(message.text))
        await send_profile(message=message, state=state)
        await message.answer(text='Ваш возраст успешно обновлен 🎉')
    elif age == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Введите возраст корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.sex)
async def change_sex(message: Message, state: FSMContext):
    if validators.sex_validate(message.text) and message.text != 'Назад':
        sex = {'Мужской': 1, 'Женский': 0}.get(message.text)
        await requests.update_single_property(tg_id=message.from_user.id, property='sex', new_value=sex)
        await state.set_state(Edit.search_desire)
        await message.answer(text='Кого вы хотите искать?', reply_markup=choice_keyboard(['Парней', 'Девушек', 'Не важно', 'Назад'], size=(3, 1)))
    elif message.text == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Введите пол корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.search_desire)
async def change_sex(message: Message, state: FSMContext):
    if validators.search_desire_validate(message.text) and message.text != 'Назад':
        search_desire = {'Парней': 1, 'Девушек': 0, 'Не важно': None}.get(message.text)
        await requests.update_single_property(tg_id=message.from_user.id, property='search_desire', new_value=search_desire)
        await state.set_state(Edit.searched_by)
        await message.answer(text='Кому отображать вашу анкету?', reply_markup=choice_keyboard(['Парням', 'Девушкам', 'Не важно', 'Назад'], size=(3, 1)))
    elif message.text == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Выберите корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.searched_by)
async def change_sex(message: Message, state: FSMContext):
    if validators.name_validate(message.text) and message.text != 'Назад':
        searched_by = {'Девушкам': 0, 'Парням': 1, 'Не важно': None}.get(message.text)
        await requests.update_single_property(tg_id=message.from_user.id, property='searched_by', new_value=searched_by)
        await send_profile(message=message, state=state)
        await message.answer(text='Ваши настройки успешно обновлены 🎉')
    elif message.text == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Выберите корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.city)
async def change_city(message: Message, state: FSMContext):
    city = message.text
    if validators.name_validate(city) and city != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='city', new_value=message.text)
        await send_profile(message=message, state=state)
        await message.answer(text='Ваш город успешно обновлен 🎉')
    elif city == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Введите город корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.description)
async def change_description(message: Message, state: FSMContext):
    description = message.text
    if validators.name_validate(description) and description != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='description', new_value=message.text)
        await send_profile(message=message, state=state)
        await message.answer(text='Ваше описание успешно обновлено 🎉')
    elif description == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Введите описание корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.photo)
async def change_photo(message: Message, state: FSMContext):
    photo = message.photo
    if validators.name_validate(photo) and photo != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='photo', new_value=message.photo[-1].file_id)
        await send_profile(message=message, state=state)
        await message.answer(text='Ваше фото успешно обновлено 🎉')
    elif photo == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_profile(message=message, state=state)
    else:
        await message.answer('Отправьте фото корректно', reply_markup=choice_keyboard('Назад'))
        return