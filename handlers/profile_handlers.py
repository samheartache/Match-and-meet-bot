from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import validators
import keyboards.inlines as kb_i
import keyboards.replies as kb_r
from keyboards.builders import choice_keyboard
from states import Register
from handlers.commands import menu, edit_profile

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
        await state.set_state(Register.search_desire)
        await message.answer(text='Чьи анкеты вы хотите смотреть?', reply_markup=kb_r.search_desire)
        return
    else:
        await message.answer(text='Выберите пол корректно', reply_markup=choice_keyboard(['Мужской', 'Женский'], size=(2, 1)))
        return


@router.message(Register.search_desire)
async def handle_search_desire(message: Message, state: FSMContext):
    if validators.search_desire_validate(message.text):
        search_desire = {'Парней': 1, 'Девушек': 2, 'Не важно': 0}.get(message.text)
        await state.update_data(search_desire=search_desire)
        await state.set_state(Register.name)
        await message.answer(text='Введите ваше имя', reply_markup=choice_keyboard(f'{message.from_user.username}'))
    else:
        await message.answer('Выберите корретно', reply_markup=kb_r.search_desire)
        return 


@router.message(Register.name)
async def handle_name(message: Message, state: FSMContext):
    if validators.name_validate(message.text):
        await state.update_data(name=message.text)
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
        await message.answer('Отправьте описание для своего профиля')
    else:
        await message.answer('Введите город корректно')
        return


@router.message(Register.description)
async def handle_description(message: Message, state: FSMContext):
    if validators.description_validate(message.text):
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
        await state.set_state(Register.is_correct)
        await send_profile(message=message, state=state, data=data)
        await message.answer('Все верно?', reply_markup=kb_i.is_profile_correct)
        return
    else:
        await message.answer('Отправьте фото корректно')
        return


async def send_profile(message: Message, state: FSMContext, data):
    await message.answer('Вот ваша анкета: ')
    await message.answer_photo(photo=data['photo'],
                               caption=f'{data['name']}, {data['age']}, {data['city']}\n\n{data['description']}')


@router.callback_query(F.data == 'correct')
async def correct_profile(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await menu(message=callback.message)


@router.callback_query(F.data == 'edit_profile')
async def edit_profile_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await edit_profile(message=callback.message)