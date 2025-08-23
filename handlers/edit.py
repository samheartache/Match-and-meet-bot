from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import validators
from states import Register, Edit, GlobalStates
from keyboards.builders import choice_keyboard
from database import requests
from handlers.commands import send_myprofile, notif_off, notif_on

router = Router()


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
    elif message.text == '🔕 Уведомления о лайках':
        await notif_off(message=message)
    elif message.text == '🔔 Уведомления о лайках':
        await notif_on(message=message)
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
        await send_myprofile(message=message, state=state)
        await message.answer(text='Ваше имя успешно обновлено 🎉')
    elif name == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_myprofile(message=message, state=state)
    else:
        await message.answer('Введите имя корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.age)
async def change_age(message: Message, state: FSMContext):
    age = message.text
    if validators.name_validate(age) and age != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='age', new_value=int(message.text))
        await send_myprofile(message=message, state=state)
        await message.answer(text='Ваш возраст успешно обновлен 🎉')
    elif age == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_myprofile(message=message, state=state)
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
        await send_myprofile(message=message, state=state)
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
        await send_myprofile(message=message, state=state)
    else:
        await message.answer('Выберите корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.searched_by)
async def change_sex(message: Message, state: FSMContext):
    if validators.name_validate(message.text) and message.text != 'Назад':
        searched_by = {'Девушкам': 0, 'Парням': 1, 'Не важно': None}.get(message.text)
        await requests.update_single_property(tg_id=message.from_user.id, property='searched_by', new_value=searched_by)
        await send_myprofile(message=message, state=state)
        await message.answer(text='Ваши настройки успешно обновлены 🎉')
    elif message.text == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_myprofile(message=message, state=state)
    else:
        await message.answer('Выберите корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.city)
async def change_city(message: Message, state: FSMContext):
    city = message.text
    if validators.name_validate(city) and city != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='city', new_value=message.text)
        await send_myprofile(message=message, state=state)
        await message.answer(text='Ваш город успешно обновлен 🎉')
    elif city == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_myprofile(message=message, state=state)
    else:
        await message.answer('Введите город корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.description)
async def change_description(message: Message, state: FSMContext):
    description = message.text
    if validators.name_validate(description) and description != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='description', new_value=message.text)
        await send_myprofile(message=message, state=state)
        await message.answer(text='Ваше описание успешно обновлено 🎉')
    elif description == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_myprofile(message=message, state=state)
    else:
        await message.answer('Введите описание корректно', reply_markup=choice_keyboard('Назад'))
        return


@router.message(Edit.photo)
async def change_photo(message: Message, state: FSMContext):
    photo = message.photo
    if validators.name_validate(photo) and photo != 'Назад':
        await requests.update_single_property(tg_id=message.from_user.id, property='photo', new_value=message.photo[-1].file_id)
        await send_myprofile(message=message, state=state)
        await message.answer(text='Ваше фото успешно обновлено 🎉')
    elif photo == 'Назад':
        await state.set_state(GlobalStates.profile_edit)
        await send_myprofile(message=message, state=state)
    else:
        await message.answer('Отправьте фото корректно', reply_markup=choice_keyboard('Назад'))
        return